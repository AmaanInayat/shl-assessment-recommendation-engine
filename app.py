import streamlit as st
import requests

# ===============================
# API CONFIG
# ===============================
API_URL = "https://shl-assessment-recommendation-engine-apii.onrender.com"

# ===============================
# PAGE UI
# ===============================
st.title("SHL Assessment Recommendation Engine")

st.write(
    "Enter a job role. The system will fetch relevant SHL assessments "
    "from the recommendation API."
)

job_role = st.text_input("Job Role (e.g. Developer, Manager, Analyst)")

# ===============================
# API CALL
# ===============================
if st.button("Recommend Assessments"):
    if job_role.strip() == "":
        st.warning("Please enter a job role.")
    else:
        with st.spinner("Fetching recommendations..."):
            try:
                response = requests.get(
                    f"{API_URL}/recommend",
                    params={"job_role": job_role},
                    timeout=10
                )

                if response.status_code == 200:
                    data = response.json()

                    if len(data) == 0:
                        st.info("No assessments found for this job role.")
                    else:
                        st.subheader("Recommended SHL Assessments")

                        for item in data:
                            st.markdown(f"### {item.get('Assessment_Name', 'N/A')}")
                            st.markdown(
                                f"[Open Assessment]({item.get('Assessment_URL', '#')})"
                            )
                            st.divider()

                else:
                    st.error("API returned an error.")

            except Exception as e:
                st.error("Unable to connect to the API.")
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
