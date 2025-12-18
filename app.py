import streamlit as st
import requests

API_URL = "https://shl-assessment-recommendation-engine-apii.onrender.com"

st.title("SHL Assessment Recommendation Engine")

st.write("Enter a job role to get relevant SHL assessments.")

job_role = st.text_input("Job Role (e.g. Developer, Manager, Analyst)")

if st.button("Recommend Assessments"):
    if job_role.strip() == "":
        st.warning("Please enter a job role.")
    else:
        st.info("Fetching recommendations...")

        response = requests.get(
            f"{API_URL}/recommend",
            params={"job_role": job_role}
        )

        if response.status_code == 200:
            data = response.json()

            if not data:
                st.info("No assessments found.")
            else:
                st.subheader("Recommended Assessments")
                for item in data:
                    st.markdown(f"### {item['Assessment_Name']}")
                    st.markdown(f"[Open Assessment]({item['Assessment_URL']})")
                    st.divider()
        else:
            st.error("API returned an error.")
