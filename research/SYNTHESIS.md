# Research synthesis: findings, limits, and the two routes forward

**Bottom line:** we can force finite growth, transport some supplying factors,
restore some lost core exponents, and guarantee recovery after a deficient step.
We can also exclude several simple invariant and prime-cofactor templates.
**We cannot yet make the recovery conditions reproduce themselves, or force a
general escaping orbit into a contradiction. No solution, divergent seed, or
historical novelty is claimed.**

This is the reading guide for notebooks 01–07 and the literature audit. It
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
| [07, supporting constraints](RECOVERY.md) | A least escaping seed is abundant and has no smaller abundant predecessor. Large primes must be sufficiently numerous to overcome a fixed deficiency margin in the small-prime part. | Neither a predecessor-covering theorem nor the required deficiency margin is established along every orbit. |

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
   because Cp would be a smaller escaping predecessor. No covering theorem
   makes this a contradiction.
2. If the small-prime part d has σ(d)/d≤2−ε, then abundance of n=dr, with
   t distinct remaining primes all exceeding B, requires
   `(2−ε)(1+1/B)^t>2`. The fixed deficiency margin is essential and is not
   supplied by prime-support escape.

The concrete narrower target is to exclude **all** finite-core coprime-prime
tails. J, P, and Q settle restricted cases; aperiodic switching with expansive
cycles remains. Even a proof of that narrower target would leave unbounded
cores and more general composite factorizations outside it.

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
- The Erdős 193 Gaussian-walk proof motivated exact valuation bookkeeping,
  not a transferable aliquot contradiction. Its all-pairs identity is absent
  here; its separate Lean build was not rerun by this project.

### Reproducible evidence, not proof premises

Python 3.11+ exact integers and proven trial factorization are authoritative.
Additive divisor sieves and divisor-pair enumeration provide algorithmically
independent checks. Factorization budget failure remains unresolved; it is
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

Source caps apply to **sources**, not already known successors. Crossing a cap
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
