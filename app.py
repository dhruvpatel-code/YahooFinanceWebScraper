import os
from bs4 import BeautifulSoup
import pandas as pd
from requests_html import HTMLSession

# define headers for requests
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

def scrape_yahoo_stocks(session, category_url):
    response = session.get(category_url, headers=HEADERS)
    response.raise_for_status()  # raise exception if invalid response
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")
    rows = table.find_all("tr")

    data = []
    for row in rows[1:]:
        cols = row.find_all("td")
        cols = [col.text.strip() for col in cols]
        data.append(cols)

    return data

def fetch_stock_details(session, stock_url):
    response = session.get(stock_url, headers=HEADERS)

    # Render the JavaScript
    response.html.render()

    soup = BeautifulSoup(response.html.html, "html.parser")
    summary_table = soup.find("table", {"class": "W(100%)"})

    # Check if the table is found
    if summary_table is None:
        return {}

    summary_table_rows = summary_table.find_all("tr")
    summary_data = {}
    for row in summary_table_rows:
        try:
            key, value = [col.text for col in row.find_all("td")]
            summary_data[key] = value
        except ValueError:
            pass

    return summary_data

def clean_data(df):
    df['Price (Intraday)'] = df['Price (Intraday)'].str.replace(',', '').astype(float)
    df['Change'] = df['Change'].str.replace(',', '').astype(float)

    # Remove commas and spaces from the 'Volume' and 'Market Cap' columns
    df['Volume'] = df['Volume'].str.replace(',', '').str.replace(' ', '')
    df['Market Cap'] = df['Market Cap'].str.replace(',', '').str.replace(' ', '')

    # Replace 'K', 'M', 'B' and 'T' with the corresponding multiplier, then evaluate each string
    df['Volume'] = df['Volume'].replace({'K': '*1e3', 'M': '*1e6', 'B': '*1e9', 'T': '*1e12'}, regex=True)
    df['Market Cap'] = df['Market Cap'].replace({'K': '*1e3', 'M': '*1e6', 'B': '*1e9', 'T': '*1e12'}, regex=True)

    # Check if 'Volume' contains any non-numeric values
    non_numeric_volume = df['Volume'].str.contains('[a-zA-Z]', regex=True)
    print(df[non_numeric_volume])

    # If no non-numeric values, you can proceed with pd.eval()
    if df[non_numeric_volume].empty:
        df['Volume'] = df['Volume'].map(pd.eval).astype(int)

    # Check if 'Market Cap' contains any non-numeric values
    non_numeric_marketcap = df['Market Cap'].str.contains('[a-zA-Z]', regex=True)
    print(df[non_numeric_marketcap])

    # If no non-numeric values, you can proceed with pd.eval()
    if df[non_numeric_marketcap].empty:
        df['Market Cap'] = df['Market Cap'].map(pd.eval).astype(float)

    # If 'N/A' found in 'PE Ratio (TTM)', replace it with NaN
    df['PE Ratio (TTM)'] = df['PE Ratio (TTM)'].replace('N/A', float('NaN'))
    df['PE Ratio (TTM)'] = df['PE Ratio (TTM)'].astype(float)

    return df

def main():
    base_url = "https://finance.yahoo.com"
    urls = {
        "most_active": f"{base_url}/most-active",
        "gainers": f"{base_url}/gainers",
        "losers": f"{base_url}/losers",
    }

    # Define the directory to save the files
    save_dir = "/Users/xion/Desktop/stockdata"
    # Define the headers
    headers = ["Symbol", "Name", "Price (Intraday)", "Change", "% Change", "Volume", "Avg Vol (3 month)", "Market Cap", "PE Ratio (TTM)", "52 Week Range"]

    with HTMLSession() as session:
        for category, url in urls.items():
            stocks = scrape_yahoo_stocks(session, url)
            df = pd.DataFrame(stocks, columns=headers)

            # Clean the data
            df = clean_data(df)

            df.to_csv(os.path.join(save_dir, f"{category}_stocks.csv"), index=False)

        # Fetch details of the first most active stock
        first_stock_url = f"{base_url}/{stocks[0][0]}/"
        first_stock_details = fetch_stock_details(session, first_stock_url)
        print(first_stock_details)

if __name__ == "__main__":
    main()



