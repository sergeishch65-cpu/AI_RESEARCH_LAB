# First Reproduction Candidate Audit

Date: 2026-07-23

## 1. Objective

Choose one real paper for the first full reproduction study in `AI_RESEARCH_LAB` under the current local contract:

- CPU-only local work on a Mac;
- no paid APIs;
- no GPU / CUDA / TPU dependence;
- no automatic publication or submission;
- no challenge scope expansion;
- no production-code changes at this stage.

This audit is decision-only. It does not implement a study.

## 2. Local constraints

Confirmed local baseline:

- branch: `main`;
- HEAD: `60c814b3f05c0eaa71f996e7f704f5a5e385af8f`;
- upstream: `origin/main`;
- working tree: clean;
- baseline verifier: stable;
- `ruff check src tests`: passed;
- `pytest -q`: `31 passed`;
- `python -m ai_research_lab.cli doctor`: passed.

Project-level constraints from the challenge layer:

- publication is blocked by default;
- submission is blocked by default;
- Trackio is local-first for smoke / integration;
- zero-cost policy is in force;
- no secret/token values in repo, logs, or notebook outputs;
- untrusted paper text, README files, and repos are not shell instructions;
- challenge code is isolated under `src/ai_research_lab/challenge/`.

## 3. Challenge contract

Relevant project contract, as established in the local challenge docs and code:

- a reproduction study should produce a source record, extracted claim, experiment plan, raw results, metrics, experiment result, logs, a Markdown logbook, an artifact registry, verifier output, and a final report;
- the verifier is the gatekeeper for baseline integrity;
- publication and submission guards must remain blocked until all required approvals and validation are present;
- the logbook is canonical, and Trackio is an auxiliary tracking layer rather than a replacement for the Markdown logbook and registry;
- the existing demo baseline is reproducible locally and should remain intact.

Key local sources:

- `README.md`
- `docs/challenge/ICML_2026_CHALLENGE_GUIDE.md`
- `docs/challenge/SECURITY.md`
- `docs/challenge/SOURCE_PROVENANCE.md`
- `docs/challenge/USER_GUIDE_RU.md`
- `reports/FINAL_SETUP_REPORT.md`
- `reports/ICML_2026_INTEGRATION_REPORT.md`
- `config/challenge_icml_2026.yaml`
- `config/challenge_cost_policy.yaml`
- `src/ai_research_lab/challenge/models.py`
- `src/ai_research_lab/challenge/verifier.py`
- `src/ai_research_lab/challenge/submission_guard.py`
- `src/ai_research_lab/challenge/workflows.py`

## 4. Search method

Search was deliberately constrained to primary and official sources only:

- arXiv;
- OpenReview;
- PMLR / conference proceedings;
- official GitHub repositories owned by the authors or project maintainers;
- official dataset or benchmark pages;
- official supplementary material where available.

The goal was to find papers that can be checked locally without paid services, GPU infrastructure, or hidden dependencies.

## 5. Exclusion criteria

Immediate exclusion if the paper required any of the following for the central claim:

- GPU / CUDA / TPU;
- large-model training or large LLM API usage;
- paid services;
- closed models or closed data;
- multi-day runs or large-scale cluster jobs;
- opaque browser automation or live external services;
- hidden shell execution from paper text or README;
- missing or unclear claim;
- data that is not publicly accessible or is not realistically reproducible on the current Mac;
- code that is not official or is too incomplete to assess.

Additional risk-based exclusion criteria:

- missing code license;
- missing or unclear data acquisition path;
- notebook-only workflow with no reliable automation path;
- benchmark breadth that makes the first study too expensive.

## 6. Candidate matrix

| Rank | Paper | Year / Venue | Claim | Paper | Code | Data | CPU | Runtime | Paid services | Challenge fit | Main risk | Verdict |
| ---- | ----- | ------------ | ----- | ----- | ---- | ---- | --- | ------- | ------------- | ------------- | --------- | ------- |
| 1 | Conformal Prediction in Multi-User Settings: An Evaluation | 2025, User Modeling and User-Adapted Interaction / arXiv 2312.05195 | WISDM conformal coverage / width ordering across UDM, UCM, UIM | PASS | OFFICIAL_CODE | OPEN_SMALL | CPU_READY | UNDER_1_HOUR | PASS | STRONG_FIT | raw-data formatting; R + notebook split | FINALIST |
| 2 | Tabular Learning Revisited: An Empirical Study of Tabular Classification | 2026, TMLR / OpenReview | OpenMLCC18 benchmark comparing tabular methods and boosted trees | PASS | OFFICIAL_CODE | OPEN_BUT_LARGE | CPU_WITH_MINOR_ADAPTATION | UNDER_1_DAY | PASS | ACCEPTABLE_FIT | benchmark breadth; W&B/offline; many method-specific deps | FINALIST |
| 3 | Well-tuned Simple Nets Excel on Tabular Datasets | 2021, NeurIPS / arXiv 2106.11189 | Regularization cocktails beat specialized NNs and XGBoost on tabular benchmarks | PASS | OFFICIAL_CODE | OPEN_BUT_LARGE | CPU_WITH_MINOR_ADAPTATION | UNDER_1_DAY | PASS | ACCEPTABLE_FIT | AutoPyTorch branch; conda/gcc/swig; HPO cost | FINALIST |
| 4 | Feature-weighted Maximum Representative Subsampling | 2026, Scientific Reports / arXiv 2603.01013 | FW-MRS keeps more instances without downstream loss | PASS | OFFICIAL_CODE | MISSING | CPU_READY | UNDER_1_DAY | PASS | WEAK_FIT | repo does not ship complete data path; mixed local / package sources | BACKUP |
| 5 | Tabular Data: Is Deep Learning all you need? | 2024, arXiv / benchmark paper | Tuned tabular methods dominate recent tabular DL baselines | PASS | OFFICIAL_CODE | OPEN_BUT_LARGE | CPU_WITH_MINOR_ADAPTATION | OVER_1_DAY | PASS | WEAK_FIT | broad benchmark scope; higher orchestration cost than a first study | BACKUP |
| 6 | Is Deep Learning finally better than Decision Trees on Tabular Data? | 2025, arXiv / benchmark paper | Tabular DL vs boosted trees over a large benchmark | PASS | OFFICIAL_CODE | OPEN_BUT_LARGE | CPU_WITH_MINOR_ADAPTATION | OVER_1_DAY | PASS | WEAK_FIT | repeated large-scale CV / broad benchmark complexity | REJECT |
| 7 | Backward Conformal Prediction | 2025, arXiv | Size-constrained conformal prediction with adaptive coverage | PASS | INSUFFICIENT | OPEN_SMALL | CPU_READY | UNDER_1_HOUR | PASS | WEAK_FIT | notebook-first repo and missing license signal; CIFAR path adds download friction | REJECT |
| 8 | Conformalized Interval Arithmetic with Symmetric Calibration | 2024, AAAI / arXiv 2408.10939 | Coverage-guaranteed intervals for sums / averages | PASS | OFFICIAL_CODE | RESTRICTED | CPU_WITH_MINOR_ADAPTATION | UNDER_1_DAY | PASS | WEAK_FIT | benchmark data include datasets with heavier acquisition / preprocessing overhead | REJECT |

Notes:

- `OPEN_SMALL` means the selected study can be done on a small open dataset or a small subset of an open dataset without changing the claim.
- `OPEN_BUT_LARGE` means the official benchmark is public, but the paper’s full scope is broad enough to be expensive for a first local study.
- `MISSING` means the repo does not provide a complete, self-contained data path in the tracked files.
- `INSUFFICIENT` means the code exists, but the paper/repo is not good enough for a first serious reproduction study.

## 7. Detailed finalist audits

### 7.1 Conformal Prediction in Multi-User Settings: An Evaluation

#### Bibliographic identity

- Title: `Conformal Prediction in Multi-User Settings: An Evaluation`
- Authors: Enrique Garcia-Ceja, Luciano Garcia-Banuelos, Nicolas Jourdan
- Year: 2025
- Venue: User Modeling and User-Adapted Interaction
- DOI: `10.1007/s11257-025-09425-5`
- Official paper URL: [arXiv 2312.05195](https://arxiv.org/abs/2312.05195)
- Official code URL: [GitHub](https://github.com/enriquegit/conformal-prediction-multiuser)
- Data URLs:
  - [WISDM Lab dataset page](https://www.cis.fordham.edu/wisdm/dataset.php)
  - [WISDM Lab home](https://www.cis.fordham.edu/wisdm/)

#### Central paper claim

The paper evaluates conformal prediction in multi-user settings and reports significant differences in conformal performance measures across evaluation strategies. For the WISDM dataset, the paper’s tables show that user-dependent / user-calibrated variants outperform the user-independent baseline in coverage / set-size tradeoffs.

#### Proposed reproduction claim

On the WISDM dataset, reproduce the paper’s conformal ranking for the four classical classifiers used in the repo (`GaussianNB`, `RandomForestClassifier`, `SVC`, `KNeighborsClassifier`) and confirm that the user-dependent / user-calibrated strategy preserves coverage near the reported level while improving the coverage-width tradeoff over the user-independent baseline.

#### Minimal experiment

- Input: the WISDM dataset prepared as `data.csv`
- Dataset scope: WISDM only, not the other three datasets
- Preprocessing: use the repo’s formatting pipeline or the already formatted `data.csv` if available
- Baseline: user-independent conformal prediction
- Methods: mixed, user-independent, user-dependent, and user-calibrated strategies
- Seed policy: keep the repo’s fixed seed policy and document it explicitly
- Metric: conformal coverage and mean prediction-set width
- Number of repetitions: follow the repo’s iteration count for the WISDM script
- Pass criterion: preserve the paper’s rank ordering and match coverage / width within a conservative tolerance
- Expected artifacts:
  - source record
  - claim JSON
  - experiment plan
  - raw result files
  - metrics JSON
  - experiment result JSON
  - log file
  - logbook
  - artifact registry
  - verifier output
  - final reproduction report

#### Local feasibility

- Python version: current project `.venv`
- Main dependencies: `numpy`, `pandas`, `scikit-learn`, `mapie`, `jupyter`
- RAM: low to moderate
- Disk: low
- CPU assumptions: CPU-only is realistic
- Estimated runtime: one WISDM-only study should be comfortably local; the full four-dataset paper is still finite, but not necessary for the first study
- Network requirements: only for one-time raw WISDM acquisition if the formatted dataset is not already present
- Mac-specific issues: R and notebook tooling may be needed for the format / visualization step, but the core conformal experiment is CPU-friendly

#### What will not be reproduced

- Opportunity
- HAR70+
- Smartwatch Gestures
- the full paper’s cross-dataset visualization set
- any publication / submission flow

This does not distort the chosen claim because the first study is explicitly reduced to the WISDM slice of the paper.

#### Risks

- medium data-preparation risk because the repo uses formatting scripts and the raw dataset may need to be fetched once
- medium workflow risk because the repo mixes Python, notebooks, and R for presentation
- low hardware risk because the core models are classical CPU models

#### Final assessment

`GO`

---

### 7.2 Tabular Learning Revisited: An Empirical Study of Tabular Classification

#### Bibliographic identity

- Title: `Tabular Learning Revisited: An Empirical Study of Tabular Classification`
- Authors: Guri Zabërgja, Arlind Kadra, Christian Frey, Josif Grabocka
- Year: 2026
- Venue: Transactions on Machine Learning Research
- DOI / identifier: OpenReview `I8BIGp4XOb`
- Official paper URL: [OpenReview](https://openreview.net/forum?id=I8BIGp4XOb)
- Official code URL: [GitHub](https://github.com/machinelearningnuremberg/Tabular-Study)
- Data URL: [OpenMLCC18 benchmark](https://www.openml.org/search?type=benchmark&sort=tasks_included&study_type=task&id=99)

#### Central paper claim

The paper revisits large-scale tabular classification and reports that boosted-tree families remain very strong, while the benchmark also compares many neural and foundation-style tabular methods on OpenMLCC18.

#### Proposed reproduction claim

Reproduce one or two official OpenMLCC18 benchmark folds from the repository’s quick-start path and confirm the reported rank ordering on a small CPU-friendly slice of the benchmark, rather than attempting the whole 68-task study on day one.

#### Minimal experiment

- Input: one OpenMLCC18 task, ideally the repository’s own quick-start dataset
- Dataset: one public OpenML task from the benchmark
- Preprocessing: use the repo’s method-specific pipeline
- Baseline: tree-based baseline versus one neural baseline
- Seed policy: fixed seed and fold
- Metric: balanced accuracy / benchmark metric used by the chosen method
- Number of repetitions: one fold plus a small sanity-check repetition budget
- Pass criterion: metric and ranking within a conservative tolerance against the reported benchmark behavior
- Expected artifacts:
  - source record
  - claim JSON
  - plan JSON
  - raw outputs
  - metrics JSON
  - experiment result JSON
  - logbook
  - registry
  - verifier output

#### Local feasibility

- Python version: Python from the repo’s `environment.yml`
- Main dependencies: method-specific stacks, `scikit-learn`, gradient boosting libraries, W&B offline mode, and additional per-method dependencies
- RAM: moderate to high
- Disk: moderate
- CPU assumptions: possible, but some methods are more comfortable when the experiment is narrowed
- Estimated runtime: the full paper is expensive; a reduced first study is still feasible
- Network requirements: OpenML downloads and optional W&B traffic
- Mac-specific issues: nested benchmark code plus multiple method subtrees increase maintenance risk

#### What will not be reproduced

- the full 68-dataset benchmark
- every method family in the repository
- any Slurm / multi-node orchestration
- any W&B online logging

This is acceptable only as a reduced-scope first study.

#### Risks

- high benchmark breadth
- medium dependency complexity
- medium version sensitivity
- medium runtime risk

#### Final assessment

`CONDITIONAL_GO`

---

### 7.3 Well-tuned Simple Nets Excel on Tabular Datasets

#### Bibliographic identity

- Title: `Well-tuned Simple Nets Excel on Tabular Datasets`
- Authors: Arlind Kadra, Marius Lindauer, Frank Hutter, Josif Grabocka
- Year: 2021
- Venue: NeurIPS 2021
- DOI / identifier: arXiv `2106.11189`
- Official paper URL: [arXiv 2106.11189](https://arxiv.org/abs/2106.11189)
- Official code URL: [GitHub](https://github.com/releaunifreiburg/WellTunedSimpleNets)
- Data URL: [OpenMLCC18 benchmark](https://www.openml.org/search?type=benchmark&sort=tasks_included&study_type=task&id=99)

#### Central paper claim

The paper reports that well-regularized plain MLPs outperform specialized neural tabular architectures and also beat strong traditional methods such as XGBoost when hyperparameters are thoroughly tuned on a 40-dataset benchmark.

#### Proposed reproduction claim

Reproduce the paper’s claim on a single OpenML task or a tiny subset of the benchmark first, using the repository’s official AutoPyTorch-based pipeline and a fixed seed, then scale up only if the initial result is stable.

#### Minimal experiment

- Input: one OpenMLCC18 task
- Dataset: a single public tabular dataset from the benchmark
- Preprocessing: the repo’s AutoPyTorch pipeline
- Baseline: a tuned MLP versus XGBoost / the paper’s selected baseline for that task
- Seed policy: fixed seed
- Metric: balanced accuracy or the task-specific benchmark metric
- Number of repetitions: one quick fold / one dataset for the first study
- Pass criterion: reproduce the paper’s qualitative ranking and approximate metric behavior
- Expected artifacts:
  - source record
  - claim JSON
  - plan JSON
  - raw outputs
  - metrics JSON
  - experiment result JSON
  - logbook
  - registry
  - verifier output

#### Local feasibility

- Python version: the repo expects a legacy AutoPyTorch-compatible environment
- Main dependencies: AutoPyTorch, PyTorch, SMAC, NumPy, pandas, and the extra regularization-cocktail stack
- RAM: moderate to high
- Disk: moderate
- CPU assumptions: CPU-only execution is possible, but the repo is tuned for heavier optimization workflows
- Estimated runtime: reduced-scope first study is feasible; full paper scope is heavy
- Network requirements: OpenML data and package downloads are expected
- Mac-specific issues: build dependencies and the AutoPyTorch branch increase setup risk

#### What will not be reproduced

- the full 40-dataset benchmark
- the complete HPO search budget
- any long wall-time AutoML run
- any non-essential visualizations

This is acceptable as a reduced-scope first study, but it is heavier than the chosen paper.

#### Risks

- high setup risk due to AutoPyTorch and legacy dependency requirements
- high runtime risk if the benchmark is scaled beyond one or two datasets
- medium version sensitivity

#### Final assessment

`CONDITIONAL_GO`

## 8. Why the selected article won

Selected paper:

- `Conformal Prediction in Multi-User Settings: An Evaluation`

Why it won:

1. The core computation is classical CPU ML, not GPU-heavy deep learning.
2. The claim is measurable with standard conformal metrics.
3. The first study can be reduced honestly to one dataset (`WISDM`) without changing the nature of the claim.
4. The code path is small enough to fit the existing local artifact pipeline.
5. The paper’s own repo already organizes the work around explicit datasets and simple classifiers.
6. The result is meaningful enough to be a real reproduction study, not just a smoke test.

Why the other two finalists were not selected:

- `Tabular Learning Revisited: An Empirical Study of Tabular Classification` is strong and well packaged, but the benchmark breadth, method matrix, and W&B / multi-method infrastructure make the first study heavier than necessary.
- `Well-tuned Simple Nets Excel on Tabular Datasets` is scientifically strong, but the AutoPyTorch stack and HPO-oriented workflow add setup and runtime risk that are unnecessary for a first local study.

## 9. Risks

Selected-paper risks:

- raw-data formatting for the WISDM slice
- notebook / R bridge for presentation artifacts
- possible tolerance tuning for conformal metrics

Why those risks are acceptable:

- the dataset is public and small enough for a local Mac
- the metrics are simple and deterministic enough to be verified locally
- the chosen claim remains scientifically meaningful even with a reduced WISDM-only scope

## 10. Sources

### Local project sources

- [README.md](../README.md)
- [ICML 2026 Challenge Guide](../docs/challenge/ICML_2026_CHALLENGE_GUIDE.md)
- [Security Guide](../docs/challenge/SECURITY.md)
- [Source Provenance](../docs/challenge/SOURCE_PROVENANCE.md)
- [Final Setup Report](FINAL_SETUP_REPORT.md)
- [ICML 2026 Integration Report](ICML_2026_INTEGRATION_REPORT.md)

### External primary sources

- [Conformal Prediction in Multi-User Settings: An Evaluation](https://arxiv.org/abs/2312.05195)
- [Multi-user code repository](https://github.com/enriquegit/conformal-prediction-multiuser)
- [WISDM dataset page](https://www.cis.fordham.edu/wisdm/dataset.php)
- [Tabular Learning Revisited: An Empirical Study of Tabular Classification](https://openreview.net/forum?id=I8BIGp4XOb)
- [TabularStudy repository](https://github.com/machinelearningnuremberg/Tabular-Study)
- [OpenMLCC18 benchmark](https://www.openml.org/search?type=benchmark&sort=tasks_included&study_type=task&id=99)
- [Well-tuned Simple Nets Excel on Tabular Datasets](https://arxiv.org/abs/2106.11189)
- [WellTunedSimpleNets repository](https://github.com/releaunifreiburg/WellTunedSimpleNets)
- [Feature-Weighted Maximum Representative Subsampling](https://arxiv.org/abs/2603.01013)
- [FeatureWeightDebiasing repository](https://github.com/kramerlab/FeatureWeightDebiasing)
- [Backward Conformal Prediction](https://arxiv.org/abs/2505.13732)
- [Backward CP repository](https://github.com/GauthierE/backward-cp)
- [Conformalized Interval Arithmetic with Symmetric Calibration](https://arxiv.org/abs/2408.10939)
- [CIA repository](https://github.com/luo-lorry/CIA)

## 11. Next engineering step

Create a new challenge study skeleton for the selected WISDM-only scope, then implement the claim extraction / experiment plan / verification path for that one dataset.

Do not do that work in this audit.
