# 19. The step after a 160-core prime return

The [160-core construction](COMPOSITE-RENEWAL.md#2-a-full-prime-entry-return-then-an-exact-obstruction) can take a prime cofactor through a product of two primes and back to a larger prime, with one of the middle primes supplying the full factor of 800 in the divisor sum. Can the new prime start the same construction, possibly using different primes? **No. The next cofactor has a forced factorization that prevents even two consecutive bridges of this kind.** A composite split can keep the full divisibility condition alive. But one fixed seed makes that split, never returns to the bridge-entry class, and reaches zero. This is a counterexample to the proposed return rule, not to Catalan–Dickson.

## 1. Factor the next term without choosing a new parameter

Let $s(n)=\sigma(n)-n$ for positive $n$, stopping at zero. Write

$$
 U=\{u\ge1:\gcd(u,10)=1,\quad 800\mid\sigma(u)\},\qquad Z=160U.
$$

At a source $160u\in Z$, multiplicativity and $\sigma(160)=378$ give the actual successor $160F(u)$ where

$$
 F(u)=\frac{189}{80}\sigma(u)-u,\qquad c=\frac{109}{80},\qquad B(x)=1+c(x+1).
$$

Since $u>1$ and $800\mid\sigma(u)$, $F(u)>cu$ and $\gcd(F(u),10)=1$. Growth is guaranteed; membership of $F(u)$ in $U$ is not. If $u$ is prime then $F(u)=B(u)$.

Define the entry class $C$ by the following finite tests on the initial cofactor $q$:

- $q$ is prime and $q\equiv-1\pmod{800}$;
- $B(q)=rp$ for **distinct primes** $r,p$, with $r\equiv-1\pmod{800}$;
- $Q=(1+c)(r+1)(p+1)-rp$ is prime and $Q\equiv-1\pmod{800}$.

These tests certify the actual cofactor path $q\to rp\to Q$ after scaling by 160. All three cofactors are in $U$. No information about the orbit beyond $Q$ is part of $C$.

**Theorem.** For every such bridge, $p\equiv-1\pmod{800}$ as well, and the next cofactor is exactly

$$
 W=F(Q)=B(r)B(p).
$$

Both displayed factors are integers greater than 1 and are **1 modulo 10**. If $W$ is a semiprime, $5\nmid\sigma(W)$. In particular $Q\notin C$: changing suppliers, even aperiodically, cannot repeat the bridge immediately.

**Proof.** Write $a=r+1$, $b=p+1$. Then $rp=ab-a-b+1$, so

$$
 Q+1=a+b+cab=a+B(r)b.
$$

Since $800\mid a$, $B(r)=1+109a/80$ is 1 modulo 10, hence invertible modulo 800. Reducing the last equality modulo 800 forces $800\mid b$. Using primality of $Q$ now gives

$$
 F(Q)=1+c(Q+1)=1+c(a+b)+c^2ab=(1+ca)(1+cb).
$$

The two integer factors $B(r),B(p)$ are distinct because $r\ne p$. If $W$ has just two prime factors counted with multiplicity, these factors must themselves be distinct primes. Both are 1 modulo 5, so $\sigma(W)\equiv(1+1)^2=4\pmod5$. No such $W$ is a supplying middle term. ∎

The [previous denominator argument](COMPOSITE-HANDOFF.md#6-why-a-periodically-repeated-prime-bridge-is-not-a-shortcut) needed an eventually periodic schedule. Here the two primes that would start the next block are constrained by the actual arithmetic of the previous one. The product identity is the 160-core analogue of the [two-prime shift in note 06](BLOCK-TRANSPORT.md#1-the-first-promising-identity-and-its-trap). A bridge whose first semiprime supplies 800 *only in aggregate*, with neither prime $-1\pmod{800}$, is outside the theorem.

## 2. Can the forced product supply 800 by splitting?

Yes. The smallest possibility is **three** prime factors counted with multiplicity. In that case one of $B(r),B(p)$ is a prime $h\equiv1\pmod{10}$; write the other as $xy$, with $x,y$ prime. Then $W\in U$ **if and only if** $x,y$ are distinct, both $-1\pmod{10}$, and

$$
 32\mid(h+1)(x+1)(y+1).
$$

Indeed $xy\equiv1\pmod5$. If $h$ coincides with $x$ or $y$, all three primes are 1 modulo 5 and their exponents are at most 3, so none of the prime-power divisor sums is divisible by 5. If $x=y\ne h$, then $x\equiv\pm1\pmod5$ and $1+x+x^2$ is nonzero modulo 5. In the distinct case, to supply even one factor of 5 requires $x$ or $y$ to be $-1\pmod5$ and hence both to be. They then supply 25 between them, and the displayed condition is precisely what remains of 800. This is a test on the two **already determined integers** $B(r),B(p)$, not a choice of replacement primes.

What if the original bridge itself uses a composite residual $v$ instead of $p$? There is also an exact test for how much of the proposed factor survives. For $r\equiv-1\pmod{800}$ prime, $\gcd(v,10r)=1$, and $Q=F(rv)\in U$ (not necessarily prime), expansion gives

$$
 80F(Q)=B(r)\big(189\sigma(v)-80v\big)+189\big(s(Q)-s(v)\big).
$$

To verify it, substitute $80Q=189(r+1)\sigma(v)-80rv$ in $80F(Q)=109Q+189s(Q)$. Here $B(r)\equiv1\pmod{10}$, and $80B(r)=109r+189$ with $\gcd(109r,189)=1$, so $B(r)$ is coprime to both 80 and 189. Consequently

$$
 \gcd\big(B(r),F(Q)\big)=\gcd\big(B(r),s(Q)-s(v)\big).
$$

For the [actual composite-residual handoff in note 17](COMPOSITE-HANDOFF.md#2-two-fresh-handoffs-on-one-actual-orbit), $r=2399$, $v=47\cdot75377$, $s(v)=75425$ and $Q=12015893599$ is prime. The right side is $\gcd(3271,75424)=1$: **none** of the proposed factor 3271 survives. This identity does not exclude new, unrelated factors of $F(Q)$.

## 3. Waiting longer: a complete fixed-seed counterexample

One could still hope every member of $C$ whose product $W$ makes the successful three-prime split eventually returns to $C$ at a larger value. The following **single** seed meets that stronger entry test and never returns to $C$ at any positive time. Put $n_0=1255679498239840$ and take actual aliquot steps. The first five terms all have the form $160u_j$:

| $j$ | Exact cofactor $u_j$ | $\sigma(u_j)\bmod800$ |
|---:|---|---:|
| 0 | $7847996863999$ (prime) | 0 |
| 1 | $2399\cdot4457230399$ | 0 |
| 2 | $14579600640799$ (prime) | 0 |
| 3 | $3271\cdot8009\cdot758269$ | 0 |
| 4 | $13\cdot2083533274783$ | 576 |

Here $B(2399)=3271$ and $B(4457230399)=6072976421=8009\cdot758269$. At index 3 the new factors 8009 and 758269 each supply one 5; their plus-ones each supply one 2, and $3271+1$ supplies the other three 2s. Thus index 3 restores the **full** guard, not just divisibility by 160. Index 4 loses it.

The calculation does not stop at this loss. The maximum is $7520281881799528$ at index 6; $n_{115}=0$. The **only** indices in $Z$ are $0,1,2,3$. For an additional check, the only later positive multiples of 160 after index 4 occur at indices 23, 101 and 104; the last two are 320 and 160 itself, neither in $Z$. The cofactor at index 2 cannot be in $C$ by the theorem, and those at indices 1 and 3 are composite. Thus the scaled orbit never returns to $160C$ at positive time, not just at the proposed two-step checkpoint.

**Scope.** “Every entry passing these tests eventually returns to a larger such entry” is false, even allowing an unbounded waiting time. It does not say every such seed terminates, or that every orbit eventually leaves $Z$. For a positive result one still needs a property of the realized composite outputs that implies a larger return **to that property**. Neither the product identity nor one successful split supplies it. No resolution or historical novelty is claimed.

### Reproduce the certificate

```sh
python3 -m unittest discover -s tests -p 'test_prime_bridge_return.py' -v
```

The seed comes from $t=51115$ in [the earlier prime-triple family](COMPOSITE-RENEWAL.md#2-a-full-prime-entry-return-then-an-exact-obstruction); the finite candidate search is not a premise. The regression starts from that one seed, permits 115 edges and caps sources at $8\cdot10^{15}$. At every source it replays the divisor sum via complete divisor enumeration as well as the multiplicative formula. It checks the Lucas prime certificates and separately trial-proves the primes used in the enumerations (bases below $10^{15}$; at most 128 divisors per source). No step is taken at zero and no budget failure counts as termination. These finite checks certify this counterexample, not the universal theorem above.
