# Aliquot

A [q5m research](https://www.q5m.ai) project exploring aliquot sequences and the potential proof or disproof of the aliquot sequence conjecture.

For positive integers, s(n) is the sum of the proper positive divisors of n. The conjecture asks whether every aliquot sequence eventually reaches 1 (then terminates at 0) or enters a cycle. Numerical experiments alone do not establish a proof or a divergent counterexample.

## Milestones

1. **PR #1 — interactive research site:** adapt the supplied Aliquot HTML explorer, add the standard q5m research header/footer, and establish testing/hosting at the requested `aliquot.q5m.ai` hostname. This is a development milestone, not a production release.
2. **Research notebook 01 — growth and driver loss:** [precise statement, elementary proofs, initial literature map, and next proof obligation](research/README.md). An exact one-step census checks the exit criterion for the class n ≡ 6 (mod 12), independently recomputing divisor sums through a second algorithm. This is foundational work, not a proof/disproof or a novelty claim.

Run the bounded experiment with `npm run research:driver-six -- --bound 100000`. Its code and results stay outside the served `site/` directory. Tests reproduce the [committed report](research/results/driver-six-100000.json).

No proof or disproof is claimed. Repository creation and project registration do not establish hosting acceptance.

## Development

Node.js 22+ runs the dependency-free tests: `npm test`.
For a local-only server: `npm run dev -- --bind 127.0.0.1 8000`.
For managed LAN testing, let the platform allocate the port:

```sh
q5m-lab serve --directory ./site --json
```

Only `site/` is served. All sequence computation happens in the browser; no backend, account, external script, or build step is required. The supplied explorer is preserved as `site/explorer.js`, with its presentation in `site/index.html` and `site/site.css`. The header follows Erdős 193's brand/navigation pattern; the footer uses Causal Sets' q5m/GitHub markup. Shared chrome uses a system-font fallback without requiring Google Fonts.

Tests cover exact proper-divisor sums, first-cycle marking, zero/perfect states, invalid inputs, cancellation, step control, a mocked canvas smoke check, and branding/icon consistency. These are not a real-browser visual or phone test.

## Canonical static hosting

Target: [aliquot.q5m.ai](https://aliquot.q5m.ai/). The owner approved the canonical production infrastructure for this **testing/research site**, not an exposed dev/debug server. `q5m.yaml` declares n01 placement and the hostname; the native contract uses the bootstrap-selected origin. The digest-pinned, unprivileged nginx image includes only `site/`, disables directory listings and hidden paths, and reports its exact source revision at `/.q5m-release`. Containers have a read-only root, no Linux capabilities, bounded memory/CPU/PIDs and local logs. No application secrets or mutable data are needed.

First-route creation uses the separately installed `q5m-production-bootstrap` operator workflow. After onboarding, releases use the approved native production lifecycle from a clean exact source commit on n01:

```sh
q5m-lab project production plan --revision FULL_COMMIT --json
q5m-lab project production deploy --revision FULL_COMMIT --json
q5m-lab project production status --service aliquot --json
q5m-lab project production rollback --service aliquot --json
```

Rollback requires a prior successful release and does not remove the public route. Never run raw Docker/DNS/tunnel operations as a fallback. The independent LAN development server can remain running for edits; those edits are not automatically published to the canonical site.

[PR #1](https://github.com/q5m-ai/aliquot/pull/1) tracks initial public-HTTPS acceptance. Fleet placement is tracked separately in [lab PR #694](https://github.com/q5m-ai/lab/pull/694); source declaration alone is not live fleet acceptance. Current operational lifecycle and exact installed state belong in [lab operations](https://github.com/q5m-ai/lab/blob/main/context/homelab-operations.md#aliquot-research-testing-bootstrap), not this README. No proof or disproof is part of the hosting milestone.
