# 16. Beyond the first fresh supplier: composite residuals and their guards

**Outcome:** the fresh-supplier approach advances past one replacement, but
still does not close. An exactly verified orbit makes **two successive fresh
handoffs**, including one through a genuinely composite residual. Neutral-power
control forces a handoff, but also forces the next supplier to be less than
one-sixth of the current one. Adding a prime tag escapes that decreasing budget:
a written construction permits **arbitrarily large replacement suppliers** with
powered composite residuals. Its output shape still does not regenerate.

The distinction matters: compositeness itself is not an obstruction. The gap
in [note 15](RETURN-CLOSURE.md) is the lack of control of the residual's divisor
sum. This note gives both neutral and nonneutral control, and precise failures
of their powered input shapes. A separate theorem keeps actual prime
predecessors while blocking any prescribed finite menu of fresh replacements.
A periodic prime-bridge repair also has an explicit finite denominator budget.

These are local deductions and finite certificates, not a solution, divergent
seed, or novelty claim. The neutral-power method specializes the existing
[invisible-multiplier argument](approaches/error-correcting-syndromes/REPORT.md#3-proved-result-a-invisible-multiplicative-perturbations).
The periodic obstruction specializes [note 07, Proposition P](RECOVERY.md#proposition-p--periodic-fixed-core-schedules-cannot-escape).
As usual, s(n)=sigma(n)-n for positive integers; stop at zero.

## 1. Keep the composite correction instead of discarding the bridge

Recall

\[
 Z=\{160u:\gcd(u,10)=1,\quad800\mid\sigma(u)\}.
\]

Every member has a larger successor with exact exponents (v2,v5)=(5,1).
The successor is in Z only if its new cofactor's divisor sum is again divisible
by 800. While the core is retained, each step grows by at least 109/80.

Let r=800a-1 be prime, let v>=1 with gcd(v,10r)=1, and set

\[
 A=1890a=\frac{189(r+1)}{80},\qquad B=1090a+1=A-r.
\]

The source 160rv is in Z. Its **actual**, not formal-prime, successor is

\[
 s(160rv)=160F_r(v),\qquad
 F_r(v)=A\sigma(v)-rv=Bv+A\,s(v).                 \tag{1}
\]

Indeed, sigma(160rv)=378(r+1)sigma(v). Division by 160 gives (1).
If one falsely treats v as prime, the proposed output is Bv+A. Its exact
missing correction is

\[
 F_r(v)-(Bv+A)=A(s(v)-1).
\]

It vanishes for a prime v, but is positive for a composite v>1.

For a proposed fresh prime R=-1 modulo 800 with R not dividing Arv, (1) gives

\[
 R\mid F_r(v)
 \quad\Longleftrightarrow\quad
 \frac{\sigma(v)}v\equiv\frac rA\pmod R.         \tag{2}
\]

The divisions here are modular inverses. To certify a unitary R and therefore
renew Z, strengthen this to R dividing F_r(v) but R^2 not dividing it.
This is a **matching** requirement, not a requirement that R divide sigma(v).
In fact, R dividing sigma(v) would block a fresh R when R does not divide rv.
Equation (2) is an exact diagnostic, not by itself a renewal theorem.

## 2. Two fresh handoffs on one actual orbit

The checked clean-160 cofactors are

```text
6237785599                          prime
  -> 8498982881 = 47 * 2399 * 75377
  -> 12015893599                    prime
  -> 16371655031 = 37 * 73 * 6061331.
```

These arrows mean actual aliquot steps **after multiplication by 160**:

```text
998045695840 -> 1359837260960 -> 1922542975840 -> 2619464804960.
```

The corresponding divisor sums of the cofactors are

```text
6237785600, 8683545600, 12015893600, 17044465584,
```

with residues 0,0,0,784 modulo 800. Thus the first three terms belong to Z;
the fourth still has the core but is outside Z.

- The first fresh supplier is 2399. It is absent from the first term and
  appears to exponent one in the second; 2399+1=2400 supplies 800.
- The second fresh supplier is 12015893599 itself. It is absent from the
  preceding term and appears to exponent one in the third; its divisor sum
  12015893600 is divisible by 800.
- The intervening residual is **not prime**:
  v=47*75377=3542719 and s(v)=75425. Formula (1), with A=5670 and B=3271,
  gives the second handoff. The composite correction is 427654080, not zero.

The entry prime is 385599+1919200*3250; this progression forces 2399 into its
first image. All named factorizations and edges are checked independently.
The fourth term disproves closure of the full Z guard at that next checkpoint;
it does not classify the orbit's eventual fate or later returns.

This answers the narrow question left by the earlier example: a composite
residual can produce a second genuinely fresh supplier, even restoring a prime
entry cofactor. It does **not** show that every successful handoff does so.

## 3. A proved family with powered composite residuals

We can replace an assumption of residual primality by a precise power shape.
This construction starts at 160rv; it does not assert that this value has a
predecessor 160q with q prime.

### Neutral-power lemma

Let R be an odd prime and put E=R^2(R-1). For every positive w coprime to R,

\[
 w^E\equiv\sigma(w^E)\equiv1\pmod{R^2}.           \tag{3}
\]

**Proof.** Factor w into prime powers p^e. The exponent d=eE is divisible
by both R^2 and R(R-1). Euler's theorem gives p^d=1 modulo R^2. If p is not
1 modulo R, p-1 is invertible, so

\[
 \sigma(p^d)-1=p\frac{p^d-1}{p-1}\equiv0\pmod{R^2}.
\]

If p=1+Rt, the binomial expansion modulo R^2 gives

\[
 \sigma(p^d)=\sum_{j=0}^{d}p^j
 \equiv d+1+Rt\frac{d(d+1)}2\equiv1\pmod{R^2}.
\]

Here R is odd and R^2 divides d. Multiplicativity proves (3), including w=1.
The extra factor R in E beyond phi(R^2) is important: Euler's theorem alone
controls the value, not its divisor sum. For example, 7^6=1 modulo 9 but
sigma(7^6)=7 modulo 9. ∎

### Powered-residual handoff theorem

Fix any prime R=-1 modulo 800. There are infinitely many primes r=-1 modulo
800 such that, for **every** positive w with gcd(w,10rR)=1,

\[
 160r w^{R^2(R-1)}\in Z,\qquad
 s\bigl(160r w^{R^2(R-1)}\bigr)\in Z,
\]

and the successor contains a fresh unitary R. In particular, w>1 gives a
composite residual without any assumed primality of that residual or its image.

**Proof.** Impose

\[
 r\equiv-1\pmod{800},\qquad
 109r+189\equiv80R\pmod{R^2}.                    \tag{4}
\]

Since R=-1 modulo 800 is not 3,7,109, the second condition is a reduced residue
for r: it is nonzero modulo R and 109 is invertible. Its modulus is coprime
to 800. CRT and Dirichlet give infinitely many prime r, all different from R.

Fix one such r. The input is in Z because r is unitary and 800 divides r+1.
For v=w^E, (3) and (1) yield

\[
 F_r(v)\equiv A-r=\frac{109r+189}{80}
          \equiv R\pmod{R^2}.
\]

Thus R occurs to exponent exactly one in the successor's clean cofactor.
It was absent from the source by gcd(wr,R)=1. Multiplicativity and
800 dividing R+1 put the successor in Z. ∎

Only r is chosen as a prime parameter. The theorem does not assume simultaneous
primality of two linear forms, and w may have any factorization consistent
with the coprimality condition.

### An exact modular certificate, and a structural failure to repeat

A checked choice is

```text
R = 2399,
r = 58933259999                 prime,
E = 13800971998,
A = 139229826750,
B = 80296566751 = 2399 * 33470849.
```

The progression in (4) is

```text
r = 3683330399 (mod 4604160800);
58933259999 = 3683330399 + 12 * 4604160800.
```

Here B=2399 modulo 2399^2. Tests certify the actual prime parameters and
also check the symbolic w=13 source by modular divisor sums; the enormous
integer 160r*13^E and its full successor are **not expanded or factored**.
The exact unitary factor R is nevertheless certified by the displayed residue.

The stronger input shape does not renew. In fact, for this fixed pair r,R and
**every allowed w additionally coprime to 3**, write the output cofactor as
F_r(w^E)=Rz. Then

\[
 z\equiv-\frac rR w^E\equiv-1\equiv2\pmod3,       \tag{5}
\]

because 3 divides A, r=R=2 modulo 3, and E is even. Consequently z is not a
square. Since R is unitary, F_r(w^E) cannot be **any prime times a square**:
that prime would have to be R, leaving the nonsquare z. It therefore cannot
have the one-prime-times-even-power form used at the input, even with a new
choice of the distinguished prime.

This is an infinite subfamily of successful fresh handoffs whose power-shape
certificate necessarily fails to reproduce. It is not an obstruction to more
general composite guards. Supplier choices with a different mod-3 phase are
not excluded by (5), and the actual orbit may continue growing outside this
particular input shape.

## 4. Neutrality forces descent; a prime tag permits upward replacement

### The neutral-handoff supplier budget

Suppose a fresh prime R=-1 modulo 800 divides F_r(v), and R divides s(v).
Then

\[
 R\le\frac{109r+189}{720}<\frac r6.               \tag{6}
\]

**Proof.** Freshness gives R not dividing v. Reducing (1) modulo R gives
R dividing B=1090a+1. Write B=Rh. Since B=1 and R=-1 modulo 10, h=-1 modulo
10, so h>=9. Thus R<=B/9=(109r+189)/720<r/6; the strict inequality holds
for r>189/11, in particular for every supplying prime here. ∎

The neutral-power construction has s(v)=0 modulo R. Consequently it **cannot
support an infinite chain of these one-step handoffs**, even if its power
shape could somehow renew: the distinguished supplier would decrease by more
than a factor of six at each step. Any infinite chain of this same single-step
kind would need infinitely many *nonneutral* handoffs, with R not dividing s(v).
Here the newly produced R must become the next distinguished supplier; switching
to an unrelated retained factor does not concatenate these inequalities.
Other core phases and variable-time mechanisms are not covered by this claim.

The actual second handoff in section 2 is nonneutral: its residual has
s(v)=75425, while its new supplier is the larger prime 12015893599.

### Prime-tagged powered-residual theorem

Fix a prime r=-1 modulo 800 and its coefficients A,B from (1). Choose **any**
prime R=-1 modulo 800 with R not dividing rAB, and any integer 1<=c<R.
There are infinitely many primes d, different from 2,5,r,R, such that for
**every** positive w with gcd(w,10rdR)=1,

\[
 n=160rd\,w^{E_R}\in Z,\qquad s(n)\in Z,
 \qquad E_R=R^2(R-1),
\]

with a genuinely fresh unitary R in the successor. All but finitely many
candidate primes R are allowed, so the target R can be arbitrarily large,
in particular larger than r.

**Proof.** Impose

\[
 Bd+A\equiv cR\pmod{R^2}.                        \tag{7}
\]

Because R does not divide AB, this is a reduced residue for d modulo R^2.
Dirichlet gives infinitely many prime d, excluding the finitely many prohibited
values. Fix one. For v=d w^E_R, coprimality and the neutral-power lemma give

\[
 v\equiv d,\qquad\sigma(v)\equiv d+1,\qquad
 s(v)\equiv1\pmod{R^2}.
\]

The source belongs to Z via its unitary r. Its actual next cofactor satisfies

\[
 F_r(v)\equiv B d+A\equiv cR\pmod{R^2}.
\]

Since c is nonzero modulo R, the new factor R has exponent one. It was absent
from the source, and R+1 supplies 800 at the successor. ∎

This controls the composite correction modulo the **new supplier's square**,
without setting the correction to zero as an integer or pretending v is prime.
The added prime tag changes s(v) from 0 to 1 modulo R, avoiding (6).
There is no assertion of a prime-q predecessor; choosing new d,w after an
actual step would change the seed, not prove renewal.

### A larger fresh supplier, and a new exact shape failure

A checked choice is

```text
r=2399, R=4799, d=2711, c=1849=43^2,
A=5670, B=3271,
B*d+A=8873351=4799*43^2,
E_R=110499863998.
```

For w=1, a small ordinary instance has clean-160 cofactors

```text
2399*2711 -> 4799*43^2 -> 13*968713.
```

The first two belong to Z after scaling; the third cofactor's divisor sum is
396 modulo 800. The new supplier 4799 is larger than both source primes 2399
and 2711. This is not persistence of a preloaded larger supplier. Even this
3-free w=1 example exits the universal tagged-power format: its 43-exponent is
2, whereas such an input has 43-exponent 0, 1 (if its tag is 43), or a positive
multiple of E_R'>2. Its supplying prime cannot be 43.

For genuinely composite residuals, take w=3^k, k>=1, and write x=3^(E_R k).
The exact formulas are

\[
 \sigma(2711x)=2712\frac{3x-1}{2}=4068x-1356,
\]

\[
 F_{2399}(2711x)=16561871x-7688520.                \tag{8}
\]

Every such source has the same finite prime support {2,3,5,2399,2711}; its
successor has the fresh, larger prime 4799 to exponent one. This is an infinite
family of **one** successful handoff, not successive handoffs on one orbit.

The output cannot re-enter any of the prime-tagged universal-power families
just proved. Indeed, 3 does not divide 16561871, while

\[
 7688520=3^5\cdot31640,\qquad3\nmid31640.
\]

Since E_R k>5, (8) has exact 3-exponent 5. In any new cofactor
r'd'w'^(E_R'), with the theorem's distinct-prime and coprimality guards,
r' is not 3; the 3-exponent is either 0, 1 (if d'=3), or a positive multiple
of E_R'>5. It cannot be 5. This excludes renewal of that entire powered format
for this subfamily, not arbitrary factorization-aware matching conditions.

There is also an important phase distinction. For any clean-160 step,
80u'=189sigma(u)-80u implies u'=-u modulo 3. Thus a prime-q entry, necessarily
3-free, stays 3-free while this core persists. The w=3^k subfamily is valid
inside the broader Z but is **not reached from that prime-entry cohort through
clean-160 steps**. The theorem has a 3-free subfamily when d is not 3 and
w is coprime to 3. No renewal theorem or prime-q predecessor is asserted for
those members either.

## 5. A finite replacement menu can be blocked with prime predecessors intact

Fix the first supplying prime r and any reduced refinement q=a modulo K of
the prime-q construction in note 15. Thus q=-1 modulo 800 and r occurs to
exponent one in

\[
 u_1=\frac{109q+189}{80}=rv.
\]

For every finite set S of candidate primes -1 modulo 800, infinitely many
prime q in this progression have **no member of S fresh in u2 relative to u1**.
This can hold even while r remains unitary in u2, so the full Z guard survives.

**Proof.** Choose one prime q0 in the progression outside S; Dirichlet allows
this finite exclusion. Let v0 be its residual. Discard r from S, since it is
already present. Refine the parameter by q=q0 modulo each remaining ell in S.
The refinement is compatible and reduced. Because 80r is invertible modulo
these ell, it preserves whether ell divides v. Partition the targets into
those already present and those absent.

Choose a prime P=-1 modulo

\[
 800r^2\prod_{\ell\ \mathrm{absent}}\ell,
\]

avoiding the prime divisors of the refined modulus and of r*109*189.
Dirichlet again permits these finite exclusions. Impose

\[
 109q+189\equiv80rP\pmod{P^2}.                    \tag{9}
\]

This is a reduced residue for q modulo P^2, since P divides neither 109 nor
189. CRT combines it with the existing reduced progression, and Dirichlet
gives infinitely many prime q. Condition (9) forces P to exponent one in v.
Hence P+1 divides sigma(v).

Each absent target ell now divides sigma(v), but not rv, so
u2=A sigma(v)-rv is nonzero modulo ell. Already-present targets cannot be
fresh. Also r^2 divides sigma(v), while r does not divide Av. Unequal-valuation
subtraction gives r to exponent one in u2, and therefore u2 remains in Z. ∎

The inserted P is new relative to the original 160q but already present at
u1; it is **not** a second-generation fresh replacement. The theorem does not
exclude other fresh suppliers outside S, aggregate supply from several
prime-power factors, or a factorization-dependent guard. In particular it
does not say that u2 leaves Z. This specializes the supply-insertion method
of [note 10, Proposition W](PARITY-HANDOFF.md#proposition-w--finite-first-image-exponents-can-be-held-unchanged)
to block the nonzero matching needed for prescribed new suppliers.

## 6. Why a periodically repeated prime bridge is not a shortcut

The finite example in section 2 returns to a prime cofactor. Another attempted
repair is to demand prime checkpoints q and intermediate cofactors rv with
r=800t-1 and v a prime different from r. If the input and output checkpoints
belong to Z, their primes are -1 modulo 800. The intermediate factorization
is a substantive additional hypothesis.

The two actual steps give

\[
 rv=\frac{109q+189}{80},\qquad
 q'=\frac{a_r q+b_r}{c_r},                         \tag{10}
\]

where

\[
 a_r=109(1090t+1),\quad
 b_r=189(640000t^2+290t+1),\quad c_r=80r.
\]

Both a_r and b_r are odd, v2(c_r)=4, and a_r>c_r. Fix a block of m such
suppliers and compose their affine maps without canceling denominators:

\[
 G(q)=\frac{a q+b}{c}.
\]

Then a,b are positive odd integers, a>c, and v2(c)=4m. The assertion about b
follows inductively: composing adds an odd multiple of the previous odd
numerator to a multiple of its even denominator. Put

\[
 W(q)=(a-c)q+b>0.
\]

Whenever the complete block is valid and its endpoint is an integer,

\[
 W(G(q))=\frac ac W(q),\qquad
 v_2(W(G(q)))=v_2(W(q))-4m.
\]

Starting from a fixed checkpoint q0, the number h of complete repetitions
therefore satisfies

\[
 h\le\left\lfloor\frac{v_2(W(q_0))}{4m}\right\rfloor. \tag{11}
\]

An eventually periodic supplier schedule is impossible for this growing
prime-bridge template, even if one tries to assume all the needed primes.
This is the concrete 2-adic denominator case of the already established
periodic-core obstruction, not a new theorem excluding general aliquot escape.

For example, with r=2399 a genuine prime-bridge block has cofactors

```text
57580223999 -> 2399 * 32702399 -> 106969552799,
```

where every displayed prime factor is certified. Formula (10) has
(a_r,b_r,c_r)=(356539,1088804619,191920), and v2(W(q0))=9, allowing at most
two full repetitions arithmetically. In fact the next intermediate cofactor
is 511 modulo 2399, so this supplier choice already fails to repeat immediately.

Aperiodic supplier choices, nonprime residuals, different core phases, and
more general variable-time returns are **not** excluded by this argument.

## 7. What advanced, and what is still missing

- A second fresh supplier can arise on the **same orbit**, through a composite
  residual. It is not merely a second seed chosen for a larger bound.
- Neutral replacement alone cannot be perpetual: its supplier decreases by
  more than sixfold. A prime tag permits nonneutral, arbitrarily large fresh
  replacements without requiring residual primality.
- Both powered formats have proved nonrenewal subfamilies. The finite-menu
  obstruction preserves actual prime predecessors and even the Z guard; it
  shows why a finite list of replacement primes is not enough.
- Returning to periodically scheduled prime bridges is also insufficient,
  by an existing obstruction with the explicit budget (11).

The remaining task is still an invariant factorization-aware condition: every
allowed exit must generate a subsequent input satisfying that condition, with
net growth. Requiring this of all future iterates merely restates the target;
choosing a new r or w after each step changes the seed instead of proving it.
No indefinitely replenished supplier mechanism has been established.

### Reproduction and scope

```sh
python3 -m unittest discover -s tests -p 'test_composite_handoff.py' -v
```

Named ordinary sources have an inclusive cap of 20000000000000; primality
certificates have cap 200000000000. Finite path verification permits at most
four edges. Divisor-pair sums independently check the ordinary aliquot edges;
exhaustive trial tests independently check the named primes. The small
composite-identity audit uses r in {2399,4799} and 1<=v<=31.

The symbolic modular audit uses powered bases w at most 31 and outer exponents
E at most 110499863998; fixed supplier/tag primes obey the primality cap above.
It compares binary geometric sums against modular evaluation of the exact
quotient (p^(d+1)-1)/(p-1), using the enlarged modulus M(p-1) before integer
division. The finite-menu certificate splits the required supply between
unitary auxiliary primes 34552799 and 356822461. Its large CRT representative
is not declared prime or presented as a prime-input orbit. No huge expanded
integer or unfactored residual is presumed prime. Budget exhaustion is unresolved computation, never escape evidence.
These are finite checks of the displayed formulas and certificates; the
universal claims rest on the written proofs, not on tests or AI agreement.
Two independent read-only analyses agreed on the descent, tagged construction,
finite-menu argument, and nonclosure calculation. Their scope checks made the
tracked-supplier condition and the 3-free cohort distinction explicit; this is
not formal verification or a historical novelty audit.
