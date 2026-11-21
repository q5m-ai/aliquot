"""Exact fixed-seed evidence for ODD-EXIT-FIXED-SEEDS.md; no density sampling."""

from itertools import product
from math import gcd, prod
import unittest

from aliquot import aliquot_sum
from aliquot.certified import CertifiedFactorizer, verify_certificates, verify_factor_product
from aliquot.two_adic import _divisor_pair_sum


SMALL_PATH = (833_054_562, 972_162_345, 972_874_455, 867_445_545, 525_211_287,
              175_070_433, 58_356_815, 18_037_633, 1, 0)
LARGE_PATH = (
    47_448_036_801_789_169_203_522, 55_356_042_937_423_035_814_545,
    59_811_450_742_194_475_379_055, 72_148_413_360_211_836_230_289,
    43_351_928_018_631_568_876_911, 24_244_433_720_275_683_592_593,
    11_722_945_225_843_364_937_327, 5_659_813_693_411_025_885_073,
    2_730_446_413_203_158_949_487, 417_026_709_833, 280_449_847, 33_713, 1, 0,
)


class OddExitFixedSeedTests(unittest.TestCase):
    def test_three_step_counterexample_terminates(self):
        self.assertEqual(SMALL_PATH[0], 18 * 6803**2)
        for source, target in zip(SMALL_PATH, SMALL_PATH[1:]):
            self.assertEqual(aliquot_sum(source), target)
            self.assertEqual(_divisor_pair_sum(source), target)
        self.assertEqual(next(j for j, n in enumerate(SMALL_PATH) if n < SMALL_PATH[0]), 4)
        self.assertEqual((len(SMALL_PATH) - 1, SMALL_PATH[-2:]), (9, (1, 0)))

    def test_growing_seed_smaller_predecessor_and_termination(self):
        engine = CertifiedFactorizer(max_work=2_000_000, max_bits=96)
        p, d, q = 51_342_010_523, 11_394, 3_378_046_191_213_809_567
        self.assertEqual(engine.factor(p), ((p, 1),))
        self.assertEqual(engine.factor(q), ((q, 1),))
        self.assertEqual(p % 32340, 29063)
        self.assertEqual(gcd(d, q), 1)
        self.assertEqual(_divisor_pair_sum(d), 14_046)
        seed = LARGE_PATH[0]
        self.assertEqual(seed, 18 * p**2)
        self.assertEqual(seed, 14_046 * q + 25_440)
        self.assertLess(d * q, seed)

        # Split the two known inputs by construction. Unknown orbit terms must
        # factor fully within budget. A work-limit exception never passes a test.
        chain = (d * q,) + LARGE_PATH
        factors = [engine.factor(d) + ((q, 1),), engine.factor(18) + ((p, 2),)]
        factors.extend(engine.factor(n) for n in LARGE_PATH[1:-1])
        proven = verify_certificates(engine.export_certificates())
        for source, target, fs in zip(chain[:-1], chain[1:], factors, strict=True):
            verify_factor_product(fs, source)
            self.assertTrue(all(prime in proven for prime, _ in fs))
            # Independent of a geometric-series divisor-sum formula.
            powers = [[prime**k for k in range(e + 1)] for prime, e in fs]
            self.assertEqual(sum(prod(v) for v in product(*powers)) - source, target)
        self.assertEqual(next(j for j, n in enumerate(LARGE_PATH) if n < seed), 4)
        self.assertEqual((len(LARGE_PATH) - 1, LARGE_PATH[-2:]), (13, (1, 0)))

    def test_simple_root_lifts_and_sign_transport(self):
        # At the split prime 17, the 2/r local fraction counts exact divisibility.
        r = 17
        a = lambda t: 7 * t**2 + 13 * t + 13
        roots = [b for b in range(1, r) if a(b) % r == 0]
        self.assertEqual(roots, [9, 11])
        for b in roots:
            self.assertEqual(sum(a(b + k * r) % (r**2) != 0 for k in range(r)), r - 1)
        # Two signs on the same certified orbit, not reselected parameters.
        t = LARGE_PATH[1]
        for j, d in ((1, 5355), (2, 5985), (3, 5355)):
            term, proper = LARGE_PATH[j], _divisor_pair_sum(d)
            sigma = d + proper
            self.assertEqual((term - (-1)**(j-1) * t) % 19, 0)
            self.assertEqual((term - sigma) % 19, 0)
            self.assertNotEqual(proper % 19, 0)
            self.assertGreater(term, proper * 19 + sigma)
