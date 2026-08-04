# First Reproduction Study Skeleton

This package is the architectural skeleton for the first WISDM reproduction study.

## What this study targets

- Paper: `Conformal Prediction in Multi-User Settings: An Evaluation`
- Dataset: WISDM Activity Prediction v1.1 transformed dataset
- Claim: compare `UCM` against `UIM` for the `RandomForestClassifier` with MAPIE LAC

## What is already defined

- immutable study identity
- claim metadata
- protocol metadata
- artifact naming contract
- status machine

## What is intentionally absent

- experiment execution
- preprocessing implementation
- dataset download
- verifier logic
- ML dependencies
- publication or submission flow

## Next steps

1. Implement data ingestion in a later stage.
2. Implement the experiment runner in a later stage.
3. Connect the study skeleton to the existing lab pipeline only after the specification is fully satisfied.

