import pandas as pd
import numpy as np

class DataProcessor:
    @staticmethod
    def process_genetic_data(genetic_data):
        """Process mock genetic data and return risk factors."""
        # Mock genetic analysis
        risk_factors = {
            'heart_disease': np.random.uniform(0, 1),
            'diabetes': np.random.uniform(0, 1),
            'cancer': np.random.uniform(0, 1),
            'alzheimers': np.random.uniform(0, 1)
        }
        return risk_factors
    
    @staticmethod
    def calculate_health_score(patient_data):
        """Calculate overall health score based on various factors."""
        base_score = 70  # Base health score
        
        # Adjust score based on lifestyle factors
        lifestyle = patient_data.get('lifestyle_factors', {})
        if lifestyle.get('exercise_frequency') == 'Regular':
            base_score += 10
        if lifestyle.get('smoking_status') == 'Never':
            base_score += 10
        
        # Cap score at 100
        return min(base_score, 100)
    
    @staticmethod
    def generate_mock_trends():
        """Generate mock health metric trends."""
        dates = pd.date_range(start='2023-01-01', periods=12, freq='M')
        return {
            'blood_pressure': [np.random.randint(110, 140) for _ in range(12)],
            'glucose_levels': [np.random.randint(80, 120) for _ in range(12)],
            'cholesterol': [np.random.randint(150, 200) for _ in range(12)],
            'dates': dates.strftime('%Y-%m-%d').tolist()
        }
