from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression
import numpy as np
import joblib
from data_processing import load_and_process_data

# Load and preprocess data
file_path = "Salary_Data.csv"
X_train, X_test, y_train, y_test, preprocessor = load_and_process_data(file_path)

# Define model (only Linear Regression)
model = LinearRegression()

# Build pipeline
clf = Pipeline(steps=[("preprocessor", preprocessor), ("model", model)])

# Train model
clf.fit(X_train, y_train)

# Predictions
preds = clf.predict(X_test)

# Evaluate
rmse = np.sqrt(mean_squared_error(y_test, preds))
r2 = r2_score(y_test, preds)

print("📊 Linear Regression Results")
print(f"   RMSE: {rmse:.2f}")
print(f"   R2 Score: {r2:.3f}")

# Save model
joblib.dump(clf, "salary_prediction_model.pkl")
print("✅ Model saved as salary_prediction_model.pkl")
