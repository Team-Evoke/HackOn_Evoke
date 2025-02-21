import streamlit as st
import pandas as pd
from utils.notification_service import send_notification #This line is added from the edited code
import base64

st.set_page_config(
    page_title="Medical Treatment Planning System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

def get_base64_encoded_image():
    return """
    <svg width="800" height="400" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" style="stop-color:#0066cc;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#00cc99;stop-opacity:1" />
            </linearGradient>
        </defs>
        <rect width="800" height="400" fill="url(#grad1)" opacity="0.1"/>
        <circle cx="400" cy="200" r="150" stroke="#0066cc" stroke-width="2" fill="none"/>
        <path d="M320 200 h160 M400 120 v160" stroke="#0066cc" stroke-width="8"/>
        <circle cx="400" cy="200" r="80" stroke="#00cc99" stroke-width="2" fill="none"/>
    </svg>
    """

def main():
    # Add custom CSS
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #0066cc;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-card {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        margin: 1rem 0;
    }
    .alert-box {
        padding: 1rem;
        border-radius: 5px;
        background-color: #e7f3fe;
        border-left: 5px solid #0066cc;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

    # Display medical logo/icon
    st.markdown(f"""
        <div style='text-align: center;'>
            {get_base64_encoded_image()}
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<h1 class='main-header'>🏥 Medical Treatment Planning System</h1>", unsafe_allow_html=True)

    # Welcome message in a card
    st.markdown("""
    <div class='feature-card'>
        <h3>Welcome to Your Personalized Healthcare Journey</h3>
        <p>Our advanced system combines genetic analysis, medical history, and lifestyle factors 
        to create customized treatment plans that optimize your health outcomes.</p>
    </div>
    """, unsafe_allow_html=True)

    # Key Features in cards
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class='feature-card'>
            <h4>🧬 Genetic Analysis</h4>
            <ul>
                <li>DNA sequence analysis</li>
                <li>Genetic risk assessment</li>
                <li>Personalized medicine recommendations</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class='feature-card'>
            <h4>📊 Health Analytics</h4>
            <ul>
                <li>Real-time health monitoring</li>
                <li>Trend analysis</li>
                <li>Predictive health insights</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='feature-card'>
            <h4>💊 Treatment Planning</h4>
            <ul>
                <li>Personalized medication schedules</li>
                <li>Lifestyle recommendations</li>
                <li>Treatment effectiveness tracking</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class='feature-card'>
            <h4>📱 Smart Notifications</h4>
            <ul>
                <li>Medication reminders</li>
                <li>Appointment alerts</li>
                <li>Health goal tracking</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # Initialize session state - from original code, integrated into new structure
    if 'patient_data' not in st.session_state:
        st.session_state.patient_data = {
            'personal_info': {},
            'medical_history': {},
            'lifestyle_factors': {},
            'genetic_data': None
        }

    # Navigation guidance
    st.markdown("""
    <div class='alert-box'>
        <h4>Getting Started</h4>
        <p>Use the sidebar navigation to:</p>
        <ol>
            <li>Input your patient data</li>
            <li>View your health analytics dashboard</li>
            <li>Generate personalized treatment plans</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()