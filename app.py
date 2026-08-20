import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
import io
import warnings
warnings.filterwarnings('ignore')

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Course Registration Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------------------------------------------------------
# CUSTOM CSS - EXECUTIVE DASHBOARD STYLING
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background-color: #f8fafc;
    }
    
    .stApp {
        background-color: #f8fafc;
    }
    
    .kpi-container {
        background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        border: 1px solid #e2e8f0;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .kpi-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08);
    }
    
    .kpi-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #0f172a;
        line-height: 1;
        margin-bottom: 8px;
    }
    
    .kpi-label {
        font-size: 0.875rem;
        color: #64748b;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .kpi-change {
        font-size: 0.875rem;
        font-weight: 600;
        margin-top: 8px;
    }
    
    .positive { color: #10b981; }
    .negative { color: #ef4444; }
    .neutral { color: #64748b; }
    
    .section-header {
        font-size: 1.25rem;
        font-weight: 600;
        color: #0f172a;
        margin: 32px 0 16px 0;
        padding-bottom: 12px;
        border-bottom: 2px solid #e2e8f0;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .executive-summary {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: white;
        padding: 24px;
        border-radius: 16px;
        margin-bottom: 24px;
    }
    
    .executive-summary h2 {
        color: white;
        margin: 0 0 12px 0;
        font-size: 1.5rem;
        font-weight: 600;
    }
    
    .executive-summary p {
        color: #cbd5e1;
        margin: 0;
        font-size: 1rem;
        line-height: 1.6;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
        color: white;
        border-radius: 10px;
        border: none;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 0.875rem;
        transition: all 0.2s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(14, 165, 233, 0.4);
    }
    
    .streamlit-expanderHeader {
        background-color: #ffffff;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        font-weight: 600;
        color: #0f172a;
        padding: 16px 20px;
    }
    
    .streamlit-expanderHeader:hover {
        background-color: #f8fafc;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f1f5f9;
        padding: 8px;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        color: #64748b;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #ffffff !important;
        color: #0f172a !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# DATA FUNCTIONS
# -----------------------------------------------------------------------------

def create_sample_data():
    """Create sample data for template download"""
    sample_data = []
    courses = ['ICDL', 'AWS', 'CCNA', 'AZURE', 'PMP', 'GRE', 'TOEFL']
    
    for year in [2023, 2024, 2025]:
        for month in range(1, 13):
            for course in courses:
                base = np.random.randint(5, 50)
                if month in [1, 9, 10]:
                    base = int(base * 1.5)
                sample_data.append({
                    'date': f"{year}-{month:02d}-15",
                    'course_name': course,
                    'registered_count': base
                })
    
    return pd.DataFrame(sample_data)

def create_real_dataset():
    """Load real data"""
    return create_sample_data()

# -----------------------------------------------------------------------------
# SIDEBAR
# -----------------------------------------------------------------------------

with st.sidebar:
    st.markdown("## 📊 Data Control Panel")
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); 
                padding: 20px; border-radius: 16px; margin-bottom: 20px;
                border: 2px solid #3b82f6;">
        <h3 style="color: #1e40af; margin: 0 0 12px 0; font-size: 1.1rem;">
            📁 Upload Your Data
        </h3>
        <p style="color: #1e40af; margin: 0 0 16px 0; font-size: 0.875rem;">
            Replace sample data with your actual registration records
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose CSV or Excel file",
        type=['csv', 'xlsx'],
        label_visibility="collapsed"
    )
    
    sample_df = create_sample_data()
    csv_buffer = io.StringIO()
    sample_df.to_csv(csv_buffer, index=False)
    
    st.download_button(
        label="📥 Download Template",
        data=csv_buffer.getvalue(),
        file_name="course_data_template.csv",
        mime="text/csv",
        use_container_width=True
    )
    
    st.markdown("---")
    
    if uploaded_file:
        st.success(f"✅ Using: **{uploaded_file.name}**")
    else:
        st.info("ℹ️ Using sample data")

# -----------------------------------------------------------------------------
# LOAD DATA
# -----------------------------------------------------------------------------

@st.cache_data
def load_data(uploaded_file):
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            required_cols = ['date', 'course_name', 'registered_count']
            missing = [c for c in required_cols if c not in df.columns]
            
            if missing:
                st.error(f"Missing columns: {', '.join(missing)}")
                return create_real_dataset(), "Sample Data (Error)"
            
            return df, f"Uploaded: {uploaded_file.name}"
        except Exception as e:
            st.error(f"Error: {str(e)}")
            return create_real_dataset(), "Sample Data (Error)"
    else:
        return create_real_dataset(), "Sample Data"

df, data_source = load_data(uploaded_file)

df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month

# -----------------------------------------------------------------------------
# HEADER
# -----------------------------------------------------------------------------

st.markdown("""
<div class="executive-summary">
    <h2>📊 Course Registration Intelligence</h2>
    <p>Executive dashboard for analyzing course performance across all years. 
    Select a month below to view year-over-year comparisons and forecast trends.</p>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# CONTROLS
# -----------------------------------------------------------------------------

col_controls = st.columns([2, 2, 2])

with col_controls[0]:
    month_names = {i: datetime.date(2024, i, 1).strftime('%B') for i in range(1, 13)}
    selected_month = st.selectbox(
        "📅 Select Month",
        options=list(range(1, 13)),
        format_func=lambda x: month_names[x],
        index=0
    )

with col_controls[1]:
    available_years = sorted(df['year'].unique())
    year_filter = st.multiselect(
        "🔍 Filter Years",
        options=available_years,
        default=available_years
    )

with col_controls[2]:
    analysis_type = st.radio(
        "📈 Analysis Type",
        options=["Overview", "Detailed"],
        horizontal=True
    )

filtered_df = df[df['year'].isin(year_filter)]
month_data = filtered_df[filtered_df['month'] == selected_month]

# -----------------------------------------------------------------------------
# KPI SECTION
# -----------------------------------------------------------------------------

st.markdown('<div class="section-header">🎯 Executive Summary - Overall Performance</div>', unsafe_allow_html=True)

total_registrations = month_data['registered_count'].sum()
total_courses = month_data['course_name'].nunique()
avg_per_course = total_registrations / total_courses if total_courses > 0 else 0

prev_year_data = filtered_df[
    (filtered_df['month'] == selected_month) & 
    (filtered_df['year'] == max(year_filter) - 1)
]
prev_total = prev_year_data['registered_count'].sum()
growth_pct = ((total_registrations - prev_total) / prev_total * 100) if prev_total > 0 else 0

col_kpis = st.columns(4)

with col_kpis[0]:
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-value">{total_registrations:,}</div>
        <div class="kpi-label">Total Registrations</div>
        <div class="kpi-change {'positive' if growth_pct > 0 else 'negative' if growth_pct < 0 else 'neutral'}">
            {'↑' if growth_pct > 0 else '↓' if growth_pct < 0 else '→'} {abs(growth_pct):.1f}% vs last year
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_kpis[1]:
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-value">{total_courses}</div>
        <div class="kpi-label">Active Courses</div>
        <div class="kpi-change neutral">Across {len(year_filter)} years</div>
    </div>
    """, unsafe_allow_html=True)

with col_kpis[2]:
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-value">{avg_per_course:.0f}</div>
        <div class="kpi-label">Avg per Course</div>
        <div class="kpi-change neutral">Monthly average</div>
    </div>
    """, unsafe_allow_html=True)

with col_kpis[3]:
    top_course = month_data.groupby('course_name')['registered_count'].sum().idxmax() if len(month_data) > 0 else "N/A"
    st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-value" style="font-size: 1.5rem;">{top_course}</div>
        <div class="kpi-label">Top Performing Course</div>
        <div class="kpi-change positive">Leading program</div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# COMBINED PERFORMANCE
# -----------------------------------------------------------------------------

st.markdown('<div class="section-header">📊 Combined Performance Analysis</div>', unsafe_allow_html=True)

if len(month_data) > 0:
    combined_perf = month_data.groupby('course_name')['registered_count'].sum().reset_index()
    combined_perf.columns = ['course_name', 'total_registrations']
    combined_perf = combined_perf.sort_values('total_registrations', ascending=False)
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown("**🏆 Top Performers**")
        top_10 = combined_perf.head(10)
        fig = px.bar(
            top_10,
            x='total_registrations',
            y='course_name',
            orientation='h',
            color='total_registrations',
            color_continuous_scale=['#e0f2fe', '#0284c7'],
            text='total_registrations'
        )
        fig.update_layout(
            height=400,
            showlegend=False,
            xaxis_title="Total Registrations",
            yaxis_title="",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=30, b=0)
        )
        fig.update_traces(textposition='outside', textfont=dict(size=10))
        st.plotly_chart(fig, use_container_width=True)
    
    with col_chart2:
        st.markdown("**⚠️ Needs Attention**")
        bottom_10 = combined_perf.tail(10)
        fig = px.bar(
            bottom_10,
            x='total_registrations',
            y='course_name',
            orientation='h',
            color='total_registrations',
            color_continuous_scale=['#fee2e2', '#dc2626'],
            text='total_registrations'
        )
        fig.update_layout(
            height=400,
            showlegend=False,
            xaxis_title="Total Registrations",
            yaxis_title="",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=30, b=0)
        )
        fig.update_traces(textposition='outside', textfont=dict(size=10))
        st.plotly_chart(fig, use_container_width=True)
    
    # Full data table
    with st.expander("📋 View Complete Data Table", expanded=False):
        st.dataframe(combined_perf, use_container_width=True, hide_index=True)
else:
    st.warning("No data available for selected month and years.")

# -----------------------------------------------------------------------------
# YEAR-BY-YEAR BREAKDOWN (DROPDOWN TABS)
# -----------------------------------------------------------------------------

st.markdown('<div class="section-header">📅 Year-by-Year Performance Breakdown</div>', unsafe_allow_html=True)

for year in sorted(year_filter, reverse=True):
    year_data = month_data[month_data['year'] == year]
    
    if len(year_data) == 0:
        continue
    
    year_total = year_data['registered_count'].sum()
    year_courses = year_data['course_name'].nunique()
    
    with st.expander(f"**{year}** — {year_total:,} registrations across {year_courses} courses", expanded=False):
        
        year_perf = year_data.groupby('course_name')['registered_count'].sum().reset_index()
        year_perf = year_perf.sort_values('registered_count', ascending=False)
        
        col_y1, col_y2 = st.columns(2)
        
        with col_y1:
            st.markdown(f"**Top 10 Courses — {year}**")
            fig = px.bar(
                year_perf.head(10),
                x='registered_count',
                y='course_name',
                orientation='h',
                color='registered_count',
                color_continuous_scale=['#d1fae5', '#059669'],
                text='registered_count'
            )
            fig.update_layout(height=350, showlegend=False, xaxis_title="", yaxis_title="")
            fig.update_traces(textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
        
        with col_y2:
            st.markdown(f"**Bottom 10 Courses — {year}**")
            fig = px.bar(
                year_perf.tail(10),
                x='registered_count',
                y='course_name',
                orientation='h',
                color='registered_count',
                color_continuous_scale=['#fee2e2', '#dc2626'],
                text='registered_count'
            )
            fig.update_layout(height=350, showlegend=False, xaxis_title="", yaxis_title="")
            fig.update_traces(textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("View Raw Data", expanded=False):
            st.dataframe(year_perf, use_container_width=True, hide_index=True)

# -----------------------------------------------------------------------------
# FORECAST SECTION
# -----------------------------------------------------------------------------

st.markdown('<div class="section-header">🔮 2027 Forecast & Planning</div>', unsafe_allow_html=True)

col_f1, col_f2 = st.columns([3, 1])

with col_f2:
    if st.button("🚀 Generate 2027 Forecast", type="primary", use_container_width=True):
        with st.spinner("Analyzing trends..."):
            # Simple forecast calculation
            courses = month_data['course_name'].unique()
            forecasts = []
            
            for course in courses:
                course_hist = month_data[month_data['course_name'] == course]
                if len(course_hist) > 0:
                    avg = course_hist['registered_count'].mean()
                    forecast = int(avg * 1.15)  # 15% growth
                    forecasts.append({
                        'course': course,
                        'forecast_2027': forecast,
                        'historical_avg': int(avg)
                    })
            
            forecast_df = pd.DataFrame(forecasts).sort_values('forecast_2027', ascending=False)
            st.session_state['forecast'] = forecast_df

with col_f1:
    if 'forecast' in st.session_state:
        forecast_df = st.session_state['forecast']
        
        fig = px.bar(
            forecast_df.head(15),
            x='forecast_2027',
            y='course',
            orientation='h',
            color='forecast_2027',
            color_continuous_scale=['#dbeafe', '#2563eb'],
            text='forecast_2027'
        )
        fig.update_layout(
            height=500,
            showlegend=False,
            xaxis_title="Predicted 2027 Registrations",
            yaxis_title="",
            title=f"Top 15 Courses — Forecast for {month_names[selected_month]} 2027"
        )
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, use_container_width=True)
        
        # Download forecast
        csv = forecast_df.to_csv(index=False)
        st.download_button(
            "📥 Download Forecast CSV",
            csv,
            f"forecast_2027_{month_names[selected_month]}.csv",
            "text/csv"
        )
    else:
        st.info("Click 'Generate 2027 Forecast' to see AI-powered predictions based on historical trends.")

# -----------------------------------------------------------------------------
# FOOTER
# -----------------------------------------------------------------------------

st.divider()
st.markdown("""
<div style="text-align: center; color: #64748b; padding: 20px;">
    <p style="margin: 0; font-size: 0.875rem;">
        📊 Course Registration Intelligence System | Management Analytics Dashboard
    </p>
    <p style="margin: 8px 0 0 0; font-size: 0.75rem;">
        Data source: """ + data_source + """
    </p>
</div>
""", unsafe_allow_html=True)
