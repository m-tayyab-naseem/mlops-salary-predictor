import joblib
import pandas as pd

def predict_salary(age, gender, education, job_title, experience):
    # Load trained model
    model = joblib.load("salary_prediction_model.pkl")

    # Create input DataFrame
    sample = {
        "Age": [age],
        "Gender": [gender],
        "Education Level": [education],
        "Job Title": [job_title],
        "Years of Experience": [experience]
    }
    sample_df = pd.DataFrame(sample)

    # Predict salary
    prediction = model.predict(sample_df)
    return prediction[0]

if __name__ == "__main__":
    # Example usage
    salary = predict_salary(28, "Female", "Master's", "Data Analyst", 3)
    print(f"Predicted Salary: {salary:.2f}")
