import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error
import datetime

# -----------------------------------------------------------------------------
# MARKETING INTELLIGENCE SYSTEM
# Purpose: Help marketing team know WHEN to promote WHICH courses
# -----------------------------------------------------------------------------

st.set_page_config(
    page_title="Course Marketing Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for marketing-friendly styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f4e79;
    }
    .insight-box {
        background-color: #f0f7ff;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1f4e79;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .recommendation {
        background-color: #e8f5e9;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #4caf50;
        margin: 10px 0;
    }
    .warning-box {
        background-color: #fff3e0;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #ff9800;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# DATA PROCESSING ENGINE
# -----------------------------------------------------------------------------

class MarketingAnalytics:
    def __init__(self):
        self.model = None
        self.label_encoders = {}
        self.is_trained = False
        self.course_insights = {}

    def load_and_process(self, df):
        """Process raw registration data into marketing-friendly format"""
        data = df.copy()
        data['date'] = pd.to_datetime(data['date'])
        data['year'] = data['date'].dt.year
        data['month'] = data['date'].dt.month
        data['month_name'] = data['date'].dt.strftime('%b')
        data['quarter'] = data['date'].dt.quarter
        data['quarter_label'] = 'Q' + data['quarter'].astype(str)
        
        # Marketing-relevant features
        data['is_peak_season'] = data['month'].isin([1, 2, 9, 10])  # Common peak months
        data['is_low_season'] = data['month'].isin([6, 7, 12])  # Common low months
        
        return data

    def generate_marketing_insights(self, df):
        """Generate actionable insights for marketing team"""
        data = self.load_and_process(df)
        
        insights = {
            'monthly_performance': {},
            'course_seasonality': {},
            'quarterly_trends': {},
            'marketing_recommendations': []
        }
        
        # Monthly aggregation for all courses
        monthly = data.groupby(['month', 'month_name'])['registered_count'].sum().reset_index()
        insights['monthly_totals'] = monthly
        
        # Per-course analysis
        for course in data['course_name'].unique():
            course_data = data[data['course_name'] == course]
            
            # Best and worst months
            monthly_perf = course_data.groupby('month_name')['registered_count'].sum()
            best_month = monthly_perf.idxmax() if not monthly_perf.empty else 'N/A'
            worst_month = monthly_perf.idxmin() if not monthly_perf.empty else 'N/A'
            peak_value = monthly_perf.max() if not monthly_perf.empty else 0
            low_value = monthly_perf.min() if not monthly_perf.empty else 0
            
            # Seasonality score (coefficient of variation)
            mean_reg = course_data['registered_count'].mean()
            std_reg = course_data['registered_count'].std()
            seasonality_score = (std_reg / mean_reg) if mean_reg > 0 else 0
            
            # Categorize course type
            if seasonality_score < 0.5:
                course_type = "Stable Year-Round"
                marketing_strategy = "Maintain consistent presence. Good for steady revenue."
            elif seasonality_score < 1.0:
                course_type = "Moderately Seasonal"
                marketing_strategy = "Increase budget 2 months before peak months."
            else:
                course_type = "Highly Seasonal"
                marketing_strategy = "Concentrate 70% of budget in peak months only."
            
            insights['course_seasonality'][course] = {
                'best_month': best_month,
                'worst_month': worst_month,
                'peak_value': peak_value,
                'low_value': low_value,
                'seasonality_score': seasonality_score,
                'course_type': course_type,
                'marketing_strategy': marketing_strategy,
                'monthly_data': monthly_perf.to_dict()
            }
        
        # Quarterly trends
        quarterly = data.groupby(['year', 'quarter'])['registered_count'].sum().reset_index()
        insights['quarterly_trends'] = quarterly
        
        return insights, data

    def train_forecast_model(self, df):
        """Train model to predict next year's monthly registrations per course"""
        data = self.load_and_process(df)
        
        # Prepare features
        le = LabelEncoder()
        data['course_encoded'] = le.fit_transform(data['course_name'])
        self.label_encoders['course'] = le
        
        features = ['month', 'quarter', 'course_encoded', 'year']
        X = data[features]
        y = data['registered_count']
        
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model.fit(X, y)
        self.is_trained = True
        
        # Feature importance for marketing insight
        importance = pd.DataFrame({
            'feature': features,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        return mean_absolute_error(y, self.model.predict(X)), importance

    def predict_next_year(self, courses, year=2026):
        """Generate monthly predictions for marketing planning"""
        if not self.is_trained:
            return None
            
        predictions = []
        for course in courses:
            try:
                course_code = self.label_encoders['course'].transform([course])[0]
                for month in range(1, 13):
                    input_data = pd.DataFrame({
                        'month': [month],
                        'quarter': [(month-1)//3 + 1],
                        'course_encoded': [course_code],
                        'year': [year]
                    })
                    pred = self.model.predict(input_data)[0]
                    predictions.append({
                        'course': course,
                        'year': year,
                        'month': month,
                        'month_name': datetime.date(2024, month, 1).strftime('%b'),
                        'predicted_registrations': max(0, round(pred))
                    })
            except:
                continue
                
        return pd.DataFrame(predictions)

# -----------------------------------------------------------------------------
# STREAMLIT MARKETING DASHBOARD
# -----------------------------------------------------------------------------

st.markdown('<p class="main-header">📊 Course Marketing Intelligence Dashboard</p>', unsafe_allow_html=True)
st.markdown("""
**Purpose**: Identify optimal timing for course marketing campaigns based on historical registration patterns.
""")

# Initialize
if 'analytics' not in st.session_state:
    st.session_state.analytics = MarketingAnalytics()
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'current_year' not in st.session_state:
    st.session_state.current_year = 2023

# -----------------------------------------------------------------------------
# SIDEBAR: Data Upload & Year Selection
# -----------------------------------------------------------------------------

with st.sidebar:
    st.header("📁 Data Management")
    
    # Year selector for multi-year view
    st.subheader("Select Year to View")
    year_options = [2023, 2024, 2025, 2026]
    selected_year = st.selectbox("Year", year_options, index=0)
    st.session_state.current_year = selected_year
    
    st.divider()
    
    # File upload
    st.subheader("Upload Registration Data")
    st.markdown("""
    **Required CSV Format:**
    - `date` (YYYY-MM-DD)
    - `course_name` 
    - `registered_count`
    """)
    
    uploaded_file = st.file_uploader("Choose CSV file", type="csv")
    
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            required = ['date', 'course_name', 'registered_count']
            if all(col in df.columns for col in required):
                st.session_state.data_loaded = True
                st.session_state.df = df
                st.success(f"✅ Loaded {len(df)} records")
            else:
                st.error(f"Missing columns: {set(required) - set(df.columns)}")
        except Exception as e:
            st.error(f"Error: {e}")
    
    # Sample data generator
    st.divider()
    if st.button("📥 Generate Sample Data"):
        # Create realistic sample based on the PDF structure
        courses = [
            'ICDL', 'GRE', 'CATIA', 'CCNA', 'AWS', 'C#', 'GDP', 'CYBER',
            'CISA', 'ACDL', 'AZURE', 'CSM', 'CASP', 'CKAD', 'COMPTIA A+',
            'DIGITAL ACADEMY', 'ANDROID', 'DATA PROTECTION', 'CIVIL'
        ]
        
        sample_data = []
        start_date = datetime.date(2023, 1, 1)
        
        for year in [2023, 2024, 2025]:
            for month in range(1, 13):
                for course in courses:
                    # Simulate realistic patterns
                    base = np.random.randint(5, 50)
                    
                    # Seasonal adjustments
                    if month in [1, 2, 9, 10]:  # Peak months
                        multiplier = 1.5
                    elif month in [6, 7, 12]:  # Low months
                        multiplier = 0.5
                    else:
                        multiplier = 1.0
                    
                    # Course-specific popularity
                    if course in ['ICDL', 'GRE', 'CATIA', 'CCNA']:
                        popularity = 2.0
                    elif course in ['AWS', 'C#', 'CYBER']:
                        popularity = 1.5
                    else:
                        popularity = 1.0
                    
                    count = int(base * multiplier * popularity * np.random.uniform(0.7, 1.3))
                    
                    sample_data.append({
                        'date': f"{year}-{month:02d}-15",
                        'course_name': course,
                        'registered_count': max(0, count)
                    })
        
        sample_df = pd.DataFrame(sample_data)
        csv = sample_df.to_csv(index=False)
        st.download_button("Download Sample CSV", csv, "sample_data.csv", "text/csv")

if not st.session_state.data_loaded:
    st.info("👆 Please upload your data or generate sample data to begin.")
    st.stop()

# -----------------------------------------------------------------------------
# MAIN DASHBOARD: YEAR-SPECIFIC VIEW
# -----------------------------------------------------------------------------

df = st.session_state.df
analytics = st.session_state.analytics

# Filter data for selected year
df['date'] = pd.to_datetime(df['date'])
df_year = df[df['date'].dt.year == selected_year]

if len(df_year) == 0:
    st.warning(f"No data found for year {selected_year}. Showing all available data.")
    df_year = df

# Generate insights
insights, processed_data = analytics.generate_marketing_insights(df_year)

# -----------------------------------------------------------------------------
# MARKETING SUMMARY CARDS
# -----------------------------------------------------------------------------

st.markdown(f"## 📅 Year {selected_year} Marketing Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    total_courses = len(df_year['course_name'].unique())
    st.metric("Active Courses", total_courses)

with col2:
    total_regs = df_year['registered_count'].sum()
    st.metric("Total Registrations", f"{total_regs:,}")

with col3:
    peak_month = insights['monthly_totals'].loc[insights['monthly_totals']['registered_count'].idxmax(), 'month_name']
    st.metric("Peak Month", peak_month)

with col4:
    avg_per_course = df_year.groupby('course_name')['registered_count'].sum().mean()
    st.metric("Avg per Course", f"{avg_per_course:.0f}")

st.divider()

# -----------------------------------------------------------------------------
# TAB 1: MONTHLY PERFORMANCE VIEW
# -----------------------------------------------------------------------------

tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Monthly Trends", 
    "🎯 Course Seasonality", 
    "🔮 Forecast & Planning",
    "📋 Marketing Recommendations"
])

with tab1:
    st.header(f"Monthly Registration Trends - {selected_year}")
    
    # Monthly bar chart
    monthly_data = insights['monthly_totals']
    
    fig_monthly = px.bar(
        monthly_data,
        x='month_name',
        y='registered_count',
        title=f"Total Registrations by Month ({selected_year})",
        labels={'month_name': 'Month', 'registered_count': 'Registrations'},
        color='registered_count',
        color_continuous_scale='Blues'
    )
    fig_monthly.update_layout(height=400)
    st.plotly_chart(fig_monthly, use_container_width=True)
    
    # Marketing insight
    best_month = monthly_data.loc[monthly_data['registered_count'].idxmax(), 'month_name']
    worst_month = monthly_data.loc[monthly_data['registered_count'].idxmin(), 'month_name']
    
    st.markdown(f"""
    <div class="insight-box">
        <h4>💡 Marketing Insight</h4>
        <p><strong>{best_month}</strong> is your strongest month. Consider launching major campaigns in 
        <strong>{worst_month}</strong> to boost low-performing periods.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Monthly breakdown table
    st.subheader("Monthly Registration Details")
    st.dataframe(monthly_data.sort_values('month'), use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 2: COURSE SEASONALITY ANALYSIS
# -----------------------------------------------------------------------------

with tab2:
    st.header("Course Performance by Seasonality")
    
    # Course selector
    all_courses = list(insights['course_seasonality'].keys())
    selected_courses = st.multiselect(
        "Select courses to analyze",
        all_courses,
        default=all_courses[:5] if len(all_courses) > 5 else all_courses
    )
    
    if selected_courses:
        # Create comparison chart
        fig = go.Figure()
        
        for course in selected_courses:
            course_info = insights['course_seasonality'][course]
            monthly_dict = course_info['monthly_data']
            
            months_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            values = [monthly_dict.get(m, 0) for m in months_order]
            
            fig.add_trace(go.Scatter(
                x=months_order,
                y=values,
                mode='lines+markers',
                name=course,
                line=dict(width=3)
            ))
        
        fig.update_layout(
            title="Monthly Registration Patterns by Course",
            xaxis_title="Month",
            yaxis_title="Registrations",
            height=500,
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Course detail cards
        st.subheader("Course Marketing Profiles")
        
        cols = st.columns(2)
        for idx, course in enumerate(selected_courses):
            with cols[idx % 2]:
                info = insights['course_seasonality'][course]
                
                st.markdown(f"""
                <div class="metric-card">
                    <h4>{course}</h4>
                    <p><strong>Type:</strong> {info['course_type']}</p>
                    <p><strong>Best Month:</strong> {info['best_month']} ({info['peak_value']} regs)</p>
                    <p><strong>Worst Month:</strong> {info['worst_month']} ({info['low_value']} regs)</p>
                    <div class="recommendation">
                        <strong>Strategy:</strong> {info['marketing_strategy']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# TAB 3: FORECASTING FOR NEXT YEAR
# -----------------------------------------------------------------------------

with tab3:
    st.header("Predictive Marketing Planning")
    
    if st.button("🚀 Train Forecasting Model", type="primary"):
        with st.spinner("Training AI model on historical patterns..."):
            mae, feature_importance = analytics.train_forecast_model(df)
            st.session_state.model_trained = True
            st.success(f"Model trained! Accuracy (MAE): {mae:.1f} registrations")
            
            st.subheader("What Drives Registrations?")
            st.dataframe(feature_importance, use_container_width=True)
    
    if st.session_state.get('model_trained', False):
        st.divider()
        st.subheader(f"📅 Predicted Performance for {selected_year + 1}")
        
        forecast_df = analytics.predict_next_year(all_courses, year=selected_year + 1)
        
        if forecast_df is not None and not forecast_df.empty:
            # Aggregate forecast by month
            monthly_forecast = forecast_df.groupby('month_name')['predicted_registrations'].sum().reset_index()
            
            fig_forecast = px.bar(
                monthly_forecast,
                x='month_name',
                y='predicted_registrations',
                title=f"Predicted Total Registrations by Month ({selected_year + 1})",
                color='predicted_registrations',
                color_continuous_scale='Greens'
            )
            st.plotly_chart(fig_forecast, use_container_width=True)
            
            # Top predicted courses
            course_forecast = forecast_df.groupby('course')['predicted_registrations'].sum().sort_values(ascending=False).head(10)
            
            st.subheader("Top 10 Courses to Focus On Next Year")
            st.bar_chart(course_forecast)
            
            # Download forecast
            csv = forecast_df.to_csv(index=False)
            st.download_button("Download Full Forecast CSV", csv, "marketing_forecast.csv", "text/csv")
        else:
            st.warning("Could not generate forecast. Ensure model is trained.")

# -----------------------------------------------------------------------------
# TAB 4: ACTIONABLE RECOMMENDATIONS
# -----------------------------------------------------------------------------

with tab4:
    st.header("🎯 Marketing Action Plan")
    
    # Generate automated recommendations
    recommendations = []
    
    # Find courses with extreme seasonality
    for course, info in insights['course_seasonality'].items():
        if info['seasonality_score'] > 1.5:
            recommendations.append({
                'priority': 'HIGH',
                'course': course,
                'action': f"Concentrate budget in {info['best_month']}. Avoid marketing in {info['worst_month']}.",
                'rationale': f"Highly seasonal (score: {info['seasonality_score']:.2f})"
            })
        elif info['peak_value'] > 50 and info['low_value'] < 10:
            recommendations.append({
                'priority': 'MEDIUM',
                'course': course,
                'action': f"Create off-season promotions for {info['worst_month']} to smooth demand.",
                'rationale': f"High variance between peak ({info['peak_value']}) and low ({info['low_value']})"
            })
    
    # Sort by priority
    recommendations.sort(key=lambda x: {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}.get(x['priority'], 3))
    
    st.subheader("Automated Marketing Recommendations")
    
    for rec in recommendations:
        color = {'HIGH': '🔴', 'MEDIUM': '🟡', 'LOW': '🟢'}.get(rec['priority'], '⚪')
        
        st.markdown(f"""
        <div class="recommendation">
            <h4>{color} {rec['priority']} PRIORITY: {rec['course']}</h4>
            <p><strong>Action:</strong> {rec['action']}</p>
            <p><em>{rec['rationale']}</em></p>
        </div>
        """, unsafe_allow_html=True)
    
    # Quarterly planning guide
    st.subheader("Quarterly Marketing Calendar")
    
    quarterly_data = insights['quarterly_trends']
    if not quarterly_data.empty:
        q_summary = quarterly_data.groupby('quarter')['registered_count'].sum().reset_index()
        q_summary['quarter_label'] = 'Q' + q_summary['quarter'].astype(str)
        
        fig_q = px.pie(
            q_summary,
            values='registered_count',
            names='quarter_label',
            title=f"Registration Distribution by Quarter ({selected_year})"
        )
        st.plotly_chart(fig_q, use_container_width=True)
        
        best_q = q_summary.loc[q_summary['registered_count'].idxmax(), 'quarter_label']
        
        st.markdown(f"""
        <div class="insight-box">
            <h4>💡 Quarterly Strategy</h4>
            <p><strong>{best_q}</strong> is your strongest quarter. Allocate 40% of annual marketing budget here.</p>
            <p>Use weaker quarters for brand building and content marketing rather than aggressive acquisition.</p>
        </div>
        """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# FOOTER
# -----------------------------------------------------------------------------

st.markdown("---")
st.markdown("""
<small>
<b>Course Marketing Intelligence System</b> | 
Designed for Marketing Teams | 
Data-driven campaign planning
</small>
""", unsafe_allow_html=True)
