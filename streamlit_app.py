# ============================================================
# HEART FAILURE ANALYTICS DASHBOARD
# Team 2 - Python Pioneers | Python Hackathon 2026
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Heart Failure Analytics",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

/* Main background */
.stApp {
    background: linear-gradient(
        135deg,
        #f8fbff 0%,
        #eef6ff 50%,
        #fdf7fa 100%
    );
}

/* Main page container */
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #102a43 0%,
        #243b53 100%
    );
}

/* Sidebar text */
[data-testid="stSidebar"] * {
    color: white;
}

/* Main title */
.dashboard-title {
    font-size: 42px;
    font-weight: 800;
    color: #102a43;
    margin-bottom: 0px;
}

/* Subtitle */
.dashboard-subtitle {
    font-size: 17px;
    color: #627d98;
    margin-top: 0px;
    margin-bottom: 25px;
}

/* Section titles */
.section-title {
    font-size: 28px;
    font-weight: 700;
    color: #102a43;
    margin-top: 15px;
}

/* Section description */
.section-description {
    color: #627d98;
    font-size: 15px;
    margin-bottom: 20px;
}

/* KPI cards */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.95);
    border: 1px solid #d9e2ec;
    border-radius: 15px;
    padding: 18px 16px;
    box-shadow: 0 4px 12px rgba(16,42,67,0.08);
}

/* KPI value */
[data-testid="stMetricValue"] {
    color: #102a43;
    font-weight: 700;
}

/* Plotly charts */
[data-testid="stPlotlyChart"] {
    background: white;
    border-radius: 15px;
}

/* Footer */
.footer {
    text-align: center;
    color: #829ab1;
    padding-top: 20px;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    return pd.read_csv(
        "Team2_PythonPioneers_Cardiac_Cleaned_Data.csv"
    )


df = load_data()


# ============================================================
# CONVERT OUTCOME COLUMNS TO NUMERIC
# ============================================================

outcome_columns = [
    "death_within_28_days",
    "death_within_6_months",
    "re_admission_within_28_days",
    "re_admission_within_6_months",
    "return_to_emergency_department_within_6_months"
]

for column in outcome_columns:

    if column in df.columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )


# ============================================================
# MAIN HEADER
# ============================================================

st.markdown(
    """
    <div class="dashboard-title">
        ❤️ Heart Failure Analytics Dashboard
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="dashboard-subtitle">
        Team 2 - Python Pioneers | Python Hackathon 2026
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR HEADER
# ============================================================

st.sidebar.title("❤️ Heart Failure")

st.sidebar.caption(
    "Interactive Analytics Dashboard"
)

st.sidebar.divider()


# ============================================================
# NAVIGATION
# ============================================================

page = st.sidebar.radio(
    "Dashboard Section",
    [
        "🏠 Overview",
        "📊 Descriptive Analysis",
        "🩺 Prescriptive Analysis",
        "🤖 Predictive Analysis",
        "📁 Explore Data"
    ]
)

st.sidebar.divider()


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.subheader("Patient Filters")


# ------------------------------------------------------------
# GENDER FILTER
# ------------------------------------------------------------

gender_options = sorted(
    df["gender"]
    .dropna()
    .astype(str)
    .unique()
)

selected_gender = st.sidebar.multiselect(
    "Gender",
    options=gender_options,
    placeholder="All Genders"
)

if not selected_gender:
    selected_gender = gender_options


# ------------------------------------------------------------
# AGE GROUP FILTER
# ------------------------------------------------------------

age_options = list(
    df["agecat"]
    .dropna()
    .astype(str)
    .unique()
)

selected_age = st.sidebar.multiselect(
    "Age Group",
    options=age_options,
    placeholder="All Age Groups"
)

if not selected_age:
    selected_age = age_options


# ------------------------------------------------------------
# ADMISSION TYPE FILTER
# ------------------------------------------------------------

admission_options = sorted(
    df["admission_way"]
    .dropna()
    .astype(str)
    .unique()
)

selected_admission = st.sidebar.multiselect(
    "Admission Type",
    options=admission_options,
    placeholder="All Admission Types"
)

if not selected_admission:
    selected_admission = admission_options


# ------------------------------------------------------------
# NYHA FILTER
# ------------------------------------------------------------

nyha_options = sorted(
    df["nyha_cardiac_function_classification"]
    .dropna()
    .unique()
)

selected_nyha = st.sidebar.multiselect(
    "NYHA Class",
    options=nyha_options,
    placeholder="All NYHA Classes"
)

if not selected_nyha:
    selected_nyha = nyha_options


# ------------------------------------------------------------
# KILLIP FILTER
# ------------------------------------------------------------

killip_options = sorted(
    df["killip_grade"]
    .dropna()
    .unique()
)

selected_killip = st.sidebar.multiselect(
    "Killip Grade",
    options=killip_options,
    placeholder="All Killip Grades"
)

if not selected_killip:
    selected_killip = killip_options


# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df[
    df["gender"].astype(str).isin(selected_gender)
    &
    df["agecat"].astype(str).isin(selected_age)
    &
    df["admission_way"].astype(str).isin(selected_admission)
    &
    df[
        "nyha_cardiac_function_classification"
    ].isin(selected_nyha)
    &
    df["killip_grade"].isin(selected_killip)
].copy()


# ============================================================
# EMPTY FILTER CHECK
# ============================================================

if filtered_df.empty:

    st.warning(
        "No patients match the selected filters. "
        "Please change your filter selections."
    )

    st.stop()


# ============================================================
# HELPER FUNCTION
# ============================================================

def percentage(data, column):

    values = pd.to_numeric(
        data[column],
        errors="coerce"
    )

    if values.notna().sum() == 0:
        return 0

    return values.mean() * 100


# ============================================================
# PAGE 1 — OVERVIEW
# ============================================================

if page == "🏠 Overview":

    st.markdown(
        """
        <div class="section-title">
            Executive Overview
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-description">
            Key patient outcomes and hospital utilization indicators.
        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # KPIs
    # --------------------------------------------------------

    total_patients = len(filtered_df)

    mortality_28 = percentage(
        filtered_df,
        "death_within_28_days"
    )

    mortality_6m = percentage(
        filtered_df,
        "death_within_6_months"
    )

    readmission_6m = percentage(
        filtered_df,
        "re_admission_within_6_months"
    )

    ed_return_6m = percentage(
        filtered_df,
        "return_to_emergency_department_within_6_months"
    )


    k1, k2, k3, k4, k5 = st.columns(5)

    k1.metric(
        "👥 Patients",
        f"{total_patients:,}"
    )

    k2.metric(
        "28-Day Mortality",
        f"{mortality_28:.1f}%"
    )

    k3.metric(
        "6-Month Mortality",
        f"{mortality_6m:.1f}%"
    )

    k4.metric(
        "6-Month Readmission",
        f"{readmission_6m:.1f}%"
    )

    k5.metric(
        "6-Month ED Return",
        f"{ed_return_6m:.1f}%"
    )


    st.divider()


    # --------------------------------------------------------
    # OVERVIEW CHARTS
    # --------------------------------------------------------

    col1, col2 = st.columns(2)


    # AGE DISTRIBUTION
    with col1:

        st.subheader(
            "Patient Distribution by Age"
        )

        age_counts = (
            filtered_df["agecat"]
            .value_counts()
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
            text="Patients",
            template="plotly_white"
        )

        fig_age.update_layout(
            height=420,
            showlegend=False
        )

        st.plotly_chart(
            fig_age,
            use_container_width=True
        )


    # GENDER DISTRIBUTION
    with col2:

        st.subheader(
            "Gender Distribution"
        )

        gender_counts = (
            filtered_df["gender"]
            .value_counts()
            .reset_index()
        )

        gender_counts.columns = [
            "Gender",
            "Patients"
        ]

        fig_gender = px.pie(
            gender_counts,
            names="Gender",
            values="Patients",
            hole=0.45
        )

        fig_gender.update_layout(
            height=420
        )

        st.plotly_chart(
            fig_gender,
            use_container_width=True
        )


    # --------------------------------------------------------
    # OUTCOMES BY ADMISSION TYPE
    # --------------------------------------------------------

    st.subheader(
        "6-Month Outcomes by Admission Type"
    )

    admission_summary = (
        filtered_df
        .groupby("admission_way")
        .agg(
            Readmission=(
                "re_admission_within_6_months",
                "mean"
            ),
            Mortality=(
                "death_within_6_months",
                "mean"
            ),
            ED_Return=(
                "return_to_emergency_department_within_6_months",
                "mean"
            )
        )
        .mul(100)
        .reset_index()
    )

    admission_long = admission_summary.melt(
        id_vars="admission_way",
        var_name="Outcome",
        value_name="Rate"
    )

    fig_admission = px.bar(
        admission_long,
        x="admission_way",
        y="Rate",
        color="Outcome",
        barmode="group",
        text_auto=".1f",
        template="plotly_white"
    )

    fig_admission.update_layout(
        xaxis_title="Admission Type",
        yaxis_title="Rate (%)"
    )

    st.plotly_chart(
        fig_admission,
        use_container_width=True
    )


# ============================================================
# PAGE 2 — DESCRIPTIVE ANALYSIS
# ============================================================

elif page == "📊 Descriptive Analysis":

    st.markdown(
        """
        <div class="section-title">
            Descriptive Analysis
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-description">
            Explore patient demographics, clinical severity,
            nutritional characteristics and biomarkers.
        </div>
        """,
        unsafe_allow_html=True
    )


    col1, col2 = st.columns(2)


    # --------------------------------------------------------
    # AGE GROUP
    # --------------------------------------------------------

    with col1:

        st.subheader(
            "Patient Distribution by Age Group"
        )

        age_counts = (
            filtered_df["agecat"]
            .value_counts()
            .reset_index()
        )

        age_counts.columns = [
            "Age Group",
            "Patients"
        ]

        fig = px.bar(
            age_counts,
            x="Age Group",
            y="Patients",
            text="Patients",
            template="plotly_white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # --------------------------------------------------------
    # BMI
    # --------------------------------------------------------

    with col2:

        st.subheader(
            "BMI Category Distribution"
        )

        bmi_counts = (
            filtered_df["bmi_category"]
            .value_counts()
            .reset_index()
        )

        bmi_counts.columns = [
            "BMI Category",
            "Patients"
        ]

        fig = px.pie(
            bmi_counts,
            names="BMI Category",
            values="Patients",
            hole=0.4
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # --------------------------------------------------------
    # SECOND ROW
    # --------------------------------------------------------

    col3, col4 = st.columns(2)


    # NYHA MORTALITY
    with col3:

        st.subheader(
            "6-Month Mortality by NYHA Class"
        )

        nyha_data = filtered_df[
            [
                "nyha_cardiac_function_classification",
                "death_within_6_months"
            ]
        ].copy()

        nyha_data[
            "death_within_6_months"
        ] = pd.to_numeric(
            nyha_data[
                "death_within_6_months"
            ],
            errors="coerce"
        )

        nyha = (
            nyha_data
            .dropna()
            .groupby(
                "nyha_cardiac_function_classification"
            )["death_within_6_months"]
            .mean()
            .mul(100)
            .reset_index()
        )

        nyha.columns = [
            "NYHA Class",
            "Mortality Rate"
        ]

        fig = px.bar(
            nyha,
            x="NYHA Class",
            y="Mortality Rate",
            text_auto=".1f",
            template="plotly_white"
        )

        fig.update_yaxes(
            title="Mortality Rate (%)"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # KILLIP MORTALITY
    with col4:

        st.subheader(
            "6-Month Mortality by Killip Grade"
        )

        killip = (
            filtered_df
            .groupby("killip_grade")[
                "death_within_6_months"
            ]
            .mean()
            .mul(100)
            .reset_index()
        )

        killip.columns = [
            "Killip Grade",
            "Mortality Rate"
        ]

        fig = px.line(
            killip,
            x="Killip Grade",
            y="Mortality Rate",
            markers=True,
            template="plotly_white"
        )

        fig.update_yaxes(
            title="Mortality Rate (%)"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # --------------------------------------------------------
    # BIOMARKER EXPLORER
    # --------------------------------------------------------

    st.divider()

    st.subheader(
        "🧪 Interactive Biomarker Explorer"
    )

    biomarker_options = {

        "BNP":
            "brain_natriuretic_peptide",

        "Troponin":
            "high_sensitivity_troponin",

        "hs-CRP":
            "hs_crp",

        "Albumin":
            "albumin",

        "Creatinine":
            "creatinine_enzymatic_method",

        "GFR":
            "glomerular_filtration_rate",

        "Sodium":
            "sodium",

        "LVEF":
            "lvef"
    }

    selected_marker = st.selectbox(
        "Select Biomarker",
        list(biomarker_options.keys())
    )

    marker_column = biomarker_options[
        selected_marker
    ]

    marker_data = filtered_df[
        [
            marker_column,
            "death_within_6_months"
        ]
    ].copy()

    marker_data[
        marker_column
    ] = pd.to_numeric(
        marker_data[
            marker_column
        ],
        errors="coerce"
    )

    marker_data = marker_data.dropna()

    marker_data[
        "6-Month Outcome"
    ] = marker_data[
        "death_within_6_months"
    ].map(
        {
            0: "Survived",
            1: "Died"
        }
    )

    fig = px.box(
        marker_data,
        x="6-Month Outcome",
        y=marker_column,
        points="outliers",
        template="plotly_white"
    )

    fig.update_yaxes(
        title=selected_marker
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# PAGE 3 — PRESCRIPTIVE ANALYSIS
# ============================================================

elif page == "🩺 Prescriptive Analysis":

    st.markdown(
        """
        <div class="section-title">
            Prescriptive Analysis
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-description">
            Identify patient groups associated with
            readmission, mortality, emergency return and
            hospital utilization.
        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # EMERGENCY VS NON-EMERGENCY
    # --------------------------------------------------------

    st.subheader(
        "🚑 Emergency vs Non-Emergency Admissions"
    )

    admission = (
        filtered_df
        .groupby("admission_way")
        .agg(
            Patients=(
                "admission_way",
                "size"
            ),
            Average_Stay=(
                "dischargeday",
                "mean"
            ),
            Readmission=(
                "re_admission_within_6_months",
                "mean"
            ),
            Mortality=(
                "death_within_6_months",
                "mean"
            )
        )
        .reset_index()
    )

    admission["Readmission"] *= 100
    admission["Mortality"] *= 100


    col1, col2 = st.columns(2)


    with col1:

        fig = px.bar(
            admission,
            x="admission_way",
            y="Average_Stay",
            text_auto=".1f",
            template="plotly_white"
        )

        fig.update_layout(
            xaxis_title="Admission Type",
            yaxis_title="Average Length of Stay"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    with col2:

        outcome_long = admission.melt(
            id_vars="admission_way",
            value_vars=[
                "Readmission",
                "Mortality"
            ],
            var_name="Outcome",
            value_name="Rate"
        )

        fig = px.bar(
            outcome_long,
            x="admission_way",
            y="Rate",
            color="Outcome",
            barmode="group",
            text_auto=".1f",
            template="plotly_white"
        )

        fig.update_yaxes(
            title="Rate (%)"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # --------------------------------------------------------
    # DISCHARGE DESTINATION
    # --------------------------------------------------------

    st.divider()

    st.subheader(
        "🏥 Outcomes by Discharge Destination"
    )

    destination = (
        filtered_df
        .groupby("destinationdischarge")
        .agg(
            Patients=(
                "destinationdischarge",
                "size"
            ),
            Readmission=(
                "re_admission_within_6_months",
                "mean"
            ),
            ED_Return=(
                "return_to_emergency_department_within_6_months",
                "mean"
            )
        )
        .reset_index()
    )

    destination[
        "Readmission"
    ] *= 100

    destination[
        "ED_Return"
    ] *= 100

    destination_long = destination.melt(
        id_vars=[
            "destinationdischarge",
            "Patients"
        ],
        value_vars=[
            "Readmission",
            "ED_Return"
        ],
        var_name="Outcome",
        value_name="Rate"
    )

    fig = px.bar(
        destination_long,
        x="destinationdischarge",
        y="Rate",
        color="Outcome",
        barmode="group",
        text_auto=".1f",
        template="plotly_white"
    )

    fig.update_layout(
        xaxis_title="Discharge Destination",
        yaxis_title="Rate (%)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # --------------------------------------------------------
    # RETURN PROFILE
    # --------------------------------------------------------

    st.divider()

    st.subheader(
        "🔁 Hospital Return Profile"
    )

    return_data = filtered_df.copy()

    return_data[
        "Return Status"
    ] = np.where(
        (
            return_data[
                "re_admission_within_6_months"
            ] == 1
        )
        |
        (
            return_data[
                "return_to_emergency_department_within_6_months"
            ] == 1
        ),
        "Returned within 6 months",
        "No recorded return"
    )

    return_summary = (
        return_data[
            "Return Status"
        ]
        .value_counts()
        .reset_index()
    )

    return_summary.columns = [
        "Return Status",
        "Patients"
    ]

    fig = px.pie(
        return_summary,
        names="Return Status",
        values="Patients",
        hole=0.5
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# PAGE 4 — PREDICTIVE ANALYSIS
# ============================================================

elif page == "🤖 Predictive Analysis":

    st.markdown(
        """
        <div class="section-title">
            Predictive Analysis
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-description">
            Explore relationships between important predictors
            and heart-failure outcomes.
        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # OUTCOME SELECTOR
    # --------------------------------------------------------

    outcome_mapping = {

        "28-Day Mortality":
            "death_within_28_days",

        "6-Month Mortality":
            "death_within_6_months",

        "6-Month Readmission":
            "re_admission_within_6_months",

        "6-Month ED Return":
            "return_to_emergency_department_within_6_months"
    }

    outcome_label = st.selectbox(
        "Select Prediction Outcome",
        list(outcome_mapping.keys())
    )

    selected_outcome = outcome_mapping[
        outcome_label
    ]


    # --------------------------------------------------------
    # PREDICTOR SELECTOR
    # --------------------------------------------------------

    predictor_options = {

        "BMI":
            "bmi",

        "NYHA Class":
            "nyha_cardiac_function_classification",

        "Killip Grade":
            "killip_grade",

        "BNP":
            "brain_natriuretic_peptide",

        "Troponin":
            "high_sensitivity_troponin",

        "hs-CRP":
            "hs_crp",

        "Albumin":
            "albumin",

        "Creatinine":
            "creatinine_enzymatic_method",

        "GFR":
            "glomerular_filtration_rate",

        "LVEF":
            "lvef",

        "CCI Score":
            "cci_score",

        "Systolic BP":
            "systolic_blood_pressure",

        "Pulse":
            "pulse",

        "Total Drugs":
            "total_drugs"
    }

    selected_predictor = st.selectbox(
        "Select Predictor",
        list(predictor_options.keys())
    )

    predictor_column = predictor_options[
        selected_predictor
    ]


    pred_data = filtered_df[
        [
            predictor_column,
            selected_outcome
        ]
    ].copy()

    pred_data[
        predictor_column
    ] = pd.to_numeric(
        pred_data[
            predictor_column
        ],
        errors="coerce"
    )

    pred_data[
        selected_outcome
    ] = pd.to_numeric(
        pred_data[
            selected_outcome
        ],
        errors="coerce"
    )

    pred_data = pred_data.dropna()

    pred_data[
        "Outcome"
    ] = pred_data[
        selected_outcome
    ].map(
        {
            0: "No",
            1: "Yes"
        }
    )


    st.subheader(
        f"{selected_predictor} vs {outcome_label}"
    )

    fig = px.violin(
        pred_data,
        x="Outcome",
        y=predictor_column,
        box=True,
        points="outliers",
        template="plotly_white"
    )

    fig.update_yaxes(
        title=selected_predictor
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # --------------------------------------------------------
    # NYHA + KILLIP RISK VIEW
    # --------------------------------------------------------

    st.divider()

    st.subheader(
        "🔥 NYHA + Killip Combined Risk View"
    )

    severity = (
        filtered_df
        .groupby(
            [
                "nyha_cardiac_function_classification",
                "killip_grade"
            ]
        )[selected_outcome]
        .mean()
        .mul(100)
        .reset_index()
    )

    severity_matrix = severity.pivot(
        index="nyha_cardiac_function_classification",
        columns="killip_grade",
        values=selected_outcome
    )

    fig = px.imshow(
        severity_matrix,
        text_auto=".1f",
        aspect="auto",
        labels={
            "x": "Killip Grade",
            "y": "NYHA Class",
            "color": "Outcome Rate (%)"
        }
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.info(
        "These charts show exploratory relationships between "
        "predictors and outcomes. They should not be interpreted "
        "as validated clinical prediction tools."
    )


# ============================================================
# PAGE 5 — EXPLORE DATA
# ============================================================

elif page == "📁 Explore Data":

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    st.markdown(
        """
        <div style="
            background:linear-gradient(90deg,#12355b,#2f6690);
            padding:24px 30px;
            border-radius:18px;
            margin-bottom:25px;
            box-shadow:0 6px 18px rgba(0,0,0,0.10);
        ">
            <h2 style="color:white;margin:0;">
                📁 Patient Data Explorer
            </h2>

            <div style="
                color:#e8f1f8;
                margin-top:8px;
                font-size:16px;
            ">
                Explore demographic, clinical, biomarker and outcome
                information for the selected patient population.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # SUMMARY KPIs
    # --------------------------------------------------------

    filtered_count = len(filtered_df)
    original_count = len(df)
    dataset_columns = len(df.columns)

    cohort_percentage = (
        filtered_count /
        original_count *
        100
    )

    d1, d2, d3, d4 = st.columns(4)

    d1.metric(
        "👥 Filtered Patients",
        f"{filtered_count:,}"
    )

    d2.metric(
        "🗂️ Dataset Variables",
        f"{dataset_columns:,}"
    )

    d3.metric(
        "🏥 Original Cohort",
        f"{original_count:,}"
    )

    d4.metric(
        "📊 Cohort Selected",
        f"{cohort_percentage:.1f}%"
    )


    st.markdown("<br>", unsafe_allow_html=True)


    # --------------------------------------------------------
    # BUILD PATIENT VIEW HEADER
    # --------------------------------------------------------

    st.markdown(
        """
        <div style="
            background:white;
            padding:18px 22px;
            border-radius:14px;
            border:1px solid #d9e2ec;
            margin-top:20px;
            margin-bottom:15px;
            box-shadow:0 3px 10px rgba(16,42,67,0.05);
        ">

            <h3 style="
                color:#102a43;
                margin:0;
            ">
                🔎 Build Your Patient View
            </h3>

            <div style="
                color:#627d98;
                margin-top:6px;
            ">
                Select variables from the categories below
                to customize the patient table.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # COLUMN GROUPS
    # --------------------------------------------------------

    demographic_columns = {

        "Patient Number":
            "inpatient_number",

        "Gender":
            "gender",

        "Age Group":
            "agecat",

        "BMI":
            "bmi",

        "BMI Category":
            "bmi_category"
    }


    clinical_columns = {

        "Admission Type":
            "admission_way",

        "Discharge Destination":
            "destinationdischarge",

        "NYHA Class":
            "nyha_cardiac_function_classification",

        "Killip Grade":
            "killip_grade",

        "Systolic BP":
            "systolic_blood_pressure",

        "Pulse":
            "pulse",

        "LVEF":
            "lvef",

        "CCI Score":
            "cci_score"
    }


    biomarker_columns = {

        "BNP":
            "brain_natriuretic_peptide",

        "Troponin":
            "high_sensitivity_troponin",

        "hs-CRP":
            "hs_crp",

        "Albumin":
            "albumin",

        "Creatinine":
            "creatinine_enzymatic_method",

        "GFR":
            "glomerular_filtration_rate",

        "Sodium":
            "sodium"
    }


    patient_outcome_columns = {

        "28-Day Mortality":
            "death_within_28_days",

        "6-Month Mortality":
            "death_within_6_months",

        "28-Day Readmission":
            "re_admission_within_28_days",

        "6-Month Readmission":
            "re_admission_within_6_months",

        "6-Month ED Return":
            "return_to_emergency_department_within_6_months"
    }


    # --------------------------------------------------------
    # TABS
    # --------------------------------------------------------

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "👤 Demographics",
            "🩺 Clinical",
            "🧪 Biomarkers",
            "📈 Outcomes"
        ]
    )


    with tab1:

        selected_demo = st.multiselect(
            "Select demographic variables",
            options=list(
                demographic_columns.keys()
            ),
            default=[
                "Patient Number",
                "Gender",
                "Age Group",
                "BMI"
            ],
            key="demo_columns"
        )


    with tab2:

        selected_clinical = st.multiselect(
            "Select clinical variables",
            options=list(
                clinical_columns.keys()
            ),
            default=[
                "Admission Type",
                "NYHA Class",
                "Killip Grade"
            ],
            key="clinical_columns"
        )


    with tab3:

        selected_biomarkers = st.multiselect(
            "Select biomarker variables",
            options=list(
                biomarker_columns.keys()
            ),
            default=[],
            key="biomarker_columns"
        )


    with tab4:

        selected_outcomes = st.multiselect(
            "Select outcome variables",
            options=list(
                patient_outcome_columns.keys()
            ),
            default=[
                "6-Month Mortality",
                "6-Month Readmission"
            ],
            key="outcome_columns"
        )


    # --------------------------------------------------------
    # COMBINE SELECTED COLUMNS
    # --------------------------------------------------------

    selected_friendly_names = (
        selected_demo
        +
        selected_clinical
        +
        selected_biomarkers
        +
        selected_outcomes
    )


    all_column_options = {}

    all_column_options.update(
        demographic_columns
    )

    all_column_options.update(
        clinical_columns
    )

    all_column_options.update(
        biomarker_columns
    )

    all_column_options.update(
        patient_outcome_columns
    )


    selected_actual_columns = [

        all_column_options[name]

        for name in selected_friendly_names

        if (
            name in all_column_options
            and
            all_column_options[name]
            in filtered_df.columns
        )
    ]


    # --------------------------------------------------------
    # PATIENT RECORDS
    # --------------------------------------------------------

    st.divider()

    st.subheader(
        "🏥 Patient Records"
    )


    if selected_actual_columns:

        display_df = filtered_df[
            selected_actual_columns
        ].copy()


        # Rename technical names
        reverse_names = {

            value: key

            for key, value
            in all_column_options.items()
        }


        display_df = display_df.rename(
            columns=reverse_names
        )


        # Patient summary
        st.info(
            f"{len(display_df):,} patients are currently "
            f"displayed using {len(display_df.columns)} "
            f"selected variables."
        )


        # Table
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            height=500
        )


        # ----------------------------------------------------
        # DOWNLOAD SELECTED DATA
        # ----------------------------------------------------

        csv = display_df.to_csv(
            index=False
        ).encode("utf-8")


        st.download_button(
            label="⬇️ Download Selected Patient Data",
            data=csv,
            file_name="heart_failure_patient_data.csv",
            mime="text/csv"
        )


    else:

        st.info(
            "Select at least one variable from the "
            "categories above to display patient data."
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div class="footer">
        ❤️ Heart Failure Analytics Dashboard
        <br>
        Team 2 - Python Pioneers | Python Hackathon 2026
    </div>
    """,
    unsafe_allow_html=True
)
