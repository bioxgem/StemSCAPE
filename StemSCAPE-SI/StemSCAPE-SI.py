#!/usr/bin/python3
"""
RandomForestClassifier + tree-based SHAP for Cancer Stemness Index (StemSCAPE-SI) prediction.

This script trains a Random Forest model and calculates SHAP values 
for feature interpretation on both training and testing datasets.
The label column in the testing file is optional.

Usage:
    python StemSCAPE-SI.py \
        -i training.txt \  # Training data file (tab-separated)
        -e testing.txt \   # Testing/Prediction data file (tab-separated). Label is OPTIONAL.
        -l TARGET_COL \    # Target label column name (Required for training data)
        -s SAMPLE_ID_COL \ # Sample ID column name (Optional)
        -o ./output_dir    # Output directory for results
"""

import argparse
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import os
import shap

def encode_non_numeric(X):
    """
    Performs Label Encoding on all non-numeric columns in the DataFrame X.
    This is necessary to handle categorical features before model training.
    """
    non_numeric = X.select_dtypes(exclude=[np.number]).columns.tolist()
    for col in non_numeric:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col].astype(str))
    return X

def process_data(filepath, label_col, sample_col, le_y, is_train):
    """
    Loads data, extracts IDs, splits X/y, and performs Label Encoding on features (X) and labels (y).
    The label column (y) is optional for the testing file (is_train=False).
    Returns: ids (str array), X (features DF), y_enc (encoded labels array or None)
    """
    df = pd.read_csv(filepath, sep='\t')
    name = os.path.basename(filepath)

    # Extract sample IDs
    ids = df[sample_col].astype(str).values if sample_col else [f"sample_{i}" for i in range(len(df))]
    
    has_label = label_col in df.columns
    
    if is_train and not has_label:
        # Training set must have the label column
        raise ValueError(f"Training file ('{name}') missing required label column '{label_col}'")

    if has_label:
        # Split features (X) and labels (y)
        X = df.drop(columns=[label_col] + ([sample_col] if sample_col else []))
        y = df[label_col]
        # Fit/transform y labels (training) or just transform (testing)
        y_enc = le_y.fit_transform(y.astype(str)) if is_train else le_y.transform(y.astype(str))
    else:
        # Testing set without label: drop only the sample ID column
        X = df.drop(columns=([sample_col] if sample_col else []))
        y_enc = None # Labels are not available

    # Encode non-numeric features in X
    X = encode_non_numeric(X)
    
    return ids, X, y_enc 

def output_shap_results(ids, X, model, explainer, baseline_class1, outdir, name):
    """
    Calculates SHAP values and prediction probabilities, then writes the results to a TSV file.
    Only the SHAP values corresponding to the positive class (class 1) are outputted.
    """
    
    # Calculate SHAP values and RF prediction probabilities
    shap_values = explainer.shap_values(X)
    si = model.predict_proba(X)[:, 1] 
    
    # Extract SHAP values for the positive class (class 1, assumed index 1)
    if isinstance(shap_values, list) and len(shap_values) > 1:
        shap_array = shap_values[1]
    elif isinstance(shap_values, np.ndarray) and shap_values.ndim == 3:
        shap_array = shap_values[:, :, 1]
    else:
        # Fallback for 2D array (e.g., if model has only one output class)
        shap_array = shap_values 
        
    # Create output DataFrame
    df_shap = pd.DataFrame(shap_array, columns=X.columns, index=ids)
    df_shap.insert(0, 'SampleID', ids)
    df_shap.insert(1, 'baseline_value', baseline_class1)
    df_shap.insert(2, 'StemSCAPE-SI', si)
    
    # Write to file (e.g., 'training_shap.tsv' or 'testing_shap.tsv')
    output_filename = os.path.join(outdir, f'{name}_shap.tsv')
    df_shap.to_csv(output_filename, sep='\t', index=False)
    
    return shap_array # Return SHAP array for mean absolute SHAP calculation


def main():
    # Setup Argument Parser
    parser = argparse.ArgumentParser(description='Random Forest Classification and SHAP Interpretation for Stemness Prediction.')
    parser.add_argument('-i', '--train', required=True, help='Path to the training data file (tab-separated).')
    parser.add_argument('-e', '--test', required=True, help='Path to the testing/prediction data file (tab-separated). Label column is optional.')
    parser.add_argument('-l', '--label', required=True, help='Column name for the target label (e.g., TARGET_COL).')
    parser.add_argument('-s', '--sample', default=None, help='Column name for Sample ID (e.g., SAMPLE_ID_COL).')
    parser.add_argument('-o', '--outdir', required=True, help='Path to the output directory.')
    args = parser.parse_args()

    # Create output directory
    os.makedirs(args.outdir, exist_ok=True)
    
    # 1. Data Loading and Preprocessing
    le_y = LabelEncoder()
    # Process training data (is_train=True)
    train_ids, X_train, y_train_enc = process_data(args.train, args.label, args.sample, le_y, is_train=True)
    # Process testing data (is_train=False, label is optional)
    test_ids, X_test, y_test_enc = process_data(args.test, args.label, args.sample, le_y, is_train=False)

    # 2. Model Training
    # Use class_weight="balanced" to handle potential class imbalance
    model = RandomForestClassifier(
        class_weight="balanced",
        min_samples_split=2, 
        min_samples_leaf=1,
    )
    model.fit(X_train, y_train_enc)
    
    # 3. RF Feature Importance
    feat_importance = pd.DataFrame({
        'Feature': X_train.columns,
        'RF_FeatureImportance': model.feature_importances_
    })

    # 4. SHAP Calculation and Output
    explainer = shap.TreeExplainer(model)
    baseline_array = np.array(explainer.expected_value)
    
    # Determine the baseline value for the positive class (class 1)
    baseline_class1 = baseline_array[1] if baseline_array.ndim > 0 and len(baseline_array) > 1 else baseline_array[0]

    # Calculate SHAP values and output results for training set
    train_shap_array = output_shap_results(
        train_ids, X_train, model, explainer, baseline_class1, args.outdir, 'training'
    )
    
    # Calculate SHAP values and output results for testing/prediction set
    output_shap_results(
        test_ids, X_test, model, explainer, baseline_class1, args.outdir, 'testing'
    )

    # 5. Calculate Mean Absolute SHAP (using training data's class 1 SHAP values)
    mean_abs_shap = np.mean(np.abs(train_shap_array), axis=0)
    feat_importance['MeanAbsSHAP'] = mean_abs_shap

    # 6. Output Feature Importance vs. Mean Abs SHAP
    feat_importance.sort_values('RF_FeatureImportance', ascending=False) \
        .to_csv(os.path.join(args.outdir, 'feature_importance_vs_shap.tsv'), sep='\t', index=False)

    print(f"--- Analysis Complete ---")
    print(f"Results successfully saved to: {args.outdir}")


if __name__ == '__main__':
    main()