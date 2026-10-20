"""Python orchestrates verification; Node is needed only to exercise browser JS."""

import json
from pathlib import Path
import subprocess
import unittest

from aliquot import aliquot_sum

ROOT = Path(__file__).resolve().parents[1]


class BrowserTests(unittest.TestCase):
    def test_browser_math_agrees_with_python(self):
        values = list(range(1, 301)) + [999983, 10 ** 15, 10 ** 16, 2 ** 2000, 2 ** 80 * 3 ** 40]
        result = subprocess.run(["node", "tests/browser-math.mjs"], cwd=ROOT, text=True,
                                input=json.dumps([str(n) for n in values]), capture_output=True, timeout=60)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), [str(aliquot_sum(n)) for n in values])

    def test_browser_ui_regressions(self):
        result = subprocess.run(["node", "--test", "tests/explorer.test.mjs"], cwd=ROOT,
                                capture_output=True, text=True, timeout=60)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
