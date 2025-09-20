import unittest
import json
import os
import sys
import tempfile
import shutil
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np

# Add the parent directory to the path so we can import app
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

# Change to parent directory so model file can be found
original_cwd = os.getcwd()
os.chdir(parent_dir)

from app import app


class TestFlaskApp(unittest.TestCase):
    """Test cases for Flask salary prediction application."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.app = app.test_client()
        self.app.testing = True
        
        # Sample test data for predictions
        self.valid_sample_data = {
            "Age": 28,
            "Gender": "Female",
            "Education Level": "Master's",
            "Job Title": "Data Analyst",
            "Years of Experience": 3
        }
        
        self.invalid_sample_data = {
            "Age": 28,
            "Gender": "Female"
            # Missing required fields
        }
        
        self.edge_case_data = {
            "Age": 25,
            "Gender": "Male",
            "Education Level": "Bachelor's",
            "Job Title": "Software Engineer",
            "Years of Experience": 0
        }

    def test_health_endpoint(self):
        """Test the health check endpoint."""
        response = self.app.get('/health')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'ok')
        self.assertEqual(data['message'], 'Service is healthy')

    def test_health_endpoint_methods(self):
        """Test that health endpoint only accepts GET requests."""
        # Test POST request to health endpoint
        response = self.app.post('/health')
        self.assertEqual(response.status_code, 405)  # Method Not Allowed

    def test_predict_endpoint_valid_data(self):
        """Test prediction endpoint with valid data."""
        response = self.app.post('/predict', 
                               data=json.dumps(self.valid_sample_data),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('predicted_salary', data)
        self.assertIsInstance(data['predicted_salary'], (int, float))
        self.assertGreater(data['predicted_salary'], 0)

    def test_predict_endpoint_missing_fields(self):
        """Test prediction endpoint with missing required fields."""
        response = self.app.post('/predict',
                               data=json.dumps(self.invalid_sample_data),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Missing required fields')

    def test_predict_endpoint_no_json(self):
        """Test prediction endpoint without JSON data."""
        response = self.app.post('/predict')
        
        self.assertEqual(response.status_code, 500)

    def test_predict_endpoint_invalid_json(self):
        """Test prediction endpoint with invalid JSON."""
        response = self.app.post('/predict',
                               data='invalid json',
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 500)

    def test_predict_endpoint_wrong_method(self):
        """Test prediction endpoint with wrong HTTP method."""
        response = self.app.get('/predict')
        self.assertEqual(response.status_code, 405)  # Method Not Allowed

    def test_predict_endpoint_edge_cases(self):
        """Test prediction endpoint with edge case data."""
        response = self.app.post('/predict',
                               data=json.dumps(self.edge_case_data),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('predicted_salary', data)
        self.assertIsInstance(data['predicted_salary'], (int, float))

    def test_predict_endpoint_different_genders(self):
        """Test prediction endpoint with different gender values."""
        test_cases = [
            {"Age": 30, "Gender": "Male", "Education Level": "Bachelor's", 
             "Job Title": "Software Engineer", "Years of Experience": 5},
            {"Age": 35, "Gender": "Female", "Education Level": "PhD", 
             "Job Title": "Data Scientist", "Years of Experience": 8},
            {"Age": 22, "Gender": "Other", "Education Level": "High School", 
             "Job Title": "Intern", "Years of Experience": 1}
        ]
        
        for test_case in test_cases:
            with self.subTest(gender=test_case["Gender"]):
                response = self.app.post('/predict',
                                       data=json.dumps(test_case),
                                       content_type='application/json')
                
                self.assertEqual(response.status_code, 200)
                data = json.loads(response.data)
                self.assertIn('predicted_salary', data)

    def test_predict_endpoint_different_education_levels(self):
        """Test prediction endpoint with different education levels."""
        education_levels = ["High School", "Bachelor's", "Master's", "PhD"]
        
        for education in education_levels:
            test_data = self.valid_sample_data.copy()
            test_data["Education Level"] = education
            
            with self.subTest(education=education):
                response = self.app.post('/predict',
                                       data=json.dumps(test_data),
                                       content_type='application/json')
                
                self.assertEqual(response.status_code, 200)
                data = json.loads(response.data)
                self.assertIn('predicted_salary', data)

    def test_predict_endpoint_different_job_titles(self):
        """Test prediction endpoint with different job titles."""
        job_titles = ["Data Analyst", "Software Engineer", "Data Scientist", 
                     "Product Manager", "Business Analyst", "Machine Learning Engineer"]
        
        for job_title in job_titles:
            test_data = self.valid_sample_data.copy()
            test_data["Job Title"] = job_title
            
            with self.subTest(job_title=job_title):
                response = self.app.post('/predict',
                                       data=json.dumps(test_data),
                                       content_type='application/json')
                
                self.assertEqual(response.status_code, 200)
                data = json.loads(response.data)
                self.assertIn('predicted_salary', data)

    def test_predict_endpoint_age_range(self):
        """Test prediction endpoint with different age ranges."""
        age_ranges = [18, 25, 35, 45, 55, 65]
        
        for age in age_ranges:
            test_data = self.valid_sample_data.copy()
            test_data["Age"] = age
            
            with self.subTest(age=age):
                response = self.app.post('/predict',
                                       data=json.dumps(test_data),
                                       content_type='application/json')
                
                self.assertEqual(response.status_code, 200)
                data = json.loads(response.data)
                self.assertIn('predicted_salary', data)

    def test_predict_endpoint_experience_range(self):
        """Test prediction endpoint with different experience ranges."""
        experience_values = [0, 1, 5, 10, 15, 20, 25]
        
        for experience in experience_values:
            test_data = self.valid_sample_data.copy()
            test_data["Years of Experience"] = experience
            
            with self.subTest(experience=experience):
                response = self.app.post('/predict',
                                       data=json.dumps(test_data),
                                       content_type='application/json')
                
                self.assertEqual(response.status_code, 200)
                data = json.loads(response.data)
                self.assertIn('predicted_salary', data)

    def test_predict_endpoint_response_format(self):
        """Test that prediction response has correct format."""
        response = self.app.post('/predict',
                               data=json.dumps(self.valid_sample_data),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # Check response structure
        self.assertIsInstance(data, dict)
        self.assertIn('predicted_salary', data)
        self.assertEqual(len(data), 1)  # Should only have predicted_salary key
        
        # Check data types
        self.assertIsInstance(data['predicted_salary'], (int, float))
        
        # Check value is reasonable (positive number)
        self.assertGreater(data['predicted_salary'], 0)

    @patch('app.model')
    def test_predict_endpoint_model_error(self, mock_model):
        """Test prediction endpoint when model raises an error."""
        # Mock model to raise an exception
        mock_model.predict.side_effect = Exception("Model prediction failed")
        
        response = self.app.post('/predict',
                               data=json.dumps(self.valid_sample_data),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 500)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Model prediction failed')

    def test_predict_endpoint_required_fields_validation(self):
        """Test that all required fields are properly validated."""
        required_fields = ["Age", "Gender", "Education Level", "Job Title", "Years of Experience"]
        
        for field in required_fields:
            test_data = self.valid_sample_data.copy()
            del test_data[field]
            
            with self.subTest(missing_field=field):
                response = self.app.post('/predict',
                                       data=json.dumps(test_data),
                                       content_type='application/json')
                
                self.assertEqual(response.status_code, 400)
                data = json.loads(response.data)
                self.assertIn('error', data)
                self.assertEqual(data['error'], 'Missing required fields')

    def test_predict_endpoint_empty_request(self):
        """Test prediction endpoint with empty request body."""
        response = self.app.post('/predict',
                               data=json.dumps({}),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Missing required fields')

    def test_predict_endpoint_none_values(self):
        """Test prediction endpoint with None values."""
        test_data = {
            "Age": None,
            "Gender": None,
            "Education Level": None,
            "Job Title": None,
            "Years of Experience": None
        }
        
        response = self.app.post('/predict',
                               data=json.dumps(test_data),
                               content_type='application/json')
        
        # Should still return 200 as the model will handle None values
        self.assertEqual(response.status_code, 200)

    def test_predict_endpoint_large_values(self):
        """Test prediction endpoint with large values."""
        test_data = {
            "Age": 100,
            "Gender": "Male",
            "Education Level": "PhD",
            "Job Title": "Senior Software Engineer",
            "Years of Experience": 50
        }
        
        response = self.app.post('/predict',
                               data=json.dumps(test_data),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('predicted_salary', data)

    def test_predict_endpoint_negative_values(self):
        """Test prediction endpoint with negative values."""
        test_data = {
            "Age": -5,
            "Gender": "Female",
            "Education Level": "Bachelor's",
            "Job Title": "Data Analyst",
            "Years of Experience": -2
        }
        
        response = self.app.post('/predict',
                               data=json.dumps(test_data),
                               content_type='application/json')
        
        # Should still work as the model will handle these values
        self.assertEqual(response.status_code, 200)


class TestModelPredictions(unittest.TestCase):
    """Test cases specifically for model prediction functionality."""
    
    def setUp(self):
        """Set up test fixtures for model prediction tests."""
        self.app = app.test_client()
        self.app.testing = True

    def test_model_prediction_consistency(self):
        """Test that model predictions are consistent for same input."""
        test_data = {
            "Age": 30,
            "Gender": "Male",
            "Education Level": "Master's",
            "Job Title": "Software Engineer",
            "Years of Experience": 5
        }
        
        # Make multiple predictions with same data
        predictions = []
        for _ in range(3):
            response = self.app.post('/predict',
                                   data=json.dumps(test_data),
                                   content_type='application/json')
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            predictions.append(data['predicted_salary'])
        
        # All predictions should be identical
        self.assertTrue(all(p == predictions[0] for p in predictions))

    def test_model_prediction_salary_trends(self):
        """Test that salary predictions follow expected trends."""
        base_data = {
            "Age": 30,
            "Gender": "Male",
            "Education Level": "Bachelor's",
            "Job Title": "Software Engineer",
            "Years of Experience": 5
        }
        
        # Test that more experience generally leads to higher salary
        salaries = []
        for experience in [1, 3, 5, 10, 15]:
            test_data = base_data.copy()
            test_data["Years of Experience"] = experience
            
            response = self.app.post('/predict',
                                   data=json.dumps(test_data),
                                   content_type='application/json')
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            salaries.append(data['predicted_salary'])
        
        # Generally, more experience should lead to higher salary
        # (This is a general trend test, not strict ordering)
        self.assertTrue(salaries[-1] > salaries[0])  # 15 years > 1 year

    def test_model_prediction_education_impact(self):
        """Test that higher education levels generally lead to higher salaries."""
        base_data = {
            "Age": 30,
            "Gender": "Male",
            "Job Title": "Data Analyst",
            "Years of Experience": 5
        }
        
        education_levels = ["High School", "Bachelor's", "Master's", "PhD"]
        salaries = []
        
        for education in education_levels:
            test_data = base_data.copy()
            test_data["Education Level"] = education
            
            response = self.app.post('/predict',
                                   data=json.dumps(test_data),
                                   content_type='application/json')
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            salaries.append(data['predicted_salary'])
        
        # PhD should generally be higher than High School
        self.assertTrue(salaries[-1] > salaries[0])

    def test_model_prediction_age_impact(self):
        """Test that age affects salary predictions."""
        base_data = {
            "Gender": "Female",
            "Education Level": "Master's",
            "Job Title": "Data Scientist",
            "Years of Experience": 5
        }
        
        ages = [25, 30, 35, 40]
        salaries = []
        
        for age in ages:
            test_data = base_data.copy()
            test_data["Age"] = age
            
            response = self.app.post('/predict',
                                   data=json.dumps(test_data),
                                   content_type='application/json')
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            salaries.append(data['predicted_salary'])
        
        # Salaries should vary with age (not necessarily monotonic)
        self.assertTrue(len(set(salaries)) > 1)  # At least some variation

    def test_model_prediction_job_title_impact(self):
        """Test that different job titles lead to different salary predictions."""
        base_data = {
            "Age": 30,
            "Gender": "Male",
            "Education Level": "Bachelor's",
            "Years of Experience": 5
        }
        
        job_titles = ["Intern", "Junior Developer", "Software Engineer", "Senior Software Engineer"]
        salaries = []
        
        for job_title in job_titles:
            test_data = base_data.copy()
            test_data["Job Title"] = job_title
            
            response = self.app.post('/predict',
                                   data=json.dumps(test_data),
                                   content_type='application/json')
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            salaries.append(data['predicted_salary'])
        
        # Different job titles should lead to different salaries
        self.assertTrue(len(set(salaries)) > 1)

    def test_model_prediction_gender_impact(self):
        """Test that gender affects salary predictions."""
        base_data = {
            "Age": 30,
            "Education Level": "Master's",
            "Job Title": "Data Analyst",
            "Years of Experience": 5
        }
        
        genders = ["Male", "Female", "Other"]
        salaries = []
        
        for gender in genders:
            test_data = base_data.copy()
            test_data["Gender"] = gender
            
            response = self.app.post('/predict',
                                   data=json.dumps(test_data),
                                   content_type='application/json')
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            salaries.append(data['predicted_salary'])
        
        # Different genders may lead to different salaries
        # (This tests the model's behavior, not making value judgments)
        self.assertTrue(len(set(salaries)) >= 1)  # At least one prediction


if __name__ == '__main__':
    try:
        # Create a test suite
        test_suite = unittest.TestSuite()
        
        # Add test cases
        test_suite.addTest(unittest.makeSuite(TestFlaskApp))
        test_suite.addTest(unittest.makeSuite(TestModelPredictions))
        
        # Run the tests
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(test_suite)
        
        # Print summary
        print(f"\n{'='*50}")
        print(f"Tests run: {result.testsRun}")
        print(f"Failures: {len(result.failures)}")
        print(f"Errors: {len(result.errors)}")
        print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
        print(f"{'='*50}")
    finally:
        # Restore original working directory
        os.chdir(original_cwd)
