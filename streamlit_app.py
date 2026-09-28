import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="Heart Failure Analytics",
    page_icon="❤️",
    layout="wide"
)

# =========================================================
# LOAD DATA
# =========================================================

df = pd.read_csv(
    "Team2_PythonPioneers_Cardiac_Cleaned_Data.csv"
)

# =========================================================
# DASHBOARD TITLE
# =========================================================

st.title("❤️ Heart Failure Analytics Dashboard")

st.write(
    "Team 2 - Python Pioneers | Python Hackathon 2026"
)

# =========================================================
# SIDEBAR FILTERS
# =========================================================

st.sidebar.header("Filters")


# -----------------------------
# Gender Filter
# -----------------------------

gender_options = sorted(
    df["gender"]
    .dropna()
    .unique()
)

selected_gender = st.sidebar.multiselect(
    "Gender",
    options=gender_options,
    default=gender_options
)


# -----------------------------
# Admission Type Filter
# -----------------------------

admission_options = sorted(
    df["admission_way"]
    .dropna()
    .unique()
)

selected_admission = st.sidebar.multiselect(
    "Admission Type",
    options=admission_options,
    default=admission_options
)


# -----------------------------
# NYHA Filter
# -----------------------------

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


# =========================================================
# APPLY FILTERS
# =========================================================

filtered_df = df[
    (df["gender"].isin(selected_gender))
    &
    (df["admission_way"].isin(selected_admission))
    &
    (
        df["nyha_cardiac_function_classification"]
        .isin(selected_nyha)
    )
].copy()


# =========================================================
# NAVIGATION
# =========================================================

st.sidebar.divider()

st.sidebar.header("Analysis")

page = st.sidebar.radio(
    "Select Page",
    [
        "Overview",
        "Descriptive Analysis",
        "Prescriptive Analysis",
        "Predictive Analysis"
    ]
)


# =========================================================
# CHECK FILTER RESULTS
# =========================================================

if filtered_df.empty:

    st.warning(
        "No patients match the selected filters. "
        "Please change the filter selections."
    )

    st.stop()


# =========================================================
# PAGE 1 - OVERVIEW
# =========================================================

if page == "Overview":

    st.header("Dashboard Overview")

    # -----------------------------
    # Calculate KPI Values
    # -----------------------------

    total_patients = len(filtered_df)

    mortality_28 = (
        filtered_df[
            "death_within_28_days"
        ].mean() * 100
    )

    mortality_6m = (
        filtered_df[
            "death_within_6_months"
        ].mean() * 100
    )

    readmission_6m = (
        filtered_df[
            "re_admission_within_6_months"
        ].mean() * 100
    )

    ed_return_6m = (
        filtered_df[
            "return_to_emergency_department_within_6_months"
        ].mean() * 100
    )


    # -----------------------------
    # KPI Cards
    # -----------------------------

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
    # Small Overview Message
    # -----------------------------

    st.info(
        "Use the filters in the sidebar to explore "
        "patient outcomes for different groups."
    )


# =========================================================
# PAGE 2 - DESCRIPTIVE ANALYSIS
# =========================================================

elif page == "Descriptive Analysis":

    st.header("Descriptive Analysis")

    st.write(
        "Explore patient demographics and "
        "heart-failure severity."
    )


    # Create two chart columns
    chart1, chart2 = st.columns(2)


    # -----------------------------------------------------
    # CHART 1 - AGE GROUP
    # -----------------------------------------------------

    with chart1:

        st.subheader(
            "Patient Distribution by Age Group"
        )

        age_counts = (
            filtered_df["agecat"]
            .value_counts()
            .sort_index()
            .reset_index()
        )

        age_counts.columns = [
            "Age Group",
            "Patients"
        ]

        fig_age = px.bar(
            age_counts,
            x="Age Group",
            y="Patients",
            text="Patients"
        )

        fig_age.update_layout(
            xaxis_title="Age Group",
            yaxis_title="Number of Patients"
        )

        st.plotly_chart(
            fig_age,
            use_container_width=True
        )


    # -----------------------------------------------------
    # CHART 2 - NYHA MORTALITY
    # -----------------------------------------------------

    with chart2:

        st.subheader(
            "6-Month Mortality by NYHA Class"
        )

        nyha_data = filtered_df[
            [
                "nyha_cardiac_function_classification",
                "death_within_6_months"
            ]
        ].copy()


        # Convert mortality to numeric
        nyha_data[
            "death_within_6_months"
        ] = pd.to_numeric(
            nyha_data[
                "death_within_6_months"
            ],
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


        fig_nyha.update_layout(
            xaxis_title="NYHA Class",
            yaxis_title="6-Month Mortality Rate (%)"
        )


        st.plotly_chart(
            fig_nyha,
            use_container_width=True
        )


# =========================================================
# PAGE 3 - PRESCRIPTIVE ANALYSIS
# =========================================================

elif page == "Prescriptive Analysis":

    st.header("Prescriptive Analysis")

    st.write(
        "Explore patient groups associated with "
        "readmission, mortality, emergency return "
        "and hospital utilization."
    )

    st.info(
        "Prescriptive analysis visualizations "
        "will be added in the next step."
    )


# =========================================================
# PAGE 4 - PREDICTIVE ANALYSIS
# =========================================================

elif page == "Predictive Analysis":

    st.header("Predictive Analysis")

    st.write(
        "Explore predictive models for mortality, "
        "readmission and other patient outcomes."
    )

    st.info(
        "Predictive analysis model results "
        "will be added after the prescriptive section."
    )
