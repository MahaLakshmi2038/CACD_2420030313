# Intelligent Cryptographic Defense Framework Against Modern Ransomware Using Behavioral Analysis

## Project Overview

This project explores ransomware detection using machine learning and file entropy analysis. It includes a Random Forest baseline model trained on precomputed dataset features and a Python utility for measuring the Shannon entropy of individual files.

## Technologies Used

- Python
- pandas
- scikit-learn
- joblib
- Shannon entropy analysis

## Machine Learning Model

- **Algorithm:** Random Forest Classifier
- **Number of trees:** 200
- **Input features:** 483
- **Test samples:** 975

### Evaluation Results

- **Accuracy:** 97.13%
- **Correct predictions:** 947 out of 975
- **Incorrect predictions:** 28 out of 975

Confusion matrix (rows = actual class, columns = predicted class):

| Actual / Predicted | Class 0 | Class 1 |
|---|---:|---:|
| Class 0 | 493 | 17 |
| Class 1 | 11 | 454 |

The meanings of class 0 and class 1 must be verified using the original dataset documentation before assigning benign or ransomware labels.

## File Entropy Analysis

The script `src/detect_file.py` reports file size, Shannon entropy in bits per byte, and whether the saved Random Forest model loads successfully.

Example command:

```powershell
python src/detect_file.py sample_files/sample.txt
```

## Limitations

- The model requires 483 precomputed input features.
- The current file-analysis script does not extract those features or classify arbitrary files using the model.
- High entropy is not proof of ransomware.
- The reported accuracy applies to the provided test dataset, not to arbitrary files or live systems.
- This is a research prototype, not a validated real-time ransomware protection system.

## Repository Structure

- `dataset/` â€” Raw and processed datasets
- `models/` â€” Saved machine learning model
- `notebooks/` â€” Dataset exploration and entropy analysis
- `sample_files/` â€” Sample files for testing
- `src/` â€” Python utility scripts
- `logs/` â€” Log directory

## Future Improvements

- Verify the original dataset labels and feature definitions.
- Implement and validate the correct 483-feature extraction pipeline.
- Integrate file and behavioral analysis with the trained model.
- Add safe testing, logging, and evaluation on unseen samples.

## Disclaimer

For educational and defensive cybersecurity research only.
