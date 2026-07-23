from __future__ import annotations

import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import huggingface_hub.constants as hf_constants

from .models import AuthStatus, AuthStatusReport, TokenSourceCategory, WriteReadiness


def hf_cli_path() -> Path | None:
    local_cli = Path(sys.executable).with_name("hf")
    if local_cli.exists():
        return local_cli
    resolved = shutil.which("hf")
    return Path(resolved) if resolved else None


def _token_source_category() -> TokenSourceCategory:
    if os.environ.get("HF" + "_TOKEN"):
        return TokenSourceCategory.HF_ENV_TOKEN
    token_path = Path(os.environ.get("HF" + "_TOKEN_PATH", getattr(hf_constants, "HF" + "_TOKEN_PATH")))
    if token_path.exists():
        return TokenSourceCategory.HF_CACHE_TOKEN
    default_token = Path(hf_constants.HF_HOME) / "token"
    if default_token.exists():
        return TokenSourceCategory.HF_LOCAL_CACHE
    return TokenSourceCategory.NONE


def _run_whoami(cli: Path) -> tuple[bool, str | None]:
    try:
        proc = subprocess.run([str(cli), "auth", "whoami"], check=False, capture_output=True, text=True)
    except OSError:
        return False, None
    if proc.returncode != 0:
        return False, None
    username = proc.stdout.splitlines()[0].strip() if proc.stdout.splitlines() else None
    return True, username or None


def get_hf_auth_status() -> AuthStatus:
    cli = hf_cli_path()
    authenticated = False
    username = None
    if cli is not None:
        authenticated, username = _run_whoami(cli)
    token_source_category = _token_source_category() if authenticated else TokenSourceCategory.NONE
    if not authenticated:
        write_readiness = WriteReadiness.NOT_AUTHENTICATED
    else:
        write_readiness = WriteReadiness.NOT_VERIFIED
    return AuthStatus(
        cli_installed=cli is not None,
        authenticated=authenticated,
        username=username,
        token_source_category=token_source_category,
        write_readiness=write_readiness,
        checked_at=datetime.now(timezone.utc),
    )


def get_hf_auth_report() -> AuthStatusReport:
    cli = hf_cli_path()
    installed_version = None
    if cli is not None:
        try:
            installed_version = subprocess.run(
                [str(cli), "--version"], check=True, capture_output=True, text=True
            ).stdout.strip()
        except Exception:
            installed_version = None
    return AuthStatusReport(
        auth_status=get_hf_auth_status(),
        installed_version=installed_version,
        cli_path=str(cli) if cli else None,
    )
