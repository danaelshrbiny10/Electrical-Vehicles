"""Helper functions for model inference."""

import os
from pathlib import Path
import joblib

ROOT = Path(__file__).resolve().parents[1]
SAVED_DIR = ROOT / "models" / "saved"
SAVED_DIR.mkdir(parents=True, exist_ok=True)


def model_path(name: str) -> Path:
    return SAVED_DIR / name


def save_model(obj, name: str):
    path = model_path(name)
    joblib.dump(obj, path)


def load_model(name: str):
    path = model_path(name)
    if not path.exists():
        return None
    return joblib.load(path)
