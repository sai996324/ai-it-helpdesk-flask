"""Train the ticket classifiers (category + priority) and report real accuracy.

Run:  python train_model.py
Uses data/tickets.csv (create it with: python data/make_dataset.py).
"""
import csv
from pathlib import Path

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline

BASE = Path(__file__).parent
DATA = BASE / "data" / "tickets.csv"
MODEL_DIR = BASE / "model"


def load():
    texts, cats, pris = [], [], []
    with DATA.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            texts.append(row["text"])
            cats.append(row["category"])
            pris.append(row["priority"])
    return texts, cats, pris


def build():
    return make_pipeline(
        TfidfVectorizer(ngram_range=(1, 2), lowercase=True),
        LogisticRegression(max_iter=1000),
    )


def main():
    if not DATA.exists():
        raise SystemExit("Missing data/tickets.csv. Run: python data/make_dataset.py")
    texts, cats, pris = load()
    MODEL_DIR.mkdir(exist_ok=True)

    for name, labels in (("category", cats), ("priority", pris)):
        X_train, X_test, y_train, y_test = train_test_split(
            texts, labels, test_size=0.2, random_state=42, stratify=labels
        )
        model = build().fit(X_train, y_train)
        acc = accuracy_score(y_test, model.predict(X_test))
        print(f"{name:9s} accuracy on held-out test set: {acc:.2%}")
        # refit on all data for the final saved model
        final = build().fit(texts, labels)
        joblib.dump(final, MODEL_DIR / f"{name}.joblib")
    print("Models saved in model/")


if __name__ == "__main__":
    main()
