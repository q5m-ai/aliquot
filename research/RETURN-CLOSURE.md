# 15. Trying to close the return condition: finite relays are not renewal

**Outcome:** no closed increasing-return class, contradiction, or escaping
aliquot orbit was obtained. This follow-up makes a stronger, scoped deduction:
**in every reduced congruence refinement of the prime-entry recovery family,
one can force an arbitrarily long finite excursion through multiples of 160,
with no return to the original deficient entry class during that excursion.**
The starting prime depends on the requested duration. The proof does not give
one seed whose excursion lasts forever.

The construction exposes a particular obstacle to closure. A finite chain of
unitary prime factors can preserve the required divisibility for a prescribed
number of steps. The argument consumes one level of its guaranteed supply at
each step. Its strict prime-square supply rule cannot form a finite cycle.
A separate construction does force one genuinely fresh replacement supplier,
but loses the prime-cofactor hypothesis used to construct it. We have not
proved indefinitely repeated replacement.

This extends the attempt in [note 14](MAXIMUM-CONTRADICTION.md), using the
existing recovery inequality and CRT/Dirichlet supply-insertion method from
[notes 07](RECOVERY.md) and [10](PARITY-HANDOFF.md). It does not claim historical
novelty. Written deductions, finite arithmetic checks, and conjectural closure
are kept separate. As usual, s(n) = sigma(n) - n for positive n; stop at zero.

## 1. The exact class to be repaired

The composite entry class already defined in note 07 is

\[
 X_0=\{4u:u>1\text{ odd},\quad7\sigma(u)<8u,\quad
                       \sigma(u)\equiv92u\pmod{160}\}.
\]

Equivalently, these are the deficient positive integers n with v2(n) = 2
and 160 dividing s(n). For n = 4u in this class,

\[
 m=s(n)=7\sigma(u)-4u=3u+7s(u)<n,\qquad160\mid m.
\]

Scaling proper divisors gives s(m)/m >= s(160)/160 = 109/80. Since u > 1,

\[
 s^2(n)\ge\frac{109}{80}(3u+7s(u))
            >\frac{327}{320}n>n.                       \tag{1}
\]

The desired missing step was to ensure a later, larger return to X0, not merely
(1). The full class fails that property: 844 belongs to X0, but its terminating
orbit has no later larger member of X0, as verified in note 14. A successful
repair must select a smaller class or admit other phases.

### A factorization restriction hidden in the entry condition

Every 4u in X0 satisfies

\[
 \gcd(u,105)=1,\qquad v_2(\sigma(u))=2.                 \tag{2}
\]

**Proof.** A factor 3, 5, or 7 in u would give respectively
sigma(u)/u >= 4/3, 6/5, or 8/7, contradicting the strict deficiency inequality.
Also 7 sigma(u) = 4u modulo 160. Since u is odd and 32 divides 160, the right
side has 2-adic valuation exactly 2, which forces the same valuation on
sigma(u). ∎

For an odd prime p with odd exponent e, the exact formula from note 02 is

\[
 v_2(\sigma(p^e))=v_2(p+1)+v_2(e+1)-1.
\]

Even exponents contribute zero. Thus u has at most two prime factors with odd
exponents. More precisely, ignoring the even exponents:

- One odd exponent e at p requires either p = 3 modulo 8 and e = 1 modulo 4,
  or p = 1 modulo 4 and e = 3 modulo 8.
- Two odd exponents require both primes to be 1 modulo 4 and both exponents
  to be 1 modulo 4.

These are necessary shape restrictions, not sufficient entry or renewal
conditions. For the clean bridge m = 160v with gcd(v,160) = 1, returning to
v2(s(m)) = 2 further requires v2(sigma(v)) = 1. This is equivalent to
v = p^(4a+1) z^2 with p prime, p = 1 modulo 4, and gcd(p,z) = 1. In particular,
a squarefree clean bridge satisfying this condition must be prime.

### Actual renewal is possible once

A small search must not be mistaken for a proof that no two-step renewal
exists. There is a genuine one:

```text
7700684 -> 5775520 -> 7869524 -> 6961600 -> 11148600.
```

Both 7700684 and 7869524 belong to X0. Their respective odd cofactors are
1925171 (prime) and 1967381 = 13 * 151337. The second checkpoint renews the
**full** input condition, not only its shape. Both recovery blocks grow.

But the next checkpoint 11148600 has v2 = 3, so it leaves X0. This finite
prefix establishes neither termination nor escape. It shows that the repair
is not vacuous and that one successful renewal still does not close it.

## 2. A stronger attempt: prearrange a chain of suppliers

Here q || m means that the prime q divides m to exponent exactly one. Such a
factor is unitary, so q + 1 divides sigma(m).

**Valuation retention.** If v_l(m) = e and l^(e+1) divides sigma(m), then
v_l(s(m)) = e, provided s(m) > 0. This is unequal-valuation subtraction.

One supplier can therefore preserve several prescribed exponents. A chain of
suppliers can preserve them for several steps, while lower-level suppliers
remain available. This gives an actual finite-horizon construction rather
than merely a density heuristic.

### Theorem: arbitrary finite bridge persistence in every prime progression

Fix a reduced progression p = a modulo K, where 160 divides K and a = 51
modulo 160. There exist integers alpha >= 5 and beta >= 1 such that, for every
H >= 1, infinitely many primes p in that progression satisfy the following
conditions. For

\[
 n_0=4p,\qquad n_j=s^j(4p),
\]

all the first H successors satisfy

\[
 v_2(n_j)=\alpha,\qquad v_5(n_j)=\beta
                       \quad(1\le j\le H).              \tag{3}
\]

Consequently each is a multiple of 160 and is outside X0. The first step
decreases, but the subsequent certified steps grow:

\[
 n_1=3p+7<n_0,\qquad
 n_j\ge\left(\frac{109}{80}\right)^{j-1}(3p+7)
    >\frac34\left(\frac{109}{80}\right)^{j-1}n_0
                       \quad(1\le j\le H).              \tag{4}
\]

The last certified term is abundant too, so its successor also grows, even
though (3) need not hold at that successor.

**Proof.** Dirichlet supplies a prime p0 in the given progression. Set

\[
 \alpha=v_2(3p_0+7),\qquad\beta=v_5(3p_0+7),\qquad
 K'=\operatorname{lcm}(K,2^{\alpha+1},5^{\beta+1}).
\]

Refine to the residue of p0 modulo K'. This remains reduced: the only newly
introduced prime divisors of the modulus are 2 and 5, neither dividing p0.
It fixes those two exponents of 3p + 7 for every prime in the refinement.
Write D = 2^(alpha+1) 5^(beta+1).

For j = 1, ..., H-1 choose distinct primes r_j satisfying

\[
 r_j\equiv-1\pmod{D\prod_{i<j}r_i^2},\qquad
 r_j\nmid21K'.                                         \tag{5}
\]

Each progression in (5) is reduced. Dirichlet permits each successive choice
while avoiding finitely many excluded primes. There are only finitely many
choices because H was fixed first.

Now impose, in addition to the refined progression for p,

\[
 3p+7\equiv r_j\pmod{r_j^2}
                         \quad(1\le j\le H-1).         \tag{6}
\]

The residue for p exists because r_j is not 3, and it is nonzero modulo r_j
because r_j is not 7. The moduli r_j^2 are pairwise coprime and coprime to K'.
CRT therefore gives a reduced progression. Dirichlet supplies infinitely many
prime p in it. No simultaneous-prime assertion about successive orbit values
is used.

Put m = 3p + 7. It has exact core exponents alpha, beta and r_j || m for every
j. We prove inductively that at s^t(m), for 0 <= t <= H-1, the same core
exponents persist and

\[
 r_i\Vert s^t(m)\qquad(1\le i\le H-1-t).                \tag{7}
\]

At t = 0 this is the construction. If t < H-1, let j = H-1-t. The highest
remaining certified supplier r_j (by index) is unitary in the current term. Its plus-one
is divisible by D and every r_i^2 for i < j. Hence the divisor sum of the
current term has strictly larger valuations than the term at 2, 5, and all
those lower suppliers. Valuation retention proves (7) at t+1. We no longer
claim anything about the exponent of r_j itself.

Every current term is a positive multiple of 160, so its aliquot sum is at
least 109/80 times that term. Thus all inductive steps are defined and positive.
This completes (3), and multiplication of these growth inequalities gives
(4). ∎

### What this does and does not exclude

For every fixed H, every such prime progression has infinitely many entries
that do **not** return to X0 during their first H steps. Therefore a finite
congruence refinement cannot give a uniformly bounded return time to X0.
The H = 2 case already rules out a universal two-step repair, while producing
an abundant rebound that itself has another growing successor.

This is not a prohibition on unbounded return times, a factorization-dependent
subclass that omits the forced entries, composite-only input classes, or a
larger return class allowing abundant phases. Nor does it establish the fate
of the constructed orbits after their certified finite excursion.

The quantifiers are essential: choose H, then the suppliers and a suitable
prime progression. Choosing a new p after increasing H changes the seed.
The same issue prevents using this theorem against the finite maximum of a
previously fixed cohort. In this particular construction,

\[
 3p+7\ge160\prod_{j=1}^{H-1}r_j\ge160\cdot11^{H-1},
\]

because every supplier avoids 2, 3, 5, and 7. Thus arbitrarily long preloaded
certificates require unbounded seeds even with alpha and beta held fixed.
This is a bound on this certificate construction, not on actual orbit lengths.

A modest exact illustration of the H = 2 retention mechanism is

```text
11261644 -> 8446240 -> 13326560,
11261644 = 4 * 2815411,
8446240  = 2^5 * 5 * 11 * 4799,
4799 + 1 = 4800 = 2^6 * 3 * 5^2.
```

The entry cofactor 2815411 is prime and is 51 modulo 160. Both successors
have exact valuations v2 = 5 and v5 = 1. This is a finite illustration of the
supplier mechanism, not a computed infinite orbit.

## 3. Can the finite relay be closed into an infinite one?

The construction keeps a fixed finite core and discards one level of its
*certified* supplier list at each step. It does not prove that the discarded
prime vanishes; it simply supplies no invariant controlling it thereafter.

A tempting fix is to arrange the same suppliers in a cycle. That fails for
this strict prime-square relay rule. If odd primes P and Q satisfy

\[
 P^2\mid Q+1,
\]

then Q >= P^2 - 1 > P. Every relay edge goes from a larger supplying prime to
a smaller recipient. No finite directed cycle can satisfy that rule. An
infinite preloaded chain would require infinitely many distinct prime factors
in the starting integer, which is impossible.

This is a limitation of the **specified sufficient relay certificate**, not
of all supplier networks or all orbits. An actual orbit may generate new
suppliers; factors can also contribute jointly, have other exponents, or use
other core phases. None of those alternatives has been shown to renew
indefinitely here.

The need for replenishment is visible in a small actual relay:

```text
767840 = 160 * 4799
       -> 1046560 = 160 * 31 * 211
       -> 1517792 = 32 * 47431.
```

The factor 4799 supplies a successful step retaining the whole 160-core. But
sigma(31 * 211) = 6784 is not divisible by 5. The next step loses 5 and the
160-core. Both steps grow; growth alone does not replenish the supplier.

Nor can primitive prime divisors of sigma(m) be treated as new factors of the
successor. If a prime r divides sigma(m) but not m, then
s(m) = -m modulo r is nonzero. To replenish from a genuinely new prime, one
must control a factor of **sigma(m) - m**, not simply one of sigma(m).

No rule forcing such a replacement at every future stage was obtained.

### A genuinely fresh supplier can be forced once

We also tried a larger class that stays in the abundant bridge phase:

\[
 Z=\{160u:u\ge1,\quad\gcd(u,10)=1,\quad800\mid\sigma(u)\}.
\]

For a member of Z, sigma(160u) = 378 sigma(u) has 2-adic valuation at least 6
and 5-adic valuation at least 2. Subtracting 160u preserves the exact exponents
(5,1), so its successor is another clean 160-core and is larger. To remain in
Z, however, the successor's odd cofactor must again have divisor sum divisible
by 800. The example 767840 above shows that this additional condition need
not persist.

**Fresh-handoff lemma.** There are infinitely many prime q for which 160q
belongs to Z and s(160q) belongs to Z, with the latter membership supplied by
a prime factor not present in 160q.

**Proof.** Choose a prime r = -1 modulo 800 with r not dividing
160 * 218 * 378. Such primes exist by Dirichlet. Impose

\[
 q\equiv-1\pmod{800},\qquad
 218q+378\equiv r\pmod{r^2}.
\]

The second condition is a reduced residue for q modulo r^2: 218 is invertible,
and q = -378 / 218 modulo r is nonzero. Its modulus is coprime to 800. CRT
and Dirichlet therefore give infinitely many prime q satisfying both conditions.

Since q + 1 is divisible by 800, the source is in Z. Write q = 800t - 1. Its
actual successor is

\[
 s(160q)=218q+378=160(1090t+1).
\]

The new cofactor u' = 1090t + 1 is coprime to 10. Also r || s(160q), hence
r || u'. This prime is genuinely fresh: r divides neither 160 nor q. Thus
r + 1 divides sigma(u'), and 800 divides sigma(u'). The successor belongs to
Z and guarantees a further growing, core-retaining step. ∎

This is a positive handoff, not merely a preloaded supplier remaining present.
But the proof cannot be reapplied automatically. We have u' = 1 modulo 10,
whereas the prime entry q is -1 modulo 10. More strongly, since r = -1 modulo
10 and u' = rv, the quotient v is -1 modulo 10 and is at least 9. Thus u' is
necessarily composite. Its divisor sum is not given by the prime formula
u' + 1; the residual factorization and its next image need new control.

A checked instance, with r = 2399 and prime q = 13753372799, is

```text
2200539647840 -> 2998235270560 -> 4098260524640.
```

Their clean-160 cofactors are respectively

```text
13753372799                         (prime),
18738970441 = 743 * 2399 * 10513,
25614128279                         (prime).
```

The first two divisor sums are divisible by 800. The third is
25614128280 = 280 modulo 800, so the third term is outside Z, although it still
has the 160-core. No eventual fate or absence of a later return is inferred.
This exhibits the exact gap in trying to repeat the fresh handoff: the full
renewed condition survives once but not at the next checkpoint in this example.

## 4. A different bridge: smaller growth requirement, another renewal failure

As a separate repair, replace 160 by 12. Define

\[
 Y=\{4u:u>1\text{ odd},\quad7\sigma(u)<8u,\quad
                         \sigma(u)\equiv4u\pmod{12}\}.
\]

Its members have m = s(4u) divisible by 12 and m < 4u. Since s(12)/12 = 4/3,

\[
 s^2(4u)\ge\frac43(3u+7s(u))=4u+\frac{28}{3}s(u)>4u.
\]

The recovery inequality works. There are infinitely many entries: if p is
prime and p = 31 modulo 36, then u = 13p satisfies the conditions, and

\[
 s(52p)=46p+98=12v,\qquad v=(23p+49)/6\equiv1\pmod6.
\]

Dirichlet supplies the primes; p >= 31 makes the deficiency inequality hold.

**But a clean prime bridge cannot return to Y in two steps.** Every member
4u of Y has u = sigma(u) = 1 modulo 3. Deficiency excludes 3 dividing u. If
u were 2 modulo 3, a prime 2 modulo 3 would occur to an odd exponent and
force sigma(u) = 0 modulo 3, contradicting the defining congruence.

Now suppose m = 12v with v > 3 prime. Then

\[
 s(m)=4w,\qquad w=4v+7.
\]

If v = 1 modulo 3, then w = 2 modulo 3 and sigma(w) = 0 modulo 3, so the
next entry congruence fails. If v = 2 modulo 3, then 3 divides w and 4w is
abundant, so the entry deficiency fails. Both cases exclude renewal. ∎

The entry p = 31 gives a complete counterexample even to a larger *later*
return for the full class Y:

```text
1612 -> 1524 -> 2060 -> 2308 -> 1738 -> 1142 -> 574
     -> 434 -> 334 -> 170 -> 154 -> 134 -> 70 -> 74
     -> 40 -> 50 -> 43 -> 1 -> 0.
```

No later value larger than 1612 belongs to Y. The bridge replacement therefore
repairs growth but not closure; it would need another, genuinely invariant
restriction or a larger phase system.

## 5. Stopping point and independent checks

The initial two-step wrong-phase theorem was obtained independently by both
read-only committee analyses and by the parent. The finite-relay extension is
written out above rather than inferred from that agreement. The alternatives
considered were the 12-bridge and a conditional six-core growth bound. Neither
provided an indefinitely repeatable mechanism; faster growth conditional on
survival does not prove survival. AI agreement is not human peer review or formal verification.

The unresolved step is now particularly concrete: **replace the finite,
prearranged supply chain by an actual, indefinitely replenished factorization
mechanism**, or prove that another explicitly specified return class closes.
The existing constructions do not do that. We therefore cannot close the
contradiction or claim a disproof of universal boundedness.

[`tests/test_return_closure.py`](../tests/test_return_closure.py) independently
checks the named divisor sums, full X0 renewal once, subsequent guard loss,
entry shape restrictions, the finite relay and CRT premises, the fresh handoff,
and the terminating 12-bridge example. Ordinary orbit sources are at most
30000000; the separately labelled fresh-handoff fixture has a source cap of
5000000000000. A separate modular certificate checks supplier primes 4799 and
110545924799, the latter satisfying r2 + 1 = 3 * 1600 * 4799^2. Its CRT residue is **not asserted prime**
or iterated; prime parameters in that progression come from the written
Dirichlet argument. No probable-prime shortcut or unbounded search is used.

Reproduce the focused checks with

```sh
python3 -m unittest discover -s tests -p 'test_return_closure.py' -v
```

All eleven focused tests passed. Both `python3 -m unittest discover -s tests -v`
and `npm test` passed all 305 tests. The required `node --check` commands passed
for `site/explorer.js`, `site/math.js`, and `site/latex.js`. These results verify
finite arithmetic and repository regressions, not the conjecture or novelty.
