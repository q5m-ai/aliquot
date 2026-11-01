"""Exact bounded regressions for the maximum-based contradiction attempt.

No finite check here establishes an escaping orbit or universal boundedness.
Every evaluated positive source is <= 40,000; every orbit run has at most
100 transitions. Each aliquot edge has an independent divisor-pair check.
"""

from functools import lru_cache
from math import isqrt
import unittest

from aliquot import ComputationLimit, aliquot_sum

SOURCE_CAP = 40_000
STEP_CAP = 100
INTERVAL_BOUND = 1000
PRIME_PARAMETER_BOUND = 10_000


@lru_cache(None)
def checked_sum(n):
    if type(n) is not int or n < 1:
        raise ValueError("Only positive integer sources are defined")
    if n > SOURCE_CAP:
        raise ComputationLimit("Source cap exceeded; computation unresolved")
    actual = aliquot_sum(n)
    independent = sum(
        d + (n // d if d * d != n else 0)
        for d in range(1, isqrt(n) + 1) if n % d == 0
    ) - n
    if actual != independent:
        raise ArithmeticError("Independent divisor-pair sum disagrees")
    return actual


def bounded_orbit(seed, *, max_steps=STEP_CAP):
    """Resolve a small orbit, or fail explicitly rather than infer its fate."""
    if type(seed) is not int or seed < 1:
        raise ValueError("Expected a positive integer seed")
    if type(max_steps) is not int or not 1 <= max_steps <= STEP_CAP:
        raise ValueError("Step limit must be within the declared test budget")
    path, seen = [seed], {seed}
    for _ in range(max_steps):
        target = checked_sum(path[-1])
        path.append(target)
        if target == 0:
            return "terminated", path
        if target in seen:
            return "cycled", path
        seen.add(target)
    raise ComputationLimit("Step cap exceeded; computation unresolved")


class MaximumContradictionTests(unittest.TestCase):
    def test_named_complete_orbits_and_peak_conditions(self):
        expected = {
            6: ("cycled", [6, 6]),
            18: ("terminated", [18, 21, 11, 1, 0]),
            24: ("terminated", [24, 36, 55, 17, 1, 0]),
            30: ("terminated", [30, 42, 54, 66, 78, 90, 144, 259,
                                45, 33, 15, 9, 4, 3, 1, 0]),
            60: ("terminated", [60, 108, 172, 136, 134, 70, 74, 40,
                                50, 43, 1, 0]),
            220: ("cycled", [220, 284, 220]),
            784: ("terminated", [784, 983, 1, 0]),
            844: ("terminated", [844, 640, 890, 730, 602, 454, 230,
                                 202, 104, 106, 56, 64, 63, 41, 1, 0]),
        }
        for seed, result in expected.items():
            with self.subTest(seed=seed):
                status, path = bounded_orbit(seed)
                self.assertEqual((status, path), result)
                self.assertLess(max(path), 1000)
                peak = max(path)
                self.assertLessEqual(checked_sum(peak), peak)
                _, tail = bounded_orbit(peak)
                self.assertLessEqual(set(tail), set(path))
                self.assertEqual(max(tail), peak)
                if peak != 6:
                    self.assertNotEqual(peak % 6, 0)

    def test_no_large_interval_is_closed_with_explicit_witnesses(self):
        closed_endpoints = []
        largest_image = 0
        for bound in range(1, INTERVAL_BOUND + 1):
            largest_image = max(largest_image, checked_sum(bound))
            if largest_image <= bound:
                closed_endpoints.append(bound)
            if bound < 24:
                continue
            witness = 24 if bound < 36 else 12 * (bound // 12)
            self.assertLessEqual(witness, bound)
            self.assertGreater(checked_sum(witness), bound)
            if bound >= 36:
                q = bound // 12
                divisors = {q, 2*q, 3*q, 4*q, 6*q}
                self.assertEqual(len(divisors), 5)
                self.assertTrue(all(witness % d == 0 and d < witness
                                    for d in divisors))
                self.assertEqual(sum(divisors), 16*q)
                self.assertGreater(16*q, bound)
                self.assertGreaterEqual(checked_sum(witness), 16*q)
        self.assertEqual(closed_endpoints, [*range(1, 12), 16, 17, 22, 23])

    def test_finite_cohort_closure_is_not_an_interval(self):
        visited = set()
        for seed in range(1, 25):
            _, path = bounded_orbit(seed)
            visited.update(path)
        self.assertEqual(visited, set(range(25)) | {36, 55})
        self.assertEqual(max(visited), 55)
        for source in visited - {0}:
            self.assertIn(checked_sum(source), visited)
        self.assertNotIn(48, visited)
        self.assertLess(48, max(visited))
        self.assertEqual(checked_sum(48), 76)
        self.assertGreater(checked_sum(48), max(visited))

        # Filling the gaps introduces new seeds, unlike following old labels.
        bound = 24
        envelope = [bound]
        for _ in range(4):
            bound = max(bound, max(checked_sum(n) for n in range(1, bound + 1)))
            envelope.append(bound)
        self.assertEqual(envelope, [24, 36, 55, 76, 123])
        self.assertGreater(envelope[-1], max(visited))

    def test_two_step_peak_exclusion_in_the_declared_prime_range(self):
        self.assertEqual(checked_sum(160), 218)
        primes = [q for q in range(51, PRIME_PARAMETER_BOUND + 1, 160)
                  if checked_sum(q) == 1]
        self.assertIn(211, primes)
        for q in primes:
            with self.subTest(q=q):
                source = 4*q
                middle = checked_sum(source)
                target = checked_sum(middle)
                self.assertEqual(middle, 3*q + 7)
                self.assertLess(middle, source)
                self.assertEqual(middle % 160, 0)
                self.assertGreaterEqual(160*target, 218*middle)
                self.assertGreater(320*target, 327*source)
                self.assertGreater(target, source)

    def test_profitable_recovery_does_not_regenerate_its_input_class(self):
        _, path = bounded_orbit(844)
        self.assertEqual(path[:3], [844, 640, 890])
        self.assertEqual(max(path), 890)
        self.assertNotEqual(890 % 4, 0)
        larger_visits = [n for n in path if n > 844]
        self.assertEqual(larger_visits, [890])
        # Thus no later larger return to the 4q family exists in this orbit.

    def test_divisibility_does_not_order_orbit_peaks(self):
        self.assertEqual(60 % 30, 0)
        self.assertGreaterEqual(checked_sum(60), 2*checked_sum(30))
        _, divisor_orbit = bounded_orbit(30)
        _, multiple_orbit = bounded_orbit(60)
        self.assertEqual(max(divisor_orbit), 259)
        self.assertEqual(max(multiple_orbit), 172)
        self.assertGreater(max(divisor_orbit), max(multiple_orbit))
        self.assertNotIn(30, multiple_orbit)

    def test_abundant_start_can_have_a_prime_peak(self):
        self.assertEqual(checked_sum(784), 983)
        self.assertGreater(983, 784)
        self.assertEqual(checked_sum(983), 1)
        self.assertTrue(all(983 % d for d in range(2, isqrt(983) + 1)))

    def test_proper_perfect_multiples_are_not_peak_candidates(self):
        for perfect in (6, 28):
            self.assertEqual(checked_sum(perfect), perfect)
            for source in range(2*perfect, INTERVAL_BOUND + 1, perfect):
                self.assertGreater(checked_sum(source), source)

    def test_limits_are_unresolved_and_zero_is_not_evaluated(self):
        for invalid in (0, -1, 1.5):
            with self.assertRaises(ValueError):
                checked_sum(invalid)
            with self.assertRaises(ValueError):
                bounded_orbit(invalid)
        with self.assertRaises(ComputationLimit):
            checked_sum(SOURCE_CAP + 1)
        with self.assertRaises(ComputationLimit):
            bounded_orbit(SOURCE_CAP + 1)
        with self.assertRaises(ComputationLimit):
            bounded_orbit(24, max_steps=2)
        for invalid in (0, STEP_CAP + 1):
            with self.assertRaises(ValueError):
                bounded_orbit(24, max_steps=invalid)
        self.assertEqual(bounded_orbit(1, max_steps=1), ("terminated", [1, 0]))
        self.assertEqual(bounded_orbit(6, max_steps=1), ("cycled", [6, 6]))


if __name__ == "__main__":
    unittest.main()
