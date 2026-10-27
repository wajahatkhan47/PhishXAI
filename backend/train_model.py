
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

import joblib


# Project folders
BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BACKEND_DIR.parent
DATASET_PATH = PROJECT_DIR / "data" / "url_features_extracted1.csv"

# Check dataset
if not DATASET_PATH.exists():
    print("Dataset file nahi mili!")
    print("Expected location:", DATASET_PATH)
else:
    df = pd.read_csv(DATASET_PATH)

    print("Dataset successfully loaded!")
    print("Dataset shape:", df.shape)

    print("\nFirst 5 rows:")
    print(df.head())

    print("\nColumn names:")
    print(df.columns.tolist())
    
    print("\nClassLabel counts:")
    print(df["ClassLabel"].value_counts(dropna=False))

    print("\nMissing values:")
    print(df.isnull().sum().sum())
    
# Remove rows with missing values
df = df.dropna().copy()

print("\nDataset after removing missing values:")
print("Shape:", df.shape)
print("Missing values remaining:", df.isnull().sum().sum())

# Separate input features and target label
feature_columns = [
    "url_length",
    "has_ip_address",
    "dot_count",
    "https_flag",
    "url_entropy",
    "token_count",
    "subdomain_count",
    "query_param_count",
    "tld_length",
    "path_length",
    "has_hyphen_in_domain",
    "number_of_digits",
    "tld_popularity",
    "suspicious_file_extension",
    "domain_name_length",
    "percentage_numeric_chars"
]

X = df[feature_columns]
y = df["ClassLabel"].astype(int)

print("\nFeatures and target prepared!")
print("X shape:", X.shape)
print("y shape:", y.shape)
print("Target classes:", sorted(y.unique()))

from sklearn.model_selection import train_test_split

# Split dataset: 80% training, 20% testing
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nDataset split completed!")
print("Training features:", X_train.shape)
print("Testing features:", X_test.shape)
print("Training labels:", y_train.shape)
print("Testing labels:", y_test.shape)





# Create and train the Random Forest model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

print("\nTraining Random Forest model...")
model.fit(X_train, y_train)

print("Model training completed successfully!")



from sklearn.metrics import accuracy_score, classification_report

# Predict on unseen test data
y_pred = model.predict(X_test)

# Evaluate model
accuracy = accuracy_score(y_test, y_pred)

print("\nModel Evaluation Results")
print("------------------------")
print(f"Accuracy: {accuracy * 100:.2f}%")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))
print("\n--- LABEL DISTRIBUTION ---")
print(df["ClassLabel"].value_counts().sort_index())

print("\n--- LABEL MEANING CHECK ---")
print("Class 0 examples:")
print(df[df["ClassLabel"] == 0]["URL"].head(5).to_string(index=False))

print("\nClass 1 examples:")
print(df[df["ClassLabel"] == 1]["URL"].head(5).to_string(index=False))



# Save trained model and feature columns
MODEL_PATH = BACKEND_DIR / "phishxai_model.joblib"
FEATURES_PATH = BACKEND_DIR / "feature_columns.joblib"

joblib.dump(model, MODEL_PATH)
joblib.dump(feature_columns, FEATURES_PATH)

print("\nModel saved successfully!")
print("Model location:", MODEL_PATH)
print("Feature columns saved:", FEATURES_PATH)
