class RecommendationEngine:
    @staticmethod
    def generate_recommendations(patient_data, risk_factors):
        """Generate treatment recommendations based on patient data and risk factors."""
        recommendations = {
            'Medications': [],
            'Lifestyle Changes': [],
            'Preventive Measures': []
        }
        
        # Process lifestyle factors
        lifestyle = patient_data.get('lifestyle_factors', {})
        if lifestyle.get('exercise_frequency') == 'Rarely':
            recommendations['Lifestyle Changes'].append(
                "Increase physical activity to at least 150 minutes per week"
            )
        
        if lifestyle.get('smoking_status') == 'Current':
            recommendations['Lifestyle Changes'].append(
                "Quit smoking - consider nicotine replacement therapy"
            )
        
        # Process risk factors
        if risk_factors.get('heart_disease', 0) > 0.5:
            recommendations['Medications'].append(
                "Consider preventive cardiovascular medication"
            )
            recommendations['Preventive Measures'].append(
                "Regular blood pressure monitoring"
            )
        
        if risk_factors.get('diabetes', 0) > 0.5:
            recommendations['Preventive Measures'].append(
                "Regular blood glucose monitoring"
            )
            recommendations['Lifestyle Changes'].append(
                "Follow a low-glycemic diet plan"
            )
        
        return recommendations
