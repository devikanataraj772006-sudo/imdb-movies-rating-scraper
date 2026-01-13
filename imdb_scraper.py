from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import json
import pandas as pd
import time

options = Options()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

driver.get("https://www.imdb.com/chart/top/")
time.sleep(6)

# ---------------- Get JSON data ----------------
script_tag = driver.find_element(
    By.XPATH, "//script[@type='application/ld+json']"
)

json_text = script_tag.get_attribute("innerHTML")
data = json.loads(json_text)

movies = []

for index, item in enumerate(data["itemListElement"], start=1):
    movies.append({
        "Rank": index,
        "Movie Name": item["item"]["name"],
        "IMDb Rating": item["item"]["aggregateRating"]["ratingValue"]
    })

df = pd.DataFrame(movies)
df.to_csv("imdb_top_250_movies.csv", index=False, encoding="utf-8")

driver.quit()
print("✅ IMDb Top 250 movies saved successfully!")
print("Movies scraped:", len(df))
print(df.head())
