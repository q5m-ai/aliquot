# Composite supplier renewal: a full return and finite-core obstructions

**Status: proof attempt, not a proof or disproof of the aliquot conjecture.**
We extend the fresh-supplier construction to composite inputs, obtain an actual
return to its original prime-entry guard, and try two mechanisms for repeating
it. A fixed prime bridge consumes a finite divisibility budget. A composite
block exchange reveals another growing core, but finite unions of unitary-core
classes with arbitrary remainders cannot be invariant. A reduced-congruence
version of that obstruction applies to the supplying blocks considered here.
Equal-valuation retention works for prime active blocks but can fail on supplied
composite active blocks. None of these results excludes every possible renewal
rule or supplies an escaping seed.

The starting `160`-core lemma is from the separate
[return-closure work in PR #18](https://github.com/q5m-ai/aliquot/pull/18), read at
[commit 38583f3](https://github.com/q5m-ai/aliquot/blob/38583f3f23989d31bdcdb8d2735dbdb5171f0dab/research/RETURN-CLOSURE.md).
That source is not merged into this branch by this note. See also
[minimum-seed/finite recharge](MINIMUM-ESCAPE.md),
[composite transport](BLOCK-TRANSPORT.md), and
[periodic prime-core schedules](RECOVERY.md).

All integers are positive unless stated otherwise. Write
`s(n)=sigma(n)-n`; stop at zero, where `s(0)` is undefined. A unitary divisor `d`
of `n` satisfies `gcd(d,n/d)=1`. Universal arguments below use exact
multiplicativity, valuations, CRT, and explicitly identified applications of
Dirichlet's theorem. Tests verify bounded arithmetic, not those universal
arguments. Two read-only AI analyses and cross-audits informed this attempt;
that is not human peer review, formal certification, or a historical novelty
check.

## 1. The actual composite map

Put
\[
U=\{u>0:\gcd(u,10)=1,\quad800\mid\sigma(u)\},\qquad
Z=160U.
\]
Since `sigma(160)=378`, define, where integral,
\[
F(u)=\frac{189}{80}\sigma(u)-u,\qquad s(160u)=160F(u).
\tag{1}
\]
For `u in U`, writing `sigma(u)=800h` gives
\[
F(u)=1890h-u,\qquad \gcd(F(u),10)=1,\qquad
F(u)>\frac{109}{80}u.
\tag{2}
\]
Thus integrality, the clean core, and growth propagate for one edge. Membership
of `F(u)` in `U` still requires `800 | sigma(F(u))`.

If `r=800k-1` is prime and `gcd(r,w)=1`, then
\[
\boxed{F(rw)=(1090k+1)w+1890k\,s(w).}
\tag{3}
\]
The last term is constant only when `w` is prime. It is an actual divisor sum,
not an independently selectable correction.

### Composite-input fresh handoffs

Fix any `A in U`, put `B=189 sigma(A)/80`, and let `p` be prime with
`p` not dividing `10A`. Then
\[
F(Ap)=(B-A)p+B.
\tag{4}
\]
Here `B` is a positive multiple of ten and `B-A>0`. Choose a prime
`r=-1 (mod 800)` avoiding `10AB(B-A)`, and prescribe
\[
(B-A)p+B\equiv r\pmod{r^2},\qquad p\equiv1\pmod{10}.
\tag{5}
\]
These conditions define a reduced CRT class: the first residue is a unit
modulo `r`, and the second is a unit modulo ten. **Dirichlet's theorem** gives
infinitely many such primes `p`, excluding the finitely many divisors of `A`.
Then `r` is new relative to `Ap`, occurs exactly once in `F(Ap)`, and supplies
`800 | r+1`. Thus `Ap` and `F(Ap)` both lie in `U`.

For example, `A=1653=3*19*29` has `sigma(A)=2400`. With
`p=278344271`, equation (4) gives
\[
F(Ap)=4017p+5670=1118108942277,
\qquad F(Ap)\equiv2399\pmod{2399^2}.
\]
This extends the method to composite input cofactors. It still selects a
starting prime parameter: it does **not** select the already determined
remainder at the next point of an orbit.

## 2. A full prime-entry return, then an exact obstruction

Fix `r=2399`, and for integers `t>=1` put
\[
\begin{aligned}
p_t&=87200t+2399,\\
q_t&=153536000t+4223999,\\
Q_t&=285231200t+7852799.
\end{aligned}
\tag{6}
\]
**Conditional return.** If all three values are prime, then
\[
160q_t\longrightarrow160r p_t\longrightarrow160Q_t
\tag{7}
\]
is an actual aliquot block, and all three terms belong to `Z`.

Indeed, `80r p_t=109q_t+189` and `Q_t=3271p_t+5670`.
The three variable primes and `r` are all `-1 mod 800`, while `p_t>r`.
Multiplicativity proves both edges and all unitary guards. The input shape
really returns: the endpoint is again `160` times a prime supplying `800`.
This restores the prime-`U` entry condition, **not** the stronger prime-triple
predicate needed to repeat this particular handoff. No assertion of infinitely
many simultaneous prime values of (6) is made.

### Exact witness and stopping point

At `t=375`, complete prime proofs give
\[
p=32702399,\quad q=57580223999,\quad Q=106969552799.
\]
The scaled path is
\[
9212835839840\longrightarrow12552488832160
\longrightarrow17115128447840.
\tag{8}
\]
Both edges grow. The new middle suppliers are `2399` and `32702399`; the
endpoint prime `106969552799` itself supplies `800` again.

But the following cofactor is
\[
F(Q)=145746015691=29^2\cdot3271\cdot52981,
\qquad \sigma(F(Q))\equiv784\pmod{800}.
\tag{9}
\]
Thus the next term still has a clean `160`-core, as (2) promises, but is outside
`Z`. The full return in (8) does not make its guard automatic forever.

### No infinite repetition with a fixed prime supplier

More generally fix any prime `r=800k-1`. Suppose a block has prime cofactors
`q -> rp -> Q`, with `p != r`. Set
\[
c=1090k+1,\quad e=1890k,\quad
 d=80r,\quad a=109c,\quad b=189c+80re.
\]
The exact two-step map is
\[
dQ=aq+b.
\tag{10}
\]
We have `a>d>0`, `b>0`, and `gcd(a,d)=1`: `c=1 mod 10`, and
`r` divides neither `109` nor `189`, hence neither `a` nor `c`.
Define
\[
H(q)=(a-d)q+b>0.
\]
Equation (10) gives
\[
H(Q)=\frac ad H(q).
\tag{11}
\]
Repeating this **same** prime-bridge rule `j` times therefore requires
\[
d^j\mid H(q_0).
\tag{12}
\]
A fixed positive integer cannot satisfy (12) for unbounded `j`. This rules out
indefinite repetition of that pattern, even before its other prime guards are
checked. It is an explicit instance of the earlier periodic-core obstruction,
not an obstruction to changing suppliers or composite active remainders.

For `r=2399`, the constants are
\[
(a,d,b)=(356539,191920,1088804619).
\]
For the source in (8), `H(q)=9478799983296000` has valuations
`(v_2,v_5,v_2399)=(9,3,1)`. Since `d=2^4*5*2399`, at most one such return is
possible, including the one already displayed: there can be no second
consecutive application from this seed. The smallest budget is exactly the
supplying prime's.

## 3. Attempting a genuine composite-block exchange

Try a composite supplying block
\[
A=3^3 7^3=9261,\qquad \sigma(A)=40\cdot400=16000.
\]
Neither of these two prime-power blocks supplies `800` alone. For **every**
`w` coprime to `10A`, including composites,
\[
F(Aw)=37800\sigma(w)-9261w
     =189\bigl(200\sigma(w)-49w\bigr).
\tag{13}
\]
This suggests changing phases rather than demanding the old block back.
Let `D=160*189=30240` and `t=200 sigma(w)-49w`. Since `sigma(D)=4D`,
\[
s(Dt)=D(4\sigma(t)-t)\ge3Dt
\tag{14}
\]
**provided** `gcd(t,D)=1`. Divisibility by `189` in (13) alone does not prove
that this new core is unitary.

For `w=1` the actual path is
\[
160\cdot9261\longrightarrow30240\cdot151
\longrightarrow30240\cdot457\longrightarrow30240\cdot1375.
\]
The last cofactor shares `5` with the core, so (14) cannot simply be applied
again. Even the first new unitarity guard need not hold for arbitrary `w`:
`w=13` gives `7 | t`.

We tried repairing (13) by admitting finitely many unitary composite cores,
including alternative growing `2^a5^b` phases. The following theorem prevents
closure **when the complementary remainder is arbitrary**.

## 4. Finite unitary-core classes are not invariant

For `D>1` define
\[
\mathcal C_D=\{Dw:w\ge1,\ \gcd(D,w)=1\}.
\]

**Finite-core theorem.** For every nonempty finite list `D_1,...,D_m>1`, the
union `X=union_i C_(D_i)` is not forward-invariant under `s`.

This means that **some actual source in this union has its next term outside
it**. It does not say every orbit leaves the union, nor exclude an invariant
subset with additional factorization or divisor-sum guards.

### Proof

Choose the numerically smallest listed core `D`. Let `P` contain all primes in
the list, and choose an integer `H>max_(i,p in P) v_p(D_i)`. For `p | D`, put
`e_p=v_p(D)` and `h_p=v_p(sigma(D))`. Call `p` weak if `h_p<=e_p`.

There is a weak prime. Otherwise `D rad(D) | sigma(D)`, contradicting
\[
\frac{\sigma(D)}D
 <\prod_{p\mid D}\frac p{p-1}
 =\frac{\operatorname{rad}(D)}{\prod_{p\mid D}(p-1)}
 \le\operatorname{rad}(D).
\tag{15}
\]
For each weak prime write `sigma(D)=p^h a`, `D=p^e b`, with `a,b` units at
`p`. Prescribe an integer `E>=2` by
\[
E+1\equiv a^{-1}\bigl(p^{e-h}b+p^{H-h}\bigr)
       \pmod{p^{H+1-h}}.
\tag{16}
\]
For each `p in P` not dividing `D`, also prescribe `E+1=0 mod p`.
CRT combines these conditions; increasing by their common modulus ensures
`E>=2`. By **Dirichlet's theorem**, choose a prime
\[
q\equiv1\pmod{\prod_{p\in P}p^{H+1}}.
\]
Then `n=Dq^E` belongs to `C_D`, and at every inventory prime
`q^E=1` and `sigma(q^E)=E+1` modulo `p^(H+1)`. The actual successor has
\[
v_p(s(n))=
\begin{cases}
H,&p\mid D,\ h_p\le e_p,\\
e_p,&p\mid D,\ h_p>e_p,\\
0,&p\in P,\ p\nmid D.
\end{cases}
\tag{17}
\]
For a weak prime, (16) makes `sigma(D) sigma(q^E)-Dq^E` congruent to
`p^H mod p^(H+1)`. Strong primes retain exponent `e_p`; absent inventory primes
are excluded by the prescribed zero of `sigma(q^E)`.

A listed unitary core of `s(n)` could use neither a weak prime (its exponent is
too large) nor an absent prime. It could use only strong blocks of `D`, at
their original exponents. Since at least one weak block was removed, any such
listed core would be a **proper unitary divisor of `D`**, contradicting its
minimality. This proves the theorem. If the chosen core is abundant, this
constructed exit edge nevertheless grows.

A small exact instance uses the list `{6,18}` and `n=6*1297^22`.
Here `1297` is prime and `s(n)` has `(v_2,v_3)=(1,3)`. Neither `6` nor `18` is
unitary in the output. This is one finite arithmetic check of (17).

### Reduced residue guards do not repair the finite supplier class

**Corollary.** Fix finitely many blocks `A_i` satisfying
`gcd(A_i,10)=1` and `800 | sigma(A_i)`, and put `D_i=160A_i`.
For each core allow its coprime remainder to lie in any nonempty finite
collection of **reduced** progressions `a mod M`, meaning `gcd(a,M)=1`.
The resulting union of classes is still not forward-invariant.

This assertion adds only residue conditions to arbitrary composite remainders.
It does not include prime-only remainders, arbitrary divisor-sum guards, or
unrestricted non-reduced progressions.

Choose the smallest core `D` and one allowed progression `a mod M`. First
construct a squarefree semiprime `z`, coprime to all inventory primes, with
\[
z\equiv a\pmod M,\qquad
v_p(\sigma(z))=0\ (p\in P,\ p\ge5),\qquad
v_3(\sigma(z))\le1.
\tag{18}
\]
Here is why this is possible. First lift `a mod M` to a unit `c` modulo
`L=lcm(M,9,product_(p in P) p)`; at primes absent from `M` its residue is free.
Split `c=xy mod L`. At `p>=5`, choose `x` avoiding `0,-1,-c mod p` and set
`y=c/x`; then neither plus-one vanishes. At `3`, a product `1 mod 3` permits
both residues `1`; a product `2 mod 3` permits `x=1`, `y=2 mod 3`. In the latter
case choose `x mod 9` among `1,4,7` so that `y` is `2` or `5`, not `8`. Lift
`x` to higher powers already in `L` and define `y=c/x`, preserving both the
prescribed product and exact valuation. At `2` only oddness and the product
are needed. CRT and two applications of **Dirichlet** give distinct prime
representatives for `x,y`, avoiding the finite inventory. Their product is the
required `z`.

There remains a weak prime after replacing `sigma(D)` by
`sigma(D) sigma(z)`. Indeed, `D=160A` already has strict surpluses at `2,5`.
If all primes became strong, (18) would force strict surplus in `sigma(D)` at
every prime except possibly `3`, where at least equality would hold. Thus
\[
D\frac{\operatorname{rad}(D)}d\mid\sigma(D),\qquad
d=3\text{ if }3\mid D,\text{ and }d=1\text{ otherwise}.
\]
This contradicts (15): the product of `(p-1)` is at least `4` because `2,5 | D`,
and at least `8` if `3 | D`, in either case greater than `d`.

Repeat (16), now using `sigma(D) sigma(z)` and `Dz` as the two coefficients.
Choose the auxiliary prime `q` also `1 mod M` and distinct from both primes
in `z`. Then `n=Dzq^E` satisfies the original remainder progression, while
(17), with the revised weak/strong classification, still forces any listed
unitary output core to be a proper divisor of `D`. This proves the corollary.

The constructed source is in `Z`, so its successor grows and retains the clean
`160`-core. The theorem excludes the proposed **finite list** of unitary
supplying cores, not possible supply from some new, unlisted factorization.

## 5. A non-strict retention attempt and its composite obstruction

Strict surplus is not necessary for retention. Choose prime `t=-1 mod 800`,
and a prime `p>t+1` in the reduced progression
\[
p=-1+th,\qquad189h\equiv-80\pmod t.
\tag{19}
\]
Dirichlet supplies such primes. Put `w=tp`. Then
\[
v_t(w)=v_t(\sigma(w))=1,\qquad
189\sigma(w)/t\equiv80p\pmod t.
\]
For **every prime** `r` coprime to `10w`,
\[
80F(wr)/t\equiv80p\bigl((r+1)-r\bigr)=80p\not\equiv0\pmod t.
\]
So `t || F(wr)`: the supplier survives at exponent one even without strict
surplus. Both source and output belong to `U`.

For an arbitrary active block `R` coprime to `10w`, the true equation is instead
\[
\boxed{80F(wR)/t\equiv80p\,s(R)\pmod t.}
\tag{20}
\]
That last divisor sum can disable the old supplier. Choose distinct primes
`a,b`, avoiding `10w`, with
\[
a=-1\pmod{800},\quad a=1\pmod t,\quad b=-2\pmod t.
\]
CRT and Dirichlet supply them. The active block `R=ab` itself supplies `800`,
but `s(R)=a+b+1=0 mod t`. Moreover, as an affine function of `b`,
\[
80F(wab)/t=
\bigl(189\sigma(w)(a+1)/t-80pa\bigr)b
 +189\sigma(w)(a+1)/t
\]
has coefficient `80p != 0 mod t`. Among the lifts of `b=-2 mod t` to `mod t^2`,
exactly one makes this expression zero modulo `t^2`. Choose any other lift and
apply Dirichlet: then `t^2 || F(wab)`.

The inherited block is now `t^2`, with `sigma(t^2)=1 mod 5`, so it no longer
supplies a factor of five. **This does not show the whole output leaves `U`:**
other factors may replace its supply.

An exact example is
\[
t=2399,\quad p=15833399,\quad a=4799,\quad b=21589.
\]
For prime active block `r=3`, `F(wr)=245148539397` has `v_t=1`.
For supplied composite active block `R=ab`,
\[
wR=3935389117266691811,\qquad
F(wR)=5368212855629308189,
\]
and the latter has `v_t=2`. Complete divisor enumeration from the independently
proved source factors verifies this edge without factoring the huge output.

The simplest splice with section 2 also fails: retaining `t` in a growing
output larger than `t` makes that output composite, not a prime checkpoint.
If the resonant block `w=tp` is used alone, its active remainder is `R=1`;
then `s(1)=0` in (20) forces `t^2 | F(w)`, again excluding a prime endpoint.
This incompatibility concerns that immediate splice, not longer phase changes.

### What a finite complement-local menu can guarantee

Fix `w` coprime to ten and let the active prime `r=-1 mod 800` vary, excluding
divisors of `10w`. Put
\[
H_w=189\sigma(w),\quad L_w=189\sigma(w)-80w,
\qquad80F(rw)=L_wr+H_w.
\tag{21}
\]
For a prime `ell` not dividing ten, let `e=v_ell(w)`, `f=v_ell(H_w)`.
For active primes `r != ell`, the output exponent is constantly `e` when
\[
f>e\quad\text{or}\quad f=e\text{ and }v_\ell(L_w)>e.
\tag{22}
\]
Otherwise `v_ell(L_w)=f`, and the two affine coefficients after division by
`ell^f` are units. There is a unit root modulo every power of `ell`; CRT and
Dirichlet make the output exponent arbitrarily large.

Define `K(w)` to contain the blocks `ell^e` with `ell | w` satisfying (22).
These are inherited blocks, including strict surplus and the equal-valuation
retention above. For any finite list `D_i` coprime to ten:

> Every admissible active prime makes at least one `D_i` unitary in `F(rw)`
> **if and only if** some `D_i` is a unitary divisor of `K(w)`.

The reverse implication follows directly from (22); primes dividing `K(w)`
already divide `w`, so the active prime cannot equal them. For the forward
implication, suppose no candidate is unitary in `K(w)`. At every variable
prime in the finite menu, force the output exponent above all candidate
exponents. CRT and Dirichlet do this simultaneously, with `r` outside all menu
supports. Every candidate then has either a wrong constant exponent or an
overshot variable exponent, so none is unitary. This proves the equivalence.
The exclusion of active `r=ell` is necessary when asserting a constant exponent
at a prime outside `w`; it is harmless for this counterconstruction.

Since `K(w) | w`, **no finite menu fixed from the complement alone guarantees
a genuinely fresh unitary supplier for every active prime**. The candidates
may be composite and share the `2/5` supply. A menu depending on the realized
active prime, or an unbounded selection from its actual output, is not covered.

## 6. Verification and exact remaining obligation

`tests/test_composite_renewal.py` checks these finite examples and local laws:

- the composite-input handoff, full prime-entry return, and its next guard loss;
- the fixed-return integer budget and the composite `9261 -> 189` exchange;
- an actual 231-bit exponent-overflow source for cores `{6,18}`;
- the residue-compatible construction with `D=1481760`, `z=341=8 mod 9`,
  `E=43070`, and certified prime `q=342206822790000001=1+19*210^7`.
  This last check evaluates source and divisor-sum congruences modulo the four
  inventory prime powers; it does **not** expand the huge source or compute
  its full successor;
- non-strict retention, its supplied-composite failure, and the finite-menu
  exponent argument, including the exceptional active prime.

The prime-triple search uses only `1<=t<=4096`, stops at `375`, and has no
unresolved certificates before stopping. Its 27 small-prime-screen survivors
are checked by bounded certified factorization (200000 work units per call,
128-bit source cap), with an independent Lucas replay. Displayed return primes
also have complete trial-division proofs. Three edges from (8) through (9)
have source values below `2*10^13` and independent divisor-pair checks.
Large smooth sources use complete proved factorizations and enumeration of
all divisors. No factorization-budget failure is treated as primality.

The attempted proof stops at a precise distinction. We can restore the full
input shape once, retain suppliers without strict surplus, and exchange
composite blocks into another growing phase. But the simple fixed bridge has
a finite budget, finite arbitrary-remainder core classes fail, and the
non-strict rule is sensitive to the actual complementary divisor sum.

A remaining candidate would have to propagate additional arithmetic structure
on its realized outputs, or use changing suppliers/variable-time returns in a
way not covered above. **No such invariant integer class has been proved here.**
A failure of these closure attempts is neither a proof of termination nor
evidence that an actual infinite renewal orbit exists.
