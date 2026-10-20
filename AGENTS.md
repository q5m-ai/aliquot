# Aliquot research

- This is a q5m research project about aliquot sequences and possible proof/disproof of the aliquot sequence conjecture. Do not claim a proof, disproof, or divergent sequence from a finite computation.
- Keep exact arithmetic, explicit computation bounds, reproducible experiments, and independent verification separate from conjectural reasoning.
- `site/` is the only served directory. Never serve the repository root, source research data, private configuration, or credentials.
- Keep `favicon.svg` and `site/favicon.svg` identical; the root icon is for Paseo discovery.
- Use isolated Git worktrees; keep the canonical checkout clean on `main`.
- Run `npm test` and `node --check site/explorer.js` before committing changes.
- Hosting and fleet registration are independent acceptance gates. Never infer live deployment from a commit, project registration, or CI success.
- PR #1 owns the initial interactive testing site milestone. Subsequent mathematical work belongs in later changes.
