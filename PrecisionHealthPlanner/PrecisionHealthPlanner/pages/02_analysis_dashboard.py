import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from utils.data_processor import DataProcessor

def create_dashboard():
    st.title("Patient Analysis Dashboard")
    
    if not st.session_state.patient_data['personal_info']:
        st.warning("Please input patient data first!")
        return
    
    # Process data
    risk_factors = DataProcessor.process_genetic_data(
        st.session_state.patient_data['genetic_data']
    )
    health_score = DataProcessor.calculate_health_score(
        st.session_state.patient_data
    )
    health_trends = DataProcessor.generate_mock_trends()
    
    # Dashboard layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Patient Overview")
        personal_info = st.session_state.patient_data['personal_info']
        st.write(f"**Name:** {personal_info['name']}")
        st.write(f"**Age:** {personal_info['age']}")
        st.write(f"**Gender:** {personal_info['gender']}")
        
        # Health Score Gauge
        fig_health_score = go.Figure(go.Indicator(
            mode="gauge+number",
            value=health_score,
            title={'text': "Health Score"},
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={'axis': {'range': [0, 100]},
                   'bar': {'color': "#0066cc"},
                   'steps': [
                       {'range': [0, 50], 'color': "lightgray"},
                       {'range': [50, 75], 'color': "gray"},
                       {'range': [75, 100], 'color': "darkgray"}
                   ]}
        ))
        st.plotly_chart(fig_health_score)
    
    with col2:
        st.subheader("Risk Factors")
        # Risk factors radar chart
        fig_risks = go.Figure()
        fig_risks.add_trace(go.Scatterpolar(
            r=list(risk_factors.values()),
            theta=list(risk_factors.keys()),
            fill='toself',
            name='Risk Factors'
        ))
        fig_risks.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
            showlegend=False
        )
        st.plotly_chart(fig_risks)
    
    # Health Metrics Trends
    st.subheader("Health Metrics Trends")
    fig_trends = go.Figure()
    metrics = ['blood_pressure', 'glucose_levels', 'cholesterol']
    for metric in metrics:
        fig_trends.add_trace(go.Scatter(
            x=health_trends['dates'],
            y=health_trends[metric],
            name=metric.replace('_', ' ').title()
        ))
    fig_trends.update_layout(
        xaxis_title="Date",
        yaxis_title="Value",
        hovermode='x unified'
    )
    st.plotly_chart(fig_trends)

if __name__ == "__main__":
    create_dashboard()
