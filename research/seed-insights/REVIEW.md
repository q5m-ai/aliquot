# Review of the five seed-insight attempts

## Bottom line

**None of the five attempts resolves the Catalan–Dickson aliquot conjecture.**
None supplies an orbit-wise bound for arbitrary starts, a global descending
quantity, or one seed with a rigorously repeatable escape mechanism.

The most concrete positive result is the **size-change certificate for prime
cofactors with cores at most 17**. The other principal additions are scoped
obstructions to proposed methods. They are worth retaining to prevent false
proofs, but are not evidence of a breakthrough or evidence for either truth
or falsity of the conjecture.

All five reports, supporting programs, and tests were read. Their main partial
arguments were checked against their stated hypotheses and the existing source
notes. I did not identify a fatal gap in the scoped conclusions summarized
below. This is an AI mathematical review, **not** human peer review, proof-
assistant verification, or a historical-priority determination. Numerical
reproduction is a separate acceptance check, not certification of those proofs.

## Findings by approach

| Seed | Strongest retained finding | Review judgment and boundary |
| --- | --- | --- |
| [Noether symmetry](../approaches/noether-symmetry/REPORT.md) | Actual guarded 84-core edges can replenish a proposed 3-adic resource by any prescribed amount. This rules out every nonincreasing height `a log(u+4)+b v_3(u+4)` with `a>0` on all such edges. A separate CRT argument rules out closure of unbounded finite unions of the specified prime-core progression families. | Valid, narrowly scoped negative results. The variational lift has an auxiliary conserved current, but it does not bound the arithmetic state. The useful prime-only denominator argument was already in the repository. No conservation-based solution emerged. |
| [Small-gain feedback](../approaches/small-gain-feedback/REPORT.md) | A composite-aware finite-graph gain condition implies boundedness when all its arithmetic hypotheses hold. Around chosen cores `20→4→20`, arbitrarily large finite amplification is possible despite bare gain `33/40<1`. | The comparison theorem is sound as a conditional statement. Its missing uniform cofactor bounds are not supplied. The middle term also has a 20-core: this is not a lost-driver restoration theorem. Core return does not regenerate the entry conditions. |
| [Error-correcting syndromes](../approaches/error-correcting-syndromes/REPORT.md) | Every realized fixed residue signature of `n, sigma(n), s(n)`, even with the stated finite valuation constraints, is compatible with arbitrarily large abundancy. A complete criterion identifies which affine prime models evade every fixed finite sieve. | A genuine obstruction to these finite signatures, not to all adaptive or factorization-aware arguments. The proposed coding residual neither reconstructs future factors nor provides a bounded error budget. The sieve criterion overlaps the symbolic report exactly. |
| [Size-change termination](../approaches/size-change-termination/REPORT.md) | A present-state lexicographic rank strictly decreases on every internal aliquot edge above 527 whose endpoints have a prime cofactor and core at most 17. The first unresolved core, 18, has an explicit two-branch return and a necessary balanced-valuation law. | The strongest concrete positive certificate in this batch. The finite domain of cores still represents infinitely many integers. However, arbitrary trajectories are not confined to it; leaving it is not resolution. The core-18 calculation narrows a question but does not close it. |
| [Symbolic dynamics](../approaches/symbolic-dynamics/REPORT.md) | Arbitrarily long actual growing prefixes can remain divisible by any fixed modulus. Thus even the complete valid finite-word language of the specified abundance/residue code cannot exclude the constant growing word. The 120-core affine model has compatible profinite paths but no infinite all-prime positive-integer lift. | Sound diagnostics against an invalid compactness or finite-state argument. The growing-word result adapts Lenstra's existing construction. The affine-sieve theorem duplicates the coding report. No lifting or descent theorem for actual unrestricted orbits was found. |

## The positive certificate, stated without overstating coverage

Let

```text
X = {n>527 : n=a p, 1<=a<=17, p prime}.
```

The representation is unique and coprime, since `p>31>a`. The rank is

```text
rho(ap) = (2, 1)             if a=6 and p=2 mod 3,
          (2, 0)             if a=6 and p=1 mod 3,
          (1, v_3(p+7))      if a=12,
          (0, ap)            otherwise.
```

The proof accounts for every edge with both endpoints in X:

- Apart from 6 and 12, the permitted cores are deficient; above the stated
  threshold the integer decreases. Parity and reduction modulo 3 prevent
  those sources from entering either exceptional core.
- A 6-core edge internal to X must be `6p→6(p+2)`, with both cofactors prime.
  It spends the one available residue phase and cannot repeat internally.
- A 12-core edge either drops to core 4, lowering the first coordinate, or
  obeys `p'+7=(4/3)(p+7)`, spending one unit of `v_3(p+7)`.

Thus no infinite tail can stay entirely in X. Since every escaping orbit
would eventually exceed 527, this proves:

> An orbit whose sufficiently late positive terms all have a prime cofactor
> and core at most 17 cannot escape.

Equivalently, every hypothetical escaping orbit must have
`n_k/P+(n_k)>=18` at infinitely many indices, where P+ is the largest prime
factor. It does **not** prove that quotient tends to infinity, that every
start with such a small core is resolved, or that domain exits come back
with a smaller rank. The cutoff 17 is not proved optimal.

This is a concrete deduction relative to the inspected repository, using
its established affine/valuation ideas. Historical novelty is unassessed.
The more ambitious continuation remains an arithmetically guarded switching
problem: its balanced recharges and intermediate primality conditions are
not controlled indefinitely.

## The common obstacle is still present

The exact identity used throughout the reports is

```text
s(Du) = s(D)u + sigma(D)s(u),       gcd(D,u)=1.
```

When u is prime, `s(u)=1` and the dynamics becomes affine. This makes
valuation depletion, modular traps, and graph calculations tractable. The
restriction is not preserved. For composite u, the correction
`delta(u)=s(u)-1` depends on the new factorization and can defeat the
proposed resource accounting.

Three independently rechecked examples make this concrete:

- **Conservation resource replenishment:** `206220→455028` preserves the
  coprime 84-core while `v_3(u+4)` rises from 0 to 1. The report's CRT/
  Dirichlet proof makes this increase arbitrarily large, but with different
  one-step seeds, not one perpetually replenishing orbit.
- **Return without renewal:** `3580→3980→4420` returns to a unitary 20-core,
  but its cofactor changes from prime 179 to composite `221=13·17`. The
  next supplier condition fails. The core representations overlap, so a
  bare product less than one is not a physical contraction estimate.
- **A prime-model obstruction does not stop the actual orbit:** the 120-core
  cofactors `7→17→37→77→211` pass through a composite and regain a prime.
  The affine model's forced divisibility does not survive the actual
  composite correction. Later loss of the coprimality guard is a failure
  of that representation, not a conclusion about the orbit.

Each report preserves this distinction. No report supplies the missing
whole-orbit control through arbitrary factorization changes.

## How distinct were the attempts?

**Five different seeds did not produce five substantially distinct closing
mechanisms.** All five initial routes returned to prime-cofactor affine
representations and recognized overlap with the existing periodic-core
obstruction. The coding and symbolic agents independently assigned to their
seeds produced the *same* finite-sieve criterion:

```text
For f(x)=a x+b, a>=2, b>=1, every fixed finite modulus has a
unit-surviving residue iff gcd(a,b)=1 and rad(a-1) divides b.
```

They also used the same 120-core model and composite repair example. Count
that as one mathematical result, not two advances or two independent pieces
of evidence for the conjecture. The reports do have distinct side results,
notably the coding signature construction and the symbolic finite-word
obstruction.

The overlap is observable; its cause is not established by this batch.
Shared model configuration, common background, and the mathematical structure
are all possible influences. There was no unseeded control or alternate-model
comparison. These findings do not establish that random seeding is useful,
useless, or intrinsically incapable of producing a different connection.
**This batch produced no unlocking connection.** No further attempts were
launched during this review.

## Verification actually performed

The 20 worker artifacts (five reports, five programs, five evidence files,
and five test files) were copied byte-for-byte into this checkout. Their
hashes are in [`artifacts.json`](artifacts.json); the worker files were not
edited. The original reports retain their original verification claims,
including incomplete/time-limited runs; this review does not rewrite them.

From the repository root:

```sh
python3 -m unittest discover -s tests -v
npm test
node --check site/explorer.js
node --check site/math.js
node --check site/latex.js
```

Both full-suite invocations passed **182 tests**, including the 50 new
worker tests. All three JavaScript syntax checks passed. `npm test` invokes
the same Python runner; it is not an independent test system. Each of the
five standalone `verify.py` programs was also rerun, and its stdout matched
its retained `evidence.json` byte-for-byte.

The additional coordinator-authored [`review_checks.py`](review_checks.py)
imports neither worker arithmetic nor the production aliquot module:

```sh
python3 research/seed-insights/review_checks.py > /tmp/aliquot-review-evidence.json
cmp /tmp/aliquot-review-evidence.json research/seed-insights/review-evidence.json
```

Its declared finite scope and results are:

- 40 distinct named aliquot edges recomputed by divisor-pair enumeration;
  largest source 275247820, source cap 300000000. Known successors can
  exceed the source cap; they are not silently iterated.
- An additive divisor sieve through 300000 inclusive, cross-checked by
  divisor pairs on 1…1000.
- All 69283 sources in X at or below 200000 checked. Their 20110 internal
  edges all decrease the stated rank. The other 49173 sources leave X;
  **these exits are not declared resolved or divergent**. Every successor
  is within the independent sieve's coverage.
- The six named 84-core replenishment witnesses, the coding signature
  collision, and the guarded composite counterexample checked separately.
- Zero unresolved arithmetic checks within these limits.

The saved result is [`review-evidence.json`](review-evidence.json). These
finite checks support arithmetic reliability, not universal proof claims.
The mathematical review of quantifiers, guards, and arguments is separate.
No exhaustive literature search, formalization, merge, or deployment was
performed.

## Disposition

Retain the size-change certificate and its exact boundary calculation as a
restricted positive result. Retain the other scoped obstructions and
counterexamples as a record of approaches that do not close. Do not present
this batch as a solution, a major advance, five independent discoveries, or
a demonstrated reason to expand the search. The objective remains a solution
of the conjecture; that objective has not been met.
