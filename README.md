# Data Processing Dashboard
The Data Processing Dashboard is a versatile web-based tool designed to process and retrieve entity-specific information from datasets. This application enables users to upload data files or connect to Google Sheets, perform automated web searches for specific columns, and use Large Language Models (LLMs) to extract meaningful insights from search results. The processed data can be reviewed, downloaded, or updated in real time.
_______________________________________
# Project summary
The dashboard simplifies data enrichment and automation for users handling tabular data. Users can:
•	Upload data in CSV format or fetch data directly from Google Sheets.
•	Define query templates for automated web searches via APIs (like SerpAPI).
•	Leverage LLMs (e.g., via Groq API) to parse results and extract actionable information.
•	View, manage, and export enriched data for downstream applications.

# Setup Instruction
Prerequisites
•	Python: Version 3.8 or higher.
•	Streamlit: For the frontend interface.
•	API Keys:
o	SerpAPI: For web search capabilities.
o	Groq API: For LLM-powered data extraction.
•	Google Sheets API Credentials: For real-time data integration.

Set up Google Sheets integration:
o	Download Google Sheets API credentials JSON file.
o	Save the file in the project directory and update the GOOGLE_CREDENTIALS_PATH in back.py.
Add your API keys:
o	Replace placeholders in config.py with your SerpAPI and Groq API keys.
________________________________________
# Usage Guide
Step 1: Start the Application
Run the dashboard using Streamlit:

_streamlit run main.py_

Step 2: Upload or Connect to Data
•	Upload File: Drag and drop a CSV file into the dashboard.
•	Connect to Google Sheets: Authenticate using your Google account and select a sheet.
Step 3: Configure Query Template
Specify a query format (e.g., “Find headquarters of {entity}”). Use {entity} as a placeholder for column values.
Step 4: Process Data
•	Start processing to:
1.	Fetch web search results for each entry.
2.	Pass the results through the LLM for parsing.
3.	Display the enriched data.
Step 5: Review and Export
•	Review results in the dashboard.
•	Export data as a CSV file or update the connected Google Sheet.
________________________________________
# Third-Party APIs and Tools
1. SerpAPI
•	Used for executing web searches based on user-defined queries.
•	Documentation: SerpAPI Documentation
2. Groq API
•	Powers the LLM functionality to extract targeted insights from search results.
•	Documentation: Groq API
3. Google Sheets API
•	Provides seamless integration for importing/exporting data with Google Sheets.
•	Documentation: Google Sheets API
