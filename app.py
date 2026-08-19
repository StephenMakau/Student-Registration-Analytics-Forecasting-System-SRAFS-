import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from analytics_engine import CourseAnalytics

# Page Configuration
st.set_page_config(
    page_title="Course Registration Intelligence",
    page_icon="📊",
    layout="wide"
)

st.title("🎓 Course Registration & Performance Intelligence")
st.mark("""
    **Management Dashboard**: Upload historical registration data to analyze course performance, 
    identify seasonal trends, and predict future enrollment numbers.
""")

# Initialize Session State
if 'analytics' not in st.session_state:
    st.session_state.analytics = CourseAnalytics()
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'model_trained' not in st.session_state:
    st.session_state.model_trained = False

# Sidebar for Data Upload
with st.sidebar:
    st.header("Data Configuration")
    uploaded_file = st.file_uploader("Upload Dataset (CSV)", type=['csv'])
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            # Validate columns
            required_columns = ['date', 'course_name', 'registered_count']
            if not all(col in df.columns for col in required_columns):
                st.error(f"Missing columns. Required: {required_columns}")
                st.stop()
            
            st.session_state.data_loaded = True
            st.success("Data loaded successfully!")
            st.info(f"Records found: {len(df)}")
            
            # Show sample
            st.write("### Data Preview")
            st.dataframe(df.head())
            
        except Exception as e:
            st.error(f"Error loading file: {e}")
            st.stop()
    else:
        st.info("Please upload a CSV file to begin.")
        st.stop()

if not st.session_state.data_loaded:
    st.stop()

# Main Dashboard Tabs
tab1, tab2, tab3 = st.tabs(["📈 Performance Overview", "🔮 Predictive Analytics", "📉 Detailed Reports"])

with tab1:
    st.header("Historical Performance Analysis")
    
    if st.button("Generate Performance Report", type="primary"):
        try:
            # Get analytics
            results = st.session_state.analytics.get_performance_overview(df)
            
            # 1. Top/Bottom Courses
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("🏆 Top Performing Courses (Total)")
                top_courses = results['course_performance'].head(5)
                st.bar_chart(top_courses['Total Registrations'], color="#28a745")
            
            with col2:
                st.subheader("📉 Underperforming Courses (Total)")
                bottom_courses = results['course_performance'].tail(5)
                st.bar_chart(bottom_courses['Total Registrations'], color="#dc3545")

            # 2. Seasonal Trends
            st.subheader("📅 Seasonal & Monthly Trends")
            fig_monthly = px.line(
                x=results['monthly_trends'].index, 
                y=results['monthly_trends'].values,
                labels={'x': 'Month', 'y': 'Total Registrations'},
                title="Registration Volume by Month (All Courses)"
            )
            st.plotly_chart(fig_monthly, use_container_width=True)
            
            st.warning("Insight: Use the 'Detailed Reports' tab to see which specific courses drive these seasonal spikes.")

        except Exception as e:
            st.error(f"Analysis failed: {e}")

with tab2:
    st.header("AI Prediction Engine")
    st.markdown("Train a model on the last 3 years of data to forecast future registration numbers.")
    
    if st.button("Train Prediction Model"):
        with st.spinner("Training Random Forest Regressor... This may take a moment."):
            try:
                mae = st.session_state.analytics.train_prediction_model(df)
                st.session_state.model_trained = True
                st.success(f"Model trained successfully! (Mean Absolute Error: {mae:.2f})")
                st.info("Model is ready for predictions in the section below.")
            except Exception as e:
                st.error(f"Training failed: {e}")
    
    if st.session_state.model_trained:
        st.divider()
        st.subheader("Generate Future Forecast")
        
        # Simple interface to generate future scenarios
        st.write("Enter parameters to simulate future performance:")
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            courses = df['course_name'].unique()
            selected_course = st.selectbox("Select Course", courses)
        with col_b:
            year = st.number_input("Year", min_value=2024, max_value=2030, value=2025)
        with col_c:
            month = st.slider("Month", 1, 12, 1)
            
        if st.button("Predict Registration"):
            try:
                future_config = [
                    {'course_name': selected_course, 'year': year, 'month': month}
                ]
                pred_df = st.session_state.analytics.predict_future(future_config)
                
                st.metric(
                    label=f"Predicted Registrations for {selected_course}",
                    value=f"{pred_df['predicted_registrations'].iloc[0]:.0f}"
                )
                st.caption("Note: Predictions are based on historical patterns. Actual results may vary due to market changes.")
            except Exception as e:
                st.error(f"Prediction failed: {e}")

with tab3:
    st.header("Detailed Management Reports")
    
    if st.button("Generate Detailed Matrices"):
        results = st.session_state.analytics.get_performance_overview(df)
        
        st.subheader("Course Performance by Quarter")
        st.write("Heatmap showing registration intensity. Darker colors indicate higher volume.")
        
        # Heatmap
        fig_heatmap = px.imshow(
            results['course_quarter_matrix'],
            labels={'x': 'Quarter', 'y': 'Course', 'color': 'Registrations'},
            color_continuous_scale="Reds",
            title="Registration Volume: Course vs Quarter"
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
        
        st.subheader("Raw Data Tables")
        st.write("### Course Performance Summary")
        st.dataframe(results['course_performance'])
        
        st.write("### Quarterly Aggregates")
        st.dataframe(results['quarterly_performance'])

# Footer
st.markdown("---")
st.markdown("Generated by Course Intelligence System | Powered by Python & Streamlit")
