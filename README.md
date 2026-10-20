# Aliquot

A [q5m research](https://www.q5m.ai) project exploring aliquot sequences and the potential proof or disproof of the aliquot sequence conjecture.

For positive integers, s(n) is the sum of the proper positive divisors of n. The conjecture asks whether every aliquot sequence eventually reaches 1 (then terminates at 0) or enters a cycle. Numerical experiments alone do not establish a proof or a divergent counterexample.

## Milestones

1. **PR #1 — interactive research site:** adapt the supplied Aliquot HTML explorer, add the standard q5m research header/footer, and establish testing/hosting at the requested `aliquot.q5m.ai` hostname. This is a development milestone, not a production release.
2. Subsequent work: precise conjecture statement, literature and known results, reproducible experiments, and independently checked proof/disproof attempts.

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

## Testing milestone status (2026-10-20)

- Public repository, minimal initial `main` commit, root favicon, and n02 Paseo registration: complete.
- Site implementation and automated checks: in PR #1, not merged.
- Managed LAN testing server: running; exact temporary lifecycle is recorded in [lab operations](https://github.com/q5m-ai/lab/blob/main/context/homelab-operations.md#aliquot-research-testing-bootstrap).
- Public testing: **blocked before provisioning**. After the initial static-review policy refusal, the owner explicitly approved n01's canonical stateless production bootstrap for the static testing site. The native declaration is committed for planning only: `auto/tcp` and Compose's port placeholder must be replaced with the bootstrap-selected origin before deployment. N01's installed bootstrap cannot load its pinned `runtime/q5m-production` because the referenced development release is absent. No origin plan succeeded, no `create` ran, and `aliquot.q5m.ai` remains unprovisioned. Protected runtime repair requires separate approval; never repoint its dependency symlink or improvise DNS/tunnel changes.
- Fleet declaration: prepared in the companion lab PR. Reviewed merge, managed manifest rollout, and per-node reconciliation remain pending; only n02's Paseo registration exists so far.

PR #1 is complete only after the requested public testing URL is verified. No production release or mathematical result is part of this milestone.
