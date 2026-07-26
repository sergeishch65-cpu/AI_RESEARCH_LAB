# Logbook

Study logbook for `repro-colorful-pinball-targeted`.

## Current State

- Start UTC: `2026-07-25T00:34:00Z`
- End UTC: `2026-07-25T02:02:06Z`
- Official article identity recovered from primary sources.
- Diamond appendix tables extracted from the official arXiv HTML/PDF.
- Official repository fixed commit confirmed at detached HEAD `98ce4fa0c851a9bfdedb609f82d4847f6e666def`.
- Source materials saved under `source_materials/original_article/`.
- Article provenance, source manifest, and search log created.
- Diamond comparison artifacts regenerated from primary sources.
- Volume/Size mapping audited and confirmed as a renamed same metric for Diamond.
- No benchmark was rerun.
- No vendor code, dataset, configuration, or wrapper files were modified.


- Detailed Diamond validation, verdict, and evidence artifacts generated.
- Pair-level verdicts, winner comparison, rank-shift analysis, discrepancy hypotheses, and claim matrix written to `analysis/diamond/`.
- Statistical reproduction plan written to `planning/`.
- No benchmark was rerun.
- No vendor code, dataset, configuration, or wrapper files were modified.


- Diamond statistical execution stage packaged from the completed 20-seed control run.
- Immutable run directory created at `execution/diamond_statistical/runs/run-001-seed-42` with run spec, command, environment, logs, result manifest, and validation artifacts.
- No new benchmark was launched during this continuation because the authoritative completed control run was already present in the workspace.
- Diamond statistical sample completion review added, confirming that the approved 20-seed sample is fully represented by the immutable control run.
- The official entrypoint still exposes no supported external seed override, so no extra seed-specific reruns were added.

## Notes

- Detailed Diamond pair-level audit completed.
- Pair-level verdicts, winner comparison, rank-shift analysis, discrepancy hypotheses, claim audit, evidence matrix, and statistical plan were regenerated to exact objective schemas.
- No benchmark was rerun.

- Recovered sources:
  - arXiv HTML v5 and PDF for the paper.
  - Official repository README, main entry point, metrics implementation, and license at the fixed commit.
  - The paper's appendix tables 6-11 were used for Diamond extraction.
  - `Cov` remains reproduction-only because the paper does not numerically tabulate it in the Diamond appendix tables.
  - The paper publishes additional delta ablations that are not present in the current reproduction file.


## COLORFUL_PINBALL_FINAL_PUBLICATION_REPORT

- Final publication package created for Diamond only.
- Main Russian report, public Russian summary, English executive summary, machine-readable verdict, citation map, publication manifest, and evidence validation files were written under `publication/`.
- Report and manifest self-hash references were removed, then publication hashes were revalidated against the final stable bundle.
- Publication validation passed: primary PDF hash verified, statistical plan hash verified, immutable run bundle verified, locked inputs unchanged, JSON/CSV parsing passed, and scope remains Diamond only.
- No benchmark rerun, no vendor/dataset/config/wrapper changes, no commit/tag/push.
