# WISDM First Reproduction Results Analysis

Study: `repro-wisdm-ucm-rf`
Paper: *Conformal Prediction in Multi-User Settings: An Evaluation*

Status: `REPRODUCED`

## 1. Data Integrity

This analysis was produced from the existing first-run artifacts only.

### Control files

| File | Expected SHA-256 | Actual SHA-256 | Match |
| --- | --- | --- | --- |
| `experiments/wisdm_ucm_uim_rf/experiment_result.json` | `a8bf4b4b98b3e3aa6578af972c8dcdad76e1d6a51314dbf561da5ec221edcfbc` | `a8bf4b4b98b3e3aa6578af972c8dcdad76e1d6a51314dbf561da5ec221edcfbc` | YES |
| `results/metrics.json` | `f37a491f03c55d8e689334fcd72b150f66dc4ea1a7760d5d8f8a88461f9e8f3e` | `f37a491f03c55d8e689334fcd72b150f66dc4ea1a7760d5d8f8a88461f9e8f3e` | YES |
| `logbook/LOGBOOK.md` | `2c52adaa33f8548b77cf93671e01e6c87d82ca872310e54a1b60c271608c7a58` | `2c52adaa33f8548b77cf93671e01e6c87d82ca872310e54a1b60c271608c7a58` | YES |
| `reports/REPRODUCTION_REPORT.md` | `645b6650aef37cff22f69377b4ebd612f814c1331999d5002ec602a0328b7449` | `645b6650aef37cff22f69377b4ebd612f814c1331999d5002ec602a0328b7449` | YES |

### Raw result checks

| Check | Value |
| --- | ---: |
| `raw_results.csv` rows | 57,600 |
| `raw_results.json` rows | 57,600 |
| UCM rows | 28,800 |
| UIM rows | 28,800 |
| Iterations | 20 |
| Paired iteration deltas positive for coverage | YES |
| Paired iteration deltas positive for set size | YES |

The raw CSV and JSON mirrors are consistent in row count and content shape. The scientific summaries in `metrics.json` are computed from user-within-iteration aggregation, not from the sample-level row count directly.

## 2. Key Results

Observed values are taken from `results/metrics.json` and are reproducible from the raw results using the study contract.

| Metric | UCM | UIM | Difference | Reference | Delta vs reference | Tolerance | Verdict |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Empirical coverage | 0.9678248900 | 0.8893864324 | 0.0784384576 | UCM 0.9628, UIM 0.8876 | UCM `+0.0050248900`, UIM `+0.0017864324` | `±0.0100` | PASS |
| Average prediction set size | 2.1174957415 | 1.3872772392 | 0.7302185023 | UCM 2.04, UIM 1.39 | UCM `+0.0774957415`, UIM `-0.0027227608` | `±0.20` | PASS |

Additional derived values from `metrics.json`:

- Coverage uplift mean: `0.07843845760810991`
- Coverage uplift standard deviation: `0.01362902495958109`
- Prediction set size difference mean: `0.7302185022689067`
- Prediction set size difference standard deviation: `0.11584150130487929`

## 3. Statistical Result

Aggregation level:

1. per sample predictions inside each user;
2. per-user mean inside each iteration;
3. mean across the 20 iterations.

Paired iteration-level differences:

| Quantity | Mean | Std. dev. | 95% CI | Exact sign-test p-value |
| --- | ---: | ---: | ---: | ---: |
| Coverage uplift | 0.0784384576 | 0.0136290250 | `[0.0724653838, 0.0844115314]` | `1.9073486328125e-06` |
| Prediction set size difference | 0.7302185023 | 0.1158415013 | `[0.6794496588, 0.7809873458]` | `1.9073486328125e-06` |

Interpretation:

- all 20 paired iteration coverage deltas are positive;
- all 20 paired iteration set-size deltas are positive;
- the study reproduces the paper direction and stays inside the declared tolerances.

## 4. Reproduction Verdict

`REPRODUCED`

### Why

- both primary metrics are inside tolerance;
- UCM coverage is higher than UIM coverage;
- UCM set size is higher than UIM set size, matching the paper direction;
- the expected first-run hashes match exactly;
- the raw result mirrors are consistent and complete.

## 5. Notes

- No rerun was performed for this analysis.
- No model, data, verifier, or challenge code was changed for this analysis.
- This file is an interpretive summary only; the authoritative artifacts remain the existing study outputs.
