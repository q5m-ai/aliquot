# Can the 6-to-28 switch on 276 lead back to a larger number of the same kind?

**A larger return happens on 276, but the proposed rule is not self-sustaining.** Let $s(n)=\sigma(n)-n$ be the sum of proper divisors. With $n_0=276$, the early path is

$$1872\to3770\to3790\to3050\to2716\to2772.$$

The launch is $144\cdot13$. After two drops the sequence reaches $2716=28\cdot97$, still above the launch, then $2772$, divisible by both 6 and 28. This is stronger than an isolated increase, but the new number is not another $144\cdot13$. To test an induction we need to specify what **same kind** means, without looking ahead for a successful return.

Take the checkpoint set $C=\{28p:p\text{ prime},\ p\equiv13\pmod{84}\}$. Here $84$ is the least common multiple of 6 and 28. This includes the observed landing at $p=97$. It fixes $p\equiv1\pmod3$, so the next term $28(p+2)$ picks up a factor of 3, and $p\equiv-1\pmod7$, so this next term still has exactly one factor of 7. On **276 itself** the first two visits to $C$ are

| Index | Term | Prime left after dividing by 28 |
|---:|---:|---:|
| 8 | 2716 | 97 |
| 44 | 9344070652 | 333716809 |

That is a larger return to the *same* arithmetic condition, not just to some multiple of 28. These are old terms of the [published sequence](https://oeis.org/A008892), not new records beyond its factoring frontier. We checked every edge from index 0 through 44 independently by divisor pairs. The return takes 36 steps. Neither endpoint satisfies the stronger two-step rule below.

**There is no third visit through index 2165.** On the [published prefix through 2162](ALPOGE-276-RECORDS.md) this needs no new factorization. At $x=28u\equiv364\pmod{2352}$, $u\equiv13\pmod{84}$, so $s(x)-x=56s(u)$; the gap is 56 exactly when $u$ is prime. The only candidates for this residue in the prefix are indices 8, 44, 52, 58, 134, 136, 152, 687, 689, 695, 717, 725, 737 and 783. Only 8 and 44 have gap 56. This is a check on published heights ([OEIS b-file](https://oeis.org/A008892/b008892.txt), then the five FactorDB entries), not a replay of 2162 historical factorizations. The [previous divisor argument](ALPOGE-276-RECORDS.md) proves terms 2163–2165 are multiples of 6, whereas no member of $C$ is divisible by 3. We have not proved a third visit or ruled it out for the rest of the orbit.

## A return that really works twice, and why it runs out

At $28u$ with $\gcd(u,28)=1$, the next term is $28(2\sigma(u)-u)$. Impose the following tests on the **starting number alone**: it is $28p$, where $p=27r-2$, $r\equiv13\pmod{84}$, and $r,p,P=53r+80$ are all prime. Call this stronger set $G$. It is a subset of $C$. Since $\sigma(27)=40$, the two actual steps are

$$28p\ \longrightarrow\ 28\cdot27r\ \longrightarrow\ 28(53r+80)=28P.$$

Indeed, $p+2=27r$ and $2\sigma(27r)-27r=80(r+1)-27r$. Both applications use cofactors coprime to 28. We have $P\equiv13\pmod{84}$ and $P>p$; the middle cofactor is composite. Thus this is a **first return to $C$**. The conditions are not a claim about the frequency of simultaneous primes. The older [supplier example](SUPPLIER-RENEWAL.md#4-the-promised-precise-first-return-lemma) $9772\to9828\to21532$ is the case $r=13$.

This rule can actually restart with all its tests satisfied. Here the two-step checkpoints are in bold:

**327292** $\to327348\to$ **644812** $\to644868\to$ **1268092**.

The starting $r$ is 433, then 853. The three checkpoint primes are 11689, 23029 and 45289. The first two checkpoints are in $G$ and all three are in $C$. But if a bridge is to be used again, the next $r'$ is **forced** by $27r'=P+2=53r+82$. Thus

$$13r'+41=\frac{53}{27}(13r+41).$$

Each restart consumes three factors of 3 in the positive integer $13r+41$. If it starts with exactly $v$ such factors, there can be at most $1+\lfloor v/3\rfloor$ consecutive bridges starting there, irrespective of primality. Here $v=4$ initially and $v=1$ at the restart, so the bound of two is attained. This says nothing about the subsequent fate of 327292.

**Waiting longer does not rescue this rule for all its entries.** At $r=6397$, $4836076\in G$ returns in two steps to $9495388\in C\setminus G$. Its *entire* remaining orbit has no member of $C$ and reaches zero at step 34 from the start. Thus $C$ admits a member with no later larger return, and even membership of $G$ need not produce another $G$ at **any** later time. This is about a separate, resolved seed; it is not a prediction for 276.

## Does changing the power of 3 avoid the obstruction?

Suppose $28p\in C$. Write $p+2=mr$ with $m=3^a$ the exact power of 3. The cofactor $p+2$ is odd and $1\pmod7$, so the second step really has cofactor

$$P=(3m-1)\sigma(r)-mr.$$

Call a two-step return *simple* here only if $r$ is prime and $28P\in C$. This allows $a$ and $r$ to change on every return. Then $P=(2m-1)r+3m-1$. In **any 13 consecutive simple returns** starting with $p>13$, at least one of the first 12 sources must have $3^{11}\mid p+2$. In particular, permitting all exponents from 1 to 10 is still not an indefinitely repeatable rule.

* Since $P\equiv1\pmod3$, we have $r\equiv1\pmod3$. Both checkpoint primes are $-1\pmod7$. Hence $mr\equiv1\pmod7$ and $(3m-1)(r+1)\equiv0\pmod7$. This forces $m\equiv5$ or $6\pmod7$, that is, $a\equiv5$ or $3\pmod6$.
* If $a\equiv1\pmod4$, then $m\equiv3\pmod5$. Both coefficients in $P+2=(2m-1)r+3m+1$ vanish modulo 5. For the **next** return to be simple its prime remainder after removing all threes would have to be 5, not $1\pmod3$. Thus each of the first 12 exponents is $3$ or $11\pmod{12}$.
* If all 12 are $3\pmod{12}$, then $m\equiv1\pmod{13}$. At each step $P\equiv r+2\equiv p+4\pmod{13}$. Thirteen successive checkpoint primes then cover every residue, including zero, but all are larger than 13. This contradiction proves the claim.

This test does not rule out very high powers of 3, composite remainders (the formula then uses their actual $\sigma(r)$), or a later return that takes more than two steps. The 36-step return on 276 is precisely outside the theorem.

## Why allowing more time or both divisors is a substantive change

At the original launch, **no rule based just on the exponents of 2, 3 and 7 can guarantee larger returns for every member of a class containing 1872**, even with unlimited waiting. For example, $46800=1872\cdot5^2$ has the same exponents at *every* prime except 5, and the same squarefree part (13, after removing all square factors). Its only later values larger than itself are 128102 and 80518, neither divisible by 6 or 28, and it reaches zero at step 21. Likewise $226512=1872\cdot11^2$ has only 523874 and 322426 above its start, again with neither divisor, and reaches zero at step 27. In particular, if membership depends just on $\gcd(n,M)$ and optionally the squarefree part of $n$, any universally restarting class containing 1872 must have $55\mid M$: otherwise at least one terminating seed is indistinguishable from it. This necessary test does **not** assert that $55\mid M$ suffices, and a requirement about primality of the remaining cofactor is not a gcd test.

The pattern of the original switch, *including the drops*, is also compatible with a cycle. The separate prime launch $144\cdot5323$ gives

$$766512\to1379060\to1573876\to1211984\to1153936\to1401456.$$

As at 1872, the first three successors are divisible by neither 6 nor 28; after two decreases the fourth is a multiple of 28 above the launch, and the fifth has both divisors. Yet this sequence reaches $1210\leftrightarrow1184$ (first repeat at step 31). The five-step pattern alone does not keep restarting. No equality of other prime factors with the 276 example is claimed.

There is also a fixed-depth obstruction even when the starting large cofactor is prime. For *each fixed* $H\ge1$:

* Among primes $p$, the limiting fraction for which $144p$ reaches **any larger multiple of 6 or 28** in steps 1 through $H$ is exactly $1/2$. Almost all the successes, in this density sense, occur at step one. Indeed $s(144p)=259p+403>144p$ for $p>3$. This image is even, always $4\pmod7$, and $p+1\pmod3$. Primes $2\pmod3$ give an immediate success; for almost all primes $1\pmod3$ neither 3 nor 7 appears in any of the first $H$ successors. This last assertion still holds in every fixed reduced refinement of $p\equiv13\pmod{84}$.
* At the *landing* $28p\in C$ the opposite obstruction holds. For almost all primes in its progression, **all** of the next $H$ terms are multiples of 84 and grow, but **none is in $C$**. Even a fixed cap on the number of distinct primes in the cofactor after dividing by 28 would miss these terms for a fraction tending to one. The conclusion persists in any fixed reduced refinement. It does not assert that most of these orbits never return.

Here is the arithmetic for both claims. This specializes the [finite prime-factor persistence argument](ODD-EXIT-FIXED-SEEDS.md#keeping-congruences-on-the-actual-orbit), not an assumption that successive iterates are independent. Write $n_1=Ap+B$ for the positive affine first image ($A=259,B=403$ or $A=28,B=56$). Fix any modulus $M$, lower cutoff $Y$, and count $J\ge1$. For a relative proportion tending to one of the primes $p$ in the given progression, $n_1,\dots,n_H$ have $J$ common primes $>Y$ to exponent one, and $n_j\equiv(-1)^{j-1}n_1\pmod M$ throughout.

To see this, take $J+H-1$ successive finite sets of candidate primes $\ell>Y$, excluding divisors of $ABM$ and the progression modulus. At each level take primes $-1$ modulo $M$ times the squares of **all** candidate primes at earlier levels, excluding earlier primes. The sum of their reciprocals diverges by the prime number theorem in arithmetic progressions. For each such $\ell$, exactly $\ell-1$ of the $\ell(\ell-1)$ unit residues for $p\bmod\ell^2$ give $\ell\parallel Ap+B$. The Chinese remainder theorem and prime counts in fixed progressions give the limiting miss fraction $\prod_\ell(1-1/\ell)$ at a level. Make it less than $\varepsilon/(J+H-1)$ per level. Outside total upper relative density at most $\varepsilon$, one prime from each level divides $n_1$ exactly once. At every step, the last remaining selected prime supplies $\ell+1\mid\sigma(n_j)$, divisible by $M$ and every earlier selected square. Subtraction negates the residue and keeps all earlier primes to exponent one; one may discard the last. All terms in the window are positive, and at least the first $J$ marks survive at $n_H$. Let $\varepsilon$ decrease to zero **after** the prime-parameter limit. Use $M=21$ for the first claim and $M=84$, $Y\ge7$ for the second. Every proper multiple of 84 grows; in fact its gain ratio exceeds $s(84)/84=5/3$.

**An arithmetic requirement even with unlimited waiting.** A landing prime $q$ at a strictly larger $C$-checkpoint cannot just be passed on by its immediate predecessor: if $s(z)=28q$, $q\ge97$ is prime, then $q\nmid z\sigma(z)$. Indeed, $q^2\mid z$ would give a proper divisor $q^2>28q$, except at $z=q^2$, which has the wrong sum. If $q\parallel z$ then $z$ cannot be odd: an odd predecessor of an even number is a square. Write $z=qb$ even. The divisor $z/2$ gives $b\le56$. But $28q=q\,s(b)+\sigma(b)$ gives $s(b)\le27$ and $q\mid\sigma(b)$, impossible since $\sigma(b)=b+s(b)\le83<q$. Finally $\sigma(z)=z+28q$. This excludes inheritance on the entering edge, not an occurrence of $q$ earlier on the orbit.

**What is missing.** We can certify a higher return and even an actual restart. We cannot force all the required factors to be regenerated indefinitely on one orbit, nor force a later replacement after a failed restart. The examples rule out those particular unconditional return rules; the density statement only rules out a uniform deadline on the specified families. Neither is a ceiling or a disproof of the aliquot conjecture. No RH, GRH, or simultaneous-prime conjecture is assumed. The [exact checks](../tests/test_six_28_higher_return.py) use factorization and independent divisor-pair sums, bounded per fixture (no stepped source exceeds $10^{10}$); they do not test a density limit. Run `python3 -m unittest discover -s tests -p 'test_six_28_higher_return.py' -v`.
