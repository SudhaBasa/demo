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
st.subheader("Dataset Overview")

st.write("Total Patients:", len(df))

st.dataframe(df.head())
