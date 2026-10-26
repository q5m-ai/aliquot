"""One bounded test of distinct-target coverage by smaller aliquot predecessors.

Targets, not sources, set the cutoff. Every smaller predecessor of a target
N <= bound is examined, because its source is < N <= bound. No claim about
larger predecessors, asymptotic density, or individual orbit fate follows.
"""

from collections import Counter, defaultdict
from fractions import Fraction
from math import gcd, isqrt

from .research import divisor_sieve, require_bound

DEFAULT_BOUND = 1_000_000
LEVELS = (1_000, 10_000, 100_000, 1_000_000)
NAMED_TARGETS = (12, 30, 138, 220, 276, 318, 552, 564, 660, 966)
SAMPLE_LIMIT = 32


def _tables(bound):
    """Eratosthenes least factors and multiplicative sigma, independent of s sieve."""
    spf = list(range(bound + 1))
    for p in range(2, isqrt(bound) + 1):
        if spf[p] == p:
            for n in range(p*p, bound + 1, p):
                if spf[n] == n:
                    spf[n] = p
    total = [None] + [1]*bound
    for n in range(2, bound + 1):
        p, rest, power, geometric = spf[n], n, 1, 1
        while rest % p == 0:
            rest //= p
            power *= p
            geometric += power
        total[n] = total[rest]*geometric
    return spf, total


def _factors(n, spf):
    result = []
    while n > 1:
        p, e = spf[n], 0
        while n % p == 0:
            n //= p
            e += 1
        result.append((p, e))
    return result


def _ratio(numerator, denominator):
    if denominator == 0:
        return None
    f = Fraction(numerator, denominator)
    return {"numerator": str(f.numerator), "denominator": str(f.denominator)}


def _summary(rows, abundant_count):
    # Rows are (target, predecessor, core, prime). Even different decompositions
    # of ONE predecessor count separately as representations, not as sources.
    representations, source_pairs = Counter(), Counter()
    for n, m, _, _ in rows:
        representations[n] += 1
        source_pairs[n, m] += 1
    sources = Counter(n for n, _ in source_pairs)
    first = sum(representations.values())
    second = sum(r*r for r in representations.values())
    source_first = len(source_pairs)
    source_second = sum(r*r for r in sources.values())
    same_source = sum(r*(r-1) for r in source_pairs.values())
    covered = len(representations)
    if first*first > covered*second or source_first**2 > covered*source_second:
        raise ArithmeticError("Cauchy accounting failed")
    return {
        "targets": covered, "predecessors": source_first, "representations": first,
        "representationSecondMoment": str(second), "predecessorSecondMoment": str(source_second),
        "samePredecessorOrderedCollisionPairs": str(same_source),
        "distinctPredecessorOrderedRepresentationPairs": str(second-first-same_source),
        "coverageOfAbundantTargets": _ratio(covered, abundant_count),
        "representationCauchyLowerBound": _ratio(first*first, second) if second else _ratio(0, 1),
        "predecessorCauchyLowerBound": _ratio(source_first**2, source_second) if source_second else _ratio(0, 1),
        "representationMultiplicity": [{"multiplicity": r, "targets": c}
                                         for r, c in sorted(Counter(representations.values()).items())],
        "predecessorMultiplicity": [{"multiplicity": r, "targets": c}
                                    for r, c in sorted(Counter(sources.values()).items())],
    }


def backward_report(bound=DEFAULT_BOUND):
    require_bound(bound)
    spf, total = _tables(bound)
    independent = divisor_sieve(bound)
    if any(total[n]-n != independent[n] for n in range(1, bound + 1)):
        raise ArithmeticError("Factor-product sums disagree with the additive sieve")
    abundant = {n for n in range(1, bound + 1) if total[n] > 2*n}
    predecessors = defaultdict(list)
    records = set()
    for m in range(1, bound + 1):
        n = total[m]-m
        if not m < n <= bound or n not in abundant:
            continue
        predecessors[n].append(m)
        for p, e in _factors(m, spf):
            if e == 1:
                c = m//p
                if total[c] > 2*c:
                    records.add((n, m, c, p))

    # A second, differently parameterized enumeration uses only additive sums.
    # For abundant C and p>=2, N=(p+1)s(C)+C>4C. All eligible C are < bound/4.
    primes = [p for p in range(2, bound + 1) if independent[p] == 1]
    rebuilt = set()
    for c in range(1, (bound-1)//4 + 1):
        a = independent[c]
        if a <= c:
            continue
        b = a+c
        for p in primes:
            n = a*p+b
            if n > bound:
                break
            if c % p == 0:
                continue
            m = c*p
            if not m < n or independent[m] != n:
                raise ArithmeticError("Independent inverse-family identity failed")
            if independent[n] > n:
                rebuilt.add((n, m, c, p))
    if records != rebuilt:
        raise ArithmeticError("Source-factor and core-prime enumerations disagree")
    del rebuilt

    root = {row for row in records if row[2]**2 <= row[0]}
    if len({m for _, m, _, _ in root}) != len(root):
        raise ArithmeticError("Square-root core family has duplicate source representations")
    all_rows = [(n, m, 0, 0) for n, sources in predecessors.items() for m in sources]
    root_targets = {n for n, _, _, _ in root}
    prime_targets = {n for n, _, _, _ in records}
    six_root = [row for row in root if row[2] % 6 == 0 and gcd(row[2]//6, 6) == 1]
    levels = []
    for limit in sorted({bound, *(x for x in LEVELS if x <= bound)}):
        count = sum(n <= limit for n in abundant)
        baseline = _summary((r for r in all_rows if r[0] <= limit), count)
        unrestricted = _summary((r for r in records if r[0] <= limit), count)
        restricted = _summary((r for r in root if r[0] <= limit), count)
        gaps = {
            "noSmallerPredecessor": count-baseline["targets"],
            "hasSmallerButNoAbundantPrimeCore": baseline["targets"]-unrestricted["targets"],
            "hasPrimeCoreButNotSquareRootCore": unrestricted["targets"]-restricted["targets"],
        }
        if min(gaps.values()) < 0 or sum(gaps.values()) != count-restricted["targets"]:
            raise ArithmeticError("Nested coverage partition failed")
        levels.append({"targetBound": str(limit), "abundantTargets": count,
                       "allSmaller": baseline, "primeCore": unrestricted,
                       "squareRootCore": restricted, "gaps": gaps})

    def example(n):
        if n not in abundant:
            raise ValueError("Examples must belong to the abundant-target universe")
        sources = predecessors.get(n, [])
        encoded = []
        for m in sources[:SAMPLE_LIMIT]:
            factors = _factors(m, spf)
            pairs = [(m//p, p) for p, e in factors if e == 1 and total[m//p] > 2*(m//p)]
            encoded.append({"source": str(m), "factors": [[str(p), e] for p, e in factors],
                            "representations": [{"core": str(c), "prime": str(p),
                                                 "coreWithinTargetSquareRoot": c*c <= n}
                                                for c, p in sorted(pairs)]})
        return {"target": str(n), "aliquotSum": str(independent[n]), "abundant": n in abundant,
                "hasSmallerPredecessor": bool(sources), "coveredByPrimeCore": n in prime_targets,
                "coveredBySquareRootCore": n in root_targets,
                "predecessorCount": len(sources), "predecessors": encoded,
                "omittedPredecessors": max(0, len(sources)-SAMPLE_LIMIT)}

    gap_examples = {}
    for n in sorted(abundant):
        category = ("noSmallerPredecessor" if n not in predecessors else
                    "hasSmallerButNoAbundantPrimeCore" if n not in prime_targets else
                    "hasPrimeCoreButNotSquareRootCore" if n not in root_targets else None)
        if category and category not in gap_examples:
            gap_examples[category] = example(n)
    collisions = Counter(n for n, _, _, _ in root)
    repeated = [n for n in sorted(collisions) if collisions[n] > 1]
    largest = min(collisions, key=lambda n: (-collisions[n], n)) if collisions else None
    return {
        "schema": "aliquot-backward-coverage-v1", "targetBound": str(bound),
        "scope": "Exact finite coverage of abundant targets by strictly smaller direct predecessors; no density or orbit conclusion.",
        "definition": "N=s(C)p+sigma(C), C abundant, p prime, gcd(C,p)=1; proposed family additionally has C*C<=N, not merely C*C<=bound.",
        "verification": {"divisorSums": "Multiplicative least-factor sieve versus independent additive divisor sieve at every positive integer through the bound.",
                         "families": "Exact equality of source-factor and independent core-prime representation sets.",
                         "baseline": "All smaller predecessors are exhausted; larger predecessors are not classified.",
                         "censoring": "No unresolved samples inside the stated finite universe; invalid bounds abort rather than produce counts.",
                         "independence": "Nested prefixes and overlapping representations are not independent trials or a blind holdout."},
        "levels": levels,
        "cleanSixSquareRootSubset": _summary(six_root, len(abundant)),
        "examples": {"namedTargets": [example(n) for n in NAMED_TARGETS if n <= bound],
                     "firstGaps": gap_examples,
                     "firstSquareRootCollision": example(repeated[0]) if repeated else None,
                     "largestSquareRootMultiplicity": example(largest) if largest is not None else None},
        "sampleLimitPerTarget": SAMPLE_LIMIT,
        "limits": "Target/source bound at most 1000000; exact sieves, no probable-prime acceptance, and no iteration at zero.",
    }
