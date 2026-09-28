import streamlit as st
import pandas as pd

# Page settings
st.set_page_config(
    page_title="Heart Failure Analytics",
    page_icon="❤️",
    layout="wide"
)

# Dashboard title
st.title("❤️ Heart Failure Analytics Dashboard")

st.write("Team 2 - Python Pioneers | Python Hackathon 2026")
# Load cleaned dataset
df = pd.read_csv(
    "Team2_PythonPioneers_Cardiac_Cleaned_Data.csv"
)

# Check that data loaded successfully
# st.subheader("Dataset Overview")

#  st.write("Total Patients:", len(df))

#  st.dataframe(df.head())
# -----------------------------
# DASHBOARD OVERVIEW
# -----------------------------

st.header("Dashboard Overview")

# Calculate KPI values
total_patients = len(df)

mortality_28 = df["death_within_28_days"].mean() * 100

mortality_6m = df["death_within_6_months"].mean() * 100

readmission_6m = (
    df["re_admission_within_6_months"].mean() * 100
)

ed_return_6m = (
    df["return_to_emergency_department_within_6_months"].mean() * 100
)

# Create KPI cards
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Total Patients",
    f"{total_patients:,}"
)

col2.metric(
    "28-Day Mortality",
    f"{mortality_28:.1f}%"
)

col3.metric(
    "6-Month Mortality",
    f"{mortality_6m:.1f}%"
)

col4.metric(
    "6-Month Readmission",
    f"{readmission_6m:.1f}%"
)

col5.metric(
    "6-Month ED Return",
    f"{ed_return_6m:.1f}%"
)
