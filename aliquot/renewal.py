"""Exact supplier diagnostics and falsification of explicitly bounded return rules.

No continuation beyond the supplied certified edge sets is computed. The small
census uses trial factorization and independent additive sieves, not a fit to
Lehmer outcomes. Unknown membership/continuation is retained as censored.
"""

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
import json
from math import gcd, isqrt, prod
from pathlib import Path

from . import ComputationLimit, factorize, positive_integer
from .certified import decode_factors
from .exponent_vectors import MAX_REPORT_BYTES, sigma, value, verify_report
from .research import divisor_sieve

TARGETS = (2, 3, 5, 7)
PHASES = ("clean6", "clean28", "A7", "surplus6", "surplus28")
WINDOWS = (8, 32, 64)
DEFAULT_BOUND = 100_000
MAX_BOUND = 100_000
DEFAULT_SOURCE = Path(__file__).resolve().parents[1] / "research/results/exponent-vectors-extended.json"


def valuation(n, p):
    positive_integer(n)
    if type(p) is not int or p not in TARGETS:
        raise ValueError("Only target primes 2,3,5,7 are supported")
    return _prime_order(n, p)


def _prime_order(n, p):
    # Internal callers supply a positive integer and an already certified prime.
    e = 0
    while n % p == 0:
        n //= p
        e += 1
    return e


def phases(n, total_sigma=None):
    """Decide clean cores and A7 without factoring the unknown large cofactor.

    A7 excludes perfect d7 itself. Its abundance is automatic when d7 is
    nondeficient and the coprime remaining cofactor is >1. Strict-surplus
    phases can be unknown (None) when sigma(n) is not certified.
    """
    if type(n) is not int or n < 0:
        raise ValueError("Expected a nonnegative integer")
    if n == 0:
        return (False,) * len(PHASES)
    a = tuple(valuation(n, p) for p in TARGETS)
    d = prod(p**e for p, e in zip(TARGETS, a))
    sd = prod((p**(e+1)-1)//(p-1) for p, e in zip(TARGETS, a))
    c6 = n > 6 and a[:2] == (1, 1)
    c28 = n > 28 and a[0] == 2 and a[3] == 1
    a7 = sd >= 2*d and (n > d or sd > 2*d)
    if total_sigma is None:
        g6, g28 = (None if c6 else False), (None if c28 else False)
    else:
        positive_integer(total_sigma, "sigma")
        b = tuple(valuation(total_sigma, p) for p in TARGETS)
        g6 = c6 and b[0] > a[0] and b[1] > a[1]
        g28 = c28 and b[0] > a[0] and b[3] > a[3]
    return c6, c28, a7, g6, g28


@dataclass(frozen=True)
class State:
    n: int
    factors: tuple
    total_sigma: int
    exponents: tuple
    supplies: tuple
    columns: tuple
    membership: tuple
    tie_residues: tuple

    @property
    def successor(self):
        return self.total_sigma - self.n


def state(factors):
    """Inputs are complete CERTIFIED factors (or small-census trial factors)."""
    factors = tuple(factors)
    if len(factors) > 512 or any(type(e) is not int or not 1 <= e <= 512 or
                               type(p) is not int or p < 2 or p.bit_length() > 512
                               for p, e in factors):
        raise ValueError("Factor vector exceeds diagnostic bounds")
    if sum((p.bit_length()-1)*e for p, e in factors) > 512:
        raise ValueError("Factor vector exceeds diagnostic bit bound")
    n = value(factors)
    if n.bit_length() > 512:
        raise ValueError("Source exceeds diagnostic bit bound")
    a = tuple(dict(factors).get(p, 0) for p in TARGETS)
    columns = tuple(tuple(valuation((p**(e+1)-1)//(p-1), ell) for ell in TARGETS)
                    for p, e in factors)
    b = tuple(sum(column[i] for column in columns) for i in range(len(TARGETS)))
    total = sigma(factors)
    if b != tuple(valuation(total, p) for p in TARGETS):
        raise ArithmeticError("Prime-power supply columns do not sum to total supply")
    ties = tuple(((total//p**e - n//p**e) % (p*p)) if e == supply else None
                 for p, e, supply in zip(TARGETS, a, b))
    return State(n, factors, total, a, b, columns, phases(n, total), ties)


def source_diagnostic(s):
    n, m = s.n, s.successor
    g = gcd(n, s.total_sigma)
    extra = ([valuation(m, p) - min(a, b)
              for p, a, b in zip(TARGETS, s.exponents, s.supplies)] if m else None)
    if extra is not None and any(c < 0 or c*abs(a-b) for c, a, b in zip(extra, s.exponents, s.supplies)):
        raise ArithmeticError("Cancellation-face identity failed")
    return {"n": str(n), "next": str(m),
            "exponents": list(s.exponents), "supply": list(s.supplies),
            "supplyMargins": [b-a for a, b in zip(s.exponents, s.supplies)],
            "suppliers": [{"prime": str(p), "exponent": e, "contribution": list(column)}
                          for (p, e), column in zip(s.factors, s.columns)],
            "tieUnitDifferenceModPrimeSquared": list(s.tie_residues),
            "extraValuations": extra, "phases": list(s.membership),
            "primitiveTriple": {"g": str(g), "u": str(n//g),
                                "v": str(s.total_sigma//g), "r": str(m//g)} if m else None}


def pair_diagnostic(s, following):
    if following.n != s.successor or s.n <= 1:
        raise ValueError("Expected a positive certified aliquot transition")
    old_primes = {p for p, _ in s.factors}
    old = tuple((p, e) for p, e in following.factors if p in old_primes)
    fresh = tuple((p, e) for p, e in following.factors if p not in old_primes)
    old_value, residual = value(old), value(fresh)
    old_sigma, fresh_sigma = sigma(old), sigma(fresh)
    if old_value*residual != following.n or gcd(old_value, residual) != 1 or gcd(residual, s.n*s.total_sigma) != 1:
        raise ArithmeticError("Old/new unitary split failed")
    old_supply = tuple(valuation(old_sigma, p) for p in TARGETS)
    fresh_supply = tuple(valuation(fresh_sigma, p) for p in TARGETS)
    demand = tuple(max(0, a+1-b) for a, b in zip(following.exponents, old_supply))
    renewed = tuple(have >= need for have, need in zip(fresh_supply, demand))
    if renewed != tuple(b > a for a, b in zip(following.exponents, following.supplies)):
        raise ArithmeticError("Residual-demand equivalence failed")
    eligible24 = (following.n > 6 and following.n % 6 == 0 and residual % 24 == 23
                  and demand[0] <= 3 and demand[1] <= 1)
    if eligible24:
        t = following.successor
        if (not renewed[0] or not renewed[1] or t <= following.n or
                tuple(valuation(t, p) for p in TARGETS[:2]) != following.exponents[:2]):
            raise ArithmeticError("Residue-24 local renewal lemma failed")
    previous_blocks = {p: (e, column) for (p, e), column in zip(s.factors, s.columns)}
    next_blocks = {p: (e, column) for (p, e), column in zip(following.factors, following.columns)}
    lost = [{"prime": str(p), "exponent": e, "contribution": list(column)}
            for p, (e, column) in previous_blocks.items() if p not in next_blocks]
    changed = [{"prime": str(p), "oldExponent": previous_blocks[p][0], "newExponent": e,
                "oldContribution": list(previous_blocks[p][1]), "newContribution": list(column)}
               for p, (e, column) in next_blocks.items()
               if p in previous_blocks and e != previous_blocks[p][0]]
    for block in changed:
        p = int(block["prime"])
        supplied = _prime_order(s.total_sigma, p)
        extra = block["newExponent"] - min(block["oldExponent"], supplied)
        if extra < 0 or extra*abs(block["oldExponent"]-supplied):
            raise ArithmeticError("Changed supplier violates the cancellation identity")
        block.update(sourceSigmaExponent=supplied, cancellationExtra=extra)
    new_suppliers = [{"prime": str(p), "exponent": e, "contribution": list(next_blocks[p][1])}
                     for p, e in fresh]
    return {"oldPart": str(old_value), "newPart": str(residual),
            "newFactors": [[str(p), e] for p, e in fresh],
            "lostBlocks": lost, "changedBlocks": changed, "newSuppliers": new_suppliers,
            "oldSupply": list(old_supply), "newSupply": list(fresh_supply),
            "demand": list(demand), "strictSurplusRenewed": list(renewed),
            "residue24Guard": eligible24}


def _ratio(numerator, denominator):
    r = Fraction(numerator, denominator)
    return {"numerator": str(r.numerator), "denominator": str(r.denominator)}


def walk_return(start, phase, edges, states, *, horizon=64, profitable=False):
    """First return, or a separately labelled search for a profitable checkpoint.

    Edges are restricted to this one certified trace. A closed certified cycle
    may be followed without new factorization. Known but unfactored frontiers
    can still be classified in clean6/clean28/A7, never guessed in surplus phases.
    """
    positive_integer(start, "start")
    positive_integer(horizon, "horizon")
    if phase not in PHASES or horizon > 64 or type(profitable) is not bool:
        raise ValueError("Unsupported phase, horizon, or recovery flag")
    index = PHASES.index(phase)
    n, seen = start, {start}
    for step in range(1, horizon+1):
        if n not in edges:
            return {"status": "censored", "steps": step-1, "end": str(n)}
        n = edges[n]
        member = (states[n].membership if n in states else phases(n))[index]
        if member is None:
            return {"status": "censored_membership", "steps": step, "end": str(n)}
        if member and (not profitable or n > start):
            return {"status": "recovered" if profitable else "returned", "steps": step,
                    "end": str(n), "gain": _ratio(n, start)}
        if n == 0:
            return {"status": "terminated_failure", "steps": step, "end": "0"}
        if n in seen:
            return {"status": "cycle_failure", "steps": step, "end": str(n)}
        seen.add(n)
    return {"status": "window_failure", "steps": horizon, "end": str(n)}


def _outcome_key(result):
    if result["status"] != "returned":
        return result["status"]
    r = result["gain"]
    n, d = int(r["numerator"]), int(r["denominator"])
    return "gain" if n > d else "loss" if n < d else "neutral"


def orbit_diagnostics(source):
    verify_report(source)
    states, edges = {}, {}
    for trace in source["traces"]:
        for row in trace["rows"]:
            s = state(decode_factors(row["factors"]))
            if s.n != int(row["n"]) or s.successor != int(row["next"]):
                raise ArithmeticError("Imported source mismatch")
            if s.n in edges and edges[s.n] != s.successor:
                raise ArithmeticError("Inconsistent shared edge")
            states[s.n], edges[s.n] = s, s.successor
    diagnostics = []
    for n, s in sorted(states.items()):
        row = source_diagnostic(s)
        if s.successor == 0:
            row.update(renewal=None, renewalStatus="terminal")
        elif s.successor in states:
            row.update(renewal=pair_diagnostic(s, states[s.successor]), renewalStatus="exact")
        else:
            row.update(renewal=None, renewalStatus="successor_factorization_unavailable")
        diagnostics.append(row)
    summaries = []
    for trace in source["traces"]:
        local_edges = {int(row["n"]): int(row["next"]) for row in trace["rows"]}
        first_returns, recoveries = [], []
        for index, row in enumerate(trace["rows"]):
            n = int(row["n"])
            for phase, member in zip(PHASES, states[n].membership):
                if member:
                    first_returns.append({"index": index, "start": str(n), "phase": phase,
                                          **walk_return(n, phase, local_edges, states)})
            if states[n].membership[2]:
                for horizon in WINDOWS:
                    recoveries.append({"index": index, "start": str(n), "horizon": horizon,
                                       **walk_return(n, "A7", local_edges, states,
                                                     horizon=horizon, profitable=True)})
        counts = {phase: dict(sorted(Counter(_outcome_key(r) for r in first_returns if r["phase"] == phase).items()))
                  for phase in PHASES}
        recovery_counts = {str(h): dict(sorted(Counter(r["status"] for r in recoveries if r["horizon"] == h).items()))
                           for h in WINDOWS}
        summaries.append({"seed": trace["seed"], "inputStatus": trace["status"],
                          "firstReturnCounts": counts, "recoveryCounts": recovery_counts,
                          "firstReturns": first_returns, "recoveries": recoveries})
    return {"uniqueCertifiedSources": len(states),
            "completeVectorPairs": sum(row["renewalStatus"] == "exact" for row in diagnostics),
            "edgeDiagnostics": diagnostics, "traces": summaries}


class _SignatureAudit:
    def __init__(self):
        self.buckets = {}
        self.witnesses = []

    def add(self, signature, target, n, successor):
        if signature not in self.buckets:
            self.buckets[signature] = [1, {target}, n, successor, target]
            return
        bucket = self.buckets[signature]
        bucket[0] += 1
        if target not in bucket[1] and len(self.witnesses) < 3:
            self.witnesses.append({"first": str(bucket[2]), "second": str(n),
                                   "firstNext": str(bucket[3]), "secondNext": str(successor),
                                   "firstTarget": list(bucket[4]), "secondTarget": list(target)})
        bucket[1].add(target)

    def report(self):
        buckets = self.buckets.values()
        return {"sources": sum(b[0] for b in buckets), "distinctStates": len(self.buckets),
                "repeatedStateBuckets": sum(b[0] > 1 for b in buckets),
                "sourcesInRepeatedBuckets": sum(b[0] for b in buckets if b[0] > 1),
                "ambiguousBuckets": sum(len(b[1]) > 1 for b in buckets),
                "witnesses": self.witnesses}


def guard13(u, total_sigma):
    """Present-arithmetic entry guard for a finite two-step 28-core return."""
    positive_integer(u, "cofactor")
    positive_integer(total_sigma, "cofactor sigma")
    if total_sigma < u:
        raise ValueError("Divisor sum cannot be below its source")
    t = 2*total_sigma - u
    return (u > 1 and gcd(u, 28) == 1 and u % 7 == 6 and total_sigma % 7 == 0
            and t % 13 == 0 and t % 169 != 0)


def _pair_sigma(n):
    positive_integer(n)
    if n > 10**8:
        raise ComputationLimit("Symbolic-family independent verification cap exceeded")
    total = 0
    for d in range(1, isqrt(n)+1):
        if n % d == 0:
            total += d
            if d*d != n:
                total += n//d
    return total


def guarded_family_census(bound, sums):
    """All cofactors u<=bound satisfying G13, not merely selected successes."""
    counts = {"eligible": 0, "twoStepLemmaPassed": 0, "guardRenewed": 0,
              "guardLost": 0, "primeProgressionEntries": 0}
    failures, examples = [], []
    reasons = {"returnedSupply7Lost": 0, "nextUnitary13Lost": 0}
    supply_loss_witness = None
    for u in range(13, bound+1, 14):
        total = u+sums[u]
        if not guard13(u, total):
            continue
        v = 2*total-u
        fv = tuple(factorize(v))
        sigma_v = sigma(fv)
        if sigma_v != _pair_sigma(v):
            raise ArithmeticError("Independent cofactor divisor sum failed")
        w = 2*sigma_v-v
        fw = tuple(factorize(w))
        sigma_w = sigma(fw)
        if sigma_w != _pair_sigma(w):
            raise ArithmeticError("Independent returned-cofactor divisor sum failed")
        counts["eligible"] += 1
        if (v % 7 != 1 or w % 7 != 6 or gcd(v*w, 28) != 1 or
                13*w <= 15*u or sigma_v % 7 != 0):
            raise ArithmeticError("Guarded two-step return lemma failed")
        # Independently check the actual scaled edges, not only the cofactor map.
        if _pair_sigma(28*u)-28*u != 28*v or _pair_sigma(28*v)-28*v != 28*w:
            raise ArithmeticError("Actual 28-core edges disagree with the reduced map")
        counts["twoStepLemmaPassed"] += 1
        renewed = guard13(w, sigma_w)
        counts["guardRenewed" if renewed else "guardLost"] += 1
        returned_t = 2*sigma_w-w
        reasons["returnedSupply7Lost"] += sigma_w % 7 != 0
        reasons["nextUnitary13Lost"] += returned_t % 13 != 0 or returned_t % 169 == 0
        fu = tuple(factorize(u))
        progression = fu == ((u, 1),) and u % 1183 == 349
        counts["primeProgressionEntries"] += progression
        witness = {"cofactors": [str(u), str(v), str(w)],
                   "aliquotPath": [str(28*u), str(28*v), str(28*w)],
                   "gain": _ratio(w, u), "guardRenewed": renewed,
                   "returnedSigma": str(sigma_w), "returnedT": str(returned_t),
                   "returnTransition": pair_diagnostic(state(tuple(factorize(28*v))),
                                                        state(tuple(factorize(28*w))))}
        if sigma_w % 7 != 0 and supply_loss_witness is None:
            supply_loss_witness = witness
        if len(examples) < 3:
            examples.append(witness)
        if not renewed and len(failures) < 3:
            failures.append(witness)
    return {"cofactorBound": str(bound), "independentSourceCap": str(10**8),
            "counts": counts, "overlappingFailureReasons": reasons,
            "returnedSupplyLossWitness": supply_loss_witness,
            "examples": examples, "nonclosureWitnesses": failures}


def renewal_census(bound=DEFAULT_BOUND):
    positive_integer(bound, "bound")
    if bound < 2 or bound > MAX_BOUND:
        raise ValueError("Renewal census bound must lie in 2..100000")
    sums = divisor_sieve(bound)
    image_bound = max(bound, max(sums[1:]))
    independent = divisor_sieve(image_bound)

    @lru_cache(maxsize=4096)
    def get(n):
        return state(tuple(factorize(n)))

    guards = {phase: {"eligible": 0, "retained": 0, "lost": 0, "witnesses": []}
              for phase in ("surplus6", "surplus28")}
    residue24 = {"eligible": 0, "localLemmaPassed": 0, "nextGuardRetained": 0,
                 "nextGuardLost": 0, "witnesses": []}
    names = ("exponents", "exponentsAndSupply", "supplyBlocks", "supplyBlocksAndTieResidues")
    audits = {population: {name: _SignatureAudit() for name in names} for population in ("all", "A7")}
    for n in range(2, bound+1):
        s = get(n)
        m = sums[n]
        following = get(m)
        if s.successor != m or following.successor != independent[m]:
            raise ArithmeticError("Supplier census disagrees with independent divisor sieve")
        for phase, result in guards.items():
            index = PHASES.index(phase)
            if s.membership[index]:
                result["eligible"] += 1
                retained = following.membership[index]
                result["retained" if retained else "lost"] += 1
                if not retained and len(result["witnesses"]) < 3:
                    result["witnesses"].append({"n": str(n), "next": str(m),
                                                "source": source_diagnostic(s),
                                                "successor": source_diagnostic(following)})
        pair = pair_diagnostic(s, following)
        if pair["residue24Guard"]:
            residue24["eligible"] += 1
            residue24["localLemmaPassed"] += 1
            second = get(following.successor)
            next_pair = pair_diagnostic(following, second)
            retained = next_pair["residue24Guard"]
            residue24["nextGuardRetained" if retained else "nextGuardLost"] += 1
            if not retained and len(residue24["witnesses"]) < 3:
                residue24["witnesses"].append({"n": str(n), "m": str(m), "t": str(second.n),
                                                "pair": pair, "nextPair": next_pair})
        base = s.exponents, s.supplies
        blocks = tuple(sorted((e, p if p in TARGETS else 0, column)
                              for (p, e), column in zip(s.factors, s.columns)))
        signatures = (s.exponents, base, (base, blocks), (base, blocks, s.tie_residues))
        target = (*tuple(b > a for a, b in zip(following.exponents, following.supplies)), following.membership[2])
        for name, signature in zip(names, signatures):
            audits["all"][name].add(signature, target, n, m)
            if s.membership[2]:
                audits["A7"][name].add(signature, target, n, m)
    modulus_checks = []
    for modulus in range(3, 129):
        tested, first_failure = 0, None
        for r in range(modulus-1, bound+1, modulus):
            tested += 1
            if (r+sums[r]) % modulus and first_failure is None:
                first_failure = {"R": str(r), "sigma": str(r+sums[r])}
        if 24 % modulus == 0 and first_failure is not None:
            raise ArithmeticError("Universal negative-one supplier lemma failed")
        modulus_checks.append({"modulus": modulus, "tested": tested,
                               "theoremGuarantees": 24 % modulus == 0, "counterexample": first_failure})
    return {"bound": str(bound), "independentSieveBound": str(image_bound),
            "sources": bound-1, "guardClosure": guards, "residue24": residue24,
            "stateSufficiency": {population: {name: audit.report() for name, audit in group.items()}
                                 for population, group in audits.items()},
            "modulusTests": modulus_checks,
            "guarded28Family": guarded_family_census(bound, sums)}


def read_source(path):
    with open(path, "rb") as source:
        raw = source.read(MAX_REPORT_BYTES + 1)
    if len(raw) > MAX_REPORT_BYTES:
        raise ValueError("Source artifact exceeds 16 MiB")
    return json.loads(raw), sha256(raw).hexdigest()


def renewal_report(source_path=DEFAULT_SOURCE, *, bound=DEFAULT_BOUND):
    source, digest = read_source(source_path)
    orbits = orbit_diagnostics(source)
    census = renewal_census(bound)
    return {"schema": "aliquot-supplier-renewal-v1",
            "scope": "Exact local identities and bounded falsification; no closed infinite-orbit class or novelty claimed.",
            "sourceArtifact": {"name": Path(source_path).name, "sha256": digest,
                               "schema": source["schema"], "bounds": source["limits"]},
            "plan": {"targets": list(TARGETS), "phases": list(PHASES),
                     "firstReturnHorizon": 64, "recoveryHorizons": list(WINDOWS),
                     "censusBound": str(bound), "moduli": [3, 128],
                     "signatureTarget": "Strict supply-surplus booleans at 2,3,5,7 and A7 membership of the successor.",
                     "scope": "Rules fixed before this diagnostic run; source traces were previously explored, not blind holdout data."},
            "verification": {"input": "Independent Lucas-prime and divisor-enumeration replay before analysis.",
                             "census": "Trial factors and prime-power formulas checked against an independent additive divisor sieve.",
                             "censoring": "Unknown factors, undecidable membership and unobserved continuation are never failures or successes.",
                             "returns": "First returns are not filtered for gains; profitable-checkpoint existence is a separate bounded search.",
                             "sharing": "Unique-source diagnostics are deduplicated; per-seed and overlapping-window counts are not independent trials.",
                             "signatures": "Source-only supply/tie features; actual prime labels outside 2,3,5,7 deliberately omitted in compressed signatures."},
            "census": census, "orbits": orbits}


def verify_renewal_report(report, source_path=DEFAULT_SOURCE):
    """Rebuild and compare ALL derived fields; not a new independent prime proof.

    Primality/edge replay and the independent census arithmetic are performed
    inside renewal_report. Canonical JSON comparison also rejects bool/int and
    float/int substitutions, which ordinary Python equality would overlook.
    """
    if not isinstance(report, dict) or report.get("schema") != "aliquot-supplier-renewal-v1":
        raise ValueError("Unsupported supplier-renewal report")
    plan = report.get("plan")
    if not isinstance(plan, dict):
        raise ValueError("Invalid diagnostic plan")
    bound = plan.get("censusBound")
    if (not isinstance(bound, str) or not 1 <= len(bound) <= 6 or
            not bound.isascii() or not bound.isdigit() or bound.startswith("0")):
        raise ValueError("Invalid census bound")
    expected = renewal_report(source_path, bound=int(bound))
    canonical = lambda obj: json.dumps(obj, sort_keys=True, separators=(",", ":"))
    if canonical(report) != canonical(expected):
        raise ValueError("Supplier-renewal report does not match exact reconstruction")
    return True
