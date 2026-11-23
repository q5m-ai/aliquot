# Three odd steps after leaving driver 6: do they force descent?

[Notebook 01](README.md#2-a-growing-class-with-an-exact-exit-criterion) identifies the odd exits from the growing class $n\equiv6\pmod{12}$: they are twice an odd square divisible by 9. Consider the subfamily

$$C=\{18p^2 : p\text{ prime},\ p\equiv11\pmod{12}\}.$$

It is infinite by Dirichlet's theorem on reduced progressions. Write $n_0=n$, $n_{j+1}=s(n_j)=\sigma(n_j)-n_j$ while $n_j>0$.

**Candidate fixed before testing:** for every $n\in C$, some $1\le j\le 3$ has $n_j=0$, $n_j=n_i$ for some $i<j$, or $n_j<n$. If true, no member of $C$ could be the least escaping seed: a smaller term would have the same escaping tail. There is no one-step descent here; every seed in $C$ is a proper multiple of the perfect number 6 and grows at the first step.

## Smallest counterexample: $p=6803$

| $j$ | $n_j$ | Prime factorization of the source | $s(n_j)$ |
|---:|---:|---|---:|
| 0 | 833054562 | $2\cdot3^2\cdot6803^2$ | 972162345 |
| 1 | 972162345 | $3\cdot5\cdot7\cdot11\cdot401\cdot2099$ | 972874455 |
| 2 | 972874455 | $3\cdot5\cdot7\cdot29\cdot319499$ | 867445545 |

All three successors are distinct and above the seed. The last step **decreases**, but not below the seed. This refutes the three-step claim, not Catalan–Dickson. The test here stops at three steps; the [fixed-seed continuation](ODD-EXIT-FIXED-SEEDS.md) reaches zero at step nine.

**Search and reproduction.** Test primes in increasing order, $11\le p\le 50000$ inclusive, stopping each trace at the first event or step three, and the search at the first counterexample. Of the 218 primes in the progression through 6803, 212 first fell below the seed on step two and five on step three. Since $18p^2$ increases with $p$, this proves minimality within $C$. The [test](../tests/test_odd_exit_descent.py) uses the repo's exact trial factorization (2,000,000 work units per call), with an inclusive $10^{12}$ cap on sources stepped. Divisor-pair enumeration independently checks primality decisions and every edge, including the controls $6\to6$, $220\to284\to220$ and $1\to0$. No incomplete factorizations or cap hits; a limit aborts the check rather than classifying the seed.

```sh
python3 -m unittest discover -s tests -p 'test_odd_exit_descent.py' -v
```

## What propagates, and what does not

Put $A=7p^2+13p+13$. Multiplicativity gives $n_1=39(p^2+p+1)-18p^2=3A$. Since $p\equiv-1\pmod{12}$, $A\equiv7\pmod{12}$. In particular $3\nmid A$, so

$$n_2=4\sigma(A)-3A=A+4s(A)\equiv3\pmod4.$$

An odd integer congruent to 3 modulo 4 has a prime factor $q\equiv3\pmod4$ to an odd exponent $e$. Pairing consecutive powers shows $q+1\mid\sigma(q^e)$, hence $4\mid\sigma(n_2)$. Thus **every** seed in $C$ has successors congruent to **1, 3, 1 modulo 4**. But descent on step two requires $4s(A)<18p^2-A$; on step three it requires $\sigma(n_2)<n_2+18p^2$. The residue information does not bound either sum tightly enough. At $p=11$, $A=17\cdot59$ and $2178\to3009\to1311$ already descends. At 6803 the same residues allow both inequalities to fail, as the factorizations show.

[Alpöge's announcement](https://alpo.ge/remark.pdf) (p. 1) describes chaining theta lifts to gain multiplicity for a von Mangoldt sum. We took only the question of what is retained at each step. No aliquot step is identified with a lift; neither RH, GRH nor any lemma from the [pinned archive](https://github.com/1337isnot1337/riemann-hypothesis-solved/tree/9d5316ec73f5df89c4d95703ed106837b8a4060e) is assumed or verified here. The orbit information obtained is elementary: an estimate averaged over primes would not control $\sigma(A)$ at a specified $p$. A proof by descent still needs a drop below the *starting seed* (or resolution), both for orbits like the witness beyond step three and for those that never visit $C$.

**Follow-up:** [Selecting drops and long rises with prime-distribution estimates](ODD-EXIT-PRIME-WINDOWS.md) rules out *every* fixed descent horizon in this same family, not just three steps.
