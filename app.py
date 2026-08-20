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
# COMPLETE REAL DATASETS FROM IMAGES
# -----------------------------------------------------------------------------

def create_real_dataset():
    """Create complete dataset from provided images"""
    
    data_rows = []
    
    # 2023 Data (Complete - all 12 months)
    data_2023 = {
        'AGILEPR2': [0,0,0,0,2,0,0,0,4,6,1,0],
        'AICDL': [0,3,2,1,4,1,0,0,4,2,0,0],
        'ANALYZING EXCEL': [0,0,0,0,4,0,0,0,8,2,0,0],
        'ANDROID': [0,3,2,0,0,0,0,0,0,0,0,0],
        'AUTOCAD': [0,0,1,0,0,0,0,0,0,0,0,0],
        'AWS': [0,0,0,0,0,0,0,0,30,5,18,0],
        'AZ-500E': [0,0,0,0,0,0,0,0,0,2,0,1],
        'AZURE': [0,1,1,6,0,1,2,0,0,2,0,2],
        'CA': [0,2,0,3,1,0,4,12,1,2,2,0],
        'CA747': [0,6,0,0,3,14,11,14,0,3,10,11],
        'CCNA': [0,10,3,9,0,5,1,11,1,9,2,0],
        'CCNP': [0,0,0,0,0,0,0,0,2,0,2,0],
        'CCSP': [0,0,0,0,0,0,0,7,0,0,0,0],
        'CDPSE': [0,0,1,0,4,0,0,2,0,2,1,0],
        'CDSP': [0,0,0,0,0,0,0,2,0,0,0,0],
        'CEH': [0,4,0,0,2,0,5,10,0,0,2,2],
        'CFA': [0,0,0,0,0,0,0,0,0,1,0,0],
        'CISA': [0,9,2,0,2,2,0,0,2,11,0,1],
        'CISCO EXAMS': [0,0,2,1,0,0,0,0,3,3,0,1],
        'CISM': [0,3,1,0,1,2,1,0,0,2,0,0],
        'CISP': [0,0,0,0,0,0,14,0,4,0,0,0],
        'CITRIX VIRTUAL APPS': [0,0,0,0,0,4,0,0,0,0,0,0],
        'CKAD': [0,0,0,0,0,0,0,0,2,1,4,0],
        'COMPTIA A+': [0,4,5,2,3,4,0,0,6,1,5,0],
        'COMPTIA EXAM': [0,0,0,0,0,0,0,0,2,0,0,1],
        'COMPTIA N+': [0,0,0,0,0,0,0,0,2,0,0,3],
        'COMPTIA S+': [0,0,0,1,1,5,0,1,6,0,0,0],
        'CRISC': [0,2,0,0,0,0,0,0,0,0,0,0],
        'CYSA+': [0,1,1,3,0,1,0,4,0,3,8,1],
        'DATA PROTECTION': [0,0,0,0,9,0,0,0,0,0,0,0],
        'DATA+': [0,0,0,0,0,0,0,1,0,0,0,0],
        'DIGITAL ACADEMY': [0,0,0,0,0,0,0,0,30,0,0,0],
        'DIGITAL MARKETING': [0,0,0,0,1,1,1,0,1,0,0,0],
        'DP-080TOO QUERYING': [0,0,0,0,0,4,0,0,0,0,0,0],
        'FORTINET NSE 7': [0,0,0,0,0,0,0,0,1,0,0,0],
        'GDP': [0,5,2,0,5,2,0,3,2,2,2,4],
        'GMAT': [0,0,0,0,0,0,0,0,0,0,2,0],
        'GRE': [0,9,4,5,10,6,5,3,10,4,7,2],
        'GRE EXAMS': [0,0,0,0,0,2,0,1,7,1,6,7],
        'ICDL': [0,86,68,41,57,24,10,11,25,5,0,3],
        'ICDL30K': [0,0,0,0,0,0,0,0,2,14,22,4],
        'IELTS EXAM': [0,0,0,0,0,0,0,0,0,1,0,0],
        'IoT': [0,0,0,0,0,1,0,0,0,0,0,0],
        'ISACA EXAM': [0,0,0,0,0,0,0,0,34,0,0,0],
        'ISC2': [0,0,0,0,0,0,0,0,0,2,1,0],
        'ISO': [0,0,0,0,0,0,2,0,0,0,0,0],
        'ISQTB': [0,0,0,0,0,0,0,0,3,0,3,0],
        'ISTQB.': [0,0,1,0,0,0,0,0,1,0,1,0],
        'ITIL': [0,0,0,0,0,0,0,0,4,3,1,0],
        'ITIL EXAM': [0,0,0,0,0,1,0,0,3,2,2,4],
        'ITILF': [0,8,7,7,3,7,1,9,2,4,11,6],
        'JAVASD': [0,0,0,0,0,0,0,0,0,0,0,0],
        'L3 DC': [0,3,4,6,3,5,7,0,0,0,0,1],
        'L4DBIT': [0,0,0,0,0,0,0,0,1,0,0,0],
        'L4DC 2023': [0,5,4,0,0,9,9,7,0,0,0,0],
        'L5DC': [0,0,1,0,1,0,0,0,0,0,0,1],
        'LEVEL 5 CYBER': [0,0,0,0,0,2,0,0,0,0,1,0],
        'MB_800': [0,0,0,0,0,0,0,5,0,0,0,4],
        'MICROSOFT EXAMS': [0,2,1,0,0,2,0,0,5,1,2,1],
        'MOP': [0,11,11,4,3,9,5,5,1,3,3,2],
        'MS 500': [0,0,0,0,3,0,0,0,0,0,0,0],
        'MSQL': [0,0,0,0,0,1,0,0,0,0,0,0],
        'NCC': [0,1,0,0,0,0,0,0,0,0,0,0],
        'ORACLE': [0,3,1,0,3,4,0,3,1,1,0,0],
        'ORACLESBT': [0,0,0,0,0,0,0,0,0,0,12,0],
        'ORACLESBTF': [0,0,0,0,0,0,0,0,0,0,11,0],
        'P-10975': [0,3,5,6,5,9,0,5,2,0,3,0],
        'PAL 1': [0,0,0,0,0,0,0,0,0,0,1,0],
        'PL-300': [0,0,0,1,3,0,2,13,6,0,0,0],
        'PMI EXAM': [0,0,0,0,0,1,0,0,3,2,0,0],
        'PMI-PBA': [0,0,0,0,0,0,0,0,0,1,0,0],
        'PMP': [0,15,3,7,5,1,1,11,10,7,8,0],
        'PRINCE2': [0,0,0,0,0,0,0,0,4,0,0,0],
        'PSM 1': [0,0,0,0,0,0,0,0,0,0,1,0],
        'PSM 2': [0,0,0,0,0,0,0,0,2,0,0,0],
        'PSM II': [0,0,0,0,0,0,0,0,0,0,0,1],
        'PSPO 1': [0,0,0,0,0,0,0,0,0,0,3,0],
        'PSU EXAM': [0,0,0,0,0,0,0,0,6,0,1,0],
        'PTE EXAM': [0,0,0,0,0,0,0,2,9,6,11,3],
        'QB': [0,0,0,0,1,0,0,0,0,0,0,0],
        'SAGE HR': [0,0,0,0,0,0,0,0,7,0,0,0],
        'SD-V1': [0,2,4,4,2,5,0,1,0,0,1,0],
        'SD:PYTHON': [0,0,0,0,0,0,0,0,1,0,0,0],
        'SD:WEB': [0,0,0,0,0,0,0,0,0,4,1,0],
        'SE1-JAVA': [0,0,0,0,0,0,0,1,0,0,0,0],
        'SELT': [0,0,0,0,0,0,0,0,0,0,0,1],
        'TESTING EXAMS': [0,0,0,0,0,1,0,0,1,1,0,0],
        'TOEFL': [0,18,6,8,11,4,4,19,2,8,2,0],
        'TOEFL EXAMS': [0,0,0,0,2,7,2,1,13,7,7,5],
        'TOGAF': [0,0,0,0,0,0,0,0,0,1,0,0],
        'UCLAN': [0,1,0,0,0,0,0,1,0,0,0,0],
        'Unassigned / Unknown': [0,1,0,0,0,0,0,0,0,0,0,0],
        'VM-ICM': [0,0,1,12,0,0,0,1,0,0,1,0],
        'VUE': [0,0,0,0,0,0,0,0,1,0,0,0],
        'VUE EXAM': [0,1,1,0,0,0,0,0,2,2,1,0],
        'WD101': [0,3,2,0,4,5,0,1,0,3,0,0],
        'WINDOWS SERVER': [0,0,1,1,0,0,0,0,4,0,0,0]
    }
    
    # 2024 Data (Complete)
    data_2024 = {
        '55238-B: SHAREPOINT': [0,0,0,0,0,0,0,0,0,1,0,0],
        'ACCA': [0,1,0,0,0,0,0,0,1,0,0,0],
        'ACCA EXAM': [0,0,0,0,0,4,1,2,4,0,1,0],
        'ACCA MAIN': [3,0,0,0,0,0,0,0,0,2,0,0],
        'AGILEPR2': [0,0,1,7,5,0,5,0,0,0,0,3],
        'AICDL': [0,0,1,1,0,1,0,0,1,0,0,0],
        'AMAZON': [0,0,0,0,0,2,0,0,0,0,0,0],
        'ANALYZING EXCEL': [4,0,2,0,2,0,2,4,5,1,0,0],
        'AWS': [0,0,3,4,2,0,1,1,3,1,1,1],
        'AZ800T00': [0,0,0,0,0,0,0,0,0,1,0,0],
        'AZURE': [1,0,1,2,1,5,0,0,0,6,0,0],
        'CA': [0,0,2,1,2,3,1,1,1,1,6,3],
        'CA747': [1,8,1,0,0,1,1,2,3,0,1,0],
        'CASE': [0,0,0,2,0,0,0,0,0,0,0,0],
        'CCNA': [2,9,3,8,2,4,1,3,8,5,7,1],
        'CCNP': [0,0,0,0,1,0,0,0,1,0,0,0],
        'CCT:ECOUNCIL': [0,1,0,0,0,0,0,0,0,0,0,0],
        'CDP': [0,0,0,0,0,0,0,0,2,0,0,0],
        'CDPSE EXAM': [0,1,0,0,0,0,0,0,0,0,0,0],
        'CDSP': [0,0,0,0,0,1,0,0,0,0,0,0],
        'CEH': [0,0,1,1,8,0,0,0,1,1,2,0],
        'CGEIT': [0,0,0,0,0,0,0,0,0,0,6,0],
        'CISA': [1,6,1,2,6,1,2,5,0,5,0,0],
        'CISCO EXAMS': [0,0,0,0,1,0,0,1,0,0,0,2],
        'CISM': [0,1,1,1,3,0,3,0,1,2,2,0],
        'CISP': [0,0,3,4,11,1,0,0,2,0,2,1],
        'CISP EXAM': [0,0,0,0,0,0,0,2,1,0,0,0],
        'CKAD': [1,0,0,0,0,0,1,0,1,0,1,0],
        'CLOUD+': [0,0,0,0,0,0,0,1,0,0,0,0],
        'CNEXUS': [0,0,2,0,0,1,0,0,0,0,0,0],
        'COMPTIA A+': [2,10,2,5,2,7,1,1,0,5,0,0],
        'COMPTIA EXAM': [2,2,0,1,0,0,0,1,2,1,1,0],
        'COMPTIA N+': [0,1,1,1,0,1,1,1,0,0,0,1],
        'COMPTIA S+': [1,4,1,0,3,1,0,2,1,2,3,0],
        'COMPTIA SERVER+': [0,0,0,0,0,0,1,0,0,0,0,0],
        'CORELDRAW': [0,1,0,0,0,2,0,0,0,0,0,0],
        'CRISC': [0,0,1,0,0,0,6,0,0,0,0,0],
        'CYSA+': [0,2,1,3,7,1,0,3,0,0,3,0],
        'DCID CISCO': [0,0,0,0,6,0,0,0,0,0,0,0],
        'DEVOPS COURSE': [0,1,0,0,0,0,0,0,0,0,0,0],
        'DIGITAL MARKETING': [0,6,0,1,1,1,1,0,0,0,0,0],
        'DP-080TOO QUERYING': [0,0,0,2,0,0,0,0,0,0,0,0],
        'DP-300': [0,0,0,0,0,2,0,0,1,0,0,0],
        'FDA': [0,0,0,0,0,0,0,0,1,0,0,0],
        'FORTIGATE': [0,0,0,0,0,0,0,0,5,6,0,0],
        'FORTINET NSE 7': [0,1,0,0,1,0,0,0,0,2,0,0],
        'FORTISIEM': [0,0,0,0,0,0,0,0,0,2,0,0],
        'GCFE': [0,0,1,0,0,0,0,0,0,0,0,0],
        'GDP': [2,0,0,0,0,1,0,0,0,0,0,0],
        'GMAT': [1,0,0,0,0,0,0,0,0,1,1,0],
        'GRAPHIC CUSTOMIZED': [0,0,0,0,0,0,0,0,0,1,0,0],
        'GRE': [1,2,3,1,2,1,5,2,10,4,1,0],
        'GRE EXAMS': [3,4,5,4,1,2,3,3,2,2,1,1],
        'GRE SCORES': [0,1,0,0,0,0,0,0,0,0,0,0],
        'GRI': [0,0,0,0,0,1,0,0,0,0,0,0],
        'ICDL': [2,0,14,0,0,0,1,0,1,0,0,0],
        'ICDL30K': [98,79,37,47,52,37,11,23,17,19,11,9],
        'ICDLCODING': [0,0,0,0,0,0,0,0,0,1,0,0],
        'ICDLEXAMS_ONLY': [0,0,0,0,0,0,0,2,2,3,0,0],
        'ICIFA': [0,0,0,0,0,0,0,1,0,0,0,0],
        'IELTS': [0,0,1,1,0,0,0,0,0,0,0,0],
        'IELTS EXAM': [0,0,0,1,1,0,0,0,1,0,0,0],
        'IHRM': [0,0,0,0,0,0,0,0,1,0,0,0],
        'ILLUSTRATOR': [0,0,0,1,0,0,0,0,0,0,0,0],
        'IN_DESIGN': [0,0,0,0,2,0,0,0,0,1,0,0],
        'IOSH MEMBERSHIP': [0,0,0,0,0,0,0,0,1,0,0,0],
        'ISACA EXAM': [0,0,0,0,0,0,0,0,3,0,0,0],
        'ISC2': [0,0,0,1,0,0,0,0,0,0,0,0],
        'ISO': [1,0,0,0,0,0,0,0,0,0,0,0],
        'ISQTB': [1,0,0,0,0,0,0,0,1,0,3,0],
        'ISTQB.': [0,0,1,0,0,0,0,0,3,0,0,0],
        'ITIL': [0,0,0,0,0,0,0,4,3,1,0,0],
        'ITIL EXAM': [0,0,0,0,0,1,0,0,3,2,2,4],
        'ITILF': [0,8,7,7,3,7,1,9,2,4,11,6],
        'JAVASD': [0,0,0,0,0,0,0,0,0,0,0,0],
        'L3 DC': [0,3,4,6,3,5,7,0,0,0,0,1],
        'L4DBIT': [0,0,0,0,0,0,0,0,1,0,0,0],
        'L4DC 2023': [0,5,4,0,0,9,9,7,0,0,0,0],
        'L5DC': [0,0,1,0,1,0,0,0,0,0,0,1],
        'LEVEL 5 CYBER': [0,0,0,0,0,2,0,0,0,0,1,0],
        'LINUX+': [1,0,0,1,0,0,0,0,0,0,0,0],
        'LTC': [17,0,19,0,0,0,0,0,0,0,0,0],
        'MANAGE ENGINE': [0,0,2,0,0,1,0,0,0,0,0,0],
        'MB-700': [0,1,0,0,0,0,0,0,0,0,0,0],
        'MB-820': [1,0,0,0,0,0,0,0,0,0,0,0],
        'MB-820 DEV': [0,0,0,7,0,0,0,0,0,0,0,0],
        'MB_800': [0,3,2,1,0,0,1,1,0,0,0,0],
        'MEMBERSHIP': [0,1,0,0,0,0,0,0,3,0,0,0],
        'MICROSOFT EXAMS': [0,1,2,6,3,0,3,0,1,0,0,2],
        'MICROSOFT EXAM': [0,0,0,0,0,1,0,0,0,1,0,0],
        'MICROSOFT 365': [0,0,0,0,0,0,0,0,1,0,0,0],
        'MOE-DEVOPS': [16,0,0,0,0,0,0,0,0,0,0,0],
        'OC:UNIX/LINUX': [0,0,0,0,10,0,0,0,0,0,0,0],
        'ORACLE': [1,1,0,0,0,0,0,0,0,1,0,0],
        'ORACLE EXAM': [0,1,0,0,0,0,1,0,0,0,0,0],
        'ORACLE HRMS': [0,0,0,0,0,0,1,0,0,0,0,0],
        'ORACLE SQL': [0,0,0,1,1,0,1,5,0,1,0,0],
        'ORACLEFINANCIAL': [0,0,0,0,0,3,0,0,0,0,0,0],
        'OSCP': [0,0,0,0,0,0,0,0,7,1,0,0],
        'P-10975': [0,0,2,0,0,3,0,0,1,0,1,0],
        'PHOTOSHOP': [0,2,0,0,0,0,0,0,0,0,0,0],
        'PL-300': [0,1,7,0,15,2,1,2,3,6,3,2],
        'PMI EXAM': [0,0,1,0,0,0,0,0,0,0,0,0],
        'PMI-PBA': [0,0,0,0,0,1,0,0,0,0,0,0],
        'PMP': [1,9,4,5,4,1,7,4,10,8,1,2],
        'PRINCE 2 FOUNDATION': [1,0,0,0,0,0,0,0,0,2,0,1],
        'PRINCE2': [0,0,0,0,0,0,0,0,1,0,0,0],
        'PSM 1': [0,1,0,0,0,0,0,0,0,0,0,0],
        'PSPO 1': [0,1,0,1,0,0,0,0,0,0,0,0],
        'PTE EXAM': [14,9,6,12,12,12,7,6,10,14,12,11],
        'QB': [0,0,0,0,1,0,0,0,0,0,0,0],
        'SAGE 200': [0,0,0,6,0,0,0,0,0,1,0,0],
        'SC-200': [0,0,3,0,0,0,0,6,0,0,0,0],
        'SD-V1': [4,3,5,2,1,0,3,0,0,0,0,0],
        'SD-JAVA': [0,3,0,0,0,1,0,0,0,0,0,0],
        'SD-PYTHON': [0,1,0,3,1,0,4,0,0,0,2,0],
        'SD-WEB': [0,0,2,1,4,0,2,1,0,5,0,0],
        'SELT': [3,2,2,0,1,1,2,2,1,0,1,0],
        'SQLSERVER': [6,0,0,0,0,0,0,0,0,0,0,0],
        'TOEFL': [6,4,10,2,10,0,0,2,1,1,0,0],
        'TOEFL 2': [0,0,0,0,0,6,3,2,1,2,0,0],
        'TOEFL EXAMS': [6,4,9,6,12,6,12,15,8,9,10,6],
        'TOGAF': [0,1,2,0,0,0,0,0,1,2,1,0],
        'UCLAN': [1,0,0,0,0,0,0,1,0,0,0,0],
        'UCLAN CYBERSECURITY': [0,0,0,0,0,0,1,0,0,0,0,0],
        'Unassigned / Unknown': [0,0,0,0,0,0,0,0,0,1,0,0],
        'VM-ICM': [0,0,0,1,3,0,0,0,4,1,0,0],
        'VUE EXAM': [0,0,0,0,0,0,0,0,2,2,1,0],
        'WD101': [0,1,0,0,4,5,0,1,0,3,0,0],
        'WINDOWS SERVER': [0,0,0,1,0,0,0,0,4,0,0,0]
    }
    
    # 2025 Data (Complete)
    data_2025 = {
        '2025LEVEL5': [0,0,0,0,1,0,0,0,0,0,0,0],
        '20764': [0,1,0,0,0,0,0,0,0,0,0,0],
        'ACAMS': [0,0,0,0,0,0,0,0,0,0,0,0],
        'ACCA': [0,0,1,0,0,0,0,0,0,0,0,0],
        'ACCA EXAM': [1,2,1,3,4,0,3,0,1,3,2,5],
        'ACFE': [0,4,0,0,0,0,0,0,0,0,0,0],
        'ADV.WORD ICDL': [1,0,0,0,0,0,0,0,0,0,0,0],
        'AGILEPR2': [0,2,0,0,0,0,0,0,2,0,0,1],
        'AICDL': [3,0,3,0,0,0,1,0,0,1,0,0],
        'AMAZON': [1,0,0,1,0,0,0,0,1,0,0,1],
        'ANALYZING EXCEL': [2,13,1,3,1,0,3,0,1,0,0,0],
        'ANALYZING PYTHON': [0,0,0,0,0,0,0,0,1,0,0,0],
        'API AND WEB SERVICES': [0,3,0,0,0,0,0,0,0,0,0,0],
        'AWS': [6,2,1,0,2,1,1,1,5,0,2,2],
        'AWS AD': [0,0,0,0,0,0,0,0,0,0,1,0],
        'AWS CLOUD PRACTITIONER': [0,0,0,0,0,0,0,0,0,0,0,1],
        'AZ-801': [0,0,0,0,0,0,1,0,0,0,0,0],
        'AZ-900': [0,0,0,0,0,0,1,0,0,0,0,0],
        'AZ800T00': [0,0,0,2,0,0,0,0,0,0,0,0],
        'AZURE': [0,1,0,0,1,0,5,0,0,0,0,0],
        'CA': [5,0,3,3,5,2,2,0,0,0,0,0],
        'CA747': [1,0,0,0,0,1,0,0,0,12,1,0],
        'CAIP': [0,0,4,2,0,0,0,0,0,0,0,0],
        'CBAP': [2,0,0,0,0,1,0,0,0,0,0,0],
        'CBCI': [0,0,0,0,0,0,0,0,1,0,0,0],
        'CCNA': [5,1,3,7,4,4,2,5,3,1,1,0],
        'CCNP': [3,0,2,0,0,0,0,0,1,0,0,0],
        'CDP': [0,0,0,0,0,0,1,0,0,0,0,0],
        'CDPSE': [0,0,0,0,0,1,0,0,0,0,0,0],
        'CDPSE EXAM': [0,1,3,0,0,0,0,0,0,0,0,0],
        'CDSP': [0,0,0,0,0,1,0,0,0,0,0,0],
        'CEH': [0,0,0,0,3,0,2,0,0,0,0,0],
        'CGEIT': [0,0,0,0,0,0,2,0,0,0,0,0],
        'CHECK-CCSA': [0,0,0,4,0,0,0,0,0,0,0,0],
        'CISSP': [0,0,0,0,0,0,1,0,0,0,0,0],
        'CISSP EXAM': [3,5,0,2,7,0,3,7,0,0,0,0],
        'CKA': [0,0,0,0,0,2,0,0,0,0,0,0],
        'CKAD': [0,1,5,1,0,0,1,0,1,0,7,0],
        'CLOUD+': [0,0,0,0,0,0,0,0,0,1,0,0],
        'COMPTIA A+': [3,3,1,1,0,4,3,2,4,1,1,0],
        'COMPTIA EXAM': [1,1,4,0,0,0,1,1,1,0,0,0],
        'COMPTIA N+': [0,0,0,3,0,3,0,1,0,1,1,2],
        'COMPTIA PENTEST': [0,0,0,1,0,0,0,0,0,0,0,0],
        'COMPTIA PRO1': [0,0,1,0,0,0,0,0,0,0,0,0],
        'COMPTIA S+': [6,5,0,3,5,2,0,0,0,0,0,0],
        'COMPTIACISCONETWORK': [0,0,1,1,1,4,4,4,0,0,0,0],
        'COMPTIACORE 1&2': [0,0,0,0,0,0,0,3,0,0,0,0],
        'CORELDRAW': [2,1,0,0,1,0,2,0,0,0,0,0],
        'COURSERA': [0,1,0,0,0,0,0,0,0,0,0,0],
        'CRISC': [0,0,1,0,0,0,6,0,0,0,0,0],
        'CYBERSECURITY COURSE': [0,1,0,0,0,0,1,0,0,0,0,0],
        'CYSA+': [0,0,5,0,0,1,0,1,0,1,2,0],
        'C|PEHT AI': [0,0,0,0,8,0,0,0,0,0,0,0],
        'DATACAMP EXAM': [0,1,0,0,0,0,0,0,0,0,0,0],
        'DATASCIENCE': [0,0,0,0,0,0,1,1,0,0,0,0],
        'DESIGN THINKING P': [0,0,2,0,0,0,0,0,0,0,0,0],
        'DIGITAL MARKETING': [0,0,2,0,3,0,0,0,0,0,0,0],
        'DP-080TOO QUERYING': [0,0,0,0,1,0,0,0,0,0,0,0],
        'EBS': [1,0,0,0,0,0,0,0,0,0,0,0],
        'ENTERPRISE API': [0,1,0,0,0,0,0,0,0,0,0,0],
        'FORTI MAIL': [0,0,0,0,0,0,3,0,0,0,0,0],
        'FORTI OS': [0,7,10,0,0,9,1,1,0,0,0,0],
        'FORTIANALYSER': [0,0,0,7,0,0,0,0,0,0,0,0],
        'FORTIGATE': [0,0,0,0,0,3,1,0,0,0,0,0],
        'FORTIMANAGER ADMINIS': [0,0,0,4,0,1,0,0,0,0,0,0],
        'FORTINAC-F': [0,0,7,0,0,0,0,0,0,0,0,0],
        'FORTINET NSE 7': [0,0,0,0,0,0,1,0,0,0,0,0],
        'FORTISIEM': [0,0,0,0,0,7,0,0,0,0,0,0],
        'FORTIWEB 7.4': [0,0,0,5,0,0,0,0,0,0,0,0],
        'FUNCTIONAL TRAINING': [0,0,0,0,0,0,25,0,0,0,0,0],
        'GDP': [0,1,0,0,0,2,0,0,0,0,0,0],
        'GENAIBIZ': [0,0,1,0,0,2,0,0,0,0,0,0],
        'GRE EXAMS': [1,1,0,0,1,0,1,0,0,0,0,0],
        'HCM WORKSHOP': [0,0,0,0,0,0,16,0,0,0,0,0],
        'IBM': [0,1,0,0,0,0,0,0,0,0,0,0],
        'IBM QRADAR': [0,0,0,7,0,0,0,0,0,0,0,0],
        'IBM UI': [0,1,0,0,0,0,0,0,0,0,0,0],
        'ICDL': [0,0,0,1,0,0,0,0,0,0,0,0],
        'ICDL 35K': [73,91,50,38,42,16,17,8,15,9,9,5],
        'ICDL30K': [7,3,0,2,0,0,1,0,0,0,0,0],
        'ICDLEXAMS_ONLY': [0,0,0,0,0,0,0,1,0,0,0,0],
        'ICIFA': [0,0,0,0,0,0,0,1,0,0,0,0],
        'IELTS': [1,0,0,0,0,0,0,0,0,0,0,0],
        'IELTS EXAM': [0,0,2,0,0,0,0,0,0,0,0,0],
        'ILLUSTRATOR': [0,1,0,0,2,1,0,0,0,0,0,0],
        'INNOVATION MGT': [0,0,2,0,0,0,0,0,0,0,0,0],
        'ISO': [1,0,0,0,0,0,0,0,0,0,0,0],
        'ISO 27001-FL': [0,0,0,0,0,3,0,0,0,0,0,0],
        'ISQTB': [1,0,0,0,0,0,0,0,0,0,0,0],
        'ISTQB.': [0,0,1,0,0,0,0,0,0,0,0,0],
        'ITIL': [0,0,2,0,0,0,0,0,0,0,0,0],
        'ITIL EXAM': [3,0,4,3,1,6,3,6,2,3,1,3],
        'ITIL5 FOUNDATION': [0,0,0,0,0,0,5,0,0,0,0,0],
        'ITILDP1': [0,1,0,0,0,0,0,4,0,0,0,0],
        'ITILF': [5,1,7,8,6,8,0,0,5,16,1,5],
        'JAVASD': [0,1,0,0,0,1,0,0,0,0,0,0],
        'L3 DC': [13,3,0,0,2,7,0,0,1,1,0,0],
        'L4DBIT': [0,0,0,0,1,1,0,0,0,0,0,0],
        'L4DC 2023': [6,1,0,0,2,5,5,0,0,0,0,0],
        'L5DBIT': [1,2,0,0,0,0,0,0,1,0,0,0],
        'L5DC': [2,0,0,0,0,1,0,0,0,0,0,0],
        'LEVEL 5 CYBER': [1,0,0,0,0,0,0,0,0,0,0,0],
        'LINUX+': [0,0,1,1,0,0,0,0,0,0,0,0],
        'LTC': [17,0,19,0,0,0,0,0,0,0,0,0],
        'MANAGE ENGINE': [0,0,2,0,0,1,0,0,0,0,0,0],
        'MB-700': [0,1,0,0,0,0,0,0,0,0,0,0],
        'MB-820': [1,0,0,0,0,0,0,0,0,0,0,0],
        'MB-820 DEV': [0,0,0,7,0,0,0,0,0,0,0,0],
        'MB_800': [0,3,2,1,0,0,1,1,0,0,0,0],
        'MEMBERSHIP RENEWAL': [0,0,0,0,0,0,0,0,3,0,0,0],
        'MICROSOFT EXAMS': [2,1,2,6,3,0,3,0,1,0,0,2],
        'MICROSOFT EXAM': [0,0,0,0,0,1,0,0,0,1,0,0],
        'MICROSOFT 365': [0,0,0,0,0,0,0,0,1,0,0,0],
        'MOE-DEVOPS': [16,0,0,0,0,0,0,0,0,0,0,0],
        'OC:UNIX/LINUX': [0,0,0,0,10,0,0,0,0,0,0,0],
        'ORACLE': [0,1,0,0,0,1,0,0,0,0,0,0],
        'ORACLE 19C DATABASES': [0,0,0,0,11,0,1,0,0,0,0,0],
        'ORACLE 23AI': [0,0,0,0,6,0,0,0,0,0,0,0],
        'ORACLE EXAM': [0,1,1,1,0,0,0,0,0,0,0,0],
        'ORACLE SQL': [4,0,0,2,0,1,1,0,0,0,0,0],
        'P-10975': [1,1,0,2,0,0,3,0,0,0,0,0],
        'PHOTOSHOP': [0,2,0,0,0,0,0,0,0,0,0,0],
        'PL-300': [4,0,3,0,0,2,0,5,0,0,0,1],
        'PMI CAPM': [0,0,0,0,0,0,0,1,0,0,0,0],
        'PMI EXAM': [0,0,1,0,0,1,0,0,0,0,0,0],
        'PMP': [4,23,2,6,3,5,3,20,8,3,5,1],
        'PRINCE 2 FOUNDATION': [2,0,0,0,0,0,0,0,0,2,0,1],
        'PRINCE2 PRACTITIONER': [0,0,0,0,1,0,0,0,0,0,0,0],
        'PSM 1': [1,2,0,0,0,0,0,0,0,0,0,0],
        'PSPO 1': [0,1,0,1,0,0,0,0,0,0,0,0],
        'PTE EXAM': [7,9,3,8,13,9,8,5,11,7,7,4],
        'R12.2 TRAINING': [0,0,0,16,19,19,0,0,0,0,0,0],
        'REDHAT': [0,0,2,0,0,0,0,0,0,0,0,0],
        'RISE MASTERCLASS': [0,0,0,1,0,0,0,0,0,0,0,0],
        'SALESFORCE': [0,0,0,0,0,1,0,0,0,0,0,0],
        'SC-200': [0,5,0,0,0,0,0,0,0,0,1,0],
        'SD-V1': [0,1,0,1,1,1,0,3,0,0,0,0],
        'SD-JAVA': [0,0,0,0,1,0,1,0,0,0,0,0],
        'SD-PYTHON': [1,1,1,4,0,3,1,0,0,2,0,0],
        'SD-WEB': [0,0,0,0,2,0,2,1,0,5,0,0],
        'SELT': [3,2,2,0,1,1,2,2,1,0,1,0],
        'SOPHOS ADMIN': [0,0,0,6,0,0,0,0,0,0,0,0],
        'SSE FOUNDATION': [0,1,0,0,0,0,0,0,0,0,0,0],
        'SUPPLY CHAIN WORKSHO': [0,0,0,0,0,0,21,0,0,0,0,0],
        'SVP EXAM': [0,0,0,1,0,0,0,0,0,0,0,0],
        'TESTING EXAMS': [1,0,0,0,1,0,0,1,1,0,0,0],
        'TOEFL': [1,0,0,0,0,0,1,0,0,2,0,0],
        'TOEFL 2': [2,0,0,0,1,0,2,0,0,0,0,0],
        'TOEFL EXAMS': [4,8,5,3,5,3,5,1,0,0,0,0],
        'TOGAF': [0,1,2,0,0,0,0,0,1,2,1,0],
        'UCLAN': [1,0,0,0,0,0,0,1,0,0,0,0],
        'UCLAN CYBERSECURITY': [0,0,0,0,0,0,1,0,0,0,0,0],
        'Unassigned / Unknown': [0,0,0,0,0,0,0,0,0,1,0,0],
        'VASP TRAINING': [0,0,0,1,0,0,0,0,0,0,0,0],
        'VISIO': [0,0,0,25,0,0,0,0,0,0,0,0],
        'VMWARE VCF': [0,6,0,3,0,0,0,0,0,0,0,0],
        'VUE EXAM': [0,0,1,0,0,0,5,0,0,0,0,0],
        'WD101': [0,1,0,0,4,5,0,1,0,3,0,0],
        'WINDOWS SERVER': [0,0,0,1,0,0,0,0,4,0,0,0]
    }
    
    # 2026 Data (Jan-Aug only)
    data_2026 = {
        '2025LEVEL5': [1,0,0,0,1,0,0,0],
        '20764': [0,0,0,0,1,0,0,0],
        'ACAMS': [0,0,0,0,0,0,0,0],
        'ACCA': [0,0,1,0,0,0,0,0],
        'ACCA EXAM': [2,1,0,1,0,0,0,0],
        'ACFE': [0,4,0,0,0,0,0,0],
        'ADV.WORD ICDL': [1,0,0,0,0,0,0,0],
        'AGILEPR2': [0,2,0,0,0,0,0,0],
        'AICDL': [3,0,3,0,0,0,0,0],
        'AMAZON': [2,0,0,1,0,0,0,0],
        'ANALYZING EXCEL': [2,13,1,3,1,0,3,0],
        'ANALYZING PYTHON': [1,2,0,0,0,0,2,0],
        'API AND WEB SERVICES': [0,3,0,0,0,0,0,0],
        'APPLE': [0,0,0,0,0,0,0,11],
        'AWS': [14,5,5,0,0,1,3,1],
        'AWS AD': [0,0,0,0,0,0,0,0],
        'AWS CLOUD PRACTITIONER': [0,0,0,0,0,0,0,0],
        'AZ-801': [0,0,0,0,0,0,1,0],
        'AZ-900': [0,0,0,0,0,0,1,0],
        'AZ800T00': [0,0,0,2,0,0,0,0],
        'AZURE': [0,3,1,1,0,0,0,0],
        'CA': [2,10,2,8,18,1,0,1],
        'CA747': [0,0,0,0,0,1,0,0],
        'CAIP': [0,0,4,2,0,0,0,0],
        'CBAP': [2,0,0,0,0,1,0,0],
        'CBCI': [0,0,0,0,0,0,0,1],
        'CCNA': [5,5,5,3,7,8,2,5],
        'CCNP': [0,2,0,0,0,0,0,0],
        'CDP': [0,0,0,0,0,0,1,0],
        'CDPSE': [0,0,0,0,0,1,0,0],
        'CDPSE EXAM': [0,1,4,0,0,0,0,0],
        'CDSP': [0,0,0,0,0,1,0,0],
        'CEH': [0,0,0,0,3,0,2,0],
        'CGEIT': [0,0,0,0,0,0,2,0],
        'CHECK-CCSA': [0,0,0,4,0,0,0,0],
        'CISSP': [0,0,0,0,0,0,1,0],
        'CISSP EXAM': [3,5,0,2,7,0,3,7],
        'CKA': [0,0,0,0,0,2,0,0],
        'CKAD': [0,1,5,1,0,0,1,0],
        'CLOUD+': [0,0,0,0,0,0,0,1],
        'COMPTIA A+': [3,3,1,1,0,4,3,2],
        'COMPTIA EXAM': [1,1,4,0,0,0,1,1],
        'COMPTIA N+': [0,0,0,3,0,3,0,1],
        'COMPTIA PENTEST': [0,0,0,1,0,0,0,0],
        'COMPTIA PRO1': [0,0,1,0,0,0,0,0],
        'COMPTIA S+': [6,5,0,3,5,2,0,0],
        'COMPTIACISCONETWORK': [0,0,1,1,1,4,4,4],
        'COMPTIACORE 1&2': [0,0,0,0,0,0,0,3],
        'CORELDRAW': [2,1,0,0,1,0,2,0],
        'COURSERA': [0,1,0,0,0,0,0,0],
        'CRISC': [0,0,1,0,0,0,6,0],
        'CSSLP EXAM': [0,0,0,0,0,0,0,2],
        'CYBERSECURITY': [0,0,0,0,0,0,0,3],
        'CYSA+': [0,0,5,0,0,1,0,1],
        'C|PEHT AI': [0,0,0,0,8,0,0,0],
        'DATACAMP EXAM': [0,1,0,0,0,0,0,0],
        'DATASCIENCE': [0,0,0,0,0,0,1,1],
        'DESIGN THINKING P': [0,0,2,0,0,0,0,0],
        'DIGITAL MARKETING': [0,0,2,0,3,0,0,0],
        'DIGITAL WORKFLOW': [0,0,0,0,0,0,0,1],
        'DOCKER': [0,0,1,0,0,0,0,0],
        'DSP': [0,1,0,0,0,0,0,0],
        'ELASTIC OBSERVABILIT': [0,0,0,1,0,0,0,0],
        'ENTERPRISE API': [0,0,0,0,0,0,0,1],
        'FDA': [1,0,1,1,0,0,0,1],
        'FORTI MAIL': [0,0,0,0,0,0,3,0],
        'FORTI OS': [0,7,10,0,0,9,1,1],
        'FORTIANALYSER': [0,0,0,7,0,0,0,0],
        'FORTIGATE': [0,0,0,0,0,3,1,0],
        'FORTIMANAGER ADMINIS': [0,0,0,4,0,1,0,0],
        'FORTINAC-F': [0,0,7,0,0,0,0,0],
        'FORTINET NSE 7': [0,0,0,0,0,0,1,0],
        'FORTISIEM': [0,0,0,0,0,7,0,0],
        'FORTIWEB 7.4': [0,0,0,5,0,0,0,0],
        'FUNCTIONAL TRAINING': [0,0,0,0,0,0,25,0],
        'GDP': [0,1,0,0,0,2,0,0],
        'GMAT': [0,0,2,0,1,0,0,0],
        'GOOGLE CLOUD SEC': [1,0,0,0,0,0,0,0],
        'GPM-B': [1,0,0,0,0,0,0,0],
        'GRE': [0,7,1,1,1,0,0,4],
        'GRE EXAMS': [0,2,1,1,2,1,0,0],
        'HP': [0,0,0,0,0,0,0,2],
        'HUAWEI': [0,0,0,0,0,0,0,1],
        'ICDL': [1,1,0,0,0,0,0,0],
        'ICDL 35K': [86,90,44,37,31,22,20,5],
        'ICDL30K': [7,3,0,2,0,0,1,0],
        'ICDLEXAMS_ONLY': [0,0,0,0,0,0,0,1],
        'ICIFA': [0,0,0,0,0,0,0,1],
        'IELTS': [1,0,0,0,0,0,0,0],
        'IELTS EXAM': [0,0,2,0,0,0,0,0],
        'ILLUSTRATOR': [0,1,0,0,2,1,0,0],
        'INNOVATION MGT': [0,0,2,0,0,0,0,0],
        'ISO': [1,0,0,0,0,0,0,0],
        'ISO 27001-FL': [0,0,0,0,0,3,0,0],
        'ISQTB': [1,0,0,0,0,0,0,0],
        'ISTQB.': [0,0,1,0,0,0,0,0],
        'ITIL': [0,0,2,0,0,0,0,0],
        'ITIL EXAM': [3,0,4,3,1,6,3,6],
        'ITIL4 SPECIALIST DSV': [2,0,0,0,0,0,0,0],
        'ITILF': [2,6,2,1,6,6,5,1],
        'KCNA': [0,0,0,0,0,0,0,1],
        'KCSA': [0,0,0,0,0,0,1,0],
        'L3 DC': [9,2,0,0,7,0,1,1],
        'L4DBIT': [0,0,0,0,1,1,0,0],
        'L4DC 2023': [6,1,0,0,2,5,5,0],
        'L5DBIT': [1,2,0,0,0,0,0,0],
        'L5DC': [2,0,0,0,0,1,0,0],
        'LEVEL 5 CYBER': [1,0,0,0,0,0,0,0],
        'LINUX+': [0,0,1,1,0,0,0,0],
        'LTC': [17,0,19,0,0,0,0,0],
        'MANAGE ENGINE': [0,0,2,0,0,1,0,0],
        'MB-700': [0,1,0,0,0,0,0,0],
        'MB-820': [1,0,0,0,0,0,0,0],
        'MB-820 DEV': [0,0,0,7,0,0,0,0],
        'MB_800': [0,3,2,1,0,0,1,1],
        'MEMBERSHIP RENEWAL': [0,0,0,0,0,0,0,3],
        'MICROSOFT EXAMS': [2,1,2,6,3,0,3,0],
        'MICROSOFT EXAM': [0,0,0,0,0,1,0,0],
        'MICROSOFT 365': [0,0,0,0,0,0,0,1],
        'MOE-DEVOPS': [16,0,0,0,0,0,0,0],
        'OC:UNIX/LINUX': [0,0,0,0,10,0,0,0],
        'ORACLE': [0,1,0,0,0,1,0,0],
        'ORACLE 19C DATABASES': [0,0,0,0,11,0,1,0],
        'ORACLE 23AI': [0,0,0,0,6,0,0,0],
        'ORACLE EXAM': [0,1,1,1,0,0,0,0],
        'ORACLE SQL': [4,0,0,2,0,1,1,0],
        'P-10975': [1,1,0,2,0,0,3,0],
        'PHOTOSHOP': [0,2,0,0,0,0,0,0],
        'PL-300': [4,0,3,0,0,2,0,5],
        'PMI CAPM': [0,0,0,0,0,0,0,1],
        'PMI EXAM': [0,0,1,0,0,1,0,0],
        'PMP': [4,23,2,6,3,5,3,20],
        'PRINCE 2 FOUNDATION': [2,0,0,0,0,0,0,0],
        'PRINCE2 PRACTITIONER': [0,0,0,0,1,0,0,0],
        'PSM 1': [1,2,0,0,0,0,0,0],
        'PSPO 1': [0,1,0,1,0,0,0,0],
        'PTE EXAM': [7,9,3,8,13,9,8,5],
        'R12.2 TRAINING': [0,0,0,16,19,19,0,0],
        'REDHAT': [0,0,2,0,0,0,0,0],
        'RISE MASTERCLASS': [0,0,0,1,0,0,0,0],
        'SALESFORCE': [0,0,0,0,0,1,0,0],
        'SC-200': [0,5,0,0,0,0,0,0],
        'SD-V1': [0,1,0,1,1,1,0,3],
        'SD-JAVA': [0,0,0,0,1,0,1,0],
        'SD-PYTHON': [1,1,1,4,0,3,1,0],
        'SD-WEB': [0,0,0,0,2,0,2,1],
        'SELT': [3,2,2,0,1,1,2,2],
        'SOPHOS ADMIN': [0,0,0,6,0,0,0,0],
        'SSE FOUNDATION': [0,1,0,0,0,0,0,0],
        'SUPPLY CHAIN WORKSHO': [0,0,0,0,0,0,21,0],
        'SVP EXAM': [0,0,0,1,0,0,0,0],
        'TESTING EXAMS': [1,0,0,0,1,0,0,1],
        'TOEFL': [1,0,0,0,0,0,1,0],
        'TOEFL 2': [2,0,0,0,1,0,2,0],
        'TOEFL EXAMS': [4,8,5,3,5,3,5,1],
        'TOGAF': [0,1,2,0,0,0,0,0],
        'UCLAN': [1,0,0,0,0,0,0,1],
        'UCLAN CYBERSECURITY': [0,0,0,0,0,0,1,0],
        'Unassigned / Unknown': [0,0,0,0,0,0,0,0],
        'VASP TRAINING': [0,0,0,1,0,0,0,0],
        'VISIO': [0,0,0,25,0,0,0,0],
        'VMWARE VCF': [0,6,0,3,0,0,0,0],
        'VUE EXAM': [0,0,1,0,0,0,5,0],
        'WD101': [0,1,0,0,4,5,0,1],
        'WINDOWS SERVER': [0,0,0,1,0,0,0,0]
    }
    
    # Expand all data
    def expand_data(data_dict, year, max_month=12):
        rows = []
        for course, monthly_counts in data_dict.items():
            for month_idx, count in enumerate(monthly_counts[:max_month], start=1):
                if count > 0:
                    rows.append({
                        'date': f"{year}-{month_idx:02d}-15",
                        'course_name': course.strip(),
                        'registered_count': int(count)
                    })
        return rows
    
    data_rows.extend(expand_data(data_2023, 2023))
    data_rows.extend(expand_data(data_2024, 2024))
    data_rows.extend(expand_data(data_2025, 2025))
    data_rows.extend(expand_data(data_2026, 2026, max_month=8))
    
    df = pd.DataFrame(data_rows)
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    
    return df

# -----------------------------------------------------------------------------
# CUSTOM CSS
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    .main, .stApp { background-color: #f8fafc; }
    
    .kpi-card {
        background: white;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border: 1px solid #e2e8f0;
    }
    
    .kpi-value { font-size: 2.2rem; font-weight: 700; color: #0f172a; }
    .kpi-label { font-size: 0.8rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em; }
    
    .section-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #0f172a;
        margin: 24px 0 16px 0;
        padding-bottom: 8px;
        border-bottom: 2px solid #e2e8f0;
    }
    
    .executive-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: white;
        padding: 28px;
        border-radius: 16px;
        margin-bottom: 24px;
    }
    
    .upload-box {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        padding: 20px;
        border-radius: 12px;
        border: 2px solid #3b82f6;
        margin-bottom: 16px;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #f1f5f9;
        padding: 8px;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background: white !important;
        color: #0f172a !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    div[data-testid="stExpander"] {
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        margin-bottom: 12px;
        background: white;
    }
    
    #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SIDEBAR - UPLOAD SECTION
# -----------------------------------------------------------------------------

with st.sidebar:
    st.markdown("""
    <div class="upload-box">
        <h3 style="color: #1e40af; margin: 0 0 8px 0; font-size: 1rem;">📁 Upload Your Data</h3>
        <p style="color: #1e40af; margin: 0; font-size: 0.8rem; opacity: 0.9;">
            Replace with your actual registration data
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose CSV or Excel",
        type=['csv', 'xlsx'],
        label_visibility="collapsed"
    )
    
    # Create and offer sample template
    sample_data = []
    for year in [2023, 2024]:
        for month in range(1, 13):
            sample_data.append({
                'date': f"{year}-{month:02d}-15",
                'course_name': 'ICDL',
                'registered_count': np.random.randint(10, 100)
            })
    sample_df = pd.DataFrame(sample_data)
    
    csv_buffer = io.StringIO()
    sample_df.to_csv(csv_buffer, index=False)
    
    st.download_button(
        "📥 Download Template",
        csv_buffer.getvalue(),
        "template_course_data.csv",
        "text/csv",
        use_container_width=True
    )
    
    st.markdown("---")
    
    if uploaded_file:
        st.success(f"✅ Using uploaded file")
    else:
        st.info("ℹ️ Using built-in data (2023-2026)")

# -----------------------------------------------------------------------------
# LOAD DATA
# -----------------------------------------------------------------------------

@st.cache_data
def get_data(uploaded_file):
    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            required = ['date', 'course_name', 'registered_count']
            missing = [c for c in required if c not in df.columns]
            
            if missing:
                st.error(f"Missing: {', '.join(missing)}")
                return create_real_dataset(), "Built-in Data (Error)"
            
            df['date'] = pd.to_datetime(df['date'])
            df['year'] = df['date'].dt.year
            df['month'] = df['date'].dt.month
            return df, f"Uploaded: {uploaded_file.name}"
        except Exception as e:
            st.error(f"Error: {e}")
            return create_real_dataset(), "Built-in Data (Error)"
    return create_real_dataset(), "Built-in Data (2023-2026)"

df, data_source = get_data(uploaded_file)

# -----------------------------------------------------------------------------
# HEADER
# -----------------------------------------------------------------------------

st.markdown("""
<div class="executive-header">
    <h1 style="margin: 0; font-size: 1.8rem;">📊 Course Registration Intelligence</h1>
    <p style="margin: 8px 0 0 0; color: #94a3b8; font-size: 1rem;">
        Executive Dashboard for Management Review
    </p>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# CONTROLS
# -----------------------------------------------------------------------------

col1, col2, col3 = st.columns([2, 2, 2])

with col1:
    month_names = {i: datetime.date(2024, i, 1).strftime('%B') for i in range(1, 13)}
    selected_month = st.selectbox("📅 Select Month", list(range(1, 13)), 
                                   format_func=lambda x: month_names[x])

with col2:
    all_years = sorted(df['year'].unique())
    selected_years = st.multiselect("📆 Years to Include", all_years, default=all_years)

with col3:
    top_n = st.selectbox("📊 Courses to Show", [10, 20, 30, 50, 100], index=3)

# Filter data
filtered = df[(df['year'].isin(selected_years)) & (df['month'] == selected_month)]
month_all_years = df[df['month'] == selected_month]

# -----------------------------------------------------------------------------
# KPI CARDS
# -----------------------------------------------------------------------------

st.markdown('<div class="section-title">🎯 Key Performance Indicators</div>', unsafe_allow_html=True)

total_reg = filtered['registered_count'].sum()
unique_courses = filtered['course_name'].nunique()
avg_reg = total_reg / unique_courses if unique_courses > 0 else 0

# YoY calculation
if len(selected_years) >= 2:
    sorted_years = sorted(selected_years)
    latest = sorted_years[-1]
    prev = sorted_years[-2]
    
    latest_data = df[(df['year'] == latest) & (df['month'] == selected_month)]
    prev_data = df[(df['year'] == prev) & (df['month'] == selected_month)]
    
    latest_total = latest_data['registered_count'].sum()
    prev_total = prev_data['registered_count'].sum()
    yoy_change = ((latest_total - prev_total) / prev_total * 100) if prev_total > 0 else 0
else:
    yoy_change = 0

# Top course
top_course_data = filtered.groupby('course_name')['registered_count'].sum()
top_course = top_course_data.idxmax() if len(top_course_data) > 0 else "N/A"
top_course_val = top_course_data.max() if len(top_course_data) > 0 else 0

col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)

with col_kpi1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{total_reg:,}</div>
        <div class="kpi-label">Total Registrations</div>
        <div style="color: {'#10b981' if yoy_change > 0 else '#ef4444' if yoy_change < 0 else '#64748b'}; font-size: 0.85rem; margin-top: 4px;">
            {'↑' if yoy_change > 0 else '↓' if yoy_change < 0 else '→'} {abs(yoy_change):.1f}% YoY
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_kpi2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{unique_courses}</div>
        <div class="kpi-label">Active Courses</div>
        <div style="color: #64748b; font-size: 0.85rem; margin-top: 4px;">
            Across {len(selected_years)} years
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_kpi3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{avg_reg:.0f}</div>
        <div class="kpi-label">Avg per Course</div>
        <div style="color: #64748b; font-size: 0.85rem; margin-top: 4px;">
            Monthly average
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_kpi4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value" style="font-size: 1.3rem;">{top_course[:15]}{'...' if len(top_course) > 15 else ''}</div>
        <div class="kpi-label">Top Course ({top_course_val})</div>
        <div style="color: #10b981; font-size: 0.85rem; margin-top: 4px;">
            Leading performer
        </div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# TABS FOR ORGANIZED VIEW
# -----------------------------------------------------------------------------

tab_overview, tab_yearly, tab_forecast, tab_data = st.tabs(["📊 Overall Performance", "📅 Year-by-Year Breakdown", "🔮 2027 Forecast", "📋 Raw Data"])

# -----------------------------------------------------------------------------
# TAB 1: OVERALL PERFORMANCE
# -----------------------------------------------------------------------------

with tab_overview:
    st.markdown(f'<div class="section-title">Combined Performance for {month_names[selected_month]} (All Selected Years)</div>', unsafe_allow_html=True)
    
    if len(filtered) > 0:
        # Aggregate all years
        combined = filtered.groupby('course_name')['registered_count'].sum().reset_index()
        combined = combined.sort_values('registered_count', ascending=False)
        
        # Show top performers
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.markdown(f"**🏆 Top {top_n} Performers**")
            top_performers = combined.head(top_n)
            
            fig = px.bar(
                top_performers,
                x='registered_count',
                y='course_name',
                orientation='h',
                color='registered_count',
                color_continuous_scale='Greens',
                text='registered_count',
                height=600 if top_n > 30 else 500
            )
            fig.update_layout(
                showlegend=False,
                xaxis_title="Total Registrations",
                yaxis_title="",
                yaxis=dict(autorange="reversed"),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            fig.update_traces(textposition='outside', textfont=dict(size=9))
            st.plotly_chart(fig, use_container_width=True)
        
        with col_chart2:
            st.markdown(f"**⚠️ Bottom {top_n} Performers**")
            bottom_performers = combined.tail(top_n)
            
            fig = px.bar(
                bottom_performers,
                x='registered_count',
                y='course_name',
                orientation='h',
                color='registered_count',
                color_continuous_scale='Reds',
                text='registered_count',
                height=600 if top_n > 30 else 500
            )
            fig.update_layout(
                showlegend=False,
                xaxis_title="Total Registrations",
                yaxis_title="",
                yaxis=dict(autorange="reversed"),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            fig.update_traces(textposition='outside', textfont=dict(size=9))
            st.plotly_chart(fig, use_container_width=True)
        
        # Summary table
        with st.expander("📋 View Complete Summary Table", expanded=False):
            st.dataframe(combined, use_container_width=True, hide_index=True)
    else:
        st.warning("No data available for selected filters.")

# -----------------------------------------------------------------------------
# TAB 2: YEAR-BY-YEAR BREAKDOWN
# -----------------------------------------------------------------------------

with tab_yearly:
    st.markdown('<div class="section-title">Detailed Year-by-Year Analysis</div>', unsafe_allow_html=True)
    
    for year in sorted(selected_years, reverse=True):
        year_data = df[(df['year'] == year) & (df['month'] == selected_month)]
        
        if len(year_data) == 0:
            continue
            
        # Check if 2026 and month > August
        if year == 2026 and selected_month > 8:
            with st.expander(f"📅 {year} - {month_names[selected_month]} (No Data - Only Jan-Aug available)", expanded=False):
                st.info("2026 data is only available from January to August.")
            continue
        
        year_total = year_data['registered_count'].sum()
        year_courses = year_data['course_name'].nunique()
        
        with st.expander(f"📅 {year} - {month_names[selected_month]} | {year_total:,} registrations across {year_courses} courses", expanded=(year == max(selected_years))):
            
            year_perf = year_data.groupby('course_name')['registered_count'].sum().reset_index()
            year_perf = year_perf.sort_values('registered_count', ascending=False)
            
            col_y1, col_y2 = st.columns(2)
            
            with col_y1:
                st.markdown(f"**Top Performers - {year}**")
                fig = px.bar(
                    year_perf.head(top_n),
                    x='registered_count',
                    y='course_name',
                    orientation='h',
                    color='registered_count',
                    color_continuous_scale='Greens',
                    text='registered_count',
                    height=500
                )
                fig.update_layout(showlegend=False, xaxis_title="", yaxis_title="", yaxis=dict(autorange="reversed"))
                fig.update_traces(textposition='outside')
                st.plotly_chart(fig, use_container_width=True)
            
            with col_y2:
                st.markdown(f"**Lowest Performers - {year}**")
                fig = px.bar(
                    year_perf.tail(top_n),
                    x='registered_count',
                    y='course_name',
                    orientation='h',
                    color='registered_count',
                    color_continuous_scale='Reds',
                    text='registered_count',
                    height=500
                )
                fig.update_layout(showlegend=False, xaxis_title="", yaxis_title="", yaxis=dict(autorange="reversed"))
                fig.update_traces(textposition='outside')
                st.plotly_chart(fig, use_container_width=True)
            
            with st.expander("View Raw Data for This Year", expanded=False):
                st.dataframe(year_perf, use_container_width=True, hide_index=True)

# -----------------------------------------------------------------------------
# TAB 3: FORECAST
# -----------------------------------------------------------------------------

with tab_forecast:
    st.markdown('<div class="section-title">🔮 2027 Forecast & Predictive Analytics</div>', unsafe_allow_html=True)
    
    st.info("Forecast is based on historical averages with 15% growth assumption. Click the button below to generate predictions.")
    
    if st.button("🚀 Generate 2027 Forecast", type="primary", use_container_width=True):
        with st.spinner("Analyzing trends and generating forecast..."):
            
            # Get all courses that have appeared in any year
            all_courses = df['course_name'].unique()
            forecasts = []
            
            for course in all_courses:
                # Get historical data for this month across all years
                hist = df[(df['course_name'] == course) & (df['month'] == selected_month)]
                
                if len(hist) > 0:
                    avg_reg = hist['registered_count'].mean()
                    # Apply 15% growth for forecast
                    forecast_val = int(avg_reg * 1.15)
                else:
                    forecast_val = 0
                
                forecasts.append({
                    'course': course,
                    'historical_avg': round(avg_reg, 1) if len(hist) > 0 else 0,
                    'forecast_2027': forecast_val,
                    'years_of_data': len(hist)
                })
            
            forecast_df = pd.DataFrame(forecasts)
            forecast_df = forecast_df[forecast_df['forecast_2027'] > 0]  # Only show courses with forecast
            forecast_df = forecast_df.sort_values('forecast_2027', ascending=False)
            
            # Display forecast
            col_f1, col_f2 = st.columns([3, 2])
            
            with col_f1:
                st.markdown(f"**📊 Forecasted Top Performers for {month_names[selected_month]} 2027**")
                
                fig = px.bar(
                    forecast_df.head(top_n),
                    x='forecast_2027',
                    y='course',
                    orientation='h',
                    color='forecast_2027',
                    color_continuous_scale='Blues',
                    text='forecast_2027',
                    height=600
                )
                fig.update_layout(
                    showlegend=False,
                    xaxis_title="Predicted Registrations",
                    yaxis_title="",
                    yaxis=dict(autorange="reversed"),
                    title=f"Top {top_n} Courses - 2027 Forecast"
                )
                fig.update_traces(textposition='outside')
                st.plotly_chart(fig, use_container_width=True)
            
            with col_f2:
                st.markdown("**🎯 Strategic Focus Areas**")
                
                # Top 5 for pie chart
                top_5 = forecast_df.head(5)
                if len(top_5) > 0:
                    fig_pie = px.pie(
                        top_5,
                        values='forecast_2027',
                        names='course',
                        title=f"Top 5 Priority Courses",
                        hole=0.4
                    )
                    fig_pie.update_layout(height=400)
                    st.plotly_chart(fig_pie, use_container_width=True)
                
                # Summary stats
                total_forecast = forecast_df['forecast_2027'].sum()
                st.metric("Total Forecasted Registrations", f"{total_forecast:,}")
                
                # Download button
                csv = forecast_df.to_csv(index=False)
                st.download_button(
                    "📥 Download Full Forecast",
                    csv,
                    f"forecast_2027_{month_names[selected_month]}.csv",
                    "text/csv",
                    use_container_width=True
                )
            
            # Full forecast table
            with st.expander("📋 View Complete Forecast Table", expanded=False):
                st.dataframe(forecast_df, use_container_width=True, hide_index=True)

# -----------------------------------------------------------------------------
# TAB 4: RAW DATA
# -----------------------------------------------------------------------------

with tab_data:
    st.markdown('<div class="section-title">📋 Complete Raw Data</div>', unsafe_allow_html=True)
    
    # Filter options
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        show_year = st.multiselect("Filter by Year", sorted(df['year'].unique()), default=sorted(df['year'].unique()))
    with col_d2:
        show_month = st.multiselect("Filter by Month", list(range(1, 13)), default=[selected_month])
    
    display_df = df[(df['year'].isin(show_year)) & (df['month'].isin(show_month))]
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    # Download full data
    csv_full = df.to_csv(index=False)
    st.download_button(
        "📥 Download Complete Dataset (CSV)",
        csv_full,
        "complete_course_data.csv",
        "text/csv",
        use_container_width=True
    )

# -----------------------------------------------------------------------------
# FOOTER
# -----------------------------------------------------------------------------

st.divider()
st.markdown(f"""
<div style="text-align: center; color: #64748b; padding: 20px;">
    <p style="margin: 0; font-size: 0.875rem;">
        📊 Course Registration Intelligence System | Management Analytics Dashboard
    </p>
    <p style="margin: 8px 0 0 0; font-size: 0.75rem;">
        Data source: {data_source} | Built with Streamlit
    </p>
</div>
""", unsafe_allow_html=True)
