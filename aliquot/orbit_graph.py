"""Exact, bounded union of aliquot orbits, with a separate inverse census.

This supplies the small public visualization, not a conjecture or novelty claim.
"""

from math import prod

from . import ComputationLimit, DEFAULT_MAX_WORK, factorize, positive_integer
from .research import divisor_sieve, require_bound


def build_orbit_graph(*, seed_bound=100, max_steps=64, max_source=1_000_000,
                      predecessor_bound=100_000, max_work=DEFAULT_MAX_WORK):
    positive_integer(seed_bound, "seed_bound")
    if seed_bound > 100:
        raise ValueError("This visualization is bounded to starts 1–100.")
    positive_integer(max_steps, "max_steps")
    if max_steps > 256:
        raise ValueError("max_steps must be at most 256")
    require_bound(max_source)
    require_bound(predecessor_bound)
    positive_integer(max_work, "max_work")
    values, edges, factors, issues = set(), {}, {}, {}
    for seed in range(1, seed_bound + 1):
        n, seen = seed, set()
        for step in range(max_steps + 1):
            values.add(n)
            if n == 0 or n in seen:
                break
            seen.add(n)
            if step == max_steps:
                issues.setdefault(n, "step limit")
                break
            if n not in edges:
                if n > max_source:
                    issues[n] = "source limit"
                    break
                try:
                    factors[n] = factorize(n, max_work=max_work)
                except ComputationLimit:
                    issues[n] = "factorization work limit"
                    break
                edges[n] = prod((p ** (e + 1) - 1) // (p - 1)
                                for p, e in factors[n]) - n
            n = edges[n]

    # Follow the merged, already verified edges: another seed may have resolved
    # a frontier left by an earlier trace. This does not compute additional edges.
    orbits = []
    memberships = {n: [] for n in values}
    for seed in range(1, seed_bound + 1):
        n, path, seen, cycle = seed, [], {}, []
        while n not in seen:
            seen[n] = len(path)
            path.append(n)
            memberships[n].append(str(seed))
            if n == 0 or n not in edges:
                break
            n = edges[n]
        else:
            cycle = path[seen[n]:]
            path.append(n)
        status = "cycle" if cycle else "terminated" if n == 0 else "unresolved"
        orbits.append({"seed": str(seed), "path": list(map(str, path)),
                       "status": status, "cycle": list(map(str, cycle))})

    incoming = {n: [] for n in values}
    for n, successor in sorted(edges.items()):
        incoming[successor].append(str(n))
    # Exact integer sieve, independent of the orbit factorization algorithm.
    sums = divisor_sieve(predecessor_bound)
    preimages = {n: [] for n in values if n != 1}
    for source in range(1, predecessor_bound + 1):
        target = sums[source]
        if target in preimages:
            preimages[target].append(str(source))
    nodes = []
    for n in sorted(values):
        ceiling = None if n == 1 else 1 if n == 0 else (n - 1) ** 2
        inverse = {"status": "infinite" if n == 1 else
                   "complete" if ceiling <= predecessor_bound else "partial",
                   "ceiling": None if ceiling is None else str(ceiling),
                   "checked_through": None if ceiling is None else str(min(ceiling, predecessor_bound)),
                   "values": None if n == 1 else preimages[n]}
        nodes.append({
            "id": str(n), "next": str(edges[n]) if n in edges else None,
            "factors": [{"prime": str(p), "exponent": e} for p, e in factors[n]] if n in factors else None,
            "prime": edges[n] == 1 and n > 1 if n in edges else False if n == 0 else None,
            "seed": 1 <= n <= seed_bound, "starts": memberships[n],
            "incoming": incoming[n], "leaf": not incoming[n],
            "untouchable": n > 0 and inverse["status"] == "complete" and not inverse["values"],
            "predecessors": inverse,
            "unresolved": issues.get(n, "step limit") if n > 0 and n not in edges else None,
        })
    return {
        "schema": "aliquot-orbit-graph-v1",
        "limits": {"seed_min": "1", "seed_max": str(seed_bound), "max_steps": max_steps,
                   "max_source": str(max_source), "factorization_work": max_work,
                   "predecessor_source_bound": str(predecessor_bound)},
        "complete_orbits": all(orbit["status"] != "unresolved" for orbit in orbits),
        "nodes": nodes,
        "edges": [{"from": str(n), "to": str(successor)} for n, successor in sorted(edges.items())],
        "orbits": orbits,
    }
