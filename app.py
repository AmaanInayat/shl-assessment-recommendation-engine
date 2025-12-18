import streamlit as st
import requests

API_URL = "https://shl-assessment-recommendation-engine-apii.onrender.com"

st.title("SHL Assessment Recommendation Engine")

st.write(
    "Paste a job description below. The system will recommend relevant SHL assessments."
)

job_description = st.text_area(
    "Job Description",
    height=200,
    placeholder="Paste full job description here..."
)

if st.button("Recommend Assessments"):
    if job_description.strip() == "":
        st.warning("Please paste a job description.")
    else:
        with st.spinner("Analyzing job description..."):
            response = requests.post(
                f"{API_URL}/recommend",
                json={"job_description": job_description},
                timeout=15
            )

            if response.status_code == 200:
                data = response.json()

                if not data:
                    st.info("No assessments found.")
                else:
                    st.subheader("Recommended SHL Assessments")
                
for item in data:
    st.markdown(f"### {item['assessment_name']}")
    st.markdown(f"[Open Assessment]({item['assessment_url']})")
    st.divider()

            else:
                st.error("API returned an error.")
