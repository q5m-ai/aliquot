# Research note 07: deficient recovery and periodic prime-cofactor templates

**Status:** scoped deductions while pursuing both directions of the
Catalan–Dickson conjecture. A deficient step can have a guaranteed, arbitrarily
large two-step rebound, even into a perfect-core class. Conversely, periodic
prime-cofactor templates cannot escape; nonperiodic finite-core templates need
an expansive transition-graph cycle. None of these results settles the
conjecture, supplies a closed return class, or establishes historical novelty.
The prime-cofactor restrictions are essential to the obstruction proofs.
This note does not depend on the unmerged factor-transport note 06.

Throughout, s(n)=σ(n)−n for positive n. Stop at zero; s(0) is undefined.
A nonterminating, nonperiodic orbit has distinct positive terms and tends to
infinity, without necessarily being monotone. Call such an orbit *escaping*.

## 1. The two approaches, without assuming the desired conclusion

**Contradiction.** If escaping seeds exist, take the least one N. No term in
its orbit can be below N: that smaller term would itself be an escaping seed.
Also s(N)>N, since equality gives a fixed point. This does **not** imply that
all later steps grow. Infinitely many terms must be abundant, because an
eventually strictly decreasing positive-integer tail is impossible; a perfect
term instead traps the orbit. Infinitely many deficient terms is not established.

The fixed-support result in [note 05](GLOBAL.md) forces
P⁺(n_k n_(k+1))→∞, not a descent. In particular large primes coexist with
one-step growth, as s(6p)=6p+12 for every prime p>3. No prime-escape cost that
forces a net loss has been proved here.

**Construction.** It would suffice to give an explicit seed in an arithmetically
defined class X and prove, for every n∈X, a finite positive-time actual return
R(n)∈X with R(n)>n. Return times and percentage gains need not be uniform.
The increasing integer checkpoints then tend to infinity, ruling out a finite
orbit or periodic tail. Intermediate steps can decrease and need not have a
perfect divisor.

This last flexibility matters. Every proper multiple n=Du of a perfect number
D is abundant: the scaled proper divisors ud of n, for d|D and d<D, sum to
u s(D)=n, and divisor 1 is additional when u>1. Therefore a deficient term has
no perfect divisor, even without a coprimality assumption. Perfect cores alone
cannot describe the whole excursion.

The accounting is multiplicative:

```text
∏_(i=0)^(r−1) s(n_i)/n_i = n_r/n_0.
```

A return to abundance is not necessarily a return above the old checkpoint,
and neither is a return to the same factor-defined class.

## 2. A guaranteed loss followed by a more-than-compensating rebound

### Divisibility lemma

If d|m, then σ(m)/m≥σ(d)/d, hence

```text
s(m)/m ≥ s(d)/d.
```

Indeed σ(p^e)/p^e=1+1/p+⋯+1/p^e increases with e, and the prime-power
factors multiply. This statement needs **no** assumption gcd(d,m/d)=1.
It is an inequality, not an unjustified use of multiplicativity on d and m/d.

### Proposition O — unbounded two-step gain starting at a deficient number

Fix **any deficient integer D>1**. For every real G>0, infinitely many primes
p coprime to D give n=Dp satisfying

```text
s(n) < n,           s²(n) > s(n),           s²(n) > G n.
```

Here s²(n) means s(s(n)), not the square of s(n).

**Proof.** Put a=s(D) and b=σ(D), so 0<a<D. Choose an integer K>1 coprime
to ab such that

```text
r = s(K)/K > max(1, GD/a).
```

Such choices exist. Let K run through squarefree products of the primes up to
B excluding the finitely many prime divisors of ab. Then

```text
σ(K)/K = ∏_(q|K)(1+1/q)
       = ∏_(q|K)(1−1/q²) ∏_(q|K)(1−1/q)^(-1) → infinity.
```

The first product has a positive limit; the second diverges by the classical
Euler prime-product theorem. Removing finitely many primes does not change
this conclusion.

Since gcd(a,K)=gcd(b,K)=1, the congruence

```text
ap+b ≡ 0 (mod K)
```

defines a reduced residue class. Dirichlet's theorem supplies infinitely many
primes p in it. Discard the finitely many with p|D or p≤b/(D−a). These two
classical theorems are imported, not proved by the finite tests below.

Put n=Dp. Multiplicativity at the coprime prime cofactor gives

```text
m = s(n) = ap+b < Dp = n.
```

Since K|m, the divisibility lemma gives

```text
s(m) ≥ r m > m,
s²(n)/n ≥ r(ap+b)/(Dp) > ra/D > G.
```

This proves all three assertions, for infinitely many distinct n. ∎

The quantifiers remain finite-block quantifiers: for each fixed deficient D
and requested G there are infinitely many **seeds** with this two-step behavior.
No single seed is shown to repeat it. Even fixing the deficient core does not
bound two-step amplification. This rules out a universal two-step net-decrease
bound for deficient sources, not longer or seed-dependent descent arguments.
The earlier finite amplification results and Lenstra's arbitrary-length
increasing prefixes are relevant benchmarks,
not perpetual-orbit certificates.

### A small, explicit profitable class

Take d=160=2⁵·5. Its divisor sum is 378, so r=218/160=109/80>4/3.
The reduced residue class is q≡51 (mod 160). Thus, for every prime q in that
class, n=4q is deficient and

```text
s²(n)/n > (3/4)(109/80) = 327/320 > 1.
```

The prime q=211 gives

```text
844 = 4·211  →  640 = 2⁷·5  →  890 = 2·5·89.
```

The middle term is abundant, and the rebound exceeds 844. But 890 is not four
times a prime, so it is outside this input class. In fact this particular
orbit terminates:

```text
844 → 640 → 890 → 730 → 602 → 454 → 230 → 202
    → 104 → 106 → 56 → 64 → 63 → 41 → 1 → 0.
```

This failure is immediate and structural, not just the absence of a longer
computation. Defining X={4q:q prime, q≡51 mod160} certifies a profitable
**block**, but s²(X)⊆X is false. No invariant enlargement is proved.

For a literal abundant–deficient–abundant excursion, an additional conditional
identity is useful. If p≡1 (mod5) and both p and q=4p+7 are primes greater than
3, then

```text
12p → 4q → 12p+28.
```

The first term is abundant; the middle one is deficient since q>7; the final
one is a multiple of the abundant number 20. It also exceeds the start.
The example p=31 is 372→524→400. The endpoint is not divisible by 12, so the
same input template cannot simply be reused. Infinitely many simultaneous
prime pairs of this form are **not** asserted. Proposition O, in contrast,
uses only one prime in a fixed reduced progression and proves infinitude.

### Composite recovery inputs, and an exact failed renewal

The input need not be four times a prime. Define the present-factorization class

```text
X₀ = {4u : u>1 odd, σ(u)<8u/7, σ(u)≡92u (mod160)}.
```

For n=4u∈X₀, coprimality of 4 and u gives

```text
m=s(n)=7σ(u)−4u=3u+7s(u)<4u,       160|m.
```

The congruence follows since 7·92≡4 (mod160). The source n is deficient;
the middle term m is abundant because it is divisible by 160. As s(u)≥1,
the divisibility lemma again yields s²(n)>(327/320)n. Thus X₀ includes composite cofactors
and the infinite prime subclass above, without referring to future iterates.

But even retaining the shape and deficiency does not renew the guard:

```text
2764=4·691 → 2080=160·13 → 3212=4·803 → 3004.
σ(803)=888 < 8·803/7,             160 does not divide 3004.
```

The returned checkpoint 3212 is deficient with v₂=2, but is not in X₀.

There is exact accounting for the composite correction. Put
v=(3u+7s(u))/160, and additionally require v>1, gcd(v,160)=1. Then

```text
s(160v)=218v+378s(v).
```

Its 2-adic valuation is 2 exactly when v₂(σ(v))=1: compare the valuations of
378σ(v) and 160v, which are 1+v₂(σ(v)) and 5. Under this guard the output is
4w with w odd, where

```text
w = (109v+189s(v))/2.
```

For δ(x)=s(x)−1, direct substitution gives

```text
w+4429 = (327/320)(u+4429)
         +(763/320)δ(u)+(189/2)δ(v).                 (R)
```

If both u and v are prime, the correction terms vanish. Repeating this
prime-only block j times would require 320^j|(u+4429), since gcd(327,320)=1.
Equivalently j≤min(⌊v₂(u+4429)/6⌋, v₅(u+4429)); there is a finite denominator
budget. This is necessary, not sufficient for the other guards. Composite
corrections can change that budget, but do not imply
σ(w)<8w/7 or σ(w)≡92w (mod160), as the displayed counterexample shows.
No propagation of those conditions or the bridge guards is established.

### Recovery can land in a perfect-core class

For any G>1 choose an odd squarefree d coprime to 42 and put C=28d, with

```text
σ(C)/C = 2 ∏_(q|d)(1+1/q) > 2G+1.
```

The same Euler product supplies such d. Dirichlet supplies infinitely many
primes p≡C−3 (mod C²), a reduced class since gcd(C,3)=1. Put p+3=Cv;
then v≡1 (mod C), so gcd(v,C)=1 and v is odd. For p>3,

```text
n=2p → m=p+3=Cv < n,
s(m)=σ(C)σ(v)−Cv > 2G·Cv > Gn.
```

Here m is abundant. Since d,v are odd and mutually coprime, and both are
coprime to 28, the recovered term r has the exact form

```text
r=28[2σ(d)σ(v)−dv]=28T(dv),       T(x)=2σ(x)−x.
```

The bracket is odd, so v₂(r)=2. Also r>28, hence r is a proper multiple of
perfect 28 and is itself abundant, even if 7 divides T(dv). Thus one further
growing step is guaranteed, not merely one rebound.

For d=5·11·13·17·19, C=6466460 and p=C−3=6466457 is prime. Exact checks give

```text
12932914 → 6466460 → 13854820 → 19397084.
```

The first transition decreases; the next two grow, and the two-step endpoint
exceeds the starting value. This is still not regeneration: every entry 2p
has v₂=1, while every recovered r has v₂=2. No return to the prime-entry family,
or later return to a controlled replacement family, follows.

## 3. A contradiction for periodically repeated prime-cofactor templates

[Proposition J in note 04](FOUR-ADIC.md#proposition-j--no-infinite-prime-cofactor-orbit-over-finitely-many-multiperfect-cores)
excludes arbitrary switching among finitely many **multiperfect** cores with
prime cofactors. The following different restriction allows arbitrary cores,
including deficient cores, but assumes their schedule is eventually periodic.
Neither theorem subsumes the other.

### Proposition P — periodic fixed-core schedules cannot escape

Let D₀,…,D_(L−1) be fixed integers greater than 1. Suppose an infinite positive
aliquot tail has the representations

```text
n_(jL+i) = D_i p_(jL+i),
p_(jL+i) prime,   gcd(D_i,p_(jL+i))=1,
```

for every j≥0 and 0≤i<L. Then this tail cannot escape; in fact it is periodic
with a period dividing L. Allowing a finite prefix before this pattern does
not change the conclusion. A core equal to 1 would give a prime term and
termination instead, so excluding it loses no escaping example.

**Proof.** Put r_i=s(D_i)/D_i>0 and c_i=σ(D_i)>0. At every source the prime
cofactor and coprimality assumptions give the exact affine step

```text
s(D_i p) = s(D_i)p+σ(D_i),
n_(k+1) = r_i n_k+c_i,             k ≡ i (mod L).
```

Composing one whole period gives

```text
n_((j+1)L) = A n_(jL)+B,
A = ∏_i r_i > 0,
B = ∑_(i=0)^(L−1) c_i ∏_(h=i+1)^(L−1) r_h > 0.
```

Thus the prime checkpoint cofactors x_j=n_(jL)/D₀ obey

```text
x_(j+1) = A x_j+C,                C=B/D₀ > 0,       (A)
```

with fixed positive rational A,C.

If A<1, the formula for (A) shows that x_j tends to C/(1−A). A convergent
integer sequence is eventually constant. Since A≠0, (A) is injective, so
constancy extends backwards to x₀. Hence n_L=n₀, and the actual aliquot tail
is periodic with period dividing L.

Suppose A>1. Write A=a/b in lowest terms and write C/(A−1)=u/v in lowest
terms, with positive integers u,v. The positive integers y_j=v x_j+u satisfy

```text
y_j = (a/b)^j y₀.
```

If b>1, integrality requires b^j|y₀ for every j, which is impossible. This
also gives a finite denominator budget: for any prime ℓ|b, a valid j must
satisfy j·v_ℓ(b)≤v_ℓ(y₀). Consequently A must be an integer if this case is
to continue indefinitely.

In the remaining cases A≥1 is an integer. Equation (A) makes C an integer
as well. The checkpoint primes grow strictly. Choose a late checkpoint prime
p=x_j not dividing A; the unbounded growth makes this possible. Modulo p,

```text
F(z)=Az+C
```

is a permutation. Therefore the orbit of 0 returns to 0 at some positive
time h≤p. The corresponding later checkpoint x_(j+h) is a multiple of p
strictly larger than p, contradicting primality. This includes A=1. ∎

The argument does not require individual steps to grow, a uniform gain per
step, or perfect cores. It allows losses inside the proposed repeated block.
It excludes that **specific infinite template**, not changing composite
cofactors, infinitely many cores, or a nonperiodic schedule of finitely many
non-multiperfect cores.

The periodic outcome is real, not an exception to hide: 220=20·11 and
284=4·71 form an amicable pair with the core pattern (20,4). Here
A=33/40, C=77/40, and the fixed checkpoint prime is x=11.

### Proposition Q — a finite-core prime system needs an expansive graph cycle

Suppose an escaping tail has n_k=D_(i_k)p_k, with prime p_k coprime to its
core, drawn from finitely many fixed cores D_i≥2. In any finite directed graph
containing its allowed core transitions, at least one directed cycle must have

```text
∏_(source cores on cycle) s(D_i)/D_i > 1.
```

In particular, this holds for the graph of transitions used infinitely often,
after deleting a finite prefix. A graph cycle need not occur consecutively in
the actual itinerary, let alone repeat forever.

**Proof.** The prime-cofactor edge i→j is

```text
p' = a_(ij)p+b_(ij),
a_(ij)=s(D_i)/D_j>0,       b_(ij)=σ(D_i)/D_j>0.
```

The product of its slopes around a cycle equals the product in the statement.
Suppose all cycles have product at most one. For each vertex i, let w_i be the
largest slope-product of a path starting there, including the empty path.
Removing a cycle cannot decrease that product, so the maximum occurs among
finitely many simple paths. Thus the w_i are positive rationals with
w_j a_(ij)≤w_i on every edge. Scale them to positive integers.

The integers z_k=w_(i_k)p_k lie in a finite union of scaled-prime sets and obey

```text
z_(k+1) ≤ z_k+H,
```

where H is an integer at least max_(edges) w_j b_(ij). That finite union has
arbitrarily long gaps: for any M choose distinct primes ℓ₁,…,ℓ_M dividing none
of the w_i. By CRT choose Z with ℓ_r|Z+r for 1≤r≤M, and choose Z larger than
all w_iℓ_r. If Z+r=w_i p with p prime, then ℓ_r|p forces p=ℓ_r, contradicting
the size bound. Hence no Z+1,…,Z+M belongs to the union.

Choose such a gap above z₀ with M>H. An unbounded sequence z_k cannot cross
it: at the first crossing above Z+M its previous value is at most Z, requiring
an increase greater than H. This contradicts the step bound. Since there are
finitely many fixed positive cores and weights, escape of n_k would make z_k
unbounded. ∎

This deals with nonperiodic switching only when **all** graph cycles are
nonexpansive. It leaves aperiodic switching with expansive cycles unresolved.
It does not assert that the existence of an expansive cycle is sufficient for
escape, nor that composite cofactors lie in a finite union of scaled primes.

## 4. What the two approaches now need

- **For a contradiction:** the least-seed argument and prime-support escape
  still lack a universal descending resource. Propositions P and Q leave
  aperiodic finite-core prime switching with expansive cycles unresolved,
  along with more general composite cofactors. A sharply narrower next target
  is whether **any** finite-core prime tail can escape; even excluding all of
  them would not settle the full conjecture. Neither a large prime nor a
  deficient term supplies universal descent: Proposition O allows any
  prescribed two-step rebound even over a fixed deficient core.
- **For a counterexample:** finite, profitable recovery is now guaranteed in
  explicit infinite families, but the entry conditions are not inherited.
  For the 4→160→4 candidate, the concrete missing step is propagation of
  σ(w)<8w/7, σ(w)≡92w (mod160), and the bridge guards under the composite
  transport (R). The full class fails, and its prime-only version has a finite
  budget. A nonempty refinement or a different closed class must prove finite
  returns and net gain for every allowed continuation. Merely naming a union
  of favorable orbits would hide the original obligation in its definition.

This is a narrowing of two attempted routes, not a claimed major advance or
resolution. Historical novelty has not been checked. The only imported
results used in the new recovery proofs are the classical Euler product and
Dirichlet progression theorems; the template obstructions are elementary.

## 5. Bounded checks, separate from the proofs

`tests/test_recovery.py` checks exact named transitions with trial factorization
and independent divisor-pair sums; finite ranges of the recovery inequalities
and the affine prime-cofactor identity; the terminating and composite-renewal
counterexamples; the perfect-core rebound; and finite illustrations of
denominator depletion, the affine modular trap, the allowed amicable fixed
point, and a scaled-prime CRT gap. The tests state their bounds and use exact
integer/rational arithmetic. They do not prove the universal results,
Dirichlet's theorem, the Euler-product limit, or historical novelty.

Two independent read-only AI analyses agreed on the recovery and periodic-core
arguments. A subsequent cross-audit accepted the general deficient-core
statement, composite correction, graph obstruction, and perfect-core refinement.
The audit clarified that the **source**, not the abundant middle term, is
deficient, and that G>0 requires the max(1,GD/a) choice above. The agents
reviewed an earlier draft and the proposed additions, not the final expanded
test file, and did not run tests. This is neither human mathematical review
nor formal verification.
