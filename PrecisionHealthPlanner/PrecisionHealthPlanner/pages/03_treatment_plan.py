import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from utils.recommendation_engine import RecommendationEngine
from utils.data_processor import DataProcessor
from utils.pdf_generator import PDFGenerator
from utils.notification_service import notification_service
from datetime import datetime, timedelta

def create_schedule_timeline(recommendations):
    """Create a timeline visualization for treatment schedule"""
    activities = []
    start_dates = []
    end_dates = []
    colors = []

    base_date = datetime.now()
    for category, items in recommendations.items():
        for i, item in enumerate(items):
            activities.append(f"{category}: {item}")
            start = base_date + timedelta(days=i*7)
            end = start + timedelta(days=28)
            start_dates.append(start.strftime('%Y-%m-%d'))
            end_dates.append(end.strftime('%Y-%m-%d'))
            colors.append('#0066cc' if category == 'Medications' else 
                         '#00cc99' if category == 'Lifestyle Changes' else '#ff9900')

    fig = go.Figure()

    for i in range(len(activities)):
        fig.add_trace(go.Bar(
            name=activities[i],
            x=[28],  # Duration in days
            y=[activities[i]],
            orientation='h',
            marker_color=colors[i],
            text=f"{start_dates[i]} to {end_dates[i]}",
            hovertext=f"{activities[i]}<br>{start_dates[i]} to {end_dates[i]}"
        ))

    fig.update_layout(
        title="Treatment Schedule Timeline",
        xaxis_title="Duration (days)",
        showlegend=False,
        height=400,
        margin=dict(l=10, r=10, t=30, b=10)
    )

    return fig

def generate_treatment_plan():
    st.title("Advanced Treatment Plan Generator")

    if 'patient_data' not in st.session_state or not st.session_state.patient_data.get('personal_info'):
        st.warning("Please input patient data first!")
        st.markdown("Go to the **Patient Input** page to enter patient information.")
        return

    try:
        # Process data and generate recommendations
        risk_factors = DataProcessor.process_genetic_data(
            st.session_state.patient_data.get('genetic_data', pd.DataFrame())
        )
        recommendations = RecommendationEngine.generate_recommendations(
            st.session_state.patient_data,
            risk_factors
        )

        # Display personalized header
        patient_name = st.session_state.patient_data['personal_info'].get('name', 'Patient')
        st.markdown(f"""
        <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px;'>
            <h2 style='color: #0066cc;'>Personalized Treatment Plan for {patient_name}</h2>
            <p>Based on your genetic profile, medical history, and lifestyle factors.</p>
        </div>
        """, unsafe_allow_html=True)

        try:
            # Display timeline
            timeline = create_schedule_timeline(recommendations)
            st.plotly_chart(timeline, use_container_width=True)
        except Exception as e:
            st.error(f"Could not create timeline visualization. Error: {str(e)}")

        # Display detailed recommendations
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🏥 Treatment Recommendations")
            for category, items in recommendations.items():
                with st.expander(f"{category} Details"):
                    for item in items:
                        st.markdown(f"- {item}")

                    # Add compliance tracking
                    if category == "Medications":
                        for item in items:
                            st.checkbox(f"Track {item}", key=f"med_track_{item}")

        with col2:
            st.subheader("📊 Health Metrics to Monitor")
            metrics = {
                "Blood Pressure": "Daily",
                "Blood Glucose": "Twice daily",
                "Weight": "Weekly",
                "Exercise Duration": "Daily"
            }
            for metric, frequency in metrics.items():
                st.markdown(f"**{metric}** - Monitor {frequency}")

        # Treatment Schedule
        st.subheader("📅 Treatment Schedule")
        schedule_col1, schedule_col2 = st.columns(2)

        with schedule_col1:
            st.markdown("### Morning Routine")
            st.markdown("""
            - 08:00 AM - Morning medications
            - 08:30 AM - Blood pressure check
            - 09:00 AM - Light exercise
            """)

        with schedule_col2:
            st.markdown("### Evening Routine")
            st.markdown("""
            - 06:00 PM - Evening medications
            - 06:30 PM - Blood pressure check
            - 07:00 PM - Evening walk
            """)

        # Notification Settings
        st.subheader("🔔 Notification Preferences")
        enable_notifications = st.toggle("Enable treatment reminders")

        if enable_notifications:
            phone_number = st.text_input("Phone number for reminders", 
                                       value=st.session_state.patient_data['personal_info'].get('phone', ''))
            reminder_frequency = st.select_slider(
                "Reminder Frequency",
                options=["Daily", "Every 2 days", "Weekly"]
            )

            if st.button("Set Up Reminders"):
                if phone_number:
                    st.session_state.patient_data['personal_info']['phone'] = phone_number
                    notification_service.schedule_reminder(
                        st.session_state.patient_data,
                        'medication',
                        f"Schedule: {reminder_frequency}"
                    )
                    st.success("Reminders set up successfully!")
                else:
                    st.error("Please enter a valid phone number")

        # Generate PDF report
        if st.button("Generate Detailed PDF Report"):
            try:
                pdf_buffer = PDFGenerator.generate_treatment_plan_pdf(
                    st.session_state.patient_data,
                    recommendations
                )

                st.download_button(
                    label="Download Treatment Plan PDF",
                    data=pdf_buffer,
                    file_name=f"treatment_plan_{datetime.now().strftime('%Y%m%d')}.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Could not generate PDF report. Error: {str(e)}")

    except Exception as e:
        st.error(f"An error occurred while generating the treatment plan: {str(e)}")
        st.info("Please ensure all required patient information is entered correctly.")

if __name__ == "__main__":
    generate_treatment_plan()