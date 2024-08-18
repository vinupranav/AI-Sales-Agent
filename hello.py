import streamlit as st
import logging
from main import main

# Set page configuration
st.set_page_config(
    page_title="AI-Powered Lead Generation",
    page_icon="🚀",
    layout="wide",
)

# Custom CSS
st.markdown("""
    <style>
    body {
        background-color: #f8f9fa;
        color: #333;
    }
    .reportview-container {
        background: #ffffff;
        border-radius: 8px;
        padding: 2rem;
    }
    h1 {
        color: #333;
        font-family: 'Arial', sans-serif;
        font-weight: 700;
    }
    .stButton>button {
        background-color: #007bff;
        color: white;
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 12px;
    }
    .stButton>button:hover {
        background-color: #0056b3;
    }
    .lead-output {
        font-size: 18px;
        color: #007bff;
        margin-top: 2rem;
    }
    .status {
        font-size: 16px;
        color: #333;
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# App title
st.title("🚀 AI-Powered Lead Generation")

# App description
st.write("""
    Welcome to the AI-Powered Lead Generation tool. Input your custom prompt and click the button below to initiate the lead generation process. The process may take a few moments, so please be patient.
""")

# Prompt input
user_prompt = st.text_area("Enter your custom prompt for the AI to personalize messages:",
                           placeholder="E.g., Please focus on the lead's industry and recent achievements...")

# HubSpot URL (Replace with your actual URL if needed)
hubspot_url = ""

# Create a button to start processing
if st.button("Generate Leads"):
    st.write("Processing, please wait...")

    # Show a spinner while processing
    with st.spinner("Running the lead generation process..."):
        try:
            # Pass the custom prompt to the main function
            main(user_prompt)

            st.success("Lead generation completed successfully!")

            # Provide a link to view leads in HubSpot
            st.write(
                "The lead generation process has been completed. You can now view the updated leads and personalized messages in HubSpot.")
            st.markdown(f"[Click here to view the updated leads in HubSpot]({hubspot_url})")

        except Exception as e:
            # Log and display error messages
            logging.error(f"An error occurred: {e}")
            st.error(f"An error occurred: {e}")

else:
    st.write("Click the button above to start generating leads.")

# Footer
st.markdown("""
    <hr>
    <footer>
        <p style="text-align:center; font-size:0.875em;">&copy; 2024 AI Sales Lead Generation. All rights reserved.</p>
    </footer>
""", unsafe_allow_html=True)
