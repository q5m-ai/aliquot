"""Four-track exponent-vector experiments; exact finite evidence, never escape.

Sparse vectors use ordered (prime, positive exponent) pairs. Zero coordinates
are implicit; the empty vector represents 1, not 0. Prime labels are retained.
"""

from collections import Counter
from math import gcd, isqrt, prod
import json

from . import ComputationLimit, DEFAULT_MAX_WORK, factorize, positive_integer
from .certified import (CertifiedFactorizer, DEFAULT_WORK, decode_factors,
                        verify_certificates, verify_factor_product)
from .research import divisor_sieve

LEHMER_FIVE = (276, 552, 564, 660, 966)
CONTROLS = (12, 30, 138, 318, 220, 28)
PROJECTION = (2, 3, 5, 7)
DEFAULT_STEPS = 256
MAX_DIVISORS = 200_000
MAX_REPORT_BYTES = 16 * 1024 * 1024
MAX_TRACES = 32
MAX_REPORT_ROWS = 8192


def _shape(factors):
    """Check sparse-vector syntax. Primality is supplied by the factor/proof layer."""
    previous = 1
    for p, e in factors:
        positive_integer(p, "prime")
        positive_integer(e, "exponent")
        if p <= previous:
            raise ValueError("Prime bases must be distinct and ascending, and at least 2")
        previous = p


def encode(factors):
    return [[str(p), e] for p, e in factors]


def value(factors):
    _shape(factors)
    return prod(p ** e for p, e in factors)


def sigma(factors):
    _shape(factors)
    return prod((p ** (e + 1) - 1) // (p - 1) for p, e in factors)


def geometric_mod(p, length, modulus):
    """Sum p**j, 0<=j<length, in O(log length); no modular division."""
    positive_integer(p, "base")
    positive_integer(length, "length")
    positive_integer(modulus, "modulus")
    result_power, result_sum = 1 % modulus, 0
    power, total = p % modulus, 1 % modulus
    while length:
        if length & 1:
            result_sum = (result_sum + result_power * total) % modulus
            result_power = result_power * power % modulus
        power, total = power * power % modulus, total * (1 + power) % modulus
        length >>= 1
    return result_sum


def aliquot_mod(factors, modulus):
    """Exact s(n) mod m from CERTIFIED factors, without constructing n or s(n)."""
    _shape(factors)
    positive_integer(modulus, "modulus")
    n_mod, sigma_mod = 1 % modulus, 1 % modulus
    for p, e in factors:
        n_mod = n_mod * pow(p, e, modulus) % modulus
        sigma_mod = sigma_mod * geometric_mod(p, e + 1, modulus) % modulus
    return (sigma_mod - n_mod) % modulus


def _power_histogram(p, e, modulus):
    # The powers modulo m enter a cycle even when gcd(p,m)>1.
    seen, path, residue = {}, [], 1 % modulus
    length = e + 1
    while residue not in seen and len(path) < length:
        seen[residue] = len(path)
        path.append(residue)
        residue = residue * p % modulus
    counts = [0] * modulus
    if len(path) == length:
        for r in path:
            counts[r] += 1
        return counts
    start = seen[residue]
    for r in path[:start]:
        counts[r] += 1
    cycles, remainder = divmod(length - start, len(path) - start)
    for i, r in enumerate(path[start:]):
        counts[r] += cycles + (i < remainder)
    return counts


def divisor_residue_counts(factors, modulus, *, proper=True):
    """Combinatorial multiplicative convolution, not enumeration of all divisors.

    O(k*m^2 + k*m) residue operations for k prime coordinates and m<=256;
    big-integer count cost still grows with log(tau(n)). Prime inputs must be
    certified by the caller. This does not predict a successor's factorization.
    """
    _shape(factors)
    positive_integer(modulus, "modulus")
    if modulus > 256 or type(proper) is not bool:
        raise ValueError("Residue histogram requires modulus<=256 and boolean proper")
    counts = [0] * modulus
    counts[1 % modulus] = 1
    n_mod = 1 % modulus
    for p, e in factors:
        powers = _power_histogram(p, e, modulus)
        new = [0] * modulus
        for r, count in enumerate(counts):
            if count:
                for t, multiplicity in enumerate(powers):
                    if multiplicity:
                        new[r*t % modulus] += count * multiplicity
        counts = new
        n_mod = n_mod * pow(p, e, modulus) % modulus
    if proper:
        counts[n_mod] -= 1
    return counts


def independent_sum(factors, *, max_divisors=MAX_DIVISORS):
    """Enumerate divisors from proven prime powers, without a geometric formula."""
    if prod(e + 1 for _, e in factors) > max_divisors:
        raise ComputationLimit("Independent divisor-enumeration budget exhausted")
    divisors = [1]
    for p, e in factors:
        old, power = divisors, 1
        divisors = []
        for _ in range(e + 1):
            divisors.extend(d * power for d in old)
            power *= p
    return sum(divisors) - max(divisors)


class _SparseLimit(ComputationLimit):
    def __init__(self, message, residual, divisions):
        super().__init__(message)
        self.residual = residual
        self.divisions = divisions


def _reuse_factor(n, old, engine):
    """Strip all powers of previously certified primes, then certify the residual."""
    retained, residual, divisions = {}, n, 0
    for p, _ in old:
        e = 0
        while True:
            divisions += 1
            if residual % p:
                break
            residual //= p
            e += 1
        if e:
            retained[p] = e
    try:
        fresh = engine.factor(residual)
    except ComputationLimit as error:
        raise _SparseLimit(str(error), residual, divisions) from error
    if any(p in retained for p, _ in fresh):
        raise ArithmeticError("Residual still contains a stripped prime")
    factors = tuple(sorted((*retained.items(), *fresh)))
    if value(factors) != n:
        raise ArithmeticError("Sparse factor reuse product mismatch")
    return factors, residual, divisions


def _features(n, factors):
    e = dict(factors)
    return {
        "projection": [e.get(p, 0) for p in PROJECTION],
        "l1": sum(e.values()), "l2Squared": sum(a*a for a in e.values()),
        "supportSize": len(e), "largestPrime": str(max(e, default=1)),
        "valueBits": n.bit_length(),
        "sparsePayloadBitsWithoutFraming": sum(p.bit_length() + a.bit_length() for p, a in factors),
        "decimalBytes": len(str(n).encode("ascii")),
        "factorJsonBytes": len(json.dumps(encode(factors), separators=(",", ":")).encode("ascii")),
    }


def trace(seed, engine, *, max_steps=DEFAULT_STEPS, benchmark=True):
    positive_integer(seed, "seed")
    positive_integer(max_steps, "max_steps")
    if max_steps > 1024:
        raise ValueError("At most 1024 transitions per seed")
    n, old = seed, ()
    seen, rows, benchmarks = {}, [], []
    limit_reason = None
    while True:
        if n == 0:
            status = "terminated"
            break
        if n in seen:
            status = "cycle"
            break
        if len(rows) >= max_steps:
            status = "step_limit"
            break
        if n.bit_length() > engine.max_bits:
            status = "source_bit_limit"
            break
        comparison = None
        if rows and benchmark:
            # Identical pre-step prime-certificate caches; no direct-run proofs
            # are leaked into the sparse run. Budgets are per method per source.
            direct = engine.fork()
            try:
                direct_factors = direct.factor(n)
                direct_status = "exact"
            except ComputationLimit:
                direct_factors, direct_status = None, "factorization_limit"
            comparison = {"from": rows[-1]["n"], "n": str(n),
                          "directStatus": direct_status, "directWork": direct.last_work}
        try:
            factors, residual, divisions = _reuse_factor(n, old, engine)
        except _SparseLimit as error:
            if comparison is not None:
                comparison.update(sparseStatus="factorization_limit", sparseWork=engine.last_work,
                                  strippingDivisions=error.divisions, residual=str(error.residual),
                                  residualBits=error.residual.bit_length())
                benchmarks.append(comparison)
            limit_reason = str(error)
            status = "factorization_limit"
            break
        if comparison is not None:
            if direct_factors is not None and direct_factors != factors:
                raise ArithmeticError("Whole-integer and sparse factorizations disagree")
            comparison.update(sparseStatus="exact", sparseWork=engine.last_work,
                              strippingDivisions=divisions, residual=str(residual),
                              residualBits=residual.bit_length())
            benchmarks.append(comparison)
        total = sigma(factors) - n
        try:
            independent = independent_sum(factors)
        except ComputationLimit as error:
            limit_reason = str(error)
            status = "verification_limit"
            break
        if total != independent:
            raise ArithmeticError("Independent orbit divisor sum mismatch")
        seen[n] = len(rows)
        rows.append({"n": str(n), "next": str(total), "factors": encode(factors),
                     **_features(n, factors)})
        n, old = total, factors
    return {"seed": str(seed), "status": status, "steps": len(rows),
            "end": str(n), "cycleStart": seen.get(n) if status == "cycle" else None,
            "limitReason": limit_reason, "rows": rows, "factorBenchmarks": benchmarks}


def trial_prefix(seed, *, max_steps, max_bits, max_work=DEFAULT_MAX_WORK):
    """Existing engine as a baseline; no probable-prime shortcut or proof cache."""
    n, seen = seed, set()
    while True:
        if n == 0:
            status = "terminated"
            break
        if n in seen:
            status = "cycle"
            break
        if len(seen) >= max_steps:
            status = "step_limit"
            break
        if n.bit_length() > max_bits:
            status = "source_bit_limit"
            break
        try:
            factors = factorize(n, max_work=max_work)
        except ComputationLimit:
            status = "factorization_limit"
            break
        seen.add(n)
        n = sigma(factors) - n
    return {"seed": str(seed), "steps": len(seen), "end": str(n), "status": status}


def summarize_trace(result):
    rows = result["rows"]
    by_n = {row["n"]: row for row in rows}
    counts = Counter()
    phase_counts, phase_edges = Counter(), Counter()
    completed_pairs, new_primes, retained_primes = 0, 0, 0
    collisions, first_phase = [], {}
    runs, run = [], 0
    core28_run = core28_longest = growth_run = growth_longest = 0
    core28_exits = []
    for row in rows:
        n, successor = int(row["n"]), int(row["next"])
        counts["growing" if successor > n else "shrinking" if successor < n else "fixed"] += 1
        counts["evenSources"] += n % 2 == 0
        phase = tuple(row["projection"])
        phase_counts[phase] += 1
        driver28 = phase[0] == 2 and phase[3] >= 1
        counts["exact28DriverSources"] += driver28
        counts["clean28Sources"] += phase[0] == 2 and phase[3] == 1
        core28_run = core28_run + 1 if driver28 else 0
        core28_longest = max(core28_longest, core28_run)
        growth_run = growth_run + 1 if successor > n else 0
        growth_longest = max(growth_longest, growth_run)
        if driver28 and not (successor % 8 == 4 and successor % 7 == 0) and len(core28_exits) < 3:
            core28_exits.append({"from": row["n"], "to": row["next"]})
        # Clean 6-core is a source property, not a forward-invariant class.
        if phase[:2] == (1, 1):
            run += 1
        else:
            runs.append(run)
            run = 0
        if row["next"] not in by_n:
            continue
        following = by_n[row["next"]]
        following_phase = tuple(following["projection"])
        phase_edges[phase, following_phase] += 1
        if phase in first_phase and first_phase[phase][0] != following_phase:
            if len(collisions) < 3:
                collisions.append({"phase": list(phase), "first": first_phase[phase][1],
                                   "second": row["n"],
                                   "firstNextPhase": list(first_phase[phase][0]),
                                   "secondNextPhase": list(following_phase)})
        else:
            first_phase.setdefault(phase, (following_phase, row["n"]))
        a = dict(decode_factors(row["factors"]))
        b = dict(decode_factors(following["factors"]))
        completed_pairs += 1
        new_primes += len(b.keys() - a.keys())
        retained_primes += len(b.keys() & a.keys())
    runs.append(run)
    benchmarks = result["factorBenchmarks"]
    paired = [b for b in benchmarks if b["directStatus"] == b["sparseStatus"] == "exact"]
    return {"counts": dict(sorted(counts.items())), "completeVectorPairs": completed_pairs,
            "newPrimeOccurrences": new_primes, "retainedPrimeOccurrences": retained_primes,
            "longestCleanSixSourceRun": max(runs, default=0),
            "longestExact28DriverRun": core28_longest,
            "longestGrowingRun": growth_longest, "first28DriverExits": core28_exits,
            "distinctProjectedPhases": len(phase_counts),
            "topPhases": [{"phase": list(p), "count": c} for p, c in phase_counts.most_common(5)],
            "topPhaseEdges": [{"from": list(p), "to": list(q), "count": c}
                              for (p, q), c in phase_edges.most_common(5)],
            "projectionCollisions": collisions,
            "maxSourceBits": max((r["valueBits"] for r in rows), default=0),
            "peakKnownValue": str(max([int(result["end"]), *(int(r["n"]) for r in rows)])),
            "factorComparison": {
                "pairedExact": len(paired),
                "directWork": sum(b["directWork"] for b in paired),
                "sparseWork": sum(b["sparseWork"] + b["strippingDivisions"] for b in paired),
                "directLimitedSparseExact": sum(b["directStatus"] != "exact" and b["sparseStatus"] == "exact" for b in benchmarks),
                "directExactSparseLimited": sum(b["directStatus"] == "exact" and b["sparseStatus"] != "exact" for b in benchmarks),
                "bothLimited": sum(b["directStatus"] != "exact" and b["sparseStatus"] != "exact" for b in benchmarks)},
            "storageTotals": {
                "decimalBytes": sum(r["decimalBytes"] for r in rows),
                "factorJsonBytes": sum(r["factorJsonBytes"] for r in rows),
                "integerBits": sum(r["valueBits"] for r in rows),
                "sparsePayloadBitsWithoutFraming": sum(r["sparsePayloadBitsWithoutFraming"] for r in rows)}}


def vector_census(bound=10_000):
    positive_integer(bound, "bound")
    if bound > 100_000:
        raise ValueError("Vector census bound must be at most 100000")
    sums = divisor_sieve(bound)
    trends = {name: Counter() for name in ("l1", "l2Squared", "linf")}
    even, odd_successors, perpendicular = 0, 0, 0
    for n in range(2, bound + 1):
        factors = factorize(n)
        if sigma(factors) - n != sums[n]:
            raise ArithmeticError("Census product/sieve disagreement")
        x, y, b = dict(factors), dict(factorize(sums[n])), dict(factorize(n + sums[n]))
        for p in x.keys() | y.keys() | b.keys():
            extra = y.get(p, 0) - min(x.get(p, 0), b.get(p, 0))
            if extra < 0 or extra * abs(x.get(p, 0) - b.get(p, 0)):
                raise ArithmeticError("Cancellation orthogonality failed")
        for name, measure in (("l1", lambda v: sum(v.values())),
                              ("l2Squared", lambda v: sum(e*e for e in v.values())),
                              ("linf", lambda v: max(v.values(), default=0))):
            before, after = measure(x), measure(y)
            trends[name]["up" if after > before else "down" if after < before else "same"] += 1
        perpendicular += not any(p in y for p in x)
        if n % 2 == 0:
            even += 1
            gate = all(e % 2 == 0 for p, e in factors if p != 2)
            if gate != (sums[n] % 2 == 1):
                raise ArithmeticError("Parity sublattice gate failed")
            odd_successors += gate
        # Composite moduli deliberately include noninvertible p-1 cases.
        for modulus in (12, 64, 81):
            if aliquot_mod(factors, modulus) != sums[n] % modulus:
                raise ArithmeticError("Modular tensor-product check failed")
    midpoint_bound = min(bound, 500)
    midpoint_pairs, abundant_pairs = 0, 0
    for n in range(1, midpoint_bound + 1):
        for m in range(n + 1, midpoint_bound + 1):
            k = isqrt(n*m)
            if k*k != n*m:
                continue
            midpoint_pairs += 1
            if (k + sums[k])**2 < (n + sums[n]) * (m + sums[m]):
                raise ArithmeticError("Integer midpoint concavity failed")
            if sums[n] > n and sums[m] > m:
                abundant_pairs += 1
                if sums[k] <= k:
                    raise ArithmeticError("Abundant midpoint failed")
    return {"bound": str(bound), "sources": max(0, bound - 1),
            "normTrends": {k: dict(sorted(v.items())) for k, v in trends.items()},
            "evenSources": even, "evenToOdd": odd_successors,
            "disjointSupportSteps": perpendicular,
            "midpointBound": midpoint_bound, "integerMidpointPairs": midpoint_pairs,
            "abundantEndpointPairs": abundant_pairs,
            "checkedModuli": [12, 64, 81]}


def vector_report(*, bound=10_000, max_steps=DEFAULT_STEPS, max_bits=256,
                  max_work=DEFAULT_WORK, trial_work=DEFAULT_MAX_WORK):
    census = vector_census(bound)
    engine = CertifiedFactorizer(max_work=max_work, max_bits=max_bits)
    traces = []
    for seed in (*LEHMER_FIVE, *CONTROLS):
        result = trace(seed, engine, max_steps=max_steps)
        result["group"] = "Lehmer five" if seed in LEHMER_FIVE else "control"
        result["summary"] = summarize_trace(result)
        result["trialBaseline"] = trial_prefix(seed, max_steps=max_steps,
                                               max_bits=max_bits, max_work=trial_work)
        traces.append(result)
    huge_exponent = 10**12
    huge_factors = ((2, huge_exponent),)
    histogram = divisor_residue_counts(huge_factors, 97)
    residue = aliquot_mod(huge_factors, 97)
    if sum(i*c for i, c in enumerate(histogram)) % 97 != residue or sum(histogram) != huge_exponent:
        raise ArithmeticError("Symbolic huge-exponent check failed")
    result = {
        "schema": "aliquot-exponent-vectors-v1",
        "scope": "Finite exact evidence; no divergent orbit, solution, or novelty established.",
        "limits": {"censusBound": str(bound), "maxSteps": max_steps,
                   "maxSourceBits": max_bits, "certifiedWorkPerFactorization": max_work,
                   "trialWorkPerFactorization": trial_work, "maxDivisors": MAX_DIVISORS,
                   "rhoRestarts": 32, "lucasWitnessCandidatesPerPrime": 64},
        "arithmetic": {
            "primality": "Complete n-1 Lucas certificates or trial proof through 1000; Miller-Rabin only rejects.",
            "factorization": "Bounded deterministic Pollard-Brent plus old-prime stripping; certified prime cache.",
            "work": "Factorization-only budgets; stripping is separate (at most twice the source bit cap). Deterministic arithmetic counts, not timings or bit complexity; trial units differ.",
            "independent": "Additive sieve for census; explicit divisor enumeration and Lucas-proof replay for every orbit edge.",
            "comparison": "Whole/sparse methods begin each paired input with identical prime-proof caches; sparse stripping counted separately.",
            "projection": "Coordinates 2,3,5,7 only; not an autonomous Markov state; shared tails are not independent samples."},
        "census": census, "traces": traces,
        "symbolicExample": {"factors": [["2", str(huge_exponent)]],
                            "expandedIntegerBits": str(huge_exponent + 1),
                            "modulus": 97, "aliquotResidue": residue,
                            "properDivisorCount": str(sum(histogram)),
                            "divisorResidueCounts": list(map(str, histogram)),
                            "scope": "No expanded integer or next factorization constructed; not a continued orbit."},
        "primeCertificates": engine.export_certificates(),
    }
    verify_report(result)
    return result


def _report_integer(raw):
    # Sources have <=512 bits; a computed successor can exceed the source cap.
    # 320 decimal digits also accommodates oversized initial seeds as frontiers.
    if (not isinstance(raw, str) or not raw.isascii() or not raw.isdigit()
            or len(raw) > 320 or (len(raw) > 1 and raw.startswith("0"))):
        raise ValueError("Expected a bounded canonical nonnegative decimal string")
    return int(raw)


def verify_report(report):
    """Replay math certificates, without calling the factorization engine.

    Aggregate proof/trace/row caps bound replay. The CLI additionally caps the
    JSON byte input before parsing; callers passing Python objects own that IO.
    """
    if report["schema"] != "aliquot-exponent-vectors-v1":
        raise ValueError("Unknown exponent-vector report schema")
    known = verify_certificates(report["primeCertificates"])
    limits = report["limits"]
    for key, ceiling in (("maxSteps", 1024), ("maxSourceBits", 512), ("maxDivisors", MAX_DIVISORS)):
        positive_integer(limits[key], key)
        if limits[key] > ceiling:
            raise ValueError("Report exceeds verifier resource limits")
    traces = report["traces"]
    if not isinstance(traces, list) or len(traces) > MAX_TRACES:
        raise ValueError("Trace count exceeds the replay budget")
    row_count = 0
    for result in traces:
        if not isinstance(result["rows"], list) or not isinstance(result["factorBenchmarks"], list):
            raise ValueError("Expected finite row and benchmark lists")
        row_count += len(result["rows"])
        if row_count > MAX_REPORT_ROWS or len(result["factorBenchmarks"]) > limits["maxSteps"]:
            raise ValueError("Aggregate row/benchmark replay budget exceeded")
        n, seen = _report_integer(result["seed"]), {}
        positive_integer(n, "seed")
        if result["steps"] != len(result["rows"]) or len(result["rows"]) > limits["maxSteps"]:
            raise ArithmeticError("Incorrect step count")
        for index, row in enumerate(result["rows"]):
            if n <= 0 or n in seen or n != _report_integer(row["n"]) or n.bit_length() > limits["maxSourceBits"]:
                raise ArithmeticError("Invalid orbit source/path")
            factors = decode_factors(row["factors"])
            if any(p not in known or e > limits["maxSourceBits"] for p, e in factors):
                raise ArithmeticError("Missing factor proof or excessive exponent")
            verify_factor_product(factors, n)
            successor = independent_sum(factors, max_divisors=limits["maxDivisors"])
            if successor != _report_integer(row["next"]):
                raise ArithmeticError("Orbit edge verification failed")
            if any(row[key] != expected for key, expected in _features(n, factors).items()):
                raise ArithmeticError("Vector feature mismatch")
            seen[n] = index
            n = successor
        if n != _report_integer(result["end"]):
            raise ArithmeticError("Incorrect orbit frontier")
        status = result["status"]
        if status == "terminated":
            valid = n == 0 and result["cycleStart"] is None
        elif status == "cycle":
            valid = n in seen and result["cycleStart"] == seen[n]
        elif status == "step_limit":
            valid = len(seen) == limits["maxSteps"] and n > 0 and n not in seen
        elif status == "source_bit_limit":
            valid = n.bit_length() > limits["maxSourceBits"] and n not in seen
        elif status in ("factorization_limit", "verification_limit"):
            # These statuses describe the bounded run, not an intrinsic inability
            # to factor the number. The certificate proves only its known prefix.
            valid = n > 0 and n not in seen
        else:
            valid = False
        if not valid:
            raise ArithmeticError("Invalid terminal/status certificate")
        if summarize_trace(result) != result["summary"]:
            raise ArithmeticError("Trace summary mismatch")
    return True
