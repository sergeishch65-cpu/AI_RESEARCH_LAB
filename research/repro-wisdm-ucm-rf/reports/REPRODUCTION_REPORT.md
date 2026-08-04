# Reproduction Report

## 1. Executive Summary

This report documents the first local reproduction study for *Conformal Prediction in Multi-User Settings: An Evaluation* on the WISDM Activity Prediction v1.1 transformed dataset. The tested claim compares user-calibrated conformal prediction (UCM) against user-independent conformal prediction (UIM) with a Random Forest base model and MAPIE LAC under a fixed 20-seed CPU-only protocol.

The study status is `REPRODUCED`. The main result is that UCM achieved empirical coverage of `0.967825` versus `0.889386` for UIM, while UCM also produced larger prediction sets (`2.117496` versus `1.387277`). The effect is consistent across all 20 iterations and matches the paper direction, but at the cost of lower set-efficiency. Confidence is `HIGH` because the measured values match the predeclared tolerances, the first-run control hashes match, and the raw-result mirrors are complete and internally consistent.

## 2. Reproduction Target

- Source paper: *Conformal Prediction in Multi-User Settings: An Evaluation*  
- Official paper URL: <https://arxiv.org/abs/2312.05195>  
- Claim ID: `wisdm-ucm-rf-coverage-v1`  
- Claim: under the official WISDM preprocessing and the paper's UCM/UIM protocol, a Random Forest base model with MAPIE LAC should reproduce the reported user-calibrated coverage uplift on WISDM, with UCM outperforming UIM on empirical coverage while also increasing mean prediction set size.

### Paper claim

The paper reports the following WISDM reference values:

- UCM empirical coverage: `0.9628`
- UIM empirical coverage: `0.8876`
- UCM average prediction set size: `2.04`
- UIM average prediction set size: `1.39`

### Local operationalization in AI_RESEARCH_LAB

- Study ID: `repro-wisdm-ucm-rf`
- Task: 6-class multi-user activity recognition
- Model: `RandomForestClassifier(n_estimators=50, random_state=seed, n_jobs=1)`
- Conformal method: `SplitConformalClassifier(confidence_level=0.95, conformity_score="lac")`
- Comparator: UIM
- Repetitions: 20
- Seeds: `101..120`
- Success criteria:
  - UCM coverage within `±0.0100` of the reference value
  - UIM coverage within `±0.0100` of the reference value
  - UCM set size within `±0.20` of the reference value
  - UIM set size within `±0.20` of the reference value
  - UCM coverage greater than UIM coverage
  - required artifacts present and checksum-valid

## 3. Dataset

- Dataset: WISDM Activity Prediction v1.1 transformed dataset
- Official dataset URL: <https://www.cis.fordham.edu/wisdm/dataset.php>
- Raw archive URL: <https://www.cis.fordham.edu/wisdm/includes/datasets/WISDM_ar_v1.1.tar.gz>
- Local raw archive path: `research/repro-wisdm-ucm-rf/data/raw/wisdm/WISDM_ar_v1.1.tar.gz`
- Local transformed ARFF path: `research/repro-wisdm-ucm-rf/data/raw/wisdm/WISDM_ar_v1.1/WISDM_ar_v1.1_transformed.arff`
- Local processed CSV path: `research/repro-wisdm-ucm-rf/data/processed/wisdm/WISDM_ar_v1.1_transformed_processed.csv`

### Dataset checksums

- Archive SHA-256: `e573791269aab4a629721cf04b6031b7cbf8e14261cd2bc86e65887a2bc592d7`
- ARFF SHA-256: `b083abfe759dea1b8f5eae01f2bef135bbecb25246c8d1eb52afdbfadd3e883a`
- Processed CSV SHA-256: `abe6875e17d0befa8b0aad804b75bc068784e6f1051004f2ca3bfe3678b15aae`

### Dataset shape and filtering

- Rows after filtering: `2869`
- Users after filtering: `16`
- Retained user IDs: `3, 5, 7, 12, 13, 18, 19, 20, 21, 27, 29, 31, 32, 33, 34, 36`
- Number of features: `39`
- Target variable: `label`
- User identifier: `userid`
- Filtering applied:
  - dropped corrupted columns `1, 33, 36, 37, 38`
  - kept only complete-activity users
  - excluded users `6` and `24`
  - preserved the processed file order

## 4. Experimental Protocol

- Seeds: `101, 102, ..., 120`
- Iterations: `20`
- Target-user logic: one retained user is selected as the target user in each evaluation round

### Split protocol

- UCM:
  - train on `60%` of non-target-user rows
  - use the target user as the calibration/test source
  - split target-user rows `50/50` into calibration and test halves
- UIM:
  - train on `60%` of non-target-user rows
  - use non-target-user calibration data
  - test on the target-user rows

### Model and conformal settings

- Random Forest parameters: `n_estimators=50`, `random_state=seed`, `n_jobs=1`
- MAPIE parameters: `SplitConformalClassifier(confidence_level=0.95, conformity_score="lac")`
- Confidence level: `0.95`
- Conformity score: `lac`

### Reproducibility controls

- fixed seed schedule
- CPU-only execution
- no synthetic replacement of WISDM data
- no rerun of the experiment during report finalization
- full raw-result preservation before aggregation

## 5. Implementation

- Main runner: `src/ai_research_lab/studies/first_reproduction/runner.py`
- Study package: `src/ai_research_lab/studies/first_reproduction/`
- Reused laboratory infrastructure:
  - existing challenge/reporting contracts
  - study-local artifact layout
  - logbook and registry conventions
  - verifier-normalized volatile metadata handling
- Dependencies used by the local run:
  - `numpy`
  - `pandas`
  - `scikit-learn`
  - `mapie`
- The implementation was local and executed in the project workspace.
- Synthetic replacement was not used; the study consumed the official WISDM archive and its transformed ARFF representation.

## 6. Data Integrity and Verification

### Raw-result completeness

| Item | Value |
| --- | ---: |
| `raw_results.csv` rows | `57600` |
| `raw_results.json` rows | `57600` |
| UCM rows | `28800` |
| UIM rows | `28800` |
| Iterations | `20` |

### Integrity checks

- No critical discrepancies were found between `raw_results.csv`, `raw_results.json`, `metrics.json`, `experiment_result.json`, `LOGBOOK.md`, and `RESULTS_ANALYSIS.md`.
- The control SHA-256 values matched exactly for:
  - `experiment_result.json`
  - `metrics.json`
  - `LOGBOOK.md`
  - `REPRODUCTION_REPORT.md`
- `pytest` passed: `31 passed`
- `ruff check .` passed
- `git diff --check` passed

### Verifier note

The older mixed verifier interface was not applied directly to this study format because the study already uses a study-local artifact contract and a normalized reporting pipeline. The verification here therefore relies on the existing study artifacts, checksum matches, and the established logbook/report contract rather than on an older standalone verifier entrypoint.

## 7. Results

| Metric | UCM | UIM | Difference | Reference | Tolerance | Verdict |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Empirical coverage | `0.9678248900` | `0.8893864324` | `0.0784384576` | UCM `0.9628`, UIM `0.8876` | `±0.0100` | PASS |
| Average prediction set size | `2.1174957415` | `1.3872772392` | `0.7302185023` | UCM `2.04`, UIM `1.39` | `±0.20` | PASS |

### Interpretation

The study reproduces the paper's direction: UCM delivers higher empirical coverage than UIM. The trade-off is that UCM does so with larger prediction sets, which means improved coverage comes at the cost of reduced set efficiency. Both metrics remain within the declared tolerances, so the reproduction succeeds under the local protocol.

## 8. Statistical Analysis

The statistical analysis uses the 20 paired iterations and the already recorded aggregated values.

### Coverage uplift

- mean = `0.0784384576`
- standard deviation = `0.0136290250`
- 95% CI = `[0.0724653838, 0.0844115314]`
- exact sign-test p-value = `1.9073486328125e-06`

### Prediction set size difference

- mean = `0.7302185023`
- standard deviation = `0.1158415013`
- 95% CI = `[0.6794496588, 0.7809873458]`
- exact sign-test p-value = `1.9073486328125e-06`

Additional facts:

- paired iterations: `20`
- all paired iteration deltas were positive for coverage
- all paired iteration deltas were positive for prediction set size
- the p-value is not the sole basis for the verdict
- the main basis is agreement between observed effect, specification tolerances, and reference values

The effect is descriptive for the studied protocol and should not be interpreted as causal.

## 9. Scientific Interpretation

### 9.1 Confirmed

- UCM increased empirical coverage relative to UIM.
- The effect was stable across all 20 iterations.
- The mean values fell inside the specification tolerances.
- The reproduction criteria were satisfied.

### 9.2 Trade-off

- UCM increased prediction set size.
- The higher coverage was obtained at the cost of lower efficiency.
- UCM is not unconditionally better across all criteria.
- Practical usefulness depends on the acceptable prediction set size.

### 9.3 Not Established

- Universal validity for other datasets is not established.
- Universal validity for other models is not established.
- Other conformal methods were not tested.
- External validation was not performed.
- Superiority in all possible conditions was not demonstrated.

## 10. Reproduction Criteria

| Criterion | Required | Actual | Verdict | Evidence |
| --- | --- | --- | --- | --- |
| UCM coverage tolerance | `0.9628 ± 0.0100` | `0.9678248900` | PASS | `results/metrics.json` |
| UIM coverage tolerance | `0.8876 ± 0.0100` | `0.8893864324` | PASS | `results/metrics.json` |
| UCM set-size tolerance | `2.04 ± 0.20` | `2.1174957415` | PASS | `results/metrics.json` |
| UIM set-size tolerance | `1.39 ± 0.20` | `1.3872772392` | PASS | `results/metrics.json` |
| Raw-result completeness | complete raw mirrors for both formats | 57,600 rows in each raw mirror | PASS | `experiments/wisdm_ucm_uim_rf/raw_results.csv`, `experiments/wisdm_ucm_uim_rf/raw_results.json` |
| Deterministic seed protocol | fixed seeds `101..120` | fixed seeds `101..120` | PASS | `experiment_result.json`, `metrics.json` |
| Real dataset use | official WISDM archive and transformed ARFF | yes | PASS | `paper/data_manifest.json` |
| No synthetic replacement | no replacement data | yes | PASS | `paper/data_manifest.json`, `LOGBOOK.md` |

## 11. Limitations

- one dataset
- 16 retained users
- 20 seeds
- transformed WISDM representation
- one Random Forest configuration
- one MAPIE LAC configuration
- one split protocol
- no other models
- no other conformal methods
- no external validation
- verifier interface does not directly model this study format

## 12. Reproducibility Artifacts

| Artifact | Path | SHA-256 | Purpose |
| --- | --- | --- | --- |
| Source record | `research/repro-wisdm-ucm-rf/paper/source_record.json` | `c798e5f91cbc2d702f3e2fd8801686abf25b09a901c4303ebbaa17a1a4097d8e` | source metadata and evidence |
| Data manifest | `research/repro-wisdm-ucm-rf/paper/data_manifest.json` | `9d7904c005643c0bb20a8bbfd91ffc90114d3afeb33f43ca64c06ddfb96e9db8` | dataset and processing contract |
| Claim | `research/repro-wisdm-ucm-rf/claims/claim.json` | `d451d71a5ce62561d4641d52cb29c7a8d0402026372d49a48f86df162587998d` | machine-checkable claim |
| Experiment plan | `research/repro-wisdm-ucm-rf/plans/experiment_plan.json` | `25134f82991ef1e5708df50c25d74a1468e5568783def949effb9de9db99d542` | protocol definition |
| Raw archive | `research/repro-wisdm-ucm-rf/data/raw/wisdm/WISDM_ar_v1.1.tar.gz` | `e573791269aab4a629721cf04b6031b7cbf8e14261cd2bc86e65887a2bc592d7` | official data source |
| Transformed ARFF | `research/repro-wisdm-ucm-rf/data/raw/wisdm/WISDM_ar_v1.1/WISDM_ar_v1.1_transformed.arff` | `b083abfe759dea1b8f5eae01f2bef135bbecb25246c8d1eb52afdbfadd3e883a` | paper-aligned input file |
| Processed CSV | `research/repro-wisdm-ucm-rf/data/processed/wisdm/WISDM_ar_v1.1_transformed_processed.csv` | `abe6875e17d0befa8b0aad804b75bc068784e6f1051004f2ca3bfe3678b15aae` | filtered dataset used by the runner |
| Raw results CSV | `research/repro-wisdm-ucm-rf/experiments/wisdm_ucm_uim_rf/raw_results.csv` | `7f3b9fee36dc15acc6e788205e749e6255a03dd4c42632fdcbf76d555e75f486` | row-level predictions and sets |
| Raw results JSON | `research/repro-wisdm-ucm-rf/experiments/wisdm_ucm_uim_rf/raw_results.json` | `31404f14c27ffe9f9c32dd2c5b5d91bba59fbe2925c6e72a0ba84c9ee178c6f5` | structured raw-result mirror |
| Metrics | `research/repro-wisdm-ucm-rf/results/metrics.json` | `f37a491f03c55d8e689334fcd72b150f66dc4ea1a7760d5d8f8a88461f9e8f3e` | study-level numerical summary |
| Experiment result | `research/repro-wisdm-ucm-rf/experiments/wisdm_ucm_uim_rf/experiment_result.json` | `445a2c13258b108b3b305be6e03849e1c37937efa40c294c40315dc55aef7f3b` | execution summary and environment |
| Logbook | `research/repro-wisdm-ucm-rf/logbook/LOGBOOK.md` | `2c52adaa33f8548b77cf93671e01e6c87d82ca872310e54a1b60c271608c7a58` | narrative laboratory log |
| Results analysis | `research/repro-wisdm-ucm-rf/analysis/RESULTS_ANALYSIS.md` | `d8fbfd042e23df193f1ad8f69f14c9f4cb610e90811d3ae4fa8a5bd8040c7ea4` | independent consistency analysis |
| Final report | `research/repro-wisdm-ucm-rf/reports/REPRODUCTION_REPORT.md` | to be recorded in the final Codex response | final human-readable report |

## 13. Final Verdict

Scientific status: `REPRODUCED`

Confidence: `HIGH`

Basis:

- real dataset
- complete first run
- verified artifacts
- matching hashes
- reference tolerances passed
- positive paired effects across all iterations
- independent results analysis completed

This reproduction supports the tested claim under the exact local protocol used here; it does not establish universal validity beyond this configuration.
