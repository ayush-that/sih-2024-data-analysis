import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime


def scrape_sih_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        print(f"Successfully fetched data from {url}")
        soup = BeautifulSoup(response.text, "html.parser")

        states = []
        cities = []

        rows = soup.find_all("tr", class_=lambda x: x and x.startswith("row"))
        print(f"Found {len(rows)} rows")

        for row in rows:
            state = row.find("td", class_="column10 style2 s")
            city = row.find("td", class_="column9 style2 s")

            if state and city:
                states.append(state.text.strip())
                cities.append(city.text.strip())
            else:
                print("State or City not found in a row")

        if not states or not cities:
            print("No data extracted. Check the HTML structure.")
            return None

        df = pd.DataFrame({"State": states, "City": cities})
        df.to_csv("sih_data.csv", index=False)
        df.to_json("sih_data.json", orient="records")

        return df

    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None


def main():
    urls = [
        "https://www.sih.gov.in/screeningresult",
        "https://www.sih.gov.in/screeningresult_batch_two",
        "https://sih.gov.in/screeningresult_batch_three",
    ]

    all_data = []

    for url in urls:
        print(f"Starting data scraping for {url}...")
        df = scrape_sih_data(url)
        if df is not None:
            all_data.append(df)

    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        combined_df.to_csv("combined_sih_data.csv", index=False)
        combined_df.to_json("combined_sih_data.json", orient="records")
        print("\nData scraping successful!")
        print("\nShape of combined data:", combined_df.shape)
        print("\nFirst few rows:")
        print(combined_df.head())
    else:
        print("No data scraped from any URL.")


if __name__ == "__main__":
    main()
