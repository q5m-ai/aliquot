# Five cross-domain approaches to the aliquot conjecture

## Objective and current status

The objective is a solution of the Catalan–Dickson conjecture: every positive
integer aliquot orbit terminates at 0 or eventually enters a positive cycle.
Generating attractive analogies, accumulating attempts, or establishing that
this search procedure is useful is not a substitute for resolving that question.

On 2026-10-26, five fresh research agents were launched, each with one starting
insight. **All five completed; none resolved the conjecture.** The coordinator's
[review](REVIEW.md) distinguishes the restricted size-change certificate from
method obstructions, duplicated results, and unresolved proof obligations.
All five evidence files reproduced exactly; both full-suite invocations passed
182 tests. These are not universal-proof or historical-novelty certifications.
No additional attempts, merge, or deployment are part of this work.

## Selection

[`pool.json`](pool.json) records 40 ideas from science and mathematics, written
before selection. [`selection.json`](selection.json) records one random draw of
five distinct entries, its random seed, the pool hash, Python version, and the
common source commit. There was no rejection or redraw. The selection is uniform
within this curated pool, not within the universe of scientific ideas.

The selected seeds, in draw order, are:

1. **Noether symmetry** — conservation laws from continuous variational symmetries.
2. **Small-gain feedback** — stability conditions for interconnected systems.
3. **Error-correcting syndromes** — redundancy and algebraic checks on information.
4. **Size-change termination** — well-founded descent across program transitions.
5. **Symbolic dynamics** — admissible itineraries and their realization.

Reproduce the selection, without launching anything:

```sh
python3 - <<'PY'
import hashlib
import json
from pathlib import Path
import random

root = Path('research/seed-insights')
pool_bytes = (root / 'pool.json').read_bytes()
pool = json.loads(pool_bytes)['candidates']
record = json.loads((root / 'selection.json').read_text())
assert hashlib.sha256(pool_bytes).hexdigest() == record['pool_sha256']
indices = random.Random(int(record['seed_decimal'])).sample(range(len(pool)), 5)
assert indices == record['selected_zero_based_indices']
assert [pool[i] for i in indices] == record['selected']
print('\n'.join(pool[i]['id'] for i in indices))
PY
```

## Research briefs and separation

[`brief-template.md`](brief-template.md) is the common brief. The exact supplied
briefs are retained in [`prompts/`](prompts/), with hashes and agent/worktree
identifiers in [`launches.jsonl`](launches.jsonl).

Each worker received only its own insight and the conjecture-solving assignment,
not the random-selection rationale, this coordinator record, other insights,
or the parent conversation. Workers started from separate worktrees at
`bb10bad78fcf431cdbc6da5edbb9c5f4119ae588`, before these coordinator files existed.
They were asked to use only their assigned checkout and public literature, not
other worktrees, branches, agents, or shared memory, and not to delegate further.
Git worktrees are organizational separation, not an OS security boundary.

All five use the same configured hard-math launch settings. They share the base
repository and its existing research. This is not statistical independence,
a guarantee of unbiased reasoning, or a controlled demonstration of benefit.
No assessment of the search method follows merely from producing reports.

The briefs allow both proof and disproof, require a serious attempt beyond the
surface analogy, and request explicit unsuccessful routes as well as positive
results. Each report must distinguish written mathematical arguments,
conditional reductions, bounded computations, and speculation; identify the
remaining proof obligation; and assess fruitfulness through specific output,
without an obligation to find the seed useful.

## Result handling

Each worker wrote `research/approaches/<seed-id>/REPORT.md`, with supporting
artifacts, in its own worktree. Workers did not commit, push, edit the site, or
open PRs. All 20 worker artifacts are now preserved byte-for-byte in this
checkout; [`artifacts.json`](artifacts.json) records their hashes. The original
reports were not rewritten to adopt the coordinator's assessment.

The [review](REVIEW.md) records the mathematical assessment, overlap with prior
work, all five evidence reproductions, full-suite checks, and additional
coordinator-authored exact checks. Passing software tests or obtaining agreeing
AI reports does not certify a universal proof. All five conjecture outcomes
remain **unresolved**, not pending computations or failed factorizations.
