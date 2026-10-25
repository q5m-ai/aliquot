# Research note 08: coalescence descent — an attempt and its stopping point

**Status:** no proof or disproof of the aliquot conjecture. The network approach
suggests a legitimate induction target, but no universal merger mechanism has
been found. A concrete smaller-predecessor construction fails on an infinite
prime progression. The proposed **one-step, finite-core, prime-cofactor covering
strategy cannot be universal**. Even unrestricted one-step shared-successor
coverage fails for infinitely many abundant sources. The argument below
uses the Chinese remainder theorem and Dirichlet's theorem; historical novelty
is unreviewed. This is a reason to stop this route for input, not to accumulate
more restricted lemmas or larger pictures.

Throughout, s(n)=sigma(n)-n for positive n; s(1)=0 and s(0) is undefined.
Iterates are used only when defined. An escaping orbit is nonterminating and
nonperiodic, hence has distinct positive terms and tends to infinity.

## 1. The actual proof target: a smaller representative

Say m and n **coalesce** if s^a(n)=s^b(m) for some nonnegative integers a,b.
The offsets need not agree. Determinism makes the subsequent futures agree.

A sufficient induction scheme is to prove, for every positive n, either:

1. its future terminates or enters a cycle; or
2. it coalesces with some positive m<n.

If the alternatives are established arithmetically for all n, strong induction
settles all seeds. This is a proof obligation, not an established covering
result. Defining a class by successful future coalescence would not prove it.

For example,

```text
56 --------> 64 -> 63 -> 41 -> 1 -> 0
48 -> 76 ---^
```

certifies a merger with a smaller seed before 56 has decreased below its
starting value. It illustrates the additional flexibility over direct descent.

If escaping seeds exist, take the least one N. Then s(N)>N, and **no point
in N's entire coalescence component is smaller than N**: such a point would
itself escape. In particular N has no smaller predecessor, but larger
predecessors are allowed. It need not be untouchable.

Contracting all actual directed cycles gives a functional DAG. Its reachability
order has finite intervals, but it can still have infinite forward rays.
Excluding those rays is the conjecture itself. State recurrence is not backward
causation, and an infinite reverse path is not an escaping forward orbit.
These observations prevent treating the causal-set reformulation as the missing
arithmetic argument.

## 2. A concrete merger attempt, and an infinite family where it fails

For a prime p>3,

```text
s(6p) = 6p+12.
```

Try to replace 6p by a smaller predecessor 18q of the same successor. If q is
prime and coprime to 18, then

```text
s(18q) = 21q+39,
q = (2p-9)/7,
6p-18q = (6p+162)/7 > 0.
```

This gives genuine smaller-seed certificates, for example

```text
174 -> 186 <- 126       (p=29, q=7)
258 -> 270 <- 198       (p=43, q=11).
```

But integrality is not enough. At p=127 the proposed q is 35, and

```text
762 -> 774,
630 -> 1242,            not 774.
```

For any positive q coprime to 18, the exact correction is

```text
s(18q) = 21q+39 + 39[s(q)-1].
```

Thus a composite q>1 destroys the asserted equality, rather than providing
another valid predecessor.

More generally, allowing a composite cofactor u coprime to a core d requires
solving the nonlinear inverse equation

```text
s(d)u + sigma(d)s(u) = s(Cp),       du < Cp.
```

A larger divisor sum can make a *possible* predecessor smaller, but it does not
ensure that the exact target has such a predecessor. The arithmetic function
has gaps; there is no intermediate-value argument supplying a solution.

This failure is not a lone numerical exception. Take primes

```text
p = 22+35t > 22.
```

Dirichlet's theorem supplies infinitely many, since gcd(22,35)=1. Then
q=5+10t is an integer greater than 5 and divisible by 5. For these primes
p>3, q is odd and q is not divisible by 3, so the displayed correction applies.
Every one of these candidates fails this merger template. This does **not**
exclude a different predecessor or a later merger for the same seed.

## 3. Why adding finitely many prime-cofactor templates cannot repair it

**Finite-palette obstruction.** Fix C>=2 and a finite set D of positive integer
cores d>=2. There are infinitely many primes p coprime to C such that no
**distinct** number dq, with d in D, q prime and gcd(d,q)=1, satisfies

```text
s(dq) = s(Cp).
```

In particular, taking C=6 rules out covering every abundant seed 6p by smaller
shared-successor predecessors from any fixed finite palette of these templates.
The conclusion excludes even larger distinct predecessors within the palette.
It concerns one-step shared successors, not arbitrary multistep coalescence.
The quantifiers are: each fixed finite palette has infinitely many misses,
not that one source misses every possible core.

**Proof.** Write

```text
a = s(C) > 0,
b_d = s(d) > 0,
beta_d = sigma(C)-sigma(d).
```

The coprime prime-cofactor identities turn a collision into

```text
a p + beta_d = b_d q.                                  (1)
```

If d=C, equation (1) forces q=p, giving the same starting number, not a
reduction. Set this case aside.

For each d with beta_d != 0, choose a different prime ell_d not dividing
`a b_d beta_d`. Impose

```text
p = -beta_d / a  (mod ell_d).
```

The division means a modular inverse. Each residue is nonzero. The Chinese
remainder theorem combines these conditions into one reduced residue class;
Dirichlet's theorem gives arbitrarily large primes p in it. If (1) has an
integer q, then ell_d divides q, because ell_d does not divide b_d. Taking p
large enough makes q>ell_d, so q is composite.

For a remaining d with beta_d=0 and d!=C, we have a!=b_d, since sigma(C)=sigma(d)
while C!=d. Reduce a/b_d to coprime positive integers A/B. Equation (1) becomes
q=A p/B. For primes p>B, integrality forces B=1; primality of q then forces
A=1. This contradicts a!=b_d. Only finitely many small exceptional p remain.

Choose p above all these finitely many bounds and above C. Then p is coprime
to C, and every nontrivial collision in the palette is excluded. If there
were no nonzero beta_d conditions, arbitrarily large primes suffice without
CRT. This proves the assertion. ∎

The scope matters: this does **not** exclude unbounded cores, general composite
cofactors, alternative representations outside the palette, or multistep
mergers. It does show that this particular proposed universal cover cannot
be obtained merely by adding a few more prime-cofactor cases.

## 4. Unrestricted one-step coverage also fails

Allowing all cores and composite cofactors does not make a smaller
shared-successor predecessor exist for every abundant source.

For each positive integer t, let r_t be the **earliest** maximizer of s(m)
on 1 <= m <= 12t. The five distinct proper divisors
`t, 2t, 3t, 4t, 6t` of 12t sum to 16t. Consequently

```text
s(r_t) >= s(12t) >= 16t > 12t >= r_t.
```

Thus r_t is abundant. Its earliest-maximizer property gives
`s(m) < s(r_t)` for every m<r_t, so it has no smaller shared-successor
predecessor at all. The values r_t are unbounded because their divisor sums
are unbounded. Hence infinitely many abundant sources obstruct blanket
one-step coverage, with no factorization restriction.

This does **not** prove that any such record escapes, or that all such records
resolve. They may have smaller direct predecessors, merge at different offsets
or later, terminate, or cycle. A complete coalescence proof must actually
handle those additional dynamical possibilities rather than assuming one-step
coverage of all sufficiently large abundant numbers.

## 5. The unresolved step, stated without geometric camouflage

Under the least-counterexample hypothesis, define

```text
B_N = union of the forward-orbit value sets of 1 <= m < N.
```

Every smaller seed terminates or cycles, so B_N is a finite set. To contradict
escape of N through coalescence, we must force N's orbit to meet B_N. Nothing
in the functional-graph or causal-set axioms forces that meeting. A reverse
branch smaller than a later term n_k is insufficient: its representative must
be below the original N, not merely below n_k.

[Proposition K](GLOBAL.md) says an escaping orbit must have
P+(n_k n_(k+1)) tending to infinity. In prime-exponent geometry, only finitely
many edges fit wholly inside a prescribed finite set of prime axes. That is
compatible with an infinite ray which avoids B_N and keeps using larger primes;
it does not furnish a decreasing height or a merger. Likewise, defining a
height as distance to a terminal component assumes that the component is
reachable, which is exactly what needs proof.

The missing input is therefore an **arithmetic mechanism forcing a merger or
other well-founded descent despite unrestricted changing factorization**.
The concrete finite-palette strategy above cannot supply it. No such mechanism,
and no explicit forward-invariant escaping class, has been established here.

**Stop here for input.** Further finite merger counts, graph layouts, or
variants of the same prime-cofactor obstruction would not discharge this
obligation. This is a genuine block in this attempt, not evidence that a
network method cannot ever work or that the conjecture has either truth value.

## 6. Verification boundary

`tests/test_coalescence.py` checks the named paths and collisions with exact
factorization and independent divisor-pair enumeration. It also checks the
composite correction on bounded inputs, finite examples of the CRT
obstruction including its zero-constant case, and the record construction for
1 <= t <= 100. Every numerical bound is stated in the tests. No computation is
a premise for Dirichlet's theorem or either universal obstruction argument.

```sh
python3 -m unittest discover -s tests -p test_coalescence.py -v
```

Two independent read-only Astra/max analyses agreed on the finite-palette
argument and the stopping point. Both found an unrestricted one-step record
obstruction; section 4 uses the direct aliquot-record argument. Their analyses
are not human peer review or proof-assistant formalization.

The written arguments, not passing software tests, carry the universal claims.
There is no claim of a divergent seed, resolution, or historical novelty.
