# Hilbert follow-up: the Lehmer five, drivers, and a known exit

**Result:** the concrete persistent patterns in the checked prefixes are
classical arithmetic drivers, not a constant Hilbert orientation. Drivers
need not be perfect. The published trajectory of 276 already leaves its
initial 28-driver phase, so that particular phase is not a permanent escape
certificate. **No new orbit extension, infinite closure, or novelty is claimed.**

This answers the follow-up to the [visual explanation](HILBERT-EXPLAINED.md).
It reuses seven existing local paths and a small, explicitly **published**
excerpt. It does not enlarge the census or the served site.

## 1. A driver need not be perfect

Some familiar drivers are perfect; others are multiperfect:

| D | Full divisor sum sigma(D) | Proper-divisor sum s(D) | sigma(D)/D |
| --- | --- | --- | --- |
| 6 | 12 | 6 | 2 |
| 28 | 56 | 28 | 2 |
| 120 | 360 | 240 | 3 |
| 496 | 992 | 496 | 2 |
| 672 | 2016 | 1344 | 3 |
| 523776 | 1571328 | 1047552 | 3 |

Thus 120, 672, and 523776 are **3-perfect**, not perfect. The guide/driver
framework is classical; see Guy–Selfridge,
[*What drives an aliquot sequence?* (1975)](https://doi.org/10.1090/S0025-5718-1975-0384669-X),
and the [existing literature boundary](README.md#6-initial-literature-map-not-a-comprehensive-review).
We are not defining every abundant divisor to be a driver, or giving a
classification of all guides by this table.

For any multiperfect core D with sigma(D)=kD, multiplicativity gives

```text
s(Du) = D [k sigma(u) - u],       provided gcd(D,u)=1.
```

This explains a one-step mechanism: D divides the successor, which exceeds
Du for u>1 and k>=2. It does **not** preserve the coprimality hypothesis, the
exact prime exponents of D, or the driver indefinitely. For example,

```text
120 -> 240 -> 504.
```

The first cofactor changes from 1 to 2. Reusing the coprime formula at u=2
would incorrectly give 840 rather than 504. Ordinary divisibility by a core,
exact driver membership, and permission to reuse a cofactor formula are
three different assertions.

## 2. What the existing local Lehmer-five prefixes actually show

The [Lehmer five](https://members.loria.fr/PZimmermann/records/aliquot.html)
are 276, 552, 564, 660, and 966. We replay only their already committed
[exact edges](../site/length-data.js), plus terminating controls 138 and 318.
Define precisely the two classes counted here:

```text
C6  = {n > 0 : n = 6  (mod 12)} = {v2(n)=1, 3 divides n},
C28 = {n > 0 : n = 28 (mod 56)} = {v2(n)=2, 7 divides n}.
```

Counts refer to **source terms** of checked transitions, excluding the last
known endpoint. They are not necessarily consecutive runs; terms outside
both classes are not being classified as driverless.

| Seed | Checked transitions | C6 sources | C28 sources | Local stop |
| --- | --- | --- | --- | --- |
| 276 | 79 | 0 | 71 | factorization_limit |
| 552 | 84 | 0 | 58 | factorization_limit |
| 564 | 115 | 32 | 5 | factorization_limit |
| 660 | 116 | 37 | 4 | factorization_limit |
| 966 | 94 | 28 | 56 | factorization_limit |
| 138 | 178 | 22 | 0 | terminated |
| 318 | 35 | 21 | 0 | terminated |

All seven checked paths visit all four terminal Hilbert states I,S,C,T.
This rejects a *constant orientation* description of these prefixes, not
subtler patterns involving several states. Terminating controls also have
driver phases: driver presence does not distinguish an escaping orbit.

The original computation limits remain **256 transitions per seed**, an
inclusive source cap of **10^30**, and **2,000,000 factorization work units
per source**. All five Lehmer paths stop at that factorization budget, not
at a known mathematical endpoint. These lengths are not current world
records, orbit survival probabilities, or evidence of divergence.

For 276, n_8=2716=28*97 starts a C28 phase. All 71 subsequent locally checked
transitions, through n_79, remain in C28. A run censored there cannot establish
that the phase persists forever.

## 3. The published 276 trajectory already supplies the counterexample

Set n_0=276. The [OEIS A008892 b-file](https://oeis.org/A008892/b008892.txt)
reports C28 membership at **every index 8 through 169**, followed by an exit
at **index 170**:

```text
n_169 = 7165455981799192761913565252   (v2 = 2)
n_170 = 7421365124006306789124764410   (v2 = 1).
```

The base-four suffix changes from `10` or `30` (exactly two factors of 2) to
`2` (exactly one). Both values are still divisible by 7, and this particular
exit step still increases. **Driver exit is not descent or termination.**

The [cached Clavier factorization](https://oeis.org/A008892/a008892.txt)
reports

```text
n_169 = 4 * 7^2 * p,
p = 36558448886730575315885537,       reported prime, p = 1 (mod 8).
```

For a prime p different from 7, the arithmetic explanation is exact:

```text
sigma(7^2 p) = 57(p+1),
s(4 * 7^2 * p) = 203p + 399.
```

If p=1 (mod 4), that successor is 2 modulo 4. The even exponent of 7 no
longer supplies powers of 2 through its divisor sum; the cofactor supplies
only one. A small independently checked example of the same mechanism is
**980=4*7^2*5 -> 1414**.

**Verification boundary:** the [committed excerpt](results/lehmer-276-published-prefix.json)
contains only published values at indices 0..170 and the reported
factorization at index 169, with source URLs and snapshot SHA-256 hashes.
Values 0..79 agree with the locally certified path. For the continuation,
tests check decimal integrity, residues, and the conditional product/sum
identity at the exit; they **do not certify the large reported prime or
all intervening aliquot edges**. The excerpt is attributed external evidence,
not a promotion of our 79-edge local computation to a 170-edge certificate.
No probable-prime shortcut is used, and no test downloads data.

## 4. The useful arithmetic condition, and the unchanged stopping point

Specializing the [existing supply/restoration law](FOUR-ADIC.md#2-a-stronger-positive-result-restoration-after-the-core-prime-is-hit),
write a C28 source as n=4*7^e*v, with e>=1 and gcd(v,14)=1. Then

```text
s(n) belongs to C28  iff  e is odd OR 8 divides sigma(v).
```

Indeed 7 always divides s(n). The successor retains exactly two factors of
2 iff the full divisor sum supplies more than two. For odd e,
`v2(sigma(7^e))=2+v2(e+1)>=3`; for even e it is zero. This gives the displayed
criterion. Restoring the **exact** exponent v7=1 after a spike additionally
requires 7 not to divide sigma(v); retaining the driver does not require that
extra condition.

Hilbert/base-four digits can label the source class or reveal its loss, but
they have not forced this supply condition at future steps. The long initial
28-driver phase of 276 is therefore not a new closed class. The published
exit is a concrete warning against treating that local pattern as permanent.

A useful next result would have to control driver loss **and** recovery:
find a nonempty arithmetic class reached by an explicit seed, prove a finite
actual return for every member, and prove that the returned value is larger
and satisfies the **same full entry conditions**. A repeated geometric state
or a profitable return to a weaker residue class is insufficient. The
[existing regeneration counterexamples](REGENERATION.md#3-why-these-blocks-do-not-compose)
already show those failures. This follow-up supplies no such closure and
stops here, rather than commissioning a larger plot or search.

## 5. Reproduce and audit

```sh
python3 -m unittest discover -s tests -p test_hilbert_drivers.py -v
```

The standard-library tests independently check the local prime factors by
deterministic trial division and enumerate divisors for every selected edge.
They reproduce the table above, check small coprime-core identities and their
failure after overlap, and keep the published continuation separate. Bounds
for additional arithmetic regressions are the six displayed cores with
1<=u<=39, and five small prime examples p in {5,13,17,29,37} of the exit family.

For an optional source-provenance audit, download the two cited OEIS text
files and compare their **complete-file** SHA-256 hashes with the fixture.
The fixture's `excerpt_sha256` separately hashes ASCII lines `index value\n`
for indices 0..170. The complete-file hashes are provenance, not offline
primality certificates; a changed upstream file needs explicit review rather
than silently refreshing the fixture. All new material remains outside
`site/`; no deployment or change to the solver is implied.
