from contextlib import redirect_stderr, redirect_stdout
from copy import deepcopy
import io
import json
from math import gcd, prod
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from aliquot import ComputationLimit, factorize
from aliquot.__main__ import main
from aliquot.certified import CertifiedFactorizer
from aliquot.exponent_vectors import (
    aliquot_mod, divisor_residue_counts, geometric_mod, independent_sum,
    sigma, summarize_trace, trace, trial_prefix, value, vector_census,
    vector_report, verify_report, MAX_REPORT_BYTES, MAX_TRACES,
)
from aliquot.research import divisor_sieve

ROOT = Path(__file__).resolve().parents[1]


class ExponentVectorTests(unittest.TestCase):
    def test_sparse_arithmetic_and_modular_tensor_product(self):
        sums = divisor_sieve(2000)
        for n in range(1, 2001):
            factors = tuple(factorize(n))
            self.assertEqual(value(factors), n)
            self.assertEqual(sigma(factors) - n, sums[n])
            for m in [1, 2, 4, 6, 12, 25, 81]:
                self.assertEqual(aliquot_mod(factors, m), sums[n] % m)
            if n <= 250:
                self.assertEqual(independent_sum(factors), sums[n])
                for m in [1, 4, 9, 12, 25]:
                    histogram = divisor_residue_counts(factors, m)
                    expected = [0] * m
                    for d in range(1, n):
                        if n % d == 0:
                            expected[d % m] += 1
                    self.assertEqual(histogram, expected)
                    all_divisors = divisor_residue_counts(factors, m, proper=False)
                    expected[n % m] += 1
                    self.assertEqual(all_divisors, expected)

    def test_huge_symbolic_exponent_without_expanded_integer(self):
        exponent = 10**12
        factors = ((2, exponent),)
        for m in [1, 8, 12, 81, 97, 256]:
            expected = (pow(2, exponent, m) - 1) % m
            self.assertEqual(aliquot_mod(factors, m), expected)
            histogram = divisor_residue_counts(factors, m)
            self.assertEqual(sum(histogram), exponent)
            self.assertEqual(sum(i*c for i, c in enumerate(histogram)) % m, expected)
        self.assertEqual(aliquot_mod(factors, 97), 60)
        for p in [2, 3, 5, 7]:
            for length in range(1, 40):
                for m in [1, 4, 9, 12]:
                    self.assertEqual(geometric_mod(p, length, m), sum(p**i for i in range(length)) % m)

    def test_geometry_certificates_and_projection_counterexamples(self):
        path = [12, 16, 15, 9]
        vectors = [tuple(dict(factorize(n)).get(p, 0) for p in [2, 3, 5]) for n in path]
        self.assertEqual(tuple(2*a for a in vectors[0]),
                         tuple(a+b for a, b in zip(vectors[1], vectors[-1])))
        for a, b in zip(path, path[1:]):
            self.assertEqual(sigma(factorize(a)) - a, b)
        # Positive combination of four displacement vectors rules out any
        # globally nonincreasing positive linear functional, even with flat steps.
        edges = [(12, 16, 3), (16, 15, 1), (30, 42, 1), (42, 54, 1)]
        total = [0] * 4
        for n, s, weight in edges:
            self.assertEqual(sigma(factorize(n)) - n, s)
            a, b = dict(factorize(n)), dict(factorize(s))
            for i, p in enumerate([2, 3, 5, 7]):
                total[i] += weight * (b.get(p, 0) - a.get(p, 0))
        self.assertEqual(total, [2, 0, 0, 0])
        self.assertEqual(tuple(dict(factorize(2)).get(p, 0) for p in [2,3,5,7]),
                         tuple(dict(factorize(22)).get(p, 0) for p in [2,3,5,7]))
        self.assertEqual(sigma(factorize(2)) - 2, 1)
        self.assertEqual(sigma(factorize(22)) - 22, 14)
        # Same unlabeled exponent multiset, all three growth classifications.
        self.assertEqual([sigma(factorize(n)) - 2*n for n in [20,28,44]], [2,0,-4])

    def test_primitive_triple_and_residual_supply_demands(self):
        sums = divisor_sieve(2000)

        def order(n, p):
            exponent = 0
            while n % p == 0:
                exponent += 1
                n //= p
            return exponent

        for n in range(2, 2001):
            m = sums[n]
            g = gcd(n, n + m)
            u, v, r = n//g, (n+m)//g, m//g
            self.assertEqual(u+r, v)
            self.assertEqual((gcd(u,v), gcd(u,r), gcd(v,r)), (1,1,1))
            old_primes = {p for p, _ in factorize(n)}
            m_factors = factorize(m)
            old = [(p,e) for p,e in m_factors if p in old_primes]
            new = [(p,e) for p,e in m_factors if p not in old_primes]
            residual = prod(p**e for p,e in new)
            self.assertEqual(gcd(residual, n*(n+m)), 1)
            for p in [2,3,5,7]:
                demand = max(0, order(m,p)+1-order(sigma(old),p))
                self.assertEqual(order(sigma(m_factors),p) > order(m,p),
                                 order(sigma(new),p) >= demand)
        self.assertEqual(gcd(12,28), 4)
        self.assertEqual((28-12)//4, 4)  # Normalized residual is NOT coprime to g.

    def test_small_prime_abundance_return_can_lose(self):
        sums = divisor_sieve(100000)
        path = [47952,94586,47296,46684,42524,31900]
        self.assertEqual([sums[n] for n in path[:-1]], path[1:])
        parts = [prod(p**e for p,e in factorize(n) if p<=7) for n in path]
        self.assertEqual(parts, [1296,2,64,4,4,100])
        membership = [sigma(factorize(d))>=2*d and sums[n]>n for n,d in zip(path,parts)]
        self.assertEqual(membership, [True,False,False,False,False,True])
        self.assertLess(path[-1], path[0])
        report = json.loads((ROOT/'research/results/exponent-vectors-extended.json').read_text())
        rows = next(t['rows'] for t in report['traces'] if t['seed']=='660')
        self.assertEqual([int(row['n']) for row in rows[9:15]], path)

    def test_known_outcomes_and_bounds(self):
        for seed, steps, status, end in [(12,7,'terminated','0'), (138,178,'terminated','0'),
                                        (318,35,'terminated','0'), (220,2,'cycle','220'), (28,1,'cycle','28')]:
            result = trace(seed, CertifiedFactorizer())
            self.assertEqual((result['steps'],result['status'],result['end']), (steps,status,end))
        self.assertEqual(trace(1, CertifiedFactorizer())['rows'][0]['factors'], [])
        self.assertEqual(trace(12, CertifiedFactorizer(), max_steps=1)['status'], 'step_limit')
        self.assertEqual(trace(28, CertifiedFactorizer(), max_steps=1)['status'], 'cycle')
        self.assertEqual(trace(1, CertifiedFactorizer(), max_steps=1)['status'], 'terminated')
        limited = trace(12, CertifiedFactorizer(max_bits=4))
        self.assertEqual((limited['steps'], limited['end'], limited['status']), (1,'16','source_bit_limit'))
        self.assertEqual(trace(276, CertifiedFactorizer(max_work=1))['status'], 'factorization_limit')
        self.assertEqual(trial_prefix(276, max_steps=256, max_bits=256)['steps'], 79)

    def test_corrupt_edges_and_primes_are_rejected(self):
        engine = CertifiedFactorizer()
        result = trace(220, engine)
        result['summary'] = summarize_trace(result)
        report = {'schema':'aliquot-exponent-vectors-v1', 'primeCertificates':engine.export_certificates(),
                  'traces':[result], 'limits':{'maxSteps':256,'maxSourceBits':256,'maxDivisors':200000}}
        self.assertTrue(verify_report(report))
        for field in ['next', 'factors', 'status', 'summary', 'steps', 'features']:
            broken = deepcopy(report)
            t = broken['traces'][0]
            if field == 'next':
                t['rows'][0]['next'] = '285'
            elif field == 'factors':
                t['rows'][0]['factors'][0][1] = 3
            elif field == 'status':
                t['status'] = 'terminated'
            elif field == 'summary':
                t['summary']['counts']['growing'] = 99
            elif field == 'steps':
                t['steps'] = 3
            else:
                t['rows'][0]['l1'] = 100
            with self.subTest(field=field):
                with self.assertRaises((ArithmeticError, ValueError)):
                    verify_report(broken)
        with patch('aliquot.exponent_vectors.independent_sum', return_value=0):
            with self.assertRaises(ArithmeticError):
                trace(12, CertifiedFactorizer())
        with patch('aliquot.exponent_vectors.independent_sum', side_effect=ComputationLimit('limit')):
            self.assertEqual(trace(12, CertifiedFactorizer())['status'], 'verification_limit')

    def test_empty_trace_seed_domain_aggregate_and_file_limits(self):
        engine = CertifiedFactorizer()
        result = trace(220, engine)
        result['summary'] = summarize_trace(result)
        report = {'schema':'aliquot-exponent-vectors-v1', 'primeCertificates':engine.export_certificates(),
                  'traces':[result], 'limits':{'maxSteps':256,'maxSourceBits':256,'maxDivisors':200000}}
        negative = deepcopy(report)
        t = negative['traces'][0]
        t.update(seed=str(-2**300), end=str(-2**300), status='source_bit_limit',
                 rows=[], factorBenchmarks=[], steps=0, cycleStart=None)
        t['summary'] = summarize_trace(t)
        with self.assertRaises(ValueError):
            verify_report(negative)
        oversized = deepcopy(report)
        oversized['traces'] *= MAX_TRACES + 1
        with self.assertRaises(ValueError):
            verify_report(oversized)
        with tempfile.NamedTemporaryFile() as source:
            source.truncate(MAX_REPORT_BYTES + 1)
            source.flush()
            out, err = io.StringIO(), io.StringIO()
            with redirect_stdout(out), redirect_stderr(err):
                self.assertEqual(main(['verify-vectors',source.name]), 1)
            self.assertEqual(out.getvalue(), '')
            self.assertIn('input budget', err.getvalue())

    def test_sparse_failure_preserves_stripping_work(self):
        # Certify 30, then force its successor's residual-7 factor call to fail.
        engine = CertifiedFactorizer()
        original = engine.factor
        calls = 0
        def bounded(n):
            nonlocal calls
            calls += 1
            if calls == 2:
                engine.last_work = engine.max_work
                raise ComputationLimit('forced residual limit')
            return original(n)
        with patch.object(engine, 'factor', side_effect=bounded):
            result = trace(30, engine)
        self.assertEqual(result['status'], 'factorization_limit')
        failed = result['factorBenchmarks'][-1]
        self.assertEqual(failed['sparseStatus'], 'factorization_limit')
        self.assertGreater(failed['strippingDivisions'], 0)
        self.assertEqual(failed['residual'], '7')
        self.assertEqual(failed['sparseWork'], engine.max_work)

    def test_census_and_committed_reproducibility(self):
        report = json.loads((ROOT/'research/results/exponent-vectors.json').read_text())
        self.assertEqual(vector_report(), report)
        self.assertTrue(verify_report(report))
        self.assertEqual(report['census']['normTrends']['l2Squared'], {'down':5472,'same':1970,'up':2557})
        self.assertEqual(report['census']['integerMidpointPairs'], 729)
        self.assertEqual(report['census']['evenToOdd'], 120)
        for result in report['traces'][:5]:
            self.assertEqual(result['status'], 'factorization_limit')
            self.assertGreater(result['steps'], result['trialBaseline']['steps'])
            self.assertTrue(result['summary']['projectionCollisions'])
        self.assertEqual(vector_census(1)['sources'], 0)

    def test_extended_report_and_certified_driver_loss(self):
        report = json.loads((ROOT/'research/results/exponent-vectors-extended.json').read_text())
        self.assertEqual(vector_report(max_steps=512, max_work=2_000_000), report)
        self.assertTrue(verify_report(report))
        self.assertEqual([t['steps'] for t in report['traces'][:5]], [348,130,231,167,189])
        orbit = report['traces'][0]
        p = 36558448886730575315885537
        row = orbit['rows'][169]
        self.assertEqual(row['factors'], [['2',2],['7',2],[str(p),1]])
        self.assertEqual(p % 8, 1)
        self.assertEqual(int(row['n']), 196*p)
        self.assertEqual(int(row['next']), 7*57*(p+1) - 196*p)
        self.assertEqual(orbit['rows'][170]['projection'][0], 1)
        self.assertEqual(orbit['summary']['longestExact28DriverRun'], 162)
        self.assertTrue(any(proof['prime'] == str(p) for proof in report['primeCertificates']))
        self.assertEqual(report['traces'][4]['rows'][173]['projection'][0], 5)

    def test_invalid_domains_and_cli_atomicity(self):
        for bad in [0, True, -1, 2.5, '4']:
            with self.assertRaises(ValueError):
                divisor_residue_counts(((2,1),), bad)
            with self.assertRaises(ValueError):
                vector_census(bad)
        for factors in [((1,1),), ((2,0),), ((2,True),), ((3,1),(2,1))]:
            with self.assertRaises(ValueError):
                aliquot_mod(factors, 12)
        with self.assertRaises(ValueError):
            divisor_residue_counts(((2,1),), 257)
        with self.assertRaises(ComputationLimit):
            independent_sum(((2,100),), max_divisors=10)
        for command, patched in [('vectors','vector_report'), ('verify-vectors','verify_report')]:
            out, err = io.StringIO(), io.StringIO()
            args = [command] if command == 'vectors' else [command, str(ROOT/'research/results/exponent-vectors.json')]
            with patch('aliquot.__main__.'+patched, side_effect=ArithmeticError('broken')):
                with redirect_stdout(out), redirect_stderr(err):
                    self.assertEqual(main(args), 1)
            self.assertEqual(out.getvalue(), '')
            self.assertIn('broken', err.getvalue())
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            self.assertEqual(main(['vectors','--bound','10','--steps','2','--trial-work','100']), 0)
        self.assertEqual(json.loads(out.getvalue())['limits']['maxSteps'], 2)
