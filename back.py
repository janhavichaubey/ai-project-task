
import requests
import pandas as pd
import time
from typing import List, Dict

class DataLoader:
    @staticmethod
    def load_csv(file) -> pd.DataFrame:
        import chardet
        try:
            result = chardet.detect(file.read(10000))  # Detect encoding
            encoding = result['encoding']
            file.seek(0)
            return pd.read_csv(file, encoding=encoding)
        except UnicodeDecodeError:
            file.seek(0)  # Fall back to latin-1
            return pd.read_csv(file, encoding='latin-1')

    @staticmethod
    def load_google_sheet(sheet_id: str, credentials: str) -> pd.DataFrame:
        import gspread
        from oauth2client.service_account import ServiceAccountCredentials

        # Authenticate with Google Sheets API
        scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials, scope)
        client = gspread.authorize(creds)
        
        # Fetch the Google Sheet by its ID
        sheet = client.open_by_key(sheet_id)
        worksheet = sheet.get_worksheet(0)  # Get the first sheet
        data = worksheet.get_all_records()  # Fetch all records
        return pd.DataFrame(data)

class WebSearcher:
    def __init__(self, api_key: str):
        self.api_key = api_key
        
    def search(self, query: str) -> List[Dict]:
        url = "https://serpapi.com/search"
        params = {
            "api_key": self.api_key,
            "q": query,
            "engine": "google"
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            results = response.json()
            return results.get('organic_results', [])
        except Exception as e:
            raise Exception(f"Search error: {str(e)}")

class LLMProcessor:
    def __init__(self, api_key: str):
        self.api_key = api_key
        # self.groq_url = "https://api.groq.com/openai/v1/completions"
        self.groq_url = "https://api.groq.com/openai/v1/chat/completions"
    
    def process_results(self, search_results: List[Dict], prompt: str) -> str:
        formatted_results = "\n".join([ 
            f"Title: {result.get('title', '')}\nSnippet: {result.get('snippet', '')}\nLink: {result.get('link', '')}"
            for result in search_results[:3]  # Limit to top 3 results
        ])
        
        try:
            # Send request to Groq API
            data = {
                "model": "gemma2-9b-it",  # Replace with the actual Groq model
                # "prompt": f"{prompt}\n\nSearch Results:\n{formatted_results}",
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": f"{prompt}\n\nSearch Results:\n{formatted_results}"}
                ],
                "max_tokens": 150  # Adjust based on Groq API capabilities
            }
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(self.groq_url, json=data, headers=headers)
            response.raise_for_status()
            generated_text = response.json().get('text', 'No response text')
            
            return generated_text
        except Exception as e:
            raise Exception(f"LLM processing error with Groq API: {str(e)}")

def process_entities(data: pd.DataFrame, column: str, query_template: str, search_api_key: str, llm_api_key: str):
    searcher = WebSearcher(search_api_key)
    llm_processor = LLMProcessor(llm_api_key)
    results = []
    
    for idx, entity in enumerate(data[column]):
        query = query_template.replace("{entity}", str(entity))
        
        # Perform search
        search_results = searcher.search(query)
        
        # Process with LLM (Groq API)
        extracted_info = llm_processor.process_results(
            search_results,
            f"Extract information about {entity} based on: {query}"
        )
        
        results.append({
            "Entity": entity,
            "Extracted Information": extracted_info
        })
        
        time.sleep(1)  # Rate limiting
        
    return results
