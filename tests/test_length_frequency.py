"""Count bounds independently: classified seed sets + binary search, not JS prefixes."""

from bisect import bisect_left, bisect_right
import json
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]


class LengthFrequencyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        text = (ROOT / 'site/length-data.js').read_text()
        cls.data = json.loads(text[text.index('{'):text.rindex('}') + 1])
        cls.options = [{'threshold': threshold, 'population': population, 'bound': 10000}
                       for threshold, population in [(100, 'all'), (100, 'even'), (100, 'odd'), (50, 'all'), (200, 'all')]]
        result = subprocess.run(['node', 'tests/length-frequency-math.mjs'], cwd=ROOT,
                                input=json.dumps({'orbits': cls.data['orbits'], 'options': cls.options}),
                                capture_output=True, text=True, timeout=60)
        if result.returncode:
            raise RuntimeError(result.stderr)
        cls.results = json.loads(result.stdout)

    def test_every_prefix_rolling_window_and_block_matches_independent_counts(self):
        for options, result in zip(self.options, self.results):
            eligible, definitely_long, possibly_long = [], [], []
            for row in self.data['orbits']:
                seed = int(row['seed'])
                if options['population'] != 'all' and seed % 2 != (options['population'] == 'odd'):
                    continue
                eligible.append(seed)
                resolved = row['status'] in ('terminated', 'cycle')
                known_length = row['steps'] if resolved else row['lower_bound']
                if known_length >= options['threshold']:
                    definitely_long.append(seed)
                if not resolved or row['steps'] >= options['threshold']:
                    possibly_long.append(seed)
            self.assertEqual(len(result['cumulative']), 10001)
            self.assertEqual(len(result['recent']), 9001)
            self.assertEqual(len(result['blocks']), 10)
            for section in ('cumulative', 'recent', 'blocks'):
                for point in result[section]:
                    a, b = point['from'], point['x']
                    for field, values in [('total', eligible), ('lower', definitely_long), ('upper', possibly_long)]:
                        expected = bisect_right(values, b) - bisect_left(values, a) if b >= a else 0
                        self.assertEqual(point[field], expected, (options, section, point, field))
                        self.assertIs(type(point[field]), int)
                    self.assertLessEqual(point['lower'], point['upper'])
                    self.assertLessEqual(point['upper'], point['total'])
                    if section == 'recent':
                        self.assertEqual(b - a + 1, 1000)

    def test_reported_finite_comparison_and_parity_denominators(self):
        all_seeds, even, odd = self.results[:3]
        self.assertEqual(all_seeds['cumulative'][1000], {'x': 1000, 'from': 1, 'total': 1000, 'lower': 22, 'upper': 30})
        self.assertEqual(all_seeds['cumulative'][-1], {'x': 10000, 'from': 1, 'total': 10000, 'lower': 581, 'upper': 1056})
        self.assertEqual(all_seeds['recent'][-1], {'x': 10000, 'from': 9001, 'total': 1000, 'lower': 58, 'upper': 133})
        # Even the conservative bounds certify a finite block-to-block increase.
        self.assertGreater(all_seeds['blocks'][-1]['lower'], all_seeds['blocks'][0]['upper'])
        self.assertEqual(even['cumulative'][-1]['total'], 5000)
        self.assertEqual(even['cumulative'][-1]['lower'], 575)
        self.assertEqual(even['cumulative'][-1]['upper'], 1050)
        self.assertEqual(odd['cumulative'][-1]['total'], 5000)
        self.assertEqual(odd['cumulative'][-1]['lower'], 6)
        self.assertEqual(odd['cumulative'][-1]['upper'], 6)

    def test_browser_interactions_and_explanations(self):
        page = (ROOT / 'site/lengths/index.html').read_text()
        for phrase in ('id="frequency"', 'Cumulative count', 'Cumulative share', 'Last 1,000 seeds',
                       'not a confidence interval', 'rounded outward', 'not automatically a long orbit',
                       'Even/odd percentages divide by eligible seeds'):
            self.assertIn(phrase, page)
        result = subprocess.run(['node', '--test', 'tests/length-frequency.test.mjs'], cwd=ROOT,
                                capture_output=True, text=True, timeout=60)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
