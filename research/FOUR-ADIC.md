# Research notebook 04: base-four phases and perfect-core restoration

**Status:** an attempt to make regeneration iterable. We obtain an exact
restoration criterion after a prime-power spike, and a conditional invariant
modulo 4. Neither propagates its full factorization guard. We also rule out two
specific finite-state/prime-cofactor shortcuts. **No infinite closure, divergent
orbit, conjecture resolution, or mathematical novelty is established.**

This extends [notebook 03](REGENERATION.md): a cofactor becoming divisible by
the core's odd prime is no longer automatically the end of the analysis. It
can be followed by a proved restoration step using the actual aliquot map.

## 1. What a 4-adic extension can and cannot add

The moduli 4^K=2^(2K) are cofinal among the binary moduli. Their inverse-limit
ring is the same as Z₂; they are not an independent prime-adic direction.
Tracking more base-four digits can nevertheless retain information that a
valuation-only state discarded.

Do not replace v₂(n) with the count floor(v₂(n)/2) of trailing base-four zeros:
that count is not an additive valuation. It is zero at 2 but one at 2·2.
A lossless representation keeps the extra bit:

```text
n = 4^r · 2^ε · w,     ε∈{0,1}, w odd,     v₂(n)=2r+ε.
```

That bit matters dynamically. The exact step 19404 → 42840 changes v₂ from
2 to 3, leaving the driver-28 class, although both trailing-base-four-zero
counts equal one. The next term belongs to the v₂=3 driver-120 class; losing
one driver does not necessarily stop growth.

### Proposition G — a conditional, square-sensitive phase invariant

For odd u, write T(u)=2σ(u)−u. Then

```text
T(u) ≡ −u (mod 4)       if u is not a square,
T(u) ≡  u ≡ 1 (mod 4)   if u is a square.
```

This follows because σ(u) is odd exactly when u is a square. In the square
case an odd square is 1 modulo 4; otherwise 2σ(u) is divisible by 4.

Let U={odd positive u≡2 (mod 3)}, and suppose u has the certified two-step
return from notebook 03. Its mod-4 phase obeys

```text
u ≡ 1 (mod 4)  => T²(u) ≡ 1 (mod 4),
u ≡ 3 (mod 4)  => T²(u) ≡ 1 if T(u) is square, and 3 otherwise.
```

Indeed u∈U cannot be a square. If u≡1 (mod 4), its middle image is 3 modulo 4
and cannot be a square either. Thus **u≡5 (mod 12) is an absorbing phase under
successful two-step returns**. This does not assert that those returns occur.
A hypothetical orbit made entirely of these returns could encounter at most
one square middle term: after it, the phase is permanently 1 modulo 4.

Examples: 47 → 49 → 65 switches phase 3→1 at a square middle; 53 → 55 → 89
keeps phase 1. The latter returned value still fails the next two-step guard.
The base-four phase closes conditionally; the factorization condition does not.

There is even extra supply in the unitary-5 case. If u≡5 (mod 12) and
T(u)=5v with gcd(5,v)=1, then v≡11 (mod 12). A prime 3 modulo 4 occurs to
an odd exponent in v, giving 4|σ(v); v≡2 (mod 3) gives 3|σ(v). Hence
72|σ(T(u)) and T²(u)≡−T(u) (mod 144). This stronger bound still holds in
53 → 55 → 89, whose next image 91 has divisor sum 112 not divisible by 3.

## 2. A stronger positive result: restoration after the core prime is hit

Let q=2^(a+1)−1 be a **prime**, a≥1, and D=2^a q. Then D is an even perfect
number, since σ(D)=q(q+1)=2D. The first two cases are D=6 and D=28.

When gcd(u,D)=1, s(Du)=D T(u). At q|u that reduction is invalid, but the full
aliquot map may still retain the driver and restore an exact D-core.

### Proposition H — complete one-step restoration criterion

Write

```text
n = 2^a q^b v,     b≥2, gcd(v,2q)=1,     q=2^(a+1)−1 prime.
```

The successor has **exactly** v₂(s(n))=a and vq(s(n))=1 if and only if

```text
q does not divide σ(v),
and either b is odd or v₂(σ(v)) > a.
```

**Proof.** Multiplicativity gives

```text
s(n) = q σ(q^b) σ(v) − 2^a q^b v.
```

Dividing by q and reducing modulo q gives σ(v), because σ(q^b)≡1 (mod q)
and b≥2. Thus the successor's q-exponent is exactly one iff q∤σ(v).

The 2-adic supply is A=v₂(σ(q^b))+v₂(σ(v)), with

```text
v₂(σ(q^b)) = 0                  if b is even,
              a+v₂(b+1) ≥ a+1  if b is odd.
```

This is the geometric-sum/LTE formula, using v₂(q+1)=a+1. The successor has
2-exponent exactly a iff A>a: A<a gives a drop, and A=a gives cancellation
and a strict rise. For odd b the supply inequality is automatic; for even b
it is exactly v₂(σ(v))>a. Combining the two conditions proves the equivalence. ∎

For b=1, the 2-exponent is always retained, because σ(q)=2^(a+1). Only a
higher q-power can expose the insufficient-supply or cancellation branches.

Every term in these driver classes above D grows: the scaled proper divisors
of the perfect number D already sum to n, and 1 is an additional divisor
when n>D. Hence a successful restoration is also a growing step.

The proposition gives infinite families without any prime-tuples assumption:
for every odd b≥3, take v=1. More importantly, it is an **if and only if** test
for every cofactor v, not just for primes or for tested values. Its proof is
independent of the numerical examples.

### Actual compositions, not an invalid continuation of T

- **Core 6:** the cofactor path from 263 has four consecutive certified
  two-step returns before it reaches 2163=3·721. The scaled term is
  12978=2·3²·721. Since σ(721)=832, which is coprime to 3 and divisible by
  2⁶, Proposition H restores the core:

  ```text
  12978 → 19470 = 6·3245.
  ```

  This extends the path after the old coprimality condition failed. It is not
  legitimate to substitute T(2163) for the next scaled cofactor.

- **Core 28:** 1316=28·47 → 1372=4·7³ → 1428=28·51. The odd spike exponent
  makes restoration automatic here. In particular T(49)=65, but the actual
  scaled successor after hitting 7 is 51, not 65.

- **A composite bridge:** 9772=28·349 eventually reaches
  60564=4·7²·309. Here σ(309)=416=2⁵·13, coprime to 7. The even-spike
  criterion holds, so 60564 → 105420=28·3765 restores the core.

The 28-core example responds to genuinely different divisibility—v₂=2 and
support from 7—not to a supposedly independent valuation at the composite
base 4. In general, u≡−1 (mod 7) does **not** imply 7|σ(u): u=27 has σ(u)=40.
The automatic mod-3 supply used in notebook 03 cannot be transferred to 7.

## 3. Attempted closure, and its exact failure

A natural candidate X_D consists of terms above D with either:

1. exact core exponents (v₂,vq)=(a,1), or
2. a higher q-power satisfying Proposition H's restoration guard.

Every member maps into the broader driver class {v₂=a, q|n}. However it need
not map into **X_D**: an exact-core member may create a bad spike.

For D=28 the explicit failure is

```text
11508 = 28·411
   → 19404 = 4·7²·99
   → 42840.
```

At the spike, σ(99)=156 has v₂=2, **equal** to a=2 rather than greater.
Cancellation raises the next exponent to 3, not 2. Thus 11508∈X₂₈ but
19404∉X₂₈. The earlier successful restoration 1372 → 1428 does not prevent
this later failure on the same orbit. The 6-core candidate likewise fails
at 78 → 90 → 144.

Even q∤σ(v) alone is insufficient. Conversely, odd b guarantees retention
of the 2-exponent but not restoration of the q-exponent: 17836=4·7³·13 has
σ(13)=14 divisible by 7, and its successor has (v₂,v₇)=(2,2), not (2,1).
It still retains driver 28; a failed exact-core restoration is not necessarily
a driver exit.

A more flexible method can allow hand-offs between drivers. For example
42840 has v₂=3 and is divisible by 120, so the displayed driver-28 exit is
not a decrease. This notebook does not supply a closed, growing union of
such hand-off states.

## 4. Arbitrarily fine 4-adic and 3-adic input tags do not decide the guard

### Proposition I — finite local ambiguity, even for prime cofactors

Fix any K≥1 and L≥2, and put M=4^K·3^L. The two-step return predicate on U
is not determined by residues of u and σ(u) modulo M, their 2- and 3-adic
valuations, and the information that u is prime.

**Proof.** The prime u=5 has σ(u)=6 and T-orbit 5 → 7 → 9, so it fails the
two-step return to U. Choose primes p satisfying

```text
p ≡ 5 (mod M),
p ≡ 3 (mod 25).
```

The moduli are coprime and both residues are units. CRT and Dirichlet give
infinitely many such primes p>5. Their p and σ(p)=p+1 match 5 and 6 modulo M.
Their valuations also match exactly: v₂(p)=v₃(p)=0, and
v₂(σ(p))=v₃(σ(p))=1.

But p+2≡5 (mod 25), so it contains exactly one factor of 5. Since p≡2 (mod 3),
the unitary-5 lemma from notebook 03 applies and T²(p)≡2 (mod 3). These
primes do have the certified two-step return. ∎

For the scaled sources 6p, even the complete current supply tuple
(v₂(n),v₃(n),v₂(σ(n)),v₃(σ(n)))=(1,1,3,2) matches that at n=30, as do
n, σ(n), and the first successor modulo M.

**Scope:** this rules out that finite local classifier, not every possible
factorization-aware invariant or multistep method. Full p-adic integers are
not being identified with one another. Factorization of T(u) distinguishes
the cases. Also 30 does return to the scaled class after **three** actual
aliquot steps (30 → 42 → 54 → 66); failure at two steps is not no-return.

## 5. Trying algebraically closed cofactor templates

Tracking a fixed core and one prime cofactor makes the next step affine,
which looks promising for exact propagation. It cannot support an infinite
growing orbit if only finitely many multiperfect cores are allowed.

### Proposition J — no infinite prime-cofactor orbit over finitely many multiperfect cores

Let D range over any fixed finite collection satisfying σ(D)=k_D D with
integer k_D≥2. There is no infinite aliquot orbit all of whose terms are
D_j p_j, with p_j prime and coprime to D_j. Arbitrary switching is allowed;
no periodicity of the core sequence is assumed.

**Proof.** Multiplicativity gives

```text
s(Dp) = D[(k_D−1)p+k_D] > Dp.
```

Such an infinite orbit would strictly grow, so its cofactor primes eventually
exceed every allowed D. Since D_j divides D_(j+1) p_(j+1), and that large
prime is coprime to D_j, we get D_j | D_(j+1). A divisibility chain in a finite
collection is eventually constant.

On the resulting fixed core, the primes follow p↦Ap+B with A=k_D−1≥1 and
B=k_D>0. Choose a sufficiently late cofactor prime p not dividing A. Modulo p
this affine map is a permutation, whose orbit from 0 returns to 0 in at most
p steps. The corresponding later cofactor is a multiple of p larger than p,
contradicting primality. ∎

This includes finite switching among 6, 28, and 120. It does **not** exclude
composite cofactors, infinitely many cores, or general factorization patterns.
It does not establish that these local deductions are historically new.

### A concrete denominator-depletion branch

The non-multiperfect core 84 is another attempted way to carry 2², 3, and 7
together. For a prime p coprime to 84, retaining an 84-core requires

```text
p' = s(84p)/84 = (5p+8)/3,
p'+4 = (5/3)(p+4).
```

Every valid prime-cofactor step consumes one unit of v₃(p+4). This cannot
continue indefinitely. The exact example is

```text
1932=84·23 → 3444=84·41 → 5964=84·71 → 10164=84·121.
```

The valuations v₃(p+4) are 3,2,1,0. The last cofactor is composite, so the
prime formula is no longer valid. The actual next term is 19628=28·701,
not a term obtained by rounding the rational prime formula. Composite
factorizations and driver changes are precisely where a more general
regeneration proof would have to do new work.

## 6. What remains open

The restoration lemma moves the boundary: it supplies rigorous transitions
through some prime-power hits, not merely an instruction to stop there.
The base-four phase can also be propagated once a two-step return is known.
But neither result forces the next spike to satisfy its restoration condition.

A successful disproof certificate still needs a nonempty class containing an
explicit seed, closure under actual aliquot returns (possibly with driver
changes), and net growth at those returns. The tested candidate X_D fails;
no replacement closed class is established. A finite growing prefix, even
with several certified restorations, is not evidence of divergence.

## 7. Verification and reproducibility

```sh
python3 -m aliquot core-returns
python3 -m aliquot core-returns > /tmp/aliquot-core-returns.json
cmp /tmp/aliquot-core-returns.json research/results/core-returns.json
python3 -m unittest discover -s tests -p test_core_returns.py -v
```

[`aliquot/core_returns.py`](../aliquot/core_returns.py) and the
[report](results/core-returns.json) check named phase/bridge examples, five
local-ambiguity witnesses, four actual driver traces, and the 84-core branch.
These are not orbit frequencies. Tests independently compare the bridge
criterion against an additive divisor sieve through 100,000 and the mod-4
phase on odd inputs below 10,000. The proofs do not depend on those bounds.

Every reported driver transition and coprime-cofactor sum is independently
recomputed by divisor-pair enumeration. The ambiguity witnesses reuse the
independently checked two-step certificates from notebook 03. No extrapolated
T step is accepted after its coprimality hypothesis fails.

Named traces permit **64 transitions**, with an inclusive **1,000,000 source
cap** and **2,000,000 factorization work units per call**. A known successor
above the source cap is retained exactly, not clipped or iterated. The 1578
and 9772 traces stop at that cap: their final known values are 1010958 and
1351308. These statuses are unresolved continuation, not divergent orbits.
A resolved driver exit concerns only that driver, not the full orbit's fate.
The reusable tracer caps requests at 256 transitions and the same source cap.

The CRT constructor is capped at 16 digits in each requested base for
resource discipline; Proposition I is an all-precision proof, not a result
inferred from those finite witnesses. JSON values are exact decimal strings;
small residue tags, exponents, counts, and bounded work limits are integers.
All research stays outside `site/`. Algorithmic checks share a Python runtime.
Two read-only AI critiques audited the restoration criterion, failed closure,
finite-precision scope, and finite-multiperfect-core obstruction and found no
substantive proof gap. They agreed that no iterable guard had been established.
Neither these critiques nor the computations constitute human peer review or
formal verification.
