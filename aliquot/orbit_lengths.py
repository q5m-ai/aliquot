"""Exact, bounded resolution times for the public seed-versus-length chart."""

from aliquot import ComputationLimit, DEFAULT_MAX_WORK, factorize, positive_integer


def build_orbit_lengths(*, seed_bound=1000, max_steps=256,
                        max_source=10**30, max_work=DEFAULT_MAX_WORK):
    """Count transitions to 0 or the first repeat; limits give lower bounds only.

    Shared edges and failed factorizations are cached, not inferred. Factored
    edges are included as reproducible certificates; all integer values are
    decimal strings. The display cap (100) is separate from computation bounds.
    """
    for name, value in locals().copy().items():
        positive_integer(value, name)
    if seed_bound > 10_000 or max_steps > 1000 or max_source > 10**100:
        raise ValueError("Chart bounds exceed 10,000 seeds / 1,000 steps / 10^100 source value")
    edges, failures, orbits = {}, set(), []
    for seed in range(1, seed_bound + 1):
        n, steps, peak = seed, 0, seed
        seen, path, cycle = {}, [], []
        while True:
            if n == 0:
                status = "terminated"
                break
            if n in seen:
                status = "cycle"
                cycle = [str(v) for v in path[seen[n]:]]
                break
            # Resolution at exactly the step bound still counts as resolved.
            if steps >= max_steps:
                status = "step_limit"
                break
            if n > max_source:
                status = "source_limit"
                break
            if n in failures:
                status = "factorization_limit"
                break
            if n not in edges:
                try:
                    factors = factorize(n, max_work=max_work)
                except ComputationLimit:
                    failures.add(n)
                    status = "factorization_limit"
                    break
                sigma = 1
                for prime, exponent in factors:
                    sigma *= (prime ** (exponent + 1) - 1) // (prime - 1)
                edges[n] = {"from": str(n), "to": str(sigma - n),
                            "factors": [[str(p), e] for p, e in factors]}
            seen[n] = steps
            path.append(n)
            n = int(edges[n]["to"])
            steps += 1
            peak = max(peak, n)
        resolved = status in ("terminated", "cycle")
        orbits.append({"seed": str(seed), "status": status, "steps": steps,
                       "lower_bound": steps if resolved else steps + 1,
                       "end": str(n), "peak": str(peak), "cycle": cycle})
    return {
        "schema": "aliquot-lengths-v1",
        "definition": "Transitions to 0 or the first repeated value; s(0) is undefined.",
        "limits": {"seed_bound": seed_bound, "max_steps": max_steps,
                   "max_source": str(max_source), "max_work": max_work,
                   "display_cap": 100},
        "orbits": orbits,
        "edges": [edges[n] for n in sorted(edges)],
    }
