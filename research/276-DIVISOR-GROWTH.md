# How high must 276 climb before it can fall?

**The sequence from 276 must set a record above $1.23\times10^{215}$ before its current run of increases can end.** We don't know at which step it crosses that height. At the particular step we tried to settle, there is a second result: **either term 2167 is a fifth consecutive record after term 2162, or term 2166 already exceeds twice term 2162.** These are lower bounds on how high the orbit goes, not a ceiling or a proof that it escapes.

## Why a multiple of 6 buys a minimum height

Consider $24\to36\to55\to17$. At 36, the divisors $18+12+6$ already add up to 36; the remaining proper divisors bring the total to 55. The factor 6 disappears going from 36 to 55, but that step still **increases**. It is the next step that falls. Here is what this distinction buys on a large orbit.

Start at any multiple $X>18$ of 6. Every multiple $x>6$ of 6 increases: $x/2,x/3,x/6$ are three proper divisors summing to $x$, and 1 is another. Look at the multiples of 6 starting at $X$:

* If $x=6r$ with $r$ divisible by neither 2 nor 3, multiplicativity gives $s(x)=6(2\sigma(r)-r)$. The next number is **still** divisible by 6.
* Otherwise $12\mid x$ or $18\mid x$. This gives $s(x)>(4/3)x$ or $s(x)>(7/6)x$, respectively. Indeed $s(12)=16$ and $s(18)=21$. For any proper divisor $d$ of $x$, $s(x)/x>s(d)/d$: the sum of $1/e$ over divisors $e$ of $x$ strictly contains the corresponding sum for $d$; subtract 1 from both.

Thus the first time the sequence can lose 6, its outgoing step already takes it **above** $7X/6$, if it hasn't crossed earlier. If it never loses 6, its strictly increasing integer values must also cross. Every step up to the first crossing increases. The argument does not assume that 6 stays forever, or that the first crossing is the very next step. In fact $7/6$ cannot be uniformly improved for all such starts: for $X=18p^2$ the first-step ratio tends to $7/6$, and [along a subsequence of primes](ODD-EXIT-PRIME-WINDOWS.md) the second term after $X$ falls below $X$.

On the [published orbit](ALPOGE-276-RECORDS.md) use $n_0=276$, $M=n_{2162}=197046C$, and $X=n_{2164}=6V$, where $C$ is the specified 210-digit composite. The earlier divisor calculation gives $X>\frac{11}{9}(453600-197046)C=313566C$, and $X$ is a strict record. We have therefore proved a strict record above

$$\frac76 X>365827C>123\cdot 10^{213}.$$

In particular $1.23\times10^{215}$ cannot be a ceiling for 276. This does **not** locate the crossing relative to term 2166.

## What would it take to miss the fifth record?

Write $Y=n_{2165}$, $Z=n_{2166}$, and $T=n_{2167}$. The earlier four-record result gives $M<n_{2163}<X<Y<Z$ and $V\equiv7\pmod{40}$. We ask whether $T>Z$. Set $S=\sigma(3V)$; it is even, since $3V\equiv5\pmod 8$ is not a square. Then

$$Y=3S-6V=6W,\qquad W=S/2-V.$$

If $8\mid S$, then $W\equiv1\pmod4$, so $Y$ has odd part $3W\equiv3\pmod4$, a nonsquare. Its divisor sum is even by complementary divisor pairing. Since $W$ is odd, $Z=3\sigma(3W)-6W$ is a multiple of 6 and $T>Z$. This works whenever the exponent $b$ of 3 in $V$ is **even**, including zero. Indeed $V=3^b m$ then has $m\equiv7\pmod8$, $3\nmid m$. Each odd divisor $d$ is its own inverse modulo 8, so pairing $d$ with $m/d$ gives $8\mid\sigma(m)\mid S$.

Suppose instead that **$T\le Z$**. We must have $b$ odd, so $18\mid X$ and $Y>7X/6$. There are only two possibilities for the number of factors of 2 in $S$:

* If $2\mid S$ but $4\nmid S$, then $W$ is even, $12\mid Y$, and $Z>4Y/3$.
* If $4\mid S$ but $8\nmid S$, then $W$ is odd. If $3W$ were nonsquare, $Z$ would again be a multiple of 6. Thus $3W$ is a square divisible by 3, making $Y=18r^2$ for some odd integer $r$. In particular $Z>7Y/6$.

In either case **$Z>(49/36)X>2M$**. If $T$ falls all the way back to $M$ or lower, $Z$ must in addition be **odd**: an even $Z$ supplies the proper divisor $Z/2>M$. Hence the odd part of $Y$ would have to be a square (equivalently $Y$ is a square or twice a square). This is a necessary condition for that deep fall, not a prediction of one.

**A sufficient divisor to look for, short of a complete factorization.** Recall $n_{2163}=54U$, $U\equiv1\pmod9$, and $V=20\sigma(U)-9U$. If $27\mid\sigma(U)$, then the exponent of 3 in $V$ is exactly 2, which proves the fifth record. One way to certify this is a prime $q\equiv-1\pmod9$ occurring to an odd exponent in the actual $U$. Its prime-power divisor sum supplies a factor of 9. Since $U\equiv1\pmod3$, some **other** prime $2\pmod3$ must also occur to an odd exponent, supplying another 3. We have not identified such a factor of the actual $U$. Failure to find one does not disprove the fifth record.

## A comparison starting two steps earlier

Does the partially factored starting shape itself force a fifth increase? The earlier example $522\to648\to1167\to393$ only matched the residue of $V$. Here is an example that starts back at **$197046C'$** and uses the same divisor formulas at **every** step. Let

$$C'=1009\cdot50534167632757103=50988975141451916927.$$

It is composite, is $179327\pmod{201600}$ just like $C$, and is coprime to $197046\cdot1000!$. It is **not** the same size or integer as $C$. Its exact path is given in factored form so the loss is visible:

| Steps from $197046C'$ | Term |
|---:|---|
| 0 | $197046C'$ |
| 1 | $54\cdot13^2\cdot19^4\cdot11018450976700873$ |
| 2 | $18\cdot1121145820747798016134949$ |
| 3 | $144\cdot163500432192387210686347$ |
| 4 | $4\cdot705644834009\cdot15002806616341$ |
| 5 | $31759958953481174835975664$ |

Both factors listed for $C'$ are prime, as are the last factors in rows 1–3 and the two odd factors in row 4. Step 4 **loses 3 but not 2**; it still increases, to $42346611937828287567764276$. Step 5 is smaller. To construct rather than assume this path, put $C'=1009p$, prescribe $U'=13^2 19^4r$, $V'=3q$, and impose $7q+13=48l$; these relations are linear in the prime partners. The displayed example has actual primes $p,r,q,l$. No theorem about simultaneous primality is needed. Conversely, the [positive comparison](ALPOGE-276-RECORDS.md) $C'=16307327$ gives $V'=864212542407$ with **four** factors of 3, so it does give a fifth rise. The matching starting shape, residue and small-prime exclusions allow **both** outcomes.

Evenness in the deep-fall argument cannot be assumed from $V\bmod40$ alone. At the **$6V$ stage only**, take $V=626248946367\equiv7\pmod{40}$. Here $6V\to(6\cdot390764)^2\to12198452524207\to1$; the penultimate term is prime. We do **not** know this $V$ to arise from a matching $197046C'$, much less from 276.

The [larger-return follow-up](SIX-28-HIGHER-RETURN.md) tests whether the earlier switch from 6 to 28 on this very orbit gives a condition that can keep restarting. It does not extend the late sequence by another exact term.

[Offline checks](../tests/test_276_record_determinants.py): `python3 -m unittest discover -s tests -p 'test_276_record_determinants.py' -v`. The comparisons use exact divisor enumeration from replayed Lucas primality certificates; the large inequality uses the published decimal for $C$, not a guessed factorization. No RH, GRH, Hankel argument or prime-tuples assumption is used. We have not determined the divisors of the actual $Z$ well enough to show that their proper sum $T$ exceeds it, nor found a ceiling, merger or cycle for 276.
