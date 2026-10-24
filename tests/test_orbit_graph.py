"""Exact forward graph, complete inverse certificates, and browser regressions."""

from collections import Counter
import json
from math import isqrt, prod
from pathlib import Path
import subprocess
import unittest

from aliquot import aliquot_sum
from aliquot.orbit_graph import build_orbit_graph
from aliquot.research import divisor_sieve
from scripts.build_orbit_graph import render

ROOT = Path(__file__).resolve().parents[1]


def divisor_pair_sum(n):
    """Independent of both trial factorization/product and the additive sieve."""
    total = 0
    for d in range(1, isqrt(n) + 1):
        if n % d == 0:
            if d < n:
                total += d
            other = n // d
            if other != d and other < n:
                total += other
    return total


class OrbitGraphTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.graph = build_orbit_graph()
        cls.large_graph = build_orbit_graph(seed_bound=1000, predecessor_bound=1_000_000)
        cls.nodes = {int(n["id"]): n for n in cls.graph["nodes"]}
        cls.ceiling = max(int(n["predecessors"]["ceiling"] or 0) for n in cls.nodes.values())
        cls.inverse = {n: [] for n in cls.nodes if n != 1}
        cls.source_sums = [None]  # s(0) is undefined.
        for m in range(1, cls.ceiling + 1):
            target = divisor_pair_sum(m)
            cls.source_sums.append(target)
            if target in cls.inverse:
                cls.inverse[target].append(str(m))

    def test_generated_public_artifact_is_exactly_reproducible(self):
        artifact = (ROOT / "site/orbit-data.js").read_text()
        self.assertEqual(artifact, render(self.large_graph))
        self.assertEqual((ROOT / "tests/fixtures/orbit-data-100.js").read_text(), render(self.graph))
        parsed = json.loads(artifact.split("const AliquotOrbitData = ", 1)[1].removesuffix(";\n"))
        self.assertEqual(parsed, self.large_graph)
        result = subprocess.run(["python3", "scripts/build_orbit_graph.py", "--check"],
                                cwd=ROOT, capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((ROOT / "site/orbit-data.js").read_text(), artifact)

    def test_all_starts_are_included_and_every_orbit_resolves(self):
        self.assertEqual([o["seed"] for o in self.graph["orbits"]], list(map(str, range(1, 101))))
        self.assertTrue(self.graph["complete_orbits"])
        self.assertEqual(len(self.nodes), 117)
        self.assertEqual(max(self.nodes), 259)
        self.assertEqual(len(self.graph["edges"]), 116)
        self.assertEqual(Counter(o["path"][-1] for o in self.graph["orbits"]), {"0": 96, "6": 3, "28": 1})
        self.assertEqual([o["seed"] for o in self.graph["orbits"] if o["path"][-1] == "6"], ["6", "25", "95"])
        for orbit in self.graph["orbits"]:
            with self.subTest(seed=orbit["seed"]):
                self.assertEqual(orbit["path"][0], orbit["seed"])
                for a, b in zip(orbit["path"], orbit["path"][1:]):
                    self.assertGreater(int(a), 0)
                    self.assertEqual(divisor_pair_sum(int(a)), int(b))
                if orbit["status"] == "cycle":
                    self.assertEqual(orbit["cycle"], [orbit["path"][-1]])
                    self.assertEqual(orbit["path"][-1], orbit["path"][-2])
                else:
                    self.assertEqual(orbit["status"], "terminated")
                    self.assertEqual(orbit["path"][-1], "0")

    def test_edges_factors_and_primality_agree_with_independent_arithmetic(self):
        edges = {int(e["from"]): int(e["to"]) for e in self.graph["edges"]}
        self.assertEqual(len(edges), len(self.graph["edges"]))
        self.assertNotIn(0, edges)
        self.assertIsNone(self.nodes[0]["next"])
        self.assertEqual(edges[1], 0)
        self.assertEqual(edges[6], 6)
        self.assertEqual(edges[28], 28)
        self.assertEqual(sum(n["prime"] for n in self.nodes.values()), 25)
        for n, node in self.nodes.items():
            with self.subTest(n=n):
                self.assertEqual(node["incoming"], [str(m) for m, successor in edges.items() if successor == n])
                self.assertEqual(node["leaf"], not node["incoming"])
                self.assertEqual(node["seed"], 1 <= n <= 100)
                self.assertEqual(node["starts"], [o["seed"] for o in self.graph["orbits"] if str(n) in o["path"]])
                self.assertIsNone(node["unresolved"])
                if n:
                    self.assertEqual(edges[n], divisor_pair_sum(n))
                    self.assertEqual(node["next"], str(edges[n]))
                    self.assertEqual(node["prime"], n > 1 and edges[n] == 1)
                    self.assertEqual(prod(int(f["prime"]) ** f["exponent"] for f in node["factors"]), n)
                    self.assertTrue(all(divisor_pair_sum(int(f["prime"])) == 1 for f in node["factors"]))

    def test_inverse_sieve_matches_every_source_sum_through_the_required_ceiling(self):
        sums = divisor_sieve(int(self.graph["limits"]["predecessor_source_bound"]))
        self.assertEqual(sums[:self.ceiling + 1], self.source_sums)

    def test_every_complete_predecessor_set_matches_all_divisor_pair_sums(self):
        self.assertEqual(self.ceiling, 66564)
        for n, node in self.nodes.items():
            inverse = node["predecessors"]
            with self.subTest(n=n):
                if n == 1:
                    self.assertEqual(inverse, {"status": "infinite", "ceiling": None, "checked_through": None, "values": None})
                    self.assertFalse(node["untouchable"])
                else:
                    self.assertEqual(inverse["status"], "complete")
                    self.assertEqual(inverse["ceiling"], "1" if n == 0 else str((n - 1) ** 2))
                    self.assertEqual(inverse["checked_through"], inverse["ceiling"])
                    self.assertEqual(inverse["values"], self.inverse[n])
                    self.assertEqual(node["untouchable"], n > 0 and not self.inverse[n])

    def test_displayed_leaves_are_distinct_from_proved_untouchables(self):
        self.assertEqual(sum(n["leaf"] for n in self.nodes.values()), 45)
        self.assertEqual([n for n, record in self.nodes.items() if record["untouchable"]], [2, 5, 52, 88, 96])
        self.assertTrue(self.nodes[52]["leaf"])
        self.assertEqual(self.nodes[52]["predecessors"]["checked_through"], "2601")
        self.assertEqual(self.nodes[52]["predecessors"]["values"], [])
        self.assertTrue(self.nodes[12]["leaf"])
        self.assertFalse(self.nodes[12]["untouchable"])
        self.assertEqual(self.nodes[12]["predecessors"]["values"], ["121"])
        self.assertNotIn(121, self.nodes)

    def test_step_source_and_factorization_limits_are_unresolved_not_terminal(self):
        for options, frontier, reason in [({"max_steps": 1}, 42, "step limit"),
                                          ({"max_source": 10}, 12, "source limit"),
                                          ({"max_work": 1}, 4, "factorization work limit")]:
            with self.subTest(options=options):
                data = build_orbit_graph(seed_bound=30, predecessor_bound=100, **options)
                self.assertFalse(data["complete_orbits"])
                node = next(n for n in data["nodes"] if n["id"] == str(frontier))
                self.assertIsNone(node["next"])
                self.assertIsNone(node["prime"])
                self.assertIsNone(node["factors"])
                self.assertEqual(node["unresolved"], reason)
                self.assertTrue(any(o["status"] == "unresolved" and o["path"][-1] == str(frontier) for o in data["orbits"]))

    def test_other_seeds_can_resolve_an_earlier_step_frontier_without_new_arithmetic(self):
        graph = build_orbit_graph(seed_bound=10, max_steps=1, predecessor_bound=100)
        self.assertTrue(graph["complete_orbits"])
        self.assertEqual(graph["orbits"][8]["path"], ["9", "4", "3", "1", "0"])
        self.assertTrue(all(n["unresolved"] is None for n in graph["nodes"]))

    def test_partial_empty_inverse_scan_is_never_a_no_predecessor_certificate(self):
        graph = build_orbit_graph(predecessor_bound=1)
        node = next(n for n in graph["nodes"] if n["id"] == "52")
        self.assertEqual(node["predecessors"], {"status": "partial", "ceiling": "2601", "checked_through": "1", "values": []})
        self.assertFalse(node["untouchable"])

    def test_budgets_are_explicit_bounded_and_validated(self):
        self.assertEqual(self.graph["limits"], {"seed_min": "1", "seed_max": "100", "max_steps": 64,
                                             "max_source": "1000000", "factorization_work": 2000000,
                                             "predecessor_source_bound": "100000"})
        for options in [{"seed_bound": 1001}, {"seed_bound": True}, {"max_steps": 0}, {"max_steps": 257},
                        {"predecessor_bound": 1000001}, {"max_source": 0}, {"max_work": -1}]:
            with self.subTest(options=options), self.assertRaises(ValueError):
                build_orbit_graph(**options)

    def test_browser_graph_and_interaction_regressions(self):
        process = subprocess.run(["node", "--test", "tests/orbits.test.mjs"], cwd=ROOT,
                                 capture_output=True, text=True, timeout=30)
        self.assertEqual(process.returncode, 0, process.stdout + process.stderr)

    def test_browser_live_session_regressions(self):
        process = subprocess.run(["node", "--test", "tests/orbit-session.test.mjs"], cwd=ROOT,
                                 capture_output=True, text=True, timeout=30)
        self.assertEqual(process.returncode, 0, process.stdout + process.stderr)

    def test_live_browser_additions_match_independent_exact_python(self):
        process = subprocess.run(["node", "tests/orbit-session-math.mjs"], cwd=ROOT,
                                 capture_output=True, text=True, timeout=30)
        self.assertEqual(process.returncode, 0, process.stderr)
        data = json.loads(process.stdout)
        nodes = {node["id"]: node for node in data["nodes"]}
        self.assertLessEqual(len(nodes), 500)
        self.assertEqual(data["schema"], "aliquot-orbit-session-v1")
        self.assertEqual(nodes["121"]["predecessors"]["status"], "complete")
        inverse = [str(n) for n in range(1, 14401) if divisor_pair_sum(n) == 121]
        self.assertEqual(nodes["121"]["predecessors"]["values"], inverse)
        for source in inverse:
            self.assertEqual(nodes[source]["next"], "121")
        for edge in data["edges"]:
            source = int(edge["from"])
            self.assertGreater(source, 0)
            # Large smooth sources are verified by the authoritative Python
            # factorization core; smaller sources also get divisor-pair checks.
            self.assertEqual(aliquot_sum(source), int(edge["to"]))
            if source < 1000000:
                self.assertEqual(divisor_pair_sum(source), int(edge["to"]))
        for node in data["nodes"]:
            if node["factors"] is not None and node["id"] != "0":
                self.assertEqual(prod(int(f["prime"]) ** f["exponent"] for f in node["factors"]), int(node["id"]))
                if node.get("sum") is not None:
                    self.assertEqual(aliquot_sum(int(node["id"])), int(node["sum"]))
            self.assertEqual(node["leaf"], not node["incoming"])
            if node["predecessors"]["status"] == "unsearched":
                self.assertFalse(node["untouchable"])
        self.assertIsNone(nodes["0"]["next"])
        self.assertTrue(any(o["seed"] == "220" and o["cycle"] == ["220", "284"] for o in data["orbits"]))
        for orbit in data["orbits"]:
            for source, target in zip(orbit["path"], orbit["path"][1:]):
                self.assertEqual(nodes[source]["next"], target)

    def test_thousand_start_graph_has_exact_edges_honest_frontiers_and_seed_coverage(self):
        data = self.large_graph
        nodes = {n["id"]: n for n in data["nodes"]}
        self.assertEqual(len(nodes), 1665)
        self.assertEqual(len(data["edges"]), 1653)
        self.assertEqual(max(map(int, nodes)), 1895712)
        self.assertEqual([o["seed"] for o in data["orbits"]], list(map(str, range(1, 1001))))
        self.assertEqual(Counter(o["status"] for o in data["orbits"]),
                         {"terminated": 948, "cycle": 22, "unresolved": 30})
        self.assertFalse(data["complete_orbits"])
        self.assertEqual(sum(n["leaf"] for n in nodes.values()), 514)
        self.assertEqual(sum(n["untouchable"] for n in nodes.values()), 89)
        self.assertEqual(nodes["121"]["next"], "12")
        self.assertFalse(nodes["12"]["leaf"])
        for edge in data["edges"]:
            source, target = int(edge["from"]), int(edge["to"])
            self.assertGreater(source, 0)
            self.assertLessEqual(source, 1000000)
            self.assertEqual(divisor_pair_sum(source), target)
            self.assertEqual(aliquot_sum(source), target)
        frontiers = [n for n in nodes.values() if n["unresolved"]]
        self.assertEqual(len(frontiers), 11)
        for node in frontiers:
            self.assertEqual(node["unresolved"], "source limit")
            self.assertGreater(int(node["id"]), 1000000)
            self.assertIsNone(node["next"])
            self.assertIsNone(node["prime"])
            self.assertIsNone(node["factors"])
        for orbit in data["orbits"]:
            for source, target in zip(orbit["path"], orbit["path"][1:]):
                self.assertEqual(nodes[source]["next"], target)
            if orbit["status"] == "unresolved":
                self.assertIsNotNone(nodes[orbit["path"][-1]]["unresolved"])
        for value in range(2, 1001):
            self.assertEqual(nodes[str(value)]["predecessors"]["status"], "complete")
        for node in nodes.values():
            if node["predecessors"]["status"] == "partial":
                self.assertFalse(node["untouchable"])
        sieve = divisor_sieve(1000000)
        for source in list(range(1, 1001)) + [99991, 100000, 999983, 1000000]:
            self.assertEqual(sieve[source], divisor_pair_sum(source))
        inverses = {str(n): [] for n in range(2, 1001)}
        for source in range(1, 1000001):
            if str(sieve[source]) in inverses:
                inverses[str(sieve[source])].append(str(source))
        for target, values in inverses.items():
            self.assertEqual(nodes[target]["predecessors"]["values"], values)

    def test_public_page_keeps_facts_scope_and_navigation_visible(self):
        page = (ROOT / "site/orbits/index.html").read_text()
        for text in ["All starts 1–1,000", "s(0) is undefined", "121 → 12", "2, 5, 52, 88, and 96",
                     "2,601", "1,000,000", "64 steps", "2,000,000", "not a proof", "514 leaves",
                     "80-node", "42 nodes", "left-to-right on every screen", "Show next +16",
                     "known successor is outside the window", "not just this window"]:
            self.assertIn(text, page)
        for name in ["index.html", "reverse/index.html", "research/index.html"]:
            self.assertIn('href="/orbits/"', (ROOT / "site" / name).read_text())
        self.assertNotIn("<aside", page)
        self.assertNotIn("<iframe", page)
        self.assertIn('class="point-details"', page)
        self.assertIn('id="download"', page)
