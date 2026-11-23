"""First-counterexample search for the three-step claim in ODD-EXIT-DESCENT.md."""

from collections import Counter
import unittest

from aliquot import ComputationLimit, aliquot_sum, factorize
from aliquot.two_adic import _divisor_pair_sum

PRIME_CAP = 50_000
SOURCE_CAP = 10**12
STEPS = 3
WITNESS = [833_054_562, 972_162_345, 972_874_455, 867_445_545]


def trace(seed):
    """Stop at the first event. A work or source limit is NOT an outcome."""
    path = [seed]
    for _ in range(STEPS):
        n = path[-1]
        if n > SOURCE_CAP:
            raise ComputationLimit(f"Unresolved source above cap: {n}")
        nxt = aliquot_sum(n)
        if nxt != _divisor_pair_sum(n):
            raise ArithmeticError(f"Independent divisor-pair sum disagrees at {n}")
        path.append(nxt)
        if nxt == 0:
            return path, "zero"
        if nxt in path[:-1]:
            return path, "repeat"
        if nxt < seed:
            return path, "below"
    return path, "no event"


class OddExitDescentTests(unittest.TestCase):
    def test_stopping_controls(self):
        self.assertEqual(trace(1), ([1, 0], "zero"))
        self.assertEqual(trace(6), ([6, 6], "repeat"))
        self.assertEqual(trace(220), ([220, 284, 220], "repeat"))
        self.assertEqual(trace(18 * 11**2), ([2178, 3009, 1311], "below"))

    def test_first_counterexample(self):
        descents = Counter()
        for p in range(11, PRIME_CAP + 1, 12):
            prime = factorize(p) == [(p, 1)]
            self.assertEqual(prime, _divisor_pair_sum(p) == 1, p)
            if not prime:
                continue
            path, outcome = trace(18 * p**2)
            a = 7 * p**2 + 13 * p + 13
            self.assertEqual(path[1], 3 * a)
            self.assertEqual(path[2], a + 4 * aliquot_sum(a))
            steps = len(path) - 1
            self.assertEqual([n % 4 for n in path[1:]], [1, 3, 1][:steps])
            if outcome == "no event":
                self.assertEqual((p, path), (6803, WITNESS))
                break
            self.assertEqual(outcome, "below")
            descents[steps] += 1
        else:
            self.fail("No counterexample found within the prime cap")
        self.assertEqual(descents, {2: 212, 3: 5})

    def test_factors_in_certificate(self):
        self.assertEqual([factorize(n) for n in WITNESS[:-1]], [
            [(2, 1), (3, 2), (6803, 2)],
            [(3, 1), (5, 1), (7, 1), (11, 1), (401, 1), (2099, 1)],
            [(3, 1), (5, 1), (7, 1), (29, 1), (319499, 1)],
        ])
