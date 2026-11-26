"""Loads the trained models and predicts category + priority for a ticket."""
from pathlib import Path

import joblib

MODEL_DIR = Path(__file__).parent / "model"
_models = {}


def _load(name):
    if name not in _models:
        path = MODEL_DIR / f"{name}.joblib"
        _models[name] = joblib.load(path) if path.exists() else None
    return _models[name]


def predict(title: str, description: str):
    """Returns (category, priority, used_ai). Falls back to defaults if no model."""
    text = f"{title} {description}".strip()
    cat_model, pri_model = _load("category"), _load("priority")
    if cat_model is None or pri_model is None:
        return "General", "Medium", False
    return cat_model.predict([text])[0], pri_model.predict([text])[0], True
