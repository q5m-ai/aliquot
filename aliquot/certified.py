"""Bounded factorization with independently replayable Lucas primality certificates.

Miller--Rabin is ONLY a compositeness filter. A surviving candidate is never
accepted without a complete n-1 Lucas certificate (or small trial proof).
Pollard--Brent supplies divisors, not primality evidence. No dependencies.
"""

from math import gcd, isqrt, prod

from . import ComputationLimit, positive_integer

SMALL_LIMIT = 1000
SMALL_PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43,
                47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97)
MAX_BITS = 512
MAX_CERTIFICATES = 20_000
DEFAULT_WORK = 200_000


class Budget:
    """One unit per trial division, modular multiplication, or gcd.

    These deterministic operation counts are not CPU timings or bit complexity.
    Modular powers are expanded into counted square-and-multiply operations.
    """

    def __init__(self, limit):
        positive_integer(limit, "max_work")
        self.limit = limit
        self.used = 0

    def tick(self):
        if self.used >= self.limit:
            raise ComputationLimit("Certified factorization work budget exhausted")
        self.used += 1

    def power(self, a, e, n):
        result = 1
        a %= n
        while e:
            if e & 1:
                self.tick()
                result = result * a % n
            e >>= 1
            if e:
                self.tick()
                a = a * a % n
        return result


def _screen(n, budget):
    """False proves compositeness; True means only 'not eliminated'."""
    d, r = n - 1, 0
    while d % 2 == 0:
        d //= 2
        r += 1
    for a in (2, 3, 5, 7, 11, 13, 17):
        if a >= n:
            continue
        x = budget.power(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            budget.tick()
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def _rho(n, budget):
    """Deterministic restarts of bounded Pollard--Brent; returns a proper divisor."""
    for c in range(1, 33):
        y, r, g = c + 1, 1, 1

        def advance(value):
            budget.tick()
            return (value * value + c) % n

        while g == 1:
            x = y
            for _ in range(r):
                y = advance(y)
            k = 0
            while k < r and g == 1:
                saved, q = y, 1
                for _ in range(min(64, r - k)):
                    y = advance(y)
                    budget.tick()
                    q = q * abs(x - y) % n
                budget.tick()
                g = gcd(q, n)
                k += 64
            r *= 2
        if g == n:
            while True:
                saved = advance(saved)
                budget.tick()
                g = gcd(abs(x - saved), n)
                if g > 1:
                    break
        if 1 < g < n:
            return g
    raise ComputationLimit("Pollard--Brent restart budget exhausted")


class CertifiedFactorizer:
    """Reusable prime-proof cache. Every factor() call gets a fresh work budget."""

    def __init__(self, *, max_work=DEFAULT_WORK, max_bits=256):
        positive_integer(max_work, "max_work")
        positive_integer(max_bits, "max_bits")
        if max_bits > MAX_BITS:
            raise ValueError(f"max_bits must be at most {MAX_BITS}")
        self.max_work = max_work
        self.max_bits = max_bits
        self.certificates = {}
        self.last_work = 0

    def fork(self):
        other = CertifiedFactorizer(max_work=self.max_work, max_bits=self.max_bits)
        # Certificates are only inserted, never mutated.
        other.certificates = self.certificates.copy()
        return other

    def factor(self, n):
        positive_integer(n)
        self.last_work = 0
        if n.bit_length() > self.max_bits:
            raise ComputationLimit("Certified factorization source-bit limit exceeded")
        budget = Budget(self.max_work)
        try:
            factors = self._factor(n, budget)
            if prod(p ** e for p, e in factors) != n:
                raise ArithmeticError("Factorization product mismatch")
            return factors
        except RecursionError as error:
            raise ComputationLimit("Prime-proof recursion budget exhausted") from error
        finally:
            self.last_work = budget.used

    def _factor(self, n, budget):
        counts = {}

        def collect(value):
            if value == 1:
                return
            if value in self.certificates:
                counts[value] = counts.get(value, 0) + 1
                return
            for p in SMALL_PRIMES:
                while True:
                    budget.tick()
                    if value % p:
                        break
                    self.certificates.setdefault(p, {"kind": "trial"})
                    counts[p] = counts.get(p, 0) + 1
                    value //= p
                if value == 1:
                    return
            if value <= SMALL_LIMIT:
                for d in range(2, isqrt(value) + 1):
                    budget.tick()
                    if value % d == 0:
                        raise ArithmeticError("Small-prime stripping failed")
                self.certificates[value] = {"kind": "trial"}
                counts[value] = counts.get(value, 0) + 1
                return
            if _screen(value, budget):
                self._certify(value, budget)
                counts[value] = counts.get(value, 0) + 1
                return
            divisor = _rho(value, budget)
            if not (1 < divisor < value and value % divisor == 0):
                raise ArithmeticError("Invalid Pollard divisor")
            collect(divisor)
            collect(value // divisor)

        collect(n)
        return tuple(sorted(counts.items()))

    def _certify(self, n, budget):
        if n in self.certificates:
            return
        factors = self._factor(n - 1, budget)
        witnesses = []
        for q, _ in factors:
            for a in range(2, 66):
                if budget.power(a, n - 1, n) != 1:
                    continue
                residue = budget.power(a, (n - 1) // q, n)
                budget.tick()
                if gcd(residue - 1, n) == 1:
                    witnesses.append((q, a))
                    break
            else:
                # Even a strong pseudoprime must stop here, never be accepted.
                raise ComputationLimit("Lucas witness search unresolved")
        self.certificates[n] = {"kind": "lucas", "factors": factors,
                                "witnesses": tuple(witnesses)}

    def export_certificates(self):
        result = []
        for p, certificate in sorted(self.certificates.items()):
            row = {"prime": str(p), "kind": certificate["kind"]}
            if certificate["kind"] == "lucas":
                row["factors"] = [[str(q), e] for q, e in certificate["factors"]]
                row["witnesses"] = [[str(q), str(a)] for q, a in certificate["witnesses"]]
            result.append(row)
        return result


def verify_certificates(rows):
    """Independent verifier: built-in pow, ascending proof DAG, no factoring/screen.

    Complete factorization of p-1 plus the Lucas congruences proves p prime.
    Certificates are deliberately restricted to this experiment's 512-bit cap.
    Malformed or missing evidence is an error, never 'probably prime'.
    """
    if not isinstance(rows, list) or len(rows) > MAX_CERTIFICATES:
        raise ValueError("Prime certificate count exceeds the replay budget")
    known = set()
    previous = 1
    for row in rows:
        p = _decimal(row["prime"])
        if p <= previous or p.bit_length() > MAX_BITS:
            raise ValueError("Prime certificates must be ascending and within the bit cap")
        previous = p
        if row["kind"] == "trial":
            if p > SMALL_LIMIT or any(p % d == 0 for d in range(2, isqrt(p) + 1)):
                raise ArithmeticError("Invalid small-prime certificate")
        elif row["kind"] == "lucas":
            factors = decode_factors(row["factors"])
            if not factors or any(q not in known for q, _ in factors):
                raise ArithmeticError("Missing predecessor-prime certificate")
            verify_factor_product(factors, p - 1)
            if not isinstance(row["witnesses"], list) or len(row["witnesses"]) != len(factors):
                raise ValueError("Witness count differs from predecessor prime support")
            witnesses = [(_decimal(q), _decimal(a)) for q, a in row["witnesses"]]
            if [q for q, _ in witnesses] != [q for q, _ in factors]:
                raise ArithmeticError("Incorrect witness support")
            for q, a in witnesses:
                if not 1 < a < p or pow(a, p - 1, p) != 1 or gcd(pow(a, (p - 1) // q, p) - 1, p) != 1:
                    raise ArithmeticError("Invalid Lucas witness")
        else:
            raise ValueError("Unknown primality-certificate kind")
        known.add(p)
    return known


def _decimal(raw):
    if not isinstance(raw, str) or not raw.isascii() or not raw.isdigit() or raw.startswith("0"):
        raise ValueError("Expected a positive canonical decimal string")
    if len(raw) > 160:
        raise ValueError("Decimal field exceeds the certificate bit budget")
    return int(raw)


def verify_factor_product(factors, target):
    """Reject oversized products by bounded exact division, never by expansion."""
    positive_integer(target, "factorization target")
    if target.bit_length() > MAX_BITS:
        raise ValueError("Factorization target exceeds the verifier bit budget")
    remaining = target
    for p, e in factors:
        positive_integer(p, "prime")
        positive_integer(e, "exponent")
        if p < 2:
            raise ValueError("Factor bases must be at least two")
        if e > target.bit_length():
            raise ArithmeticError("Exponent exceeds factorization target size")
        for _ in range(e):
            if remaining % p:
                raise ArithmeticError("Factorization product does not match target")
            remaining //= p
    if remaining != 1:
        raise ArithmeticError("Incomplete factorization product")


def decode_factors(rows):
    if not isinstance(rows, (list, tuple)) or len(rows) > MAX_BITS:
        raise ValueError("Factor list exceeds the verifier length budget")
    factors = []
    previous = 1
    for raw_p, e in rows:
        p = _decimal(raw_p)
        positive_integer(e, "exponent")
        if p <= previous or p.bit_length() > MAX_BITS:
            raise ValueError("Factors must have ascending distinct prime bases within the bit cap")
        factors.append((p, e))
        previous = p
    return tuple(factors)
