"""Independent Python verification of the served inverse search and its UI."""

import json
from math import isqrt
from pathlib import Path
import subprocess
import unittest

from aliquot import aliquot_sum

ROOT = Path(__file__).resolve().parents[1]


def divisor_pair_sum(n):
    """Independent of both the browser's sieve and prime factorization."""
    total = 0
    for d in range(1, isqrt(n) + 1):
        if n % d == 0:
            other = n // d
            if d < n:
                total += d
            if other != d and other < n:
                total += other
    return total


class ReverseTests(unittest.TestCase):
    def browser(self, **request):
        process = subprocess.run(["node", "tests/reverse-math.mjs"], cwd=ROOT,
                                 input=json.dumps(request), text=True,
                                 capture_output=True, timeout=60)
        self.assertEqual(process.returncode, 0, process.stderr)
        return json.loads(process.stdout)

    def test_every_sieve_sum_and_predecessor_list_agrees_with_independent_enumeration(self):
        bound = 10000
        targets = list(range(301)) + [10000, 9007199254740993, 10**100]
        data = self.browser(bound=bound, targets=[str(n) for n in targets])
        expected = {n: divisor_pair_sum(n) for n in range(1, bound + 1)}
        self.assertEqual(data["sums"], [[str(n), str(expected[n])] for n in expected])
        for target, result in zip(targets, data["results"]):
            with self.subTest(target=target):
                ceiling = 1 if target == 0 else None if target == 1 else (target - 1)**2
                checked = bound if ceiling is None else min(bound, ceiling)
                self.assertEqual(result["target"], str(target))
                self.assertEqual(result["bound"], bound)
                self.assertEqual(result["checked"], checked)
                self.assertEqual(result["ceiling"], None if ceiling is None else str(ceiling))
                self.assertEqual(result["complete"], ceiling is not None and ceiling <= bound)
                self.assertEqual(result["values"], [str(n) for n in range(1, bound + 1)
                                                    if expected[n] == target])
        results = {int(r["target"]): r for r in data["results"]}
        self.assertEqual(results[0]["values"], ["1"])
        self.assertEqual(len(results[1]["values"]), 1229)
        self.assertFalse(results[1]["complete"])
        self.assertEqual(results[2]["values"], [])
        self.assertTrue(results[2]["complete"])
        self.assertEqual(results[12]["values"], ["121"])
        self.assertEqual(results[16]["values"], ["12", "26"])

    def test_upper_resource_bound_sums_agree_with_two_independent_methods(self):
        samples = [1, 2, 6, 12, 99991, 500000, 720720, 999983, 999999, 1000000]
        data = self.browser(bound=1000000, samples=samples)
        for source, result in data["sums"]:
            n = int(source)
            self.assertEqual(int(result), aliquot_sum(n))
            self.assertEqual(int(result), divisor_pair_sum(n))

    def test_browser_reverse_interactions(self):
        process = subprocess.run(["node", "--test", "tests/reverse.test.mjs"], cwd=ROOT,
                                 capture_output=True, text=True, timeout=60)
        self.assertEqual(process.returncode, 0, process.stdout + process.stderr)

    def test_reverse_page_keeps_bounds_direction_and_nondivergence_explicit(self):
        page = (ROOT / "site/reverse/index.html").read_text()
        for text in ["All arrows point forward", "alternatives, not consecutive terms",
                     "up to 1,000,000 per sieve", "Rows are layout, not a numeric scale",
                     "m ≤ (n − 1)²", "every finite search is partial", "s(0) is undefined",
                     "not a proof of an unbounded forward orbit", "exact decimal strings",
                     'id="point-compute"', 'id="point-follow"', 'id="verify-stop"', 'id="search-stop"',
                     'src="/point-info.js"', 'src="/reverse-math.js"']:
            self.assertIn(text, page)
        for path in ["site/index.html", "site/research/index.html"]:
            self.assertIn('href="/reverse/"', (ROOT / path).read_text())
        for path in ["site/explorer.js", "site/reverse.js"]:
            code = (ROOT / path).read_text()
            self.assertIn("AliquotPointInfo.basic", code)
            self.assertIn("AliquotPointInfo.divisors", code)
        css = (ROOT / "site/reverse.css").read_text()
        card = css.split(".reverse-inspector .point-details {", 1)[1].split("}", 1)[0]
        self.assertIn("position: static", card)
        self.assertNotIn("height", card)
        self.assertNotIn("overflow", card)
        self.assertIn("@media (max-width: 800px)", css)
