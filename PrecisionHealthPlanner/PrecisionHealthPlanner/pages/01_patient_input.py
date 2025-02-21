import streamlit as st
import pandas as pd
import io

def patient_input_form():
    st.title("Patient Data Input")
    
    with st.form("patient_data_form"):
        st.subheader("Personal Information")
        personal_info = {
            'name': st.text_input("Full Name"),
            'age': st.number_input("Age", min_value=0, max_value=120),
            'gender': st.selectbox("Gender", ['Male', 'Female', 'Other']),
            'height': st.number_input("Height (cm)", min_value=0, max_value=300),
            'weight': st.number_input("Weight (kg)", min_value=0, max_value=500)
        }
        
        st.subheader("Medical History")
        medical_history = {
            'conditions': st.multiselect(
                "Existing Medical Conditions",
                ['Diabetes', 'Hypertension', 'Heart Disease', 'Asthma', 'None']
            ),
            'medications': st.text_area("Current Medications"),
            'allergies': st.text_area("Known Allergies")
        }
        
        st.subheader("Lifestyle Factors")
        lifestyle_factors = {
            'exercise_frequency': st.selectbox(
                "Exercise Frequency",
                ['Regular', 'Occasional', 'Rarely', 'Never']
            ),
            'smoking_status': st.selectbox(
                "Smoking Status",
                ['Never', 'Former', 'Current']
            ),
            'alcohol_consumption': st.selectbox(
                "Alcohol Consumption",
                ['None', 'Occasional', 'Moderate', 'Heavy']
            ),
            'diet_type': st.selectbox(
                "Diet Type",
                ['Balanced', 'Vegetarian', 'Vegan', 'Keto', 'Other']
            )
        }
        
        st.subheader("Genetic Data")
        genetic_file = st.file_uploader("Upload Genetic Data (CSV)", type=['csv'])
        
        if st.form_submit_button("Save Patient Data"):
            if genetic_file is not None:
                genetic_data = pd.read_csv(genetic_file)
            else:
                # Mock genetic data
                genetic_data = pd.DataFrame({
                    'gene': ['BRCA1', 'BRCA2', 'APOE'],
                    'variant': ['wild', 'mutation', 'wild']
                })
            
            st.session_state.patient_data = {
                'personal_info': personal_info,
                'medical_history': medical_history,
                'lifestyle_factors': lifestyle_factors,
                'genetic_data': genetic_data
            }
            
            st.success("Patient data saved successfully!")

if __name__ == "__main__":
    patient_input_form()
