import requests
import pandas as pd
import os

API_KEY = "ee60b81c1d764f93b501aa421f1256bb"  # Replace with your API key
URL = "https://newsapi.org/v2/top-headlines"

# ✅ Change these values when needed
country = "us"         # Example: "us", "in", "gb"
category = "business"  # Example: "sports", "technology", "business"

EXCEL_PATH = "all_news.xlsx"  # Single file for all news

params = {
    "country": country,
    "category": category,
    "apiKey": API_KEY,
    "pageSize": 100  # ✅ Max limit for free accounts
}

response = requests.get(URL, params=params)
news_data = response.json()

if response.status_code != 200:
    print(f"Error: {news_data.get('message', 'Failed to fetch news')}")
    exit()

articles = news_data.get("articles", [])

if not articles:
    print("No new articles fetched. Exiting.")
    exit()

# Convert to DataFrame
new_df = pd.DataFrame([
    {
        "Country": country,
        "Category": category,
        "Author": article.get("author"),
        "Title": article.get("title"),
        "Source": article.get("source", {}).get("name"),
        "URL": article.get("url"),
        "Description": article.get("description"),
        "Published At": article.get("publishedAt"),
        "Content": article.get("content")
    }
    for article in articles
])

# Load existing data if the file exists
if os.path.exists(EXCEL_PATH):
    old_df = pd.read_excel(EXCEL_PATH)
    combined_df = pd.concat([old_df, new_df]).drop_duplicates(subset=["Title", "URL"], keep="last")
else:
    combined_df = new_df

# Save to Excel
combined_df.to_excel(EXCEL_PATH, index=False, engine="openpyxl")

print(f"News data saved to {EXCEL_PATH} with {len(combined_df)} unique articles.")
