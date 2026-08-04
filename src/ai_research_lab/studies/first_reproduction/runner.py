from __future__ import annotations

import argparse
import json
import platform
import sys
import subprocess
import tarfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import mapie
import sklearn
from mapie.classification import SplitConformalClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

from ...artifact_registry import register_artifacts, sha256_file
from ...models import ExperimentResult, WorkflowStatus
from ...paths import portable_relative_path, project_root
from .contracts import StudyClaim, StudyProtocol
from .metadata import SPECIFICATION_VERSION, STUDY_ID, STUDY_VERSION

PAPER_URL = "https://arxiv.org/abs/2312.05195"
CODE_URL = "https://github.com/enriquegit/conformal-prediction-multiuser"
DATASET_PAGE_URL = "https://www.cis.fordham.edu/wisdm/dataset.php"
DATASET_ARCHIVE_URL = "https://www.cis.fordham.edu/wisdm/includes/datasets/WISDM_ar_v1.1.tar.gz"
DATASET_NAME = "WISDM Activity Prediction v1.1 transformed dataset"
DATASET_SUBSET = "Retained users after official formatter filtering"
STUDY_EXPERIMENT_ID = "wisdm_ucm_uim_rf"
CONFORMAL_ALPHA = 0.05
CONFORMAL_CONFIDENCE = 1.0 - CONFORMAL_ALPHA
EXCLUDED_USERS = {6, 24}
RETAINED_LABELS = ["Walking", "Jogging", "Upstairs", "Downstairs", "Sitting", "Standing"]
SEEDS = list(range(101, 121))
DROP_COLUMN_POSITIONS = {1, 33, 36, 37, 38}


@dataclass(frozen=True, slots=True)
class WISDMPaths:
    study_root: Path
    paper_dir: Path
    claims_dir: Path
    plans_dir: Path
    experiments_dir: Path
    results_dir: Path
    figures_dir: Path
    logs_dir: Path
    logbook_dir: Path
    data_raw_dir: Path
    data_processed_dir: Path
    archive_path: Path
    extracted_dir: Path
    arff_path: Path
    processed_csv_path: Path


def _json_write(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _project_paths(root_dir: Path | None = None) -> WISDMPaths:
    root = Path(root_dir or project_root()).resolve()
    study_root = root / "research" / STUDY_ID
    paper_dir = study_root / "paper"
    claims_dir = study_root / "claims"
    plans_dir = study_root / "plans"
    experiments_dir = study_root / "experiments"
    results_dir = study_root / "results"
    figures_dir = study_root / "figures"
    logs_dir = study_root / "logs"
    logbook_dir = study_root / "logbook"
    data_raw_dir = study_root / "data" / "raw" / "wisdm"
    data_processed_dir = study_root / "data" / "processed" / "wisdm"
    archive_path = data_raw_dir / "WISDM_ar_v1.1.tar.gz"
    extracted_dir = data_raw_dir / "WISDM_ar_v1.1"
    arff_path = extracted_dir / "WISDM_ar_v1.1_transformed.arff"
    processed_csv_path = data_processed_dir / "WISDM_ar_v1.1_transformed_processed.csv"
    return WISDMPaths(
        study_root=study_root,
        paper_dir=paper_dir,
        claims_dir=claims_dir,
        plans_dir=plans_dir,
        experiments_dir=experiments_dir,
        results_dir=results_dir,
        figures_dir=figures_dir,
        logs_dir=logs_dir,
        logbook_dir=logbook_dir,
        data_raw_dir=data_raw_dir,
        data_processed_dir=data_processed_dir,
        archive_path=archive_path,
        extracted_dir=extracted_dir,
        arff_path=arff_path,
        processed_csv_path=processed_csv_path,
    )


def _ensure_directories(paths: WISDMPaths) -> None:
    for directory in [
        paths.study_root,
        paths.paper_dir,
        paths.claims_dir,
        paths.plans_dir,
        paths.experiments_dir,
        paths.results_dir,
        paths.figures_dir,
        paths.logs_dir,
        paths.logbook_dir,
        paths.data_raw_dir,
        paths.data_processed_dir,
    ]:
        directory.mkdir(parents=True, exist_ok=True)


def _download_archive(paths: WISDMPaths) -> None:
    if paths.archive_path.exists():
        return
    tmp_path = paths.archive_path.with_suffix(".part")
    if tmp_path.exists():
        tmp_path.unlink()
    subprocess.run(
        [
            "curl",
            "-L",
            "--fail",
            "--silent",
            "--show-error",
            DATASET_ARCHIVE_URL,
            "-o",
            str(tmp_path),
        ],
        check=True,
    )
    tmp_path.replace(paths.archive_path)


def _safe_extract_tar(archive_path: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    with tarfile.open(archive_path, "r:gz") as tar:
        for member in tar.getmembers():
            member_path = (destination / member.name).resolve()
            if destination.resolve() not in member_path.parents and member_path != destination.resolve():
                raise ValueError(f"Unsafe tar member path: {member.name}")
        tar.extractall(destination, filter="data")


def _ensure_dataset(paths: WISDMPaths) -> None:
    _download_archive(paths)
    if not paths.arff_path.exists():
        _safe_extract_tar(paths.archive_path, paths.data_raw_dir)
    if not paths.arff_path.exists():
        raise FileNotFoundError(f"Не найден WISDM ARFF: {paths.arff_path}")


def _parse_arff(arff_path: Path) -> pd.DataFrame:
    attributes: list[str] = []
    data_rows: list[list[str]] = []
    in_data = False
    for raw_line in arff_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("%"):
            continue
        if not in_data:
            if line.lower().startswith("@data"):
                in_data = True
                continue
            if line.lower().startswith("@attribute"):
                rest = line[len("@attribute"):].strip()
                if rest.startswith('"'):
                    end = rest.find('"', 1)
                    name = rest[1:end]
                else:
                    name = rest.split()[0].rstrip("{").strip()
                attributes.append(name)
            continue
        data_rows.append([cell.strip() for cell in line.split(",")])

    frame = pd.DataFrame(data_rows, columns=attributes)
    return frame


def _formatter_drop_columns(frame: pd.DataFrame) -> pd.DataFrame:
    columns = list(frame.columns)
    keep_columns = [column for index, column in enumerate(columns, start=1) if index not in DROP_COLUMN_POSITIONS]
    return frame[keep_columns].copy()


def _retain_complete_users(frame: pd.DataFrame) -> tuple[pd.DataFrame, list[int]]:
    complete_users: list[int] = []
    for user_id, user_frame in frame.groupby("userid", sort=True):
        if set(user_frame["label"].unique()) == set(RETAINED_LABELS):
            complete_users.append(int(user_id))
    retained_users = [user_id for user_id in complete_users if user_id not in EXCLUDED_USERS]
    filtered = frame[frame["userid"].isin(retained_users)].copy().reset_index(drop=True)
    return filtered, retained_users


def _prepare_dataset(paths: WISDMPaths) -> dict[str, Any]:
    _ensure_dataset(paths)
    raw_frame = _parse_arff(paths.arff_path)
    cleaned_frame = _formatter_drop_columns(raw_frame)
    cleaned_frame = cleaned_frame.rename(columns={"user": "userid", "class": "label"})
    cleaned_frame["userid"] = pd.to_numeric(cleaned_frame["userid"], errors="coerce")
    for column in cleaned_frame.columns:
        if column not in {"userid", "label"}:
            cleaned_frame[column] = pd.to_numeric(cleaned_frame[column], errors="coerce")
    cleaned_frame = cleaned_frame.dropna().reset_index(drop=True)
    cleaned_frame["userid"] = cleaned_frame["userid"].astype(int)
    cleaned_frame["label"] = cleaned_frame["label"].astype(str).str.strip().str.strip('"')
    processed_frame, retained_users = _retain_complete_users(cleaned_frame)
    processed_frame.to_csv(paths.processed_csv_path, index=False)

    feature_columns = [column for column in processed_frame.columns if column not in {"userid", "label"}]
    raw_archive_sha256 = sha256_file(paths.archive_path)
    raw_arff_sha256 = sha256_file(paths.arff_path)
    processed_csv_sha256 = sha256_file(paths.processed_csv_path)

    source_record = {
        "study_id": STUDY_ID,
        "study_version": STUDY_VERSION,
        "specification_version": SPECIFICATION_VERSION,
        "created_at": _now_iso(),
        "paper": {
            "title": "Conformal Prediction in Multi-User Settings: An Evaluation",
            "url": PAPER_URL,
            "code_url": CODE_URL,
            "dataset_page_url": DATASET_PAGE_URL,
        },
        "dataset": {
            "name": DATASET_NAME,
            "archive_url": DATASET_ARCHIVE_URL,
            "archive_file": paths.archive_path.name,
            "archive_sha256": raw_archive_sha256,
            "arff_file": paths.arff_path.name,
            "arff_sha256": raw_arff_sha256,
            "processed_file": paths.processed_csv_path.name,
            "processed_sha256": processed_csv_sha256,
            "rows": int(processed_frame.shape[0]),
            "users": int(processed_frame["userid"].nunique()),
            "retained_users": retained_users,
            "labels": RETAINED_LABELS,
            "feature_columns": feature_columns,
            "target_column": "label",
            "user_column": "userid",
            "drop_columns_1_based": sorted(DROP_COLUMN_POSITIONS),
        },
        "claim": {
            "claim_id": "wisdm-ucm-rf-coverage-v1",
            "summary": "Compare user-calibrated and user-independent conformal prediction on WISDM with Random Forest + MAPIE LAC.",
        },
        "evidence_notes": [
            "Paper tables 8 and 9",
            "Official WISDM dataset page",
            "Official WISDM formatter semantics",
            "Official conformal-prediction-multiuser repository",
        ],
    }
    _json_write(paths.paper_dir / "source_record.json", source_record)

    data_manifest = {
        "study_id": STUDY_ID,
        "created_at": _now_iso(),
        "dataset": source_record["dataset"],
        "processing": {
            "formatter_drop_columns_1_based": sorted(DROP_COLUMN_POSITIONS),
            "formatter_drop_columns_names": [
                raw_frame.columns[index - 1] for index in sorted(DROP_COLUMN_POSITIONS)
            ],
            "complete_activity_users_only": True,
            "excluded_users": sorted(EXCLUDED_USERS),
            "scaling": "MinMaxScaler fit on training rows only",
            "conformal_score": "lac",
        },
        "checksums": {
            "raw_archive_sha256": raw_archive_sha256,
            "raw_arff_sha256": raw_arff_sha256,
            "processed_csv_sha256": processed_csv_sha256,
        },
    }
    _json_write(paths.paper_dir / "data_manifest.json", data_manifest)

    claim = StudyClaim(
        claim_id="wisdm-ucm-rf-coverage-v1",
        paper="Conformal Prediction in Multi-User Settings: An Evaluation",
        dataset=DATASET_NAME,
        subset=DATASET_SUBSET,
        population="All retained users, one target user at a time",
        task="6-class multi-user activity recognition",
        model="RandomForestClassifier(n_estimators=50, random_state=seed, n_jobs=1)",
        conformal_method='SplitConformalClassifier(confidence_level=0.95, conformity_score="lac")',
        comparator="User-independent model (UIM)",
        metric="Empirical coverage uplift",
        reported_result="Reference paper reports UCM coverage about 96.28% versus UIM coverage about 88.76%; UCM set size about 2.04 versus UIM set size about 1.39",
        expected_direction="UCM coverage > UIM coverage",
        tolerance="Coverage +/- 1.0 percentage points; set size +/- 0.2",
        repetitions=20,
        seed_policy="random_seed = 100 + iteration for iterations 1..20",
        source_evidence=[
            "Paper tables 8 and 9",
            "Official WISDM dataset page",
            "Official repository notebooks/globals.py",
            "Official repository notebooks/run_uc-model.ipynb",
            "Official repository notebooks/run_ui-model.ipynb",
        ],
    )
    _json_write(paths.claims_dir / "claim.json", claim.model_dump(mode="json"))

    protocol = StudyProtocol(
        dataset=DATASET_NAME,
        subset=DATASET_SUBSET,
        users="All retained users, one target user at a time",
        preprocessing=[
            "Download the official WISDM v1.1 transformed archive",
            "Drop corrupted columns 1, 33, 36, 37, 38",
            "Keep only complete-activity users",
            "Exclude users 6 and 24",
            "Fit MinMaxScaler on training data only",
        ],
        split_strategy=[
            "UIM: 60/40 split on non-target-user rows; test on target-user rows",
            "UCM: 60/40 split on non-target-user rows; 50/50 split on target-user rows",
        ],
        model="RandomForestClassifier(n_estimators=50, random_state=seed, n_jobs=1)",
        conformal_method='SplitConformalClassifier(confidence_level=0.95, conformity_score="lac")',
        comparator="UIM",
        primary_metric="empirical coverage",
        secondary_metric="average prediction set size",
        repetitions=20,
        seeds=SEEDS,
    )
    _json_write(paths.plans_dir / "experiment_plan.json", protocol.model_dump(mode="json"))

    return {
        "source_record": source_record,
        "data_manifest": data_manifest,
        "claim": claim,
        "protocol": protocol,
        "frame": processed_frame,
        "feature_columns": feature_columns,
        "retained_users": retained_users,
    }


def _split_frame(frame: pd.DataFrame, train_size: float, seed: int) -> tuple[pd.DataFrame, pd.DataFrame, bool]:
    stratify = frame["label"] if frame["label"].value_counts().min() >= 2 else None
    try:
        train, test = train_test_split(
            frame,
            train_size=train_size,
            random_state=seed,
            shuffle=True,
            stratify=stratify,
        )
        return train.reset_index(drop=True), test.reset_index(drop=True), stratify is not None
    except ValueError:
        train, test = train_test_split(
            frame,
            train_size=train_size,
            random_state=seed,
            shuffle=True,
            stratify=None,
        )
        return train.reset_index(drop=True), test.reset_index(drop=True), False


def _evaluate_method(
    *,
    train_frame: pd.DataFrame,
    calibrate_frame: pd.DataFrame,
    test_frame: pd.DataFrame,
    feature_columns: list[str],
    seed: int,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    scaler = MinMaxScaler()
    x_train = scaler.fit_transform(train_frame[feature_columns])
    x_calibrate = scaler.transform(calibrate_frame[feature_columns])
    x_test = scaler.transform(test_frame[feature_columns])
    y_train = train_frame["label"].to_numpy()
    y_calibrate = calibrate_frame["label"].to_numpy()
    y_test = test_frame["label"].to_numpy()

    estimator = RandomForestClassifier(n_estimators=50, random_state=seed, n_jobs=1)
    estimator.fit(x_train, y_train)

    conformal = SplitConformalClassifier(
        estimator=estimator,
        confidence_level=CONFORMAL_CONFIDENCE,
        conformity_score="lac",
        prefit=True,
        random_state=seed,
    )
    conformal.conformalize(x_calibrate, y_calibrate)
    predicted_labels, prediction_sets = conformal.predict_set(x_test)
    prediction_sets = np.asarray(prediction_sets).squeeze(-1)
    class_order = list(estimator.classes_)
    label_to_index = {label: idx for idx, label in enumerate(class_order)}
    target_index = np.array([label_to_index[label] for label in y_test], dtype=int)
    hits = prediction_sets[np.arange(prediction_sets.shape[0]), target_index]
    set_sizes = prediction_sets.sum(axis=1)
    predicted_labels = [str(label) for label in np.asarray(predicted_labels, dtype=object).tolist()]

    sample_rows: list[dict[str, Any]] = []
    for row_index, (true_label, predicted_label, hit, set_size, membership_row) in enumerate(
        zip(y_test, predicted_labels, hits, set_sizes, prediction_sets, strict=True)
    ):
        sample_rows.append(
            {
                "sample_index": row_index,
                "true_label": true_label,
                "predicted_label": predicted_label,
                "coverage_hit": bool(hit),
                "prediction_set_size": int(set_size),
                "prediction_set": [label for label, flag in zip(class_order, membership_row, strict=True) if bool(flag)],
            }
        )

    summary = {
        "coverage": float(np.mean(hits)),
        "average_prediction_set_size": float(np.mean(set_sizes)),
        "n_samples": int(len(y_test)),
        "calibration_size": int(len(y_calibrate)),
        "train_size": int(len(y_train)),
        "classes": class_order,
    }
    return summary, sample_rows


def _run_iteration(
    *,
    frame: pd.DataFrame,
    feature_columns: list[str],
    seed: int,
    iteration: int,
) -> tuple[dict[str, Any], list[dict[str, Any]], list[str]]:
    iteration_rows: list[dict[str, Any]] = []
    per_user_rows: list[dict[str, Any]] = []
    per_method_user_metrics: dict[str, list[dict[str, float]]] = {"UCM": [], "UIM": []}
    warnings: list[str] = []
    retained_users = sorted(int(user) for user in frame["userid"].unique())

    for target_user in retained_users:
        target_frame = frame[frame["userid"] == target_user].reset_index(drop=True)
        non_target_frame = frame[frame["userid"] != target_user].reset_index(drop=True)

        non_target_train, non_target_calibrate, non_target_stratified = _split_frame(
            non_target_frame, train_size=0.6, seed=seed
        )
        target_calibrate, target_test, target_stratified = _split_frame(
            target_frame, train_size=0.5, seed=seed
        )
        if not non_target_stratified:
            warnings.append(f"Iteration {iteration}, seed {seed}, target user {target_user}: non-target split used without stratification.")
        if not target_stratified:
            warnings.append(f"Iteration {iteration}, seed {seed}, target user {target_user}: target split used without stratification.")

        uim_summary, uim_samples = _evaluate_method(
            train_frame=non_target_train,
            calibrate_frame=non_target_calibrate,
            test_frame=target_test,
            feature_columns=feature_columns,
            seed=seed,
        )
        ucm_summary, ucm_samples = _evaluate_method(
            train_frame=non_target_train,
            calibrate_frame=target_calibrate,
            test_frame=target_test,
            feature_columns=feature_columns,
            seed=seed,
        )

        per_method_user_metrics["UIM"].append(uim_summary)
        per_method_user_metrics["UCM"].append(ucm_summary)

        combined_samples = []
        for method_name, summary, samples in [
            ("UIM", uim_summary, uim_samples),
            ("UCM", ucm_summary, ucm_samples),
        ]:
            for sample in samples:
                combined_samples.append(
                    {
                        "iteration": iteration,
                        "seed": seed,
                        "target_user": target_user,
                        "method": method_name,
                        "true_label": sample["true_label"],
                        "predicted_label": sample["predicted_label"],
                        "coverage_hit": sample["coverage_hit"],
                        "prediction_set_size": sample["prediction_set_size"],
                        "prediction_set": sample["prediction_set"],
                    }
                )

        per_user_rows.append(
            {
                "iteration": iteration,
                "seed": seed,
                "target_user": target_user,
                "uim": uim_summary,
                "ucm": ucm_summary,
                "coverage_uplift": float(ucm_summary["coverage"] - uim_summary["coverage"]),
                "prediction_set_size_difference": float(
                    ucm_summary["average_prediction_set_size"] - uim_summary["average_prediction_set_size"]
                ),
            }
        )
        iteration_rows.extend(combined_samples)

    iteration_summary = {
        "iteration": iteration,
        "seed": seed,
        "ucm": {
            "coverage": float(np.mean([row["coverage"] for row in per_method_user_metrics["UCM"]])),
            "average_prediction_set_size": float(
                np.mean([row["average_prediction_set_size"] for row in per_method_user_metrics["UCM"]])
            ),
        },
        "uim": {
            "coverage": float(np.mean([row["coverage"] for row in per_method_user_metrics["UIM"]])),
            "average_prediction_set_size": float(
                np.mean([row["average_prediction_set_size"] for row in per_method_user_metrics["UIM"]])
            ),
        },
    }
    iteration_summary["coverage_uplift"] = float(iteration_summary["ucm"]["coverage"] - iteration_summary["uim"]["coverage"])
    iteration_summary["prediction_set_size_difference"] = float(
        iteration_summary["ucm"]["average_prediction_set_size"]
        - iteration_summary["uim"]["average_prediction_set_size"]
    )
    iteration_summary["per_user"] = per_user_rows
    return iteration_summary, iteration_rows, warnings


def _aggregate_overall(per_iteration: list[dict[str, Any]]) -> dict[str, Any]:
    ucm_coverages = [row["ucm"]["coverage"] for row in per_iteration]
    uim_coverages = [row["uim"]["coverage"] for row in per_iteration]
    ucm_sizes = [row["ucm"]["average_prediction_set_size"] for row in per_iteration]
    uim_sizes = [row["uim"]["average_prediction_set_size"] for row in per_iteration]
    coverage_uplifts = [row["coverage_uplift"] for row in per_iteration]
    set_size_differences = [row["prediction_set_size_difference"] for row in per_iteration]

    return {
        "ucm": {
            "coverage_mean": float(np.mean(ucm_coverages)),
            "coverage_std": float(np.std(ucm_coverages, ddof=1)) if len(ucm_coverages) > 1 else 0.0,
            "average_prediction_set_size_mean": float(np.mean(ucm_sizes)),
            "average_prediction_set_size_std": float(np.std(ucm_sizes, ddof=1)) if len(ucm_sizes) > 1 else 0.0,
        },
        "uim": {
            "coverage_mean": float(np.mean(uim_coverages)),
            "coverage_std": float(np.std(uim_coverages, ddof=1)) if len(uim_coverages) > 1 else 0.0,
            "average_prediction_set_size_mean": float(np.mean(uim_sizes)),
            "average_prediction_set_size_std": float(np.std(uim_sizes, ddof=1)) if len(uim_sizes) > 1 else 0.0,
        },
        "coverage_uplift": {
            "mean": float(np.mean(coverage_uplifts)),
            "std": float(np.std(coverage_uplifts, ddof=1)) if len(coverage_uplifts) > 1 else 0.0,
        },
        "prediction_set_size_difference": {
            "mean": float(np.mean(set_size_differences)),
            "std": float(np.std(set_size_differences, ddof=1)) if len(set_size_differences) > 1 else 0.0,
        },
    }


def _build_logbook(
    *,
    paths: WISDMPaths,
    source_record: dict[str, Any],
    protocol: StudyProtocol,
    metrics: dict[str, Any],
    artifacts: list[dict[str, Any]],
    started_at: str,
    completed_at: str,
) -> Path:
    artifact_rows = "\n".join(
        f"| {item['artifact_id']} | {item['artifact_type']} | {item['path']} | {item['sha256']} |"
        for item in artifacts
    )
    logbook_path = paths.logbook_dir / "LOGBOOK.md"
    body = f"""# Logbook: {STUDY_ID}

Дата и время создания: {completed_at}

## FACT
- Study ID: {STUDY_ID}
- Specification version: {SPECIFICATION_VERSION}
- Study version: {STUDY_VERSION}
- Source paper: {source_record['paper']['title']}
- Dataset: {source_record['dataset']['name']}
- Retained users: {', '.join(str(user) for user in source_record['dataset']['retained_users'])}
- Seeds: {', '.join(str(seed) for seed in protocol.seeds)}
- Started at: {started_at}
- Completed at: {completed_at}

### Metrics
| Metric | UCM | UIM | Difference |
|---|---:|---:|---:|
| empirical coverage | {metrics['overall']['ucm']['coverage_mean']:.6f} | {metrics['overall']['uim']['coverage_mean']:.6f} | {metrics['overall']['coverage_uplift']['mean']:.6f} |
| average prediction set size | {metrics['overall']['ucm']['average_prediction_set_size_mean']:.6f} | {metrics['overall']['uim']['average_prediction_set_size_mean']:.6f} | {metrics['overall']['prediction_set_size_difference']['mean']:.6f} |

### Artifacts
| artifact_id | artifact_type | path | sha256 |
|---|---|---|---|
{artifact_rows}

## INTERPRETATION
UCM calibration on target-user held-out data yielded the study-local coverage uplift estimate relative to UIM on the same target-user test rows.

## LIMITATION
- This is a single local CPU run.
- No publication or push was attempted.
- No synthetic data replaced WISDM.

## NEXT STEP
- Compare the obtained metrics against the paper tolerances in the reproduction report.
"""
    logbook_path.write_text(body, encoding="utf-8")
    return logbook_path


def _build_report(
    *,
    paths: WISDMPaths,
    source_record: dict[str, Any],
    metrics: dict[str, Any],
    artifacts: list[dict[str, Any]],
    started_at: str,
    completed_at: str,
    warnings: list[str],
) -> Path:
    artifact_rows = "\n".join(
        f"| {item['artifact_id']} | {item['path']} | {item['sha256']} |"
        for item in artifacts
    )
    report_path = paths.study_root / "reports" / "REPRODUCTION_REPORT.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    warning_block = "\n".join(f"- {warning}" for warning in warnings) if warnings else "- none"
    body = f"""# Reproduction Report: {STUDY_ID}

Status: {metrics['scientific_status']}

## Study
- Paper: {source_record['paper']['title']}
- Dataset: {source_record['dataset']['name']}
- Archive SHA-256: {source_record['dataset']['archive_sha256']}
- Processed rows: {source_record['dataset']['rows']}
- Retained users: {len(source_record['dataset']['retained_users'])}
- Started at: {started_at}
- Completed at: {completed_at}

## Results
| Metric | UCM | UIM | Difference |
|---|---:|---:|---:|
| empirical coverage | {metrics['overall']['ucm']['coverage_mean']:.6f} | {metrics['overall']['uim']['coverage_mean']:.6f} | {metrics['overall']['coverage_uplift']['mean']:.6f} |
| average prediction set size | {metrics['overall']['ucm']['average_prediction_set_size_mean']:.6f} | {metrics['overall']['uim']['average_prediction_set_size_mean']:.6f} | {metrics['overall']['prediction_set_size_difference']['mean']:.6f} |

## Protocol
- Seeds: {', '.join(str(seed) for seed in SEEDS)}
- Model: RandomForestClassifier(n_estimators=50, random_state=seed, n_jobs=1)
- Conformal method: SplitConformalClassifier(confidence_level=0.95, conformity_score="lac")
- UCM: target-user calibration only
- UIM: non-target calibration only

## Artifacts
| artifact_id | path | sha256 |
|---|---|---|
{artifact_rows}

## Warnings
{warning_block}

## Notes
- NO PUBLICATION
- NO PUSH
- NO SYNTHETIC REPLACEMENT
- FIRST REAL RUN ATTEMPTED
"""
    report_path.write_text(body, encoding="utf-8")
    return report_path


def run_first_reproduction(root_dir: Path | None = None) -> dict[str, Any]:
    paths = _project_paths(root_dir)
    _ensure_directories(paths)
    prepared = _prepare_dataset(paths)
    frame: pd.DataFrame = prepared["frame"]
    feature_columns: list[str] = prepared["feature_columns"]
    source_record: dict[str, Any] = prepared["source_record"]
    protocol: StudyProtocol = prepared["protocol"]

    started_at = _now_iso()
    warnings: list[str] = []
    raw_records: list[dict[str, Any]] = []
    per_iteration: list[dict[str, Any]] = []
    for iteration, seed in enumerate(SEEDS, start=1):
        iteration_summary, iteration_records, iteration_warnings = _run_iteration(
            frame=frame,
            feature_columns=feature_columns,
            seed=seed,
            iteration=iteration,
        )
        per_iteration.append(iteration_summary)
        raw_records.extend(iteration_records)
        warnings.extend(iteration_warnings)
    completed_at = _now_iso()

    metrics = {
        "study_id": STUDY_ID,
        "dataset": source_record["dataset"],
        "protocol": protocol.model_dump(mode="json"),
        "per_iteration": per_iteration,
        "overall": _aggregate_overall(per_iteration),
    }
    reference = {
        "ucm_coverage": 0.9628,
        "uim_coverage": 0.8876,
        "ucm_average_prediction_set_size": 2.04,
        "uim_average_prediction_set_size": 1.39,
        "coverage_tolerance": 0.01,
        "set_size_tolerance": 0.2,
    }
    coverage_within_tolerance = (
        abs(metrics["overall"]["ucm"]["coverage_mean"] - reference["ucm_coverage"]) <= reference["coverage_tolerance"]
        and abs(metrics["overall"]["uim"]["coverage_mean"] - reference["uim_coverage"]) <= reference["coverage_tolerance"]
    )
    set_size_within_tolerance = (
        abs(
            metrics["overall"]["ucm"]["average_prediction_set_size_mean"]
            - reference["ucm_average_prediction_set_size"]
        )
        <= reference["set_size_tolerance"]
        and abs(
            metrics["overall"]["uim"]["average_prediction_set_size_mean"]
            - reference["uim_average_prediction_set_size"]
        )
        <= reference["set_size_tolerance"]
    )
    if coverage_within_tolerance and set_size_within_tolerance and metrics["overall"]["coverage_uplift"]["mean"] > 0:
        scientific_status = "REPRODUCED"
    elif metrics["overall"]["coverage_uplift"]["mean"] > 0:
        scientific_status = "PARTIALLY_REPRODUCED"
    else:
        scientific_status = "NOT_REPRODUCED"
    metrics["reference"] = reference
    metrics["tolerance_checks"] = {
        "coverage_within_tolerance": coverage_within_tolerance,
        "set_size_within_tolerance": set_size_within_tolerance,
    }
    metrics["scientific_status"] = scientific_status

    experiment_dir = paths.experiments_dir / STUDY_EXPERIMENT_ID
    experiment_dir.mkdir(parents=True, exist_ok=True)
    raw_csv_path = experiment_dir / "raw_results.csv"
    raw_json_path = experiment_dir / "raw_results.json"
    metrics_path = paths.results_dir / "metrics.json"
    experiment_log_path = paths.logs_dir / f"{STUDY_EXPERIMENT_ID}.log"
    result_path = experiment_dir / "experiment_result.json"

    raw_frame = pd.DataFrame(raw_records)
    raw_frame.to_csv(raw_csv_path, index=False)
    _json_write(raw_json_path, raw_records)
    _json_write(metrics_path, metrics)

    experiment_log_path.write_text(
        "\n".join(
            [
                f"study_id={STUDY_ID}",
                f"started_at={started_at}",
                f"completed_at={completed_at}",
                f"scientific_status={scientific_status}",
                f"seed_count={len(SEEDS)}",
                f"retained_users={len(source_record['dataset']['retained_users'])}",
                f"warnings={len(warnings)}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    experiment_result = ExperimentResult(
        experiment_id=STUDY_EXPERIMENT_ID,
        started_at=started_at,
        completed_at=completed_at,
        status=WorkflowStatus.COMPLETED,
        parameters={
            "study_id": STUDY_ID,
            "dataset_archive_url": DATASET_ARCHIVE_URL,
            "dataset_page_url": DATASET_PAGE_URL,
            "paper_url": PAPER_URL,
            "code_url": CODE_URL,
            "seeds": SEEDS,
            "alpha": CONFORMAL_ALPHA,
            "confidence_level": CONFORMAL_CONFIDENCE,
            "model": "RandomForestClassifier(n_estimators=50, random_state=seed, n_jobs=1)",
            "conformal_method": 'SplitConformalClassifier(confidence_level=0.95, conformity_score="lac")',
            "split_strategy": {
                "non_target_train_size": 0.6,
                "target_calibration_size": 0.5,
            },
        },
        metrics=metrics,
        artifact_paths=[],
        environment={
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "numpy": np.__version__,
            "pandas": pd.__version__,
            "scikit_learn": sklearn.__version__,
            "mapie": mapie.__version__,
        },
        error_message=None,
    )
    source_record_path = paths.paper_dir / "source_record.json"
    data_manifest_path = paths.paper_dir / "data_manifest.json"
    claim_path = paths.claims_dir / "claim.json"
    plan_path = paths.plans_dir / "experiment_plan.json"
    artifact_inputs = [
        source_record_path,
        data_manifest_path,
        claim_path,
        plan_path,
        paths.archive_path,
        paths.arff_path,
        paths.processed_csv_path,
        raw_csv_path,
        raw_json_path,
        metrics_path,
        experiment_log_path,
        result_path,
    ]
    initial_result_artifact_paths = [
        portable_relative_path(path, project_root()) for path in artifact_inputs
    ]
    experiment_result = experiment_result.model_copy(update={"artifact_paths": initial_result_artifact_paths})
    result_path.write_text(
        json.dumps(experiment_result.model_dump(mode="json"), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    initial_artifacts = register_artifacts(paths.study_root, STUDY_EXPERIMENT_ID, artifact_inputs)
    logbook_path = _build_logbook(
        paths=paths,
        source_record=source_record,
        protocol=protocol,
        metrics=metrics,
        artifacts=[artifact.model_dump(mode="json") for artifact in initial_artifacts],
        started_at=started_at,
        completed_at=completed_at,
    )
    report_path = _build_report(
        paths=paths,
        source_record=source_record,
        metrics=metrics,
        artifacts=[artifact.model_dump(mode="json") for artifact in initial_artifacts],
        started_at=started_at,
        completed_at=completed_at,
        warnings=warnings,
    )
    final_artifact_inputs = [*artifact_inputs, logbook_path, report_path]
    final_result_artifact_paths = [
        portable_relative_path(path, project_root()) for path in final_artifact_inputs
    ]
    experiment_result = experiment_result.model_copy(update={"artifact_paths": final_result_artifact_paths})
    result_path.write_text(
        json.dumps(experiment_result.model_dump(mode="json"), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    register_artifacts(paths.study_root, STUDY_EXPERIMENT_ID, final_artifact_inputs)

    return {
        "status": scientific_status,
        "study_id": STUDY_ID,
        "study_version": STUDY_VERSION,
        "specification_version": SPECIFICATION_VERSION,
        "study_root": str(paths.study_root),
        "source_record": str(source_record_path),
        "data_manifest": str(data_manifest_path),
        "claim": str(claim_path),
        "experiment_plan": str(plan_path),
        "raw_archive": str(paths.archive_path),
        "raw_arff": str(paths.arff_path),
        "processed_csv": str(paths.processed_csv_path),
        "raw_results_csv": str(raw_csv_path),
        "raw_results_json": str(raw_json_path),
        "metrics": str(metrics_path),
        "experiment_result": str(result_path),
        "experiment_log": str(experiment_log_path),
        "logbook": str(logbook_path),
        "reproduction_report": str(report_path),
        "warnings": warnings,
        "metrics_summary": metrics,
        "result": experiment_result.model_dump(mode="json"),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the first WISDM reproduction study locally.")
    parser.add_argument("--root", type=Path, default=None, help="Project root; defaults to the current repository root.")
    args = parser.parse_args(argv)
    summary = run_first_reproduction(args.root)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
