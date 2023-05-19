import unittest
from unittest.mock import patch, Mock
import os
from datetime import datetime
import yfinance as yf
import pandas as pd
import numpy as np

from .financial_analysis import download_data, fetch_financial_data, calc_stats, get_yahoo_finance_news, generate_financial_data
from . import AutoGPTFinancialAnalysis

class TestAutoGPTFinancialAnalysis(unittest.TestCase):
    def setUp(self):
        self.plugin = AutoGPTFinancialAnalysis()
        self.symbol = "AAPL"
        self.dummy_data = pd.DataFrame({
            'High': np.random.rand(10) * 100,
            'Low': np.random.rand(10) * 100,
            'Open': np.random.rand(10) * 100,
            'Close': np.random.rand(10) * 100,
            'Volume': np.random.rand(10) * 1000000,
            'Adj Close': np.random.rand(10) * 100,
        })

    def test_can_handle_post_prompt(self):
        self.assertTrue(self.plugin.can_handle_post_prompt())

    def test_can_handle_pre_command(self):
        self.assertTrue(self.plugin.can_handle_pre_command())

    @patch('src.autogpt_plugin_financial_analysis.financial_analysis.yf.download')
    def test_download_data(self, mock_download):
        mock_download.return_value = self.dummy_data
        data = download_data(self.symbol, "2022-01-01", "2023-01-01")
        self.assertTrue(isinstance(data, pd.DataFrame))
        self.assertEqual(len(data), 10)

    @patch('src.autogpt_plugin_financial_analysis.financial_analysis.Ticker')
    def test_fetch_financial_data(self, mock_ticker):
        df_income = pd.DataFrame({
            'periodType': ['3M', '3M', '6M', '6M'],
            'asOfDate': pd.date_range(end='1/1/2022', periods=4),
            'TotalRevenue': np.random.rand(4) * 1000,
            'CostOfRevenue': np.random.rand(4) * 1000,
            'GrossProfit': np.random.rand(4) * 1000,
            'OperatingIncome': np.random.rand(4) * 1000,
            'NetIncome': np.random.rand(4) * 1000,
            'OperatingExpense': np.random.rand(4) * 1000,
            'ResearchAndDevelopment': np.random.rand(4) * 1000,
        })

        df_balance = pd.DataFrame({
            'periodType': ['3M', '3M', '6M', '6M'],
            'asOfDate': pd.date_range(end='1/1/2022', periods=4),
            'TotalAssets': np.random.rand(4) * 1000,
            'TotalLiabilitiesNetMinorityInterest': np.random.rand(4) * 1000,
            'StockholdersEquity': np.random.rand(4) * 1000,
            'CashAndCashEquivalents': np.random.rand(4) * 1000,
            'LongTermDebt': np.random.rand(4) * 1000,
            'CurrentAssets': np.random.rand(4) * 1000,
            'CurrentLiabilities': np.random.rand(4) * 1000,
        })

        df_cash_flow = pd.DataFrame({
            'periodType': ['3M', '3M', '6M', '6M'],
            'asOfDate': pd.date_range(end='1/1/2022', periods=4),
            'OperatingCashFlow': np.random.rand(4) * 1000,
            'InvestingCashFlow': np.random.rand(4) * 1000,
            'FinancingCashFlow': np.random.rand(4) * 1000,
            'FreeCashFlow': np.random.rand(4) * 1000,
            'NetIncome': np.random.rand(4) * 1000,
        })

        mock_ticker.return_value.income_statement.return_value = df_income
        mock_ticker.return_value.balance_sheet.return_value = df_balance
        mock_ticker.return_value.cash_flow.return_value = df_cash_flow
        result = fetch_financial_data(self.symbol)
        self.assertTrue(isinstance(result, str))

    @patch('src.autogpt_plugin_financial_analysis.financial_analysis.yf.Ticker')
    @patch('src.autogpt_plugin_financial_analysis.financial_analysis.download_data')
    def test_calc_stats(self, mock_download_data, mock_ticker):
        mock_download_data.return_value = self.dummy_data
        mock_ticker.return_value.info.get.return_value = "2022-01-01"
        result = calc_stats(self.symbol)
        self.assertTrue(isinstance(result, str))

    @patch('src.autogpt_plugin_financial_analysis.financial_analysis.requests.get')
    def test_get_yahoo_finance_news(self, mock_get):
        mock_response = Mock()
        mock_response.content = b'<rss><channel><item><title>Test news</title><pubDate>2023-05-19</pubDate><description>Test description</description></item></channel></rss>'
        mock_get.return_value = mock_response
        result = get_yahoo_finance_news(self.symbol)
        self.assertTrue(isinstance(result, str))

    @patch('src.autogpt_plugin_financial_analysis.financial_analysis.fetch_financial_data')
    @patch('src.autogpt_plugin_financial_analysis.financial_analysis.calc_stats')
    @patch('src.autogpt_plugin_financial_analysis.financial_analysis.get_yahoo_finance_news')
    def test_generate_financial_data(self, mock_news, mock_stats, mock_fin_data):
        mock_news.return_value = "News"
        mock_stats.return_value = "Stats"
        mock_fin_data.return_value = "Financial data"
        result = generate_financial_data(self.symbol)
        self.assertTrue(isinstance(result, str))

    @patch('src.autogpt_plugin_financial_analysis.financial_analysis.os.getcwd')
    def test_pre_command(self, mock_getcwd):
        mock_getcwd.return_value = '/home'
        command_name, arguments = self.plugin.pre_command(
            "generate_financial_data", {"symbol": self.symbol}
        )
        self.assertEqual(command_name, "write_to_file")