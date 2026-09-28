# ============================================================
# HEART FAILURE ANALYTICS DASHBOARD
# Team 2 - Python Pioneers | Python Hackathon 2026
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

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
# CUSTOM DASHBOARD DESIGN
# ============================================================

st.markdown("""
<style>

/* Main page background */
.stApp {
    background: linear-gradient(
        135deg,
        #f8fbff 0%,
        #eef6ff 50%,
        #fdf7fa 100%
    );
}

/* Main container */
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

/* Sidebar headings */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #ffffff;
}

/* Main dashboard title */
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

/* Section heading */
.section-title {
    font-size: 27px;
    font-weight: 700;
    color: #102a43;
    margin-top: 15px;
    margin-bottom: 5px;
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

/* KPI label */
[data-testid="stMetricLabel"] {
    font-weight: 600;
}

/* KPI value */
[data-testid="stMetricValue"] {
    color: #102a43;
    font-weight: 700;
}

/* Plot containers */
[data-testid="stPlotlyChart"] {
    background: white;
    border-radius: 15px;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border-radius: 12px;
}

/* Horizontal line */
hr {
    border: none;
    height: 1px;
    background-color: #d9e2ec;
    margin-top: 25px;
    margin-bottom: 25px;
}

/* Insight box */
.insight-box {
    background-color: white;
    border-left: 5px solid #3b82f6;
    padding: 16px 20px;
    border-radius: 8px;
    box-shadow: 0 3px 10px rgba(16,42,67,0.06);
    margin-top: 10px;
    margin-bottom: 20px;
}

/* Footer */
.footer {
    text-align: center;
    color: #829ab1;
    padding-top: 30px;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    data = pd.read_csv(
        "Team2_PythonPioneers_Cardiac_Cleaned_Data.csv"
    )

    return data


df = load_data()


# ============================================================
# CONVERT IMPORTANT OUTCOME VARIABLES TO NUMERIC
# ============================================================

numeric_outcomes = [
    "death_within_28_days",
    "death_within_6_months",
    "re_admission_within_28_days",
    "re_admission_within_6_months",
    "return_to_emergency_department_within_6_months"
]

for column in numeric_outcomes:

    if column in df.columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="dashboard-title">'
    '❤️ Heart Failure Analytics Dashboard'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-subtitle">'
    'Team 2 - Python Pioneers | Python Hackathon 2026'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("❤️ Heart Failure")
st.sidebar.caption("Interactive Analytics Dashboard")

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
# FILTERS
# ============================================================

st.sidebar.subheader("Patient Filters")


# ---------------------------
# Gender
# ---------------------------

gender_options = sorted(
    df["gender"]
    .dropna()
    .astype(str)
    .unique()
)

selected_gender = st.sidebar.multiselect(
    "Gender",
    gender_options,
    default=gender_options
)


# ---------------------------
# Age Group
# ---------------------------

age_options = list(
    df["agecat"]
    .dropna()
    .astype(str)
    .unique()
)

selected_age = st.sidebar.multiselect(
    "Age Group",
    age_options,
    default=age_options
)


# ---------------------------
# Admission Type
# ---------------------------

admission_options = sorted(
    df["admission_way"]
    .dropna()
    .astype(str)
    .unique()
)

selected_admission = st.sidebar.multiselect(
    "Admission Type",
    admission_options,
    default=admission_options
)


# ---------------------------
# NYHA
# ---------------------------

nyha_options = sorted(
    df["nyha_cardiac_function_classification"]
    .dropna()
    .unique()
)

selected_nyha = st.sidebar.multiselect(
    "NYHA Class",
    nyha_options,
    default=nyha_options
)


# ---------------------------
# Killip
# ---------------------------

killip_options = sorted(
    df["killip_grade"]
    .dropna()
    .unique()
)

selected_killip = st.sidebar.multiselect(
    "Killip Grade",
    killip_options,
    default=killip_options
)


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
# HANDLE EMPTY FILTER RESULT
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
# OVERVIEW PAGE
# ============================================================

if page == "🏠 Overview":

    st.markdown(
        '<div class="section-title">'
        'Executive Overview'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Key patient outcomes and hospital utilization indicators.'
        '</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # KPI CARDS
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


    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(
        "Patients",
        f"{total_patients:,}"
    )

    c2.metric(
        "28-Day Mortality",
        f"{mortality_28:.1f}%"
    )

    c3.metric(
        "6-Month Mortality",
        f"{mortality_6m:.1f}%"
    )

    c4.metric(
        "6-Month Readmission",
        f"{readmission_6m:.1f}%"
    )

    c5.metric(
        "6-Month ED Return",
        f"{ed_return_6m:.1f}%"
    )


    st.divider()


    # --------------------------------------------------------
    # AGE DISTRIBUTION
    # --------------------------------------------------------

    left, right = st.columns(2)


    with left:

        st.subheader("Patient Distribution by Age")

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

        fig.update_layout(
            showlegend=False,
            height=420
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # --------------------------------------------------------
    # GENDER DISTRIBUTION
    # --------------------------------------------------------

    with right:

        st.subheader("Gender Distribution")

        gender_counts = (
            filtered_df["gender"]
            .value_counts()
            .reset_index()
        )

        gender_counts.columns = [
            "Gender",
            "Patients"
        ]

        fig = px.pie(
            gender_counts,
            names="Gender",
            values="Patients",
            hole=0.45,
            template="plotly_white"
        )

        fig.update_layout(
            height=420
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # --------------------------------------------------------
    # ADMISSION OUTCOMES
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

    fig = px.bar(
        admission_long,
        x="admission_way",
        y="Rate",
        color="Outcome",
        barmode="group",
        text_auto=".1f",
        template="plotly_white"
    )

    fig.update_layout(
        xaxis_title="Admission Type",
        yaxis_title="Rate (%)",
        legend_title="Outcome"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# DESCRIPTIVE ANALYSIS PAGE
# ============================================================

elif page == "📊 Descriptive Analysis":

    st.markdown(
        '<div class="section-title">'
        'Descriptive Analysis'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Explore patient demographics, disease severity, '
        'clinical characteristics and biomarkers.'
        '</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # ROW 1
    # ========================================================

    col1, col2 = st.columns(2)


    # --------------------------------------------------------
    # AGE DISTRIBUTION
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

        fig_age = px.bar(
            age_counts,
            x="Age Group",
            y="Patients",
            text="Patients",
            template="plotly_white"
        )

        st.plotly_chart(
            fig_age,
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

        fig_bmi = px.pie(
            bmi_counts,
            names="BMI Category",
            values="Patients",
            hole=0.4
        )

        st.plotly_chart(
            fig_bmi,
            use_container_width=True
        )


    # ========================================================
    # ROW 2
    # ========================================================

    col3, col4 = st.columns(2)


    # --------------------------------------------------------
    # NYHA
    # --------------------------------------------------------

    with col3:

        st.subheader(
            "6-Month Mortality by NYHA Class"
        )

        nyha = (
            filtered_df
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


    # --------------------------------------------------------
    # KILLIP
    # --------------------------------------------------------

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


    # ========================================================
    # BIOMARKER EXPLORER
    # ========================================================

    st.divider()

    st.subheader("Interactive Biomarker Explorer")

    biomarker_options = {
        "BNP": "brain_natriuretic_peptide",
        "Troponin": "high_sensitivity_troponin",
        "hs-CRP": "hs_crp",
        "Albumin": "albumin",
        "Creatinine": "creatinine_enzymatic_method",
        "GFR": "glomerular_filtration_rate",
        "Sodium": "sodium",
        "LVEF": "lvef"
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

    marker_data[marker_column] = pd.to_numeric(
        marker_data[marker_column],
        errors="coerce"
    )

    marker_data = marker_data.dropna()

    marker_data["6-Month Outcome"] = (
        marker_data["death_within_6_months"]
        .map(
            {
                0: "Survived",
                1: "Died"
            }
        )
    )

    fig_marker = px.box(
        marker_data,
        x="6-Month Outcome",
        y=marker_column,
        points="outliers",
        template="plotly_white"
    )

    fig_marker.update_yaxes(
        title=selected_marker
    )

    st.plotly_chart(
        fig_marker,
        use_container_width=True
    )


# ============================================================
# PRESCRIPTIVE ANALYSIS PAGE
# ============================================================

elif page == "🩺 Prescriptive Analysis":

    st.markdown(
        '<div class="section-title">'
        'Prescriptive Analysis'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Identify patient groups that may benefit from '
        'closer follow-up, discharge planning and '
        'transitional-care support.'
        '</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # EMERGENCY VS NON-EMERGENCY
    # ========================================================

    st.subheader(
        "Emergency vs Non-Emergency Admissions"
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

    admission[
        "Readmission"
    ] *= 100

    admission[
        "Mortality"
    ] *= 100


    a1, a2 = st.columns(2)


    with a1:

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


    with a2:

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

        fig.update_layout(
            xaxis_title="Admission Type",
            yaxis_title="Rate (%)"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # ========================================================
    # DISCHARGE DESTINATION
    # ========================================================

    st.divider()

    st.subheader(
        "Outcomes by Discharge Destination"
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


    # ========================================================
    # FREQUENT RETURNERS
    # ========================================================

    st.divider()

    st.subheader(
        "Hospital Return Profile"
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


    # ========================================================
    # RISK MARKERS
    # ========================================================

    st.divider()

    st.subheader(
        "Clinical Risk Marker Explorer"
    )

    risk_marker_options = {
        "BNP": "brain_natriuretic_peptide",
        "Troponin": "high_sensitivity_troponin",
        "hs-CRP": "hs_crp",
        "Albumin": "albumin",
        "Creatinine": "creatinine_enzymatic_method",
        "GFR": "glomerular_filtration_rate",
        "LVEF": "lvef",
        "Systolic BP": "systolic_blood_pressure",
        "CCI Score": "cci_score"
    }


    risk_marker = st.selectbox(
        "Select Risk Marker",
        list(risk_marker_options.keys())
    )


    risk_column = risk_marker_options[
        risk_marker
    ]


    risk_df = return_data[
        [
            risk_column,
            "Return Status"
        ]
    ].copy()


    risk_df[risk_column] = pd.to_numeric(
        risk_df[risk_column],
        errors="coerce"
    )

    risk_df = risk_df.dropna()


    fig = px.box(
        risk_df,
        x="Return Status",
        y=risk_column,
        points="outliers",
        template="plotly_white"
    )

    fig.update_yaxes(
        title=risk_marker
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# PREDICTIVE ANALYSIS PAGE
# ============================================================

elif page == "🤖 Predictive Analysis":

    st.markdown(
        '<div class="section-title">'
        'Predictive Analysis'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Explore predictors used in the heart-failure '
        'risk models and visualize their relationship '
        'with patient outcomes.'
        '</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # OUTCOME SELECTION
    # ========================================================

    outcome_label = st.selectbox(
        "Select Prediction Outcome",
        [
            "28-Day Mortality",
            "6-Month Mortality",
            "6-Month Readmission",
            "6-Month ED Return"
        ]
    )


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


    selected_outcome = outcome_mapping[
        outcome_label
    ]


    # ========================================================
    # PREDICTOR EXPLORER
    # ========================================================

    predictor_options = {

        "BMI": "bmi",

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


    pred_data[predictor_column] = pd.to_numeric(
        pred_data[predictor_column],
        errors="coerce"
    )


    pred_data[selected_outcome] = pd.to_numeric(
        pred_data[selected_outcome],
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


    # ========================================================
    # PREDICTOR DISTRIBUTION
    # ========================================================

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


    # ========================================================
    # NYHA + KILLIP HEATMAP
    # ========================================================

    st.divider()

    st.subheader(
        "NYHA + Killip Combined Risk View"
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


    st.markdown(
        """
        <div class="insight-box">
        <b>How to interpret this page:</b><br>
        Use the outcome and predictor selectors to explore how
        individual clinical characteristics differ between
        patients with and without the selected outcome.
        The NYHA–Killip heatmap shows the observed outcome rate
        across combinations of heart-failure severity.
        These are exploratory associations and are not a
        substitute for validated clinical prediction models.
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# DATA EXPLORER PAGE
# ============================================================

elif page == "📁 Explore Data":

    st.markdown(
        '<div class="section-title">'
        'Explore Cleaned Dataset'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-description">'
        'Review the patient records included after applying '
        'the selected dashboard filters.'
        '</div>',
        unsafe_allow_html=True
    )


    d1, d2, d3 = st.columns(3)

    d1.metric(
        "Filtered Patients",
        f"{len(filtered_df):,}"
    )

    d2.metric(
        "Dataset Columns",
        len(filtered_df.columns)
    )

    d3.metric(
        "Original Patients",
        f"{len(df):,}"
    )


    st.divider()


    search = st.text_input(
        "Search column name"
    )


    if search:

        selected_columns = [
            column
            for column in filtered_df.columns
            if search.lower() in column.lower()
        ]

        if selected_columns:

            st.dataframe(
                filtered_df[selected_columns],
                use_container_width=True
            )

        else:

            st.info(
                "No column names matched your search."
            )

    else:

        default_columns = [
            "inpatient_number",
            "gender",
            "agecat",
            "admission_way",
            "destinationdischarge",
            "nyha_cardiac_function_classification",
            "killip_grade",
            "bmi",
            "death_within_28_days",
            "death_within_6_months",
            "re_admission_within_6_months",
            "return_to_emergency_department_within_6_months"
        ]

        default_columns = [
            c for c in default_columns
            if c in filtered_df.columns
        ]

        st.dataframe(
            filtered_df[default_columns],
            use_container_width=True
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div class="footer">
    ❤️ Heart Failure Analytics Dashboard<br>
    Team 2 - Python Pioneers | Python Hackathon 2026
    </div>
    """,
    unsafe_allow_html=True
)
