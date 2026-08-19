import pandas as pd
import numpy as np
from sklearn.modeling import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error
import pickle
import os

class CourseAnalytics:
    def __init__(self):
        self.model = None
        self.label_encoders = {}
        self.is_trained = False

    def preprocess_data(self, df):
        """
        Prepares data for analysis and modeling.
        Expected columns: 'date', 'course_name', 'registered_count'
        """
        data = df.copy()
        
        # Convert date column
        data['date'] = pd.to_datetime(data['date'])
        
        # Extract time features
        data['year'] = data['date'].dt.year
        data['month'] = data['date'].dt.month
        data['quarter'] = data['date'].dt.quarter
        
        # Encode categorical data (Course Names)
        le = LabelEncoder()
        data['course_encoded'] = le.fit_transform(data['course_name'])
        self.label_encoders['course'] = le
        
        return data

    def get_performance_overview(self, df):
        """
        Generates aggregated statistics for management reporting.
        Returns: Dict of dataframes for reporting.
        """
        data = self.preprocess_data(df)
        
        # 1. Course Performance (Total & Average)
        course_perf = data.groupby('course_name')['registered_count'].agg(
            ['sum', 'mean', 'std', 'count']
        ).rename(columns={
            'sum': 'Total Registrations',
            'mean': 'Avg Registrations',
            'std': 'Std Dev',
            'count': 'Data Points'
        }).sort_values('Total Registrations', ascending=False)

        # 2. Seasonal/Monthly Trends
        monthly_trends = data.groupby('month')['registered_count'].sum()
        monthly_trends.index = [f"Month {i}" for i in monthly_trends.index]
        
        # 3. Quarterly Performance
        quarterly_perf = data.groupby('quarter')['registered_count'].sum()
        quarterly_perf.index = [f"Q{i}" for i in quarterly_perf.index]

        # 4. Course x Quarter Matrix (Heatmap data)
        course_quarter_matrix = pd.pivot_table(
            data, 
            values='registered_count', 
            index='course_name', 
            columns='quarter', 
            aggfunc='sum', 
            fill_value=0
        )

        return {
            'course_performance': course_perf,
            'monthly_trends': monthly_trends,
            'quarterly_performance': quarterly_perf,
            'course_quarter_matrix': course_quarter_matrix,
            'processed_data': data
        }

    def train_prediction_model(self, df):
        """
        Trains a Random Forest model to predict future registrations.
        Features: Month, Quarter, Course Encoding
        Target: Registered Count
        """
        data = self.preprocess_data(df)
        
        features = ['month', 'quarter', 'course_encoded']
        X = data[features]
        y = data['registered_count']

        # Train Random Forest Regressor
        self.model = RandomForestRegressor(
            n_estimators=100, 
            random_state=42, 
            n_jobs=-1
        )
        self.model.fit(X, y)
        self.is_trained = True
        
        # Calculate training error for reporting
        predictions = self.model.predict(X)
        mae = mean_absolute_error(y, predictions)
        
        return mae

    def predict_future(self, future_dates_config):
        """
        Generates predictions based on user configuration.
        future_dates_config: List of dicts with 'course_name', 'year', 'month'
        """
        if not self.is_trained:
            raise Exception("Model not trained. Please train the model first.")
        
        predictions = []
        for item in future_dates_config:
            # Encode course
            try:
                course_code = self.label_encoders['course'].transform([item['course_name']])[0]
            except:
                continue # Skip unknown courses
                
            input_data = pd.DataFrame({
                'month': [item['month']],
                'quarter': [pd.Timestamp(f"{item['year']}-{item['month']}-01").quarter],
                'course_encoded': [course_code]
            })
            
            pred = self.model.predict(input_data)[0]
            predictions.append({
                'course': item['course_name'],
                'year': item['year'],
                'month': item['month'],
                'predicted_registrations': max(0, pred) # No negative registrations
            })
            
        return pd.DataFrame(predictions)

# Helper to save/load model if needed later
def save_model(analytics_instance, path='model.pkl'):
    with open(path, 'wb') as f:
        pickle.dump(analytics_instance, f)

def load_model(path='model.pkl'):
    with open(path, 'rb') as f:
        return pickle.load(f)
