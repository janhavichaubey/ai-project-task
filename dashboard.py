import streamlit as st
import pandas as pd
from io import StringIO
from back import DataLoader, process_entities  # Assuming back.py is where the backend logic is
import time

# Initialize Streamlit session state variables
if 'data' not in st.session_state:
    st.session_state.data = None
if 'selected_column' not in st.session_state:
    st.session_state.selected_column = None
if 'results' not in st.session_state:
    st.session_state.results = None
if 'processing_done' not in st.session_state:
    st.session_state.processing_done = False  # Track if processing is done

# Title of the Dashboard
st.title("Data Processing Dashboard")

# File Upload Section
st.header("1. File Upload")
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    # Load the file
    st.session_state.data = DataLoader.load_csv(uploaded_file)
    st.write("Data Loaded:")
    st.dataframe(st.session_state.data)
    st.session_state.processing_done = False  # Reset when a new file is uploaded

# Column Selection Section
st.header("2. Select Column for Processing")
if st.session_state.data is not None:
    columns = st.session_state.data.columns.tolist()
    st.session_state.selected_column = st.selectbox("Choose a column", columns)

# Search Query Template Input
st.header("3. Search Query Template")
search_query_template = st.text_input(
    "Enter Search Query (use {entity} as a placeholder for each entity)",
    value="Search information about {entity}"
)

# API Configuration
st.header("4. API Configuration")
search_api_key = st.text_input("Enter Search API Key (SerpAPI)", type="password")
llm_api_key = st.text_input("Enter LLM API Key (Groq)", type="password")  # Update label for Groq API

# When the 'Start Processing' button is pressed
if st.button("Start Processing"):
    if not search_api_key or not llm_api_key:
        st.error("Please provide both API keys")
    elif st.session_state.selected_column is None:
        st.error("Please select a column to process")
    elif not search_query_template:
        st.error("Please provide a valid search query template")
    else:
        try:
            if not st.session_state.processing_done:  # Check if processing has already been done
                with st.spinner('Processing...'):
                    # Processing the data
                    results = process_entities(
                        st.session_state.data, 
                        st.session_state.selected_column, 
                        search_query_template,  # Using the search query template
                        search_api_key,
                        llm_api_key
                    )
                    
                    # Storing results in session state
                    st.session_state.results = pd.DataFrame(results)
                    st.session_state.processing_done = True  # Mark processing as done
                    st.success('Processing completed.')
        except Exception as e:
            st.error(f"Error during processing: {str(e)}")

# Displaying the results after processing
if st.session_state.results is not None:
    st.header("5. Results")
    st.dataframe(st.session_state.results)
