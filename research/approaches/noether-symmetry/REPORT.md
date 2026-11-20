# Noether symmetry: an exact affine charge, and its arithmetic failure

## 1. Verdict

**Unresolved. No candidate proof or disproof of the Catalan–Dickson conjecture is obtained.**

This attempt derives a genuine, elementary discrete variational symmetry for a
restricted affine aliquot branch, then follows its arithmetic consequence rather
than treating the analogy as a theorem about all aliquot sequences. The first
consequence—denominator depletion for periodically repeated prime-cofactor
branches—is already in this repository. The substantial further attempt was to
extend that resource to composite cofactors and turn it into a decreasing height.

The strongest additional scoped result is a counterexample family to that
extension:

> For every integer `K >= 1`, infinitely many actual transitions
> `84u -> 84v`, with both `gcd(u,84)=gcd(v,84)=1`, satisfy
> `v_3(u+4)=0` and `v_3(v+4)=K`.

The input can have exactly two distinct prime factors, `u=5q`. The proof uses
CRT and the classical Dirichlet theorem, not a prime-tuples conjecture. Thus the
prime-branch divisibility resource is arbitrarily replenishable **without losing
the chosen coprime core in that step**. Together with one prime-branch edge, this
excludes every nonincreasing height

```text
E(u) = a log(u+4) + b v_3(u+4),      a>0, b real,
```

on all guarded 84-core edges. A second scoped result excludes closure of any
unbounded finite union of prime-core arithmetic-progression families with cores
at least two. Neither result excludes an exceptional infinite orbit, establishes
a whole-orbit bound, or constructs indefinitely repeatable escape.

“Proved” below means a written mathematical argument is supplied. These arguments
have not received independent mathematical review or formal verification. No
historical novelty is claimed.

## 2. Mathematical bridge and hypotheses

### 2.1 What Noether's theorem actually asks for

Noether's first theorem concerns an invariant variational problem under a
continuous group, with suitable differentiability; on the Euler–Lagrange
equations the associated divergence vanishes. In one independent variable this
gives a first integral. Sections 1–2 of Noether's original paper, in Tavel's
translation [N], were consulted, including the differentiability assumption,
Theorem I, and the passage to the variational equations.

The aliquot map on positive integers comes with neither a specified
differentiable action nor a continuous symmetry. With the usual discrete topology,
a continuous action of a connected group on the integers is trivial: the orbit
map of any integer has connected image in a discrete space and hence constant
image. This observation does **not** prohibit embeddings, discrete symmetries,
or variational formulations with additional variables.

There is a stronger obstruction to the most literal conserved-energy strategy.

**Proposition 1 (no globally coercive first integral on the original states).**
Suppose `I(s(n))=I(n)` for every `n>1`. Then the fiber of `I(1)` is infinite.
In particular `I` cannot have all finite fibers, or, if real-valued, all finite
sublevel sets.

**Proof.** For every prime `p`, `s(p)=1`, so `I(p)=I(1)`. There are infinitely
many primes. This proves both conclusions. No value of `s(0)` is used. ∎

Consequently a globally conserved scalar whose level set alone bounds *every*
trajectory cannot be the answer. This does not rule out a Lyapunov function,
conditional invariants on a restricted domain, or a conserved quantity with an
additional orbit label. An arbitrary label or freely adjustable extra variable,
however, supplies no bound on the integer state.

### 2.2 The exact arithmetic branch

For positive coprime integers `c,u`, multiplicativity gives

```text
s(cu) = s(c)u + sigma(c)s(u).                         (1)
```

If `u=p` is prime, `s(p)=1`, so the cofactor evolution with prescribed next core
`d` is exactly

```text
p' = [s(c)/d] p + sigma(c)/d.                         (2)
```

Primality, integrality of `p'`, and coprimality with `d` remain separate guards.
The formula cannot be iterated after those hypotheses fail.

For the concrete core

```text
84 = 2^2 * 3 * 7,   sigma(84)=224,   s(84)=140,
```

preserving a coprime 84-core with prime input gives

```text
p' = (5p+8)/3,          y=p+4,          y'=(5/3)y.     (3)
```

This is an exact affine branch, not an asymptotic approximation.

### 2.3 A genuine discrete variational model, with an auxiliary variable

Let `r=5/3`, let `y_0,...,y_N` and `lambda_0,...,lambda_(N-1)` be real variables,
and define the finite discrete action

```text
A_N = sum_(i=0)^(N-1) lambda_i (y_(i+1) - r y_i).     (4)
```

Take variations of all multipliers and of the interior `y_i`, with the endpoints
of `y` fixed for deriving the equations. Stationarity gives

```text
y_(i+1)=r y_i,
lambda_(i-1)=r lambda_i        (1 <= i <= N-1).       (5)
```

The smooth one-parameter transformations

```text
y_i -> exp(epsilon) y_i,
lambda_i -> exp(-epsilon) lambda_i
```

leave every summand of (4) invariant, even off the equations of motion. The
associated discrete current can be verified directly:

```text
Q_i = lambda_(i-1) y_i,
Q_(i+1) = lambda_i r y_i = lambda_(i-1)y_i = Q_i.     (6)
```

Thus there really is an action, a continuous symmetry of that action, stationary
paths, and a conserved current. This direct derivation avoids assuming a regular
Legendre transform or an invertible symplectic realization: (4) is a degenerate
constraint action, and no such stronger claim is needed.

The limitations are equally concrete:

* The transformations generally do not preserve integer or prime cofactors.
* `lambda` is auxiliary and freely normalizable. Along a growing `y`, it shrinks
  reciprocally. A fixed `Q` does not bound `y`.
* The action represents the prime branch only while its arithmetic guards hold,
  not the unrestricted aliquot map.

**The productive departure from the original analogy** is to discard the
auxiliary momentum and use rational dilation against integrality. From (3), `j`
successful affine steps with integer endpoints require

```text
3^j | (p_0+4),         j <= v_3(p_0+4).              (7)
```

This is an arithmetic obstruction, not a conserved physical energy. It is the
most useful implication of the real symmetry in this attempt.

## 3. Results, proofs, and comparison with existing work

### 3.1 The initial route is already established in the repository

The derivation of (1)–(7) and the proposed periodic-core obstruction preceded
reading `research/SYNTHESIS.md`. The subsequent comparison found:

* `research/FOUR-ADIC.md`, section 5, already gives exactly the 84-core branch,
  the shifted variable `p+4`, and its denominator budget.
* `research/RECOVERY.md`, Proposition P, already excludes escape under an
  eventually periodic schedule of arbitrary fixed cores and coprime prime
  cofactors. It explicitly permits true aliquot cycles.
* Proposition Q there treats arbitrary finite-core switching when all recurrent
  graph cycles are nonexpansive. A nonabundant-core restriction would therefore
  not be an additional general obstruction.
* `FOUR-ADIC.md`, Proposition J, already handles arbitrary switching among
  finitely many multiperfect cores.
* `research/BLOCK-TRANSPORT.md` and `RECOVERY.md` already use the exact defect
  `delta(u)=s(u)-1` and emphasize failure of the next factorization guard.

For completeness, here is the short complete periodic-core argument used in
this attempt; it is **a rederivation of Proposition P, not an addition**.

**Proposition 2 (existing periodic-core obstruction).** Fix cores
`c_0,...,c_(L-1)>1`. If an infinite positive aliquot tail has
`n_(jL+i)=c_i p_(jL+i)` with prime cofactors coprime to their respective cores
at every source, it is periodic with period dividing `L`.

**Proof.** At each phase,

```text
n' = r_i n + b_i,    r_i=s(c_i)/c_i>0,    b_i=sigma(c_i)>0.
```

Composing one period and dividing checkpoint values by `c_0` gives primes
`x_j` satisfying `x_(j+1)=A x_j+B`, with positive rational `A,B` and
`A=product_i r_i`.

If `A<1`, this recurrence converges to `B/(1-A)`. A convergent integer sequence
is eventually constant. Since the affine map is injective, it was constant
from the first checkpoint. The actual deterministic orbit therefore repeats
after `L` steps.

If `A>1`, write `A=a/b` in lowest terms and `B/(A-1)=u/v` in lowest terms,
with all four integers positive. The positive integers `y_j=v x_j+u` obey
`y_j=(a/b)^j y_0`. If `b>1`, integrality requires `b^j|y_0` for every `j`, an
impossibility. Thus any remaining infinite case has integral `A>=1`.
Integrality of two adjacent `x_j` then makes `B` an integer too. These checkpoint
primes strictly increase. Choose one, `P`, not dividing `A`. Modulo `P`,
`z -> Az+B` is a permutation, so its orbit of zero returns to zero after some
`1<=h<=P`. The corresponding later checkpoint is divisible by `P` and strictly
larger than `P`, contradicting primality. ∎

A core equal to one would give a prime term, followed by `1,0`, so excluding it
does not discard an escaping case. The cycle exception is real:
`220=20*11 <-> 284=4*71` has checkpoint coefficients
`A=33/40, B=77/40` and fixed prime `11`.

This proof leaves aperiodic switching, unbounded cores, and composite cofactors.
An expansive graph cycle is not a repeatable arithmetic itinerary. Those are
precisely the limits already recorded in the synthesis.

### 3.2 Composite cofactors give an exact forced balance, not the same charge

For `u>1`, put `delta(u)=s(u)-1>=0`; it vanishes exactly when `u` is prime.
From (1), if an actual edge has the guarded form `84u -> 84v`, then

```text
v = (5u+8s(u))/3,
v+4 = (5/3)(u+4) + (8/3)delta(u).                   (8)
```

The equality is a rational identity at every coprime source; interpreting it
as a *next guarded state* additionally requires an integer `v` coprime to 84.
This correction is elementary multiplicativity, in the same style as the
repository's existing composite-correction identities.

If one continues the auxiliary adjoint equation in (5), the old current has
the balance law

```text
Q_(i+1)-Q_i = (8/3) lambda_i delta(u_i).              (9)
```

Thus the extra arithmetic term explicitly breaks the conservation law. Its
positivity when `lambda_i>0` does not make the 3-adic valuation monotone.
Valuations of sums depend on cancellation, not on their real signs.

### 3.3 Arbitrarily large actual replenishment of the denominator resource

**Proposition 3 (guarded replenishment).** For every `K>=1`, there are infinitely
many primes `q` for which, with

```text
u=5q,       v=11q+16,
```

all of the following hold:

```text
s(84u)=84v,
gcd(u,84)=gcd(v,84)=1,
v_3(u+4)=0,       v_3(v+4)=K,
v>u,             5 does not divide v.
```

**Proof.** Prescribe

```text
q = 1                             (mod 70),
11q+20 = 3^K                      (mod 3^(K+1)).    (10)
```

Since 11 is invertible modulo `3^(K+1)`, the second congruence has a unique
solution for `q`. Modulo 3 it is `q=2`. The two moduli are coprime; the first
residue is a unit modulo 70 and the second a unit modulo `3^(K+1)`.
CRT therefore produces a reduced residue class modulo `70*3^(K+1)`.
**Dirichlet's theorem** supplies infinitely many prime `q` in it. Discard
finitely many small primes if necessary. In particular `q` is odd, is neither
3 nor 5 nor 7, and is distinct from 5.

We have `sigma(5q)=6(q+1)`, hence `s(5q)=q+6`. Substitution into (8) gives

```text
v = [25q+8(q+6)]/3 = 11q+16.
```

The input is coprime to 84. The output is odd, is `2 mod 3`, and is `6 mod 7`
(the last because `q=1 mod 7`), so it too is coprime to 84. Also

```text
u+4 = 5q+4 = 2 (mod 3),
v+4 = 11q+20 = 3^K (mod 3^(K+1)).
```

These give the exact valuations. Finally `v-u=6q+16>0`, while `q=1 mod 5`
gives `v=2 mod 5`. ∎

This proves much more than a formally adjustable error term: all numbers in
the construction are realized by a true aliquot edge and the output core
remains unitary. On the other hand, the quantifiers are

```text
for each K, infinitely many one-step seeds,
```

not one seed with infinitely many replenishments. The special supplying factor
5 is **always lost** in this construction. This is an explicit failure of the
most immediate attempt to repeat the replenishment.

The exact quantified replenishment statement was not found in the consulted
repository notes. Its ingredients are classical, and the closely related
finite recovery constructions in `RECOVERY.md` already use CRT/Dirichlet.
It is an additional local application in this report, not an asserted new
result in the literature.

### 3.4 No linear combination of size and this valuation gives descent

**Corollary 4.** There are no real constants `a>0,b` such that

```text
E(u)=a log(u+4)+b v_3(u+4)
```

is nonincreasing on **every** edge `84u -> 84v` with `u,v>1` and both cofactors
coprime to 84.

**Proof.** The actual guarded prime edge `23 -> 41` in cofactor coordinates
has `(41+4)/(23+4)=5/3` and changes the valuation from 3 to 2. Nonincrease
there would require

```text
a log(5/3)-b <= 0,       hence b >= a log(5/3)>0.
```

But on any edge from Proposition 3,

```text
E(v)-E(u) = a log((v+4)/(u+4)) + b K > 0,
```

since both terms are positive. Contradiction. ∎

This is a universal impossibility statement for the stated height family,
not a test of a few fitted coefficients. It does not exclude nonlinear heights,
additional factorization information, or decreases only after suitable returns.

### 3.5 Finite congruence information cannot close a prime-core family

The next repair attempted was to replace a single affine branch by finitely
many prime-core branches with arithmetic-progression guards.

**Proposition 5 (forced factor complexity in any reduced prime progression).**
Fix `c>=2`, a reduced residue `r mod M`, a bound `B>=c`, and an integer `R>=1`.
There are distinct primes `ell_1,...,ell_R>B` and infinitely many primes
`p=r mod M`, coprime to `c`, such that

```text
v_(ell_i)(s(cp))=1       for every i.
```

**Proof.** Put `a=s(c)>0` and `b=sigma(c)>0`. Choose distinct primes
`ell_i>B` dividing none of `abM`; only finitely many primes are forbidden.
For each one impose

```text
ap+b = ell_i              (mod ell_i^2),
p = r                     (mod M).                 (11)
```

The local residue for `p` exists because `a` is a unit modulo `ell_i^2`.
It is nonzero modulo `ell_i` because `b` is a unit there. CRT again gives a
reduced progression. Dirichlet yields infinitely many primes in it. Remove
the finitely many dividing `c`. Formula (2) now gives `s(cp)=ap+b`, and (11)
gives every exact exponent one. ∎

**Consequence.** Let `X`, up to finitely many exceptions, be a finite union of
classes

```text
{ cp : p prime, gcd(c,p)=1, p in specified arithmetic progressions },
```

with a finite collection of cores `c>=2`. If `X` is unbounded, it is not
forward-invariant under `s`.

Indeed, at least one progression contributing an unbounded family is reduced
(a nonreduced progression contains at most finitely many primes). Apply
Proposition 5 with `B` at least every permitted core and `R=2` to that family.
Neither forced prime can divide any permitted core, and a single prime
cofactor cannot contain both. Thus the successor lies outside every class.
Take the source sufficiently large to put the successor outside the finite
exception set too. ∎

This closes a precise failed *class construction*, not the finite-core orbit
problem. A hypothetical exceptional path could avoid these forced-exit primes
forever while belonging to the same broad classes. No density argument here
forces it to meet a bad source. Variable-length return classes and general
composite cofactors are also outside this consequence. The restriction `c>=2`
matters: primes followed by `1,0` give an elementary terminating class when
core one is allowed.

The method is the same classical CRT/Dirichlet forcing already used in the
repository's local-ambiguity and recovery propositions. The displayed
finite-union conclusion is a scoped extension, with no historical novelty claim.

## 4. Failed routes actually pursued

| Proposal | What was attempted | Decisive failure or revision |
| --- | --- | --- |
| A conserved energy on positive integers | Seek a finite-level-set first integral that bounds orbits | Proposition 1: all primes share the value at 1. A proper global first integral cannot exist, independently of the conjecture. |
| Transfer Noether directly | Construct an action and check its symmetry, rather than citing Noether by analogy | The constrained real affine lift has a genuine current, but its symmetry does not preserve the arithmetic state space and its auxiliary multiplier defeats coercivity. |
| Spend a finite denominator budget | Shift affine core returns to rational dilation and use integrality | Correct for prime cofactors and repeating schedules; already Proposition P and the 84 example in the repository. |
| Use size plus the denominator budget for arbitrary cofactors | Compute the exact source term and attempt a nonincreasing logarithmic/valuation height | Proposition 3 replenishes the budget by arbitrary K on actual guarded edges. Corollary 4 rules out every coefficient choice in the proposed height family. |
| Turn replenishment into a divergence construction | Retain the coprime 84-core and try to reuse the supplier 5 | The output is always `2 mod 5`, so it is not another `5q` input. No replacement supplier is proved. Output primality is not asserted. |
| Close a finite congruence-tagged union of prime branches | Allow multiple cores and progression guards | Proposition 5 forces two new prime factors larger than every core, within any unbounded input progression. This invalidates one-step closure, not exceptional paths. |

The named branch supplies a small exact warning against invalid continuation:

```text
1932 = 84*23 -> 3444 = 84*41 -> 5964 = 84*71
             -> 10164 = 84*121 -> 19628 = 28*701.
```

The first three cofactor inputs are prime. At 121, the prime formula would give
`613/3`, while the actual next integer is 19628, not divisible by 84. It is
not legitimate to round the formula or keep iterating it. This example and its
interpretation are already in `FOUR-ADIC.md`.

One might instead claim that a finite set of cores forces a periodic core word.
It does not: repetition of a symbol or graph cycle is weaker than eventual
periodicity of an infinite word. The integer cofactor retains unbounded state.
Neither Proposition 2 nor the finite-class nonclosure consequence resolves
aperiodic switching. This failed step was not used in any proof.

## 5. Exact remaining obligation

### 5.1 What would close even the selected 84-core route?

Define the guarded map on integer cofactors by

```text
F(u) = (8 sigma(u)-3u)/3 = (5u+8s(u))/3,
U = {u>1 : gcd(u,84)=1}.
```

An edge in this restricted dynamical system is admitted only if `F(u)` is an
integer in `U`. It then is exactly the actual aliquot edge `84u -> 84F(u)`.

A narrow unresolved question is:

> Must every starting `u in U` eventually fail that integer/coprimality guard?

This is **not** being offered as a renamed proof of the full conjecture. Proving
it would only exclude permanent residence in this particular core class; other
cores, core overlaps and other factorizations remain. An explicit seed with a
rigorous infinite-guard argument would, however, disprove the conjecture:
`F(u)>(5/3)u`, so its actual aliquot trajectory would escape. Neither direction
of this restricted question has been established here.

The exact accounting behind the attempted proof is, for `y_j=u_j+4`,

```text
3^k y_k = 5^k y_0
          + 8 sum_(j=0)^(k-1) 5^(k-1-j) 3^j delta(u_j).      (12)
```

This follows by induction from (8). Prime-only branches have zero sum and the
finite budget (7). Composite branches supply actual, not freely chosen, values
`delta(u_j)=s(u_j)-1`. A closing argument would have to constrain those values
together with the next factorization and coprimality conditions. Their
nonnegativity cannot control 3-adic cancellation; Proposition 3 proves
arbitrarily large cancellation of exactly the kind a depletion proof must
prevent. On the construction side, it would have to prove that the replacement
factorization supplies another guarded refill or other growing return. The
lost factor 5 shows that the family given here does not do that.

There is also a useful exact necessary formulation, not an extra theorem that
solves the issue. If an infinite guarded path existed, division of (12) by
`5^k` and passage to the 3-adic limit would give

```text
y_0 + (8/5) sum_(j>=0) (3/5)^j delta(u_j) = 0 in Z_3.       (13)
```

The series converges 3-adically because each `delta(u_j)` is an integer; the
left term `(3/5)^k y_k` tends to zero 3-adically for the same reason. The terms
are nonnegative in the real ordering, which says nothing contradictory about
their 3-adic sum. No theorem proved here excludes (13) for the **realized**
defects. Choosing formal defects to satisfy it would not realize an aliquot
orbit.

### 5.2 What remains for the full conjecture

A proof still requires an orbit-wise bound or another argument covering every
actual escaping candidate, including aperiodic/composite behavior and changing
cores. A disproof still requires one explicit seed with an infinite argument.
No established result in this report forces arbitrary trajectories into the
restricted domain above. Infinitely many one-step examples do not bridge that
gap. Cycles remain allowed throughout: a repeated positive integer gives an
eventually periodic orbit, and nothing here purports to eliminate them.

## 6. Evidence and reproducibility

### 6.1 Declared limits, before running the witness search

The standalone script is `research/approaches/noether-symmetry/verify.py`.
It uses only the standard library and the existing authoritative `aliquot`
API. It uses no probable-prime tests and no new runtime dependencies.

* Replenishment levels: **1 through 6 inclusive**.
* For each of those six progressions, and one forced-exit progression:
  at most **256 candidates**, indices **0 through 255 inclusive**, stopping
  at the first proven prime within the limits.
* Inclusive source cap: **10,000,000,000**. A candidate above the cap is not
  used as a source. This is a resource limit, not a divergence test.
* Trial factorization budget: **2,000,000 work units per call**, with the
  definition inherited from `aliquot.factorize`.
* **One** actual edge per new witness; **four** edges of the named 84-core branch.
  No hard orbit is extended.
* Every reported source sum is independently recomputed by enumerating divisor
  pairs for **1 <= d <= floor(sqrt(source))**.
* Candidate or edge factorization failures are retained as unresolved statuses,
  not converted to primality, compositeness, or divergence.
* Mathematical integers and rational components in `evidence.json` are decimal
  strings; small counts, exponents and work limits are integers.

### 6.2 Finite results—not premises of the universal propositions

| K | Proven prime q | Actual source 420q | Actual successor 84(11q+16) | Charge change |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 491 | 206220 | 455028 | 0 -> 1 |
| 2 | 701 | 294420 | 649068 | 0 -> 2 |
| 3 | 10781 | 4528020 | 9962988 | 0 -> 3 |
| 4 | 18341 | 7703220 | 16948428 | 0 -> 4 |
| 5 | 75041 | 31517220 | 69339228 | 0 -> 5 |
| 6 | 347201 | 145824420 | 320815068 | 0 -> 6 |

For the finite-class obstruction, take core 20, input residue `p=11 mod 12`,
and force primes 23 and 29 to exponent one in `22p+42`. The script proves
`p=13762391` prime and checks

```text
275247820 -> 302772644,
v_23(302772644)=v_29(302772644)=1.
```

Thus the successor cannot be `c*p'` for **any** `1<=c<=20` and prime `p'`.
This is one exact example of Proposition 5, not a census of finite-core paths.

One script run checks **11 edges**, tests **14 progression candidates**, and
makes **40,455 divisor-pair loop iterations** in the independent edge checks.
The maximum checked source is **275247820**. There are **zero unresolved
candidate factorizations** and **zero unresolved requested edge checks**.
These counts do not resolve the future fate of any new witness: those
continuations were deliberately not attempted.

### 6.3 Commands actually run

From the assigned repository root, using Python **3.12.3** and Node **v22.22.0**:

```sh
python3 research/approaches/noether-symmetry/verify.py \
  > research/approaches/noether-symmetry/evidence.json

python3 -m unittest discover -s tests -p test_noether_symmetry.py -v
# PASS: 9 tests.

python3 research/approaches/noether-symmetry/verify.py \
  > /tmp/noether-symmetry-evidence.json
cmp research/approaches/noether-symmetry/evidence.json \
  /tmp/noether-symmetry-evidence.json
# PASS: byte-for-byte reproduction.

node --check site/explorer.js
node --check site/math.js
node --check site/latex.js
# PASS: all three syntax checks. No site files were edited.
```

The focused tests additionally build an additive proper-divisor sieve through
**168000 inclusive** and check (8) for every coprime `u` in **2 through 2000
inclusive**, one source at a time. They check the real/rational variational
identities separately from arithmetic trajectories, exact named prime/cofactor
facts, invalid-input behavior, and deliberately exhausted work limits. A
six-step *formal* rational dilation in one test is expressly not asserted to
be an actual prime or aliquot path.

The repository-wide checks were also attempted, concurrently, each with a
**180-second tool timeout**, via these exact shell commands:

```sh
python3 -m unittest discover -s tests -v > /tmp/noether-symmetry-full-tests.log 2>&1; status=$?; tail -n 8 /tmp/noether-symmetry-full-tests.log; exit "$status"
npm test > /tmp/noether-symmetry-npm-test.log 2>&1; status=$?; tail -n 8 /tmp/noether-symmetry-npm-test.log; exit "$status"
```

**Both runs timed out and are incomplete**, not passes. Both logs stopped in
the pre-existing
`test_orbit_lengths.OrbitLengthTests.test_every_edge_has_independently_verified_factors_and_divisors`.
No failure was reported before that point, but this does not certify the tests
that did not complete. The resource limit was not enlarged to pursue unrelated
large divisor enumeration. `npm test` invokes the same Python discovery
command; it is not an independent proof check.

The independent arithmetic algorithms share a Python runtime. They check
finite identities and examples, not Dirichlet's theorem, the universal proofs,
absence of escaping orbits, or historical novelty. No proof-assistant check or
independent researcher review was performed.

## 7. Literature and attribution limits

The source comparison was made **after** the initial affine/symmetry route was
derived. Consulted repository sources were `SYNTHESIS.md`, `LITERATURE.md`,
`README.md`, `GLOBAL.md`, `FOUR-ADIC.md`, `BLOCK-TRANSPORT.md`, `RECOVERY.md`,
and the relevant arithmetic and recovery tests. No other worktrees, branches,
agent sessions, or shared agent memory were consulted; no delegation occurred.

Public sources checked for this attempt:

* **[N] Emmy Noether**, *Invariante Variationsprobleme* (1918), Tavel's English
  translation, *Invariant Variation Problems*.
  [arXiv metadata](https://arxiv.org/abs/physics/0503066),
  [full HTML, version 3](https://arxiv.org/html/physics/0503066v3).
  Sections 1–2 were read for the theorem's actual hypotheses and divergence
  identity. The elementary discrete derivation (4)–(6) is written here rather
  than attributed to a literal application of the differential theorem.
* **Dirichlet's theorem on primes in reduced arithmetic progressions** is the
  sole non-elementary imported existence theorem in the added constructions.
  The [MathWorld statement](https://mathworld.wolfram.com/DirichletsTheorem.html)
  was checked. It requires `gcd(residue,modulus)=1`; this is verified in both
  constructions. The theorem itself is not reproved here.
* [MathWorld, *Catalan's Aliquot Sequence Conjecture*](https://mathworld.wolfram.com/CatalansAliquotSequenceConjecture.html)
  was consulted for the stated termination-or-cycle target and open status.
  This report uses the user's precise convention `s(1)=0`, with `s(0)` undefined.
* [MathWorld, *Cunningham Chain*](https://mathworld.wolfram.com/CunninghamChain.html)
  was consulted as related literature on prime affine recurrences. The familiar
  special recurrence `p -> 2p+1` is not a new Noether-inspired object, nor does
  finite prime-chain evidence imply an infinite aliquot construction. No
  numerical record from that page is used here.

A Marsden–West discrete mechanics PDF was retrieved, but no theorem from it was
used or claimed to have been reviewed; the current above is verified directly.
The attempted MathWorld URL `NoethersTheorem.html` returned 404. A Wikipedia
Noether page was also retrieved, but primary text [N] supplies the relevant
hypothesis check. These retrievals were bounded `curl -L --max-time 25` requests
with maximum file sizes 1.5–2 MB; HTML text was extracted with Python's standard
library. They were literature retrievals, not numerical experiments.

The consulted sources do **not** constitute an exhaustive bibliographic search
for the replenishment or finite-union statements. The guide/driver setting,
composite corrections, affine prime recurrences, CRT and Dirichlet forcing are
all established tools. The discrete action is a general constraint-lifting
construction, not evidence that aliquot dynamics is a new physical system.

## 8. Fruitfulness assessment

**Not useful as a closing mechanism in this attempt.** The bridge produced a
valid symmetry/current and led to a precise arithmetic resource, but its
prime-only obstruction was already present. The strongest additional output
is the arbitrary guarded replenishment theorem and the resulting impossibility
of the proposed size-plus-valuation height. The finite-progression repair also
fails by an explicit theorem.

These are useful diagnostics for avoiding specific false proofs, not evidence
of substantial progress toward bounding all aliquot orbits. No new closed
growing class, orbit-wise bound, or contradiction for arbitrary escape emerged.
The failure of the tested symmetry-based resource is not evidence that the
Catalan–Dickson conjecture is true or false.

**Final mathematical status: the conjecture has not been resolved.**
