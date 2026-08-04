# First Reproduction Specification

Date: 2026-07-24

## 1. Document Status

- Status: `planning-only`
- Decision gate: `READY_FOR_SKELETON`
- Scope: first local reproduction study only, no implementation yet
- Non-goals: no code, no dataset download, no notebook execution, no study directory creation, no publication, no submission

## 2. Study Identity

| Field | Value | Fact type |
| --- | --- | --- |
| Study ID | `repro-wisdm-ucm-rf` | `ENGINEERING_DECISION` |
| Paper | `Conformal Prediction in Multi-User Settings: An Evaluation` | `PAPER_FACT` |
| Primary dataset | WISDM Activity Prediction v1.1 transformed dataset | `PAPER_FACT` + `CODE_FACT` |
| Local objective | Reproduce one quantitative WISDM claim with the smallest viable CPU-only protocol | `ENGINEERING_DECISION` |

## 3. Primary Sources

### 3.1 Paper

- Official paper URL: <https://arxiv.org/abs/2312.05195>
- Supporting HTML source used for table inspection: <https://arxiv.org/html/2312.05195v1>
- Relevant paper sections:
  - Section 4.1 / 4.5 for the WISDM dataset summary and experimental setup
  - Tables 8 and 9 for UIM and UCM WISDM results

### 3.2 Official code

- Official repository: <https://github.com/enriquegit/conformal-prediction-multiuser>
- Repository owner: `enriquegit`
- Default branch: `main`
- License: `GPL-3.0`
- Relevant files:
  - `README.md`
  - `notebooks/globals.py`
  - `notebooks/run_ui-model.ipynb`
  - `notebooks/run_uc-model.ipynb`
  - `notebooks/run_ud-model.ipynb`
  - `notebooks/run_mixed-model.ipynb`
  - `format-datasets/format-wisdm.R`
  - `format-results/run_format.R`
  - `format-results/format_results_functions.R`

### 3.3 Official dataset source

- Official dataset page: <https://www.cis.fordham.edu/wisdm/dataset.php>
- Selected dataset file: `WISDM_ar_v1.1_transformed.arff`
- Why this version:
  - the repository formatter names this file explicitly;
  - the paper's WISDM summary matches the transformed dataset footprint;
  - the dataset page exposes the transformed Activity Prediction dataset as an official WISDM resource

## 4. Fact Separation

### 4.1 PAPER_FACT

- The paper evaluates four multi-user strategies: MM, UDM, UIM, UCM.
- The paper evaluates four classifiers: Naive Bayes, Random Forest, SVM, KNN.
- The paper runs the experiments 20 times.
- The paper sets conformal confidence to 0.05.
- The paper reports WISDM table values for UIM and UCM.

### 4.2 CODE_FACT

- `notebooks/globals.py` fixes:
  - `DATASET_NAME = "wisdm"`
  - `PCT_TRAIN = 0.6`
  - `PCT_CALIBRATION = 0.50`
  - `PCT_TARGET_TEST = 0.5`
  - `ITERATIONS = 20`
  - `ALPHA = 0.05`
- `notebooks/run_ui-model.ipynb` and `notebooks/run_uc-model.ipynb` use:
  - `train_test_split(..., train_size=PCT_TRAIN, stratify=...)`
  - `MinMaxScaler` fit on training data only
  - `MapieClassifier(estimator=..., cv="prefit", method="score", random_state=random_seed)`
  - `compute_pvalues` with LAC-style nonconformity scores
- `format-datasets/format-wisdm.R` uses:
  - `WISDM_ar_v1.1_transformed.arff`
  - removal of corrupted columns `1, 33, 36, 37, 38`
  - retention of users who performed all activities
  - exclusion of users `6` and `24`
  - `write.csv(..., "data.csv")`
- `format-results/format_results_functions.R` defines:
  - coverage as fraction of prediction sets containing the ground-truth label
  - average set size as mean cardinality of prediction sets
  - per-iteration and per-user aggregation
  - mean and standard deviation across iterations

### 4.3 ENGINEERING_DECISION

- The minimal claim will use only the RF classifier.
- The minimal claim will compare only UCM against UIM.
- The minimal claim will not require the mixed model, UDM, KNN, SVM, or Naive Bayes.
- The minimal claim will not require the R plotting workflow.

## 5. Exact Reproduction Claim

### 5.1 Machine-checkable claim

| Field | Specification | Fact type |
| --- | --- | --- |
| Claim ID | `wisdm-ucm-rf-coverage-v1` | `ENGINEERING_DECISION` |
| Paper | `Conformal Prediction in Multi-User Settings: An Evaluation` | `PAPER_FACT` |
| Dataset | WISDM Activity Prediction v1.1 transformed dataset | `PAPER_FACT` + `CODE_FACT` |
| Subset | Users retained by the formatter: complete-activity users excluding 6 and 24 | `CODE_FACT` |
| Population / users | All retained users, one target user at a time | `PAPER_FACT` + `CODE_FACT` |
| Task | 6-class multi-user activity recognition | `PAPER_FACT` |
| Model | `RandomForestClassifier(n_estimators=50, random_state=seed)` | `CODE_FACT` |
| Conformal method | `MapieClassifier(cv="prefit", method="score")` with LAC scores and `alpha=0.05` | `CODE_FACT` |
| Comparator | User-independent model (`UIM`) with the same base model and seed policy | `PAPER_FACT` + `CODE_FACT` |
| Primary metric | Conformal coverage | `PAPER_FACT` + `CODE_FACT` |
| Secondary metric | Mean prediction set size | `PAPER_FACT` + `CODE_FACT` |
| Reported result | `UCM RF coverage = 96.28 ± 0.62`, `UCM RF set size = 2.04 ± 0.09`; `UIM RF coverage = 88.76 ± 1.35`, `UIM RF set size = 1.39 ± 0.04` | `PAPER_FACT` |
| Expected direction | `UCM coverage > UIM coverage`; `UCM set size > UIM set size` | `ENGINEERING_DECISION` grounded by `PAPER_FACT` |
| Tolerance | Coverage mean absolute tolerance `±1.0 percentage points`; set-size mean absolute tolerance `±0.2` | `ENGINEERING_DECISION` |
| Repetitions | 20 iterations | `PAPER_FACT` + `CODE_FACT` |
| Seed policy | `random_seed = 100 + iteration`, iterations `1..20` | `CODE_FACT` |

### 5.2 Claim sentence

Under the official WISDM preprocessing and the paper's UCM/UIM protocol, a Random Forest base model with MAPIE LAC should reproduce the reported user-calibrated coverage uplift on WISDM: UCM should average about 96.28% coverage versus about 88.76% for UIM, with corresponding mean prediction set sizes of about 2.04 and 1.39 respectively, using 20 fixed seeds.

### 5.3 Source evidence for the claim

- Paper Table 8: UIM WISDM results
- Paper Table 9: UCM WISDM results
- `notebooks/run_ui-model.ipynb`
- `notebooks/run_uc-model.ipynb`
- `notebooks/globals.py`
- `format-results/format_results_functions.R`

## 6. Minimal Scope

### 6.1 In scope

- Dataset: WISDM Activity Prediction v1.1 transformed dataset
- Subset: retained users only, after repository filtering
- Users: every retained user, one target user per evaluation round
- Preprocessing:
  - parse transformed ARFF to CSV using the official formatter
  - keep the repository's user filtering
  - label-encode the target column
  - min-max scale features using training data only
- Split strategy:
  - UIM: train/calibration from all non-target users; test from target user
  - UCM: train from all non-target users; calibration/test split within the target user
- Model: Random Forest only
- Conformal method: MAPIE LAC only
- Comparator: UIM only
- Primary metric: coverage
- Secondary metric: mean prediction set size
- Repetitions: 20
- Seeds: 101 through 120

## 7. Out of Scope

- Opportunity, HAR70+, Smartwatch Gestures
- Mixed model, UDM, SVM, KNN, Naive Bayes
- Full paper reproduction
- All figures and visualization artifacts
- Hyperparameter sweep
- GPU experiments
- Paid services
- Publication and submission
- R report generation if it is not needed to validate the minimal claim

## 8. Data Contract

| Item | Contract | Fact type |
| --- | --- | --- |
| Official URL | <https://www.cis.fordham.edu/wisdm/dataset.php> | `PAPER_FACT` |
| Exact archive / file | `WISDM_ar_v1.1_transformed.arff` | `CODE_FACT` |
| Expected format | Transformed ARFF downloaded from the WISDM Activity Prediction dataset, then converted to CSV | `CODE_FACT` |
| Estimated size | 5,435 transformed examples before repository filtering; 16 retained subjects after filtering | `PAPER_FACT` + `CODE_FACT` |
| License / usage conditions | The official page requests citation and retention of the dataset readme; no paid API or proprietary access is indicated in the official snapshot | `PAPER_FACT` |
| Checksum policy | Store SHA-256 for the raw archive and the processed CSV in the study-local manifest; do not commit raw data | `ENGINEERING_DECISION` |
| Local storage | `research/<study>/data/raw/wisdm/` and `research/<study>/data/processed/wisdm/` | `ENGINEERING_DECISION` |
| Raw data in Git | No | `ENGINEERING_DECISION` |
| Raw -> processed rule | Use `format-datasets/format-wisdm.R` semantics exactly | `CODE_FACT` |
| Malformed rows | Remove the columns dropped by the formatter and exclude users 6 and 24 | `CODE_FACT` |
| Missing values | None expected in the transformed dataset snapshot used by the paper; do not impute unless the official formatter requires it | `PAPER_FACT` + `CODE_FACT` |
| User identifiers | Column `userid` | `CODE_FACT` |
| Activity labels | Column `label` | `CODE_FACT` |
| Feature columns | All remaining numeric sensor features after formatter cleaning | `CODE_FACT` |
| Target column | `label` | `CODE_FACT` |
| Row order | Preserve processed file order; do not add a new shuffle step before splits | `ENGINEERING_DECISION` |
| Deterministic sorting | No extra sort beyond the official formatter; deterministic splits come from fixed seeds | `ENGINEERING_DECISION` |
| Split leakage risks | Fit scalers only on training data; keep target-user data out of UIM training; keep calibration split separate from test split | `ENGINEERING_DECISION` |

## 9. Preprocessing Contract

| Step | Contract | Fact type |
| --- | --- | --- |
| Parsing | Read `WISDM_ar_v1.1_transformed.arff` using the official formatter's expectations | `CODE_FACT` |
| Cleaning | Drop corrupted columns `1, 33, 36, 37, 38` before analysis | `CODE_FACT` |
| Columns | Keep `userid`, `label`, and numeric sensor features | `CODE_FACT` |
| Label encoding | Encode `label` with `LabelEncoder`, then preserve the class order for downstream reporting | `CODE_FACT` |
| User selection | Keep only complete-activity users and exclude users 6 and 24 | `CODE_FACT` |
| Data ordering | Preserve file order after filtering; no extra randomization before split | `ENGINEERING_DECISION` |
| UIM split | `train_size = 0.6` on all non-target-user rows, then test on the target user rows | `CODE_FACT` |
| UCM split | `train_size = 0.6` on all non-target-user rows, then `train_size = 0.5` on the target user rows to obtain calibration/test halves | `CODE_FACT` |
| Scaling | Fit `MinMaxScaler` on training data only, then transform calibration and test data | `CODE_FACT` |
| Leakage prevention | No target-user information enters UIM training; no scaler fit uses calibration or test rows | `ENGINEERING_DECISION` |
| Conformal score | LAC-style nonconformity: one minus the probability of the true label | `CODE_FACT` |
| Output protocol | Save raw prediction labels, prediction sets, scores, and p-values before summary aggregation | `CODE_FACT` |

## 10. Experiment Protocol

| Item | Contract | Fact type |
| --- | --- | --- |
| Python version target | Python 3.11+ in the current project environment | `ENGINEERING_DECISION` |
| Dependencies | `numpy`, `pandas`, `scikit-learn`, `mapie`; `jupyter` only if notebooks are used for parity checks | `CODE_FACT` + `ENGINEERING_DECISION` |
| CPU-only requirement | Yes | `ENGINEERING_DECISION` |
| Model parameters | RF only, `n_estimators=50`, `random_state=seed` | `CODE_FACT` |
| Conformal parameters | `MapieClassifier(cv="prefit", method="score", random_state=seed)`, `alpha=0.05` | `CODE_FACT` |
| Random states | `101..120` derived from `100 + iteration` | `CODE_FACT` |
| Split proportions | UIM: 60/40 on non-target users; UCM: 60/40 on non-target users plus 50/50 target-user calibration/test split | `CODE_FACT` |
| Calibration setup | UIM uses all non-target users for calibration; UCM uses target-user calibration only | `CODE_FACT` |
| Fitting order | scale train data -> fit RF on train -> fit MAPIE on calibration -> predict test | `CODE_FACT` |
| Prediction order | Predict once per test set, then aggregate raw rows into per-user and per-iteration summaries | `CODE_FACT` |
| Metric definitions | Coverage and mean prediction set size, as defined in `format_results_functions.R` | `CODE_FACT` |
| Aggregation method | Per-user within each iteration, then mean and sd across iterations | `CODE_FACT` |
| Number of repetitions | 20 | `PAPER_FACT` + `CODE_FACT` |
| Seeds | 101 through 120 | `CODE_FACT` |
| Expected runtime | Low; local CPU study should be measured in minutes, not hours | `ENGINEERING_DECISION` |
| Expected RAM | Low to moderate | `ENGINEERING_DECISION` |
| Expected disk | Low | `ENGINEERING_DECISION` |
| Offline / online requirements | Offline after one-time WISDM acquisition; no cloud or paid service required | `ENGINEERING_DECISION` |

## 11. Metrics Contract

### 10.1 Primary metric: conformal coverage

- Meaning: fraction of samples whose ground-truth label is contained in the conformal prediction set
- Formula: `coverage = hits / n`
- Unit: percentage or fraction, depending on presentation
- Direction: higher is better
- Level of aggregation:
  - per user within iteration
  - mean across users in the iteration
  - mean and standard deviation across iterations
- Ties: not applicable
- Rounding policy: keep full precision in machine artifacts; round to 2 decimals only for human-facing summaries
- Expected reference values:
  - UCM RF: `96.28 ± 0.62`
  - UIM RF: `88.76 ± 1.35`
- Failure threshold:
  - coverage outside tolerance
  - coverage ordering reversed

### 10.2 Secondary metric: mean prediction set size

- Meaning: average cardinality of the conformal prediction set
- Formula: mean of `|S_i|`
- Unit: number of labels
- Direction: smaller is usually preferred, but for this claim it is interpreted as a cost of restoring coverage
- Level of aggregation:
  - per user within iteration
  - mean across users in the iteration
  - mean and standard deviation across iterations
- Ties: not applicable
- Rounding policy: keep full precision in machine artifacts; round to 2 decimals only for human-facing summaries
- Expected reference values:
  - UCM RF: `2.04 ± 0.09`
  - UIM RF: `1.39 ± 0.04`
- Failure threshold:
  - set-size outside tolerance
  - set-size relation inconsistent with the paper's reported direction

## 12. Pass / Fail Contract

### PASS

- scientific result meets the defined coverage and set-size tolerances
- UCM coverage is higher than UIM coverage
- all required artifacts are present and checksum-valid
- deterministic rerun condition is met under the fixed seed policy
- no leakage is detected
- no forbidden dependency is used

### FAIL

- metric outside tolerance
- comparator relation reversed
- missing artifact
- invalid checksum
- nondeterministic scientific outputs beyond allowed tolerance
- protocol deviation
- unresolved blocking ambiguity

### Status labels

- `REPRODUCED`: PASS with all required artifacts and the claim within tolerance
- `PARTIALLY_REPRODUCED`: run succeeds and direction holds, but at least one metric is outside tolerance
- `NOT_REPRODUCED`: run succeeds but the scientific direction is wrong or the claim is materially contradicted
- `EXECUTION_FAILED`: the protocol cannot complete for technical reasons

## 13. Determinism Contract

### Byte-stable artifacts

- `source_record.json`
- `claim.json`
- `experiment_plan.json`
- `data_manifest.json`
- `raw_results.csv`
- `raw_results.json`
- `metrics.json`
- normalized verifier hashes

### Wall-clock volatile artifacts

- `experiment_result.json` timestamps
- `experiment.log`
- `LOGBOOK.md` creation timestamp
- `artifact_registry.json` per-record `created_at`
- `verification_result.json` if it stores run timestamps

### Contract with the existing mixed verifier

- Scientific fields must be stable for a fixed environment and fixed seeds
- Wall-clock metadata may vary and must be normalized by the verifier
- The verifier must not rewrite the real files
- No new clock model should be introduced

## 14. Artifact Contract

| Artifact | Format | Producer | Contents | Stable fields | Volatile fields | Verifier rule |
| --- | --- | --- | --- | --- | --- | --- |
| `paper/source_record.json` | JSON | source-record step | Paper metadata, code URL, dataset URL, selected claim, evidence notes | paper identity, URLs, selected scope | access timestamps, fetched-at timestamps | present and schema-valid |
| `claims/claim.json` | JSON | claim extractor / study init | Single reproduction claim and tolerances | claim text, comparator, metric, tolerance, seed policy | `updated_at` if used | present and schema-valid |
| `plans/experiment_plan.json` | JSON | experiment planner | Split protocol, model, conformal method, repetitions | all protocol fields | none expected | present and schema-valid |
| `paper/data_manifest.json` | JSON | data prep | Raw download metadata, processing decisions, checksums | file names, rule set, checksums | fetch timestamps | present and checksum-consistent |
| `experiments/<experiment_id>/raw_results.csv` | CSV | experiment runner | Raw per-row predictions, sets, scores, p-values | row content under fixed seeds | none expected | stable under rerun |
| `experiments/<experiment_id>/raw_results.json` | JSON | experiment runner | Raw row-level result mirror | row content under fixed seeds | none expected | stable under rerun |
| `results/metrics.json` | JSON | postprocessor / runner | Coverage and set-size summaries | metric values, aggregation outputs | none expected | stable under rerun |
| `experiments/<experiment_id>/experiment_result.json` | JSON | experiment runner | Execution summary, metrics, environment, artifact paths | experiment_id, parameters, metrics, artifact paths | `started_at`, `completed_at` | verifier-normalized |
| `logs/experiment.log` | text | runner / CLI | Minimal execution trace | semantic content | timestamps | present |
| `logbook/LOGBOOK.md` | Markdown | logbook builder | FACT / INTERPRETATION / LIMITATION / NEXT STEP narrative | narrative body, artifact links, metric summaries | `created_at` derived from result time | verifier-normalized |
| `logs/artifact_registry.json` | JSON | registry | Paths, types, SHA-256, creation times | path list, sha list after normalization | `created_at` | verifier-normalized |
| `reports/REPRODUCTION_REPORT.md` | Markdown | report builder | Final human-readable reproduction summary | report body | timestamps if any | present and consistent with logbook |
| `verification_result.json` | JSON | verifier | Pass/fail, normalized hashes, diagnostics | verdict, reasons, normalized hashes | run timestamps if any | must reflect claim status |

### Notes on naming

- The current lab already uses `claim.json`, `experiment_plan.json`, `experiment_result.json`, `metrics.json`, `LOGBOOK.md`, and `artifact_registry.json`.
- `source_record.json`, `data_manifest.json`, and `REPRODUCTION_REPORT.md` are new study-level artifacts introduced only as planning artifacts for this study, not as a new parallel contract family.
- `LOGBOOK.md` remains canonical; Trackio, if used later, is auxiliary and must not replace the Markdown logbook or registry.

## 15. Risks and Open Questions

| ID | Risk / question | Type | Evidence | Blocking | Resolution before implementation |
| --- | --- | --- | --- | --- | --- |
| R1 | Exact WISDM download link may vary across page versions | DATA | Official WISDM page and formatter script | No | Confirm the archive path when the study is implemented; use the page and file name in the manifest |
| R2 | Local storage location for raw and processed WISDM is not yet created | DATA | No study-local data directory exists yet | No | Create `research/<study>/data/raw/wisdm/` and `research/<study>/data/processed/wisdm/` at implementation time |
| R3 | R workflow is optional for the minimal claim but still defines the paper-style summaries | METHOD | `format-results/format_results_functions.R` | No | Mirror the aggregation formulas in the implementation or use the R scripts only for presentation parity |
| R4 | Version sensitivity of `mapie` and `scikit-learn` could slightly shift the reported values | DETERMINISM | Notebook code and estimator stack | No | Pin the environment and keep the fixed seed policy |
| R5 | The paper reports tables for all four classifiers, but the study only uses RF | PAPER_CODE_MISMATCH | Paper tables vs minimal-scope decision | No | Keep the reduced scope explicit and do not generalize to other classifiers |

## 16. Implementation Gate

Verdict: `READY_FOR_SKELETON`

Reason:

- one claim is defined
- the dataset version is defined
- preprocessing is precise enough
- the split strategy is defined
- the model is defined
- the conformal method is defined
- the metric and tolerance are defined
- pass/fail is defined
- CPU feasibility is confirmed
- no blocking license issue is present in the official sources snapshot
- the expected artifact family is defined

## 17. Next one engineering step

Create the study skeleton from the existing reproduction template and populate it with this WISDM claim, data manifest, and experiment plan without implementing the run itself.
