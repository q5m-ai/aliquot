"""Finite checks of composite fresh handoffs, not perpetual renewal.

Ordinary sources <= 20,000,000,000,000; prime candidates <= 200,000,000,000;
paths <= 4 edges. Powered bases w <= 31, outer exponents E <= 110,499,863,998.
Symbolic checks never expand the huge powered source or presume its image prime.
"""

from fractions import Fraction
from functools import lru_cache
from math import gcd, isqrt, prod
import unittest

from aliquot import ComputationLimit, aliquot_sum, factorize
from aliquot.exponent_vectors import aliquot_mod, geometric_mod

SOURCE_CAP = 20_000_000_000_000
PRIME_CAP = 200_000_000_000
STEP_CAP = 4
BASE_CAP = 31
EXPONENT_CAP = 110_499_863_998
MODULUS_CAP = 160 * 4799**2


def valuation(n, p):
    if type(n) is not int or n < 1 or type(p) is not int or p < 2:
        raise ValueError("Expected a positive integer and a base >= 2")
    e = 0
    while n % p == 0:
        n //= p
        e += 1
    return e


@lru_cache(None)
def checked_sigma(n):
    if type(n) is not int or n < 1:
        raise ValueError("Divisor sums require positive integer sources")
    if n > SOURCE_CAP:
        raise ComputationLimit("Source cap exceeded; computation unresolved")
    actual = n + aliquot_sum(n)
    independent = sum(
        d + (n // d if d*d != n else 0)
        for d in range(1, isqrt(n) + 1) if n % d == 0
    )
    if actual != independent:
        raise ArithmeticError("Independent divisor-pair sum disagrees")
    return actual


@lru_cache(None)
def checked_prime(n):
    if type(n) is not int or n < 2:
        raise ValueError("Prime candidates must be integers >= 2")
    if n > PRIME_CAP:
        raise ComputationLimit("Primality cap exceeded; computation unresolved")
    actual = factorize(n) == [(n, 1)]
    independent = all(n % d for d in range(2, isqrt(n) + 1))
    if actual != independent:
        raise ArithmeticError("Independent exhaustive primality check disagrees")
    return actual


def verify_path(path):
    if not 1 <= len(path)-1 <= STEP_CAP:
        raise ComputationLimit("Path cap exceeded; computation unresolved")
    for source, target in zip(path, path[1:]):
        if checked_sigma(source)-source != target:
            raise ArithmeticError("Named aliquot edge is incorrect")


def symbolic_sigma_mod(base, exponent, modulus):
    """Two exact modular methods; base factorization is independently certified."""
    for value in (base, exponent, modulus):
        if type(value) is not int or value < 1:
            raise ValueError("Symbolic parameters must be positive integers")
    if base > BASE_CAP or exponent > EXPONENT_CAP or modulus > MODULUS_CAP:
        raise ComputationLimit("Symbolic audit cap exceeded; computation unresolved")
    factors = factorize(base)
    if (prod(p**e for p, e in factors) != base
            or not all(checked_prime(p) for p, _ in factors)):
        raise ArithmeticError("Base factorization certificate is invalid")
    actual = independent = 1
    for p, e in factors:
        length = e*exponent + 1
        actual = actual * geometric_mod(p, length, modulus) % modulus
        # Reduce the numerator modulo M*(p-1), then divide in Z, not modulo M.
        # This remains valid when p-1 is not invertible modulo M.
        quotient = (pow(p, length, modulus*(p-1))-1) // (p-1)
        independent = independent * quotient % modulus
    if actual % modulus != independent % modulus:
        raise ArithmeticError("Independent modular geometric sum disagrees")
    return actual % modulus


def affine_coefficients(r):
    if r < 2 or r % 800 != 799:
        raise ValueError("Expected a supplier parameter congruent to -1 modulo 800")
    # Primality and actual bridge guards are checked separately, not inferred here.
    t = (r+1) // 800
    return (109*(1090*t+1), 189*(640000*t*t+290*t+1), 80*r)


class CompositeHandoffTests(unittest.TestCase):
    def test_exact_composite_correction_and_matching_condition(self):
        for r in (2399, 4799):
            self.assertTrue(checked_prime(r))
            a = (r+1) // 800
            A, B = 1890*a, 1090*a+1
            for v in range(1, BASE_CAP+1):
                if gcd(v, 10*r) != 1:
                    continue
                sigma = checked_sigma(v)
                actual = checked_sigma(160*r*v) - 160*r*v
                cofactor = A*sigma-r*v
                self.assertEqual(actual, 160*cofactor)
                self.assertEqual(cofactor, B*v+A*(sigma-v))
                self.assertEqual(cofactor-(B*v+A), A*(sigma-v-1))
                self.assertEqual(gcd(cofactor, 10), 1)
                self.assertGreaterEqual(80*actual, 109*160*r*v)
                # The matching identity holds for any invertible prime modulus;
                # only suppliers -1 mod800 certify the full Z guard.
                for R in (11, 13, 17):
                    if gcd(R, A*r*v) != 1:
                        continue
                    match = sigma*pow(v, -1, R) % R == r*pow(A, -1, R) % R
                    self.assertEqual(cofactor % R == 0, match)
        self.assertEqual(checked_sigma(9), 13)
        self.assertNotEqual((5670*13-2399*9) % 13, 0)

    def test_two_successive_fresh_suppliers_through_a_composite_residual(self):
        cofactors = [6237785599, 8498982881, 12015893599, 16371655031]
        path = [160*u for u in cofactors]
        self.assertEqual(path, [998045695840, 1359837260960,
                                1922542975840, 2619464804960])
        verify_path(path)
        expected = [[(6237785599, 1)], [(47, 1), (2399, 1), (75377, 1)],
                    [(12015893599, 1)], [(37, 1), (73, 1), (6061331, 1)]]
        for u, factors in zip(cofactors, expected):
            self.assertEqual(factorize(u), factors)
            self.assertTrue(all(checked_prime(p) for p, _ in factors))
        sigmas = [checked_sigma(u) for u in cofactors]
        self.assertEqual(sigmas, [6237785600, 8683545600, 12015893600, 17044465584])
        self.assertEqual([s % 800 for s in sigmas], [0, 0, 0, 784])
        for index, supplier in ((0, 2399), (1, 12015893599)):
            self.assertNotEqual(path[index] % supplier, 0)
            self.assertEqual(valuation(path[index+1], supplier), 1)
            self.assertEqual((supplier+1) % 800, 0)
        for source, target in zip(path, path[1:]):
            self.assertGreaterEqual(80*target, 109*source)
        for value in path:
            self.assertEqual((valuation(value, 2), valuation(value, 5)), (5, 1))
        self.assertEqual(cofactors[0], 385599+1919200*3250)
        residual = 47*75377
        self.assertEqual(residual, 3542719)
        self.assertEqual(checked_sigma(residual)-residual, 75425)
        self.assertEqual(cofactors[2]-(3271*residual+5670), 427654080)
        # The fourth term's guard loss is not an eventual-orbit classification.

    def test_modular_sigma_helper_against_small_expanded_sources(self):
        for base in range(1, 17):
            for exponent in range(1, 4):
                sigma = checked_sigma(base**exponent)
                for modulus in (9, 25, 49):
                    self.assertEqual(symbolic_sigma_mod(base, exponent, modulus),
                                     sigma % modulus)

    def test_neutral_power_lemma_for_small_bases_and_prime_moduli(self):
        for R in (3, 5, 7, 11, 13):
            self.assertTrue(checked_prime(R))
            exponent = R*R*(R-1)
            for base in range(1, BASE_CAP+1):
                if gcd(base, R) != 1:
                    continue
                self.assertEqual(pow(base, exponent, R*R), 1)
                self.assertEqual(symbolic_sigma_mod(base, exponent, R*R), 1)

    def test_euler_value_neutrality_does_not_imply_sigma_neutrality(self):
        self.assertEqual(pow(7, 6, 9), 1)
        self.assertEqual(symbolic_sigma_mod(7, 6, 9), 7)
        self.assertEqual(checked_sigma(7**6) % 9, 7)

    def test_reduced_progression_and_actual_prime_parameters(self):
        R, r = 2399, 58933259999
        self.assertTrue(checked_prime(R))
        self.assertTrue(checked_prime(r))
        local = (80*R-189)*pow(109, -1, R*R) % (R*R)
        modulus = 800*R*R
        residue = (799+800*((local-799)*pow(800, -1, R*R) % (R*R))) % modulus
        self.assertEqual((residue, modulus), (3683330399, 4604160800))
        self.assertEqual(gcd(residue, modulus), 1)
        self.assertEqual(r, residue+12*modulus)
        self.assertEqual(r % 800, 799)
        self.assertEqual((109*r+189) % (R*R), 80*R % (R*R))
        A = 189*(r+1) // 80
        B = A-r
        self.assertEqual((A, B), (139229826750, 80296566751))
        self.assertEqual(B % (R*R), R)
        self.assertEqual(B, R*33470849)
        self.assertTrue(checked_prime(33470849))
        verify_path([160*r, 160*B])  # Base w=1 is an ordinary, expanded fixture.

    def test_symbolic_powered_composite_handoff_without_expanding_the_source(self):
        R, r, w = 2399, 58933259999, 13
        exponent = R*R*(R-1)
        self.assertEqual(exponent, 13_800_971_998)
        self.assertEqual(gcd(w, 10*r*R), 1)
        self.assertEqual(pow(w, exponent, R*R), 1)
        self.assertEqual(symbolic_sigma_mod(w, exponent, R*R), 1)
        A = 189*(r+1) // 80
        output = (A*symbolic_sigma_mod(w, exponent, R*R)
                  - r*pow(w, exponent, R*R)) % (R*R)
        self.assertEqual(output, R)
        # Independently use the complete certified factorization of the symbolic
        # source. The still-unknown output residual is never treated as prime.
        factors = [(2, 5), (5, 1), (13, exponent), (r, 1)]
        self.assertTrue(all(checked_prime(p) for p, _ in factors))
        self.assertEqual(aliquot_mod(factors, 160*R*R), 160*R)
        core_residue = aliquot_mod(factors, 1600)
        self.assertEqual(core_residue % 160, 0)
        self.assertEqual(gcd(core_residue // 160, 10), 1)
        self.assertEqual((R+1) % 800, 0)

    def test_powered_input_shape_need_not_renew_even_as_prime_times_square(self):
        R, r, w = 2399, 58933259999, 13
        exponent = R*R*(R-1)
        A = 189*(r+1) // 80
        self.assertEqual((r % 3, R % 3, A % 3, exponent % 2), (2, 2, 0, 0))
        modulus = 3*R
        output = (A*symbolic_sigma_mod(w, exponent, modulus)
                  - r*pow(w, exponent, modulus)) % modulus
        self.assertEqual(output % R, 0)
        self.assertEqual(output // R, 2)
        self.assertNotIn(output // R, {a*a % 3 for a in range(3)})
        # R is unitary by the R^2 certificate; its complementary factor is not
        # a square. This forbids one-prime-times-square shape, not further growth.
        self.assertEqual((A*symbolic_sigma_mod(w, exponent, R*R)
                          - r*pow(w, exponent, R*R)) % (R*R), R)

    def test_actual_prime_bridge_and_its_finite_denominator_budget(self):
        r, q, v, end = 2399, 57580223999, 32702399, 106969552799
        for p in (r, q, v, end):
            self.assertTrue(checked_prime(p))
            self.assertEqual(p % 800, 799)
        self.assertNotEqual(r, v)
        cofactors = [q, r*v, end]
        self.assertEqual(cofactors, [57580223999, 78453055201, 106969552799])
        verify_path([160*u for u in cofactors])
        a, b, c = affine_coefficients(r)
        self.assertEqual((a, b, c), (356539, 1088804619, 191920))
        self.assertEqual(a*q+b, c*end)
        start_W, end_W = (a-c)*q+b, (a-c)*end+b
        self.assertEqual(c*end_W, a*start_W)
        self.assertEqual((valuation(start_W, 2), valuation(end_W, 2)), (9, 5))
        self.assertEqual(valuation(start_W, 2) // 4, 2)
        next_cofactor = (109*end+189) // 80
        self.assertEqual(checked_sigma(160*end)-160*end, 160*next_cofactor)
        self.assertEqual(next_cofactor % r, 511)

    def test_composed_affine_period_has_four_binary_denominator_bits_per_block(self):
        for suppliers in ((2399,), (2399, 4799), (4799, 2399, 4799)):
            a, b, c = 1, 0, 1
            expected_slope = Fraction(1)
            for r in suppliers:
                self.assertTrue(checked_prime(r))
                x, y, z = affine_coefficients(r)
                a, b, c = x*a, x*b+y*c, z*c
                expected_slope *= Fraction(x, z)
            self.assertEqual((a % 2, b % 2), (1, 1))
            self.assertGreater(a, c)
            self.assertEqual(valuation(c, 2), 4*len(suppliers))
            self.assertEqual(Fraction(a, c), expected_slope)
            for q in (1, 7, 31):
                image = Fraction(a*q+b, c)
                self.assertEqual((a-c)*image+b, Fraction(a, c)*((a-c)*q+b))
            # These compositions are algebraic checks, NOT claimed orbit blocks.

    def test_neutral_supplier_budget_and_nonneutral_exception(self):
        R = 2399
        for r in (6237785599, 58933259999):
            self.assertTrue(checked_prime(r))
            self.assertEqual(r % 800, 799)
            B = (109*r+189) // 80
            self.assertEqual(B % R, 0)
            quotient = B // R
            self.assertEqual(quotient % 10, 9)
            self.assertGreaterEqual(quotient, 9)
            self.assertLessEqual(720*R, 109*r+189)
            self.assertLess(6*R, r)
        # The observed composite bridge escapes the hypothesis, not the bound.
        r, v, R = 2399, 3542719, 12015893599
        self.assertGreater(R, r)
        self.assertEqual(checked_sigma(v)-v, 75425)
        self.assertNotEqual((checked_sigma(v)-v) % R, 0)
        self.assertEqual(5670*checked_sigma(v)-r*v, R)

    def test_prime_tag_progression_and_expanded_upward_handoff(self):
        r, R, d, c = 2399, 4799, 2711, 1849
        A, B = 5670, 3271
        for p in (r, R, d, 43, 13, 968713):
            self.assertTrue(checked_prime(p))
        self.assertEqual(gcd(R, r*A*B), 1)
        self.assertGreater(R, max(r, d))
        self.assertTrue(1 <= c < R)
        residue = (c*R-A)*pow(B, -1, R*R) % (R*R)
        self.assertEqual(residue, d)
        self.assertEqual(gcd(residue, R*R), 1)
        self.assertEqual(B*d+A, R*43**2)
        cofactors = [r*d, R*43**2, 13*968713]
        self.assertEqual(cofactors, [6503689, 8873351, 12593269])
        verify_path([160*u for u in cofactors])
        self.assertEqual([checked_sigma(u) % 800 for u in cofactors], [0, 0, 396])
        self.assertNotEqual(cofactors[0] % R, 0)
        self.assertEqual(valuation(cofactors[1], R), 1)
        # No eventual fate follows from this third term's guard loss.

    def test_tagged_symbolic_composite_residual_is_nonneutral(self):
        r, R, d, w = 2399, 4799, 2711, 13
        exponent = R*R*(R-1)
        self.assertEqual(exponent, EXPONENT_CAP)
        self.assertEqual(gcd(w, 10*r*R*d), 1)
        self.assertEqual(pow(w, exponent, R*R), 1)
        self.assertEqual(symbolic_sigma_mod(w, exponent, R*R), 1)
        v_mod = d*pow(w, exponent, R*R) % (R*R)
        sigma_mod = (d+1)*symbolic_sigma_mod(w, exponent, R*R) % (R*R)
        self.assertEqual((sigma_mod-v_mod) % (R*R), 1)
        output_mod = (5670*sigma_mod-r*v_mod) % (R*R)
        self.assertEqual(output_mod, R*43**2)
        self.assertEqual(valuation(output_mod, R), 1)
        factors = [(2, 5), (5, 1), (13, exponent), (r, 1), (d, 1)]
        self.assertTrue(all(checked_prime(p) for p, _ in factors))
        self.assertEqual(aliquot_mod(factors, 160*R*R), 160*R*43**2)
        self.assertEqual((R+1) % 800, 0)
        # The symbolic source and its unknown full successor are not expanded.

    def test_tagged_output_has_a_forbidden_three_exponent(self):
        r, R, d = 2399, 4799, 2711
        exponent = R*R*(R-1)
        A = 5670
        x_coefficient = A*(d+1)*3 // 2-r*d
        constant = A*(d+1) // 2
        self.assertEqual((x_coefficient, constant), (16561871, 7688520))
        self.assertEqual(valuation(x_coefficient, 3), 0)
        self.assertEqual(valuation(constant, 3), 5)
        self.assertGreater(exponent, 5)
        self.assertEqual(exponent % 2, 0)
        modulus = 3**6
        output = (A*(d+1)*symbolic_sigma_mod(3, exponent, modulus)
                  - r*d*pow(3, exponent, modulus)) % modulus
        self.assertEqual(output, 3**5)
        self.assertEqual((x_coefficient*pow(3, exponent, modulus)-constant) % modulus,
                         output)
        # With coprime r',d',w' and r' !=3, a universal tagged-power input has
        # 3-exponent 0, 1, or a positive multiple of E_R'>5, not 5.
        # This 3-divisible family is a different phase from the prime-q cohort.
        cofactors = [6237785599, 8498982881, 12015893599, 16371655031]
        for source, target in zip(cofactors, cofactors[1:]):
            self.assertNotEqual(source % 3, 0)
            self.assertEqual((source+target) % 3, 0)

    def test_finite_menu_modular_certificate_does_not_assume_a_prime_residue(self):
        r, R, q0 = 2399, 4799, 13753372799
        P, Q = 34552799, 356822461
        for p in (r, R, q0, P, Q):
            self.assertTrue(checked_prime(p))
        self.assertEqual((P+1) % (800*R), 0)
        self.assertEqual((Q+1) % (r*r), 0)
        # Two unitary auxiliary primes split the divisibility requirements
        # imposed on the single auxiliary prime in the written proof.
        modulus = 800*r*r
        residue = q0 % modulus
        self.assertEqual(residue, 4545051199)
        conditions = [(q0 % R, R)] + [
            ((80*r*p-189)*pow(109, -1, p*p) % (p*p), p*p) for p in (P, Q)
        ]
        for local, local_modulus in conditions:
            self.assertEqual(gcd(modulus, local_modulus), 1)
            residue = (residue+modulus*((local-residue)*pow(modulus, -1, local_modulus)
                                       % local_modulus)) % (modulus*local_modulus)
            modulus *= local_modulus
        self.assertEqual(gcd(residue, modulus), 1)
        self.assertEqual((109*residue+189) % (80*r), 0)
        v = (109*residue+189) // (80*r)
        self.assertEqual((v % r, v % R), (15, 3186))
        for p in (P, Q):
            self.assertEqual(v % (p*p), p)
            self.assertNotEqual(residue % p, 0)
        # The certified factors force sigma(v)=0 mod R and mod r^2, independent
        # of the unfactored residual. Thus R stays absent and old r stays unitary.
        self.assertNotEqual((-r*v) % R, 0)
        self.assertEqual(valuation((-r*v) % (r*r), r), 1)
        # This CRT representative is NOT called prime or used as a prime-input
        # orbit. Existence of prime parameters in the progression is Dirichlet.
        self.assertGreater(residue, SOURCE_CAP)
        with self.assertRaises(ComputationLimit):
            checked_sigma(v)

    def test_domains_and_caps_keep_unresolved_arithmetic_separate(self):
        for invalid in (0, -1, 1.5, True):
            with self.assertRaises(ValueError):
                checked_sigma(invalid)
        with self.assertRaises(ComputationLimit):
            checked_sigma(SOURCE_CAP+1)
        with self.assertRaises(ComputationLimit):
            checked_prime(PRIME_CAP+1)
        with self.assertRaises(ComputationLimit):
            verify_path([6]*(STEP_CAP+2))
        with self.assertRaises(ValueError):
            verify_path([0, 0])
        for args in ((BASE_CAP+1, 1, 3), (1, EXPONENT_CAP+1, 3),
                     (1, 1, MODULUS_CAP+1)):
            with self.assertRaises(ComputationLimit):
                symbolic_sigma_mod(*args)
        with self.assertRaises(ValueError):
            symbolic_sigma_mod(1, 0, 3)
        with self.assertRaises(ValueError):
            affine_coefficients(800)
        verify_path([1, 0])


if __name__ == "__main__":
    unittest.main()
