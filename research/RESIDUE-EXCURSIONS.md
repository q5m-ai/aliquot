# 18. Can a fixed modulus certify escape or force a return?

The [last attempt](COMPOSITE-HANDOFF.md) replaced a prime supporting growth
twice on one orbit, but could not show that replacements continue indefinitely. I tried allowing
many different growing classes at once: could some collection of residues
modulo a sufficiently large integer be closed, or at least force a quick
return? There are two different answers about what residues can tell us:

1. **Every nonempty proper union of residue classes has an outgoing aliquot
   edge, arbitrarily far out.** This is a statement about *all* moduli, not a
   search up to a modulus cutoff.
2. **If the union is unchanged by negation, an exit can last arbitrarily long
   with every step growing by more than any prescribed factor.** This part
   constructs an actual orbit segment; it does not concatenate unrelated edges.

For example, for any integer $H\ge1$ and real $G>1$, some $n_0\equiv6\pmod{12}$
visits $9,3,9,3,\ldots\pmod{12}$ on its next $H$ steps, gaining a factor greater
than $G$ at *each* step. The small representative $18\to21$ of the same first
residue transition instead continues $21\to11\to1\to0$. The seed in the
construction depends on $H$. **Neither conclusion settles Catalan–Dickson.**

## 1. No nontrivial residue set is closed

Let $\sigma(n)$ be the sum of all positive divisors of $n$, and $s(n)=\sigma(n)-n$
its aliquot sum. Iterate only while positive. Fix $M\ge2$. Draw an arrow
$a\to b$ between residues if some $n>1$ has $n\equiv a$ and $s(n)\equiv b$
modulo $M$. Different arrows may have different integer witnesses.

**Theorem 1.** This directed graph is strongly connected: each residue can
reach every other. This remains true if both ends of each witnessing integer
edge must exceed any fixed cutoff.

For any positive integer $y$ and any integer $t$, we have the arrow

$$
 y\bmod M\ \longrightarrow\ (t\sigma(y)-y)\bmod M. \tag{1}
$$

Indeed, take $n=yr^E$ with $E\ge2$, $E+1\equiv t\pmod M$, and $r\equiv1\pmod M$
prime, not dividing $y$. Then $n\equiv y$ and $\sigma(n)\equiv(E+1)\sigma(y)$.
Dirichlet's theorem supplies arbitrarily large $r$; even the proper divisor
$n/r$ tends to infinity. With $t=1$ this lifts *any* existing arrow above a
cutoff; $t=0$ gives $a\to-a$. Every **unit** residue (coprime to $M$) reaches
1: take a prime $y$ in that residue and $t=1$. From 1, taking $y=1$ in (1)
gives every target. The task is therefore to reach a unit from any residue.

**Make one prime-power component zero without losing the zeros already made.**
For $p^k\Vert M$ call the component zero if $a\equiv0\pmod{p^k}$. At each
nonzero component there is a specified exponent $e_p=v_p(a)<k$, possibly 0.
Let $d$ be the product of $p^{e_p}$ over these nonzero components. We can
zero a nonzero component at $p$ if

$$
 v_p(\sigma(d))\le e_p\quad(p\text{ odd}),\qquad
 v_2(\sigma(d))< e_2\quad(p=2). \tag{2}
$$

To prove the rule, let $z$ be the product of the primes at the zero components,
each raised to the same exponent $L$, a multiple of $p(p-1)$ at least as large
as every exponent in $M$. Then $p\nmid\sigma(z)$: for each such base $u\ne p$,
the sum $1+u+\cdots+u^L$ is 1 modulo $p$, by counting terms if $u\equiv1$ and
by Fermat's theorem and the geometric series otherwise. Empty products are 1.

Represent one of the reachable signs of $a$ by $y=dzq\equiv\epsilon a\pmod M$
with $q\nmid M$ prime. At each nonzero component $\ell^j$, cancel
$\ell^{e_\ell}$: this prescribes a unit residue for $q$ modulo
$\ell^{j-e_\ell}$. At zero components there is no condition. At the selected
odd $p$, the two signs give opposite nonzero residues, so choose a sign with
$q\not\equiv-1\pmod p$. At $p=2$, choose the sign giving $q\equiv1\pmod4$,
imposing this as a lift if only oddness was prescribed. The Chinese remainder
theorem (CRT) and Dirichlet now give $q$. Multiplicativity gives
$v_p(\sigma(y))=v_p(\sigma(d))$ for odd $p$, or $v_2(\sigma(d))+1$ at 2.
By (2) this is at most $e_p$, so we can solve $t\sigma(y)\equiv y\pmod{p^k}$.
Take also $t\equiv0\pmod{M/p^k}$. Arrow (1) zeros the selected component
and negates the others, preserving their zero status.

**Why a component is available.** If $d>1$, some prime of $d$ satisfies (2).
For a power of two its divisor sum is odd. Otherwise, if all its primes
failed (2), then $d\prod_{p\mid d,\ p>2}p$ would divide $\sigma(d)$. But

$$
 \frac{\sigma(d)}d < \prod_{p\mid d}\frac p{p-1}
                  \le \prod_{p\mid d,\ p>2}p . \tag{3}
$$

Even one odd prime contributes a denominator $p-1\ge2$, enough for a possible
factor 2. This adapts the weak-prime argument in the [finite unitary-core
theorem](COMPOSITE-RENEWAL.md#4-finite-unitary-core-classes-are-not-invariant).
If $d=1$, any remaining nonzero odd component satisfies (2) with both
valuations zero. Each operation adds a zero component. Thus we reach either
the residue 0 or one in which all odd components are zero and the component
at 2 is a unit.

In the first case take $y=\prod_{p\mid M}p^L$ with $L$ sufficiently large and
divisible by every $p(p-1)$ for $p\mid M$. Then $y\equiv0\pmod M$ and
$\sigma(y)\equiv1\pmod p$ for each $p\mid M$; the factor from $p^L$ itself also
gives 1 modulo $p$. Thus $s(y)$ is a unit. In the other case use just the odd
prime powers in that product, calling it $z$. Choose an odd prime $q$ with
$zq\equiv a$ at the power of two in $M$ and $q\equiv1\pmod p$ at each odd
$p\mid M$. Then $s(zq)$ is odd and is 2 modulo each such odd $p$, hence is a
unit. This proves Theorem 1. ∎

Consequently no nonempty proper union of full residue classes, even above a
finite cutoff, is forward-invariant. Finitely many moduli can be replaced by
their least common multiple. **If escaping seeds exist, their set is not
eventually periodic as a subset of the integers:** it is forward-invariant,
would be infinite (an escaping orbit has distinct terms), and cannot contain
all large integers (primes terminate). This does not rule out an individual
orbit staying in some classes without filling them.

## 2. Continue a prescribed exit on one orbit

Theorem 1 does not license concatenating witnesses. Modulo 36 the arrows
$30\to6\to18\to0$ are witnessed by $30\to42$, $42\to54$, and $90\to144$.
The third source is not 54: in fact $s(54)=66$.

**Theorem 2.** Fix any residue edge $a\to b$, integer $H\ge1$ and real $G>1$.
There are arbitrarily large $n_0\equiv a\pmod M$ whose actual iterates satisfy,
for every $1\le j\le H$,

$$
 n_j\equiv(-1)^{j-1}b\pmod M,\qquad M\mid\sigma(n_j),\qquad n_j>G n_{j-1}.
$$

Choose an edge representative $y$. Since $s(y)/y=\sigma(y)/y-1$, we first
enlarge its abundancy $\sigma(y)/y$ while keeping the edge. For $F=M\varphi(M)$ and $p\nmid M$, both $p^F$ and $\sigma(p^F)$ are
1 modulo $M$: the terms from $p$ to $p^F$ form $M$ identical blocks modulo
$M$ by Euler's theorem. Multiply $y$ by such powers of distinct primes not
dividing $My$, obtaining $D\equiv a$ with $s(D)\equiv b$ and
$\sigma(D)/D>G+1$. This is the [invisible-multiplier lemma](approaches/error-correcting-syndromes/REPORT.md#3-proved-result-a-invisible-multiplicative-perturbations);
it uses the divergence of $\prod_p(1+1/p)$ after finite exclusions.

Choose distinct primes $q_1,\ldots,q_t$ not dividing $M\sigma(D)$ with
$\prod_{i\le t}(1+1/q_i)>G+1$, and append $H-1$ further distinct primes with
the same exclusion. For each in order choose $e_i\ge1$ with

$$
 L_i=M\prod_{j<i}q_j^{e_j+1}\ \mid\ \sigma(q_i^{e_i}). \tag{4}
$$

This is possible: $q_i$ is coprime to $L_i(q_i-1)$, so take $e_i+1$ a
sufficiently large multiple of $\varphi(L_i(q_i-1))$ and divide
$q_i^{e_i+1}-1$ by $q_i-1$. This is [Lenstra's finite relay](GLOBAL.md).

**Insert the relay into the first image.** Let $K=M\prod_i q_i^{e_i+1}$.
Choose an exponent $E\ge2$ satisfying

$$
 E\equiv0\pmod M,\qquad (E+1)\sigma(D)-D\equiv q_i^{e_i}
                         \pmod{q_i^{e_i+1}}\quad\text{for each }i.
$$

CRT works because every $q_i$ is coprime to $\sigma(D)$. Take $n_0=Dr^E$ with
$r\equiv1\pmod K$ prime and $r\nmid D$. The successor is $(E+1)\sigma(D)-D$
**modulo $K$**, so $n_1\equiv b\pmod M$ and $v_{q_i}(n_1)=e_i$. Also
$\sigma(n_0)/n_0\ge\sigma(D)/D$, giving the first gain. In contrast to the
[prime-parameter lift](MINIMUM-ESCAPE.md), the free parameter prescribing the
first image here is an *exponent*. This works even for an edge on which the
divisor sum must be odd.

If a term has the first $l$ exact powers, its divisor sum is divisible by
$L_l$ by (4) and multiplicativity. Subtraction negates the term modulo $M$ and
keeps the first $l-1$ exponents exact: at those primes the term's valuation
is strictly smaller than the divisor sum's. While $l\ge t$, the abundancy is
at least $\prod_{i\le t}(1+1/q_i)>G+1$. Starting with $t+H-1$ powers at
$n_1$ leaves at least $t$ at $n_H$, proving even the divisibility assertion
at the last term. Dirichlet gives arbitrarily large $r$ for the fixed choices. ∎

**Return obstruction.** If $R=-R$ is nonempty and proper modulo $M$, Theorem 1
supplies an edge out of $R$ to a $b\notin R$. Both $b$ and $-b$ are outside,
so Theorem 2 proves the claimed growing excursion. The introductory example
uses $18\to21$ modulo 12. The symmetry hypothesis matters: for
$R=\{0,1,2\}\pmod4$ the complement cannot contain even two consecutive terms.
Every $n\equiv3\pmod4$ has a prime $3\pmod4$ to an odd exponent; hence
$4\mid\sigma(n)$ and $s(n)\equiv1\pmod4$.

## 3. What this says about the previous 160-core attempt

Its class $Z$ consists of $n=160u$ with $\gcd(u,10)=1$ and $800\mid\sigma(u)$.
For such a clean factorization $\sigma(n)=378\sigma(u)$, so the supply test is
exactly $1600\mid\sigma(n)$. This is **not** a test on the residue of $n$ alone;
Theorem 1 is not an exit theorem for $Z$.

Take *any* $y\in Z$ and any desired precision $m\ge1$. Apply Theorem 2 to its
edge modulo $M=\operatorname{lcm}(1600,m)$. The new source agrees with $y$ in
both $n$ and $\sigma(n)$ modulo $m$ (the two ends of the edge determine their
sum). Modulo 1600 its terms satisfy $n_j\equiv(-1)^j y$: the first image is
$-y$ because $1600\mid\sigma(y)$. Since $1600=2^6 5^2$, these residues keep
$v_2=5$ and $v_5=1$. Together with the prescribed divisor-sum divisibility,
**the full class $Z$ survives through step $H$**, with every gain greater than
$G$. This holds even starting from the signature of $767840\in Z$, whose own
successor $1046560=160\cdot31\cdot211$ leaves $Z$ since $\sigma(31\cdot211)=6784$.
Primality of the source cofactor is not preserved by the construction.

**Stopping point.** Thus no finite precision on the current value and divisor
sum forces quick loss of this core, even at the signature of a known exit.
But the proof chooses a different integer with that signature: it does not
change what happens to 767840. When the prearranged powers run out, (4) gives
no replacement on the chosen orbit. Neither indefinite growth of one seed
nor eventual descent or cycling of every seed follows.

## Finite arithmetic checks (not proof premises)

Run `python3 -m unittest discover -s tests -p 'test_residue_excursions.py' -v`.
The tests check actual sums by distinct algorithms, small residue graphs using
sources 64–8192 and successors at least 64, the modulo-36 witness mismatch,
and two different outcomes from the same 160-core signature modulo 1600. One
ordinary excursion is $960498\to1791405\to2192211$ with residues $6,9,3$ modulo
12 and both gains greater than $6/5$.

A separate modular fixture takes $M=5$, $D=400$, $q_1^{e_1}=2^3$ and
$q_2^{e_2}=7^3$. Here $\sigma(400)=961$, $\sigma(7^3)=400$, and
$r=1536641=1+8\cdot192080$ is prime. With $E=43655$ the first image of $400r^E$
is 79576 modulo 192080: it has the two exact powers and is 1 modulo 5. The
next term is 4 modulo 5 and retains $2^3$. The first two gains exceed $8/7$ by
the abundancies of 400 and $2^3 7^3$. No full factorization of this first
image or further orbit is asserted. Historical novelty and independent human
review have not been established.
