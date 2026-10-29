from collections import Counter
from contextlib import redirect_stderr, redirect_stdout
from fractions import Fraction
from math import gcd, isqrt
from pathlib import Path
import io
import json
import unittest
from unittest.mock import patch

from aliquot import factorize
from aliquot.__main__ import main
from aliquot.backward import _tables, backward_report

ROOT = Path(__file__).resolve().parents[1]


def direct_sum(n):
    return sum(d for d in range(1, n) if n % d == 0)


def fraction(row):
    return Fraction(int(row['numerator']), int(row['denominator']))


class BackwardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = backward_report()
        cls.small = backward_report(1500)

    def test_artifact_and_predeclared_nested_bounds(self):
        raw = (ROOT/'research/results/backward-coverage.json').read_text()
        self.assertEqual(raw, json.dumps(self.report, ensure_ascii=False, separators=(',', ':'))+'\n')
        expected = [(1000, 246, 97, 54, 22), (10000, 2488, 1049, 797, 436),
                    (100000, 24795, 10384, 8853, 5339),
                    (1000000, 247545, 104107, 93288, 58896)]
        for row, (bound, abundant, all_smaller, prime, root) in zip(self.report['levels'], expected):
            self.assertEqual(int(row['targetBound']), bound)
            self.assertEqual(row['abundantTargets'], abundant)
            self.assertEqual([row[k]['targets'] for k in ('allSmaller', 'primeCore', 'squareRootCore')],
                             [all_smaller, prime, root])
        self.assertEqual(len(self.report['levels']), len(expected))
        # A target-bound prefix already includes ALL of its smaller sources.
        self.assertEqual(backward_report(1000)['levels'][0], self.report['levels'][0])

    def test_multiplicative_table_against_literal_divisors(self):
        spf, total = _tables(1500)
        self.assertIsNone(total[0])
        for n in range(1, 1501):
            self.assertEqual(total[n]-n, direct_sum(n))
            if n > 1:
                self.assertEqual(spf[n], factorize(n)[0][0])

    def test_independent_small_oracle_all_sources_and_core_decompositions(self):
        bound = 1500
        sums = [None]+[direct_sum(n) for n in range(1, bound+1)]
        abundant = {n for n in range(1, bound+1) if sums[n] > n}
        rows = {'allSmaller': set(), 'primeCore': set(), 'squareRootCore': set()}
        for m in range(1, bound+1):
            n = sums[m]
            if not m < n <= bound or n not in abundant:
                continue
            rows['allSmaller'].add((n, m, 0, 0))
            # Enumerate every proper divisor C directly, not using least factors.
            for c in range(1, m):
                if m % c:
                    continue
                p = m//c
                if (gcd(c, p) == 1 and sums[c] > c
                        and all(p % d for d in range(2, isqrt(p)+1))):
                    record = (n, m, c, p)
                    rows['primeCore'].add(record)
                    if c*c <= n:
                        rows['squareRootCore'].add(record)
        for key, records in rows.items():
            got = self.small['levels'][-1][key]
            targets = Counter(n for n, _, _, _ in records)
            source_pairs = Counter((n, m) for n, m, _, _ in records)
            sources = Counter(n for n, _ in source_pairs)
            self.assertEqual(got['targets'], len(targets))
            self.assertEqual(got['representations'], len(records))
            self.assertEqual(got['predecessors'], len(source_pairs))
            self.assertEqual(int(got['representationSecondMoment']), sum(r*r for r in targets.values()))
            self.assertEqual(int(got['predecessorSecondMoment']), sum(r*r for r in sources.values()))
            self.assertEqual(int(got['samePredecessorOrderedCollisionPairs']),
                             sum(r*(r-1) for r in source_pairs.values()))
        six = {r for r in rows['squareRootCore'] if r[2] % 6 == 0 and gcd(r[2]//6, 6) == 1}
        self.assertEqual(self.small['cleanSixSquareRootSubset']['representations'], len(six))
        self.assertIn((1038, 690, 30, 23), six)

    def test_square_root_uses_each_target_not_the_outer_bound(self):
        row = self.report['examples']['firstGaps']['hasPrimeCoreButNotSquareRootCore']
        self.assertEqual(row['target'], '108')
        self.assertFalse(row['coveredBySquareRootCore'])
        source = next(s for s in row['predecessors'] if s['source'] == '60')
        self.assertEqual(source['representations'], [
            {'core': '12', 'prime': '5', 'coreWithinTargetSquareRoot': False},
            {'core': '20', 'prime': '3', 'coreWithinTargetSquareRoot': False},
        ])
        # 12^2 and 20^2 are below both report bounds, but exceed target 108.
        self.assertEqual(row, self.small['examples']['firstGaps']['hasPrimeCoreButNotSquareRootCore'])

    def test_actual_distinct_source_collision_is_not_one_source_counted_twice(self):
        row = self.report['examples']['firstSquareRootCollision']
        self.assertEqual((row['target'], row['predecessorCount']), ('396', 2))
        self.assertEqual([s['source'] for s in row['predecessors']], ['276', '306'])
        self.assertEqual([s['representations'] for s in row['predecessors']], [
            [{'core': '12', 'prime': '23', 'coreWithinTargetSquareRoot': True}],
            [{'core': '18', 'prime': '17', 'coreWithinTargetSquareRoot': True}],
        ])
        self.assertEqual(16*23+28, 21*17+39)

    def test_all_named_seeds_are_outside_even_the_complete_smaller_predecessor_filter(self):
        for row in self.report['examples']['namedTargets']:
            self.assertTrue(row['abundant'])
            self.assertEqual(row['predecessorCount'], 0)
            self.assertFalse(row['hasSmallerPredecessor'])
        # Uncovered does not mean escape: explicit terminating and cyclic controls.
        self.assertEqual([direct_sum(n) for n in (12, 16, 15, 9, 4, 3, 1)], [16, 15, 9, 4, 3, 1, 0])
        self.assertEqual((direct_sum(220), direct_sum(284)), (284, 220))

    def test_moments_histograms_and_gap_partition(self):
        for level in self.report['levels']:
            abundant = level['abundantTargets']
            self.assertEqual(sum(level['gaps'].values()), abundant-level['squareRootCore']['targets'])
            for name in ('allSmaller', 'primeCore', 'squareRootCore'):
                row = level[name]
                r1, r2 = row['representations'], int(row['representationSecondMoment'])
                self.assertEqual(sum(x['targets'] for x in row['representationMultiplicity']), row['targets'])
                self.assertEqual(sum(x['targets']*x['multiplicity'] for x in row['representationMultiplicity']), r1)
                self.assertEqual(sum(x['targets']*x['multiplicity']**2 for x in row['representationMultiplicity']), r2)
                self.assertEqual(fraction(row['representationCauchyLowerBound']), Fraction(r1*r1, r2))
                self.assertLessEqual(fraction(row['representationCauchyLowerBound']), row['targets'])
                self.assertEqual(fraction(row['coverageOfAbundantTargets']), Fraction(row['targets'], abundant))
                self.assertEqual(int(row['samePredecessorOrderedCollisionPairs'])+
                                 int(row['distinctPredecessorOrderedRepresentationPairs']), r2-r1)
            root = level['squareRootCore']
            self.assertEqual(root['representations'], root['predecessors'])
            self.assertEqual(root['samePredecessorOrderedCollisionPairs'], '0')
            self.assertEqual(root['representationSecondMoment'], root['predecessorSecondMoment'])
        self.assertGreater(int(self.report['levels'][-1]['primeCore']['samePredecessorOrderedCollisionPairs']), 0)

    def test_all_reported_predecessors_and_factors(self):
        examples = self.report['examples']
        rows = (examples['namedTargets']+list(examples['firstGaps'].values())+
                [examples['firstSquareRootCollision'], examples['largestSquareRootMultiplicity']])
        for row in rows:
            n = int(row['target'])
            self.assertEqual(row['predecessorCount'], len(row['predecessors'])+row['omittedPredecessors'])
            for source in row['predecessors']:
                m = int(source['source'])
                self.assertLess(m, n)
                self.assertEqual(factorize(m), [(int(p), e) for p, e in source['factors']])
                # Divisor pairs keep this independent check bounded for large examples.
                total = sum(d+(m//d if d*d != m else 0) for d in range(1, isqrt(m)+1) if m % d == 0)
                self.assertEqual(total-m, n)
                for r in source['representations']:
                    c, p = int(r['core']), int(r['prime'])
                    self.assertEqual(c*p, m)
                    self.assertEqual(gcd(c, p), 1)
                    self.assertEqual(factorize(p), [(p, 1)])
                    self.assertGreater(direct_sum(c), c)
                    self.assertEqual(direct_sum(c)*p+direct_sum(c)+c, n)
                    self.assertEqual(r['coreWithinTargetSquareRoot'], c*c <= n)

    def test_empty_small_universes_and_invalid_bounds(self):
        for bound in (1, 6, 11):
            report = backward_report(bound)
            row = report['levels'][0]
            self.assertEqual(row['abundantTargets'], 0)
            self.assertIsNone(row['squareRootCore']['coverageOfAbundantTargets'])
            self.assertEqual(fraction(row['squareRootCore']['representationCauchyLowerBound']), 0)
            self.assertEqual(report['examples']['namedTargets'], [])
        for bound in (0, -1, True, 1.5, '100', 1000001):
            with self.assertRaises(ValueError):
                backward_report(bound)

    def test_cli_limits_and_independent_check_failures_are_atomic(self):
        for arguments in (['backward', '--bound', '1000001'],):
            out, err = io.StringIO(), io.StringIO()
            with redirect_stdout(out), redirect_stderr(err):
                self.assertEqual(main(arguments), 1)
            self.assertEqual(out.getvalue(), '')
            self.assertTrue(err.getvalue())
        for target, replacement in [('aliquot.__main__.MAX_REPORT_BYTES', 1),
                                    ('aliquot.backward.divisor_sieve', lambda bound: [None]+[0]*bound),
                                    ('aliquot.backward._factors', lambda n, spf: [])]:
            out, err = io.StringIO(), io.StringIO()
            with patch(target, replacement), redirect_stdout(out), redirect_stderr(err):
                self.assertEqual(main(['backward', '--bound', '1000', '--compact']), 1)
            self.assertEqual(out.getvalue(), '')
            self.assertTrue(err.getvalue())
        out = io.StringIO()
        with redirect_stdout(out):
            self.assertEqual(main(['backward', '--bound', '1', '--compact']), 0)
        self.assertEqual(json.loads(out.getvalue())['targetBound'], '1')


if __name__ == '__main__':
    unittest.main()
