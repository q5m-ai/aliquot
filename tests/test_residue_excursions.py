"""Finite arithmetic in note 18. Graph paths may change integer witnesses."""

from math import isqrt
import unittest

from aliquot import aliquot_sum
from aliquot.research import divisor_sieve


def pair_sum(n):
    return sum(d + (n // d if d * d != n else 0)
               for d in range(1, isqrt(n) + 1) if n % d == 0) - n


def reachable_from_one(graph):
    seen = {1}
    todo = [1]
    while todo:
        new = graph[todo.pop()] - seen
        seen.update(new)
        todo.extend(new)
    return seen


class ResidueExcursionTests(unittest.TestCase):
    def test_connectivity_with_only_observed_above_cutoff_edges(self):
        # The finite subgraph suffices for these M, not for all M or all cutoffs.
        sums = divisor_sieve(8192)
        for n in range(64, 8193):
            self.assertEqual(sums[n], aliquot_sum(n))
        for modulus in (2, 4, 8, 9, 12, 36, 72, 160, 800):
            with self.subTest(modulus=modulus):
                forward = [set() for _ in range(modulus)]
                reverse = [set() for _ in range(modulus)]
                for n in range(64, 8193):
                    if sums[n] >= 64:
                        a, b = n % modulus, sums[n] % modulus
                        forward[a].add(b)
                        reverse[b].add(a)
                vertices = set(range(modulus))
                self.assertEqual(reachable_from_one(forward), vertices)
                self.assertEqual(reachable_from_one(reverse), vertices)

    def test_steering_and_sign_at_two(self):
        # From 6 mod 8 the odd part is 3 mod 4; its sigma supplies 4.
        # Negating the class first, rather than trying to zero it directly, works.
        for n in range(6, 1024, 8):
            self.assertNotEqual(pair_sum(n) % 8, 0)
        self.assertEqual((pair_sum(14), pair_sum(10)), (10, 8))
        # Equation (1) at an odd component: sigma(42)=96, t=4.
        n = 42 * 37**3
        self.assertEqual(n % 36, 6)
        self.assertEqual(aliquot_sum(n), pair_sum(n))
        self.assertEqual(pair_sum(n) % 36, (4 * 96 - 42) % 36)
        self.assertEqual(pair_sum(n) % 36, 18)

    def test_mod_36_graph_witnesses_need_not_concatenate(self):
        edges = [(30, 42), (42, 54), (90, 144)]
        self.assertEqual([(n % 36, m % 36) for n, m in edges],
                         [(30, 6), (6, 18), (18, 0)])
        for n, m in edges:
            self.assertEqual(pair_sum(n), m)
        self.assertEqual(pair_sum(54), 66)  # does not take the 18 -> 0 arrow

    def test_symmetric_exit_on_one_ordinary_orbit(self):
        path = [960498, 1791405, 2192211]
        self.assertEqual([n % 12 for n in path], [6, 9, 3])
        for n, m in zip(path, path[1:]):
            self.assertEqual(aliquot_sum(n), m)
            self.assertEqual(pair_sum(n), m)
            self.assertGreater(5 * m, 6 * n)
        control = [18, 21, 11, 1, 0]
        for n, m in zip(control, control[1:]):
            self.assertEqual(pair_sum(n), m)

    def test_same_160_core_signature_does_not_decide_successor_membership(self):
        # Both start at residue 1440, sigma residue 0. Their clean successors
        # have the same value residue but different divisor-sum residues.
        for n, m, sigma_mod in ((767840, 1046560, 1152),
                                (27775840, 37844960, 0)):
            with self.subTest(source=n):
                self.assertEqual(pair_sum(n), m)
                self.assertEqual(aliquot_sum(n), m)
                self.assertEqual((n % 1600, (n + m) % 1600), (1440, 0))
                self.assertEqual(m % 1600, 160)
                self.assertEqual((m + pair_sum(m)) % 1600, sigma_mod)
                self.assertEqual(m + pair_sum(m), 378 * (m // 160 + pair_sum(m // 160)))

    def test_first_image_relay_without_factoring_the_image(self):
        modulus, d, r, exponent = 5, 400, 1536641, 43655
        k = modulus * 2**4 * 7**4
        self.assertEqual(r, 8 * k + 1)
        self.assertTrue(all(r % i for i in range(2, isqrt(r) + 1)))
        self.assertEqual(exponent % modulus, 0)
        sigma_d = d + pair_sum(d)
        self.assertEqual(sigma_d, 961)
        # Independent of r == 1 simplification: division by r-1 is not a
        # modular inverse. Reduce the numerator modulo k*(r-1) before dividing.
        numerator = pow(r, exponent + 1, k * (r - 1)) - 1
        sigma_r, remainder = divmod(numerator, r - 1)
        self.assertEqual(remainder, 0)
        first = (sigma_d * sigma_r - d * pow(r, exponent, k)) % k
        self.assertEqual(first, (sigma_d * (exponent + 1) - d) % k)
        self.assertEqual(first, 79576)
        self.assertEqual((first % 5, first % 16, first % 2401), (1, 8, 343))
        # 7^3 is unitary, so its sigma divides the unknown full sigma.
        sigma_343 = 343 + pair_sum(343)
        self.assertEqual(sigma_343 % (5 * 16), 0)
        self.assertEqual(((-first) % 5, (-first) % 16), (4, 8))
        for guaranteed_divisor in (d, 8 * 343):
            self.assertGreater(7 * pair_sum(guaranteed_divisor),
                               8 * guaranteed_divisor)

    def test_nonsymmetric_complement_cannot_be_visited_twice(self):
        for n in range(3, 1024, 4):
            self.assertEqual(pair_sum(n) % 4, 1)
