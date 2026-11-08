
import streamlit as st
from agent import analyze_opportunity

# Configure the browser page
st.set_page_config(
    page_title="Enterprise Opportunity Intelligence",
    page_icon="🤖",
    layout="wide"
)

# Application heading
st.title("Enterprise Opportunity Intelligence Agent")

st.write(
    "Analyze customer business challenges and "
    "identify potential technology opportunities."
)

# Example requirement
sample_requirement = """
We operate 120 commercial buildings worldwide.
Our maintenance operations are reactive.
Equipment failures are increasing.
We want to explore AI-driven predictive maintenance.
"""

# Remember the latest assessment
if "assessment" not in st.session_state:
    st.session_state.assessment = None

# Customer input form
with st.form("opportunity_form"):

    requirement = st.text_area(
        "Describe the customer's business requirements",
        value=sample_requirement,
        height=180
    )

    submitted = st.form_submit_button(
        "Analyze Opportunity",
        type="primary"
    )

# Process the submitted requirement
if submitted:

    st.session_state.assessment = None

    if not requirement.strip():
        st.warning("Please enter customer requirements.")

    else:
        try:
            with st.spinner("Analyzing opportunity..."):
                st.session_state.assessment = (
                    analyze_opportunity(requirement)
                )

        except Exception as error:
            st.error("Analysis failed. Check the terminal.")
            print(f"Analysis error: {error}")

# Display the assessment
assessment = st.session_state.assessment

if assessment is not None:

    st.divider()
    st.header("Opportunity Assessment")

    st.subheader("Customer Summary")
    st.write(assessment.customer_summary)

    st.subheader("Known Facts")
    for fact in assessment.known_facts:
        st.write(f"- {fact}")

    st.subheader("Assumptions")
    for assumption in assessment.assumptions:
        st.write(f"- {assumption}")

    st.subheader("Identified Opportunities")

    for index, opportunity in enumerate(
        assessment.opportunities, start=1
    ):
        with st.expander(
            f"{index}. {opportunity.title}",
            expanded=True
        ):
            st.markdown("**Business Problem**")
            st.write(opportunity.business_problem)

            st.markdown("**Proposed Solution**")
            st.write(opportunity.proposed_solution)

            st.markdown("**Expected Business Value**")
            st.write(opportunity.expected_business_value)

            st.markdown("**Supporting Facts**")
            for fact in opportunity.supporting_facts:
                st.write(f"- {fact}")

    st.subheader("Discovery Questions")
    for question in assessment.discovery_questions:
        st.write(f"- {question}")

    st.subheader("Recommended Next Step")
    st.write(assessment.recommended_next_step)

    # Convert assessment into JSON
    json_output = assessment.model_dump_json(indent=2)

    # Allow the user to download the result
    st.download_button(
        label="Download Assessment (JSON)",
        data=json_output,
        file_name="opportunity_assessment.json",
        mime="application/json"
    )