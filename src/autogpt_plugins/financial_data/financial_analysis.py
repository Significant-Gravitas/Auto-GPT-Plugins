import yfinance as yf
import pandas as pd
from yahooquery import Ticker
from datetime import datetime 
import requests
from bs4 import BeautifulSoup

def download_data(symbol, start_date, end_date):
    data = yf.download(symbol, start_date, end_date)
    return data

def fetch_financial_data(symbol):
    ticker = Ticker(symbol)

    # Fetch income statement, balance sheet and cash flow
    income_statement = ticker.income_statement('q')
    balance_sheet = ticker.balance_sheet('q')
    cash_flow = ticker.cash_flow('q')

    income_statement = income_statement[income_statement.periodType == '3M']
    balance_sheet = balance_sheet[balance_sheet.periodType == '3M']
    cash_flow = cash_flow[cash_flow.periodType == '3M']

    # Filter for key financial metrics
    income_statement_keys = ['asOfDate', 'TotalRevenue', 'CostOfRevenue', 'GrossProfit', 'OperatingIncome', 'NetIncome', 'OperatingExpense', 'ResearchAndDevelopment']
    balance_sheet_keys = ['asOfDate', 'TotalAssets', 'TotalLiabilitiesNetMinorityInterest', 'StockholdersEquity', 'CashAndCashEquivalents', 'LongTermDebt', 'CurrentAssets', 'CurrentLiabilities']
    cash_flow_keys = ['asOfDate', 'OperatingCashFlow', 'InvestingCashFlow', 'FinancingCashFlow', 'FreeCashFlow', 'NetIncome']

    # Filter financial data and prepare for presentation
    income_statement = income_statement.loc[:, income_statement_keys]
    balance_sheet = balance_sheet.loc[:, balance_sheet_keys]
    cash_flow = cash_flow.loc[:, cash_flow_keys]

    # Sort and get the latest 4 quarters
    income_statement = income_statement.sort_values('asOfDate', ascending=False).head(4)
    balance_sheet = balance_sheet.sort_values('asOfDate', ascending=False).head(4)
    cash_flow = cash_flow.sort_values('asOfDate', ascending=False).head(4)

    # Present data in a natural language format
    result = f"Financial Analysis for {symbol}:\n\n"
    for _, row in income_statement.iterrows():
        result += f"\nAs of the quarter ending {row['asOfDate']}, {symbol} had:\n"
        for key in income_statement_keys[1:]:
            result += f"{key}: ${row[key]:,.2f}\n"

    for _, row in balance_sheet.iterrows():
        result += f"\nFor the quarter ending {row['asOfDate']}, {symbol}'s balance sheet was:\n"
        for key in balance_sheet_keys[1:]:
            result += f"{key}: ${row[key]:,.2f}\n"

    for _, row in cash_flow.iterrows():
        result += f"\nFor the quarter ending {row['asOfDate']}, {symbol}'s cash flow was:\n"
        for key in cash_flow_keys[1:]:
            result += f"{key}: ${row[key]:,.2f}\n"

    return result

def calc_stats(symbol, periods=[30, 90, 180, 365, 3 * 365, 5 * 365]):
    descriptions = []
    ticker = yf.Ticker(symbol)
    ipo_date = ticker.info.get("ipoDate")

    # Convert IPO date string to datetime object, if it exists
    if ipo_date:
        ipo_date = datetime.strptime(ipo_date, "%Y-%m-%d")

    # Download all available data for this stock
    all_data = download_data(symbol, ipo_date, datetime.today())

    for period in periods:
        # Check if the company has been listed for the specified number of days
        if len(all_data.index) < period:
            descriptions.append(
                f"{symbol} has not been listed for {period} trading days."
            )
            continue

        data = all_data.tail(period).copy()

        start_date = data.index[0].strftime("%Y-%m-%d")
        end_date = data.index[-1].strftime("%Y-%m-%d")
        start_price = data["Adj Close"].iloc[0]
        end_price = data["Adj Close"].iloc[-1]
        pct_change = (end_price - start_price) / start_price * 100
        high = data["High"].max()
        high_date = data["High"].idxmax().strftime("%Y-%m-%d")
        low = data["Low"].min()
        low_date = data["Low"].idxmin().strftime("%Y-%m-%d")
        avg_volume = data["Volume"].mean()
        data["Return"] = data["Adj Close"].pct_change()
        volatility = data["Return"].std()
        description = f"For the last {period} days ({start_date} to {end_date}):\n"
        description += (
            f"Start price was {start_price:.2f} and end price was {end_price:.2f}. "
        )
        description += f"This is a percentage change of {pct_change:.2f}%.\n"
        description += f"Highest price was {high:.2f} on {high_date}, "
        description += f"and lowest price was {low:.2f} on {low_date}.\n"
        description += f"Average volume was {avg_volume:.2f}, "
        description += f"and the standard deviation of daily returns (volatility) was {volatility:.2f}."

        descriptions.append(description)

    return "\n\n".join(descriptions)

def get_yahoo_finance_news(symbol):
    url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={symbol}&region=US&lang=en-US"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.content, features='xml')
    items = soup.findAll('item')
    result = f"Latest news for {symbol}:\n\n"
    for item in items:
        title = item.title.text
        pubDate = item.pubDate.text
        description = item.description.text

        # Add the item's details to the result
        result += f"Title: {title}\n"
        result += f"Published: {pubDate}\n"
        result += f"Description: {description}\n\n"

    return result

def generate_financial_data(symbol):
        prompt = "As a senior analyst, your task is to write a comprehensive analysis report on a given stock using the provided information below. The report should offer a detailed overview of the company's financial condition, covering all essential aspects of its financial performance. Additionally, it should include your insights and a summary. Aim for a highly detailed report, consisting of approximately 3000 words."
        prompt += "\n\n"
        prompt += fetch_financial_data(symbol)
        prompt += "\n\n"
        prompt += calc_stats(symbol)
        prompt += "\n\n"
        prompt += get_yahoo_finance_news(symbol)
        return prompt