"""Python orchestrates verification; Node is needed only to exercise browser JS."""

import json
from math import prod
from pathlib import Path
import subprocess
import unittest

from aliquot import aliquot_sum, factorize

ROOT = Path(__file__).resolve().parents[1]


class BrowserTests(unittest.TestCase):
    def test_browser_math_agrees_with_python(self):
        values = list(range(1, 301)) + [999983, 10 ** 15, 10 ** 16, 2 ** 2000, 2 ** 80 * 3 ** 40]
        result = subprocess.run(["node", "tests/browser-math.mjs"], cwd=ROOT, text=True,
                                input=json.dumps([str(n) for n in values]), capture_output=True, timeout=60)
        self.assertEqual(result.returncode, 0, result.stderr)
        results = json.loads(result.stdout)
        self.assertEqual(len(results), len(values))
        for n, browser in zip(values, results):
            with self.subTest(n=n):
                self.assertEqual(browser["sum"], str(aliquot_sum(n)))
                factors = factorize(n)
                self.assertEqual(browser["factors"], [{"prime": str(p), "exponent": e} for p, e in factors])
                # Python has no built-in base-12 formatter: independent integer conversion.
                remaining, digits = n, []
                while remaining:
                    remaining, remainder = divmod(remaining, 12)
                    digits.append("0123456789AB"[remainder])
                self.assertEqual(browser["base12"], "".join(reversed(digits)))
                divisor_info = browser["divisors"]
                count = prod(e + 1 for _, e in factors) - 1
                self.assertEqual(divisor_info["count"], str(count))
                self.assertEqual(divisor_info["sum"], str(aliquot_sum(n)))
                divisors = [int(d) for d in divisor_info["values"]]
                self.assertLessEqual(len(divisors), 200)
                self.assertEqual(divisors, sorted(set(divisors)))
                self.assertTrue(all(0 < d < n and n % d == 0 for d in divisors))
                self.assertEqual(divisor_info["truncated"], len(divisors) < count)
                if n <= 300:
                    # This does not use prime factors or the browser's generation algorithm.
                    expected = [d for d in range(1, n) if n % d == 0]
                    self.assertEqual(divisors, expected)
                    self.assertEqual(sum(divisors), int(browser["sum"]))

    def test_browser_ui_regressions(self):
        result = subprocess.run(["node", "--test", "tests/explorer.test.mjs"], cwd=ROOT,
                                capture_output=True, text=True, timeout=60)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
