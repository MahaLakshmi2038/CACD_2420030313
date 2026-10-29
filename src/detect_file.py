from pathlib import Path
from collections import Counter
import math
import joblib
import sys

MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "random_forest_baseline.joblib"

def calculate_entropy(file_path):
    data = Path(file_path).read_bytes()
    if not data:
        return 0.0
    counts = Counter(data)
    total = len(data)
    return -sum(
        (count / total) * math.log2(count / total)
        for count in counts.values()
    )

def main():
    if len(sys.argv) != 2:
        print("Usage: python src/detect_file.py <file_path>")
        return

    file_path = Path(sys.argv[1])
    if not file_path.is_file():
        print(f"Error: file not found: {file_path}")
        return

    try:
        model = joblib.load(MODEL_PATH)
        entropy = calculate_entropy(file_path)
        print(f"File: {file_path.name}")
        print(f"Size: {file_path.stat().st_size} bytes")
        print(f"Shannon entropy: {entropy:.4f} bits/byte")
        print("Saved Random Forest model loaded successfully.")
        print("Note: entropy is reported separately; this script does not")
        print("classify the file with the model because its 483 input")
        print("features must come from the original dataset feature pipeline.")
    except Exception as exc:
        print(f"Error: {exc}")

if __name__ == "__main__":
    main()
