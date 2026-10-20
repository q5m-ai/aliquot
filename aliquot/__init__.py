"""Exact aliquot arithmetic. No probable-prime assumptions or s(0) extension."""

DEFAULT_MAX_WORK = 2_000_000


class ComputationLimit(RuntimeError):
    """Factorization is unresolved within the requested work budget."""


def positive_integer(value, name="n"):
    if type(value) is not int or value < 1:
        raise ValueError(f"{name} must be a positive integer")


def factorize(n: int, *, max_work: int = DEFAULT_MAX_WORK) -> list[tuple[int, int]]:
    """Proven prime factors via trial division, for arbitrary-size Python ints.

    Each candidate divisibility test and each successful division costs one unit.
    On exhaustion raise ComputationLimit; never treat a residual as probable prime.
    The bound is a work count, not a wall-clock or memory guarantee.
    """
    positive_integer(n)
    positive_integer(max_work, "max_work")
    work = 0

    def tick():
        nonlocal work
        if work >= max_work:
            raise ComputationLimit("Factorization work limit reached; next term unresolved.")
        work += 1

    remaining, p = n, 2
    factors = []
    while p * p <= remaining:
        tick()
        exponent = 0
        while remaining % p == 0:
            tick()
            remaining //= p
            exponent += 1
        if exponent:
            factors.append((p, exponent))
        p = 3 if p == 2 else p + 2
    if remaining > 1:
        factors.append((remaining, 1))
    return factors


def aliquot_sum(n: int, *, max_work: int = DEFAULT_MAX_WORK) -> int:
    """s(n) for n >= 1; exact result or explicit computation-limit exception."""
    factors = factorize(n, max_work=max_work)
    sigma = 1
    for prime, exponent in factors:
        sigma *= (prime ** (exponent + 1) - 1) // (prime - 1)
    return sigma - n
