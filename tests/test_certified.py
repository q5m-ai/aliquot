from copy import deepcopy
from math import prod
import unittest
from unittest.mock import patch

from aliquot import ComputationLimit, factorize
from aliquot.certified import (
    Budget, CertifiedFactorizer, MAX_CERTIFICATES, decode_factors,
    verify_certificates, verify_factor_product,
)


class CertifiedFactorizationTests(unittest.TestCase):
    def test_exhaustive_small_inputs_and_proof_replay(self):
        engine = CertifiedFactorizer()
        for n in range(1, 5001):
            self.assertEqual(engine.factor(n), tuple(factorize(n)))
        known = verify_certificates(engine.export_certificates())
        self.assertEqual(known, set(engine.certificates))

    def test_large_certified_primes_and_semiprime(self):
        engine = CertifiedFactorizer()
        for n in [1000000007 * 1000000009, 2**89 - 1, 2**127 - 1]:
            factors = engine.factor(n)
            self.assertEqual(prod(p**e for p, e in factors), n)
            known = verify_certificates(engine.export_certificates())
            self.assertTrue(all(p in known for p, _ in factors))
        self.assertEqual(engine.factor(1000000007 * 1000000009),
                         ((1000000007, 1), (1000000009, 1)))
        self.assertEqual(engine.factor(2**127 - 1), ((2**127 - 1, 1),))

    def test_pseudoprimes_are_never_accepted(self):
        engine = CertifiedFactorizer()
        for n in [341, 561, 1105, 1729, 2047, 1373653, 3215031751]:
            self.assertEqual(engine.factor(n), tuple(factorize(n)))
            self.assertNotIn(n, engine.certificates)
        # Passing a probabilistic screen cannot by itself certify a candidate.
        with patch('aliquot.certified._screen', return_value=True):
            with patch.object(engine, '_certify', side_effect=ComputationLimit('unresolved')):
                with self.assertRaises(ComputationLimit):
                    engine.factor(1009 * 1013)
        self.assertNotIn(1009 * 1013, engine.certificates)

    def test_budget_caps_cache_and_fork(self):
        with self.assertRaises(ComputationLimit):
            CertifiedFactorizer(max_work=1).factor(1009)
        with self.assertRaises(ComputationLimit):
            CertifiedFactorizer(max_bits=64).factor(2**64)
        engine = CertifiedFactorizer()
        engine.factor(1009)
        clone = engine.fork()
        clone.factor(1013)
        self.assertNotIn(1013, engine.certificates)
        self.assertIn(1013, clone.certificates)
        engine.factor(1009)
        self.assertEqual(engine.last_work, 0)
        self.assertEqual(engine.factor(1), ())
        for a, e, n in [(3, 10, 8), (17, 33, 101), (2, 100, 91)]:
            budget = Budget(1000)
            self.assertEqual(budget.power(a, e, n), pow(a, e, n))
            self.assertGreater(budget.used, 0)

    def test_certificate_corruption_fails_closed(self):
        engine = CertifiedFactorizer()
        engine.factor(1009)
        original = engine.export_certificates()
        self.assertIn(1009, verify_certificates(original))
        for mutation in ['witness', 'product', 'missing', 'order', 'trial', 'composite']:
            rows = deepcopy(original)
            if mutation == 'witness':
                rows[-1]['witnesses'][0][1] = '1'
            elif mutation == 'product':
                rows[-1]['factors'][0][1] += 1
            elif mutation == 'missing':
                rows = rows[1:]
            elif mutation == 'order':
                rows = list(reversed(rows))
            elif mutation == 'trial':
                rows[-1] = {'prime': '1009', 'kind': 'trial'}
            else:
                rows = [{'prime': '9', 'kind': 'trial'}]
            with self.subTest(mutation=mutation):
                with self.assertRaises((ValueError, ArithmeticError)):
                    verify_certificates(rows)

    def test_replay_aggregate_limits_and_bounded_product_check(self):
        with self.assertRaises(ValueError):
            verify_certificates([{'prime':'2','kind':'trial'}] * (MAX_CERTIFICATES + 1))
        with self.assertRaises(ValueError):
            decode_factors([['2',1]] * 513)
        with self.assertRaises(ArithmeticError):
            verify_factor_product(((2,10**12),), 1008)
        with self.assertRaises(ArithmeticError):
            verify_factor_product(((2**511-1,512),), 1008)
        self.assertIsNone(verify_factor_product(((2,4),(3,2)),144))
        engine = CertifiedFactorizer()
        with patch.object(engine, '_factor', side_effect=RecursionError('depth')):
            with self.assertRaises(ComputationLimit):
                engine.factor(1009)

    def test_invalid_domains(self):
        for bad in [0, -1, True, '10', 1.2]:
            with self.assertRaises(ValueError):
                CertifiedFactorizer().factor(bad)
            with self.assertRaises(ValueError):
                CertifiedFactorizer(max_work=bad)
        for bad in [0, 513, True]:
            with self.assertRaises(ValueError):
                CertifiedFactorizer(max_bits=bad)
        for rows in [[['2', 0]], [['2', True]], [['02', 1]], [['3', 1], ['2', 1]], [['2', 1], ['2', 1]]]:
            with self.assertRaises(ValueError):
                decode_factors(rows)
