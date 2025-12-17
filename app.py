import streamlit as st
import pandas as pd

# Page title
st.title("SHL Assessment Recommendation Engine")

st.write(
    "Paste a job description below. The system will recommend relevant SHL assessments based on keyword matching."
)

# Job Description input
job_description = st.text_area("Job Description", height=200)

# Load SHL assessment data
@st.cache_data
def load_data():
    return pd.read_excel("shl_individual_assessments.xlsx")

df = load_data()

# Recommend button
if st.button("Recommend Assessments"):
    if job_description.strip() == "":
        st.warning("Please paste a job description.")
    else:
        jd_words = job_description.lower().split()

        # Simple keyword matching
        def is_relevant(name):
            name = name.lower()
            return any(word in name for word in jd_words)

        filtered_df = df[df["Assessment_Name"].apply(is_relevant)]

        # If no match found, show fallback
        if filtered_df.empty:
            st.info(
                "No strong keyword match found. Showing general recommended assessments."
            )
            filtered_df = df.head(10)
        else:
            filtered_df = filtered_df.head(10)

        st.subheader("Recommended SHL Assessments")
        st.dataframe(
            filtered_df[["Assessment_Name", "Assessment_URL"]],
            use_container_width=True
        )
