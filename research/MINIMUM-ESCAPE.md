# 14. Least-seed contradiction attempt: prime deletion and finite recharge

**Outcome:** a substantive attempted contradiction, with an exact arithmetic
obstruction at its transport step—not a proof or disproof of the aliquot
conjecture. Deleting a prime really does give a smaller, resolved companion at
a least escaping seed. But literal divisor companionship almost always breaks
immediately, and a fixed resolved companion can accompany arbitrarily long,
arbitrarily amplified **finite** growth. Two proposed valuation-budget repairs
also admit unbounded replenishment. No escaping orbit, historical novelty,
human peer review, or formal verification is claimed.

The finite-growth construction adapts Lenstra's existing supplier-chain
argument, then uses CRT and Dirichlet to put its entry into a preselected
prime-cofactor family. Its ingredients and limitations are explicit below.

## 1. Use minimality at the initial seed, where it is strongest

For positive n, write s(n)=sigma(n)-n and stop at zero; s(0) is undefined.
Assume escaping seeds exist, and choose the least one N over **all** seeds.
Its orbit a_0=N, a_(j+1)=s(a_j) has distinct positive terms, all a_j>N for j>0,
and tends to infinity. Thus N is abundant.

For every prime p dividing N, the seed b=N/p is smaller and therefore
terminates or eventually cycles. Its orbit is bounded. This gives an actual
smaller companion, not merely a request to find a descent later.

The attempted proof is:

1. Delete a prime from N to obtain the bounded companion.
2. Relate the two actual aliquot orbits exactly.
3. Transport the companion's boundedness through that relation.
4. Contradict escape of N.

Deleting from a later term would not give the same premise: its quotient
need not be below N. The argument here deliberately uses the initial seed.

The S-unit result in [GLOBAL.md](GLOBAL.md) supplies another constraint:
P+(a_j a_(j+1)) tends to infinity. These are prime **factors**, not prime
terms. We test whether their replacement can be charged to the companion or
to a finite valuation budget, rather than assuming it causes descent.

## 2. Exact prime deletion and a complete divisibility classification

Write n=p^e d with p prime, e>=1, and p not dividing d; put b=n/p. Since
sigma(p^e)=p*sigma(p^(e-1))+1, multiplicativity gives

\[
 \boxed{s(n)=p\,s(b)+\sigma(d).}                       \tag{1}
\]

The correction is sigma(d), **not generally sigma(b)**. In particular,
s(n)=sigma(d) modulo p. If p does not divide sigma(d), the entire p-power
in n disappears from its successor. The numerical correction remains positive.

### Proposition: when does the divisor companion survive one step?

For an abundant n and a prime p dividing n,

\[
 s(n/p)\mid s(n)
 \quad\Longleftrightarrow\quad
 v_p(n)=1\text{ and }n/p\text{ is perfect}.            \tag{2}
\]

**Proof.** In (1), divisibility is equivalent to s(b)|sigma(d).

If e>=2, abundance rules out d=1, since prime powers are deficient. Therefore
s(d)>0 and

\[
 s(b)=p^{e-1}s(d)+(1+p+\cdots+p^{e-2})\sigma(d)
      >\sigma(d).
\]

If e=1, divisibility is equivalent to s(d)|sigma(d), hence to s(d)|d. For
d>1 this last property holds only when d is prime or perfect: s(d)>d cannot
divide d, and if 1<s(d)<d divided d, then s(d) and 1 would be distinct proper
divisors of d whose sum already exceeds s(d). The case s(d)=1 is primality.
But a product of two distinct primes is never abundant. The perfect case
works directly. QED.

Thus at a least escaping seed, **every literal prime-deleted divisor companion
breaks immediately except deletion down to a perfect core**. This does not
exclude other comparisons; it identifies the exact exception to this one.
For a unitary prime factor, a useful exact overlap formula is

\[
 \gcd(s(Dp),s(D))=\gcd(D,s(D)),\qquad p\nmid D.        \tag{3}
\]

It follows by subtracting p*s(D) and using sigma(D)=D+s(D).

## 3. Try to transport a controlled additive error instead

For a unitary input Dp, let a_j=s^j(Dp), b_j=s^j(D), and
E_j=a_j-p*b_j, while these iterates exist. Put A=s(D), B=sigma(D). Then

\[
 E_0=0,\quad E_1=B,\qquad
 E_{j+1}=\sigma(pb_j+E_j)-p\sigma(b_j)-E_j,            \tag{4}
\]

where the recurrence is used only when both current arguments are positive.
In particular

\[
 E_2=\sigma(pA+B)-p\sigma(A)-B.
\]

The first factorization relation has been lost. Even the sign of the error
need not be preserved. The fixed terminating companion is

\[
 12\to16\to15\to9\to4\to3\to1\to0.
\]

Its scaled first terms are 12p,16p,15p, whereas actual paths include

| p | Actual first three terms | E_1 | E_2 |
| --- | --- | --- | --- |
| 13 | 156 → 236 → 184 | 28 | −11 |
| 17 | 204 → 300 → 568 | 28 | 313 |
| 19 | 228 → 332 → 256 | 28 | −29 |

A single sign change is not the main obstruction. We next test whether there
is at least an upper budget of the form E_2<=C(D)*p, or a bound on the growing
prefix depending on the resolved companion. Both uniform proposals fail.

## 4. Embed arbitrarily amplified finite growth above any fixed core

### Fixed-core prime-lifting proposition

Fix an integer D>1, an integer L>=1, a real G>1, and a prime cutoff Y.
There are infinitely many primes p not dividing D such that the actual orbit
from a_0=Dp satisfies

\[
 a_{j+1}>G a_j\qquad(1\le j\le L).                   \tag{5}
\]

The supplying prime powers can all use primes greater than Y and absent from
Dp. If D is abundant or perfect, the initial step a_0 -> a_1 also grows,
though no G-factor is asserted for that initial step.

**Proof.** Write A=s(D)>0, B=sigma(D). The actual first image is

\[
 a_1=Ap+B.                                           \tag{6}
\]

Let q_i enumerate **all** primes greater than Y and not dividing DAB, in
increasing order. Removing finitely many primes preserves the divergence of
the squarefree Euler product, so choose t
with

\[
 \prod_{i=1}^{t}(1+1/q_i)>G+1.
\]

For completeness, the unboundedness of these products follows from
(1+1/q)=(1-1/q^2)/(1-1/q): the first product has a positive limit and Euler's
prime product in the denominator diverges. This is an imported classical
fact, not a numerical assumption about primes in an orbit.

Set h=t+L-1. Start with any positive e_1, and recursively choose

\[
 e_{i+1}=\varphi\bigl(q_i^{e_i+1}(q_{i+1}-1)\bigr)-1.
\]

Euler's theorem applies because q_(i+1) is coprime to the modulus. Dividing
q_(i+1)^(e_(i+1)+1)-1 by q_(i+1)-1 gives

\[
 q_i^{e_i+1}\mid\sigma(q_{i+1}^{e_{i+1}}).             \tag{7}
\]

Let C_l be the positive integers with exact valuations v_(q_i)(x)=e_i for
i<=l. If x is in C_l and i<l, its whole q_(i+1)-power is a unitary factor
and supplies v_(q_i)(sigma(x))>=e_i+1. Since v_(q_i)(x)=e_i, subtraction gives
v_(q_i)(s(x))=e_i. Therefore

\[
 s(C_l)\subseteq C_{l-1}\quad(l\ge1).                \tag{8}
\]

Only these positive-source classes are used; no iteration at zero is taken.
Every x in C_l with l>=t also satisfies

\[
 \frac{\sigma(x)}x
 \ge\prod_{i=1}^{t}\frac{\sigma(q_i^{e_i})}{q_i^{e_i}}
 \ge\prod_{i=1}^{t}(1+1/q_i)>G+1,
\]

so s(x)>Gx. This is Lenstra's finite supplier-chain mechanism with a chosen
gain, not a new infinite-growth mechanism; see [GLOBAL.md](GLOBAL.md) and
[the amplified construction](approaches/small-gain-feedback/REPORT.md).

Now force the *actual* first image (6) into C_h by imposing

\[
 Ap+B\equiv q_i^{e_i}\pmod{q_i^{e_i+1}}
 \qquad(i\le h).                                    \tag{9}
\]

Each congruence determines a class for p. Modulo q_i that class is
-BA^(-1), nonzero because q_i divides neither A nor B. The Chinese remainder
theorem combines these into a **reduced** progression. **Dirichlet's theorem**
supplies infinitely many prime p in it; discard the finitely many dividing D.
No simultaneous-primality assertion is used.

Thus a_1 lies in C_h, and a_1,...,a_L retain at least the first t prescribed
powers by (8). This proves (5). Each q_i is absent from Dp: it does not divide
D, and the nonzero residue of p modulo q_i also excludes p=q_i.
Finally, a_1-Dp=(s(D)-D)p+sigma(D)>0 when D is abundant or perfect. QED.

## 5. Apply the construction to the proposed contradiction

### 5.1 The companion can terminate while the larger orbit keeps growing

Take D=12. For every prescribed L,G there are infinitely many prime seeds
12p with an initially growing step followed by L steps of gain greater than G.
Yet the companion 12 always terminates after seven transitions, and

\[
 \omega(12p)=3,\qquad \Omega(12p)=4,\qquad\tau(12p)=12
 \quad(p>3).
\]

Thus neither the fixed companion nor these fixed factorization counts supply
a uniform duration budget. In particular

\[
 E_1=28,\qquad \sup_p\frac{E_2}{p}=\infty.             \tag{10}
\]

A sharper version retains a fixed adjacent gcd. In the proof, additionally
impose p=1 modulo 6. This is compatible with the existing moduli, since the
q_i avoid the factors of D=12. For p>12,

\[
 \gcd(12p,16p+28)=4\gcd(3p,4p+7)=4.
\]

For arbitrary epsilon>0 and H>0, choose G>max(1,15H/16), L=1, and then a
sufficiently large prime p in the progression. The result satisfies

\[
 \frac{E_1}{16p}<\varepsilon,\qquad
 \frac{a_2}{15p}>H,\qquad \gcd(a_0,a_1)=4.            \tag{11}
\]

A vanishing relative deletion error can therefore become an arbitrarily large
relative error one step later, despite complete loss of the deleted prime
and a fixed common factor. This refutes the uniform perturbation bound being
tested, not every possible seed-dependent comparison.

### 5.2 The perfect-core exception permits fresh finite recharge too

The literal-companion exception in (2) includes

\[
 6p\to6(p+2),\qquad 6\to6,
\]

with E_1=12 and gcd(6p,6(p+2))=6 for primes p>3. The lifting proposition
applies even here. It can also require that **every** prime factor of p+2
exceed any given Y>=3: choose the q_i>Y and add

\[
 p\equiv-1\pmod{\prod_{\ell\le Y,\ \ell\text{ prime}}\ell}.
\]

These moduli are disjoint from the q_i-power moduli and all classes remain
reduced. Thus the first step loses p, gains only fresh primes above Y, and
increases the value by just 12, while enabling any prescribed finite L,G.
The old prime p is absent from p+2 since p>3.

One can preserve v_2=v_3=1 throughout this finite block as well. Before
building the chain, choose e_1=5. For q_1>3, the six terms of
sigma(q_1^5) sum to zero modulo 3, whether q_1 is 1 or -1 modulo 3.
The first output is clean because
p+2 is coprime to 6. At each of the L growing sources, the retained unitary
q_1-power makes sigma(u) divisible by 3. For a clean source 6u, sigma(6u)
=12*sigma(u) is then divisible by 4 and 9. Subtraction preserves the exact
exponents v_2=v_3=1. The supplier chain guarantees its availability for the
specified finite duration.

**Quantifier boundary:** different L,G,Y may require different, enormous p.
One prime can encode an arbitrarily large *finite* future supply through its
residue classes. No fixed prime is shown to encode inexhaustible supply.
Neither a bound depending on the full numerical seed nor the conjecture is
refuted by this construction.

## 6. Try a valuation-budget repair, including composite intermediates

For n=6u, u>1, gcd(u,6)=1, put

\[
 T(u)=2\sigma(u)-u=u+2+2(s(u)-1),\qquad s(6u)=6T(u).
\]

Every such step grows. Its successor remains clean precisely when 3 does not
divide T(u); oddness is automatic. Leaving that guard is not resolution.
For prime p>3, T(p)=p+2. An all-prime cofactor run cannot persist: p=1 modulo
3 exits immediately, while p=2 modulo 3 followed by another prime exits on
the following step. Composite cofactors add the **positive** correction
2(s(u)-1), so this prime-only exhaustion is not a whole-orbit argument.

Try B(u)=v_3(u+1), which at a prime cofactor measures the divisor-sum supply
of 3. A guarded prime step spends its positive B. But at prime checkpoints
it can rise instead of fall:

\[
 6\cdot683\to6\cdot685\to6\cdot971,
 \qquad B(683)=2,\quad B(971)=5.
\]

Indeed 685=5*137 and T(685)=2*(6*138)-685=971. Both endpoint cofactors are
prime. The smaller block 6*167 -> 6*13^2 -> 6*197 raises B from 1 to 2.
These are finite counterexamples to that rank, not escaping orbits.

At composite cofactors B(u) need not equal the actual supply
C(u)=v_3(sigma(u)). Changing to C does not give a bounded reset rule either.

### Proposition: the tag and actual supply can both reset arbitrarily high

For arbitrary K,L>=1 there are infinitely many prime q such that the actual
clean growing edge u=q^2 -> r=q^2+2q+2 satisfies

\[
 B(u)=0,\quad C(u)=1,\qquad B(r)\ge L,\quad C(r)\ge K. \tag{12}
\]

**Proof.** First lift a root of F(x)=(x+1)^2+2 modulo 3^L. Start at a_1=1
modulo 3. If a_j is a root modulo 3^j, then

\[
 F(a_j+t3^j)\equiv F(a_j)+t3^j\,2(a_j+1)
                   \pmod{3^{j+1}}.
\]

Since 2(a_j+1)=1 modulo 3, exactly one t in {0,1,2} gives the next lift.
Every resulting a_L is 1 modulo 3, hence a reduced residue.

Next choose a prime ell with ell=1 modulo 4 and ell=-1 modulo 3^K, using
CRT and Dirichlet. As ell=1 modulo 4, -1 has a square root z modulo ell.
This elementary fact also follows from Wilson's theorem by pairing
complementary factors of (ell-1)!. Put c=z-1. It is nonzero modulo ell,
since z=1 would imply ell|2.

For R(x)=(x+1)^2+1, R(c)=0 modulo ell and R'(c)=2z is nonzero. Exactly one
lift of c modulo ell^2 makes R vanish modulo ell^2. Choose another lift c'.
It forces ell exactly dividing R(q) for q=c' modulo ell^2.

Combine q=a_L modulo 3^L with q=c' modulo ell^2. Both classes are reduced
and the moduli are coprime, so Dirichlet supplies infinitely many prime q.
Discard q<=3. The exact formula T(q^2)=q^2+2q+2=r holds; both u and r are odd
and are respectively 1 and 2 modulo 3, so the clean guards hold and r>u.

Writing q=1+3t gives

\[
 \sigma(q^2)=3(1+3t+3t^2),
\]

hence C(u)=1 exactly. Also B(u)=0 and B(r)>=L. Finally ell exactly divides
r, so it is a unitary factor and

\[
 \sigma(r)=(\ell+1)\sigma(r/\ell),\qquad 3^K\mid\ell+1.
\]

This proves C(r)>=K. QED.

No output primality or repeatability is asserted. This excludes a
nonincreasing B or C, and a reset bound depending only on their current
values. It does not exclude an additional well-founded charge depending on
the whole integer. A prime-checkpoint rank has a further coverage gap:
an escaping guarded orbit need not visit prime cofactors infinitely often.

## 7. Exact stopping point and provenance

The least-seed assumption supplies a bounded smaller companion. Formula (1)
relates its first step to the original seed. The attempted **transport of
boundedness** is where the contradiction fails:

- Literal divisor transport has the narrow classification (2).
- Uniform linear-error transport fails by (10)–(11), even for a terminating
  companion and a fixed adjacent gcd.
- Initial factorization complexity and a fixed perfect core do not bound
  the available finite growth, by the prime-lifting construction.
- The tested 3-adic budget repairs replenish without bound, by (12).

These constructions do not show that any hypothetical least escaping orbit
visits the exhibited reset classes. Minimality might impose further
restrictions, but none of the transport rules tested here derives them. Nor
do finite blocks exclude a more subtle comparison depending on the entire
seed, all intermediate arithmetic, or a different well-founded rank.

**Established ingredients already in the repository:** the affine
prime-cofactor formula, Lenstra's supplier-chain mechanism and its amplified
version, CRT/Dirichlet finite rebounds, and gcd/cancellation accounting. See
[GLOBAL.md](GLOBAL.md), [RECOVERY.md](RECOVERY.md),
[REGENERATION.md](REGENERATION.md), and
[the amplified chain](approaches/small-gain-feedback/REPORT.md).

**Additional derivations in this attempt:** the prime-deletion divisibility
classification, the fixed-companion error obstruction, lifting the finite
chain into any preselected Dp family, and the explicit valuation reset tests
and simultaneous reset argument. These are applications/extensions of the
identified ingredients; historical novelty has not been established.

**Bottom line:** this is an attempted contradiction with its decisive
arithmetic step tested and disproved in its proposed forms. It is not a
solution, an infinite recharge mechanism, or evidence of divergence. The
remaining global problem is not answered by a larger numerical census.

## 8. Verification is finite and separate

`tests/test_minimum_escape.py` checks prime deletion and its classification
on a bounded range, exact companion examples, modular supplier/CRT identities,
and the valuation-reset examples using both factorization and independent
divisor-pair enumeration. These tests do not certify the universal proofs,
the imported theorems, or the conjecture.

The correction check uses cofactors through 2000. Root lifts use L=1..8,
with deterministic trial division and at most 10000 progression candidates
per prime witness. The largest displayed source is below 1.8 billion. Three
fixed supplier witnesses check actual supply and its unitary guard. The tests
state the other finite ranges explicitly; symbolic modular checks are not
expanded into immense aliquot orbits.

Two read-only AI analyses developed and cross-checked the companion argument
and audited the valuation repair. Their checks agreed on the scoped claims;
the text explicitly enumerates all eligible supplier primes, excludes the
small gcd exception, and does not confuse long increasing prefixes with time
to entry into an unknown cycle. These checks are not independent human review
or formal certification.
