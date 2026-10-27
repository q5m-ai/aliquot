You are investigating the Catalan–Dickson aliquot sequence conjecture. Make a serious mathematical attempt to resolve it, starting from the insight below. The objective is a proof or disproof of the conjecture, not merely an attractive analogy or a numerical study.

## Starting insight

size-change-termination — program verification

Size-change termination: track strict and weak descent of well-founded quantities across transitions; suitable composed transition graphs force an infinite descending thread in any hypothetical infinite execution.

Develop a concrete mathematical bridge from this insight to aliquot dynamics. Do not assume the source theorem applies: define its proposed objects and verify the hypotheses, or derive and justify an appropriate analogue. If a literal transfer fails, pursue the strongest mathematically justified variation rather than stopping at a superficial mismatch. You may follow a productive implication beyond the original analogy; identify where that happens. Neither a positive assessment nor a negative assessment is preferred.

## Exact target

For a positive integer n, let sigma(n) be the sum of all positive divisors and s(n)=sigma(n)-n. Starting at any n_0>=1, iterate n_(k+1)=s(n_k) while positive. s(1)=0 and s(0) is undefined. The conjecture is that every orbit terminates at 0 or eventually enters a positive cycle, including a perfect-number fixed point.

An infinite nonperiodic orbit has distinct positive values and tends to infinity, though it need not grow monotonically. A proof must cover every starting integer, allowing cycles. A disproof needs an explicit starting integer with a rigorous infinite-escape argument. Unbounded finite prefixes, large peaks, failure to factor, positive average drift, or a formally admissible but unrealized itinerary do not establish either result.

## Working approach

- First develop your own mathematical mapping and most promising proof route. Then consult research/SYNTHESIS.md and the relevant source notes to distinguish actual additions from already established results and known counterexamples. Do not assume the existing research framework is the only one available.
- Seek a mechanism that closes: a well-founded descent, orbit-wise bound, contradiction for any escaping orbit, or explicit indefinitely repeatable escape construction. Be equally willing to prove or disprove the conjecture.
- Work beyond merely naming an equivalent missing theorem. Try to prove the difficult step; use exact counterexamples to revise failed claims. Be explicit about all quantifiers, exceptional cases, cycle handling, realizability, and imported theorems.
- Make one substantial attempt. If no solution emerges, deliver the strongest precisely justified partial result and the exact remaining obstruction. Do not manufacture a promising conclusion or claim historical novelty without checking relevant literature.
- Distinguish a mathematical argument from software verification. Exact computations may reject candidate claims and check examples but cannot certify a universal theorem. State limits before substantial searches and preserve unresolved cases. Avoid open-ended brute-force searches and expensive attempts to extend known hard orbits.

## Workspace and verification

Use only your assigned checkout and public literature; do not inspect other worktrees, branches, agents, session transcripts, or shared agent memory. Do not delegate to additional agents. Follow AGENTS.md. Do not change site/, deployment settings, credentials, or the core API. No hosting, merging, or deployment is authorized.

Python 3.11+ exact arithmetic is authoritative. The existing aliquot module exports factorize, aliquot_sum, and ComputationLimit. Factorization budget failure is unresolved, never a probable-prime shortcut. Independently check important finite examples by divisor-pair enumeration or an additive divisor sieve where feasible. Use exact integers/rationals and decimal strings for large persisted integers. Record commands, inclusive bounds, step/work limits, and unresolved counts. Use bounded computations; no new runtime dependencies are needed.

Write the main report to research/approaches/size-change-termination/REPORT.md. Put any supporting standalone scripts/data in the same directory and any regression tests in uniquely named tests/test_size_change_termination.py. Do not edit existing shared research notes. Do not commit, push, or open a PR; the coordinating researcher will review and integrate the work. Run focused verification for any added code and report exactly what ran.

## Required report

1. **Verdict:** conjecture resolved by a candidate proof/disproof, or unresolved. Any candidate solution requires a complete argument, not just an outline, and must be labeled as awaiting independent review.
2. **Mathematical bridge:** concrete definitions and the relevant source insight, including hypotheses that do or do not transfer.
3. **Results:** separate proved statements with written proofs, conditional results, finite observations, and speculation. State what is already present in the repository or known literature.
4. **Failed routes:** the strongest proposals actually attempted, their counterexamples or precise broken steps, and any revisions pursued.
5. **Remaining obligation:** the smallest explicit statement still needed, why you could not establish it, and how it relates to the full conjecture. Do not disguise the original conjecture as a new lemma.
6. **Evidence and reproducibility:** exact commands and computation bounds; distinguish independent arithmetic checks from a mathematical proof review.
7. **Fruitfulness assessment:** useful, not useful, or undetermined for this attempt, supported by specific mathematical output rather than enthusiasm, elapsed effort, or amount of code. A restricted obstruction or reformulation is not automatically progress toward a complete solution.

End your response with the report path, a concise clinical summary of the strongest result and its limitation, verification performed, and an explicit statement of whether the conjecture has been resolved.
