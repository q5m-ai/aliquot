# Research note 06: transporting factors, and the composite correction

**Status:** an attempt at the missing regeneration step, not a new census.
There is an exact conditional two-step factor handoff with composite output
blocks. However, its hypotheses do not regenerate. Several simpler transport
rules can be excluded algebraically. **No closed return class, infinite orbit
control, conjecture resolution, or historical novelty is established.**

Write s(x)=σ(x)−x and T(x)=2σ(x)−x=x+2s(x). The map T is defined for all
positive integers and strictly increases x>1. It represents an actual aliquot
step by s(6x)=6T(x) **only when gcd(x,6)=1**. This hypothesis must hold at
each source, not merely at the initial source. Never iterate s at zero.

## 1. The first promising identity, and its trap

For distinct primes q,r,

```text
T(qr) = qr+2q+2r+2 = (q+2)(r+2)−2.
```

If p=qr−2 and C=(q+2)(r+2)−2 are also prime, we obtain exact transport:

```text
p → qr → C → (q+2)(r+2)                  under T.
```

No primality of q+2 or r+2 is needed for that last product identity. But its
subsequent divisor sum depends on their actual factorizations and overlap.

Suppose q,r>3 are both 2 modulo 3. If q+2,r+2 are also prime, they are both
1 modulo 3, so σ((q+2)(r+2))≡1 (mod 3). The next two-step return to the
2-modulo-3 cofactor class fails. Keeping the new blocks prime preserves the
simple algebra but loses the required supply.

Composite shifts can supply 3 again: for q=5,r=53 the chain is

```text
263 → 265=5·53 → 383 → 385=7·55.
```

Here 55=5·11 supplies 3 and is coprime to 7. Yet one may not keep shifting
these blocks by 2: the actual next value is T(385)=767, not 9·57−2=511.
The latter substitutes a prime-only formula into a composite block.

## 2. Exact accounting for composite blocks

For x>1 set δ(x)=s(x)−1. It is nonnegative and is zero exactly when x is
prime. For **coprime** v,w>1, expanding σ(vw)=σ(v)σ(w) gives

```text
T(vw) = vw+2v s(w)+2w s(v)+2s(v)s(w).
```

There are two useful ways to express the correction:

```text
T(vw)+2 = T(v)T(w)−2[s(v)s(w)−1],                    (1)

T(vw)+2 = (v+2)(w+2)+D(v,w),                        (2)
D(v,w) = 2(w+1)δ(v)+2(v+1)δ(w)+2δ(v)δ(w).
```

In particular, there are no extra +2 terms on the T(v),T(w) factors in (1).
A proposed expression with those extra shifts was rejected during this attempt.

Put C=T(vw). Applying T once more yields

```text
T²(vw) = (v+2)(w+2)+D(v,w)+2δ(C),                   (3)
T²(vw) = T(v)T(w)+2E(v,w),                          (4)
E(v,w) = s(T(vw))−s(v)s(w).
```

These are unconditional identities for coprime blocks, not assumptions that
C is prime. The correction E can have either sign.

### Proposition L — rigidity and a budget obstruction

For coprime integers v,w>1:

1. **Literal shifts:** T²(vw)=(v+2)(w+2) if and only if v,w,C are all prime.
2. **Independent T-updates:** T²(vw)=T(v)T(w) if and only if
   s(C)=s(v)s(w).
3. If K=s(v)s(w)>1, that second equality requires C≤(K−1)².
4. In particular, for distinct odd primes q,r,
   T²(qr²)≠T(q)T(r²).

**Proof.** In (3), every correction is nonnegative. D vanishes exactly when
both blocks are prime, and δ(C) vanishes exactly when C is prime. This proves
1. Equation (4) proves 2. If K>1 and s(C)=K, then C is composite. A composite
C has a proper divisor at least √C, distinct from 1; hence
s(C)≥1+√C, giving 3. For v=q,w=r², K=r+1 but C=T(qr²)>qr²>r²,
contradicting 3. ∎

Thus even the natural supply-bearing block r² with r≡1 (mod 3) cannot replace
one prime block while preserving exact independent T-updates. This does not
exclude regrouping, partial inheritance, or transport with nonzero E.

Nor can literal +2 block transport continue indefinitely: successive odd
blocks q,q+2,q+4,... necessarily reach a multiple of 3 larger than 3, whereas
part 1 requires every transported block to remain prime.

## 3. A positive handoff with composite output blocks

The next attempt allows one prime to persist through the intermediate term,
instead of updating all factors independently.

### Proposition M — retained-prime transport

Let a,b,p be distinct odd primes with a|(p+1). Define

```text
t = (p+1)/a,
R = T(ab) = (a+2)b+2a+2,
h = tR+b,
Q = t(a+2)+1.
```

If h is prime, then

```text
T(apb) = a h,
T²(apb) = R Q.                                     (5)
```

Neither R nor Q is required to be prime.

**Proof.** Since p=at−1, multiplicativity gives

```text
T(apb) = 2(a+1)(p+1)(b+1)−apb
       = a[t((a+2)b+2a+2)+b] = ah.
```

We have h>a, so its primality makes it coprime to a. Consequently

```text
T(ah) = (a+2)h+2a+2
      = t(a+2)R+(a+2)b+2a+2 = RQ.
```

This proves both identities. ∎

The prime-bridge hypothesis is substantive. If h is instead composite but
still coprime to a, the second formula becomes

```text
T(ah) = RQ+2(a+1)[s(h)−1],
```

with a strictly positive correction; the factorization RQ no longer follows.

**A guarded middle-to-middle return.** Additionally suppose

```text
a ≡ 1 (mod 3),    b ≡ p ≡ 2 (mod 3),
gcd(R,Q)=1,       and 3|σ(R) or 3|σ(Q).
```

Then t≡0, R≡Q≡1, and ah≡2 (mod 3). Thus apb, ah, RQ are odd and coprime
to 3. The input apb and output RQ both lie in

```text
M = {m>1 : m odd, m≡1 (mod 3), 3|σ(m)}.
```

For the input, b and p supply factors of 3. For the output, the coprime
blocks R,Q and the stated divisor-sum condition supply 3. The intermediate
term is 2 modulo 3, so this is a two-step first return to M. Both steps are
strictly growing actual aliquot steps after scaling by 6.

**Exact witness, including a prime-square supplier.** Take

```text
a=7, b=17, p=41, t=6,
R=169=13², h=1031 (prime), Q=55=5·11.
```

Then

```text
4879=7·17·41 → 7217=7·1031 → 9295=13²·5·11       under T,
29274       → 43302       → 55770                under s.
```

The output blocks 169 and 55 are coprime. Their divisor sums are 183 and 72,
both divisible by 3. This replaces the original supplying primes by different
factors, including a prime 1 modulo 3 at exponent 2. The prime 4877 may also
be prepended, since T(4877)=4879.

**Why this does not close.** The output has four prime factors counted with
multiplicity, with 13 repeated; it is not a product of three distinct primes
as required at the input of Proposition M. More generally, (5) does not force
RQ back into that input family or into any other proved closed family.
The condition that h is prime is checked for the witness, not guaranteed at
future returns. No infinitude of simultaneous prime parameters is asserted.
The full class M is not closed: 55→89→91, with 3∤σ(91).

This is a successful conditional factor handoff, not successful perpetual
regeneration.

## 4. A filter for partial supplier inheritance

One might retain just a supplying prime from a formal prime-bridge output
C+2, even when C is actually composite. The following identifies a restriction
on that repair.

### Proposition N — quadratic obstruction at a semiprime bridge

Let C=ab with distinct primes a,b, and let ℓ be an odd prime dividing C+2.
Then

```text
ℓ | T(C)  iff  a+b ≡ 0 (mod ℓ).
```

In particular, retention implies a²≡2 (mod ℓ). For the supplier type
ℓ≡2 (mod 3) occurring to an odd exponent, necessarily

```text
ℓ ≡ 17 or 23 (mod 24).
```

**Proof.** From ab≡−2 and T(ab)=ab+2(a+b+1), the equivalence follows by
reducing modulo ℓ and canceling 2. With b≡−a, the relation ab≡−2 becomes
a²≡2. The classical supplementary quadratic-reciprocity law
(2/ℓ)=(−1)^((ℓ²−1)/8) gives ℓ≡1 or 7 (mod 8); combine this with
ℓ≡2 (mod 3). ∎

Thus 5 and 11 cannot survive this particular semiprime replacement of a
prime bridge. The allowable residue classes are necessary, not sufficient
conditions for an arbitrary bridge. For example, C=23·11=253 has
T(C)=323=17·19, and C=5·41=205 has T(C)=299=13·23.

A square bridge C=a² with a prime cannot retain any odd prime ℓ|C+2:
T(a²)−(a²+2)=2a, and gcd(a,a²+2) divides 2. Higher-complexity bridges
are not excluded. Even retained divisibility would still need the correct
exponent to supply 3; a unitary block needs gcd(d,T(C)/d)=1 as well.

## 5. What remains unproved

The factor transport in Proposition M succeeds where independent block
updates fail, but it does not regenerate its hypotheses. A finite collection
of such handoffs would need to cover **every** allowed exit, establish finite
return times, and prove net growth on all possible return-graph cycles.
Observing one profitable cycle in a diagram would not show that an actual
orbit follows it indefinitely.

The concrete missing operation is to factor the corrected product

```text
T(v)T(w)+2E(v,w)
```

into new unitary supplying blocks by a rule whose conditions follow from
the input conditions and recur. Defining the class by demanding that all
future guards hold merely restates the problem; it does not exhibit a seed
or prove closure.

The strongest honest outcome is conditional algebraic transport plus explicit
obstructions. This is not an established advance toward a whole-orbit bound
or escape certificate. No novelty review specific to these elementary
identities has been completed; see [the literature audit](LITERATURE.md) for
related known work and the separate status of the S-unit deduction.

## 6. Bounded verification, separate from the proofs

```sh
python3 -m unittest discover -s tests -p test_block_transport.py -v
```

The tests check the written identities using an additive proper-divisor sieve
through 100,000, with coprime odd block inputs 3≤v,w≤79. They check the
conditional transport formula on odd prime parameters up to 59, prime-square
obstructions for named primes through 23, and the semiprime filter using
prime factors below 100 and supplying-prime tests below 50. Bounds are finite
regression coverage, never premises of the universal proofs.

The named bridges have independent trial-factorization and divisor-pair-sum
checks, including the scaled actual aliquot transitions. No probable-prime
shortcut, new census report, runtime API, or site change is introduced.
Software tests do not verify the universal proofs or replace human review.
Two independent read-only AI analyses agreed on the corrected identities and
obstructions, and both subsequently audited the conditional positive handoff
and its witness. They found no substantive gap and agreed that no infinite
closure was obtained. This is neither human mathematical review nor formal
verification.
