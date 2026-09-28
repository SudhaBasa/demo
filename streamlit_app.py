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
# -----------------------------
# SIDEBAR FILTERS
# -----------------------------

st.sidebar.header("Filters")

# Gender filter
gender_options = sorted(
    df["gender"].dropna().unique()
)

selected_gender = st.sidebar.multiselect(
    "Gender",
    options=gender_options,
    default=gender_options
)

# Admission Type filter
admission_options = sorted(
    df["admission_way"].dropna().unique()
)

selected_admission = st.sidebar.multiselect(
    "Admission Type",
    options=admission_options,
    default=admission_options
)

# NYHA filter
nyha_options = sorted(
    df["nyha_cardiac_function_classification"]
    .dropna()
    .unique()
)

selected_nyha = st.sidebar.multiselect(
    "NYHA Class",
    options=nyha_options,
    default=nyha_options
)

# Apply filters
filtered_df = df[
    (df["gender"].isin(selected_gender))
    &
    (df["admission_way"].isin(selected_admission))
    &
    (
        df["nyha_cardiac_function_classification"]
        .isin(selected_nyha)
    )
]
# Check that data loaded successfully
# st.subheader("Dataset Overview")

#  st.write("Total Patients:", len(df))

#  st.dataframe(df.head())
# -----------------------------
# DASHBOARD OVERVIEW
# -----------------------------

st.header("Dashboard Overview")

# Calculate KPI values
total_patients = len(filtered_df)

mortality_28 = (
    filtered_df["death_within_28_days"].mean() * 100
)

mortality_6m = (
    filtered_df["death_within_6_months"].mean() * 100
)

readmission_6m = (
    filtered_df["re_admission_within_6_months"].mean() * 100
)

ed_return_6m = (
    filtered_df[
        "return_to_emergency_department_within_6_months"
    ].mean() * 100
)

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
       filtered_df["agecat"]
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
# Chart 2 - 6-Month Mortality by NYHA Class
with chart2:

    st.subheader("6-Month Mortality by NYHA Class")

    # Make sure mortality is numeric
    nyha_data = filtered_df[
        [
            "nyha_cardiac_function_classification",
            "death_within_6_months"
        ]
    ].copy()

    nyha_data["death_within_6_months"] = pd.to_numeric(
        nyha_data["death_within_6_months"],
        errors="coerce"
    )

    # Calculate mortality rate
    nyha_mortality = (
        nyha_data
        .dropna()
        .groupby(
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

    # Create chart
    fig_nyha = px.bar(
        nyha_mortality,
        x="NYHA Class",
        y="Mortality Rate",
        text_auto=".1f"
    )

    fig_nyha.update_yaxes(
        title="6-Month Mortality Rate (%)"
    )

    fig_nyha.update_xaxes(
        title="NYHA Class"
    )

    st.plotly_chart(
        fig_nyha,
        use_container_width=True
    )
