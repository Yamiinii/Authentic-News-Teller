import requests
import pandas as pd
import os
import time
from dotenv import load_dotenv
import logging
import gspread
from oauth2client.service_account import ServiceAccountCredentials
load_dotenv()

API_KEY = os.environ.get("API_KEY", "KEY_INVALID")

URL = "https://newsapi.org/v2/top-headlines"

# EXCEL_PATH = "./data/all_news.xlsx" 

# CREDENTIALS_FILE = os.environ.get("CREDENTIALS_FILE", "FILE_NOT_FOUND")
CREDENTIALS_FILE = "pathway-rag-166d1aa63a1c.json"

# Google Sheets authentication
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
client = gspread.authorize(creds)

# Google Sheet ID
SHEET_ID = os.environ.get("SHEET_ID", "SHEETID_NOT_FOUND") # Replace with your actual Sheet ID

logging.basicConfig(
    # filename="news_fetch.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

params = {
    "apiKey": API_KEY,
    "language":"en",
}

while True:
    response = requests.get(URL, params=params)
    news_data = response.json()

    if response.status_code != 200:
        print(f"Error: {news_data.get('status', 'Failed to fetch news')}")
        logging.error(f"API Error: {news_data.get('message', 'Failed to fetch news')}")
    else:
        articles = news_data.get("articles", [])
        sheet = client.open_by_key(SHEET_ID).sheet1
        if articles:
            new_df = pd.DataFrame([
                {
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
            new_df["content"] = new_df.apply(
                lambda x: f"{x['Title']}. {x['Description']}. Read more at {x['URL']}. Published on {x['Published At']} by {x['Source']}.",
                axis=1
            )

            new_df = new_df[["Content", "URL"]]
            data = sheet.get_all_records()
            old_df = pd.DataFrame(data)

            updated_df = pd.concat([old_df, new_df]).drop_duplicates(subset=["URL"], keep="last")

            # Convert DataFrame to list format for Google Sheets
            sheet_data = [updated_df.columns.tolist()] + updated_df.values.tolist()
            # Update Google Sheet
            sheet.clear()
            sheet.update(sheet_data)
            logging.info(f"Total Unique Articles in Sheet: {len(updated_df)}")

        else:
            print("No new articles fetched.")
            logging.warning("No new articles fetched.")
            # logging.warning("No new articles fetched.")

    print("Waiting for 10 minutes before the next API call...")
    logging.info("Waiting for 10 minutes before the next API call...")
    time.sleep(600)
