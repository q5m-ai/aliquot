# KaTeX 0.19.0

Self-hosted browser bundle from https://registry.npmjs.org/katex/-/katex-0.19.0.tgz
(MIT; see the [vendored license](../../site/vendor/katex/LICENSE)). Only
`dist/katex.min.js` and the upstream license belong in the served directory.
This provenance note stays outside `site/` so managed static previews do not
expose source documentation.
No package installation or CDN access is required by the website.

Upstream tarball integrity (verified before extraction):

```
sha512-v6Tznz3zJ7u3niRCoDTsumM2+HA2XXcCu+WAacCeHD2z3p9A9Ks987o5FzfTGBN0e8A0vjEgIDvLbICrXpdw/Q==
```

Vendored bundle SHA-256:

```
103a53763cc033bba8d175bf3f0ba597c3505c9b6747dd3f2c7bc2a6bfcc8ae7
```

`site/latex.js` uses MathML-only output, not KaTeX's HTML/CSS renderer. Native
MathML uses browser math fonts, so the CSS/font assets are deliberately omitted.
Keep trust disabled, use explicit TeX fields, and preserve readable fallback text.
When upgrading, verify the new package integrity, review the output for the
formulas actually used, update the pinned hash test, and run the full suite.
