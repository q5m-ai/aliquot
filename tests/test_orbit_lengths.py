"""Independent certificates, exact resolution semantics, and chart regressions."""

from collections import Counter
import json
from math import isqrt, prod
from pathlib import Path
import subprocess
import unittest

from aliquot.orbit_lengths import build_orbit_lengths
from scripts.build_orbit_lengths import render

ROOT = Path(__file__).resolve().parents[1]


def is_prime(n):
    # Independent of the core's factorizer; no probable-prime tests.
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    return all(n % d and n % (d + 2) for d in range(5, isqrt(n) + 1, 6))


class OrbitLengthTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = build_orbit_lengths()
        cls.rows = {int(row['seed']): row for row in cls.data['orbits']}

    def test_committed_artifact_is_reproducible_and_exact(self):
        text = (ROOT / 'site/length-data.js').read_text()
        self.assertEqual(text, render(self.data))
        self.assertEqual(json.loads(text[text.index('{'):text.rindex('}') + 1]), self.data)
        self.assertEqual(set(self.rows), set(range(1, 10_001)))
        self.assertEqual(self.data['limits']['seed_bound'], 10_000)
        self.assertEqual(Counter(row['status'] for row in self.rows.values()),
                         {'terminated': 8951, 'cycle': 224, 'factorization_limit': 818, 'step_limit': 7})
        self.assertEqual(Counter(self.rows[n]['status'] for n in range(1, 1001)),
                         {'terminated': 961, 'cycle': 22, 'factorization_limit': 17})
        for row in self.rows.values():
            for key in ('seed', 'end', 'peak'):
                self.assertIsInstance(row[key], str)
                self.assertEqual(str(int(row[key])), row[key])

    def test_every_edge_has_independently_verified_factors_and_divisors(self):
        primes = {int(p) for edge in self.data['edges'] for p, _ in edge['factors']}
        self.assertTrue(all(is_prime(p) for p in primes))
        for edge in self.data['edges']:
            n = int(edge['from'])
            factors = [(int(p), e) for p, e in edge['factors']]
            self.assertEqual(prod(p**e for p, e in factors), n)
            self.assertEqual([p for p, _ in factors], sorted({p for p, _ in factors}))
            self.assertTrue(all(type(e) is int and e > 0 for _, e in factors))
            divisors = [1]
            for p, e in factors:
                divisors = [d * p**k for d in divisors for k in range(e + 1)]
            self.assertEqual(sum(d for d in divisors if d < n), int(edge['to']), n)
        sources = {edge['from'] for edge in self.data['edges']}
        self.assertNotIn('0', sources)
        # Every chart seed has certified factors and a successor for the shared
        # info panel. No hover-time factorization or probable-prime fallback.
        self.assertTrue({str(n) for n in self.rows}.issubset(sources))

    def test_every_record_replays_to_its_exact_first_stop_or_lower_bound(self):
        edges = {int(edge['from']): int(edge['to']) for edge in self.data['edges']}
        limits = self.data['limits']
        for seed, row in self.rows.items():
            n, path = seed, []
            for _ in range(row['steps']):
                self.assertNotEqual(n, 0)
                self.assertNotIn(n, path)
                self.assertLessEqual(n, int(limits['max_source']))
                path.append(n)
                n = edges[n]
            self.assertEqual(str(n), row['end'])
            self.assertEqual(str(max(path + [n])), row['peak'])
            self.assertLessEqual(row['steps'], limits['max_steps'])
            if row['status'] == 'terminated':
                self.assertEqual(n, 0)
                self.assertEqual(row['lower_bound'], row['steps'])
            elif row['status'] == 'cycle':
                self.assertIn(n, path)
                self.assertEqual(row['cycle'], list(map(str, path[path.index(n):])))
                self.assertEqual(row['lower_bound'], row['steps'])
            else:
                self.assertNotEqual(n, 0)
                self.assertNotIn(n, path)
                if row['status'] == 'factorization_limit':
                    self.assertNotIn(n, edges)
                elif row['status'] == 'step_limit':
                    # Another start may have computed this edge; the per-start
                    # transition bound still makes this a lower bound only.
                    self.assertEqual(row['steps'], limits['max_steps'])
                else:
                    self.assertEqual(row['status'], 'source_limit')
                    self.assertGreater(n, int(limits['max_source']))
                self.assertEqual(row['lower_bound'], row['steps'] + 1)

    def test_138_is_resolved_beyond_display_cap_but_276_is_only_a_lower_bound(self):
        self.assertEqual(self.rows[138]['steps'], 178)
        self.assertEqual(self.rows[138]['status'], 'terminated')
        self.assertEqual(self.rows[138]['peak'], '179931895322')
        self.assertEqual(self.rows[276]['steps'], 79)
        self.assertEqual(self.rows[276]['lower_bound'], 80)
        self.assertEqual(self.rows[276]['status'], 'factorization_limit')
        self.assertEqual(self.rows[276]['end'], '2556878765995204')
        for seed, steps in [(1, 1), (6, 1), (28, 1), (137, 2), (139, 2), (220, 2), (275, 3), (277, 2),
                            (1184, 2), (8128, 1), (10_000, 4)]:
            self.assertEqual(self.rows[seed]['steps'], steps)

    def test_resolution_at_exact_step_cap_is_not_censored(self):
        data = build_orbit_lengths(seed_bound=6, max_steps=1)
        rows = {int(row['seed']): row for row in data['orbits']}
        self.assertEqual(rows[1]['status'], 'terminated')
        self.assertEqual(rows[6]['status'], 'cycle')
        self.assertEqual(rows[2]['status'], 'step_limit')
        self.assertEqual(rows[2]['lower_bound'], 2)

    def test_small_budgets_never_invent_a_length_or_prime(self):
        rows = build_orbit_lengths(seed_bound=4, max_work=1)['orbits']
        self.assertEqual(rows[-1]['status'], 'factorization_limit')
        self.assertEqual(rows[-1]['steps'], 0)
        self.assertEqual(rows[-1]['lower_bound'], 1)
        row = build_orbit_lengths(seed_bound=12, max_source=12)['orbits'][-1]
        self.assertEqual(row['status'], 'source_limit')
        self.assertEqual(row['end'], '16')
        self.assertEqual(row['lower_bound'], 2)
        for kwargs in ({'max_steps': 0}, {'max_work': True}, {'max_source': -1},
                       {'seed_bound': 10_001}, {'max_steps': 1001}, {'max_source': 10**101}):
            with self.assertRaises(ValueError):
                build_orbit_lengths(**kwargs)

    def test_page_navigation_bounds_and_browser_regressions(self):
        page = (ROOT / 'site/lengths/index.html').read_text()
        for text in ('100+ steps', 'logarithmic', '79 verified steps', 'at least 80 steps',
                     '256 transitions', '2,000,000', 'not a measured length', 's(0)',
                     '1–10,000', 'value="5000"', 'value="10000"', 'point-info.js',
                     'id="chart" class="chart"', 'id="point-details" class="point-details"',
                     'id="point-factorization"', 'id="point-divisors"', 'id="point-close"'):
            self.assertIn(text.lower(), page.lower())
        for page in (ROOT / 'site').rglob('index.html'):
            self.assertIn('href="/lengths/"', page.read_text())
        result = subprocess.run(['node', '--test', 'tests/lengths.test.mjs'], cwd=ROOT,
                                capture_output=True, text=True, timeout=60)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
