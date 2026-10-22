# Research note 05: a global reset and finite prime support

**Status:** no proof or disproof of the aliquot conjecture. The earlier notes
clarify local arithmetic, but have not established an indefinitely repeatable
mechanism or demonstrated a major advance toward resolution. This note gives a
global finiteness deduction from the established **S-unit theorem**, not an
elementary solution or a claim of historical novelty. No numerical experiment
is a premise of the proof.

## 1. The classical benchmark is already stronger than finite survival

Lenstra proved that, for every prescribed k, some aliquot sequence satisfies

```text
n < s(n) < ... < s^k(n).
```

Erdős reproduces the short proof in [1, pp. 641–642]. Its mechanism is a finite
chain of prime powers: each link supplies enough divisibility to preserve the
preceding link for one step. One link of the guaranteed chain is spent at each
iteration. Choosing a longer chain gives a longer increasing prefix, not one
integer with an inexhaustible chain.

Here is a precise version. Let p_i be the successive primes, and choose positive
exponents a_i with a_1=2 and

```text
p_i^(a_i+1) divides σ(p_(i+1)^a_(i+1)).
```

Such a choice is possible recursively: for q=p_(i+1), put
L=p_i^(a_i+1)(q−1) and a_(i+1)=φ(L)−1. Euler's theorem applies since gcd(q,L)=1;
dividing q^φ(L)−1 by q−1 gives the required divisor sum.

Let A_l consist of integers with exact exponents v_(p_i)(n)=a_i for i≤l.
If l≥2 and n∈A_l, then 12|n, so s(n)>n. For each i<l, multiplicativity gives
p_i^(a_i+1)|σ(n), while v_(p_i)(n)=a_i. Thus v_(p_i)(s(n))=a_i and
s(n)∈A_(l−1). Starting in A_(k+1) proves the displayed finite-prefix statement.

The missing quantifier exchange is fundamental:

```text
for every k there exists a seed n_k
```

does not imply

```text
there exists a seed n that works for every k.
```

Neither a longer computed prefix nor an infinite family of finite return
blocks fixes this. Likewise, arbitrarily long increasing prefixes rule out a
uniform, fixed-number-of-steps descent argument in the ordinary size n. They
do not rule out a different height, seed-dependent descent, or a return map.
Only the finite-prefix construction from [1] is used here, not its other
asymptotic claims.

## 2. A deduction that is genuinely global

Call a positive integer **S-smooth** if every prime dividing it belongs to the
finite prime set S; 1 is allowed. As throughout the project, s(n)=σ(n)−n for
n>0, and s(0) is undefined.

### Proposition K — finitely many adjacent pairs with fixed prime support

For every finite prime set S, there are only finitely many integers n>1 for
which both n and s(n) are S-smooth.

This permits arbitrary exponents and does not assume any particular driver,
parity pattern, or monotonicity.

**External theorem used.** For a fixed finite prime set P and a fixed number
of variables r, the equation

```text
u_1 + ... + u_r = 1
```

has only finitely many solutions in nonzero rational P-units (signed rationals
whose numerator and denominator primes belong to P), provided no nonempty
subsum on the left vanishes. This is the classical S-unit finiteness theorem;
[2, Theorem 1.1] supplies a stronger finite-rank version. The r=1 case is
immediate. The deep theorem is imported here, not reproved or computationally
verified.

**Proof of Proposition K.** The empty S case is vacuous. Suppose otherwise that
there are distinct admissible n_j tending to infinity, and set m_j=s(n_j).
For any prime p dividing n_j, the proper divisor n_j/p gives

```text
m_j ≥ n_j / max(S) → infinity.
```

By successively passing to subsequences, each of the finitely many prime
exponents in n_j can be made constant or tending to infinity. Therefore

```text
n_j = d ∏_(p∈Q) x_(p,j),     x_(p,j)=p^a_(p,j) → infinity,
```

where Q is a nonempty subset of S, d is fixed, and gcd(d,∏_(p∈Q)p)=1.
Put D=∏_(p∈Q)(p−1). Multiplicativity yields

```text
σ(d) ∏_(p∈Q)(p x_(p,j) − 1)
  − Dd ∏_(p∈Q) x_(p,j) − Dm_j = 0.                    (1)
```

Expand and combine the two full-product terms. The constant term is
c=(−1)^|Q| σ(d), which is nonzero. The full-product coefficient is

```text
σ(d) ∏_(p∈Q)p − d ∏_(p∈Q)(p−1) > 0.
```

Every other monomial has a fixed nonzero coefficient. Thus every term of (1)
other than c tends to infinity in absolute value: it is either a nonempty
monomial in the x_(p,j), or −Dm_j. All terms are signed units for one fixed
finite prime set P, obtained by adjoining the prime factors of the fixed
coefficients to S.

For each j select an inclusion-minimal zero subsum of (1) containing c.
It has no proper nonempty zero subsum: one containing c contradicts
minimality, and one not containing c could be removed to get a smaller
zero subsum still containing c. Only finitely many term-index sets exist,
so one choice occurs on an infinite subsequence.

Divide its other terms by −c. They sum to 1 with no vanishing subsum, so the
S-unit theorem permits only finitely many tuples. But every coordinate tends
to infinity in absolute value. This contradiction proves finiteness. ∎

## 3. What the theorem does, and does not, buy

An orbit whose positive tail uses only a fixed finite set of primes must
terminate or eventually cycle. Otherwise all its distinct tail terms would
belong to the finite set in Proposition K.

More precisely, put P⁺(a) for the largest prime factor of a>1. Every hypothetical
escaping aliquot orbit n_j must satisfy

```text
P⁺(n_j n_(j+1)) → infinity.
```

For each fixed B, Proposition K leaves only finitely many possible adjacent
pairs whose endpoints both have prime factors at most B. A nonperiodic orbit
cannot repeat their starting terms. Eventually every adjacent pair therefore
contains a prime exceeding B.

This does **not** assert P⁺(n_j)→infinity term by term, an effective numerical
bound for the finite set, or a contradiction to escape. Continuously changing
prime support is compatible with everything proved here.

In fact, after Proposition K, bounding the primes along each orbit is
equivalent to bounding that orbit. Calling that bound the next lemma would
not make it an easier established route to the conjecture.

Two tempting shortcuts still fail:

- **Large primes do not force a decrease.** For any prime p>3,
  s(6p)=6p+12>6p. This is one-step growth, not a divergent orbit.
- **Primitive divisors of σ(n) do not automatically enter the successor.**
  If q|σ(n) and q∤n, then s(n)≡−n≢0 (mod q). Such a prime is specifically
  absent from s(n). A primitive-divisor theorem cannot be transferred through
  subtraction without a new argument.

The difference from the earlier local notes is real but limited: Proposition K
restricts every possible escaping orbit, with no fixed core. It does not supply
a decreasing height, an explicit escaping seed, or a closed growing return
class. **No elegant resolution has been found.**

## 4. Sources and review status

The broader [literature audit](LITERATURE.md) identifies an explicit related
predecessor: Pollack (2012), end of section 5, states fixed-prime-support
finiteness for amicable pairs and notes extensions to sociable cycles and
amicable tuples. Those cycle consequences are not new here. His statement
is not the same as arbitrary one-way adjacent-pair finiteness in Proposition K;
an exact earlier statement of that proposition remains unlocated, not ruled
out. The audit also records older S-unit machinery, the Pollack erratum, and
hypotheses that prevent transferring related results automatically.

1. P. Erdős, [*On Asymptotic Properties of Aliquot Sequences*](https://www.renyi.hu/~p_erdos/1976-22.pdf),
   *Mathematics of Computation* 30 (1976), 641–645. The opening pages reproduce
   Lenstra's finite increasing-chain argument. That argument, not a novel
   construction here, supplies the benchmark in section 1.
2. J.-H. Evertse, H. P. Schlickewei, and W. M. Schmidt,
   [*Linear equations in variables which lie in a multiplicative group*](https://pub.math.leidenuniv.nl/~evertsejh/00-equation.pdf),
   *Annals of Mathematics* 155 (2002), 807–836, Theorem 1.1. The linked author
   manuscript's theorem statement and nondegeneracy definition were consulted.
   The application to adjacent aliquot pairs is proved above; its historical
   novelty has not been established by the focused literature search.

Two fresh read-only AI analyses agreed on the S-unit deduction and on the
absence of a solution. This is not human peer review or formal verification.
No new census, factorization run, or software feature is needed for the proof.
The existing software tests check the implementation, not the S-unit theorem
or the universal mathematical deduction.
