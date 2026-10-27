# Aliquot

A [q5m research](https://www.q5m.ai) project exploring aliquot sequences and the potential proof or disproof of the aliquot sequence conjecture.

For positive integers, s(n) is the sum of the proper positive divisors of n. The conjecture asks whether every aliquot sequence eventually reaches 1 (then terminates at 0) or enters a cycle. Numerical experiments alone do not establish a proof or a divergent counterexample.

**Start here:** [Research synthesis](research/SYNTHESIS.md) — the result map for notes 01–12, exact failure cases, attribution, bounded evidence, and the remaining contradiction/recovery obligations. It distinguishes progress within this investigation from a claimed advance or solution to the conjecture.

## Milestones

1. **PR #1 — interactive research site:** adapt the supplied Aliquot HTML explorer, add the standard q5m research header/footer, and establish testing/hosting at the requested `aliquot.q5m.ai` hostname. This is a development milestone, not a production release.
2. **Research notebook 01 — growth and driver loss:** [precise statement, elementary proofs, initial literature map, and next proof obligation](research/README.md). An exact one-step census checks the exit criterion for the class n ≡ 6 (mod 12), independently recomputing divisor sums through a second algorithm. This is foundational work, not a proof/disproof or a novelty claim.
3. **Research notebook 02 — the 2-adic approach:** [adaptation of the Erdős 193 strategy](research/TWO-ADIC.md), including the exact valuation transition, an obstruction to binary-residue-only invariant growing classes, failed fingerprint candidates, and an odd-cofactor reduction with an explicit unproved avoidance obligation. A bounded two-step census is supporting verification, not an infinite-orbit result.
4. **Research notebook 03 — coupled divisibility and regeneration:** [a proved family of finite return blocks](research/REGENERATION.md), with arbitrarily large two-step amplification, exact 2–3 supply accounting, and counterexamples to universal regeneration and net-growth claims. The entry condition does not propagate: no perpetual return or novelty is established.
5. **Research notebook 04 — base-four phases and core restoration:** [an exact criterion for restoring perfect cores after prime-power spikes](research/FOUR-ADIC.md), including 28 and its v₂=2 driver. A conditional mod-4 tag propagates, but the restoration guard does not. Finite local tags and finite multiperfect-core/prime-cofactor templates have explicit limitations; no infinite closure is established.
6. **Research note 05 — global reset:** [a finiteness deduction from the classical S-unit theorem](research/GLOBAL.md). For any fixed finite prime set, only finitely many adjacent aliquot pairs use that set alone. This constrains every hypothetical escaping orbit, but does not exclude changing prime support. Lenstra's earlier arbitrary-length finite growth theorem is the benchmark; the local notes are not a demonstrated breakthrough.
7. **Research note 06 — factor transport:** [an exact conditional handoff to composite supplying blocks](research/BLOCK-TRANSPORT.md), together with correction identities and obstructions to simpler renewal rules. The output does not regenerate the input hypotheses: no closed return family or whole-orbit control is obtained.
8. **Research note 07 — deficient recovery:** [guaranteed finite rebounds and scoped template obstructions](research/RECOVERY.md). Any fixed deficient core D>1 admits arbitrarily large two-step recovery for infinitely many coprime prime cofactors; periodic prime-cofactor schedules cannot escape, and finite-core prime schedules need an expansive graph cycle. Composite entry conditions still fail to renew. No closed return class, resolution, or novelty is claimed.

9. **Research notebook 08 — exponent-vector dynamics:** [four-track geometry, combinatorics, Lehmer-five analysis, and computational scaling](research/EXPONENT-VECTORS.md). Convex abundance regions, cancellation orthogonality, and exact energy obstructions guide guarded-return research. New bounded prefixes carry replayable Lucas prime certificates; paired measurements distinguish factorization improvements from sparse-encoding claims. Modular divisor-box calculations handle symbolic trillion-sized exponents without expanding the integer. No infinite closure or solution is claimed.

10. **Research notebook 09 — supplier renewal:** [a precise guarded return lemma and exact nonclosure](research/SUPPLIER-RENEWAL.md). A two-step 28-core return gains more than 15/13, but cancellation can retain a supplier while changing its exponent and destroying its supply. A sharp residue-supplier theorem, full return-block diagnostics, and a 100000-source census preserve losing returns and censored cases. No perpetual regeneration is proved.

11. **Research notebook 10 — parity-aware supplier handoff:** [controlled replacement and a genuine supplier round trip](research/PARITY-HANDOFF.md). A fresh 181 can replace a disabled 13 and restore its useful exponent after two steps. Exact counterexamples show that the full guard still fails, even with composite cofactors. A scoped theorem rules out finite congruence refinements as a universal repair of old-supplier restoration. No closed infinite-return class is established.

12. **Research notebook 11 — backward coverage:** [a literature-backed density argument and one exact target census](research/BACKWARD-COVERAGE.md). Adapting Luca–Pomerance's collision bounds gives positive-density coverage by smaller abundant-core predecessors, not universal coverage. Through 1000000, the proposed family covers 58896 of 247545 abundant targets; even all smaller predecessors leave every Lehmer-five seed unexcluded. The remaining least-seed obligation is explicit; further census expansion is parked.

13. **Research notebook 12 — beyond density:** [a bounded-depth ancestry obstruction](research/ANCESTRY-BARRIER.md). For every fixed backward/forward depth, only a density-zero fraction of abundant direct roots is eliminated; at least X/48−o(X) candidates remain. The proof imports the valid Erdős growth theorem, not his withdrawn general decreasing claim. General forward coalescence is separate; explicit countermodels prevent inferring escape from growing test depths. No global merger mechanism or novelty is claimed, and no new large census is added.

Run the bounded experiment with `python3 -m aliquot scan-six --bound 100000`. Its code and results stay outside the served `site/` directory. Tests reproduce the [committed report](research/results/driver-six-100000.json).

No proof or disproof is claimed. Repository creation and project registration do not establish hosting acceptance.

## Python math and local verification

Python **3.11+** is the authoritative research implementation. No runtime or test dependencies are needed. Run commands from the repository root; installation is optional (`python3 -m pip install .` provides the `aliquot` command).

```sh
# Exact one-step arithmetic, including above the former website ceiling:
python3 -m aliquot sum 10000000000000000
python3 -m aliquot sum 999983 --max-work 10000

# Bounded censuses with algorithmically independent verification:
python3 -m aliquot scan-six --bound 100000
python3 -m aliquot scan-two-adic --bound 100000

# Named finite return certificates and counterexamples (not another census):
python3 -m aliquot regeneration
python3 -m aliquot core-returns

# Four-track exponent-vector report and independent orbit/prime-proof replay:
python3 -m aliquot vectors --compact > /tmp/exponent-vectors.json
python3 -m aliquot verify-vectors /tmp/exponent-vectors.json

# Supplier diagnostics reuse the committed certified extended artifact:
python3 -m aliquot renewal --compact > /tmp/supplier-renewal.json
python3 -m aliquot verify-renewal /tmp/supplier-renewal.json
# Installed copies outside this checkout need --source /path/to/exponent-vectors-extended.json.

# Exact supplier handoffs and failed renewal, without extending Lehmer traces:
python3 -m aliquot handoff --compact > /tmp/supplier-handoff.json

# Distinct abundant targets with smaller predecessors; inclusive target cap 1000000:
python3 -m aliquot backward --compact > /tmp/backward-coverage.json

# Full verification, including browser-JS parity and UI checks (needs Node.js 22+):
python3 -m unittest discover -s tests -v
# npm test is a convenience alias for the same Python runner.

# Python-only arithmetic/research checks (no Node or npm):
python3 -m unittest discover -s tests -p test_arithmetic.py -v
python3 -m unittest discover -s tests -p test_research.py -v
```

`aliquot/` uses arbitrary-precision Python `int`, exact division, and exhaustive trial factorization. The default per-call work budget is 2,000,000 candidate tests/successful divisions. A budget failure raises `ComputationLimit`; the CLI exits nonzero with no partial JSON. This is **unresolved**, not a probable-prime result or evidence of divergence. The one-step C6 census retains its separate inclusive source-bound cap of 1,000,000; the two-adic/two-step census is capped at 100,000. Named regeneration/core-restoration traces use 64 steps and a 1,000,000 source-term cap, with explicit unresolved statuses for limits. A driver exit settles only that driver's retention, not the full orbit's fate. Large integer values and rational numerators/denominators in JSON use decimal strings. Python's default decimal text-conversion safety limit remains enabled; the integer API is not restricted by that text limit.

The backward census has a separate **target** cap of 1,000,000. Multiplicative least-factor and independent additive sieves exhaust every smaller predecessor, and a second core/prime enumeration verifies the complete family representation set. It does not classify larger predecessors, extend orbits, or derive asymptotic claims from finite frequencies.

## Browser architecture and larger values

The static website keeps JavaScript for controls/canvas and an isolated `site/math.js` adapter using exact `BigInt`. Python tests compare the **actual served adapter** against the Python core, including hundreds-digit inputs. The browser no longer stops at 10¹⁵; tests cover stepping across that boundary. It has explicit resource budgets of 1,000 decimal digits per term and 2,000,000 factorization work units per step. Large smooth integers may be easy; a much smaller prime or semiprime may exhaust the budget. Trial division is not a scalable large-integer factorization engine.

Graph coordinates are approximate, never used in sequence arithmetic, and stay finite beyond floating-point range using logarithms or normalized linear coordinates. Displayed integer values remain exact. There is no claim that a finite run establishes divergence.

Starting-number presets sit beside the input. The ten curated examples cover termination, a temporary rise (30), a perfect fixed point (28), aspiring numbers reaching a perfect number (95 and 790), amicable pairs (220 and 1184), sociable cycles of length 4 and 5 (1264460 and 12496), and the unresolved sequence from 276. Selecting a shortcut shows a short explanation; the active seed is highlighted. Python tests check the finite example paths with both factorization and independent divisor-pair enumeration, without treating 276's finite prefix as a conclusion about its orbit.

The −/+ buttons restart with the adjacent seed using exact integer arithmetic, bounded below by 0 and by the browser digit budget. The wider speed slider has 20 settings spanning target step intervals of 2,040…140 ms (about 0.5…7.1 steps/s), excluding computation and frame scheduling. The fastest target is twice the previous maximum rate (280 ms per step); the 100-step checkpoints are unchanged.

Autoplay pauses at step 100, 200, 300, and every subsequent 100-step checkpoint. Click **Resume** to authorize the next block. Manual Step stays paused, and an early pause/resume does not move the next checkpoint. Reset starts a fresh run at step 0. Once the current transition finishes, a paused chart stops its animation-frame loop; hover, selection, resize, and scale changes redraw on demand.

Hover a completed point to inspect its exact value, index, digit count/parity, remainder modulo 12 alongside the full base-12 value (for example, `10₁₂` for decimal 12), known next value, and status. A compact overlay follows the point, flipping and clamping horizontally inside the chart. Pin it to reveal previous value/change and use its controls. Pinned cards and divisor lists have no internal vertical scrolling or height cap; tall cards can extend below the chart. The card also shows the prime factorization, proper positive divisors (excluding the number itself), their exact count, and exact sum. It reuses factorizations completed for sequence steps. If factors are not available, pin the point and click **Compute divisors**: this pauses autoplay and computes only that point's details, without advancing the sequence. Closing the card or resetting cancels this optional work. Zero's divisor sum stays undefined; 1 has an empty proper-divisor list.

Divisor displays are limited to **200 entries / 8,000 characters** and wrap at their natural height. Truncated lists are explicitly labelled samples, not necessarily the smallest divisors; the total count and sum remain exact. This prevents a highly composite number from creating an enormous list. Click/tap to pin; click the same point again, empty chart space, or Close to dismiss. Pins retain the selected point even when the rolling 180-point chart advances. Focus the chart and use arrow keys (or Home/End), Enter to pin, and Escape to dismiss. Hovering only reads computed data; it never launches a factorization or guesses primality. The optional compute button requires an explicit click and uses the same factorization work budget and cancellation checks as sequence computation.

Browser Python is **not included in this change**: Pyodide would add a sizeable runtime, assets, startup cost, and CSP/worker requirements without itself making factorization faster. The isolated adapter leaves room for a future self-hosted Python/WASM worker. A stronger proven factorization/certificate pipeline, rather than a language change alone, is the next step for difficult large terms.

### Reverse-orbit graph

Open **Reverse** (`/reverse/`) to search for exact positive predecessors `m` satisfying `s(m)=n`. The default target 16 has predecessors 12 and 26. The full-page-width canvas parallels Explore: **x is forward step k** (the target is at 0, backward steps are negative) and **y is numeric value**, with linear/log scales. Hollow predecessor points sit one step left of the current frontier; solid points form the chosen chain. **Clicking a predecessor immediately advances backward and refits both axes**, including the newly found candidates. Alternatives are never connected to each other; hovering one previews its forward edge. Repeated values are amber cycle links, not growth.

**Hover** shows the same floating, chart-anchored information card as Explore: exact value, parity, base 12, next term, classification, proven factors, and bounded divisors. There is no sidebar or separate Follow button. Click a chosen point to pin its card; Space or Shift-click pins any point without advancing, enabling explicit divisor computation. Arrow keys inspect points individually (including crowded predecessors); Enter selects and Escape dismisses. Touch taps on predecessors advance immediately; tap the resulting chosen point to inspect. Undo or use a pinned older point’s **Branch backward here** action to try another route. The chart redraws only on interaction/data/resize, not in an idle animation loop.

The browser exhaustively sieves sources `1 ≤ m ≤ B`, initially `B=10,000`, with a resource cap of 1,000,000. A completed table is reused; work yields to the UI and can be stopped. The sieve uses Float64 integers exactly: even the loose sum bound `m(m−1)/2 < 5×10¹¹` is below `2⁵³`. Targets and selected values use `BigInt`, and downloaded values use decimal strings. Python independently checks every sum through 10,000 by divisor-pair enumeration and upper-cap samples by both divisor pairs and factorization.

For `n>1`, any predecessor is composite and has a proper divisor `d ≥ √m`, so `n=s(m) ≥ 1+d` implies **`m ≤ (n−1)²`**. The UI reports a complete predecessor set only when the scan covers this ceiling. Otherwise, absence is only within the searched range. The only positive predecessor of 0 is 1; the predecessors of 1 are all primes, so every finite search for 1 is partial. Zero is never a source: `s(0)` remains undefined.

**Test a predecessor outside the scan** checks an explicitly entered integer using the existing exact factorization adapter and its 1,000-digit / 2,000,000-work-unit budgets. Only a verified match becomes selectable. Cancellation and budget exhaustion are unresolved, not rejection; a single manual check does not enlarge exhaustive coverage. Closing a card or changing the path cancels stale inspection work. Resetting also cancels obsolete search/verification jobs.

**All found predecessors are plotted, without pagination.** Overlapping pixels share a glyph but retain every exact keyboard/hit target; hover near a crowded group, then use ↑/↓ to inspect its neighboring values. Coordinates are approximate only; arithmetic and displayed integers remain exact. The latest **180 chosen points** are drawn, matching Explore’s rolling window, while the whole chosen path remains in tab memory with no preset backward-depth cap.

Search settings, presets, manual verification, the proof of the search ceiling, and **Download exact chain** are tucked into **Search options & limits** below the graph. The current complete/partial search coverage stays visible. The download saves the target-first path, signed target-minus-earliest gain, current search coverage, and manually verified candidates as exact JSON. Reloading starts over. Deep links such as `/reverse/?n=220` work, including **Explore backward** on a pinned home-page point. Browser memory and computation budgets remain finite, and extending an incoming path does **not** prove an unbounded forward orbit.

Run the reverse UI regressions with `node --test tests/reverse.test.mjs` or the full Python suite. Both explorers use `site/point-info.js` for their shared exact card formatting. The reverse view uses `site/reverse.js`, `site/reverse-math.js`, and `site/reverse.css`; no backend, external dependency, or CSP relaxation is introduced.

### Directed orbit graph

Open **Graph** (`/orbits/`) to explore **every start 1–1,000** as a directed graph, merging shared values and edges. The full loaded dataset has 1,665 nodes and 1,653 arrows, including values above 1,000 reached along the way (maximum 1,895,712). Only **42 nodes from starts 1–30** are drawn initially, in a rolling **80-node display window**. Exploring an orbit reveals known terms in batches of 16; predecessor actions reveal up to 25 incoming branches. On overflow, older branches leave the window but remain in the exact session data. The selected node is retained. Of these starting orbits, 948 terminate at 0, 22 reach fixed points or cycles, and 30 are unresolved at eleven source-limit frontiers. The graph includes perfect numbers 6, 28, 496 and the amicable cycle 220 ↔ 284. Use Number → Explore to reveal any loaded value or add a new start. A → … marker indicates a known successor outside the window, distinct from an unresolved computation frontier. Genuine self-loops are retained; zero has no outgoing edge because `s(0)` is undefined. Layers group distance to the terminal/cycle, not numeric size: always left-to-right, including on mobile (initially zoomed near 12 for legibility; pan or use Fit for the whole window). Placement within a layer is only layout. There is no force simulation or idle animation loop.

Primes are green, perfect numbers amber, and a pink ring marks **proved absence of any positive predecessor**. This is stronger than having no incoming arrow in the window, or being one of the 514 leaves in the full initial dataset. Among starts through 1,000, 89 targets have certified absence of predecessors. Among starts 1–100, exactly **2, 5, 52, 88, 96** have no predecessor. In particular, every possible source for 52 lies at or below `(52−1)² = 2601`, and the complete scan finds none. The edge 121 → 12 is loaded but initially hidden: select 12 and Show / add predecessors to reveal it. Node cards distinguish visible predecessors, known hidden predecessors, and the complete/partial global inverse set; 1 is characterized separately as having infinitely many prime predecessors.

Hover to inspect the shared floating exact-value card; click/tap or use Tab/Enter to pin it and highlight that node's forward orbit. **Number → Explore** selects an existing node or adds a new starting orbit; `/orbits/?n=52` also works. **Add predecessors** grows incoming branches in place: try expanding 121 to reveal additional incoming branches. **Show next +16** reveals another batch of already-known forward terms without computing. Once the known computation frontier is visible, **Extend forward +64** resumes it, even if older terms have left the window; its verified new terms are also revealed in batches. Unknown factor/divisor details are computed only with **Compute divisors**. Primality is never guessed. Drag individual nodes to move them (incident edges follow); drag empty space or Shift-drag to pan. Scroll/pinch or use ± to zoom; Fit recovers the current layout and Arrange restores the layered layout. Closing the card leaves its highlighted path visible; click the node again to reopen details. **Small overview** restores the initial window without deleting new starts or computations. Keyboard focus brings offscreen/small nodes into view. Divisor lists and the inverse-search certificate are available on the pinned card, with a link to Reverse. **Download exact graph** saves all loaded nodes (not just visible ones), edges, starting paths, bounds, inverse certificates, the optional selection, and window limits/visible IDs as JSON with decimal-string integer values.

The initial math is precomputed by authoritative Python, not approximated by the SVG renderer. `aliquot/orbit_graph.py` follows exact factorization-derived sums with a 64-step-per-start limit, a 1,000,000 source cap, and the core's 2,000,000-work-unit factorization budget. The merged known edges can resolve a frontier previously left by another seed's step limit. Remaining frontiers are explicitly unresolved, never probable primes or divergence. A separate exact additive divisor sieve checks positive sources through 1,000,000. That covers the proven inverse ceiling for every starting target 2–1,000; 1 has infinitely many prime predecessors. Larger reached targets can have partial coverage, never a no-predecessor claim from absence alone. Python independently verifies every displayed edge and the source-limit frontiers. The smaller 1–100 regression fixture retains exhaustive divisor-pair verification through its maximum required ceiling, 66,564; the larger census adds independent sampled source checks and verifies all 1,000 starting paths.

The live session adapter `site/orbit-session.js` adds only exactly verified edges. Each forward action computes at most 64 new steps, with a 1,000-digit drawn-node limit and 2,000,000 factorization work units per step. A limit retains its verified prefix and an explicitly unresolved frontier; another action may continue it. New inverse searches reuse `site/reverse-math.js`, with a default inclusive source bound of 10,000 (maximum 1,000,000, under Search settings). Already complete certificates are reused without downgrading their coverage. New nodes are labelled **Not searched**, never no-predecessor. Each action adds at most 25 missing predecessor edges to the full graph, then reveals up to 25 incoming branches in the window (new branches first, then least-recently shown known branches). It reports remaining matches independently of complete/partial/infinite search coverage. The session has a 5,000-node cap, separate from the 80-node window; unadded matches remain in the inverse record.

**Stop**, selection changes, resizing, and dragging cancel unfinished actions atomically; no partial sieve or obsolete graph edit is published. **Undo** retains ten completed graph/window actions, restoring math only when that action changed it. **Reset to starts 1–1,000** restores the initial data and small window. Changes live only in the tab. Download exports the exact current graph as `aliquot-orbit-session-v1`, including paths, inverse records, explicit session limits, and a separate `window` record; layout positions are not mathematical data and are not exported. Long labels are abbreviated only on the SVG; cards/downloads retain every decimal digit. Existing starts such as 220 highlight an exact amicable cycle, and browser arithmetic/additions are independently checked by Python.

Only the deliberately public generated artifact `site/orbit-data.js` is served; the generator and source research remain outside `site/`. No runtime dependencies, backend, external assets, or CSP changes are needed. Reproduce/check the artifact with:

```sh
python3 scripts/build_orbit_graph.py
python3 scripts/build_orbit_graph.py --check
python3 scripts/version_assets.py
node --test tests/orbits.test.mjs tests/orbit-session.test.mjs
```

The generator also reproduces `tests/fixtures/orbit-data-100.js`, a small, independently checked fixture for interaction and resource-limit regressions. It is outside the served directory. The test suite rejects stale data and assets. This bounded graph is for pattern discovery; it does not resolve the aliquot conjecture or establish any divergent orbit.

### Orbit-length chart

Open **Lengths** (`/lengths/`) for starting number versus steps to 0 or the first repeated value. The y-axis is logarithmic with ticks 1, 2, 5, 10, 20, 50, **100+**. Resolved lengths at or above 100 are clipped visually, not altered in the data. Seed 138 retains its exact 178 steps to 0 (177 to 1). The range selector shows starts 1–100, 1–300, 1–1,000 (default), 1–5,000, or all **1–10,000**. The SVG uses compact marks and x-bucket hit testing, so dense points are selected by proximity rather than paint order; every seed is also available with the keyboard.

Hover uses the **same floating point card** as Explore, Reverse, and Graph: exact seed value, classification, next value, digit count/parity, mod 12/base 12, self-hosted TeX factorization, proper divisors, and their count/sum. All seed factorizations are precomputed and certified; shared `AliquotPointInfo` formatting never launches factorization on hover. The card additionally shows exact orbit length or its lower bound. Click/tap or Enter to pin; a pin keeps its seed while the pointer moves, reveals full details and the peak/frontier, and links to Graph and Reverse. Close/Escape dismiss; keyboard arrows and Home/End inspect seeds; 138/276 shortcuts pin those examples. Cards flip/clamp inside the chart horizontally and follow resize; tall pinned cards can extend below the chart without internal scrollbars. The former static selection box is removed. There is no idle animation or browser-side orbit computation.

The exact Python dataset has 8,951 terminated starts, 224 reaching a cycle/fixed point, and 825 unresolved within its bounds (818 factorization limits, 7 step limits): 256 steps per seed, an inclusive source-value ceiling of 10³⁰, and 2,000,000 trial-factorization work units per new source. A failure is not treated as a probable prime. Unresolved runs use hollow upward arrows; below the display cap, a dashed range starts at the proved lower bound (verified steps + 1). For example, 276's 79 verified steps establish a resolution time of at least 80, **not** a measured 100-step run or divergence. Its range extends upward through the cap rather than inventing a length. Shared tails mean these are not independent trials.

Only the deliberately public `site/length-data.js` is served. Its download contains all seed records, bounds, exact edges and prime factorizations, with integer values as decimal strings. Tests independently verify primality, enumerate divisors from the certificates, replay every path, and reproduce the artifact. Generator and verifier stay outside `site/`:

```sh
python3 scripts/build_orbit_lengths.py
python3 scripts/build_orbit_lengths.py --check
python3 scripts/version_assets.py
node --test tests/lengths.test.mjs
```

#### Long-orbit counting function and frequency

Below the scatter plot, **How common are long orbits?** (`/lengths/#frequency`) defines `L_t(x)` as the number of selected seeds through `x` whose resolution time is at least `t`. Thresholds are 10, 25, 50, 100 (default), and 200 steps. Compare the cumulative counting function (like π(x)), cumulative share, or the share in the last 1,000 seed values. The frequency chart has a separate linear y-axis with a zero baseline; the scatter remains logarithmic/capped at 100+. All/even/odd filters use the actual number of eligible seeds as denominator, including for the recent window. Recent curves start at the first complete window, x = 1,000. Range options extend to 10,000.

The solid lower curve counts resolved long orbits plus unfinished runs whose verified lower bound already meets the threshold. The dashed upper curve also counts unfinished runs still uncertain at that threshold. The shaded band is **computation uncertainty, not a confidence interval**; unresolved is not synonymous with long or divergent. Percentages with uncertainty are rounded outward to two decimal places. Counts and denominators are exact integers, and there is no independence assumption: merging seeds are counted separately.

For 100+ steps, seeds 1–1,000 contain 22–30 qualifying starts (2.20–3.00%), while 9,001–10,000 contain 58–133 (5.80–13.30%). Thus the last block has a higher frequency even under the most conservative classification of uncertain cases. Across all 10,000 starts the count is 581–1,056 (5.81–10.56%). This is a finite-range comparison, not monotonicity or an asymptotic statement. A rising cumulative count alone would not demonstrate increasing frequency.

Hover/pin the shared-style aggregate card to inspect any integer bound, or use arrows/Home/End/Enter/Escape. A table compares consecutive 1,000-seed blocks under the same threshold/population filters. Download exact counts saves cumulative, recent-window, and block bounds with source computation limits; percentages and interpolated chart coordinates are not stored as exact data. `site/length-frequency.js` derives these counts without any new orbit computations. Python independently checks every cumulative/recent/block result against direct classified-seed sets and binary searches; Node covers threshold boundaries, zero denominators, controls, cards, and exports.

### Formula rendering

The definition and iteration rule sit directly below the title. Explicit `data-tex` fields and point-card factorizations use **self-hosted KaTeX 0.19.0**, with native MathML output and readable text fallbacks. There are no CDN requests, extra font downloads, or relaxed CSP rules. Unchanged formulas are cached rather than re-typeset on hover.

The pinned bundle and MIT license are in `site/vendor/katex/`; provenance and hash are recorded there and checked by tests. `site/latex.js` keeps untrusted commands disabled and bounds expression length/expansion. Static formulas use `data-tex` (and `data-display="true"` for display math); arithmetic still uses Python/BigInt, never the typesetter.

## Local website development

For a local-only server: `python3 -m http.server --directory site --bind 127.0.0.1 8000`.
For managed LAN testing, let the platform allocate the port:

```sh
q5m-lab serve --directory ./site --json
```

Only `site/` is served. Explore and Reverse compute in the browser; Graph starts with a committed, Python-verified public dataset and uses the same exact browser arithmetic for explicit live additions. Serving the committed site requires no backend, account, external script, or build step. Local Python code and research reports are never served. The explorer UI is `site/explorer.js`, with its presentation in `site/index.html` and `site/site.css`. The dedicated `/research/` timeline lives in `site/research/index.html` and `site/research.css`, with dated findings, explicit limitations, and pinned links to the source notes. It loads only the shared formula renderer, not the explorer runtime. The header follows Erdős 193's brand/navigation pattern; the footer uses Causal Sets' q5m/GitHub markup. Shared chrome uses a system-font fallback without requiring Google Fonts.

Python's `unittest` runner covers exact sums, independent sieve/divisor-pair verification, census reproduction, CLI failures, hosting boundaries, and Python/browser parity. It also invokes Node's UI harness for cycle marking, zero/perfect states, invalid inputs, cancellation, step control, budget exhaustion, finite canvas coordinates for hundreds-digit values, and hover/pin/keyboard inspection (including high-DPI hit testing, overlay bounds at desktop/mobile sizes and after resize, reset/eviction, exact long values, base-12 conversion, bounded divisor lists, explicit computation and cancellation). Browser factorization, divisor counts/sums, and small complete divisor lists are also checked against Python. These are mocked canvas checks, not a real-browser visual or phone test.

CSS and JavaScript URLs on all pages include a SHA-256 content version so browser/CDN caches cannot reuse an older asset after its content changes. After editing a CSS or JS file, run `python3 scripts/version_assets.py` and commit the refreshed HTML with the asset. `python3 scripts/version_assets.py --check` and the test suite reject stale versions. The helper stays outside `site/`; no runtime or deployment build step is required.

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
