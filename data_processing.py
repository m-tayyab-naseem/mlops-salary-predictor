import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

def load_and_process_data(file_path):
    df = pd.read_csv(file_path)

    # Drop rows where target is missing
    df = df.dropna(subset=["Salary"])

    # Separate features and target
    X = df.drop("Salary", axis=1)
    y = df["Salary"]

    # Columns
    categorical_low = ["Gender", "Education Level"]  # one-hot
    categorical_high = ["Job Title"]                 # ordinal encoding
    numeric_cols = ["Age", "Years of Experience"]

    # Transformers
    numeric_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median"))
    ])

    categorical_low_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore"))
    ])

    categorical_high_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("ordinal", OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1))
    ])

    # Combine preprocessing
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_cols),
            ("cat_low", categorical_low_transformer, categorical_low),
            ("cat_high", categorical_high_transformer, categorical_high),
        ]
    )

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    return X_train, X_test, y_train, y_test, preprocessor
