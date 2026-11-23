"""Exact finite witnesses for SIX-28-HIGHER-RETURN.md; not a density experiment."""

import json
from math import gcd, isqrt
from pathlib import Path
import unittest

from aliquot import aliquot_sum
from aliquot.two_adic import _divisor_pair_sum


def prime(n):
    return n > 1 and all(n % d for d in range(2, isqrt(n) + 1))


def checkpoint(n):
    p, remainder = divmod(n, 28)
    return remainder == 0 and p % 84 == 13 and prime(p)


def bridge(n):
    r, remainder = divmod(n//28 + 2, 27)
    return checkpoint(n) and remainder == 0 and r % 84 == 13 and prime(r) and prime(53*r+80)


class Six28HigherReturnTests(unittest.TestCase):
    def path(self, n, edges, cap):
        values = [n]
        for _ in range(edges):
            self.assertTrue(0 < n <= cap)
            y = aliquot_sum(n)
            self.assertEqual(_divisor_pair_sum(n), y)
            values.append(y)
            n = y
        return values

    def test_same_checkpoint_on_the_actual_276_orbit(self):
        seq = self.path(276, 44, 10**10)
        self.assertEqual(seq[4:10], [1872, 3770, 3790, 3050, 2716, 2772])
        self.assertEqual([(j, x) for j, x in enumerate(seq) if checkpoint(x)],
                         [(8, 28*97), (44, 28*333_716_809)])
        self.assertEqual(seq[-1], 9_344_070_652)
        self.assertFalse(bridge(seq[8]))  # The general return need not take two steps.
        self.assertFalse(bridge(seq[44]))
        # Separate published-only checkpoint test, not a factor replay up to 170.
        src = Path(__file__).resolve().parents[1] / 'research/results/lehmer-276-published-prefix.json'
        excerpt = [int(x) for x in json.loads(src.read_text())['terms']]
        candidates = [(i, x, y) for i, (x, y) in enumerate(zip(excerpt, excerpt[1:]))
                      if x % 2352 == 364]
        self.assertEqual([i for i, _, _ in candidates], [8, 44, 52, 58, 134, 136, 152])
        self.assertEqual([i for i, x, y in candidates if y-x == 56], [8, 44])
        for i in (8, 44):
            self.assertEqual(gcd(seq[i]//28, seq[i-1]), 1)

    def test_two_successive_bridges_and_the_denominator_they_spend(self):
        seq = self.path(327_292, 4, 1_300_000)
        self.assertEqual(seq, [327_292, 327_348, 644_812, 644_868, 1_268_092])
        self.assertEqual([j for j, n in enumerate(seq) if checkpoint(n)], [0, 2, 4])
        self.assertEqual([j for j, n in enumerate(seq) if bridge(n)], [0, 2])
        for j, r in ((0, 433), (2, 853)):
            self.assertEqual(seq[j:j+3], [28*(27*r-2), 28*27*r, 28*(53*r+80)])
            self.assertTrue(all(prime(x) for x in (r, 27*r-2, 53*r+80)))
        self.assertEqual(27*(13*853+41), 53*(13*433+41))
        self.assertTrue((13*433+41) % 3**4 == 0 and (13*433+41) % 3**5 != 0)
        self.assertTrue((13*853+41) % 3 == 0 and (13*853+41) % 9 != 0)

    def test_return_then_no_later_checkpoint_even_with_unlimited_waiting(self):
        r = 6397
        seq = self.path(28*(27*r-2), 34, 19_372_486)
        self.assertEqual(seq[:3], [4_836_076, 4_836_132, 9_495_388])
        self.assertEqual(seq[-5:], [3053, 115, 29, 1, 0])
        self.assertEqual(max(seq), 19_372_486)
        self.assertEqual([j for j, n in enumerate(seq) if checkpoint(n)], [0, 2])
        self.assertEqual([j for j, n in enumerate(seq) if bridge(n)], [0])
        self.assertEqual(seq[2]//28, 53*r+80)

    def test_fixed_launch_fails_even_with_squareclass_and_exact_core_exponents(self):
        for q, edges, larger in ((5, 21, [128_102, 80_518]), (11, 27, [523_874, 322_426])):
            x = 1872*q*q
            seq = self.path(x, edges, max(larger))
            self.assertEqual(seq[-1], 0)
            self.assertEqual([y for y in seq if y > x], larger)
            self.assertTrue(all(y % 6 and y % 28 for y in larger))
            self.assertTrue(prime(q) and 1872 % q != 0)
        self.assertEqual(1872, 2**4 * 3**2 * 13)

    def test_same_switch_after_two_drops_can_enter_an_amicable_cycle(self):
        seq = self.path(144*5323, 31, 4_163_392)
        self.assertTrue(prime(5323))
        self.assertEqual(seq[:6], [766_512, 1_379_060, 1_573_876, 1_211_984, 1_153_936, 1_401_456])
        self.assertEqual([(x%6 == 0, x%28 == 0) for x in seq[:6]],
                         [(True, False)] + [(False, False)]*3 + [(False, True), (True, True)])
        self.assertTrue(seq[2] > seq[3] > seq[4] > seq[0])
        self.assertEqual(seq[-3:], [1210, 1184, 1210])
        self.assertEqual(len(set(seq[:-1])), len(seq)-1)

    def test_local_obstructions_when_the_three_exponent_varies(self):
        # Modulo 7 a C-to-C step with a prime remainder requires mr=1,
        # (3m-1)(r+1)=0. Modulo 3 the remainder must be 1, not 5.
        allowed = {a for a in range(6) if any((3**a*r - 1) % 7 == 0
                   and ((3*3**a-1)*(r+1)) % 7 == 0 for r in range(1, 7))}
        self.assertEqual(allowed, {3, 5})
        self.assertEqual([r for r in (1, 2) if (-r-1) % 3 == 1], [1])
        for r in range(5):
            self.assertEqual(((2*3-1)*r + 3*3+1) % 5, 0)
        self.assertEqual({a for a in range(12) if a%6 in allowed and a%4 != 1}, {3, 11})
        self.assertEqual(pow(3, 3, 13), 1)
        for p in range(13):
            self.assertEqual({(p+4*j) % 13 for j in range(13)}, set(range(13)))

    def test_affine_first_images_and_supply_at_one_later_step(self):
        for p in (5, 11, 13, 19, 181, 5323):
            self.assertTrue(prime(p))
            m = _divisor_pair_sum(144*p)
            self.assertEqual(m, 259*p+403)
            self.assertEqual(m%7, 4)
            self.assertEqual(m%6 == 0, p%3 == 2)
            self.assertGreater(m, 144*p)
        # An upper supplying prime keeps a lower mark exact; this is a single
        # witness, not a numerical validation of a limiting prime proportion.
        p, lo, hi = 850_093, 5, 2099
        self.assertTrue(all(prime(n) for n in (p, lo, hi)))
        self.assertEqual((p % 84, (hi+1) % (84*lo**2)), (13, 0))
        _, m, y = self.path(28*p, 2, 24_000_000)
        self.assertEqual((m, y), (23_802_660, 61_574_940))
        self.assertEqual((gcd(m, hi**2), gcd(m, lo**2), gcd(y, lo**2)), (hi, lo, lo))
        self.assertEqual((m % 84, y % 84), (0, 0))
