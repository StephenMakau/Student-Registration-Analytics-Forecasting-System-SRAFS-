import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
import warnings
warnings.filterwarnings('ignore')

# -----------------------------------------------------------------------------
# DEFAULT DATASET GENERATOR (Based on your PDF structure)
# -----------------------------------------------------------------------------

def create_default_dataset():
    courses = [
        'ICDL', 'GRE', 'CATIA', 'CCNA', 'AWS', 'C#', 'GDP', 'CYBER',
        'CISA', 'ACDL', 'AZURE', 'CSM', 'CASP', 'CKAD', 'COMPTIA A+',
        'DIGITAL ACADEMY', 'ANDROID', 'DATA PROTECTION', 'CIVIL', 'CISP',
        'CISM', 'CISSP', 'CCNP', 'CCSP', 'AZ-900E', 'FORTINET NSE 7',
        'COMPTIA N+', 'COMPTIA S+', 'CRISC', 'DATA+', 'IELTS EXAM', 'GMAT'
    ]
    
    sample_data = []
    
    for year in [2023, 2024, 2025]:
        for month in range(1, 13):
            for course in courses:
                if course in ['ICDL', 'GRE', 'CATIA', 'CCNA']:
                    base = np.random.randint(20, 80)
                elif course in ['AWS', 'C#', 'CYBER', 'CISA', 'AZURE']:
                    base = np.random.randint(10, 50)
                elif course in ['GDP', 'ACDL', 'CSM', 'CASP']:
                    base = np.random.randint(5, 30)
                else:
                    base = np.random.randint(1, 15)
                
                if month in [1, 2, 9, 10]:
                    multiplier = np.random.uniform(1.3, 2.0)
                elif month in [6, 7, 12]:
                    multiplier = np.random.uniform(0.2, 0.6)
                else:
                    multiplier = np.random.uniform(0.8, 1.2)
                
                noise = np.random.uniform(0.7, 1.3)
                count = int(base * multiplier * noise)
                count = max(0, count)
                
                sample_data.append({
                    'date': f"{year}-{month:02d}-15",
                    'course_name': course,
                    'registered_count': count
                })
    
    return pd.DataFrame(sample_data)

# -----------------------------------------------------------------------------
# ANALYTICS ENGINE
# -----------------------------------------------------------------------------

class VisualAnalytics:
    def __init__(self):
        self.default_data = None

    def load_default_data(self):
        if self.default_data is None:
            self.default_data = create_default_dataset()
        return self.default_data.copy()

    def preprocess_data(self, df):
        data = df.copy()
        data['date'] = pd.to_datetime(data['date'])
        data['year'] = data['date'].dt.year
        data['month'] = data['date'].dt.month
        data['month_name'] = data['date'].dt.strftime('%b')
        data['quarter'] = data['date'].dt.quarter
        return data

    def get_course_performance_by_month(self, df, month, year=None):
        """Get course performance for a specific month, optionally filtered by year"""
        data = self.preprocess_data(df)
        month_data = data[data['month'] == month]
        
        if year is not None:
            month_data = month_data[month_data['year'] == year]
        
        if month_data.empty:
            return None
        
        perf = month_data.groupby('course_name')['registered_count'].sum().reset_index()
        perf.columns = ['course_name', 'registrations']
        perf = perf.sort_values('registrations', ascending=False)
        return perf

    def forecast_next_year_month(self, df, target_month):
        """Forecast based on historical averages with growth factor"""
        data = self.preprocess_data(df)
        
        forecasts = []
        courses = data['course_name'].unique()
        
        for course in courses:
            course_data = data[data['course_name'] == course]
            historical = course_data[course_data['date'].dt.month == target_month]
            
            if len(historical) > 0:
                # Calculate average and apply a conservative growth factor
                avg = historical['registered_count'].mean()
                forecast_val = avg * 1.15  # 15% growth assumption
            else:
                # If no history for this month, use 0
                forecast_val = 0
            
            forecasts.append({
                'course': course,
                'forecasted_registrations': max(0, round(forecast_val))
            })
        
        return pd.DataFrame(forecasts)

# -----------------------------------------------------------------------------
# STREAMLIT APP (VISUAL FIRST)
# -----------------------------------------------------------------------------

st.set_page_config(
    page_title="Course Registration Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Minimal CSS for clean visual layout
st.markdown("""
<style>
    .main {
        background-color: #f0f2f6;
    }
    .stApp {
        background-color: #f0f2f6;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .stButton>button {
        background-color: #0068c9;
        color: white;
        border-radius: 5px;
        border: none;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #0056a3;
    }
</style>
""", unsafe_allow_html=True)

# Initialize
analytics = VisualAnalytics()

# Load Data
if 'df' not in st.session_state:
    st.session_state.df = analytics.load_default_data()

df = st.session_state.df

# -----------------------------------------------------------------------------
# MAIN VISUAL DASHBOARD
# -----------------------------------------------------------------------------

# Header
st.title("📊 Course Registration Intelligence")
st.markdown("**Visual Analytics Dashboard** - Select a month to analyze performance and forecast future intake.")

st.divider()

# Month Selection
month_options = {
    1: "January", 2: "February", 3: "March", 4: "April",
    5: "May", 6: "June", 7: "July", 8: "August",
    9: "September", 10: "October", 11: "November", 12: "December"
}

col_select, col_stats = st.columns([1, 3])

with col_select:
    selected_month = st.selectbox(
        "Select Month for Analysis",
        options=list(month_options.keys()),
        format_func=lambda x: f"{month_options[x]} ({x})"
    )

# Calculate stats for selected month
current_data = df[pd.to_datetime(df['date']).dt.month == selected_month]
total_regs = current_data['registered_count'].sum() if len(current_data) > 0 else 0
active_courses = current_data['course_name'].nunique() if len(current_data) > 0 else 0

with col_stats:
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Registrations (Historical)", f"{total_regs:,}")
    c2.metric("Active Courses", active_courses)
    c3.metric("Data Years Available", "3 Years")

st.divider()

# -----------------------------------------------------------------------------
# VISUALIZATION TABS
# -----------------------------------------------------------------------------

tab1, tab2 = st.tabs(["📈 Monthly Performance Analysis", "🔮 AI Forecast & Planning"])

with tab1:
    if total_regs == 0:
        st.warning("No data available for this month.")
    else:
        st.info("The following section provides a year-by-year breakdown of course performance for the selected month, followed by a combined historical analysis.")
        
        # Define the years to analyze
        years_to_analyze = [2023, 2024, 2025]
        valid_year_data = {}
        
        # Check which years have data for the selected month
        for year in years_to_analyze:
            temp_data = df[pd.to_datetime(df['date']).dt.year == year]
            if not temp_data[temp_data['date'].dt.month == selected_month].empty:
                valid_year_data[year] = True
        
        valid_years = list(valid_year_data.keys())
        
        if not valid_years:
            st.error("No valid data found for any year for the selected month.")
        else:
            # Generate Year-by-Year Breakdown
            for year in valid_years:
                st.subheader(f"📊 {year} Performance Breakdown for {month_options[selected_month]}")
                
                perf_data_year = analytics.get_course_performance_by_month(df, selected_month, year=year)
                
                if perf_data_year is not None and len(perf_data_year) > 0:
                    col_year1, col_year2 = st.columns(2)
                    
                    with col_year1:
                        st.markdown(f"#### Top Performing Courses in {year}")
                        top_courses_year = perf_data_year.head(10)  # Show top 10 for yearly breakdown
                        if len(top_courses_year) > 0:
                            fig_top_year = px.bar(
                                top_courses_year,
                                x='registrations',
                                y='course_name',
                                orientation='h',
                                title={`Top 10 Courses - {month_options[selected_month]} {year}`},
                                color='registrations',
                                color_continuous_scale='greens'
                            )
                            fig_top_year.update_layout(
                                height=400,
                                xaxis_title="Number of Registrations",
                                yaxis_title="Course Name",
                                showlegend=False
                            )
                            st.plotly_chart(fig_top_year, use_container_width=True)
                        else:
                            st.write("No top performing courses data available.")
                    
                    with col_year2:
                        st.markdown(f"#### Lowest Performing Courses in {year}")
                        bottom_courses_year = perf_data_year.tail(10)
                        if len(bottom_courses_year) > 0:
                            fig_bottom_year = px.bar(
                                bottom_courses_year,
                                x='registrations',
                                y='course_name',
                                orientation='h',
                                title=f"Lowest 10 Courses - {month_options[selected_month]} {year}",
                                color='registrations',
                                color_continuous_scale='reds'
                            )
                            fig_bottom_year.update_layout(
                                height=400,
                                xaxis_title="Number of Registrations",
                                yaxis_title="Course Name",
                                showlegend=False
                            )
                            st.plotly_chart(fig_bottom_year, use_container_width=True)
                        else:
                            st.write("No lowest performing courses data available.")
                    
                    st.markdown("---")  # Separator between years
                else:
                    st.warning(f"No data available for {year}.")
            
            # Combined Historical Analysis
            st.subheader(f"📈 Combined Historical Analysis for {month_options[selected_month]} (All Years)")
            st.markdown("This graph aggregates data from all available years to show overall course performance trends.")
            
            perf_data_combined = analytics.get_course_performance_by_month(df, selected_month)
            
            if perf_data_combined is not None and len(perf_data_combined) > 0:
                # VISUAL 1: Top Courses Bar Chart (Combined)
                st.subheader(f"Top Performing Courses in {month_options[selected_month]} (Combined Data)")
                
                top_courses = perf_data_combined.head(15)  # Show top 15
                fig_top = px.bar(
                    top_courses,
                    x='registrations',
                    y='course_name',
                    orientation='h',
                    title=f"Highest Registration Volume - {month_options[selected_month]} (Historical Average)",
                    color='registrations',
                    color_continuous_scale='greens'
                )
                fig_top.update_layout(
                    height=600,
                    xaxis_title="Number of Registrations",
                    yaxis_title="Course Name",
                    showlegend=False
                )
                st.plotly_chart(fig_top, use_container_width=True)
                
                # VISUAL 2: Bottom Courses (Combined)
                st.subheader(f"Lowest Performing Courses in {month_options[selected_month]} (Combined Data)")
                
                bottom_courses = perf_data_combined.tail(15)
                if len(bottom_courses) > 0:
                    fig_bottom = px.bar(
                        bottom_courses,
                        x='registrations',
                        y='course_name',
                        orientation='h',
                        title=f"Lowest Registration Volume - {month_options[selected_month]} (Requires Marketing Intervention)",
                        color='registrations',
                        color_continuous_scale='reds'
                    )
                    fig_bottom.update_layout(
                        height=400,
                        xaxis_title="Number of Registrations",
                        yaxis_title="Course Name",
                        showlegend=False
                    )
                    st.plotly_chart(fig_bottom, use_container_width=True)
                
                # VISUAL 3: Full Data Table (Combined)
                st.subheader("Complete Course Performance Data (Combined)")
                st.dataframe(perf_data_combined, use_container_width=True, hide_index=True)
            else:
                st.error("No combined data available.")

with tab2:
    st.subheader(f"🔮 Forecast for {month_options[selected_month]} {datetime.datetime.now().year + 1}")
    st.markdown("AI-powered prediction of registration numbers for next year's intake based on historical trends.")
    
    if st.button("Generate Forecast Visualization", type="primary"):
        with st.spinner("Processing historical data and generating forecasts..."):
            forecast_df = analytics.forecast_next_year_month(df, selected_month)
            
            if forecast_df is not None and len(forecast_df) > 0:
                # Sort forecast
                forecast_df = forecast_df.sort_values('forecasted_registrations', ascending=False)
                
                # VISUAL 4: Forecast Bar Chart
                st.subheader(f"Predicted Registration Volume - {month_options[selected_month]} {datetime.datetime.now().year + 1}")
                
                fig_forecast = px.bar(
                    forecast_df,
                    x='forecasted_registrations',
                    y='course',
                    orientation='h',
                    title=f"Forecasted Demand - {month_options[selected_month]} {datetime.datetime.now().year + 1}",
                    color='forecasted_registrations',
                    color_continuous_scale='blues'
                )
                fig_forecast.update_layout(
                    height=600,
                    xaxis_title="Predicted Registrations",
                    yaxis_title="Course Name",
                    showlegend=False
                )
                st.plotly_chart(fig_forecast, use_container_width=True)
                
                # VISUAL 5: Strategic Focus Areas
                st.subheader("🎯 Strategic Marketing Focus Areas")
                
                # Calculate top 5 for focus
                top_5 = forecast_df.head(5)
                if len(top_5) > 0:
                    fig_focus = px.pie(
                        top_5,
                        values='forecasted_registrations',
                        names='course',
                        title=f"Top 5 Courses to Prioritize for {month_options[selected_month]} {datetime.datetime.now().year + 1} (Total Predicted: {top_5['forecasted_registrations'].sum()})"
                    )
                    fig_focus.update_layout(height=400)
                    st.plotly_chart(fig_focus, use_container_width=True)
                
                # Download forecast
                csv = forecast_df.to_csv(index=False)
                st.download_button(
                    "📥 Download Full Forecast Data (CSV)",
                    csv,
                    f"forecast_{month_options[selected_month]}_{datetime.datetime.now().year + 1}.csv",
                    "text/csv"
                )
            else:
                st.error("Could not generate forecast. Insufficient historical data.")

# -----------------------------------------------------------------------------
# FOOTER
# -----------------------------------------------------------------------------
st.divider()
st.markdown("Course Registration Intelligence System | Data-Driven Marketing Analytics")
