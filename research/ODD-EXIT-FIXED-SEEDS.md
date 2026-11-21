# Can a smaller seed explain a long rise after leaving driver 6?

The [prime-window argument](ODD-EXIT-PRIME-WINDOWS.md) selects different prime parameters for steep drops and long rises. This time fix the seed $N=18p^2$, $p\equiv11\pmod{12}$ prime, and look for a **smaller predecessor of a term on its own orbit**. A match would rule out $N$ as the least escaping seed without waiting for the rise to end. Write $n_0=N$, $n_{j+1}=s(n_j)=\sigma(n_j)-n_j$ while $n_j>0$.

## Two fixed seeds, now resolved

For the growing example from the previous note, $p=51342010523$, there is a smaller predecessor of **the seed itself**. Take $d=11394=2\cdot3^3\cdot211$ and $q=3378046191213809567$, a prime not dividing $d$. Since $\sigma(d)=25440$ and $s(d)=14046$,

$$s(dq)=14046q+25440=47448036801789169203522=N,
\qquad dq=38489458302690146206398<N.$$

Thus the two seeds share their entire future from $N$ on. This was a positive hit testing $2\le d\le25000$, not a claim of uniqueness or a complete inverse search. We also followed both previously named hard examples to their endpoints:

| Prime parameter | First drop below $N$ | Last prime $\to1\to0$ | Steps from $N$ to zero |
|---:|---:|---:|---:|
| 6803 (three-step counterexample) | $n_4=525211287$ | 18037633 | 9 |
| 51342010523 (growing example) | $n_4=43351928018631568876911$ | 33713 | 13 |

The [two exact paths and their verifier](../tests/test_odd_exit_fixed_seeds.py) check the small path by divisor pairs. For the larger path they use the known factorization of $N$, a 96-bit cap and at most 2,000,000 work units per certified factorization. Prime certificates are replayed, factor products checked, and divisors enumerated to verify the edges. Zero is an endpoint, not a source. Reproduce with `python3 -m unittest discover -s tests -p 'test_odd_exit_fixed_seeds.py' -v`. The density proof does not use these computations.

## Does adding these predecessors rescue a fixed-depth descent proof?

**Theorem.** Fix any integer $H\ge1$ and any finite list of integers $d\ge2$. Among primes $p\equiv29063\pmod{32340}$, the proportion satisfying **both** of the following tends to one as the upper bound on $p$ tends to infinity:

1. $N=n_0<n_1<\cdots<n_H$, with $n_1,\ldots,n_H$ odd.
2. **None** of $n_0,\ldots,n_H$ equals $s(dq)$ for any listed $d$ and any prime $q\nmid d$, even without the requirement $dq<N$.

This progression accounts for $\varphi(12)/\varphi(32340)=1/1680$ of the original prime parameters. Both statements about proportions are **unconditional**. Under Dirichlet GRH, the same proportions hold when counting only $X<p\le X+X^{1/2+\varepsilon}$ for any fixed $0<\varepsilon<1/2$. This uses the [classical progression estimate](ODD-EXIT-PRIME-WINDOWS.md#the-analytic-input), not a verification of the announced proof.

### Keeping congruences on the actual orbit

The idea is [Erdős's persistence of small prime factors](ANCESTRY-BARRIER.md#1-definitions-and-the-surviving-classical-input). An almost-all theorem for integer seeds need not hold on this sparse family of quadratic prime inputs, so we count factors on the family itself. Write $A(t)=7t^2+13t+13$ and $T(t)=3A(t)$, so $n_1=T(p)>N$. In the stated progression $D=8085$ divides $n_1$, $s(D)=8331>D$, and $32340=4D$. Every multiple of $D$ grows, by scaling its proper divisors.

Fix a positive integer $L$ with $13\nmid L$. We claim that for a proportion tending to one in this progression the orbit grows through step $H$ and

$$n_j\equiv(-1)^{j-1}T(p)\pmod{4L}\qquad(1\le j\le H).$$

For this we need a chain of distinct primes $r_1,\ldots,r_H$ each dividing $A(p)$ **exactly once**. Starting with $r_0=1$, the eligible next primes are

$$r_i\equiv-1\pmod{4DLr_{i-1}^2},\qquad r_i\equiv2\pmod{13}.$$

These conditions specify a reduced class. The reciprocals of its primes have divergent sum by the prime number theorem in arithmetic progressions and partial summation. At each such $r$, the discriminant $-195$ of $A$ is a nonzero square: the quadratic characters of $-1,3,5,13$ are $-1,+1,+1,-1$, respectively, as in the [previous construction](ODD-EXIT-PRIME-WINDOWS.md#selecting-a-long-rise-on-one-orbit). Thus $A$ has two simple, nonzero roots modulo $r$. For each root, exactly one of its $r$ lifts modulo $r^2$ is still a root. Among the $r(r-1)$ unit classes, exactly $2(r-1)$ give exponent one: a fraction $2/r$.

**Why a chain is typical, not just possible.** For a finite set $S$ of eligible next primes, all new to the chain, the limiting fraction of parameters missing them all is $\prod_{r\in S}(1-2/r)$. This also holds conditional on the preceding exact factors: the Chinese remainder theorem (CRT) and the prime number theorem for the resulting **fixed** modulus give the product. By divergence we can make it arbitrarily small. For any $\eta>0$, start with the empty chain. At a level with $K$ candidate chains choose finitely many children of each so its miss fraction is below $\eta/(HK)$. The union bound loses at most $\eta/H$ at that level, whether or not the parent events overlap. After $H$ levels a finite tree covers limiting fraction at least $1-\eta$. Only then let $\eta$ tend to zero. No independence of successive aliquot values or countable union of density-zero exceptions is assumed.

Given such a chain, if $x$ is a current multiple of $D$ carrying the first $k\ge1$ primes to exponent one, $r_1+1\mid\sigma(x)$, hence $4DL\mid\sigma(x)$. Subtraction retains $D$ and negates $x$ modulo $4L$. For $i<k$, also $r_i^2\mid r_{i+1}+1\mid\sigma(x)$, so $r_i$ still divides $s(x)$ exactly once. Each step spends only the last guaranteed link. Starting at the odd $n_1$, this proves the claim on one and the same orbit.

### Ruling out an incoming edge anywhere in that prefix

For each listed $d$, put $a=s(d)>0$, $b=\sigma(d)$. Since $s(dq)=aq+b$ when $q$ is prime and $q\nmid d$, it suffices to force a small prime factor of the candidate quotient $(n_j-b)/a$ whenever it is integral. Use the three polynomials

$$18t^2-b,\qquad T(t)-b,\qquad -T(t)-b.$$

For each polynomial $F$ there are primes $\ell$ of divergent reciprocal sum at which $F$ has a **nonzero** root. Indeed the discriminants are $72b,84b-1755,-84b-1755$, respectively, all nonzero for integral $b>0$. Take $\ell\equiv1\pmod{8|\operatorname{disc}(F)|}$, omitting the finitely many divisors of $13\cdot32340\cdot21a$. Quadratic reciprocity makes the discriminant a square modulo $\ell$; the two roots are distinct, so at least one is nonzero even when $b=39$.

Fix one nonzero root modulo each of finitely many such $\ell$. The limiting fraction of prime parameters that avoid all the specified roots is $\prod_\ell(1-1/(\ell-1))$ by CRT. For any $\delta>0$ choose finite sets large enough that, except for a fraction at most $\delta$ in the limit, **every** polynomial for **every** listed core has a prime divisor from its set at $p$ (finite union bound). Let $L$ be the product of all distinct chosen primes, or 1 for an empty list. In particular $13\nmid L$.

Apply the orbit congruence for this fixed $L$. At $j=0$ use the first polynomial; at every later checkpoint use the sign dictated by $j$. Some $\ell\mid n_j-b$ with $\ell\nmid a$. For sufficiently large $p$, strict growth gives $n_j\ge N>b+a\ell$ simultaneously for all the finitely many tests. An integral candidate quotient is therefore divisible by $\ell$ and larger than $\ell$: it cannot be prime. Letting $\delta\downarrow0$ proves the joint assertion. For the short-window version, every finite residue count used here has the same limiting proportions by subtracting the Dirichlet-GRH prime counts at the endpoints. The moduli are fixed **before** $X\to\infty$.

**Stopping point.** A real smaller predecessor works for the named growing seed. But checking arbitrarily many *fixed* forward steps and a fixed menu of such predecessors at **every** one of them still misses asymptotically the whole displayed progression. This rules out neither a seed-dependent time nor unrestricted smaller representatives that take several steps to merge. The exceptional primes may change with $H$; no prime has been shown to grow forever. To complete a proof by descent we still need to force resolution or find a smaller seed with the same future for the cases this test misses.
