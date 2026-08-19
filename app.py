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

    def get_monthly_course_matrix(self, df):
        """Create a matrix of courses x months for heatmap"""
        data = self.preprocess_data(df)
        matrix = pd.pivot_table(
            data, 
            values='registered_count', 
            index='course_name', 
            columns='month', 
            aggfunc='sum', 
            fill_value=0
        )
        return matrix

    def get_course_performance_by_month(self, df, month):
        """Get course performance for a specific month"""
        data = self.preprocess_data(df)
        month_data = data[data['month'] == month]
        
        if month_data.empty:
            return None
        
        perf = month_data.groupby('course_name')['registered_count'].sum().reset_index()
        perf.columns = ['course_name', 'registrations']
        perf = perf.sort_values('registrations', ascending=False)
        return perf

    def forecast_next_year_month(self, df, target_month):
        """Simple forecasting based on historical averages + growth trend"""
        data = self.preprocess_data(df)
        
        forecasts = []
        courses = data['course_name'].unique()
        
        for course in courses:
            course_data = data[data['course_name'] == course]
            historical = course_data[course_data['date'].dt.month == target_month]
            
            if len(historical) > 0:
                # Calculate average and apply a conservative growth factor
                avg = historical['registered_count'].mean()
                forecast_val = avg * 1.15 
