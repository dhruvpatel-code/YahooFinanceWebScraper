# Yahoo Finance Stock Scraper and Analyzer

This program is a web scraper and data analyzer for stocks listed on Yahoo Finance. It allows you to fetch stock data, perform basic data cleaning, calculate statistics, and visualize the data using various plots. The program is written in Python.

## Installation

To use this program, you need to have Python installed on your machine. You can download Python from the official website: [python.org](https://www.python.org/).

Additionally, you need to install the required dependencies. Open a terminal or command prompt and run the following command:

```
pip install beautifulsoup4 requests-html pandas matplotlib seaborn scikit-learn
```

## Usage

1. Clone or download the repository from GitHub.
2. Navigate to the project directory.
3. Open the Python file containing the code (e.g., `stocks_scraper.py`) in a text editor.
4. Modify the `save_dir` variable to specify the directory where you want to save the scraped stock data.
5. Run the following command to start the program:

   ```
   python stocks_scraper.py
   ```

6. The program will scrape data from Yahoo Finance for the most active, gainers, and losers categories of stocks. It will save the data as CSV files in the specified directory.
7. The program will also calculate basic statistics, such as mean, median, and standard deviation of the stock prices. It will plot a histogram of prices and a scatterplot of volume vs. price for each category of stocks.

## Customization

You can customize the program in several ways:

- **Categories:** By default, the program scrapes data for the "most active," "gainers," and "losers" categories. You can modify the `urls` dictionary in the code to scrape data for different categories or additional categories.

- **Data Cleaning:** The `clean_data` function performs data cleaning operations, such as removing commas and spaces, converting values to appropriate data types, and handling non-numeric values. You can modify this function to add or remove cleaning steps based on your requirements.

- **Data Analysis:** After scraping and cleaning the data, the program calculates basic statistics and creates plots. You can modify or extend the code to perform additional analysis or create different types of visualizations.

## Contributing

If you want to contribute to this project, feel free to fork the repository and submit a pull request with your changes.
