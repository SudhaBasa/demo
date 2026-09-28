import streamlit as st
import pandas as pd
import plotly.express as px

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
# -----------------------------
# DESCRIPTIVE ANALYSIS
# -----------------------------

st.header("Descriptive Analysis")

# Create two columns for charts
chart1, chart2 = st.columns(2)

# Chart 1 - Patients by Age Group
with chart1:
    st.subheader("Patient Distribution by Age Group")

    age_counts = (
        df["agecat"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    age_counts.columns = ["Age Group", "Patients"]

    fig_age = px.bar(
        age_counts,
        x="Age Group",
        y="Patients",
        text="Patients"
    )

    st.plotly_chart(
        fig_age,
        use_container_width=True
    )


# Chart 2 - 6-Month Mortality by NYHA Class
with chart2:
    st.subheader("6-Month Mortality by NYHA Class")

    nyha_mortality = (
        df.groupby(
            "nyha_cardiac_function_classification"
        )["death_within_6_months"]
        .mean()
        .mul(100)
        .reset_index()
    )

    nyha_mortality.columns = [
        "NYHA Class",
        "Mortality Rate"
    ]

    fig_nyha = px.line(
        nyha_mortality,
        x="NYHA Class",
        y="Mortality Rate",
        markers=True
    )

    fig_nyha.update_yaxes(
        title="Mortality Rate (%)"
    )

    st.plotly_chart(
        fig_nyha,
        use_container_width=True
    )
