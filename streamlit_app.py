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
        #eef6ff 55%,
        #fdf7fa 100%
    );
}

/* Main content */
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
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: white !important;
}

/* KPI cards */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.96);
    border: 1px solid #d9e2ec;
    border-radius: 15px;
    padding: 18px 16px;
    box-shadow: 0 4px 12px rgba(16,42,67,0.08);
}

/* KPI values */
[data-testid="stMetricValue"] {
    color: #102a43;
    font-weight: 700;
}

/* KPI labels */
[data-testid="stMetricLabel"] {
    color: #334e68;
}

/* Tabs */
button[data-baseweb="tab"] {
    font-size: 15px;
    font-weight: 600;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    background: white;
    border-radius: 12px;
}

/* Download button */
.stDownloadButton button {
    border-radius: 10px;
    font-weight: 600;
}

/* Footer */
.footer-text {
    text-align: center;
    color: #829ab1;
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

outcome_cols = [
    "death_within_28_days",
    "death_within_6_months",
    "re_admission_within_28_days",
    "re_admission_within_6_months",
    "return_to_emergency_department_within_6_months"
]

for col in outcome_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )


# ============================================================
# MAIN DASHBOARD HEADER
# ============================================================

st.title("❤️ Heart Failure Analytics Dashboard")

st.caption(
    "Team 2 - Python Pioneers | Python Hackathon 2026"
)


# ============================================================
# SIDEBAR
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
# PATIENT FILTERS
# ============================================================

st.sidebar.subheader("Patient Filters")


# Gender
gender_options = sorted(
    df["gender"]
    .dropna()
    .astype(str)
    .unique()
)

selected_gender = st.sidebar.multiselect(
    "Gender",
    gender_options,
    placeholder="All Genders"
)

if not selected_gender:
    selected_gender = gender_options


# Age Group
age_options = list(
    df["agecat"]
    .dropna()
    .astype(str)
    .unique()
)

selected_age = st.sidebar.multiselect(
    "Age Group",
    age_options,
    placeholder="All Age Groups"
)

if not selected_age:
    selected_age = age_options


# Admission Type
admission_options = sorted(
    df["admission_way"]
    .dropna()
    .astype(str)
    .unique()
)

selected_admission = st.sidebar.multiselect(
    "Admission Type",
    admission_options,
    placeholder="All Admission Types"
)

if not selected_admission:
    selected_admission = admission_options


# NYHA
nyha_options = sorted(
    df[
        "nyha_cardiac_function_classification"
    ]
    .dropna()
    .unique()
)

selected_nyha = st.sidebar.multiselect(
    "NYHA Class",
    nyha_options,
    placeholder="All NYHA Classes"
)

if not selected_nyha:
    selected_nyha = nyha_options


# Killip
killip_options = sorted(
    df["killip_grade"]
    .dropna()
    .unique()
)

selected_killip = st.sidebar.multiselect(
    "Killip Grade",
    killip_options,
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
    df["admission_way"].astype(str).isin(
        selected_admission
    )
    &
    df[
        "nyha_cardiac_function_classification"
    ].isin(selected_nyha)
    &
    df["killip_grade"].isin(selected_killip)
].copy()


if filtered_df.empty:
    st.warning(
        "No patients match the selected filters. "
        "Please change the filter selections."
    )
    st.stop()


# ============================================================
# HELPER FUNCTION
# ============================================================

def get_percentage(data, column):

    if column not in data.columns:
        return 0

    values = pd.to_numeric(
        data[column],
        errors="coerce"
    )

    if values.notna().sum() == 0:
        return 0

    return values.mean() * 100


# ============================================================
# OVERVIEW
# ============================================================

if page == "🏠 Overview":

    st.header("Executive Overview")

    st.caption(
        "Key patient outcomes and hospital utilization indicators."
    )

    total_patients = len(filtered_df)

    mortality_28 = get_percentage(
        filtered_df,
        "death_within_28_days"
    )

    mortality_6m = get_percentage(
        filtered_df,
        "death_within_6_months"
    )

    readmission_6m = get_percentage(
        filtered_df,
        "re_admission_within_6_months"
    )

    ed_return_6m = get_percentage(
        filtered_df,
        "return_to_emergency_department_within_6_months"
    )


    # KPI CARDS
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
    # AGE AND GENDER
    # --------------------------------------------------------

    col1, col2 = st.columns(2)


    with col1:

        st.subheader(
            "👥 Patient Distribution by Age"
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


    with col2:

        st.subheader(
            "👤 Gender Distribution"
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
    # ADMISSION OUTCOMES
    # --------------------------------------------------------

    st.subheader(
        "🏥 6-Month Outcomes by Admission Type"
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
# DESCRIPTIVE ANALYSIS
# ============================================================

elif page == "📊 Descriptive Analysis":

    st.header("📊 Descriptive Analysis")

    st.caption(
        "Explore patient demographics, clinical severity, "
        "nutritional characteristics and biomarkers."
    )


    col1, col2 = st.columns(2)


    # --------------------------------------------------------
    # AGE
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

        if "bmi_category" in filtered_df.columns:

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

        fig = px.bar(
            nyha_mortality,
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


    with col4:

        st.subheader(
            "6-Month Mortality by Killip Grade"
        )

        killip_data = (
            filtered_df
            .groupby("killip_grade")[
                "death_within_6_months"
            ]
            .mean()
            .mul(100)
            .reset_index()
        )

        killip_data.columns = [
            "Killip Grade",
            "Mortality Rate"
        ]

        fig = px.line(
            killip_data,
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

    available_biomarkers = {
        label: column
        for label, column
        in biomarker_options.items()
        if column in filtered_df.columns
    }

    if available_biomarkers:

        selected_marker = st.selectbox(
            "Select Biomarker",
            list(
                available_biomarkers.keys()
            )
        )

        marker_column = available_biomarkers[
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
# PRESCRIPTIVE ANALYSIS
# ============================================================

elif page == "🩺 Prescriptive Analysis":

    st.header("🩺 Prescriptive Analysis")

    st.caption(
        "Explore patient groups associated with "
        "readmission, mortality, emergency return and "
        "hospital utilization."
    )


    # --------------------------------------------------------
    # ADMISSION TYPE
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

    destination["Readmission"] *= 100
    destination["ED_Return"] *= 100

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
# PREDICTIVE ANALYSIS
# ============================================================

elif page == "🤖 Predictive Analysis":

    st.header("🤖 Predictive Analysis")

    st.caption(
        "Explore relationships between important predictors "
        "and heart-failure outcomes."
    )


    # --------------------------------------------------------
    # OUTCOME
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
    # PREDICTOR
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

    available_predictors = {
        label: column
        for label, column
        in predictor_options.items()
        if column in filtered_df.columns
    }

    selected_predictor = st.selectbox(
        "Select Predictor",
        list(
            available_predictors.keys()
        )
    )

    predictor_column = available_predictors[
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

    pred_data["Outcome"] = pred_data[
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
    # NYHA + KILLIP HEATMAP
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
        "These visualizations show exploratory relationships "
        "between predictors and outcomes. They are not validated "
        "clinical prediction tools."
    )


# ============================================================
# EXPLORE DATA
# ============================================================

elif page == "📁 Explore Data":

    # ========================================================
    # HEADER — NATIVE STREAMLIT, NO CUSTOM HTML
    # ========================================================

    st.header("📁 Patient Data Explorer")

    st.caption(
        "Explore demographic, clinical, biomarker and outcome "
        "information for the selected patient population."
    )


    # ========================================================
    # SUMMARY
    # ========================================================

    filtered_count = len(filtered_df)
    original_count = len(df)
    dataset_columns = len(df.columns)

    cohort_percentage = (
        filtered_count / original_count * 100
        if original_count > 0
        else 0
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


    st.divider()


    # ========================================================
    # BUILD PATIENT VIEW
    # ========================================================

    st.subheader(
        "🔎 Build Your Patient View"
    )

    st.caption(
        "Select variables from the categories below "
        "to customize the patient table."
    )


    # ========================================================
    # COLUMN GROUPS
    # ========================================================

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


    # Remove options not present in dataset
    demographic_columns = {
        k: v
        for k, v in demographic_columns.items()
        if v in filtered_df.columns
    }

    clinical_columns = {
        k: v
        for k, v in clinical_columns.items()
        if v in filtered_df.columns
    }

    biomarker_columns = {
        k: v
        for k, v in biomarker_columns.items()
        if v in filtered_df.columns
    }

    patient_outcome_columns = {
        k: v
        for k, v in patient_outcome_columns.items()
        if v in filtered_df.columns
    }


    # ========================================================
    # CATEGORY TABS
    # ========================================================

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "👤 Demographics",
            "🩺 Clinical",
            "🧪 Biomarkers",
            "📈 Outcomes"
        ]
    )


    # --------------------------------------------------------
    # DEMOGRAPHICS
    # --------------------------------------------------------

    with tab1:

        default_demo = [
            x
            for x in [
                "Patient Number",
                "Gender",
                "Age Group",
                "BMI"
            ]
            if x in demographic_columns
        ]

        selected_demo = st.multiselect(
            "Select demographic variables",
            options=list(
                demographic_columns.keys()
            ),
            default=default_demo,
            key="demo_columns"
        )


    # --------------------------------------------------------
    # CLINICAL
    # --------------------------------------------------------

    with tab2:

        default_clinical = [
            x
            for x in [
                "Admission Type",
                "NYHA Class",
                "Killip Grade"
            ]
            if x in clinical_columns
        ]

        selected_clinical = st.multiselect(
            "Select clinical variables",
            options=list(
                clinical_columns.keys()
            ),
            default=default_clinical,
            key="clinical_columns"
        )


    # --------------------------------------------------------
    # BIOMARKERS
    # --------------------------------------------------------

    with tab3:

        selected_biomarkers = st.multiselect(
            "Select biomarker variables",
            options=list(
                biomarker_columns.keys()
            ),
            default=[],
            key="biomarker_columns"
        )


    # --------------------------------------------------------
    # OUTCOMES
    # --------------------------------------------------------

    with tab4:

        default_outcomes = [
            x
            for x in [
                "6-Month Mortality",
                "6-Month Readmission"
            ]
            if x in patient_outcome_columns
        ]

        selected_outcomes = st.multiselect(
            "Select outcome variables",
            options=list(
                patient_outcome_columns.keys()
            ),
            default=default_outcomes,
            key="outcome_columns"
        )


    # ========================================================
    # COMBINE ALL AVAILABLE COLUMN OPTIONS
    # ========================================================

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


    selected_friendly_names = (
        selected_demo
        +
        selected_clinical
        +
        selected_biomarkers
        +
        selected_outcomes
    )


    selected_actual_columns = [
        all_column_options[name]
        for name in selected_friendly_names
        if name in all_column_options
    ]


    # ========================================================
    # PATIENT RECORDS
    # ========================================================

    st.divider()

    st.subheader(
        "🏥 Patient Records"
    )


    if selected_actual_columns:

        display_df = filtered_df[
            selected_actual_columns
        ].copy()


        # Rename technical dataset names
        reverse_names = {
            value: key
            for key, value
            in all_column_options.items()
        }


        display_df = display_df.rename(
            columns=reverse_names
        )


        # ----------------------------------------------------
        # RECORD SUMMARY
        # ----------------------------------------------------

        r1, r2 = st.columns(2)

        r1.metric(
            "Patients Displayed",
            f"{len(display_df):,}"
        )

        r2.metric(
            "Variables Selected",
            len(display_df.columns)
        )


        # ----------------------------------------------------
        # DATA TABLE
        # ----------------------------------------------------

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
            height=500
        )


        # ----------------------------------------------------
        # DOWNLOAD
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
            "👆 Select at least one variable from "
            "Demographics, Clinical, Biomarkers or Outcomes."
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "❤️ Heart Failure Analytics Dashboard | "
    "Team 2 - Python Pioneers | Python Hackathon 2026"
)
