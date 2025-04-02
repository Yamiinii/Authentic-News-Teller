import requests
from bs4 import BeautifulSoup
import serpapi
# from playwright.sync_api import sync_playwright
from google.genai import types
# from langgraph.llms.google import Gemini
from google import genai
import os

from dotenv import load_dotenv
load_dotenv()
# Set your API keys

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "GEMINI-KEY-NOT-FOUND")
SERPAPI_KEY = os.environ.get("SERPAPI", "SERPAPI-KEY-NOT-FOUND")

client = genai.Client(api_key=GEMINI_API_KEY)
clientSerpapi = serpapi.Client(api_key=SERPAPI_KEY)

# 1. Search Google with SerpAPI
def search_query(query):
    params = {
        "q": query,
        "api_key": SERPAPI_KEY,
        "engine": "google"
    }
    response = clientSerpapi.search(params)
    # print(response)
    if "organic_results" in response:
        return response["organic_results"][0]["link"]  # First search result
    return None

# 2. Scrape Website Content
def scrape_website(url):
    # Send a GET request to the website
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the content of the page with BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")
        
        body = soup.find("body")
        
        # Extract all the text from the body content
        content = body.get_text(strip=True)
        
        # Optionally, you can limit the content length (e.g., first 5000 characters)
        return content[:10000]
    
    else:
        print(f"Failed to retrieve content from {url}. Status code: {response.status_code}")
        return None

# 3. Summarize with Google Gemini via Langraph
def summarize_text(text, query):
    prompt=f"""
    Summarize this article on the query - {query}
    Answer: {text}"""
    response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=[prompt],
    config=types.GenerateContentConfig(
    system_instruction="You are a news asistant. Tell me what is the correct answer to the query in the answer text and tell me if is authentic or fake"),
    )

    return response.text

# 4. Main Function
def webAgent(query):
    url = search_query(query)
    
    if not url:
        print("No results found.")
        return "No results found."
    
    print(f"\nScraping: {url}")
    content = scrape_website(url)
    summary = summarize_text(content, query)

    print("\nSummary:")
    print(summary)
    return summary

# if __name__ == "__main__":
#     webAgent("did elon musk sold twitter")