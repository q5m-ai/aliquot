# Can one aliquot orbit stay at six times two distinct primes?

Almost every seed of this form leaves it on the **first** step. That is not an answer for an individual seed. On a fixed orbit we can rule out another possibility: the sequence cannot grow forever just by keeping each smaller prime for a long stretch and then replacing it with a fresh one. It would have to **lose and regain** smaller primes, with no uniform bound on the number of separate visits per prime. We do not prove that such returns are impossible.

Write the aliquot term as $6u$, with $u=pq$ and $3<p<q$ primes. Since $\sigma(6)=12$, multiplicativity gives the cofactor of the next term:

$$v=T(pq)=2(p+1)(q+1)-pq=(p+2)(q+2)-2=pq+2(p+q+1).$$

This is odd and not divisible by 3: modulo 3 the shifted factors are each 0 or 1. Every step from such a source strictly increases. **The test is the factorization of $v$ itself**: to use the shifted-product formula again we need two distinct prime partners greater than 3 at this new source. An infinite run would therefore disprove Catalan–Dickson, but leaving this form need not even make the next term decrease.

## What separate returns cost on one orbit

The larger prime never survives the next step: $T(pq)\equiv 2(p+1)\not\equiv0\pmod q$, since $q>p+1$. The smaller one survives exactly if $p\mid q+1$. If the result is again a product of two distinct primes and $p$ survives, it is still the smaller prime: writing the result as $pq'$, one has $q'>q$. In this case

$$q'+p+1=\frac{p+2}{p}(q+p+1). \tag{1}$$

Thus every consecutive transition keeping $p$ spends exactly one factor of $p$ from $q+p+1$. For example, in cofactor coordinates $5\cdot19\to5\cdot29\to5\cdot43\to313$ uses both factors of 5 in $19+5+1=25$. The bound can be attained; it only counts uninterrupted transitions.

**Fixed-seed bound.** Suppose $u_0,\ldots,u_{m-1}$ are such sources on one orbit, with final output $u_m$ not necessarily a semiprime. Let $R_m(p)$ count the maximal consecutive blocks of the smaller prime $p$ in those $m$ sources. A switch of smaller prime loses the old one completely at that step. With $L(x)=\log(2x)$,

$$\boxed{\displaystyle \log\frac{L(u_m)}{L(u_0)}\ \le\ 4\sum_{p\le\sqrt{u_m}}\frac{R_m(p)}{p\log p}.} \tag{2}$$

To prove it, take a block of $k$ sources starting at $x=pq$ and ending just before its output $y$. Only the $k-1$ internal transitions have to preserve $p$. By (1), $p^{k-1}\mid q+p+1$, so $p^k\le p(q+p+1)\le2x$. Every step of the block, **including its last**, has gain $1+(2/p)(1+(p+1)/q_i)<1+4/p$, since the current partner $q_i>p+1$. Consequently $L(y)-L(x)\le 4k/p\le 4L(x)/(p\log p)$. Multiply the bounds for $L(y)/L(x)$ over the blocks and take logs. Strict growth ensures that all counted smaller primes are below $\sqrt{u_m}$.

In particular, a uniform cap $C$ on **blocks** per prime, even one depending on the seed and with no uniform cap on block *lengths*, forces exit. Indeed $W=\sum_{p>3}1/(p\log p)<\infty$ over primes by partial summation. Then (2) gives $2u_m\le(2u_0)^{\exp(4CW)}$, whereas an infinite run grows without bound. This sharpens the distinction in the [record-source bound](ALPOGE-RECORD-HEIGHT.md): counting an unbroken run of $p$ repeatedly is no longer enough. It does **not** show one named prime must return infinitely often.

**How many separate visits would be necessary?** Let $R(p)$ be the total number on a hypothetical infinite run. If every $R(p)$ is finite, then

$$\liminf_{z\to\infty}\frac{1}{\log\log z}\sum_{p\le z}\frac{R(p)}{p\log p}\ \ge\ \frac12. \tag{3}$$

In particular $R(p)\le c\log p$ for all sufficiently large primes with $c<1/2$ is impossible in this case, by [Mertens' prime reciprocal estimate][mertens]. To see the improvement over (2), the gain per step is less than $(1+2/p)(1+2/q_i)$. The partner increases inside a block, so $\log(L(y)/L(x))\le k(2/p+2/q)/L(x)$ using the **entry** partner $q$. For $k=1$ this is at most $2/(p\log p)$ since $2x>p^2$. For $k\ge2$ it is at most $2/(p\log p)+2/(q\log p)$ by the block length bound. In the latter case $q=jp-1$ for some $j\ge2$. Different blocks at the same $p$ have different entry partners by strict growth. The sum of $1/q$ over the nonsingleton blocks at $p$ is therefore at most $(1/p)\sum_{i=1}^{R_m(p)}1/i$.

Write $w_p=1/(p\log p)$ for primes $p>3$, $W=\sum_p w_p<\infty$, and $A_m=\sum_p w_p R_m(p)$. The harmonic sum above is $O(\log(1+R_m(p)))$. By concavity of $\log$, $\sum_p w_p\log(1+R_m(p))\le W\log(1+A_m/W)$. Summing the block bounds gives $\log(L(u_m)/L(u_0))\le2A_m+O(\log(1+A_m))$. If all visit counts are finite, the smaller primes on an infinite run are unbounded by (2). Stop at the **first** source $u_m$ whose smaller prime exceeds $z$. Then $u_m>z^2$ but all earlier labels were at most $z$. Thus $A(z)=\sum_{p\le z}w_pR(p)$ satisfies $\log\log z+O_{u_0}(1)\le2A(z)+O(\log(1+A(z)))$, proving (3).

A real return need not recover an old number. Starting at $6\cdot3707$, the successive factorizations **after dividing out 6** are

$$11\cdot337\ \to\ 5\cdot881\ \to\ 37\cdot167\ \to\ 11\cdot599\ \to\ 73\cdot107\ \to\ 11\cdot743\ \to\ 23\cdot421\ \to\ 97\cdot109\ \to\ 10987.$$

The last cofactor is prime. The three separate visits to 11 have three different partners; in fact no neighboring cofactors in this example share a prime. The [finite-core return theorem](ALPOGE-PRIME-ARRIVALS.md#when-a-large-prime-really-does-force-a-return-on-one-orbit) needs recurrence of an entire core itinerary on an actual infinite tail, not repeated appearances of a single prime.

### Testing repeated losses and returns to the same two primes

Can we force exit by showing that a long series of returns to 11 is already impossible modulo some prime? Consider the particular schedule of smaller primes $11,23,11,23,\ldots$, with larger partners $Q_i>23$. The required steps satisfy $23Q_{2j+1}=13Q_{2j}+24$ and $11Q_{2j+2}=25Q_{2j+1}+48$. Put $U_{2j}=3Q_{2j}+71$ and $U_{2j+1}=3Q_{2j+1}+37$. The two multipliers on $U$ are $13/23$ and $25/11$, respectively. For $2h$ transitions this forces $253^h\mid U_0$, since $U_{2h}=(325/253)^h U_0$ and $\gcd(325,253)=1$. **No fixed positive seed can alternate forever.** One actual round trip, after dividing by 6, is $11\cdot1663\to23\cdot941\to11\cdot2143$.

Nevertheless, **at every fixed length the partner forms pass every finite set of prime divisibility tests**. Write $U_0=253^h t$, $t=2+3z$. The resulting $Q_i=(C_i t-d_i)/3$ are integral linear forms in $z$, with

$$C_{2j}=253^{h-j}325^j,\quad d_{2j}=71;\qquad C_{2j+1}=143\cdot253^{h-j-1}325^j,\quad d_{2j+1}=37$$

for $0\le j\le h$ at even indices and $0\le j<h$ at odd ones. To avoid a prime $r\notin\{3,37,71\}$ in every partner, take $t=0\bmod r$. At 3, choose $z$ so $Q_0\ne0\bmod3$; the step equations then alternate signs. At 37 or 71 choose $t\ne0\bmod r$. This protects the parity whose offset $d_i$ vanishes. At the other parity the excluded values $d_i/C_i$ lie in a single coset of the subgroup generated by $325/253$. This subgroup is proper: the ratio is $26\bmod37$ with $26^3=1\bmod37$, and $17\bmod71$ with $17^{10}=1\bmod71$. The Chinese remainder theorem combines any finite list of these choices. It cannot certify that the partners are prime.

**Conditional on Dickson's prime-tuples conjecture**, this gives, for every prescribed $h$, infinitely many seeds with all $2h$ actual transitions. The forms have positive slopes and are pairwise nonproportional: within either parity the coefficients are distinct and the offset is fixed, and neither 37 nor 71 divides a coefficient. This is a different conjecture from the aliquot conjecture; no implication from Dirichlet GRH is known here. The unconditional denominator obstruction still applies to every fixed seed. For an arbitrary, changing sequence of smaller primes there is no single multiplier $325/253$ to iterate.

## How many seeds leave on the first step?

**Relative-density theorem (unconditional).** Order the seeds $6pq$ by $pq\le X$, counting each pair of primes $3<p<q$ once. For any *fixed* $K\ge1$ and $Y$, the proportion for which $T(pq)$ has at least $K$ distinct prime divisors greater than $Y$ tends to one. In particular, take $K=3$: the proportion surviving even one transition as a squarefree semiprime tends to **zero**. Here “greater than $Y$” does not mean greater than both input primes.

First fix a modulus $M$ and two unit classes $a,b\bmod M$. The number of pairs in these classes in the given order is asymptotic to

$$\frac{1}{\varphi(M)^2}\,\frac{X\log\log X}{\log X}. \tag{4}$$

For detail, sum $\pi(X/p;M,b)-\pi(p;M,b)$ over primes $3<p\le\sqrt X$, $p\equiv a\pmod M$, with $\pi(t;M,b)$ the prime count in that class. The subtractions total $O(X/\log^2 X)$. For the first term the [prime number theorem in fixed progressions][pnt] applies uniformly to its arguments $X/p\ge\sqrt X$. In the resulting sum we can replace $1/\log(X/p)$ by $1/\log X$: the error *before multiplying by $X$* is $O((\log X)^{-2}\sum_{p\le\sqrt X}(\log p)/p)=O(1/\log X)$. Partial summation of the same prime number theorem gives $\sum_{p\le\sqrt X,\ p\equiv a\bmod M}1/p\sim(\log\log X)/\varphi(M)$. This proves (4); $M=1$ gives the total. Pairs involving a prime divisor of fixed $M$ contribute only $O_M(X/\log X)$.

For a probe prime $r\ge5$, exactly $r-3$ of the $(r-1)^2$ ordered unit pairs satisfy $(a+2)(b+2)=2\pmod r$: for $a\ne0,-2,-1$ there is exactly one $b=2/(a+2)-2$, and it is nonzero. Thus the limiting hit fraction is $d_r=(r-3)/(r-1)^2$. Its sum over primes $r>\max(3,Y)$ diverges. For a **finite** set $S$ of those primes, (4) with $M=\prod_{r\in S}r$ and the Chinese remainder theorem give miss fraction $\prod_{r\in S}(1-d_r)$. Given $\eta>0$, choose $K$ disjoint finite sets each with miss fraction below $\eta/K$. Outside their combined misses the output has at least $K$ distinct prime factors. A union bound followed by $\eta\downarrow0$ proves the assertion. No independence of successive aliquot steps or prime-count estimate for a growing modulus is used.

**Stopping point.** The typical first step and the fixed-orbit bound answer different questions. The first cannot exclude one exceptional starting integer. In fact $T(pq)\ge pq+4\sqrt{pq}+2>(\sqrt{pq}+1)^2$: even an infinite surviving orbit would itself supply only $O(\sqrt X)$ starting cofactors up to $X$, of relative density zero by (4). On a fixed orbit we can bound what one uninterrupted visit contributes. To start a new $k$-source visit to $p$ from a cofactor $ab$ lacking $p$, it is necessary that $(a+2)(b+2)\equiv2-p(p+1)\pmod{p^k}$: the entering cofactor is $pq=T(ab)$ with $p^{k-1}\mid q+p+1$. This congruence does not guarantee primality of the new partner. We have no upper bound on how often such entries occur on that seed strong enough to contradict (2) or (3). The density and fixed-orbit bounds are unconditional aliquot results, not new transfers from Alpöge's archive.

[Follow-up: signed lattice indices for returns](ALPOGE-RETURN-INDICES.md). An ordered list of smaller primes cannot repeat arbitrarily early, even with an unbounded set of labels. We also test what remains when visits to one prime have different continuations.

[Exact finite checks](../tests/test_six_semiprime_returns.py) replay the factorizations, divisor sums and finite residue counts independently of the asymptotic argument: `python3 -m unittest discover -s tests -p 'test_six_semiprime_returns.py' -v`.

[mertens]: https://dlmf.nist.gov/27.11#E8
[pnt]: https://dlmf.nist.gov/27.11#p4
