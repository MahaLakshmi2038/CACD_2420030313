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

Class 0 represents goodware (benign files), and class 1 represents ransomware, verified against the original MLRan dataset metadata. The dataset contains 2,550 goodware samples and 2,330 ransomware samples.

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


## Feature Mapping and Importance Analysis

The project includes the original MLRan feature-name mapping at `dataset/raw/RFE_selected_feature_names_dic.json`. The mapping contains 483 entries, and all 483 feature IDs were verified against the training dataset with no missing or extra mappings.

The top 20 features ranked by the existing feature-importance analysis are available in `dataset/processed/top20_feature_importance_named.csv`. This report includes each feature ID, its original feature name, and its importance score. The original `top20_feature_importance.csv` is preserved.

Feature importance indicates how features contribute to the trained model's predictions; it does not establish that an individual API call, DLL load, registry operation, or string is malicious. These results should be interpreted in the context of the dataset and model evaluation.
