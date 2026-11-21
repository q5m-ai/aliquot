# What Dirichlet GRH buys after an odd exit from driver 6

Can a prime-distribution theorem force an aliquot orbit below its starting value? For the [driver-6 exits](ODD-EXIT-DESCENT.md) $n_0=18p^2$, with $p\equiv11\pmod{12}$ prime, it can **select** seeds that drop sharply. The same theorem can select nearby seeds with increasingly long runs of growth. The distinction is between choosing a seed and controlling one already given.

**Conditional result.** Let $0<\varepsilon<1/2$ be fixed. Assuming GRH for Dirichlet $L$-functions, every sufficiently large interval of **prime parameters**

$$X<p\le X+X^{1/2+\varepsilon}$$

contains examples of both kinds, writing $n_{j+1}=s(n_j)=\sigma(n_j)-n_j$:

- **Drop:** $n_2/n_0=7/18+O_\varepsilon(1/\log\log X)$. The constant $7/18$ is a sharp asymptotic lower bound in this family.
- **Rise:** $n_0<n_1<\cdots<n_{h+1}$ with all $h+1$ successors odd, where $h=\lfloor\log\log X/(2\log 6)\rfloor$. Logs are natural. Even **without GRH**, for every fixed $h\ge1$ infinitely many primes in the family give such a rise. Thus replacing three steps by *any* fixed horizon cannot repair the previous descent argument.

## The analytic input

[Alpöge's announcement](https://alpo.ge/remark.pdf) includes the Dirichlet generalization, not just RH for the zeta function. The [pinned Lean entry point](https://github.com/1337isnot1337/riemann-hypothesis-solved/blob/9d5316ec73f5df89c4d95703ed106837b8a4060e/extracted/lean/src/Main.lean) declares `LFunction_eq_zero_re`; its [statement](https://github.com/1337isnot1337/riemann-hypothesis-solved/blob/9d5316ec73f5df89c4d95703ed106837b8a4060e/extracted/lean/src/Statements.lean) concerns zeros in the open critical strip for all Dirichlet characters. We have not verified the claimed proof. We use a **classical consequence** of that statement, not an analogy between theta lifts and aliquot steps.

Under Dirichlet GRH, uniformly for $3\le m\le t$ and $(a,m)=1$, the count of primes through $t$ in the class $a\bmod m$ satisfies

$$\pi(t;m,a)=\operatorname{li}(t)/\varphi(m)+O(\sqrt t\log t).$$

See [Ernvall-Hytönen and Palojärvi, *Explicit bound for the number of primes in arithmetic progressions assuming the Generalized Riemann Hypothesis*](https://arxiv.org/abs/2003.01925), Corollary 2. We use it twice:

1. If $m\le X^{\varepsilon/2}$, **every reduced class** has a prime in the stated window. Subtract the two counts: the main term is at least $X^{1/2+\varepsilon}/(m\log(2X))$, which dominates both errors.
2. A reduced class modulo $m$ has a prime $\ll m^3$: at $t=m^3$ the main term is $\gg m^2/\log m$, larger than the error for large $m$. Enlarge the constant for the finitely many small moduli.

## Selecting a two-step drop

Put $A(t)=7t^2+13t+13$. Multiplicativity gives $n_1=3A(p)>n_0$ and $3\nmid A(p)$, so $n_2=4\sigma(A(p))-3A(p)$. In particular $n_2\ge A(p)>7n_0/18$. To approach this floor we do **not** need $A(p)$ itself to be prime.

Take $y=c_\varepsilon\log X$ and $m=\operatorname{lcm}(12,\prod_{q\le y}q)$, the product over primes. By Chebyshev's bound $\sum_{q\le y}\log q=O(y)$, we can fix $c_\varepsilon>0$ small enough that $m\le X^{\varepsilon/2}$. Require $p\equiv-1\pmod{12}$ and $p\equiv-1\pmod q$ at all primes $q\le y$ **except 7**, where we take $p\equiv1\pmod7$. These conditions give a reduced class by the Chinese remainder theorem (CRT). Since $A(-1)=7$ and $A(1)=33$, no prime $q\le y$ divides $A=A(p)$ for the prime supplied in the window.

There are at most $\log A/\log y$ distinct prime divisors, each exceeding $y$. The finite Euler product for $\sigma(A)/A$ therefore gives

$$0\le\log\frac{\sigma(A)}A\le\sum_{q\mid A,\ q\text{ prime}}\frac1{q-1}\le\frac{\log A}{(y-1)\log y}=O_\varepsilon(1/\log\log X).$$

Exponentiate and use $n_2=A(4\sigma(A)/A-3)$ and $A/n_0=7/18+O(1/p)$. This proves the drop, and excludes each such seed from being the *least* escaping seed: its smaller second successor has the very same tail.

**What needs GRH here is the location, not the limiting ratio.** Without prescribing a window, let $y\to\infty$ and use [Linnik's least-prime theorem](https://arxiv.org/abs/0906.2749) in the same reduced class. It gives a prime $p\ll m^L$ for an absolute $L$. Since $p$ is coprime to $m$, $p>y$; since $\log m=O(y)$, $\log A(p)=O(y)$. The same divisor bound tends to zero, proving $\liminf n_2/n_0=7/18$ unconditionally over the prime parameters.

## Selecting a long rise on one orbit

We adapt [Lenstra's finite growth construction](GLOBAL.md) to the **quadratic** first image $3A(p)$. Start with an odd abundant divisor $D=3\cdot5\cdot7^2\cdot11=8085$, for which $s(D)=8331>D$. Impose $p\equiv29063\pmod{4D}$: its residues modulo $12,5,49,11$ are $11,3,6,1$. Since $A(3)=115$, $A(6)=343$, and $A(1)=33$, this ensures $D\mid n_1$. Every multiple $x$ of $D$ grows: scaling the proper divisors of $D$ gives $s(x)/x\ge s(D)/D>1$. The task is to *keep* that divisor at the next steps.

Set $r_0=1$. For $i=1,\ldots,h$ take a prime

$$r_i\equiv-1\pmod{4D r_{i-1}^2},\qquad r_i\equiv2\pmod{13}.$$

These form a reduced class since $13\nmid 4D r_{i-1}$; Dirichlet's theorem suffices for existence. The primes increase and are coprime to $4D$. Why can they divide $A(p)$? Its discriminant is $-195=-1\cdot3\cdot5\cdot13$. At $r=r_i$, the Legendre symbols of these four factors are respectively $-1,+1,+1,-1$ by quadratic reciprocity ($r\equiv-1\bmod 60$, $r\equiv2\bmod13$). The discriminant is thus a nonzero square mod $r$. As $r\nmid 2\cdot7\cdot13$, the roots are simple and nonzero. Of the $r$ lifts of a root $b$ modulo $r^2$, just one makes $A(b+kr)\equiv0\pmod{r^2}$, by the expansion $A(b)+krA'(b)\pmod{r^2}$. Pick any other lift for $p$. This forces $r_i\parallel n_1$ (exponent **exactly one**).

Combine the lifts and the base class for $p$ by CRT, with modulus $M=4D\prod_{i=1}^{h}r_i^2$. The resulting class is reduced, so for fixed $h$ it already contains infinitely many primes unconditionally.

Suppose $D\mid x$ and $r_1,\ldots,r_\ell$ each divide $x$ exactly once, with $\ell\ge1$. Then $r_1+1\mid\sigma(x)$ by multiplicativity, so $4D\mid\sigma(x)$. Consequently $D\mid s(x)$ and $s(x)\equiv-x\pmod4$. For each $i<\ell$, also $r_i^2\mid r_{i+1}+1\mid\sigma(x)$; subtracting $x$ preserves exponent one at $r_i$. This proves the induction: each step consumes just the *last guaranteed* prime. Starting at $x=n_1=3A(p)\equiv3A(-1)\equiv1\pmod4$, the next $h$ steps grow and retain odd parity. Together with $n_1>n_0$ this proves the fixed-horizon claim on actual iterates, not on unrelated edges.

For the window result, choose the least eligible $r_i$. The GRH bound above gives $r_i\ll(52D r_{i-1}^2)^3$, so $\log r_i\le6\log r_{i-1}+O_D(1)$. Iterating and summing yields $\log M=O_D(6^h)$. For the stated $h=h(X)$ this is $O_D(\sqrt{\log X})$, hence $M\le X^{\varepsilon/2}$ eventually. The window contains a prime in the constructed class. This use of a **uniform** estimate matters: Dirichlet's infinitude for each fixed class does not give a location when the modulus grows with $X$.

## Checks and stopping point

At $p=659$ the small-prime exclusions through 11 give $7817058\to9145641\to3068119$. For a growing example, $r_1=711479$ and $p=51342010523$ realize one link: $r_1\parallel n_1$ and $4D\mid r_1+1$, so the second term after the seed retains $D$. The [exact regressions](../tests/test_odd_exit_prime_windows.py) check only these two steps for each seed, by divisor pairs or by enumerating divisors from checked prime factors. They do not test an asymptotic or the announced proof. Run `python3 -m unittest discover -s tests -p 'test_odd_exit_prime_windows.py' -v`.

A prime in the next prescribed class generally starts a **different orbit**. No supply after the last link, or drop for an arbitrary fixed seed, follows from counting primes. To finish a descent proof one still needs resolution or a drop below the initial seed on its own orbit, at a time allowed to depend on the seed, including seeds outside this family. Neither a divergent orbit nor a proof of Catalan–Dickson is obtained.
