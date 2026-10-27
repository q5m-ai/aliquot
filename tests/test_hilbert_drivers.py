"""Bounded local driver regressions and separately labelled published evidence."""

import hashlib
import json
from math import gcd, isqrt, prod
from pathlib import Path
import unittest

from aliquot import aliquot_sum
from aliquot.hilbert import address, base_four
from aliquot.two_adic import _divisor_pair_sum, valuation_two

ROOT = Path(__file__).resolve().parents[1]
SEEDS = (276, 552, 564, 660, 966, 138, 318)


def is_prime_by_division(n):
    """Independent exact primality check for LOCAL certificates only."""
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    return all(n % d and n % (d + 2) for d in range(5, isqrt(n) + 1, 6))


class HilbertDriverTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        text = (ROOT / "site/length-data.js").read_text()
        cls.local = json.loads(text[text.index("{"):text.rindex("}") + 1])
        cls.rows = {int(row["seed"]): row for row in cls.local["orbits"]}
        cls.edges = {int(edge["from"]): edge for edge in cls.local["edges"]}
        cls.paths = {}
        for seed in SEEDS:
            path = [seed]
            for _ in range(cls.rows[seed]["steps"]):
                path.append(int(cls.edges[path[-1]]["to"]))
            cls.paths[seed] = path
        cls.note = (ROOT / "research/HILBERT-DRIVERS.md").read_text()
        # Never feed these published-only terms to the local certificate checker.
        cls.published = json.loads(
            (ROOT / "research/results/lehmer-276-published-prefix.json").read_text())

    def test_driver_examples_need_not_be_perfect(self):
        for core, multiplier in ((6, 2), (28, 2), (120, 3), (496, 2),
                                 (672, 3), (523776, 3)):
            proper = _divisor_pair_sum(core)
            self.assertEqual(aliquot_sum(core), proper)
            self.assertEqual(proper, (multiplier - 1) * core)
            self.assertIn(f"| {core} | {proper + core} | {proper} | {multiplier} |", self.note)

    def test_coprime_core_identity_does_not_license_reuse_after_overlap(self):
        for core, multiplier in ((6, 2), (28, 2), (120, 3), (496, 2),
                                 (672, 3), (523776, 3)):
            for u in range(1, 40):
                if gcd(core, u) != 1:
                    continue
                successor = _divisor_pair_sum(core * u)
                expected = core * (multiplier * (_divisor_pair_sum(u) + u) - u)
                self.assertEqual(successor, expected)
                self.assertEqual(aliquot_sum(core * u), successor)
                if u > 1:
                    self.assertGreater(successor, core * u)
        self.assertEqual((_divisor_pair_sum(120), _divisor_pair_sum(240)), (240, 504))
        self.assertNotEqual(gcd(120, 240 // 120), 1)
        self.assertEqual(120 * (3 * (_divisor_pair_sum(2) + 2) - 2), 840)
        self.assertNotEqual(504, 840)

    def test_selected_local_edges_have_independent_exact_certificates(self):
        sources = {n for path in self.paths.values() for n in path[:-1]}
        primes = {int(p) for n in sources for p, _ in self.edges[n]["factors"]}
        self.assertTrue(all(is_prime_by_division(p) for p in primes))
        for n in sources:
            factors = [(int(p), e) for p, e in self.edges[n]["factors"]]
            self.assertEqual([p for p, _ in factors], sorted({p for p, _ in factors}))
            self.assertTrue(all(type(e) is int and e > 0 for _, e in factors))
            self.assertEqual(prod(p ** e for p, e in factors), n)
            divisors = [1]
            for p, e in factors:
                divisors = [d * p ** j for d in divisors for j in range(e + 1)]
            self.assertEqual(sum(d for d in divisors if d < n), int(self.edges[n]["to"]), n)

    def test_local_summary_reproduces_without_extending_any_orbit(self):
        expected = {
            276: (79, 0, 71, "factorization_limit"),
            552: (84, 0, 58, "factorization_limit"),
            564: (115, 32, 5, "factorization_limit"),
            660: (116, 37, 4, "factorization_limit"),
            966: (94, 28, 56, "factorization_limit"),
            138: (178, 22, 0, "terminated"),
            318: (35, 21, 0, "terminated"),
        }
        self.assertEqual(self.local["limits"]["max_steps"], 256)
        self.assertEqual(self.local["limits"]["max_source"], str(10 ** 30))
        self.assertEqual(self.local["limits"]["max_work"], 2_000_000)
        for seed, (steps, c6, c28, status) in expected.items():
            path = self.paths[seed]
            sources = path[:-1]
            self.assertEqual(len(sources), steps)
            self.assertEqual(len(set(path)), len(path))
            self.assertTrue(all(0 < n <= 10 ** 30 for n in sources))
            self.assertEqual(str(path[-1]), self.rows[seed]["end"])
            self.assertEqual(sum(n % 12 == 6 for n in sources), c6)
            self.assertEqual(sum(n % 56 == 28 for n in sources), c28)
            self.assertEqual(self.rows[seed]["status"], status)
            self.assertEqual({address(n).state for n in sources}, {"I", "S", "C", "T"})
            self.assertIn(f"| {seed} | {steps} | {c6} | {c28} | {status} |", self.note)
            if status == "factorization_limit":
                self.assertNotIn(path[-1], self.edges)
                self.assertEqual(self.rows[seed]["lower_bound"], steps + 1)
            else:
                self.assertEqual(path[-1], 0)
                self.assertEqual(self.rows[seed]["lower_bound"], steps)

    def test_local_276_driver_phase_is_censored_not_permanent(self):
        path = self.paths[276]
        self.assertEqual(path[8:12], [2716, 2772, 5964, 10164])
        self.assertEqual(len(path) - 1 - 8, 71)
        self.assertTrue(all(n % 56 == 28 for n in path[8:]))
        self.assertTrue(all(a < b for a, b in zip(path[8:], path[9:])))
        self.assertEqual(path[-1], 2556878765995204)
        self.assertNotIn(path[-1], self.edges)

    def test_driver_retention_criterion_on_selected_local_edges(self):
        sources = {n for path in self.paths.values() for n in path[:-1] if n % 56 == 28}
        outcomes = set()
        for n in sources:
            edge = self.edges[n]
            factors = {int(p): e for p, e in edge["factors"]}
            sigma_v = prod(sum(p ** j for j in range(e + 1))
                           for p, e in factors.items() if p not in (2, 7))
            retained = factors[7] % 2 == 1 or sigma_v % 8 == 0
            self.assertEqual(int(edge["to"]) % 56 == 28, retained)
            self.assertEqual(int(edge["to"]) % 7, 0)
            self.assertIn(base_four(n)[-2:], ("10", "30"))
            outcomes.add(retained)
        self.assertEqual(outcomes, {False, True})

    def test_published_excerpt_preserves_provenance_and_verification_boundary(self):
        data = self.published
        self.assertEqual(data["schema"], "aliquot-published-driver-excerpt-v1")
        self.assertEqual((data["sequence"], data["seed"]), ("A008892", "276"))
        self.assertEqual((data["index_origin"], data["first_index"], data["last_index"]), (0, 0, 170))
        self.assertEqual(data["continuation_status"], "published_only_not_locally_certified")
        self.assertEqual(data["locally_certified_through_index"], 79)
        self.assertEqual(data["source"]["url"], "https://oeis.org/A008892/b008892.txt")
        self.assertEqual(data["source"]["sha256"],
                         "ec6ddf94fbf2824f1dfeb35e07dd5c2d370e211cd7bdff66116587368a8faf96")
        self.assertEqual(len(data["terms"]), 171)
        for n in data["terms"]:
            self.assertIsInstance(n, str)
            self.assertGreater(int(n), 0)
            self.assertEqual(str(int(n)), n)
        canonical = "".join(f"{i} {n}\n" for i, n in enumerate(data["terms"]))
        self.assertEqual(data["excerpt_sha256"],
                         "0c9d67197f600c7c821b8c6638118b7a082631594b557ba4331b4a3004551e96")
        self.assertEqual(hashlib.sha256(canonical.encode("ascii")).hexdigest(), data["excerpt_sha256"])
        self.assertEqual(list(map(int, data["terms"][:80])), self.paths[276])
        # Remaining values are NOT added to self.edges or called locally certified.
        self.assertGreater(data["last_index"], data["locally_certified_through_index"])

    def test_reported_exit_residues_and_conditional_prime_formula_only(self):
        data = self.published
        terms = list(map(int, data["terms"]))
        self.assertTrue(all(n % 56 == 28 for n in terms[8:170]))
        source, successor = terms[169:171]
        self.assertEqual((valuation_two(source), valuation_two(successor)), (2, 1))
        self.assertIn(base_four(source)[-2:], ("10", "30"))
        self.assertEqual(base_four(successor)[-1], "2")
        self.assertEqual(successor % 7, 0)
        self.assertGreater(successor, source)  # This exit is still a growing step.
        claim = data["exit_factorization"]
        self.assertEqual(claim["index"], 169)
        self.assertEqual(claim["source"]["url"], "https://oeis.org/A008892/a008892.txt")
        self.assertEqual(claim["source"]["sha256"],
                         "48e2c781d9619ca37c76f65f2b61b15e29b2579dc008ed51862e1ac69ca2c727")
        self.assertEqual(claim["large_prime_status"], "reported_by_source_not_independently_certified")
        self.assertIs(claim["independent_large_prime_verification"], False)
        self.assertEqual(claim["reported_factors"],
                         [["2", 2], ["7", 2], ["36558448886730575315885537", 1]])
        p = int(claim["reported_factors"][-1][0])
        self.assertEqual(source, 4 * 7 ** 2 * p)
        self.assertEqual(p % 8, 1)
        self.assertEqual(successor, 203 * p + 399)
        self.assertEqual(valuation_two(57 * (p + 1)), 1)
        # No is_prime/aliquot_sum call on p or the published continuation:
        # the last two identities explain the step IF the reported p is prime.

    def test_small_prime_exit_examples_are_independently_verified(self):
        for p in (5, 13, 17, 29, 37):
            self.assertTrue(is_prime_by_division(p))
            self.assertEqual(p % 4, 1)
            source = 4 * 7 ** 2 * p
            successor = _divisor_pair_sum(source)
            self.assertEqual(aliquot_sum(source), successor)
            self.assertEqual(successor, 203 * p + 399)
            self.assertEqual(source % 56, 28)
            self.assertEqual(valuation_two(successor), 1)
            self.assertGreater(successor, source)
        self.assertEqual(_divisor_pair_sum(980), 1414)
