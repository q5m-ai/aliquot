"""Small exact regressions, not proofs of the all-length mathematical claims."""

from dataclasses import asdict
import json
from math import isqrt
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

from aliquot import ComputationLimit
from aliquot.hilbert import (
    MAX_SOURCE, MAX_STEPS, address, base_four, build_report, checked_sum, trace,
)
from aliquot.two_adic import _divisor_pair_sum, valuation_two

ROOT = Path(__file__).resolve().parents[1]


def independent_hilbert(n, order):
    """Low-to-high rotate/translate algorithm, unlike the production transducer."""
    x = y = 0
    scale = 1
    while scale < 2 ** order:
        rx, ry = (n // 2) & 1, (n ^ (n // 2)) & 1
        if not ry:
            if rx:
                x, y = scale - 1 - x, scale - 1 - y
            x, y = y, x
        x, y = x + scale * rx, y + scale * ry
        n //= 4
        scale *= 2
    return x, y


class HilbertTests(unittest.TestCase):
    def test_domain_padding_and_arbitrary_precision(self):
        for n in (0, 1, 18, 255, 256, 4096, 4 ** 500 + 18):
            word = base_four(n)
            self.assertEqual(len(word) % 2, 0)
            self.assertEqual(int(word, 4), n)
            h = address(n)
            self.assertEqual((h.x, h.y), independent_hilbert(n, len(word)))
            self.assertEqual((h.x, h.y), independent_hilbert(n, len(word) + 2))
            self.assertTrue(all(type(v) is int for v in (h.x, h.y, h.norm_squared)))
        self.assertEqual(base_four(18), "0102")
        self.assertEqual(asdict(address(18)), {"x": 5, "y": 1, "state": "I"})
        for bad in (-1, True, 0.5, "18", None):
            with self.assertRaises(ValueError):
                address(bad)

    def test_independent_coordinates_adjacency_and_state_through_4095(self):
        points = [address(n) for n in range(4096)]
        self.assertEqual(len({(h.x, h.y) for h in points}), 4096)
        state_by_parities = {(0, 0): "I", (1, 0): "S", (0, 1): "T", (1, 1): "C"}
        for n, h in enumerate(points):
            self.assertEqual((h.x, h.y), independent_hilbert(n, 6))
            word = base_four(n)
            self.assertEqual(h.state, state_by_parities[word.count("0") % 2, word.count("3") % 2])
            self.assertEqual((h.x + h.y) % 2, n % 2)
            for r in range(4):
                self.assertEqual(n < 16 ** r, max(h.x, h.y) < 4 ** r)
            if n:
                p = points[n - 1]
                self.assertEqual(abs(h.x - p.x) + abs(h.y - p.y), 1)
        # An odd-order extension is NOT the frozen infinite convention.
        self.assertNotEqual(independent_hilbert(1, 1), independent_hilbert(1, 2))

    def test_geometric_scaling_and_the_arithmetic_correction(self):
        for n in range(1, 65):
            h = address(n)
            a = valuation_two(n)
            odd = n // 2 ** a
            sigma_odd = _divisor_pair_sum(odd) + odd
            epsilon = int(h.state in ("C", "T"))
            for r in range(1, 4):
                scaled = address(16 ** r * n)
                correction = (4 ** r - 1) * epsilon
                self.assertEqual(scaled.state, h.state)
                self.assertEqual((scaled.x, scaled.y),
                                 (4 ** r * h.x + correction, 4 ** r * h.y + correction))
                self.assertEqual(checked_sum(16 ** r * n),
                                 16 ** r * checked_sum(n) + (16 ** r - 1) * sigma_odd)
        # Finite regressions for the all-r norm-growth family in the note.
        for r in range(4):
            t = 4 ** r
            n, successor = 24 * t * t, 40 * t * t - 4
            self.assertEqual(checked_sum(n), successor)
            h, k = address(n), address(successor)
            self.assertEqual((h.state, k.state), ("I", "I"))
            self.assertEqual((h.x, h.y, k.x, k.y), (6 * t, 2 * t, 6 * t, 6 * t - 2))
            self.assertEqual(k.norm_squared - h.norm_squared, 4 * (4 * t - 1) * (2 * t - 1))
            self.assertEqual(base_four(successor), "021" + "3" * (2 * r) + "0")

    def test_same_state_pair_law_below_256_only(self):
        points = [address(n) for n in range(256)]
        for n, h in enumerate(points):
            for m, p in enumerate(points[:n]):
                if h.state == p.state:
                    norm = (h.x - p.x) ** 2 + (h.y - p.y) ** 2
                    self.assertEqual(valuation_two(norm), valuation_two(n - m))
        # The terminal-state qualification cannot be silently omitted.
        a, b = address(1), address(5)
        self.assertNotEqual(a.state, b.state)
        self.assertNotEqual(valuation_two((a.x - b.x) ** 2 + (a.y - b.y) ** 2),
                            valuation_two(5 - 1))

    def test_aliquot_chord_uses_displacement_not_successor_valuation(self):
        # All three branches of v2(sigma(n)-2n), with matching endpoint states.
        for n, successor, a, b, expected in [(2, 1, 1, 0, 0), (38, 22, 1, 2, 4),
                                            (70, 74, 1, 4, 2)]:
            self.assertEqual(checked_sum(n), successor)
            odd = n // 2 ** a
            sigma_odd = _divisor_pair_sum(odd) + odd
            self.assertEqual(valuation_two(sigma_odd), b)
            if b != a + 1:
                predicted = min(b, a + 1)
            else:
                unit = (2 ** (a + 1) - 1) * (sigma_odd // 2 ** (a + 1)) - odd
                predicted = a + 1 + valuation_two(abs(unit))
            x, y = address(n), address(successor)
            self.assertEqual(x.state, y.state)
            self.assertEqual(predicted, expected)
            self.assertEqual(valuation_two(abs(successor - n)), expected)
            self.assertEqual(valuation_two((x.x - y.x) ** 2 + (x.y - y.y) ** 2), expected)
        self.assertNotEqual(valuation_two(22), valuation_two(abs(22 - 38)))
        path = [30, 42, 54, 66, 78]
        for n, successor in zip(path, path[1:]):
            self.assertEqual(checked_sum(n), successor)
        a, b, c = [address(n) for n in path[::2]]
        self.assertEqual((a.state, b.state, c.state), ("C", "C", "C"))
        first, second = (b.x - a.x, b.y - a.y), (c.x - b.x, c.y - b.y)
        self.assertEqual((first, second), ((-2, 2), (-2, 6)))
        self.assertNotEqual(first[0] * second[1], first[1] * second[0])

    def test_same_state_suffix_ambiguity_is_a_bounded_regression(self):
        self.assertEqual(checked_sum(18), 21)
        for j in range(3, 9):
            n = 18 * (1 + 4 ** j)
            self.assertEqual(n % 4 ** j, 18)
            self.assertEqual(address(n).state, "I")
            self.assertEqual(address(18).state, "I")
            odd = n // 2
            self.assertNotEqual(isqrt(odd) ** 2, odd)
            successor = checked_sum(n)
            self.assertEqual(successor % 2, 0)
            a, b = address(n), address(18)
            self.assertEqual(valuation_two((a.x - b.x) ** 2 + (a.y - b.y) ** 2), 2 * j + 1)
        # The first numeral proves the exact state-count bookkeeping is exercised.
        self.assertEqual(base_four(18 * (1 + 4 ** 3)), "102102")

    def test_norm_is_not_numeric_order_or_a_descent_rank(self):
        for n, following, norms in [(15, 9, (9, 13)), (24, 36, (40, 52)), (72, 123, (104, 89))]:
            self.assertEqual(checked_sum(n), following)
            self.assertEqual((address(n).norm_squared, address(following).norm_squared), norms)
            self.assertEqual(address(n).state, address(following).state)
        # Even a natural geometric linearity used in a divisor-sum argument fails.
        a, b, c = address(3), address(5), address(8)
        self.assertNotEqual((a.x + b.x, a.y + b.y), (c.x, c.y))

    def test_trace_statuses_and_known_successors_are_not_clipped(self):
        t = trace(12)
        self.assertEqual(t["status"], "terminated")
        self.assertEqual([int(p["n"]) for p in t["points"]], [12, 16, 15, 9, 4, 3, 1, 0])
        for seed, steps in ((28, 1), (220, 2)):
            t = trace(seed)
            self.assertEqual((t["status"], t["cycleStart"], t["verifiedSteps"]), ("cycle", 0, steps))
        t = trace(276)
        self.assertEqual((t["status"], t["verifiedSteps"]), ("source_limit", 10))
        self.assertEqual(t["points"][-1]["n"], "5964")
        self.assertEqual(trace(276, max_steps=1)["status"], "step_limit")
        self.assertEqual(trace(276, max_source=100)["verifiedSteps"], 0)
        self.assertEqual(trace(999983, max_source=1_000_000, max_work=1)["status"], "factorization_limit")
        # Resolution takes precedence when the last allowed step is decisive.
        self.assertEqual(trace(1, max_steps=1)["status"], "terminated")
        self.assertEqual(trace(28, max_steps=1)["status"], "cycle")
        with patch("aliquot.hilbert.aliquot_sum", return_value=999):
            with self.assertRaises(ArithmeticError):
                trace(12)
        with self.assertRaises(ComputationLimit):
            checked_sum(MAX_SOURCE + 1)
        for kwargs in ({"max_source": MAX_SOURCE + 1}, {"max_steps": MAX_STEPS + 1},
                       {"max_steps": True}, {"max_steps": 0}, {"max_work": 0}):
            with self.assertRaises(ValueError):
                trace(12, **kwargs)
        with self.assertRaises(ValueError):
            trace(0)

    def test_report_and_nonserved_figure_reproduce(self):
        report = build_report()
        expected = json.loads((ROOT / "research/results/hilbert-base4.json").read_text())
        self.assertEqual(report, expected)
        for t in report["traces"]:
            for p, q in zip(t["points"], t["points"][1:]):
                self.assertEqual(_divisor_pair_sum(int(p["n"])), int(q["n"]))
                for key in ("n", "x", "y", "normSquared", "base4"):
                    self.assertIsInstance(p[key], str)
        svg = ET.parse(ROOT / "research/results/hilbert-base4.svg")
        self.assertEqual(svg.getroot().tag, "{http://www.w3.org/2000/svg}svg")
        result = subprocess.run([sys.executable, "scripts/build_hilbert_diagnostic.py", "--check"],
                                cwd=ROOT, text=True, capture_output=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
