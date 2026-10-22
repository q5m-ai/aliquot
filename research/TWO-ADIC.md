# Research notebook 02: adapting the Erdős 193 valuation strategy

**Status:** a proof attempt with rigorous partial deductions, failed candidate
invariants, and bounded exact checks. **No proof or disproof of the aliquot
conjecture, no divergent orbit, and no novelty claim.** The proofs below do not
use the numerical census as a premise. They are not Lean-formalized.

The useful outcome is not an infinite orbit. It is a precise obstruction to a
binary-residue-only construction, together with a smaller factorization-aware
problem on which to focus a disproof attempt.

## 1. What actually transfers from Erdős 193?

The source consulted is Cambie–Kalviainen's
[Gaussian-walk paper at revision `e5ceac4`](https://github.com/q5m-ai/erdos-193/blob/e5ceac4bf1be27fff297c18be379ae9da4efff83/paper/erdos193.tex),
not just the older Hilbert exposition. It constructs a walk and proves the
**all-pairs identity**

```text
v₂(|w_n − w_m|²) = v₂(h_n − h_m).
```

The squared norm scales with twice the valuation of a multiplier, whereas the
height scales with it once. Collinearity would therefore force positive A, B
with v₂(A) = v₂(B) = v₂(A+B), an impossibility. A binary recursion and explicit
state tags establish the identity for every pair, not merely a finite prefix.

For aliquot iteration the map is prescribed: s(n) = σ(n) − n. We cannot choose
tags that change its arithmetic. Neither σ nor s has the required homogeneity,
and an escaping orbit does not impose collinearity or equal slopes. Thus the
norm/height contradiction does **not** transfer by replacing the walk indices
with aliquot terms.

What does transfer is the method: derive an exact valuation law; identify the
state needed to propagate it; then prove a closure or descent statement. The
last step is still missing here. This session reads the mathematical source;
it does not rerun the separate Erdős 193 Lean build.

## 2. Exact even-step law: the prime-exponent fingerprint

For an even positive integer write

```text
n = 2^a m,    a ≥ 1, m odd,
b = v₂(σ(m)),
C = 2^(a+1) − 1.
```

Multiplicativity gives s(n) = C σ(m) − 2^a m. If m = ∏ p^e, the exact fingerprint is

```text
b = Σ over odd exponents e of [v₂(p+1) + v₂(e+1) − 1].
```

Even exponents contribute zero. This is the geometric-sum/LTE identity proved
in [notebook 01](README.md#2-a-growing-class-with-an-exact-exit-criterion).
A subsequent literature audit located this known formula explicitly in
Amdeberhan–Moll–Sharma–Villamizar, Theorem 1.1; see the
[prior-art note in notebook 03](REGENERATION.md#1-growth-versus-the-supply-of-factors-2-and-3).
In particular it depends on **prime exponents**, not just m's final binary digits.

### Proposition A — complete valuation transition

```text
v₂(s(n)) = b                                  if b < a,
           a                                  if b > a,
           a + v₂(C [σ(m)/2^a] − m) ≥ a+1     if b = a.
```

**Proof.** The two terms in C σ(m) − 2^a m have valuations b and a, since C
and m are odd. Unequal valuations give the smaller valuation. If they agree,
factor out 2^a; the two remaining units are odd, so their difference is even.
That difference is positive because s(n) ≥ 1 for even n ≥ 2. Thus the displayed
valuation is finite. ∎

The equality case is a genuine cancellation case; replacing it by min(a,b) is
wrong. For example, 12 → 16 has (a,b) = (2,2) but successor valuation 4.
Even knowing (a,b) does not determine that cancellation:

```text
10 →    8       (a,b) = (1,1), next valuation 3
26 →   16       (a,b) = (1,1), next valuation 4
2042 → 1024    (a,b) = (1,1), next valuation 10.
```

**In fact the jump is unbounded with the same (a,b).** For any t ≥ 2, Dirichlet's
prime-in-progressions theorem supplies a prime p ≡ 2^t−3 (mod 2^(t+1)). This
is an odd residue, and p ≡ 1 (mod 4). For n = 2p we have (a,b) = (1,1) and
s(n) = p+3, whose valuation is exactly t. This is an existence proof using
Dirichlet's theorem, not an assertion that a particular prime polynomial
always takes prime values.

### Consequence for the growing driver-six class

Let C6 = {n > 0 : n ≡ 6 (mod 12)}. Here a=1 and 3 divides every successor.
Proposition A gives precisely

```text
s(n) ∈ C6  iff  b ≥ 2.
```

Above 6, every C6 source grows strictly. A proven perpetual C6 orbit would
therefore disprove the conjecture. But the fingerprint does not propagate:

| Source | (a,b) | Successor | Its b | Second successor |
| ---: | :---: | ---: | ---: | ---: |
| 30 | (1,3) | 42 | 5 | 54, retained |
| 78 | (1,3) | 90 | 1 | 144, exits to a multiple of 4 |
| 438 | (1,3) | 450 | 0 | 759, exits to odd |

Even demanding a large initial b does not repair the obvious invariant:

```text
72198 = 2 · 3³ · 7 · 191
σ(72198/2) = 61440, v₂ = 12
72198 → 112122 = 2 · 3² · 6229 → 130848
σ(112122/2) = 80990, v₂ = 1.
```

Thus every proposed class `{n ∈ C6 : b(n) ≥ B}` with 2 ≤ B ≤ 12 fails closure
on this one exact witness. Nothing here establishes the fate of thresholds
B > 12. Likewise 48222 → 66978 → 80559 collapses b from 9 to 0 before an odd
exit. A large valuation reserve is not a monotone rank or a survival guarantee.

## 3. An elementary obstruction to a continuous 2-adic map

### Proposition B — s is not 2-adically continuous at 18, even within C6

For K ≥ 4 put n_K = 18(1+2^K). Then

```text
v₂(n_K − 18) = K+1,
s(18) = 21 is odd,
s(n_K) is even.
```

**Proof.** An odd positive integer has odd σ exactly when it is a square:
in the prime-power product, σ(p^e) is odd exactly when e is even. The same
criterion holds for σ(2^a m), using the odd part m.

For positive K, 1+2^K can be a square only when K=3. Indeed, if x²−1=2^K,
then x−1 and x+1 are powers of 2 differing by 2; they must be 2 and 4, giving
x=3 and K=3. Therefore 9(1+2^K) is not a square for K≥4. Its divisor sum is
even, so s(n_K) is even. Meanwhile n_K is in C6 and converges 2-adically to
18, whose successor is odd. ∎

Consequently, no finite precision of the input's binary digits determines even
the **parity** of its successor near 18. There is no continuous map on Z₂ that
agrees with s on every positive integer. In particular, a compatible system
of residue-only transition maps cannot represent the full aliquot map.

**Boundary:** this is not a ban on 2-adic reasoning, state tags involving prime
factorization, selected restricted domains, or discontinuous digit algorithms.
It does not say that s is discontinuous at every integer. Nor does a putative
infinite 2-adic path automatically give a positive-integer seed: compatibility
of arbitrarily long finite constraints can yield only a 2-adic integer, and
2-adic convergence is unrelated to ordinary escape to infinity.

## 4. A stronger obstruction: no fixed-binary-residue growing subclass

The following rules out an actual family of disproof certificates, rather
than merely failure of a globally defined map.

### Proposition C — no nonempty eventually residue-defined invariant subset of C6

Fix an integer N ≥ 0, K ≥ 1, and a set R of residues modulo 2^K. Define

```text
X = {n > N : n ∈ C6 and n mod 2^K ∈ R}.
```

If X is nonempty, it cannot satisfy s(X) ⊆ X.

**Classical input:** Dirichlet's theorem says that every residue a coprime to
its positive modulus d contains arbitrarily large primes a+jd. This is the
only prime-existence theorem used here; it is not an unproved assumption.

**Proof.** We may refine to K≥2 and discard residues not equal to 2 modulo 4.
For each remaining r in R, solve

```text
p ≡ 3⁻¹(r/2)  (mod 2^(K−1)).
```

This is an odd residue, hence coprime to the modulus. Dirichlet supplies a
prime p>3 large enough that 6p>N. Then 6p ∈ X, and, since p does not divide 6,

```text
s(6p) = σ(6)σ(p) − 6p = 12(p+1) − 6p = 6p+12.
```

This successor still lies in C6 and exceeds N. Closure of X would therefore
force r+12 (mod 2^K) into R. On the residues 2 modulo 4, addition by 12 is a
**single cycle**: write r=2+4j and note that addition by 3 generates the cyclic
group modulo 2^(K−2). A nonempty R closed under this translation must contain
every eligible residue. Thus X contains every C6 integer above N.

Choose an odd t with 18t²>N. This belongs to X, but its odd part 9t² is a
square, so σ(18t²) is odd and s(18t²) is odd. Its successor is not in C6,
contradicting closure. ∎

Any finite union of binary cylinders can be expressed at a common precision,
so the result covers that formulation too. Allowing an arbitrarily large
finite starting cutoff N does not save it.

**Boundary:** this does not exclude an invariant class with odd-prime/exponent
tags, conditions modulo odd prime powers, unbounded memory, a multistep return
map, or a divergent orbit that leaves C6. It is not evidence that the full
aliquot conjecture is true. It rules out precisely this simple route to
constructing a divergent orbit.

## 5. A concrete reduced target: the odd-cofactor map

Rather than another residue-only search, retain one exact factorization tag:
**the exponent of 3 is exactly one**. Write

```text
n = 6u,    gcd(u,6)=1,
T(u) = 2σ(u) − u = u + 2s(u).
```

### Proposition D — exact core reduction and conditional escape

While u is odd and not divisible by 3,

```text
s(6u) = 6T(u).
```

For every odd u>1, T(u) is odd and T(u)≥u+2. Therefore, if there exists an
odd u₀>1 whose **entire** T-orbit avoids multiples of 3, then

```text
s^k(6u₀) = 6T^k(u₀) ≥ 6u₀ + 12k
```

for all k, giving a rigorous counterexample to the full aliquot conjecture.

**Proof.** Coprimality gives σ(6u)=12σ(u), proving the identity. Oddness follows
from 2σ(u)−u. For u>1 the divisor 1 contributes to s(u), so T(u)≥u+2. Avoidance
of 3 preserves coprimality with 6 and allows the identity to be applied
inductively forever. ∎

The exclusion u₀=1 matters: it gives T(1)=1 and the perfect fixed point 6.
If a T-orbit hits a multiple of 3, the reduction stops being applicable at
that term. This **does not** mean the corresponding aliquot orbit exits C6
or starts decreasing; e.g. 30 → 42 → 54 remains in C6.

### The mod-3 transition is exact, but its factorization tag is not closed

For 3∤u, an odd prime-power factor contributes

```text
σ(p^e) ≡ e+1 (mod 3)     if p ≡ 1 (mod 3),
         1 (mod 3)       if p ≡ 2 (mod 3) and e is even,
         0 (mod 3)       if p ≡ 2 (mod 3) and e is odd.
```

If u≡2 (mod 3), at least one prime of the last kind occurs, so σ(u)≡0.
The only possible residue transitions are consequently:

| u mod 3 | σ(u) mod 3 | T(u) mod 3 |
| ---: | ---: | ---: |
| 2 | 0 | 1 |
| 1 | 0 | 2 |
| 1 | 1 | 1 |
| 1 | 2 | 0 — leaves this core |

This gives a specific sufficient disproof target:

> Find an explicit odd u₀>1 and prove that no T-iterate has the forbidden
> signature `u≡1 (mod 3), σ(u)≡2 (mod 3)` and that 3∤u₀.

It removes the growth obligation: growth is automatic. What remains is an
infinite avoidance theorem for an **arithmetic**, not freely chosen, orbit.
This is a narrower target than perpetual C6 membership, since the exponent of
3 is kept at one. Proving that every such T-orbit hits a multiple of 3 would
eliminate only this narrower mechanism, not prove the aliquot conjecture.

Small candidates fail quickly: T-orbits 5 → 7 → 9, 25 → 37 → 39, and
49 → 65 → 103 → 105 hit multiples of 3. A finite prefix avoiding 3 would not
solve the problem either. We have no invariant factorization language or
well-founded descent rank proving the required universal statement. That is
the missing analogue of the all-pairs propagation lemma in Erdős 193.

## 6. Reproducible checks — not premises of the proofs

From the repository root:

```sh
python3 -m aliquot scan-two-adic --bound 100000
python3 -m aliquot scan-two-adic --bound 100000 > /tmp/aliquot-two-adic.json
cmp /tmp/aliquot-two-adic.json research/results/two-adic-100000.json
python3 -m unittest discover -s tests -p test_two_adic.py -v
```

The [committed report](results/two-adic-100000.json) covers:

- **50,000 even sources**, 2≤n≤100,000, one transition each: the valuation
  drops for 8,394, stays equal for 34,248, and rises for 7,358.
- **8,333 C6 sources** in that interval, followed until their first exit or
  through two transitions. The fixed point 6 is included.

| C6 outcome | Sources |
| --- | ---: |
| First transition exits to odd | 37 |
| First transition exits to a multiple of 4 | 475 |
| First retains, second exits to odd | 30 |
| First retains, second exits to a multiple of 4 | 502 |
| Both transitions retain C6 | 7,289 |

There are 7,821 independently checked second transitions. The largest
successor in the even-source first-step census is 304,920; the largest in the
C6 second-step check is 402,570. **Only the sources** are bounded by 100,000;
no successor is clipped to the source bound.

For the finite illustration of Proposition C at modulus 1024, the census finds
prime-branch witnesses for all 256 eligible residues. The largest of their
first witness primes is 7,681. This demonstrates the translation edges at
that modulus only; Dirichlet and the written cycle argument, not this census,
prove the assertion for all K.

The implementation in [`aliquot/two_adic.py`](../aliquot/two_adic.py) uses exact
Python integers, proven trial factorization, and the prime-exponent valuation
formula. An additive divisor sieve independently checks first-step sums and
odd-part divisor sums. Divisor-pair enumeration independently checks all
second-step sums and their odd parts. Mismatches abort the report. The tests
also check the named failed invariants, the discontinuity examples for
4≤K≤16, the odd-cofactor identity/mod-3 table, and the exceptional K=3 square.
These finite checks do not prove the universal lemmas.

The source-bound cap is **100,000** for this experiment. The core retains its
2,000,000-unit per-factorization work budget; exhaustion is unresolved and
raises an exception, never a probable-prime shortcut. Values in JSON use
exact decimal strings; bounded counts and valuation exponents use integers.
An empty census reports zero for an unobserved maximum, not an evaluation of
s(0). All code and results stay outside `site/`.

The checkers share a Python runtime: their algorithms differ, but this is not
independent human review or formal verification. The second-step frequencies
are **not** survival probabilities, and a short residue graph is not an
infinite-orbit certificate.

**Follow-up:** [notebook 03](REGENERATION.md) derives coupled 2–3 supply laws
and proves an infinite family of guarded finite return blocks. The return
condition is not closed; neither perpetual regeneration nor novelty is claimed.
