"""Check the educational examples against exact arithmetic, not their labels."""

from html.parser import HTMLParser
from math import isqrt
from pathlib import Path
import unittest

from aliquot import aliquot_sum

ROOT = Path(__file__).resolve().parents[1]
CASES = {
    12: ("terminating", [12, 16, 15, 9, 4, 3, 1, 0]),
    30: ("terminating", [30, 42, 54, 66, 78, 90, 144, 259, 45, 33, 15, 9, 4, 3, 1, 0]),
    28: ("perfect", [28, 28]),
    95: ("aspiring", [95, 25, 6, 6]),
    790: ("aspiring", [790, 650, 652, 496, 496]),
    220: ("amicable", [220, 284, 220]),
    1184: ("amicable", [1184, 1210, 1184]),
    1264460: ("sociable", [1264460, 1547860, 1727636, 1305184, 1264460]),
    12496: ("sociable", [12496, 14288, 15472, 14536, 14264, 12496]),
    # Only a finite prefix is checked here. It cannot establish unresolved status
    # or divergence; the description explicitly warns against that inference.
    276: ("unresolved", [276, 396, 696, 1104, 1872]),
}


class PresetParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.presets = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "button" and "data-n" in attrs:
            self.presets.append(attrs)


def divisor_pair_sum(n):
    total = 0
    for d in range(1, isqrt(n) + 1):
        if n % d == 0:
            if d < n:
                total += d
            other = n // d
            if other != d and other < n:
                total += other
    return total


class PresetTests(unittest.TestCase):
    def setUp(self):
        parser = PresetParser()
        parser.feed((ROOT / "site/index.html").read_text())
        self.presets = parser.presets

    def test_catalog_categories_and_descriptions(self):
        self.assertEqual(len(self.presets), len(CASES))
        self.assertEqual([int(p["data-n"]) for p in self.presets], list(CASES))
        for preset in self.presets:
            self.assertEqual(preset["type"], "button")
            self.assertEqual(preset["data-kind"], CASES[int(preset["data-n"])][0])
            self.assertTrue(preset["data-description"])
            self.assertLess(len(preset["data-description"]), 100)

    def test_paths_match_factorization_and_independent_divisor_pairs(self):
        for seed, (kind, path) in CASES.items():
            with self.subTest(seed=seed):
                for current, following in zip(path, path[1:]):
                    self.assertEqual(aliquot_sum(current), following)
                    self.assertEqual(divisor_pair_sum(current), following)
                if kind == "terminating":
                    self.assertEqual(path[-1], 0)
                elif kind == "aspiring":
                    self.assertEqual(path[-1], path[-2])
                    self.assertNotEqual(seed, path[-1])
                    self.assertEqual(aliquot_sum(path[-1]), path[-1])
                elif kind in {"perfect", "amicable", "sociable"}:
                    self.assertEqual(path[-1], seed)
                    self.assertEqual(len(set(path[:-1])), len(path) - 1)
                    if kind == "perfect":
                        self.assertEqual(len(path) - 1, 1)
                    elif kind == "amicable":
                        self.assertEqual(len(path) - 1, 2)
                    else:
                        self.assertIn(len(path) - 1, [4, 5])

    def test_growth_examples_have_cautious_descriptions(self):
        descriptions = {int(p["data-n"]): p["data-description"] for p in self.presets}
        self.assertEqual(max(CASES[30][1]), 259)
        self.assertIn("peaks at 259", descriptions[30])
        self.assertIn("terminates at 0", descriptions[30])
        self.assertIn("not known to terminate or cycle", descriptions[276])
        self.assertIn("not proof of divergence", descriptions[276])
