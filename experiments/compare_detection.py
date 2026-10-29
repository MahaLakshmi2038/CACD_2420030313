import math
import random
import tempfile
from collections import Counter
from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)
from sklearn.model_selection import train_test_split


RANDOM_STATE = 42


def entropy(data):
    """Calculate Shannon entropy in bits per byte."""
    if not data:
        return 0.0

    counts = Counter(data)
    total = len(data)

    return -sum(
        (count / total) * math.log2(count / total)
        for count in counts.values()
    )


import random
from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)
from sklearn.model_selection import train_test_split


RANDOM_STATE = 42


def create_dataset(number_per_class=300):
    """
    Generate a controlled synthetic dataset for comparing:
    1. Behavioral indicators
    2. Cryptographic indicators
    3. Combined hybrid indicators

    IMPORTANT:
    This dataset is simulated. It is not evidence of real-world
    ransomware detection performance.
    """
    rng = random.Random(RANDOM_STATE)
    records = []

    for label in (0, 1):
        for _ in range(number_per_class):
            # Overlapping ranges: neither class is perfectly separable.
            files_modified = rng.randint(1, 40)
            rename_count = rng.randint(0, 20)
            write_count = rng.randint(1, 60)
            entropy_change = rng.uniform(-0.2, 1.5)
            high_entropy_ratio = rng.uniform(0.0, 1.0)

            # Weak simulated tendencies, not deterministic rules.
            if label == 1:
                files_modified += rng.randint(0, 8)
                write_count += rng.randint(0, 12)
                entropy_change += rng.uniform(0.0, 0.25)
                high_entropy_ratio += rng.uniform(0.0, 0.15)
            else:
                files_modified += rng.randint(0, 3)

            records.append({
                "files_modified": min(files_modified, 60),
                "rename_count": rename_count,
                "write_count": min(write_count, 80),
                "entropy_change": min(entropy_change, 1.5),
                "high_entropy_ratio": min(high_entropy_ratio, 1.0),
                "label": label,
            })

    frame = pd.DataFrame(records)
    return frame.sample(
        frac=1,
        random_state=RANDOM_STATE,
    ).reset_index(drop=True)


def evaluate_model(
    name,
    frame,
    feature_columns,
    train_indices,
    test_indices,
):
    model = RandomForestClassifier(
        n_estimators=200,
        random_state=RANDOM_STATE,
        class_weight="balanced",
        n_jobs=-1,
    )

    X = frame[feature_columns]
    y = frame["label"]

    model.fit(X.iloc[train_indices], y.iloc[train_indices])

    predictions = model.predict(X.iloc[test_indices])
    actual = y.iloc[test_indices]

    tn, fp, fn, tp = confusion_matrix(
        actual,
        predictions,
        labels=[0, 1],
    ).ravel()

    false_positive_rate = (
        fp / (fp + tn) if (fp + tn) else 0.0
    )

    return {
        "approach": name,
        "accuracy": accuracy_score(actual, predictions),
        "precision": precision_score(
            actual, predictions, zero_division=0
        ),
        "recall": recall_score(
            actual, predictions, zero_division=0
        ),
        "f1_score": f1_score(
            actual, predictions, zero_division=0
        ),
        "false_positive_rate": false_positive_rate,
        "true_negatives": tn,
        "false_positives": fp,
        "false_negatives": fn,
        "true_positives": tp,
    }


def main():
    frame = create_dataset()

    train_indices, test_indices = train_test_split(
        list(range(len(frame))),
        test_size=0.25,
        random_state=RANDOM_STATE,
        stratify=frame["label"],
    )

    behavioral_features = [
        "files_modified",
        "rename_count",
        "write_count",
    ]

    crypto_features = [
        "entropy_change",
        "high_entropy_ratio",
    ]

    hybrid_features = behavioral_features + crypto_features

    results = [
        evaluate_model(
            "Behavioral only",
            frame,
            behavioral_features,
            train_indices,
            test_indices,
        ),
        evaluate_model(
            "Cryptographic only",
            frame,
            crypto_features,
            train_indices,
            test_indices,
        ),
        evaluate_model(
            "Hybrid",
            frame,
            hybrid_features,
            train_indices,
            test_indices,
        ),
    ]

    results_frame = pd.DataFrame(results)

    output_dir = Path(__file__).resolve().parent
    output_path = output_dir / "comparison_results.csv"

    results_frame.to_csv(output_path, index=False)

    display_columns = [
        "approach",
        "accuracy",
        "precision",
        "recall",
        "f1_score",
        "false_positive_rate",
    ]

    print("\n=== SYNTHETIC DETECTION COMPARISON ===")
    print("Samples:", len(frame))
    print("Training samples:", len(train_indices))
    print("Test samples:", len(test_indices))
    print("\nMetrics:")
    print(
        results_frame[display_columns]
        .round(3)
        .to_string(index=False)
    )

    print("\nConfusion matrix counts:")
    print("Rows: actual [0, 1]; columns: predicted [0, 1]")
    for _, row in results_frame.iterrows():
        print(
            f"{row['approach']}: "
            f"[[{row['true_negatives']}, {row['false_positives']}], "
            f"[{row['false_negatives']}, {row['true_positives']}]]"
        )

    print(f"\nResults saved to: {output_path}")
    print(
        "\nLIMITATION: These results use simulated indicators and labels. "
        "They demonstrate the experimental workflow only and do not "
        "measure real-world ransomware detection performance."
    )


if __name__ == "__main__":
    main()