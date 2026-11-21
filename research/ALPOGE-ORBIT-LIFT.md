# Trying Alpöge’s amplifier on one aliquot orbit

**Outcome.** A nonprincipal Dirichlet character can carry the **exact growth of a given orbit**, and the finite-field amplifier in Alpöge’s archive really does amplify it. The missing step is an *independent upper bound*: the amplified value attains the full norm of our operator. We also tried the archive’s polynomial for removing unwanted components. It separates them exactly, but gives no size saving. In fact the family of amplified characters in this construction has a provably unavoidable common denominator. Neither RH nor GRH is assumed.

## What was taken from the proof work

[Alpöge’s announcement](https://alpo.ge/remark.pdf) describes gaining multiplicity by chaining theta lifts, then comparing divisibility with the cost of the lifts (pp. 1, 3–4). Rather than identify an aliquot step with an automorphic theta lift, we took two explicit operations from the released source:

- The [Gauss operator times its adjoint][gauss-proof], and the [scalar multiplication rule for a chain][chain] on a subspace preserved by the adjoints. The former has a subtraction term: the gain is **not** the same on constants and on nonprincipal characters.
- The polynomial [`PP`, with `KillerVal` and `KillerKills`][pp], and its [implementation][pp-proof]. It annihilates specified weights while retaining a known amount of divisibility at the surviving weight. This is a specific polynomial from the archive, not just an appeal to cancellation in prime counts.

The Gauss-sum algebra itself is classical. The orbit operators and polynomial weights below are our proposed specialization, not a claim from the archive. We inspected the cited source at commit `9d5316ec73f5df89c4d95703ed106837b8a4060e` and give the finite calculations below; we did not build or verify the full announced proof.

**Why not use the theta chain directly?** There is even a classical theta series for one aliquot step: let $a_m$ be one eighth of the number of integer four-square representations of $m$, the coefficient of $z^m$ in $(\sum_{k\in\mathbb Z}z^{k^2})^4/8$. [Jacobi’s four-square theorem](https://mathworld.wolfram.com/SumofSquaresFunction.html) gives $a_n=\sigma(n)$ for odd $n$. If $a_n-n$ is also odd and positive, the next step needs the coefficient **at index** $a_n-n$. This is not the linear operation of composing the archive’s [fixed lift kernels][kernels]. For example, $B(a)=a_{a_{15}-15}=a_9=13$, but $B(2a)=2a_{33}=96\ne2B(a)$. Scaling the input series is a test of linearity, not a second aliquot orbit. This blocks the direct identification, not a more elaborate encoding of a fixed series.

## Put the orbit growth on an amplified character

Start with **any actual block** $n_0=N,\ n_{j+1}=s(n_j)$ of length $h\ge1$, with every source $n_j>1$. A source equal to 1 already terminates. Set $Q=\prod_{j=0}^{h-1}n_j$. Choose a prime $q>Q$ congruent to $-1$ modulo $\operatorname{lcm}(8,Q)$ by Dirichlet’s theorem. It is the *probe* $q$ that depends on the block; the orbit never changes.

Every prime $r\mid Q$ is a square modulo $q$. For $r=2$ use $q\equiv7\pmod8$. For odd $r$, quadratic reciprocity gives $(r/q)=(-1)^{(r-1)/2}(q/r)=1$ since $q\equiv3\pmod4$ and $q\equiv-1\pmod r$. Thus the nonprincipal quadratic character $\xi=(\cdot/q)$ takes the value $+1$ on **every proper divisor** in the block.

On complex functions on $U=(\mathbb Z/q\mathbb Z)^\times$ let $R_a f(x)=f(ax)$. Use the actual proper divisors for the step operator, and the archive’s Gauss operator for the amplifier:

$$K_j=\frac1{n_j}\sum_{d\mid n_j,\ d<n_j}d R_d,\qquad G=\sum_{a\in U}e^{2\pi i a/q} R_a.$$

This uses the rank-one case of the archive’s identity, extending functions on $U$ by zero at the origin. With the ordinary counting inner product, $GG^*=qI-\sum_{u\in U}R_u$: the coefficient of $R_u$ is the sum of $e^{2\pi i(u-1)b/q}$ over $b\in U$. This is $q-1$ at $u=1$ and $-1$ elsewhere. Hence $GG^*$ has eigenvalue 1 on the constant character and $q$ on every nonprincipal character. These character lines are preserved by each step and its adjoint, so the scalar factors multiply, just as in the archive’s chain calculation.

In particular $K_j\xi=(n_{j+1}/n_j)\xi$. For the product $A_h=\prod_{j=0}^{h-1}(GG^* K_j)$ we obtain

$$ A_h\xi=q^h\frac{n_h}{N}\,\xi,\qquad \boxed{\|A_h\|_{2\to2}=q^h\frac{n_h}{N}}. $$

The equality of norms matters. Characters form an orthogonal basis, and on *any* character the absolute step multiplier of $K_j$ is at most $s(n_j)/n_j$ by the triangle inequality. The quadratic character attains equality at every step. A bound $\|A_h\|\le C(N)q^h$ for all such blocks would therefore bound the orbit and force termination or repetition. Multiplicity alone does not give that bound: dividing it out leaves **exactly the ratio we started with**.

## Can the archive’s polynomial separate a useful integral part?

For each character $\chi$ keep track of the divisor choices before summing. Write $\Omega(d)$ for the number of prime factors counted with multiplicity, $\Omega(1)=0$. Define

$$F_\chi(z)=\prod_{j=0}^{h-1}\ \sum_{d\mid n_j,\ d<n_j}d\,\chi(d)z^{\Omega(d)}.$$

Its degree is at most $R=\sum_{j<h}(\Omega(n_j)-1)$, since a proper divisor omits at least one prime factor. We have $F_\chi(0)=1$, whereas $F_\xi(1)/Q=n_h/N$. The constant term is integral and common to all characters. Can we keep that integrality *and* the full orbit signal?

Apply `PP` literally with an odd prime $\lambda$, the $\lambda$-adic unit $c=1+\lambda$, depth $e\ge0$, and weight set $\{1,\ldots,R\}$. On polynomials in $z$ use $T f(z)=f(cz)$; the weight-$i$ eigenvalue is $c^i$. Put $m=\lambda^e$. Taking $c$ integral lets us do the calculation over the cyclotomic integers containing the $\chi(d)$; equivalently extend coefficients at $\lambda$ to use the source’s module formulation. The polynomial is

$$P(X)=\left(\prod_{i=1}^{R}(X^m-c^{im})\right)(1+X+\cdots+X^{m-1}).$$

It kills every $z^i$ with $1\le i\le R$. It does **not** kill constants: $v_\lambda(P(1))=e+(1+e)R+v_\lambda(R!)$, since $v_\lambda(c^{im}-1)=1+e+v_\lambda(i)$ for odd $\lambda$. Thus $P(T)F_\chi=P(1)$: after removing the known scalar we have retained only the common coefficient 1, not the endpoint ratio. There is a natural repair: first translate $z\mapsto1+z$ so the desired value is the constant term. Then

$$P(T)[F_\chi(1+z)]=P(1)F_\chi(1).$$

The same divisibility gain now multiplies the desired value, but after dividing out $P(1)$ its size is unchanged. This calculation takes place on integral polynomials before the normalization by $Q$; it does not assume that $Q$ is a unit at $\lambda$.

## Why combining the amplified characters does not clear the intermediate terms

The archive’s [integral chain rule][integral] allows one clearing factor per step. Our factors are $n_j$, with product $Q$. On the single quadratic character they telescope: multiplying the normalized output by just $N$ suffices. Could that saving hold across the other amplified characters, giving more information than the one equality? For this probe the answer is sharp:

**The least positive integer clearing all the amplified eigenvalues on the odd characters is exactly $Q$.** Here “odd” means $\chi(-1)=-1$, and “clearing” means making each value an algebraic integer. This concerns the joint data after removing any known filter scalar $P(1)$, not an arbitrary selection of characters or choice of probe.

Indeed let $H=U^2$, of order $b=(q-1)/2$. Since $q\equiv7\pmod8$, $b$ is odd and $U=H\times\{1,-1\}$. Each character of $H$ has a unique odd extension; all these extensions have the $q^h$ gain. Expand $F_\chi(1)$ into terms $w\chi(w)$ where $w$ is the product of one proper divisor per step. Every $w$ lies in $H$ modulo $q$ and $1\le w<Q<q$. Only the all-ones choice gives $w\equiv1\pmod q$. By character orthogonality on $H$,

$$\sum_{\chi\ \mathrm{odd}} F_\chi(1)=b.$$

The eigenvalue of $A_h$ on each odd $\chi$ is $q^h F_\chi(1)/Q$. If $D$ times this value is integral for every odd $\chi$, their sum $D q^h b/Q$ is a **rational** algebraic integer, hence an integer. Now $q$ is coprime to $Q$ and so is $b$: for each odd $r\mid Q$, $b\equiv-1\pmod r$, and $b$ is odd. Thus $Q\mid D$. Conversely $D=Q$ works, since character values are roots of unity. The Gauss factors at $q$ therefore cannot pay a denominator at any prime dividing a source. If we keep the translated filter’s scalar, the same trace and converse give the joint denominator $Q/\gcd(Q,P(1))$: any saving comes from the scalar we multiplied in, not from a bound on the orbit.

**Exact check on one block, not a census.** On $12\to16\to15$ take $q=383$. The orbit is still above 12. The quadratic channel gives $383^2(5/4)$. Before amplification its denominator is only 4, but the joint odd-character denominator is $12\cdot16=192$ even after amplification. Here $F_\xi(z)=(1+5z+10z^2)(1+2z+4z^2+8z^3)$. With $\lambda=3,e=1$ the filter has $v_3(P(1))=12$: it preserves 1 before translation and 240 after translation, each times exactly $P(1)$. The [exact arithmetic tests](../tests/test_alpoge_orbit_lift.py) check this example and the small theta coefficients above. Run `python3 -m unittest discover -s tests -p 'test_alpoge_orbit_lift.py' -v`; the general argument does not rest on these checks.

**Stopping point.** The overlap with Dirichlet characters is real. It gives a faithful amplified measurement of one orbit, not a bound on that measurement. What we could not transfer is an independent height estimate for the retained component, of cost at most $C(N)q^h$, without already knowing $n_h$. The new automorphic estimates concern particular theta lifts and periods; these divisor operators have not been identified with those objects. This obstructs the attempted transplant, not all uses of the proof work, and it does not settle the aliquot conjecture.

**Follow-up:** [A determinant bound and a restriction on record growth](ALPOGE-RECORD-HEIGHT.md). The archive’s determinant rule does yield a uniform saving, but its map-height condition uses the largest multiplier instead. An Euler factorization on that multiplier bounds what new records can be reached without repeatedly using the same odd primes.

[kernels]: https://github.com/1337isnot1337/riemann-hypothesis-solved/blob/9d5316ec73f5df89c4d95703ed106837b8a4060e/extracted/lean/src/Formalism/ThetaLiftIndependence/Statement.lean#L10-L30
[gauss-proof]: https://github.com/1337isnot1337/riemann-hypothesis-solved/blob/9d5316ec73f5df89c4d95703ed106837b8a4060e/extracted/lean/src/Formalism/LogVandermondeBounds/LogVandermondeProofs/FourierIsometryOnNormKernel.lean#L84-L113
[chain]: https://github.com/1337isnot1337/riemann-hypothesis-solved/blob/9d5316ec73f5df89c4d95703ed106837b8a4060e/extracted/lean/src/Formalism/ThetaLiftIndependence/Statement.lean#L244-L251
[integral]: https://github.com/1337isnot1337/riemann-hypothesis-solved/blob/9d5316ec73f5df89c4d95703ed106837b8a4060e/extracted/lean/src/Formalism/ThetaLiftIndependence/Statement.lean#L40-L46
[pp]: https://github.com/1337isnot1337/riemann-hypothesis-solved/blob/9d5316ec73f5df89c4d95703ed106837b8a4060e/extracted/lean/src/Formalism/WindowSums/Statement.lean#L104-L122
[pp-proof]: https://github.com/1337isnot1337/riemann-hypothesis-solved/blob/9d5316ec73f5df89c4d95703ed106837b8a4060e/extracted/lean/src/Formalism/WindowSums/PowerSeriesRelationList.lean#L15-L18
