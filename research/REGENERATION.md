# Research notebook 03: coupled divisibility and certified return blocks

**Status:** exact local arithmetic, a proved infinite family of **finite**
regeneration blocks, and counterexamples to stronger return claims. No perpetual
regeneration, divergent orbit, conjecture resolution, or mathematical novelty
is claimed. None of the family proofs uses an experimental census as a premise.

The positive result is stronger than one surviving numerical example: for every
L>1, infinitely many starting values have a certified two-step first return to
one residue class with growth factor greater than L. The quantifiers do **not**
say that one starting value has infinitely many such returns.

## 1. Growth versus the supply of factors 2 and 3

Write n=2^a 3^b m, with gcd(m,6)=1 and a,b≥0. Multiplicativity gives

```text
s(n)/n = (2 − 2^(−a)) (3/2 − 1/(2·3^b)) σ(m)/m − 1.
```

Prime-power contributions multiply. Their order does not matter. Higher powers
of 2 and 3 increase their contributions, but those contributions saturate at
2 and 3/2 respectively; the other prime factors remain essential. Every
multiple of 6 above 6 grows, but 72=2³3² → 123 immediately loses evenness.

Set A=v₂(σ(n)), B=v₃(σ(n)). The coupled supply laws are

```text
A = v₂(σ(m)) + [0 if b is even; 1+v₂(b+1) if b is odd],
B = v₃(σ(m)) + [0 if a is even; 1+v₃(a+1) if a is odd].
```

For an odd prime q≠3 and exponent e≥0, the cofactor contributions are

```text
v₂(σ(q^e)) = 0                               if e is even,
              v₂(q+1)+v₂(e+1)−1             if e is odd;

v₃(σ(q^e)) = v₃(e+1)                         if q ≡ 1 (mod 3),
              0                              if q ≡ 2 (mod 3), e even,
              v₃(q+1)+v₃(e+1)                if q ≡ 2 (mod 3), e odd.
```

**Derivation.** Apply the geometric-sum formula and lifting the exponent (LTE).
For q≡1 (mod 3), cancel v₃(q−1) from the numerator. For q≡2 (mod 3), an odd
power q^(e+1) is not 1 modulo 3; an even power gives the last displayed formula
by applying LTE to q². Apply these identities also to σ(3^b) and σ(2^a), noting
that σ(2^a) is odd and σ(3^b) is coprime to 3. Multiplicativity adds valuations.

For either prime ℓ∈{2,3}, let c=vℓ(n), C=vℓ(σ(n)). When n>1,

```text
vℓ(s(n)) = min(c,C)                                  if c≠C,
            c + vℓ(σ(n)/ℓ^c − n/ℓ^c)                 if c=C.
```

The equal case always increases the 2-adic valuation, but need not increase
the 3-adic valuation: 6 → 6 retains v₃=1 whereas 42 → 54 raises it from 1 to 3.
For n=1, s(n)=0 and neither successor valuation is assigned a finite value.

Thus a **strict surplus** A>a, B>b preserves the current exponents for one
step. It does not prove a surplus at the next term. New higher valuations
come from cancellation at equal valuations, not from surplus alone.

**Prior art.** This is classical divisor-sum arithmetic, not a new valuation
principle. See Theorem 1.1 of Amdeberhan–Moll–Sharma–Villamizar,
[*Arithmetic properties of the sum of divisors*](https://arxiv.org/abs/2007.03088),
*Journal of Number Theory* 223 (2021), 325–349, for the 2-adic formula.
[Guy–Selfridge (1975)](https://doi.org/10.1090/S0025-5718-1975-0384669-X)
already develops the driver framework and the perpetual-driver route to
possible divergence. No exhaustive novelty review of the return lemma below
has been completed.

## 2. A positive two-step regeneration lemma

Use the exact core reduction from [notebook 02](TWO-ADIC.md#5-a-concrete-reduced-target-the-odd-cofactor-map):

```text
T(u) = 2σ(u) − u,
s(6u) = 6T(u) whenever gcd(u,6)=1.
```

Define the cofactor class U={positive odd u: u≡2 (mod 3)} and its scaled class
G=6U={positive n: n≡30 (mod 36)}. In particular u≥5 in U. If u∈U, an odd
exponent of a prime congruent to 2 modulo 3 occurs in u. Its divisor sum is
divisible by 3, so σ(u)≡0 and T(u)≡1 (mod 3).

A divisor d of w is **unitary** when w=dv and gcd(d,v)=1. This restriction is
needed to multiply σ(d) and σ(v); ordinary divisibility is insufficient.

### Proposition E — a guarded first return with amplification

Suppose u∈U, and T(u)=dv where

```text
d>1, gcd(d,6)=1, gcd(d,v)=1, and 3 divides σ(d).
```

Then T²(u)∈U, and 6u → 6T(u) → 6T²(u) is a genuine two-step first return to G.
All three terms have v₂=v₃=1, and all three have strict 2- and 3-adic supply
surpluses. Moreover, putting ρ(d)=2σ(d)/d−1>1,

```text
T²(u) ≥ ρ(d) T(u) > ρ(d) u.
```

**Proof.** T preserves oddness, and T(u)≡1 (mod 3), so the core reduction is
valid for both transitions. Multiplicativity gives
σ(T(u))=σ(d)σ(v)≡0 (mod 3); hence T²(u)≡−T(u)≡2 (mod 3). This is the first
positive-time return to U since the intermediate cofactor is 1 modulo 3.

As σ(v)≥v,

```text
T²(u) = 2σ(d)σ(v) − dv ≥ (2σ(d)/d−1) dv = ρ(d) T(u).
```

Since d>1, σ(d)>d and ρ(d)>1. Also T(u)=u+2s(u)>u because u>1. The two-step
gain is therefore strictly greater than ρ(d). For each of the three cofactors
w, σ(w) is divisible by 3: for the endpoints use w∈U, and for the middle use
the unitary factor. Thus σ(6w)=12σ(w) has v₂≥2>1 and v₃≥2>1. ∎

### Proposition F — infinitely many entries, without a prime-tuples assumption

Fix any d satisfying d>1, gcd(d,6)=1, and 3|σ(d). Consider primes p>3 such that

```text
p ≡ 5       (mod 6),
p ≡ d−2     (mod d²).
```

These congruences define a reduced residue class modulo 6d², because the moduli
are coprime and gcd(d−2,d)=1 for odd d. **Dirichlet's theorem** therefore gives
infinitely many such primes. For each, T(p)=p+2=dv with v≡1 (mod d), so d is
unitary and Proposition E applies.

Only one variable is required to be prime. We do not assume that p+2, the
returned cofactor, or any simultaneous collection of linear forms is prime.

For d=5 the entry class is p≡53 (mod 150), and ρ=7/5. For example,

```text
p=53:       318 → 330 → 534,
cofactors:   53 →  55 →  89,
actual gain: 89/53 > 7/5.
```

### Corollary — arbitrarily large finite amplification in the same core

For every L>1 there are infinitely many n∈G whose two-step first return to G
exceeds Ln; the intermediate term and both endpoints still have v₂=v₃=1.

**Proof.** Take d to be a squarefree product of primes ≥5, including 5. Then
3|σ(d), and σ(d)/d=∏(1+1/q) can be made arbitrarily large. To justify this
last classical fact, use

```text
∏(1+1/q) = ∏(1−1/q²) · ∏(1−1/q)^(−1):
```

the first product has a positive limit and the second diverges; omitting
2 and 3 changes only a fixed constant. Thus choose d with ρ(d)>L and apply
Proposition F. ∎

**Boundary:** arbitrarily large gains at fixed finite time are compatible
with every orbit eventually terminating or cycling. Large exponents of 2
and 3 in the terms themselves are not necessary for these gains.

## 3. Why these blocks do not yet compose

The sufficient entry condition concerns a factorization of **T(u)**. The proof
returns T²(u) to U, but gives no corresponding factorization of **T³(u)**.
It has not returned to the same guarded subset.

This failure already occurs in the smallest displayed example:

```text
53 → 55 → 89       is certified using d=5,
89 → 91 → 133      does not return to U after two steps.
```

Indeed σ(91)=112 is not divisible by 3, so no unitary divisor of 91 could
satisfy 3|σ(d). Changing the choice of d cannot rescue that next two-step
block. The actual first return from 534 takes four steps:

```text
534 → 546 → 798 → 1122 → 1470.
```

A broader return map permits excursions through different (a,b). For example,

```text
1470 → 2634 → 2646 → 4194 → 4932 → 7626
(a,b): (1,1), (1,1), (1,3), (1,2), (2,2), (1,1).
```

But neither existence nor growth of all such returns is true.

### Exact failures of proposed stronger claims

1. **Strict initial surpluses do not guarantee eventual regeneration.**
   For 66, σ(66)=144=2⁴3², yet

   ```text
   66 → 78 → 90 → 144 → 259 → 45 → 33 → 15 → 9 → 4 → 3 → 1 → 0.
   ```

   There is no positive-time return to G. Other starts can instead enter a
   cycle outside G: 3162 eventually reaches 1184 ↔ 1210.

2. **Even an actual first return can have a net loss, while remaining even.**
   The following is a 27-step first return to G:

   ```text
   500394 → 500406 → 500418 → 621252 → 949226 → 485878 → 246002
   → 123004 → 135044 → 166600 → 310490 → 258670 → 206954 → 147286
   → 73646 → 41698 → 20852 → 18544 → 19896 → 29904 → 59376
   → 94136 → 112624 → 105616 → 144368 → 175552 → 201384 → 344226.
   ```

   No intermediate term is 30 modulo 36. The gain is only 57371/83399<1.
   The initial source even has strict supply surpluses (A,B)=(5,2) above
   (a,b)=(1,1). Thus surplus plus eventual even return is not a net-growth
   certificate. One exact counterexample suffices; no frequency estimate is used.

3. **Several profitable returns do not establish perpetual regeneration.**
   The sequence starting at 318 has returns 534, 1470, and 7626. The checked
   continuation from 7626 reaches 0 without another visit to G. The original
   successful example therefore terminates, despite three profitable blocks.

## 4. The remaining proof obligation

A sufficient disproof route would require an explicit seed in a nonempty
subset X⊆G, a proof that each member has a finite first return R(n), and
proofs that R(n)∈X and R(n)>n. The return sequence would be unbounded. The
full deterministic orbit would then be nonterminating and nonperiodic, hence
tend to infinity as explained in notebook 01. No such X is supplied here.

For the narrower two-step route, it would suffice to find a nonempty subset
of the guarded cofactors in Proposition E closed under T². The example
53 → 89 proves that taking **all** guarded cofactors does not work.

The next meaningful question is therefore which factorization information can
force a suitable unitary factor in a later T-image, while surviving return.
The coupled valuations diagnose supply and cancellation but do not, by
themselves, determine that new factorization. A graph of observed transitions
or a stochastic resupply model cannot replace this deterministic closure lemma.

## 5. Reproducible certificates and bounds

```sh
python3 -m aliquot regeneration
python3 -m aliquot regeneration > /tmp/aliquot-regeneration.json
cmp /tmp/aliquot-regeneration.json research/results/regeneration-examples.json
python3 -m unittest discover -s tests -p test_regeneration.py -v
```

The [report](results/regeneration-examples.json) contains seven coupled-law
examples, five prime-entry certificates, and eight named first-return traces.
It is not a source census, a probability estimate, or an infinite-orbit search.
The written proofs, not prime enumeration, establish the infinite families.

[`aliquot/regeneration.py`](../aliquot/regeneration.py) uses proven trial
factorization and prime-power valuation formulas. Divisor-pair enumeration
independently checks every computed transition, including its coprime-cofactor
sum; the five prime parameters also receive independent divisor-pair checks.
Tests compare the law with an additive sieve for all 1≤n≤10,000, including odd
inputs and s(1)=0, and test both 3-adic cancellation outcomes.

Each named trace allows at most **64 transitions** and an inclusive **1,000,000
source-term cap**. The reusable tracer permits at most 256 transitions and
no larger source cap, bounding independent trial checks. A successor above the
cap is recorded exactly; if it resolves a return, termination, or cycle, no
further factorization is needed. Otherwise it is not iterated. Step, term, and
factorization limits are distinct **unresolved** statuses with checked prefixes,
not no-return conclusions. A cycle outside G or termination proves no future
return for that specific seed. s(0) is never evaluated.

The factorization budget remains 2,000,000 work units per call. A failed
certificate raises `ComputationLimit`; the CLI serializes only a complete
report. A tracer's explicit limit status is not a successful return certificate.
All terms and rational numerators/denominators in JSON are exact decimal
strings. Counts, indices, valuations, and bounded work limits are integers.
All code/data remains outside `site/`; independent algorithms share a Python
runtime and are not independent human review or formal verification.

**Follow-up:** [notebook 04](FOUR-ADIC.md) adds a conditional base-four phase
invariant and an exact restoration criterion after a perfect core's odd prime
is hit. It follows some actual restoration steps that the coprime T-reduction
cannot cover. That larger candidate still fails closure; no infinite orbit or
historical novelty is claimed.
