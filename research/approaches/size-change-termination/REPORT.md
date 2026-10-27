# Size-change termination and aliquot dynamics

## 1. Verdict

**Unresolved. No candidate proof or disproof of the Catalan–Dickson conjecture
is obtained.** There is no certified escaping seed. The mathematical statements
below have written proofs, but have not had independent mathematical review or
proof-assistant verification.

For `n>=1`, let `sigma(n)` be the sum of its positive divisors and let
`s(n)=sigma(n)-n`. Iterate while positive, with `s(1)=0` and `s(0)` undefined.
The target conjecture says that every positive starting integer reaches zero
or eventually enters a positive cycle, including a perfect fixed point.

The strongest positive result of this attempt is a genuine two-coordinate
size-change certificate on a restricted, infinite arithmetic domain:

> **Restricted theorem.** An aliquot orbit that, at every sufficiently late
> positive term, has the form `n = a p`, with `1 <= a <= 17` and `p` prime,
> cannot be infinite and nonperiodic. Coprimality need not be assumed in this
> statement: it follows automatically on a hypothetical escaping tail.

This is not a theorem about all starting integers. In particular it does not
say that an orbit starting with such a factorization keeps it. The cutoff 17
is a proved sufficient cutoff, **not** a claimed optimal one.

Pursuing the first missing core, 18, gives an exact two-branch prime-guarded
return map. An infinite execution of that map would have to satisfy the
additional restriction

```
v_2(p+c) = v_3(p+c) + 2,
c = 13 if p == 2 mod 3, and 17 if p == 1 mod 3,
```

at every checkpoint. A compressed form of its necessary replenishment law is

```
6^t' u' = 7^t u + epsilon,
epsilon alternates between +1 and -1,
t,t' >= 1, gcd(u,6) = gcd(u',6) = 1.
```

The prime guards on all intermediate numbers remain essential. I could
neither rule out an infinite guarded execution nor construct one. This is a
restricted obstruction/necessary condition, not demonstrated progress toward
a complete conjecture resolution.

## 2. What was attempted first, and what was already known here

Before consulting `research/SYNTHESIS.md`, I selected the following concrete
mapping. Factor a state as `n = a p` with a finite choice of cores `a`, and a
prime `p` coprime to `a`. Then

```
s(ap) = s(a)p + sigma(a).                              (1)
```

An edge from core `a` to core `b` is the guarded affine transition

```
p' = [s(a)p + sigma(a)] / b,                           (2)
```

where integrality, primality, and coprimality at the new source must all be
checked. A repeated itinerary gives an affine return on the prime coordinate.
I pursued two prospective termination resources: a denominator valuation,
and a modular return to a previously used prime.

Reading the synthesis and source notes then established that this initial
route was **already substantially present**:

- `research/RECOVERY.md`, Proposition P, excludes escaping eventually periodic
  prime-cofactor schedules over arbitrary fixed cores. Its proof already uses
  denominator depletion and a modular prime obstruction.
- Proposition Q in that note excludes finite-core prime escape when all
  recurrent graph cycles are nonexpansive, using weighted sizes and CRT gaps.
- `research/FOUR-ADIC.md`, Proposition J, handles arbitrary switching among
  finitely many multiperfect cores; its 84-core example already exhibits a
  decreasing shifted valuation.
- `research/GLOBAL.md` proves fixed-prime-support finiteness using an imported
  S-unit theorem and recalls Lenstra's arbitrary finite increasing prefixes.
  Neither result supplies a rank for changing, unbounded factorizations.

The present additions relative to the inspected notes are the explicit
17-core rank, the exact 18-core boundary calculation, and its balanced
2–3-valuation restriction. They are elementary developments of the existing
affine method, not claims of historical novelty. A search of the assigned
checkout did not locate these particular statements. This is not a substitute
for a comprehensive literature search.

For completeness, the initial modular argument can be stated without first
making the affine slope integral. Core 1 cannot occur in an infinite positive
orbit, because a prime goes to 1 and then 0. Write a periodic checkpoint map as
`F(x)=(U x+V)/D`, with positive integers `U,V,D`. If `U/D<1`, an infinite
integer orbit converges and is constant, giving an actual aliquot cycle. If
`U/D>=1`, the checkpoint primes strictly increase. Choose a late checkpoint
prime `ell` not dividing `UD`. Reduction of `F` modulo `ell` is a permutation;
its orbit from zero returns to zero within at most `ell` iterations. The later
checkpoint prime is therefore a multiple of `ell` larger than `ell`, a
contradiction. All intervening rational expressions are integers by the
itinerary hypothesis. This is an alternative proof of the already recorded
periodic-template obstruction, not a new theorem about arbitrary switching.

## 3. Mathematical bridge to size-change termination

### 3.1 The source principle and the soundness obligation

In the standard size-change setting [1,2], there are finitely many control
locations and finitely many parameter positions at each location, with values
in a well-founded ordered set. A sound transition graph records inequalities

```
x_i >= x_j'       (weak edge),
x_i >  x_j'       (strict edge)
```

that hold for **every concrete transition represented by that graph**. Graph
composition follows parameter threads; any strict edge makes the composed
thread strict. If every infinite graph path has a thread with infinitely many
strict edges, there can be no infinite concrete execution. The finite closure
criterion is that every idempotent self-graph in the composition closure have
a strict self-loop. This is a criterion for the abstraction, not a theorem
that arbitrary arithmetic dynamics admit a suitable abstraction.

There are two immediate difficulties for aliquot dynamics:

1. The whole relation has legal infinite executions: perfect fixed points and
   positive cycles. Applying a global strict rank to all positive steps would
   assert a false statement.
2. A chosen finite list of cores need not represent the next factorization.
   An omitted transition is not a terminating orbit. Conversely, an abstract
   infinite path need not be arithmetically realizable.

I therefore use **termination of a restricted relation**, not termination of
the whole aliquot program. States leaving its arithmetic domain are exits of
that analysis, not conclusions about the full orbit. Finite exceptional values
are also exits. A hypothetical escaping orbit eventually avoids every finite
exceptional set; thus a rank on a domain rules out escape only if that orbit
is proved eventually to remain in the domain.

### 3.2 An explicit cycle-compatible analogue

Let `X` be a set of positive integers, and let `rho: X -> N x N` decrease
strictly in lexicographic order on every aliquot edge with both endpoints in
`X`. There is no infinite aliquot tail wholly contained in `X`.

**Proof.** In a strictly decreasing lexicographic sequence, the first natural
coordinate can fall only finitely often. Thereafter it is constant and the
second coordinate would decrease indefinitely in `N`, which is impossible.
No behavior at an exit from `X` has been asserted. QED.

If `X` contains all sufficiently large members of an arithmetic class `A`,
then an orbit eventually in `A` cannot escape. Indeed, a deterministic
infinite nonperiodic orbit has no repeated positive values and eventually
exceeds every fixed bound. It would consequently have a tail in `X`.
Termination at zero and positive cycles are left intact. There is no need to
recognize, enumerate, or assume a bound on all aliquot cycles.

This elementary lemma is enough below; no black-box program analyzer or
unverified transfer of the SCT theorem is used.

## 4. Proved result: an explicit rank for cores at most 17

### 4.1 Domain and uniqueness

Define

```
X_17 = { n > 527 : n = a p, 1 <= a <= 17, p prime }.
```

Since `527=17*31`, every representation in this domain has `p>31>a`.
Consequently `gcd(a,p)=1`, `p` occurs to exponent one, and `p` is the largest
prime factor of `n`. The representation is unique: from `ap=bq` with
`a,b<=17` and `p,q>31`, divisibility forces `p=q` and then `a=b`.

For `n=ap` in `X_17`, set

```
rho(n) = (2, 1)                    if a=6 and p == 2 mod 3,
         (2, 0)                    if a=6 and p == 1 mod 3,
         (1, v_3(p+7))             if a=12,
         (0, n)                    otherwise.             (3)
```

These are nonnegative integer coordinates computable from the current
factorization, not from any future orbit property.

### 4.2 The finite core calculations used in the proof

The exact small-core table is

| a | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| s(a) | 0 | 1 | 1 | 3 | 1 | 6 | 1 | 7 | 4 | 8 | 1 | 16 | 1 | 10 | 9 | 15 | 1 |

These entries follow by listing the divisors of the seventeen integers; the
program checks them by two different arithmetic algorithms. In particular,
all cores other than 6 and 12 are deficient, and for each such core

```
sigma(a)/(a-s(a)) <= 31.                              (4)
```

The largest value is 31 at `a=16`. Therefore `p>31` implies

```
s(ap)-ap = -(a-s(a))p + sigma(a) < 0                  (5)
```

for these cores. The finite exceptional threshold is necessary: a deficient
core alone does not make every prime multiple deficient. For example
`16*31=496` is perfect.

### 4.3 Theorem: every internal edge decreases (3)

**Theorem.** If `n,m` belong to `X_17` and `m=s(n)`, then
`rho(m) < rho(n)` in lexicographic order.

**Proof.** Write `n=ap`, `m=bq`, with `p,q>31` prime.

**Case I: `a` is neither 6 nor 12.** Equation (5) gives `m<n`. It remains to
show that the phase cannot rise from 0.

If `a` is odd, then `n` is odd and `sigma(n)=sigma(a)(p+1)` is even.
Thus `m` is odd, so `b` is odd; neither exceptional even core is possible.
This also covers `a=1`, where `m=1` is actually outside `X_17`.

For the remaining even cores, reduction of (1) modulo 3 gives

| a | 2 | 4 | 8 | 10 | 14 | 16 |
|---|---|---|---|---|---|---|
| s(ap) mod 3 | p | 1 | p | 2p | p | 1 |

None is zero since `p>31` is prime. Hence `b` cannot be 6 or 12. The phase
stays 0 and its second coordinate decreases from `n` to `m`.

**Case II: `a=6`.** Equation (1) is `m=6(p+2)`. Since `p` is odd, `v_2(m)=1`.
Also `3|m`, and `q>31` is neither 2 nor 3. Among cores at most 17 the only
possibility is `b=6`. Thus `q=p+2` is prime. It is greater than 3, so
`p == 2 mod 3` and `q == 1 mod 3`; the second coordinate falls from 1 to 0.
Another internal 6-core step is then impossible. If `p+2` is composite, the
transition simply does not have both endpoints in this domain.

**Case III: `a=12`.** Here

```
m=16p+28=4(4p+7),      v_2(m)=2.
```

Because `q` is odd, the only possible target cores at most 17 are 4 and 12.
For `b=4` the phase falls from 1 to 0, regardless of the increase in `m`.
For `b=12` one has

```
q=(4p+7)/3,
q+7=(4/3)(p+7),
v_3(q+7)=v_3(p+7)-1.                                 (6)
```

Thus the second coordinate strictly decreases. These cases exhaust every
internal edge. QED.

### 4.4 The size-change graphs really close

Use parameter positions `P` (the phase in (3)) and `R` (its second coordinate).
The proved cases have only two types of sound size-change graph:

```
G_same:  P >= P',  R > R'
G_drop:  P > P',   no constraint on R'.
```

Composing only `G_same` gives `G_same`; any composition containing `G_drop`
has the strict `P -> P` thread and gives `G_drop` with these minimal graphs.
Both are idempotent, both have a strict self-loop, and all internal concrete
edges have been accounted for. Equivalently, an infinite graph path either
has infinitely many phase drops or eventually has only strict `R` descent.
This verifies the SCT hypotheses on this domain rather than merely naming a
potential ranking quantity.

### 4.5 Consequences and limitations

The restricted theorem in section 1 follows from section 3.2. Equivalently,
if `P+(n)` denotes the largest prime factor, then every hypothetical escaping
orbit must satisfy

```
n_k / P+(n_k) >= 18 for infinitely many k.             (7)
```

Otherwise an escaping tail would lie in `X_17`. Neither (7) nor the proof
claims that this quotient tends to infinity.

The growing phases also have explicit finite budgets. A 6-core run above the
threshold has at most one internal transition. In a 12-core run with initial
cofactor `p`, (6) permits at most `v_3(p+7)` internal 12-to-12 transitions.
There can be one further growing transition into the deficient phase. If
`t=v_3(p+7)`, every value before that phase begins is at most

```
(4/3)^(t+1) * (n_initial+84) - 84,
```

provided the run stays in the domain; this follows from
`n'+84=(4/3)(n+84)`. After entering phase 0 all internal values decrease.
This is a bound for a **single uninterrupted visit to the domain**, not for
an orbit that leaves and later re-enters it.

Exact examples show why the phase and local rank must differ:

```
606 -> 618 -> 630             ranks (2,1) -> (2,0), then outside X_17;
1212 -> 1644 -> 2220          ranks (1,3) -> (1,2), then outside X_17;
732 -> 1004                  phase 1 -> 0 although the number increases;
592 -> 586                   size decreases in phase 0.
```

The legal cycles `220 <-> 284` and `496 -> 496` are below the cutoff and are
not contradicted. Reaching a value at most 527 is not itself declared
termination or periodicity.

## 5. Pursuing the first obstruction rather than stopping at the rank

### 5.1 Reduction of a hypothetical tail with cores at most 19

Suppose an escaping tail has cores at most 19. Discard a finite prefix so
that all values exceed `19*31=589`; now every cofactor prime exceeds 31 and
each representation is unique and coprime.

The new core 19 is odd and deficient. The previous parity/mod-3 argument
still shows that the deficient phase cannot enter a core divisible by 6.
The 12-core phase still has only targets 4 and 12 and cannot persist forever.
An escaping tail therefore cannot enter either of these two phases.

From core 6 the only remaining targets are 6 and 18. A 6-to-6 step cannot
occur twice consecutively, since the prime would go through `p,p+2,p+4`.
Thus an escaping tail visits core 18 infinitely often.

At a core-18 source the exact formula is

```
s(18p) = 21p+39 = 3(7p+13).                           (8)
```

A successor still having a core at most 19 must have core 6, 12, or 18.
To remain in the only possibly escaping subsystem `{6,18}`, it must have
2-adic exponent 1. This requires `p == 3 mod 4`. The following cases give
**all** returns to core 18 within that subsystem.

- If `p == 2 mod 3`, the successor in (8) is divisible by 18. Its core can
  remain at most 19 in the subsystem only when

  ```
  q=(7p+13)/6 is prime;        18p -> 18q.              (A)
  ```

- If `p == 1 mod 3`, (8) has exactly one factor of 3. It must have core 6,
  with prime `r=(7p+13)/2`. This prime satisfies `r == 1 mod 3`, so the next
  6-core step cannot stay in core 6. The return requires

  ```
  r=(7p+13)/2 prime, q=(7p+17)/6 prime;
  18p -> 6r -> 18q.                                   (B)
  ```

All these integers are greater than 31 when used as cofactors. The original
core-coprimality requirements are consequently satisfied. Conversely, if
these guards hold, multiplicativity proves precisely the displayed actual
aliquot transitions. No assumption about an unspecified factorization is
being substituted for the guards.

Thus an infinite sequence of primes `p_j>31`, all `3 mod 4`, obeying (A)/(B)
and their extra prime guards would give an actual escaping aliquot orbit.
Indeed every indicated term is a proper multiple of 6 and grows; also
`p_(j+1)>(7/6)p_j`. Conversely every escaping tail with cores at most 19
would supply such a sequence. This is equivalence for a restricted class,
not equivalence to the full Catalan–Dickson conjecture.

### 5.2 Attempted descending resources and an exact recharge

Choose `c=13` in branch A and `c=17` in branch B, and write

```
alpha = v_2(p+c),    beta = v_3(p+c).
```

At any checkpoint that can continue, `alpha>=2`, `beta>=1`. Either return
satisfies

```
q+c=(7/6)(p+c).                                      (9)
```

If the branch stays the same, both valuations decrease by one. This is the
natural multi-resource size-change proposal. It fails at a branch change:

```
p=107, c=13:  p+c=120, (alpha,beta)=(3,1);
q=127, c'=17: q+c'=144, (alpha',beta')=(4,2);
1926 -> 2286.                                       (10)
```

Both cofactors really are prime and (10) really is an aliquot transition.
Both proposed counters increase simultaneously. In this witness the next
step is `2286 -> 2706=6*11*41`, outside the bounded-core class. This refutes
the universal weak/strict descent claim, **not** the conjecture, and not the
possibility of a different ranking.

### 5.3 A necessary balanced-valuation law for an infinite guarded run

**Proposition.** Every checkpoint of an infinite execution of (A)/(B) has

```
alpha = beta + 2.                                   (11)
```

**Proof.** If `beta>=2`, equation (9) gives `3|(q+c)`. Since `q>31` is prime,
its residue determines the same branch, so `c'=c`. In this case the two
valuations both decrease by one.

If `beta=1`, equation (9) instead gives `3` not dividing `q+c`. The prime
`q` is not divisible by 3. Its residue must therefore be the other allowable
residue, and `c'` is the other shift. Thus a switch occurs exactly at
`beta=1`, and

```
q+c' = (7/6)(p+c) + (c'-c),     c'-c = +4 or -4.       (12)
```

At such a switch:

- If `alpha=2`, the first summand on the right has 2-adic valuation 1,
  while the correction has valuation 2. Hence `alpha'=1`. As both shifts
  are `1 mod 4`, this makes `q == 1 mod 4`, so the next return is impossible.
- If `alpha>=4`, the first summand has valuation at least 3. Adding or
  subtracting 4 gives `alpha'=2`. At the next return, division by 6 gives
  valuation 1; switching its shift by 4 cannot change that valuation.
  Hence the following prime is `1 mod 4`, again incompatible with an
  infinite run.
- An infinite run must consequently reach every switch with `alpha=3`.

Starting at any checkpoint with `(alpha,beta)`, the next `beta-1` returns
have the same shift and decrease both coordinates by one. At the ensuing
switch they are `(alpha-beta+1,1)`. They must equal `(3,1)`. This is (11).
Every assumed intermediate return exists because the execution was assumed
infinite. QED.

This is stronger than simply observing that a fixed branch consumes its
valuation. It establishes a precise condition on arbitrary switching.
It does not prove that condition cannot keep reproducing itself.

### 5.4 Compressing a whole run between switches

At a checkpoint satisfying (11), put `t=beta`. There is a positive integer
`u`, coprime to 6, with

```
p+c=4*6^t*u,       t>=1.                             (13)
```

If an infinite guarded continuation exists, after exactly `t` returns the
shift switches. Repeated use of (9) gives

```
p_new+c = 4*7^t*u,
p_new+c_new = 4*(7^t*u+epsilon),
epsilon = +1 for 13 -> 17, and -1 for 17 -> 13.       (14)
```

Applying (11) to the new checkpoint now forces

```
v_2(7^t*u+epsilon) = v_3(7^t*u+epsilon) = t' >= 1,
u'=(7^t*u+epsilon)/6^t',       gcd(u',6)=1.            (15)
```

The signs alternate. Equations (13)–(15) are necessary replenishment laws.
They are not sufficient on their own: every checkpoint
`(7/6)^j(p+c)-c` before the switch must be prime, and each branch-B return
also needs its intermediate `(7p_j+13)/2` prime. The next checkpoint must
pass the corresponding conditions again.

This is where the investigation went beyond literal SCT. I tried to find a
resource in (15) that cannot replenish indefinitely. The factors 6 in the
denominator supply descent in two valuations; the `+1`/`-1` at a switch can
supply fresh factors of both 2 and 3. The explicit recharge (10) prevents
claiming those factors are globally consumed. The balance condition restricts
the replenishment but gives no decreasing natural quantity on `u,t`.
Constant or periodic **core schedules** are already excluded by Proposition P;
variable run lengths with all these prime guards are not handled by that
argument.

A concrete attempt at continuing the balanced recharge was also boundedly
tested. The four forms

```
p = 864v+107,   q = 1008v+127,
r = 3528v+451,  z = 1176v+151                       (16)
```

satisfy `18p -> 18q -> 6r -> 18z` if all four are prime and
`gcd(7v+1,6)=1`. Here `p+13=24(36v+5)` and
`q+17=144(7v+1)`, so the first return refills `(3,1)` to `(4,2)` under this
coprimality restriction. The tested range `0<=v<=1000` had no all-prime
quadruple. This finite negative result supplies **no** impossibility proof.

In fact even a fixed finite prime-divisor covering obstruction to all four
forms is unavailable: restrict to `v=6w`. Their coefficients are divisible
by 2 and 3, their constants are not, and each coefficient is coprime to its
constant. For any prime `ell>=5` the four forms exclude at most four residues
of `w`, strictly fewer than `ell`. CRT therefore produces parameters avoiding
any prescribed finite set of prime divisors. This elementary admissibility
calculation asserts neither simultaneous primality nor indefinite
realizability. It explains why simply adding a few modular tags is not a
closure proof for this candidate block.

## 6. Failed routes, revisions, and the exact remaining obligation

### Failed routes actually pursued

1. **Use the ordinary size, or insist on a fixed-window size drop.**
   `s(6p)=6p+12` immediately defeats stepwise size descent. The already-known
   Lenstra construction defeats a uniform bounded window for all seeds.
   Revision: use a phase, a residue counter, and a shifted valuation instead.

2. **Repeat an affine core loop to obtain escape.** Periodic schedules cannot
   escape, as the repository already proves. A single growing loop is not a
   repeatable certificate. Revision: allow genuinely different branches and
   track what their switching does to valuations.

3. **Turn exclusion of repeated loops into exclusion of all finite-control
   paths.** A finite graph may have infinite aperiodic paths. A recurrent
   edge/cycle need not be repeated consecutively. Proposition P cannot be
   applied to an arbitrary itinerary just because its alphabet is finite.
   Revision: prove a sound graph on a restricted domain; the 17-core graph
   really satisfies SCT, while the 18-core branch switching does not supply
   the needed weak inequalities.

4. **Assume the two active valuations cannot refill together.** The exact
   transition (10) refutes it. Revision: analyze the switch cases completely,
   obtaining (11), then the stronger compressed law (15). Neither law closes
   a well-founded descent argument.

5. **Try to reproduce a balanced refill with prime cofactors.** The finite
   family (16) yielded no witness in the specified range, but the elementary
   local admissibility calculation prevents interpreting that as a modular
   impossibility proof. No prime-tuples conjecture is imported as a theorem.
   Even a valid block would leave indefinite regeneration unproved.

### Smallest explicit outstanding statement for this continuation

A sharply narrower next obligation is:

> There is no infinite sequence of primes `p_j>31`, all `3 mod 4`, following
> (A) and (B), with the extra intermediate prime in every B step.

The work above did not merely rename that statement: it proved all the
17-core cases and forced (11)–(15) in the unresolved subsystem. What is still
missing is an argument that a prime-guarded sequence of balanced recharges
cannot continue forever, or an explicit seed for which it provably does.
The failure is not a factorization budget failure. It is the absence of any
proved control on how the corrected outputs in (12)/(15) factor at future
switches.

A proof of this restricted statement would exclude every escaping tail whose
cores are at most 19. It would **not** establish the full conjecture. An
arbitrary escaping orbit could have larger and unbounded cores, repeated
large prime factors, or multiple freely varying prime factors. No theorem in
this attempt forces it into a bounded-core domain. Claiming that every orbit
eventually enters `X_17`, or that all domain exits eventually return with a
smaller rank, would be an additional very strong unproved claim, not a
consequence of SCT. No such global coverage assertion is offered as a lemma.

For a disproof, an infinite prime-guarded run of (A)/(B) would suffice; merely
solving the relaxed integer recurrence (15), or finding a long finite prime
run, would not.

## 7. Evidence and reproducibility

### Scope declared before the searches

The principal scan is one exact transition per coprime pair with core
`1..19` and prime cofactor `2..10000`, inclusive. The boundary check uses at
most two accelerated returns for selected recharge witnesses (each return
contains at most two actual transitions). A separate fixed parameter range
`v=0..1000` tests (16). No hard aliquot orbit was extended. No observed
frequency is interpreted as an orbit probability.

Python 3.12.3 was used. All arithmetic is integer or `fractions.Fraction`.
Every factorization call in the supporting verifier has a 100,000-work-unit
budget using the existing exact trial-division API. A failure is recorded in
`unresolved`, not treated as composite, prime, or divergence; the verifier
exits nonzero if such records exist. The tests explicitly exercise that
behavior with an inadequate budget. The additive sieve has inclusive bound
500,000. The four-form primality checks are independently checked by
proper-divisor-pair enumeration, with values at most 3,528,451. Domain values
in JSON are decimal strings; no floating-point conversion is used.

The standalone program is `verify.py`; its output is `evidence.json` in this
directory. The only added test file is
`tests/test_size_change_termination.py`. No core API or shared research note
was edited.

### Recorded finite results

| Check | Exact scope/result |
|---|---|
| Prime list | 1,229 primes in 2..10,000, sieve and trial-factorization checked |
| Affine identity | 23,327 coprime core/prime pairs, one step each |
| Largest source / successor in that scan | 189,487 / 209,472 |
| Internal 17-core rank comparisons | 8,459; every computed comparison decreases |
| Phase-edge counts | 0->0: 7,914; 1->0: 199; 1->1: 149; 2->2: 197 |
| Guarded core-18 returns | 124, comprising 96 A returns and 28 B returns |
| Largest checked source in those returns | 197,502 |
| Both counters increase | p=107, 7019, 7883; next-return guard fails for all three |
| Four-form scan (16) | 334 eligible parameters, 1,336 independently checked primality decisions, zero all-prime quadruples |
| Named exact aliquot edges | 13, all also checked by divisor pairs |
| Computation-limit unresolved cases | **0** |

The rank and balanced-valuation theorems do not follow from these counts.
Their proofs are the all-integer arguments in sections 4–5. The computations
check formulas, finite examples, guard handling, and implementation mistakes.
Independent arithmetic algorithms share a Python runtime; they are not an
independent mathematical review.

### Commands executed

From the assigned checkout root:

```sh
python3 research/approaches/size-change-termination/verify.py \
  > research/approaches/size-change-termination/evidence.json
python3 -m unittest discover -s tests -p test_size_change_termination.py -v
```

The focused suite passed **12 tests**, including exact reproduction of the
entire saved evidence file. Two exploratory inline Python checks preceded the
saved verifier; their bounds were respectively `p=37..10000` with at most two
returns, and `v=0..1000` for (16). Their computations and outcomes are
reproduced by `verify.py`, rather than leaving an unreproducible search result.

Additional commands executed:

```sh
python3 -m unittest discover -s tests -v
npm test
node --check site/explorer.js
node --check site/math.js
node --check site/latex.js
python3 -m py_compile research/approaches/size-change-termination/verify.py \
  tests/test_size_change_termination.py
git diff --check
```

The direct full-suite invocation reached its 180-second command timeout;
no test failure had been reported, but that invocation was incomplete. A
single bounded rerun via `npm test` (which invokes the same Python discovery
command), with a 360-second timeout, completed: **144 tests passed** in
188.976 seconds. All three JavaScript syntax checks, Python compilation, and
`git diff --check` passed. No site code was changed. These are software
regressions, not independent review of the mathematical proofs.

Only the requested new approach files and the uniquely named test file are
left for integration. No commit, push, PR, hosting, merge, or deployment was
performed.

## 8. Sources, attribution, and literature-check limits

1. C. S. Lee, N. D. Jones, A. M. Ben-Amram, **The size-change principle for
   program termination**, POPL 2001, pp. 81–92,
   <https://doi.org/10.1145/360204.360210>. Crossref metadata and the published
   abstract were checked in this attempt; the parallel SIGPLAN Notices DOI
   is `10.1145/373243.360210`.
2. A. M. Ben-Amram and C. S. Lee, **Ranking Functions for Size-Change
   Termination II**, Logical Methods in Computer Science 5(2:8), 2009,
   <https://arxiv.org/abs/0903.4382>,
   <https://arxiv.org/html/0903.4382v4>,
   DOI `10.2168/LMCS-5(2:8)2009`. The primary text's section 2 definitions,
   infinite descending threads, soundness theorem, composition, idempotent
   closure criterion, and ranking-function definition were consulted.
3. P. Erdős, **On Asymptotic Properties of Aliquot Sequences**, Mathematics of
   Computation 30 (1976), 641–645,
   <https://www.renyi.hu/~p_erdos/1976-22.pdf>. The Lenstra finite-prefix
   argument is recorded and proved in `research/GLOBAL.md`; that repository
   treatment was inspected here. The original PDF was not re-reviewed in
   this attempt. No claim about a new finite-growth construction is made.
4. Assigned-checkout sources inspected after developing the initial mapping:
   `research/SYNTHESIS.md`, `README.md`, `LITERATURE.md`, `GLOBAL.md`,
   `RECOVERY.md`, and `FOUR-ADIC.md` (all under `research/`). These identify
   the existing affine/valuation results, the prime-support theorem, their
   imported inputs, and the guide/driver literature.

The SCT theorem is used only with sound arithmetic graphs explicitly verified
here; the independent lexicographic proof also establishes the needed special
case. The small-core and boundary theorems need no deep imported number theory.
The analogy to rational-affine/Collatz-like switching in (15) is descriptive,
not an imported theorem about that system.

Public retrieval used `curl -L --fail --max-time 30` for the arXiv abstract
and the Crossref title query, and Python's standard-library `urllib.request`
with a 30-second timeout to inspect the arXiv HTML sections. No shared agent
memory, other worktree, other branch, or additional agent was consulted.
This was a focused source check, not an exhaustive bibliographic novelty
review. None of the results here is claimed to be historically new.

## 9. Fruitfulness assessment

**Undetermined for resolving the conjecture in this attempt.** The bridge is
mathematically real on an explicitly delimited domain: it produces a complete
SCT certificate, not just an analogy. The continuation also produces a precise
necessary balanced-valuation condition and an exact counterexample to the
simplest attempted replenishment-free ranking.

Those outputs are useful for auditing this restricted method. They do not
show that the essential unbounded-factorization problem has become easier,
that most or all orbits enter the certified domain, or that the prime-guarded
recharge system is empty. A restricted termination certificate and a sharper
missing condition are not by themselves evidence of a major advance toward
a full proof or disproof.

**Final mathematical status: the Catalan–Dickson conjecture remains unresolved.**
