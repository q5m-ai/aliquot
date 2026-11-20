"""Exact, even-padded Hilbert addresses for a bounded aliquot proof diagnostic.

The map labels *values*, not iteration indices. Its geometry alone supplies no
orbit bound. See research/HILBERT.md for the convention and proof obligations.
"""

from dataclasses import dataclass

from . import ComputationLimit, DEFAULT_MAX_WORK, aliquot_sum, positive_integer
from .two_adic import _divisor_pair_sum

# A state optionally swaps the two bits, then optionally complements both.
# Composition is XOR in this four-element subgroup of square symmetries.
STATES = ("I", "S", "C", "T")
REFINEMENT = (1, 0, 0, 3)  # Children 0,1,2,3 apply S,I,I,T respectively.
MAX_SOURCE = 2_000_000
MAX_STEPS = 256


def base_four(n: int) -> str:
    """Even-length base-4 word; adding another pair of leading zeros is inert."""
    if type(n) is not int or n < 0:
        raise ValueError("n must be a nonnegative integer")
    length = max(2, (n.bit_length() + 1) // 2)
    length += length % 2
    return "".join(str((n >> (2 * j)) & 3) for j in range(length - 1, -1, -1))


@dataclass(frozen=True)
class Address:
    x: int
    y: int
    state: str

    @property
    def norm_squared(self) -> int:
        return self.x * self.x + self.y * self.y


def address(n: int) -> Address:
    """Decode H(n) in the nested-even convention; all coordinates are exact."""
    x = y = state = 0
    for digit in base_four(n):
        q = int(digit)
        bx, by = q >> 1, (q >> 1) ^ (q & 1)
        if state & 1:
            bx, by = by, bx
        if state & 2:
            bx, by = bx ^ 1, by ^ 1
        x, y = 2 * x + bx, 2 * y + by
        state ^= REFINEMENT[q]
    return Address(x, y, STATES[state])


def point(n: int) -> dict:
    """JSON-safe exact values; these coordinates are data, not screen pixels."""
    h = address(n)
    return {"n": str(n), "base4": base_four(n), "x": str(h.x), "y": str(h.y),
            "state": h.state, "normSquared": str(h.norm_squared)}


def checked_sum(n: int, *, max_work: int = DEFAULT_MAX_WORK) -> int:
    """Trial-factorization sum, independently checked by divisor pairs.

    The verification cap applies only to sources. A limit is never evidence
    about primality, no-return, or divergence.
    """
    positive_integer(n)
    if n > MAX_SOURCE:
        raise ComputationLimit("Source exceeds the Hilbert diagnostic verification cap.")
    result = aliquot_sum(n, max_work=max_work)
    if result != _divisor_pair_sum(n):
        raise ArithmeticError(f"Independent divisor-sum mismatch at {n}")
    return result


def trace(seed: int, *, max_source: int = 4095, max_steps: int = 32,
          max_work: int = DEFAULT_MAX_WORK) -> dict:
    """Keep the exact known successor even when it exceeds the source cap."""
    positive_integer(seed, "seed")
    positive_integer(max_source, "max_source")
    positive_integer(max_steps, "max_steps")
    positive_integer(max_work, "max_work")
    if max_source > MAX_SOURCE or max_steps > MAX_STEPS:
        raise ValueError(f"Caps: max_source <= {MAX_SOURCE}, max_steps <= {MAX_STEPS}")
    terms, seen = [seed], {seed: 0}
    cycle_start = None
    while True:
        current = terms[-1]
        if current > max_source:
            status = "source_limit"
            break
        if len(terms) - 1 >= max_steps:
            status = "step_limit"
            break
        try:
            following = checked_sum(current, max_work=max_work)
        except ComputationLimit:
            status = "factorization_limit"
            break
        terms.append(following)
        if following == 0:
            status = "terminated"
            break
        if following in seen:
            status, cycle_start = "cycle", seen[following]
            break
        seen[following] = len(terms) - 1
    return {"seed": str(seed), "status": status, "cycleStart": cycle_start,
            "verifiedSteps": len(terms) - 1,
            "limits": {"maxSource": str(max_source), "maxSteps": max_steps,
                       "maxWorkPerStep": max_work},
            "points": [point(n) for n in terms]}


def build_report() -> dict:
    """Named falsification examples, not a census or survival estimate."""
    ambiguity = []
    for j in range(3, 9):
        n = 18 * (1 + 4 ** j)
        following = checked_sum(n)
        ambiguity.append({"j": j, "source": point(n), "successor": point(following),
                          "modulus": str(4 ** j)})
    return {
        "schema": "aliquot-hilbert-diagnostic-v1",
        "convention": "Even-padded base-4, children S/I/I/T, value indices (not orbit time).",
        "verification": {
            "sums": "Exact trial factorization and independent divisor-pair enumeration.",
            "maxWorkPerSum": DEFAULT_MAX_WORK,
            "ambiguityExponents": [3, 8],
            "largestCheckedSource": str(18 * (1 + 4 ** 8)),
        },
        "normExamples": [{"source": point(n), "successor": point(checked_sum(n))}
                         for n in (15, 24, 72)],
        "ambiguityAnchor": {"source": point(18), "successor": point(checked_sum(18))},
        "sameStateSuffixAmbiguity": ambiguity,
        "traces": [trace(n) for n in (12, 28, 220, 276)],
        "conclusion": "No orbit bound, closed escaping class, or conjecture solution. Limits are unresolved.",
    }
