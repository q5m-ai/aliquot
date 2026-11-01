# Research synthesis: findings, limits, and the two routes forward

**Bottom line:** we can force finite growth, transport some supplying factors,
restore some lost core exponents, and guarantee recovery after a deficient step.
We can also exclude several simple invariant and prime-cofactor templates.
**We cannot yet make the recovery conditions reproduce themselves, or force a
general escaping orbit into a contradiction. No solution, divergent seed, or
historical novelty is claimed.**

This is the reading guide for notebooks 01–17, the composite-renewal follow-up,
and the literature audit.
[Notebook 08](EXPONENT-VECTORS.md) adds an exponent-vector research program:
convex growth regions, cancellation orthogonality, exact obstructions to simple
energies, modular divisor-box combinatorics, and certified Lehmer/control traces.
[Notebook 09](SUPPLIER-RENEWAL.md) proves a guarded two-step 28-core return,
then exhibits exact guard failure when a retained supplier's exponent changes
parity. [Notebook 10](PARITY-HANDOFF.md) supplies a controlled replacement and
an actual return of the original supplying exponent, then shows that the full
handoff guard still fails. It also excludes a congruence-only repair of the
specified old-supplier return, while preserving actual prime predecessors.
[Notebook 11](BACKWARD-COVERAGE.md) tests backward exclusions: an explicit
adaptation of Luca–Pomerance's collision method supplies positive-density
coverage by smaller predecessors, but neither that argument nor the complete
million-target census forces a least escaping seed into a covered class.
[Notebook 12](ANCESTRY-BARRIER.md) proves that every fixed-depth ancestry/forward
extension eliminates only a density-zero part of the direct roots. It separates
that limitation from genuine forward coalescence and from infinite survival.
[Notebook 13](BOUNDARY-OUTFLOW.md) translates boundary outflow into exits,
returns, and still-open excursions. It derives fixed-time and fixed-scale
first-passage corollaries, separates unrelated all-source inflow from actual
returning paths, and keeps starting labels when paths merge. It supplies no
same-label bound across indefinitely many fences.
[Notebook 14](MINIMUM-ESCAPE.md) deletes a prime directly from a least escaping
seed to obtain a resolved smaller companion. Exact divisibility transport has
a narrow perfect-core exception. A CRT/Dirichlet lift of Lenstra's finite
supplier chain produces arbitrarily long amplified blocks above any fixed
core, including a terminating companion; uniform error bounds fail. The tested
valuation-budget repairs also replenish without bound. No seed-dependent
global comparison or least-seed contradiction is obtained.
The [composite-renewal follow-up](COMPOSITE-RENEWAL.md) obtains an actual
full return to a `160`-core prime-entry guard, then proves that a fixed supplier
bridge consumes a finite divisibility budget. A composite exchange reaches a
quadruple-perfect growing core, but its new unitarity guard need not persist.
Nonempty finite unions of unitary-core classes (cores greater than one) with
arbitrary complementary remainders are not invariant; reduced residue refinements of the stated supplying classes
do not repair that result. Equal-valuation retention and its composite failure
are derived separately. These scoped obstructions do not say every individual
orbit leaves a finite core list, or exclude changing, factorization-aware
suppliers and variable-time returns.
[Notebook 15](MAXIMUM-CONTRADICTION.md) attempts the opposite contradiction:
assume all orbits are bounded and challenge an actual orbit maximum. Abundance
and two-step recovery exclude some peak shapes, but neither condition persists.
It proves that no initial interval through B >= 24 is forward-closed, while the
fully resolved cohort through 24 has the finite, non-interval closure with
maximum 55. Orbit peaks also fail divisibility monotonicity. Expanding an
interval enclosure is therefore not an escaping orbit.
[Notebook 16](RETURN-CLOSURE.md) tries to repair that missing return condition.
A finite prime-supplier relay can preserve a growing 160-core for any prescribed
finite duration, even inside any reduced refinement of the original prime-entry
progression. Consequently those congruences cannot guarantee a uniformly bounded
return to the deficient entry class. An actual composite entry renews once;
a smaller 12-bridge fails a separate return test. The relay's strict prime-square
supply rule cannot form a finite cycle. A separate construction forces a genuinely
fresh supplier and renews a larger abundant-core guard once, but its output loses
the prime-cofactor hypothesis. No perpetual renewal is proved.
[Notebook 17](COMPOSITE-HANDOFF.md) carries the fresh handoff through a composite
residual: an exact orbit makes two successive replacements. Neutral replacement
forces a more-than-sixfold supplier decrease. A prime tag permits nonneutral,
arbitrarily large fresh suppliers with powered residuals, but that input shape
also has a proved nonrenewal subfamily. Another theorem blocks any prescribed
finite replacement menu while preserving actual prime predecessors and the full
core guard. Periodic prime bridges consume a finite 2-adic denominator budget,
specializing the existing periodic-core obstruction. None supplies an invariant
larger-return class.
None closes the remaining whole-orbit obligations. This synthesis
consolidates the factor-transport work originally in PR #4 with the recovery
work in PR #6. Notes 01–05 were already incorporated through PR #3; the summary
does not present them as new changes in PR #6. PR #5 was site presentation only.
All source notes and regression tests are now available on this branch; no
merge to `main` or deployment is implied.

“Proved” below means that a mathematical argument is written out, with imported
theorems identified—not that software tests, AI audits, or a merged PR certify
it. Conditional statements retain every stated hypothesis. Finite examples are
separate evidence. Human mathematical review and historical novelty checks
remain outstanding.

## 1. Definitions and the central distinction

For n>0, let σ(n) be the sum of all positive divisors and s(n)=σ(n)−n. Iterate
while positive; s(0) is undefined. A source is abundant, perfect, or deficient
according as s(n) is greater than, equal to, or less than n.

The Catalan–Dickson conjecture predicts termination or eventual positive
periodicity, including perfect fixed points. An infinite nonperiodic orbit has
distinct positive terms, hence tends to infinity. It need not grow monotonically.

- **Core:** a chosen factor D in n=Du. Multiplying divisor sums requires
  gcd(D,u)=1 at **each source**, not merely at the initial seed.
- **Unitary factor:** d|n with gcd(d,n/d)=1. Ordinary divisibility alone does
  not justify σ(n)=σ(d)σ(n/d).
- **Prime support:** P(n) is the set of primes dividing n, with P(1)=∅.
  Prescribing these identities is different from bounding their number.
- **Return:** reaching the same residue or abundance class is weaker than
  reaching the same factorization-guarded class, and neither implies net gain.

The recurring distinction is

```text
for every finite duration/gain, there exists a suitable seed
```

versus

```text
there exists one seed whose certified mechanism works forever.
```

Only the former is obtained by the finite growth and recovery constructions.

## 2. Complete result map

Each row links to its proof and its full hypotheses; the short description is
not a replacement for those hypotheses.

| Source / result | Established finding | Boundary that remains |
| --- | --- | --- |
| [01, Propositions 1–2](README.md) | Every multiple of 6 above 6 grows. For C6={n≡6 mod12}, square/prime-exponent conditions classify one-step exits exactly. | Growth does not preserve C6. |
| [01, Proposition 3](README.md) | For every d>1, the class of all multiples of d is not forward-invariant under s. | Restricted subsets, unions, and multistep returns are not excluded. |
| [02, A](TWO-ADIC.md) | Exact 2-adic transition, including cancellation when current exponent equals divisor-sum supply; the cancellation jump is unbounded even with the same exponent pair. | Current supply does not determine future supply. The underlying valuation formula is classical. |
| [02, B–C](TWO-ADIC.md) | s is not 2-adically continuous at 18. No nonempty eventually fixed-binary-residue-defined subset of C6 is forward-invariant. | Not a prohibition on all p-adic, factorization-aware, or return-map methods. |
| [02, D](TWO-ADIC.md) | s(6u)=6T(u) for gcd(u,6)=1, where T(u)=2σ(u)−u. T grows on u>1; perpetual odd-cofactor avoidance of 3 would certify escape. | Perpetual avoidance is unproved; hitting 3 invalidates the reduction, not necessarily the actual driver. |
| [03, coupled laws](REGENERATION.md) | Exact 2–3 supply and cancellation accounting. Strict surplus preserves the current exponents for one step. | Surplus is not an inexhaustible resource. |
| [03, E–F](REGENERATION.md) | A unitary supplying factor certifies a two-step first return. Dirichlet progressions give infinitely many entries and arbitrary prescribed finite amplification. | The returned residue class does not inherit the supplying-factor guard. |
| [04, G](FOUR-ADIC.md) | A square-sensitive mod-4 phase propagates under successful two-step returns. | It does not guarantee those returns. Base four is not an independent valuation. |
| [04, H](FOUR-ADIC.md) | An if-and-only-if criterion restores the exact even-perfect core after its odd prime exponent spikes. | The core-plus-good-spike class is not closed. |
| [04, I](FOUR-ADIC.md) | Arbitrarily fine 4-/3-adic tags of u and σ(u), valuations, and prime-cofactor type cannot decide the two-step guard. | Richer arithmetic information is not excluded. |
| [04, J](FOUR-ADIC.md) | No infinite prime-cofactor orbit over finitely many multiperfect cores, allowing arbitrary switching. | Composite cofactors, general non-multiperfect cores, and infinitely many cores remain possible. |
| [05, K](GLOBAL.md) | For every fixed finite prime set, only finitely many adjacent aliquot pairs use it alone. Every escaping orbit must have P⁺(n_k n_(k+1))→∞. | Classical S-unit finiteness is imported. Changing prime support is not controlled. |
| [06, L](BLOCK-TRANSPORT.md) | Exact composite correction identities; literal +2 block renewal is prime-rigid; independent updates face a divisor-sum budget obstruction. | Regrouping or nonzero corrections are not excluded. |
| [06, M](BLOCK-TRANSPORT.md) | Conditional retained-prime transport can replace suppliers by composite output blocks, including a prime square. | The prime bridge and input factorization template do not regenerate. |
| [06, N](BLOCK-TRANSPORT.md) | A semiprime bridge retaining a supplier of the stated type requires a quadratic residue of 2; the supplying prime must be 17 or 23 modulo 24. | Necessary for that bridge only; no guarantee of exponent, unitarity, or repetition. |
| [07, O](RECOVERY.md) | Every fixed deficient D>1 admits arbitrarily large prescribed two-step rebounds for infinitely many prime cofactors. | Different finite gains may use different seeds; no repeated recovery is proved. |
| [07, recovery refinements](RECOVERY.md) | Recovery can land in a proper multiple of perfect 28, guaranteeing another growing step. An enlarged composite input class has exact corrected transport. | The perfect-core endpoint is outside its entry class; the composite class also fails renewal. |
| [07, P](RECOVERY.md) | An eventually periodic schedule of arbitrary fixed cores with coprime prime cofactors cannot escape, even through deficient steps. | Aperiodic switching and composite cofactors remain. Periodic aliquot cycles are allowed. |
| [07, Q](RECOVERY.md) | An escaping finite-core prime itinerary needs an expansive cycle in its recurrent transition graph. | The graph cycle need not occur consecutively, be repeatable, or be sufficient for escape. |
| [07, supporting constraints](RECOVERY.md) | A least escaping seed is abundant and has no smaller abundant predecessor. Large primes must be sufficiently numerous to overcome a fixed deficiency margin in the small-prime part. | Neither universal predecessor coverage nor the required deficiency margin is established along every orbit. |

The [composite-renewal follow-up](COMPOSITE-RENEWAL.md) adds:

| Result | Established finding | Boundary that remains |
| --- | --- | --- |
| Composite-input handoff | Any fixed supplying factor admits infinitely many prime-parameter inputs with one fresh unitary supplier in the output. | The parameter cannot be selected again on the already fixed orbit. |
| Full prime-entry return | An exact growing two-step block restores the original prime-input shape and `800`-supply. A fixed supplier's affine return consumes an integer divisibility budget. | The displayed next cofactor loses the guard; changing suppliers and composite remainders are not ruled out. |
| Composite phase exchange | The block `3^3*7^3` transforms into `189` times an actual divisor-sum expression; `160*189` is quadruple-perfect. | The output must still be coprime to the new core; ordinary divisibility does not ensure it. |
| Finite unitary-core theorem | Every nonempty finite union of whole unitary-core classes (cores greater than one) has an actual one-step exit, even with arbitrary composite remainders. The stated `160`-supplier version also excludes finite reduced residue refinements. | Not a theorem that every orbit exits; additional arithmetic guards and variable-time returns remain. |
| Non-strict retention and finite menus | Equal-valuation retention works for prime active blocks but can fail on supplied composites. A finite complement-local menu guarantees a unitary block for every active prime only if it contains an inherited stable block. | Does not exclude selection depending on the realized active block or unbounded fresh supplier choices. |

The [exponent-vector follow-up](EXPONENT-VECTORS.md) adds:

| Track | Established finding | Boundary that remains |
| --- | --- | --- |
| Geometry | Abundant vectors are integer points in a convex superlevel region; the extra successor-exponent vector is orthogonal to the absolute supply deficit. Exact small paths exclude global positive linear nonincrease and global convex strict stepwise descent. | The growth region is not invariant; piecewise proper return heights are unproved. |
| Combinatorics | Proper divisors form a weighted exponent box; modular convolution and binary geometric sums compute exact residues without expanding the source. | Prime identities and cancellation matter; residue/shape projections are not autonomous. |
| Lehmer/control patterns | Default prefixes of 126,130,206,162,160 steps extend to 348,130,231,167,189 under a larger budget. The latter certify 276's 28-driver loss at edge 169 and 966's at edge 172. | All frontiers are factorization-limited, not divergent. Permanent 28-driver retention is false for those two seeds; terminating controls exhibit long growth too. |
| Computational scale | A Lucas-certified Pollard--Brent engine extends this repository's old prefixes; symbolic trillion-exponent modular calculations avoid enormous expanded integers. | Sparse factoring is slightly more work in the paired Lehmer aggregate; encoding alone does not remove factorization complexity. |

The [supplier-renewal follow-up](SUPPLIER-RENEWAL.md) adds:

| Result | Established finding | Boundary that remains |
| --- | --- | --- |
| 09, R | For M>2, the universal implication R≡−1 mod M ⇒ M divides σ(R) holds exactly when M divides 24. The proof imports Dirichlet for necessity. | This classifies one residue template, not all possible modular/factorization guards; 7-supply is not automatic. |
| 09, S | If u is odd, u≡−1 mod7, 7 divides σ(u), and 13 exactly divides T(u), then 28u has a two-step first return to that clean-28 residue phase with gain >15/13. | 1987→1989→4563 under T retains supplier 13 but changes its exponent 1→2, losing 7-supply. The returned guard is not invariant. |
| 09, bounded return tests | Supply columns and complete first-return blocks retain losses and censoring. At index 171 in the 276 trace, the first A7 return loses value after 56 steps; no profitable checkpoint exists within 64. | That source actually recovers above its checkpoint after 142 steps. Neither a universal recovery bound nor universal recovery is established. |

The [parity-aware handoff follow-up](PARITY-HANDOFF.md) adds:

| Result | Established finding | Boundary that remains |
| --- | --- | --- |
| 10, T | For a fixed coprime core and one prime parameter, CRT/Dirichlet force specified valuations at finitely many primes not dividing the affine coefficients. | This controls one image, not its divisor sums or subsequent images; excluded core-overlapping primes and composite corrections matter. |
| 10, U | A fresh unitary41 can replace13 when cancellation changes its exponent1→2; the guarded two-step residue return has gain >126645/90077. | At the displayed parameter77141, the endpoint loses both13 and7-supply. |
| 10, V | A fresh181 supplies both7 and13. With the explicit tail condition13∤σ(R), the two-step return restores the old13 exponent to1 and gains >41565/30589. Composite cofactors are allowed. | The restored supplier does not restore the entire guard; the next middle cofactor can be a prime supplying no7. Infinitely many entries to this stronger tail-guarded class are not asserted. |
| 10, W | In any reduced prime-parameter refinement fixing finitely many first-image exponents, a fresh unitary supplier can force all those exponents to remain unchanged at the next image. | This rules out a finite congruence-only guarantee of the old13 restoration, not factorization-aware guards or a different supplier/return phase. |

The [backward-coverage feasibility pass](BACKWARD-COVERAGE.md) adds:

| Result | Established finding | Boundary that remains |
| --- | --- | --- |
| 11, X | Adapting Luca–Pomerance's smooth-stratified collision estimate to bounded-abundancy sources gives positive lower density of abundant N=s(Cp)>Cp with abundant C≤√N and coprime prime p. | This is an adaptation of existing analytic machinery, not a novelty claim; no exceptional least seed is forced into the covered set. |
| 11, bounded census | Through target1000000, the square-root-core family covers58896 of247545 abundant targets; all smaller predecessors cover104107. Representations and distinct sources are checked separately. | Every Lehmer-five seed has no smaller direct predecessor. The same is true of terminating/cyclic controls; uncovered is not escape. No larger-predecessor or multistep exclusion is inferred. |

The [ancestry-barrier follow-up](ANCESTRY-BARRIER.md) adds:

| Result | Established finding | Boundary that remains |
| --- | --- | --- |
| 12, root accounting | Boundary outflow and image collisions force at least floor(X/12)−floor(X/16) abundant targets through X to have no smaller direct predecessor. | The multiples of12 used in counting are unused sources, not identified root targets. Larger predecessors remain allowed. |
| 12, Y | For every fixed ancestry depth h, newly excluded direct roots number at most the sum of fixed-prefix growth exceptions at depths2…h, hence o(X). Fixed forward checks still leave at least X/48−o(X) survivors. | Intermediates are unrestricted, but the theorem does not cover general forward coalescence. An unbounded-depth diagonal corollary assigns each seed only finitely many tests. |
| 12, Z | Proposition X gives positive density of abundant least-preimage sources with no smaller shared successor, even after fixed forward growth tests. | This is an immediate corollary, not a new collision theorem; later or asynchronous mergers remain possible. No intersection with the ancestry-root class is proved. |

The [boundary-outflow follow-up](BOUNDARY-OUTFLOW.md) adds:

| Result | Established finding | Boundary that remains |
| --- | --- | --- |
| 13, excursion accounting | Immediate exits that return or repeat outside by step h are among the e_h(B) growth exceptions. For fixed h, the fraction of exits still open tends to 1 as B grows. | A direct corollary of the valid Erdős theorem, not uniform-in-time control; universal eventual termination/cycling is still compatible. |
| 13, fixed-scale first passage | For each fixed enlargement factor, all but o(B) immediate exit starts reach the higher fence before returning or cycling in the band. | A deduction from small-prime persistence and Davenport continuity, with no effective rate. The inherited, merger-weighted cohort is not a fresh population at the next fence. |
| 13, incoming sources | Removing target1 makes all-source inflow finite, with source ceiling (B−1)². Distinct semiprime sources give at least P(P−1)/2−B incoming edges, where P counts primes through floor((B−1)/2). | The prime number theorem makes this exceed every linear bound eventually, but these incoming sources need not be on outgoing paths. |
| 13, labelled balance | Outward minus inward crossings equals currently-outside starting labels. Actual seeds126 and174 share one return edge at fence174. | Unique-edge counts lose merger multiplicity; remaining outside one fence may mean a cycle. No fixed finite cohort is proved to reach arbitrarily high fences. |

The [minimum-seed contradiction attempt](MINIMUM-ESCAPE.md) adds:

| Result | Established finding | Boundary that remains |
| --- | --- | --- |
| 14, prime-deleted companion | For abundant n, s(n/p) divides s(n) exactly when p occurs once and n/p is perfect. The additive companion error can change sign and has unbounded normalized second-step amplification even above the fixed terminating core 12. | Excludes literal divisor transport and the tested uniform error bound, not every seed-dependent comparison. |
| 14, fixed-core prime lifting | For any D>1, finite length L and gain G>1, infinitely many prime p make the actual orbit from Dp grow by a factor >G on the L steps after its first image. The suppliers can use fresh primes above any cutoff. | Uses Lenstra's finite-chain mechanism, Euler products, CRT and Dirichlet. Different lengths/gains may require different primes; no one seed or infinite budget is obtained. |
| 14, prime-checkpoint budget | The actual block 6*683 → 6*685 → 6*971 preserves the clean 6-core and raises v₃(p+1) from 2 to 5 between prime checkpoints. | Rejects that monotone checkpoint rank; it is not an escaping orbit. Prime checkpoints need not recur in an arbitrary orbit. |
| 14, unbounded reset | For arbitrary K,L, root lifting, CRT, and Dirichlet give infinitely many growing clean-6 edges q² → q²+2q+2 at the cofactor level. The tag v₃(u+1) rises from 0 to at least L, and actual supply v₃(σ(u)) from 1 to at least K. | Different resets may use different seeds. The output cofactor is not asserted prime; no infinite reset sequence, other-rank obstruction, or novelty is established. |

The [maximum-based contradiction attempt](MAXIMUM-CONTRADICTION.md) adds:

| Result | Established finding | Boundary that remains |
| --- | --- | --- |
| 15, peak exclusions | An orbit maximum cannot be abundant; the existing recovery inequality also excludes 4q with prime q≡51 mod160 despite its initial decrease. | A different deficient or prime peak remains possible; the recovery input class does not regenerate. |
| 15, interval obstruction | Every interval {0,…,B} with B≥24 has an outgoing aliquot edge, yet the complete closure of seeds1…24 is {0,…,24,36,55}. | Repeatedly filling gaps adds new seeds. Divergence of this enclosure algorithm does not imply escape of any original seed. |
| 15, divisor repair failure | Exact terminating orbits have H(30)=259>172=H(60), although30 divides60. | One-step divisor inequalities cannot order whole-orbit maxima. No closed larger-return class or unbounded fixed cohort is proved. |

The [return-closure follow-up](RETURN-CLOSURE.md) adds:

| Result | Established finding | Boundary that remains |
| --- | --- | --- |
| 16, full entry guard | The deficient 4u recovery class requires gcd(u,105)=1 and v₂(σ(u))=2, restricting odd-exponent prime factors. The path7700684→5775520→7869524 renews the full class once. | The next recovery endpoint11148600 loses the required valuation. One renewal is not closure. |
| 16, finite supplier relay | In every reduced refinement of p≡51 mod160, infinitely many prime entries4p retain exact bridge exponents v₂≥5 and v₅≥1 for any prescribed finite number of successors. | CRT/Dirichlet constructs different seeds as the horizon changes. This excludes a uniformly bounded return to the deficient class from those congruences, not all return mechanisms. |
| 16, fresh handoff | CRT/Dirichlet force infinitely many prime q with a fresh unitary r in s(160q), preserving the full guard of the larger abundant-core class for one transition. | The output cofactor is necessarily composite; a checked example loses the guard at the next checkpoint despite returning to the same residue phase. |
| 16, attempted repairs | The strict prime-square relay cannot cycle over a finite supplier set. Replacing160 by12 still guarantees recovery, but a clean prime bridge never renews the specified deficient class;1612 is a terminating counterexample to its larger-return property. | Actual generation of fresh suppliers, richer factorization guards, other phases, and unbounded return times remain uncontrolled. |

The [composite-handoff follow-up](COMPOSITE-HANDOFF.md) adds:

| Result | Established finding | Boundary that remains |
| --- | --- | --- |
| 17, composite continuation | The exact residual correction permits two successive fresh suppliers on one checked orbit, with three consecutive members of the full 160-core guard. | The fourth term loses that guard. This is one finite path, not a repeatability theorem. |
| 17, neutral supplier budget | CRT/Dirichlet and neutral powers force a fresh unitary R, but any fresh handoff with R dividing s(v) has R<r/6. | Even hypothetical power-guard renewal could not make these neutral handoffs perpetual. Other handoffs are not excluded. |
| 17, prime-tagged powered residuals | Adding a prime tag makes s(v)≡1 modR² and permits any target supplier R≡−1 mod800 outside a finite exclusion set, including arbitrarily large R>r. | No prime predecessor is asserted. An infinite subfamily exits with exact 3-exponent5, outside every universal tagged-power format; the 3-divisible example is a different phase from clean prime-q entries. |
| 17, finite-menu obstruction | In every reduced refinement of the prime-q first-handoff progression, infinitely many prime entries block all fresh second-handoff candidates from a prescribed finite set, while retaining the old supplier and Z guard. | Other fresh primes, distributed prime-power supply, and factorization-dependent refinements are not excluded. |
| 17, prime-bridge budget | A fixed period of m prime-semiprime-prime blocks consumes 4m units of a positive integer's 2-adic valuation per repetition. | This specializes note07's periodic-core obstruction; aperiodic suppliers and more general composite guards remain open. |

## 3. The strongest statements, with their quantifiers

### Global prime-support constraint

[Proposition K](GLOBAL.md) gives, for every finite set S of primes,

```text
#{n>1 : P(n) ∪ P(s(n)) ⊆ S} < infinity.
```

Its proof extracts fixed/growing prime exponents and expands the divisor-sum
identity. A minimal vanishing subsum containing a fixed nonzero constant
handles degeneracy before applying classical S-unit finiteness.

Distinctness of an escaping orbit then gives

```text
P⁺(n_k n_(k+1)) → infinity,
|union_k P(n_k)| = countably infinite.
```

This is not termwise P⁺(n_k)→∞, a new prime at every step, occurrence of every
prime, or an effective bound on the orbit. Without nonperiodicity, finitely
many admissible source values can recur at infinitely many indices, as at 6.
After K, bounding each orbit's prime support would be equivalent to bounding
its values; calling that the next lemma does not make it easier.

### Finite amplification and deficient recovery

The [note 03](REGENERATION.md) construction stays in a clean 6-core for two
steps and returns to n≡30 mod36 with any requested finite gain. The sufficient
unitary-factor guard is not inherited.

[Proposition O](RECOVERY.md) adds genuine deficiency:

```text
for every deficient D>1 and every G>0,
infinitely many primes p coprime to D give n=Dp with
s(n)<n,  s²(n)>s(n),  and s²(n)>Gn.
```

Here s² means composition. Write a=s(D), b=σ(D), so s(Dp)=ap+b. Force
ap+b to be divisible by a highly abundant K through one reduced prime
progression, then use s(m)/m≥s(K)/K for K|m. This inequality does not need a
unitary factor. Dirichlet's theorem and Euler-product divergence are the
classical inputs; neither successive primality nor a prime-tuples hypothesis
is assumed.

The stronger perfect-core refinement gives infinitely many blocks

```text
2p → Cv → 28T(dv),       C=28d,
```

with a deficient first step, recovery above any requested multiple of 2p,
and an abundant recovered term. Exact example:

```text
12932914 → 6466460 → 13854820 → 19397084.
```

The recovered value has v₂=2; the entry 2p has v₂=1. It is not a return to the
same entry family. Likewise a multiple of 28 is not itself a perfect number;
this construction does not answer the perfect-successor question in section 5.

### What the template obstructions collectively exclude

The three prime-cofactor restrictions are distinct:

| Core hypothesis | Itinerary hypothesis | Conclusion |
| --- | --- | --- |
| Finitely many multiperfect cores | Arbitrary switching | No infinite orbit of those coprime prime-cofactor shapes (J). |
| Arbitrary fixed cores | Eventually periodic core schedule | Any infinite such tail is periodic, with period dividing the schedule length (P). |
| Finitely many arbitrary cores | Every recurrent-graph cycle has slope product ≤1 | No escaping prime-cofactor itinerary (Q). |

For P, composing the prime-cofactor steps yields x' = Ax+C. A nonintegral
expanding slope consumes a finite denominator budget; an integral slope
forces a later multiple of an earlier cofactor prime. A contracting schedule
can instead describe a true cycle, such as 220↔284.

For Q, nonexpansive cycles allow rational weights making upward jumps bounded.
The weighted prime values lie in a finite union of scaled-prime sets, which
has arbitrarily long CRT-constructed gaps. A bounded upward jump cannot cross
such a gap. This proof relies on **prime cofactors** and does not apply to
arbitrary composites.

## 4. Successful mechanisms and the exact failures to remember

| Tempting inference | Exact correction or counterexample |
| --- | --- |
| The same valuation pair determines the next supply. | 30, 78, 438 all start with (a,b)=(1,3), but their successors have supplies 5, 1, 0. |
| A large initial reserve guarantees persistence. | 72198→112122→130848 drops the tested supply from 12 to 1; it refutes thresholds 2 through 12, not every threshold. |
| A valid cofactor identity can be iterated after overlap. | 30→42→54, but s(54)=66 whereas 6T(9)=102; gcd(9,6) is no longer 1. |
| A certified return reproduces its guard. | 53→55→89 under T succeeds, but 89→91→133 fails the next two-step return. |
| Any eventual return to an abundant class is profitable. | 500394 returns to 344226 after 27 steps, with ratio 57371/83399<1. |
| Several profitable returns imply survival. | The seed 318 has several profitable returns and nevertheless terminates. |
| Exact core restoration always repeats. | 11508→19404→42840 loses the exact 28-core exponent through cancellation, although the last step grows. |
| Prime block-shift algebra extends unchanged to composites. | 263→265→383→385 under T is valid, but T(385)=767, not the formal shifted product 511. |
| Replacing suppliers regenerates the original factorization. | 29274→43302→55770 replaces the cofactor 7·17·41 by 13²·5·11, not three distinct primes. |
| A profitable deficient rebound means divergence. | 844→640→890 eventually reaches 0. |
| Keeping deficiency and the 4u shape is enough. | 2764→2080→3212→3004: 3212 is still deficient with v₂=2, but loses the required divisibility by 160 at its successor. |
| Large primes themselves force decline. | s(6p)=6p+12 for every prime p>3. |
| Primitive divisors of σ(n) enter s(n). | If q|σ(n) and q∤n, then q∤s(n), because s(n)≡−n modulo q. |
| Retaining the supplying prime preserves its supply. | 1989=3²·13·17 maps under T to 4563=3³·13²: cancellation at 13 changes σ(13)=14 to σ(13²)=183 and destroys its 7-supply. |
| Detailed small-prime supply columns determine future supply. | 860 and 1340 have identical tested supply-block states and no target-prime ties; their successors 988 and 1516 have different 2-surplus status. |

The retained-prime handoff has a real positive conclusion: under its guards,
composite output blocks replace supplying primes. The [exact formula and
quadratic filter](BLOCK-TRANSPORT.md) are now incorporated, not merely linked
to an external branch. But subsequent factorization remains uncontrolled.

A bounded continuation of its witness makes the issue concrete. Starting at
n₀=29274 and checking exactly 34 transitions, all sources below 10⁹:

- The first source outside the clean coprime-6 representation is
  n₂₃=2079918=2·3⁴·37·347, followed by 2720394.
- The first deficient source is
  n₃₂=101368952=2³·19·666901, followed by n₃₃=98701648.
- The next source is abundant: n₃₃→n₃₄=100848080. But n₃₄<n₃₂: abundance
  has returned without fully compensating that loss.

These are exact finite facts, not a conclusion about the remaining orbit.
The source cap and 34-step boundary are regression limits, not divergence tests.

## 5. Side investigation: entry into a perfect number remains unsettled here

The precise question was whether

```text
n < s(n)=P,         s(P)=P.
```

An aspiring sequence can contain an upward step, as 608→652→496 and
790→650→652→496 show. Their **final** entries into 496 are downward; they do
not answer the displayed question. Also 95→25→6 enters 6 from above.

The perfect-multiple argument proves only

```text
s(n)=P and n≠P  =>  P does not divide n:
```

a proper multiple of perfect P is abundant and has successor larger than
itself, hence larger than P. This does not imply n>P.

The following earlier bounded checks have been rerun and retained in
[`tests/test_synthesis.py`](../tests/test_synthesis.py):

| Perfect target P | All direct predecessors n≤100000 found | Any n<P? | Basin inside 1…1000000, including P |
| ---: | --- | --- | ---: |
| 6 | 6, 25 | No | 5329 |
| 28 | 28 | No | 1 |
| 496 | 496, 652 | No | 13 |
| 8128 | 8128, 10682, 10828 | No | 696 |

Since these four targets are below 100000, the direct test exhausts their
**smaller direct predecessors**. It does not exhaust larger predecessors, all
perfect targets, or paths that leave the million-bound and later return.
The bounded basins contain no seed below their respective target.

A second restricted search considered n=cp with **abundant c≤200000**,
p prime, gcd(c,p)=1, using

```text
p = [P−σ(c)]/s(c).
```

The eight even-perfect targets have Mersenne exponents
2,3,5,7,13,17,19,31. No witness was found. The first six targets yielded no
positive coprime integer candidate p>1; each of the last two yielded one,
proved composite (divisible by 7 and 11 respectively). No factorization check
was unresolved. This does not cover arbitrary abundant predecessors: the
restriction on c matters.

No universal direction-of-entry theorem or counterexample has been established
by this work. Failure to locate one does not certify that the question is a
known open problem. Odd perfect numbers have not been assumed nonexistent;
these computations concern only the specified even targets. The search is
not an ingredient of any proof in the result map.

## 6. How the two approaches now fit together

### Contradiction / descent

A least escaping seed N must be abundant, and its orbit never falls below N.
Its later terms need not grow at each step. It has infinitely many abundant
sources; infinitely many deficient runs has not been proved.

The supporting constraints now written in [note 07](RECOVERY.md) add:

1. N cannot have the form s(C)p+σ(C) for abundant C and prime p coprime to C,
   because Cp would be a smaller escaping predecessor. The positive-density
   covering argument in note11 is not universal and does not give a contradiction.
2. If the small-prime part d has σ(d)/d≤2−ε, then abundance of n=dr, with
   t distinct remaining primes all exceeding B, requires
   `(2−ε)(1+1/B)^t>2`. The fixed deficiency margin is essential and is not
   supplied by prime-support escape.

An earlier narrower target was to exclude **all** finite-core coprime-prime
tails. J, P, and Q settle restricted cases; aperiodic switching with expansive
cycles remains. Even a proof of that narrower target would leave unbounded
cores and more general composite factorizations outside it. Supplier-circuit
expansion is now parked. The subsequent backward feasibility pass clears the
distinct-image density gate using established machinery, but stops at the
missing least-seed coverage implication rather than enlarging the census.
Note12 subsequently proves that any fixed-depth ancestry/forward extension
still leaves positive-density candidates. This is a scoped limitation, not a
ban on all finite certificates or on arithmetic coalescence arguments.
Note13 makes the related boundary obstruction explicit: even fixed-scale
first-passage success for almost all exits does not control the inherited
cohort across infinitely many fences. All-source inflow is not returning
traffic, and merging requires retained seed labels. No new same-seed mechanism
is supplied by this accounting.

A complete proof still needs an orbit-wise bound, a well-founded decreasing
quantity, or another contradiction that covers arbitrary actual trajectories.
Neither a statistical tendency nor an isolated deficient step supplies one.

### Counterexample / repeatable recovery

The growth obligation is comparatively well understood. For a counterexample
by this checkpoint approach, it suffices to give an explicit seed in a
present-arithmetic class X, prove a finite positive return R(n) for **every**
n∈X, and prove R(n)∈X and R(n)>n. Temporary decreases, changing cores, and
variable return times are allowed. This is a sufficient certificate, not a
necessary form for every conceivable resolution.

Every proper multiple of a perfect number is abundant, so a deficient term
has no perfect divisor. Switching perfect cores alone cannot describe it.
For changing cores, compare the whole values, not just their cofactors:

```text
n_end/n_start = (D_end/D_start)(u_end/u_start)
              = product of all step multipliers.
```

Arithmetic-average multipliers can mislead: 1/2 and 8/5 average above 1,
but their product is 4/5. For a hypothetical escaping orbit the accumulated
product tends to infinity, but no positive limiting mean logarithmic growth
or growth in every fixed-size window follows.

The two exact composite corrections expose the current missing step:

```text
T²(vw)=T(v)T(w)+2[s(T(vw))−s(v)s(w)]      (coprime v,w>1),

w+4429=(327/320)(u+4429)+(763/320)δ(u)+(189/2)δ(v)
         in the guarded 4→160→4 block, δ(x)=s(x)−1.
```

We need factorization information on these corrected outputs that forces
fresh unitary suppliers or the next recovery congruence. Positive size
corrections alone do not do so. A profitable graph cycle alone is also
insufficient: actual transitions, all necessary exits, and finite returns
must be controlled. Defining X by demanding successful future iterations
would simply restate the missing theorem.

## 7. Attribution, verification, and what counts as advancement

### Known inputs and related work

- The valuation formulas and guide/driver framework are classical; see
  Amdeberhan–Moll–Sharma–Villamizar and Guy–Selfridge in [notes 01](README.md)
  and [03](REGENERATION.md). The author is **D. Villamizar**.
- Lenstra's arbitrary-length finite increasing prefixes, reproduced by Erdős
  (1976), already prevent treating long finite survival as a breakthrough.
  Erdős's valid fixed-depth almost-all abundant-growth theorem supplies note12.
  His general decreasing/upper-control claim must not be imported; Pomerance's
  2020 lecture records its withdrawal. Note12 uses only the proved small-prime
  persistence argument and the classical continuous abundancy distribution.
- Euler-product divergence and Dirichlet's progression theorem supply the
  finite amplification families; they are imported, not computationally proved.
- Classical S-unit finiteness supplies K. Evertse (1984) already provides
  sufficient qualitative machinery; Evertse–Schlickewei–Schmidt (2002) gives
  a stronger theorem. Nondegeneracy is handled explicitly in our application.
- Pollack (2012), corrected manuscript and 2013 erratum, explicitly states
  related fixed-support amicable-pair/cycle finiteness. Those consequences are
  not new here. The exact earlier publication of K remains unlocated, not
  ruled out. The [literature audit](LITERATURE.md) records this distinction,
  different hypotheses in related work, and unchecked leads such as Luca's
  exact theorem.
- Luca–Pomerance (2015) already prove positive-density even aliquot values and
  state a fixed-progression extension. Note11 adapts their collision proof,
  explicitly replacing its deficiency bounds; the later squarefreeness lemma
  and normal-order inputs are essential. The census does not prove these
  analytic estimates or establish novelty.
- The Erdős 193 Gaussian-walk proof motivated exact valuation bookkeeping,
  not a transferable aliquot contradiction. Its all-pairs identity is absent
  here; its separate Lean build was not rerun by this project.

### Reproducible evidence, not proof premises

Python 3.11+ exact integers and proven factorizations are authoritative.
The original engine uses trial division; notebook 08 adds bounded Pollard--Brent
with complete n-1 Lucas primality certificates. Passing a Miller--Rabin screen
alone never certifies a prime. Additive divisor sieves, divisor-pair/divisor-box
enumeration, and separate certificate replay provide independent checks. Factorization budget failure remains unresolved; it is
never replaced by a probable-prime assumption. Persisted report integers and
rational components are exact decimal strings.

| Evidence | Scope / reproduction |
| --- | --- |
| [Driver-six report](results/driver-six-100000.json) | 8333 C6 sources through 100000; one transition each. `python3 -m aliquot scan-six --bound 100000`. |
| [Two-adic report](results/two-adic-100000.json) | 50000 even sources and at most two steps from each of 8333 C6 sources. `python3 -m aliquot scan-two-adic --bound 100000`. |
| [Regeneration report](results/regeneration-examples.json) | Named certificates and traces, at most 64 transitions and a 1000000 source cap. `python3 -m aliquot regeneration`. |
| [Core-return report](results/core-returns.json) | Named phases, restorations, and traces under the same stated source/step caps. `python3 -m aliquot core-returns`. |
| [Factor-transport tests](../tests/test_block_transport.py) | Bounded identity checks, prime-parameter cases, and independently checked named handoffs. |
| [Recovery tests](../tests/test_recovery.py) | Exact rebounds, failed closure, affine obstructions, composite corrections, and CRT-gap illustrations. |
| [Synthesis tests](../tests/test_synthesis.py) | Supporting constraints, the 34-step handoff continuation, and the previously discussed bounded perfect-target searches. |
| [Exponent-vector reports](EXPONENT-VECTORS.md#5-reproduction-and-prioritized-next-work) | Census through 10000; five Lehmer seeds and six controls, default 256-step and extended 512-step caps; separate work budgets. Both artifacts have full prime/edge certificates and deterministic reproduction tests. |

The [supplier-renewal report](results/supplier-renewal.json) replays the extended
vector artifact before deriving 1296 unique-source diagnostics, first returns
within 64 edges, and separate 8/32/64-edge recovery tests. Its small census covers
sources and guarded-family cofactors through 100000, with independent divisor
sums. Reproduce with `python3 -m aliquot renewal --compact`; reconstruct every
field with `python3 -m aliquot verify-renewal research/results/supplier-renewal.json`.

The [parity-handoff report](results/supplier-handoff.json) has independently
checked named replacement/round-trip blocks and all 21 necessary congruence
candidates with prime parameter at most1000000. Three are admitted prime
parameters; none renews the full41 guard. Named controls are separate from
that bounded cohort. An extra CRT construction illustrates the saturation
obstruction without claiming its least residue is prime. Reproduce with
`python3 -m aliquot handoff --compact`.

The [backward-coverage report](results/backward-coverage.json) instead fixes a
**target** cap1000000, exhausts all smaller sources, and independently verifies
the core/prime representation sets. It records exact moments, distinct targets,
duplicate-source representations, nested coverage gaps, and unresolved-orbit
controls without continuing those orbits. Reproduce with
`python3 -m aliquot backward --compact`.

The [ancestry regressions](../tests/test_ancestry.py) check exact root accounting,
all depth1–4 paths from seeds1–1000 (including excursions beyond1000), the
minimum-path charging inequalities, named mergers, and abstract countermodels.
They have a separate100000 encountered-source cap, no new report/CLI, and do
not computationally prove any density statement.

In the forward experiments, source caps apply to **sources**, not already known successors. Crossing a cap
is unresolved continuation, not divergence. The census frequencies are not
orbit survival probabilities. A read-only AI consolidation audit checked this
summary and the supporting constraints against the notes; its two scope/wording
clarifications were incorporated. It did not run tests. AI critiques do not
replace human mathematical review, and software tests do not verify the
universal proofs.

The advancements are therefore within this investigation: sharper exact
conditions, constructive finite recovery, explicit failed shortcuts, and
scoped necessary constraints on escape. **A major advance toward resolving
the full conjecture has not been established.** The proof sources, attribution
limits, and two missing whole-orbit obligations are now collected in one PR,
without equating CI success with deployment. A separate presentation change now
adds the dedicated website timeline; source notes and computation reports remain
outside the served directory.

## 8. Hilbert/base-four follow-up

The separate [Hilbert proof attempt](HILBERT.md) reads the actual same-terminal
Hilbert pair law and applies it to integer values along aliquot orbits. It
supplies an exact coordinate diagnostic, not a new dynamical constraint.
The proposed squared-radius rank fails even on same-state returns. The family
18(1+4^j), j>=3, shares state I and arbitrarily long low suffixes with 18, but
has even successors while s(18)=21 is odd. Thus orientation does not repair a
fixed-suffix transition rule. A small [figure](results/hilbert-base4.svg) and
[tests](../tests/test_hilbert.py) record the attempt without increasing the
orbit census. A factor-aware descent/closure theorem remains missing; the
attempt stops there. No solution or historical novelty is claimed.

The [Lehmer-five/driver clarification](HILBERT-DRIVERS.md) replays only
existing certified prefixes and records the published loss of 276's initial
28-driver at index 170. That continuation remains attributed external data,
not a locally certified extension. Drivers need not be perfect; a coprime
multiperfect-core formula does not preserve its own hypotheses. The same
factor-aware loss/recovery closure obligation remains.
