#Have to work on this idea

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Authenticate with Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("your_credentials.json", scope)
client = gspread.authorize(creds)

# Open Google Sheet (replace with your sheet name)
sheet = client.open("News Data").sheet1

# Convert DataFrame to list of lists
data = new_df.values.tolist()
sheet.append_rows(data)

print("News data updated in Google Sheets!")
