# Aliquot

A [q5m research](https://www.q5m.ai) project exploring aliquot sequences and the potential proof or disproof of the aliquot sequence conjecture.

For positive integers, s(n) is the sum of the proper positive divisors of n. The conjecture asks whether every aliquot sequence eventually reaches 1 (then terminates at 0) or enters a cycle. Numerical experiments alone do not establish a proof or a divergent counterexample.

## Milestones

1. **PR #1 — interactive research site:** adapt the supplied Aliquot HTML explorer, add the standard q5m research header/footer, and establish testing/hosting at the requested `aliquot.q5m.ai` hostname. This is a development milestone, not a production release.
2. **Research notebook 01 — growth and driver loss:** [precise statement, elementary proofs, initial literature map, and next proof obligation](research/README.md). An exact one-step census checks the exit criterion for the class n ≡ 6 (mod 12), independently recomputing divisor sums through a second algorithm. This is foundational work, not a proof/disproof or a novelty claim.

Run the bounded experiment with `python3 -m aliquot scan-six --bound 100000`. Its code and results stay outside the served `site/` directory. Tests reproduce the [committed report](research/results/driver-six-100000.json).

No proof or disproof is claimed. Repository creation and project registration do not establish hosting acceptance.

## Python math and local verification

Python **3.11+** is the authoritative research implementation. No runtime or test dependencies are needed. Run commands from the repository root; installation is optional (`python3 -m pip install .` provides the `aliquot` command).

```sh
# Exact one-step arithmetic, including above the former website ceiling:
python3 -m aliquot sum 10000000000000000
python3 -m aliquot sum 999983 --max-work 10000

# Bounded census with algorithmically independent verification:
python3 -m aliquot scan-six --bound 100000

# Full verification, including browser-JS parity and UI checks (needs Node.js 22+):
python3 -m unittest discover -s tests -v
# npm test is a convenience alias for the same Python runner.

# Python-only arithmetic/research checks (no Node or npm):
python3 -m unittest discover -s tests -p test_arithmetic.py -v
python3 -m unittest discover -s tests -p test_research.py -v
```

`aliquot/` uses arbitrary-precision Python `int`, exact division, and exhaustive trial factorization. The default per-call work budget is 2,000,000 candidate tests/successful divisions. A budget failure raises `ComputationLimit`; the CLI exits nonzero with no partial JSON. This is **unresolved**, not a probable-prime result or evidence of divergence. The census retains its separate inclusive source-bound cap of 1,000,000. Large integer values in JSON use decimal strings. Python's default decimal text-conversion safety limit remains enabled; the integer API is not restricted by that text limit.

## Browser architecture and larger values

The static website keeps JavaScript for controls/canvas and an isolated `site/math.js` adapter using exact `BigInt`. Python tests compare the **actual served adapter** against the Python core, including hundreds-digit inputs. The browser no longer stops at 10¹⁵; tests cover stepping across that boundary. It has explicit resource budgets of 1,000 decimal digits per term and 2,000,000 factorization work units per step. Large smooth integers may be easy; a much smaller prime or semiprime may exhaust the budget. Trial division is not a scalable large-integer factorization engine.

Graph coordinates are approximate, never used in sequence arithmetic, and stay finite beyond floating-point range using logarithms or normalized linear coordinates. Displayed integer values remain exact. There is no claim that a finite run establishes divergence.

Starting-number presets sit beside the input. The ten curated examples cover termination, a temporary rise (30), a perfect fixed point (28), aspiring numbers reaching a perfect number (95 and 790), amicable pairs (220 and 1184), sociable cycles of length 4 and 5 (1264460 and 12496), and the unresolved sequence from 276. Selecting a shortcut shows a short explanation; the active seed is highlighted. Python tests check the finite example paths with both factorization and independent divisor-pair enumeration, without treating 276's finite prefix as a conclusion about its orbit.

The −/+ buttons restart with the adjacent seed using exact integer arithmetic, bounded below by 0 and by the browser digit budget. The wider speed slider has 20 settings spanning target step intervals of 2,040…140 ms (about 0.5…7.1 steps/s), excluding computation and frame scheduling. The fastest target is twice the previous maximum rate (280 ms per step); the 100-step checkpoints are unchanged.

Autoplay pauses at step 100, 200, 300, and every subsequent 100-step checkpoint. Click **Resume** to authorize the next block. Manual Step stays paused, and an early pause/resume does not move the next checkpoint. Reset starts a fresh run at step 0. Once the current transition finishes, a paused chart stops its animation-frame loop; hover, selection, resize, and scale changes redraw on demand.

Hover a completed point to inspect its exact value, index, digit count/parity, remainder modulo 12 alongside the full base-12 value (for example, `10₁₂` for decimal 12), known next value, and status. A compact overlay follows the point, flipping and clamping horizontally inside the chart. Pin it to reveal previous value/change and use its controls. Pinned cards and divisor lists have no internal vertical scrolling or height cap; tall cards can extend below the chart. The card also shows the prime factorization, proper positive divisors (excluding the number itself), their exact count, and exact sum. It reuses factorizations completed for sequence steps. If factors are not available, pin the point and click **Compute divisors**: this pauses autoplay and computes only that point's details, without advancing the sequence. Closing the card or resetting cancels this optional work. Zero's divisor sum stays undefined; 1 has an empty proper-divisor list.

Divisor displays are limited to **200 entries / 8,000 characters** and wrap at their natural height. Truncated lists are explicitly labelled samples, not necessarily the smallest divisors; the total count and sum remain exact. This prevents a highly composite number from creating an enormous list. Click/tap to pin; click the same point again, empty chart space, or Close to dismiss. Pins retain the selected point even when the rolling 180-point chart advances. Focus the chart and use arrow keys (or Home/End), Enter to pin, and Escape to dismiss. Hovering only reads computed data; it never launches a factorization or guesses primality. The optional compute button requires an explicit click and uses the same factorization work budget and cancellation checks as sequence computation.

Browser Python is **not included in this change**: Pyodide would add a sizeable runtime, assets, startup cost, and CSP/worker requirements without itself making factorization faster. The isolated adapter leaves room for a future self-hosted Python/WASM worker. A stronger proven factorization/certificate pipeline, rather than a language change alone, is the next step for difficult large terms.

### Formula rendering

The definition and iteration rule sit directly below the title. Explicit `data-tex` fields and point-card factorizations use **self-hosted KaTeX 0.19.0**, with native MathML output and readable text fallbacks. There are no CDN requests, extra font downloads, or relaxed CSP rules. Unchanged formulas are cached rather than re-typeset on hover.

The pinned bundle and MIT license are in `site/vendor/katex/`; provenance and hash are recorded there and checked by tests. `site/latex.js` keeps untrusted commands disabled and bounds expression length/expansion. Static formulas use `data-tex` (and `data-display="true"` for display math); arithmetic still uses Python/BigInt, never the typesetter.

## Local website development

For a local-only server: `python3 -m http.server --directory site --bind 127.0.0.1 8000`.
For managed LAN testing, let the platform allocate the port:

```sh
q5m-lab serve --directory ./site --json
```

Only `site/` is served. Website sequence computation happens in the browser; no backend, account, external script, or build step is required. Local Python code and research reports are never served. The explorer UI is `site/explorer.js`, with its presentation in `site/index.html` and `site/site.css`. The header follows Erdős 193's brand/navigation pattern; the footer uses Causal Sets' q5m/GitHub markup. Shared chrome uses a system-font fallback without requiring Google Fonts.

Python's `unittest` runner covers exact sums, independent sieve/divisor-pair verification, census reproduction, CLI failures, hosting boundaries, and Python/browser parity. It also invokes Node's UI harness for cycle marking, zero/perfect states, invalid inputs, cancellation, step control, budget exhaustion, finite canvas coordinates for hundreds-digit values, and hover/pin/keyboard inspection (including high-DPI hit testing, overlay bounds at desktop/mobile sizes and after resize, reset/eviction, exact long values, base-12 conversion, bounded divisor lists, explicit computation and cancellation). Browser factorization, divisor counts/sums, and small complete divisor lists are also checked against Python. These are mocked canvas checks, not a real-browser visual or phone test.

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
