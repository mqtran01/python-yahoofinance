from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import json
import csv
import requests
import re
import pandas as pd
from io import StringIO
from datetime import date, datetime

from .dataconfigs import DataFormat, Locale, DataEvent, DataFrequency
from .interfaces import IYahooData


class BalanceSheet(IYahooData):
    """Retrieves annual balance sheet information from Yahoo Finance.

    :param stock: The a stock code to query.
    :param locale: A `Locale` constant to determine which domain to query from. Default: `Locale.US`.

    :return: :class:`BalanceSheet` object
    :rtype: `BalanceSheet`

    E.g. https://finance.yahoo.com/quote/AAPL/balance-sheet

    Usage::

      >>> from yahoofinance import BalanceSheet
      >>> req = BalanceSheet('AAPL')
      Object<BalanceSheet>
    """

    _df_mapping = {
        'Assets': [
            ('Cash And Cash Equivalents', 'cash'),
            ('Short Term Investments', 'shortTermInvestments'),
            ('Net Receivables', 'netReceivables'),
            ('Inventory', 'inventory'),
            ('Other Current Assets', 'otherCurrentAssets'),
            ('Total Current Assets', 'totalCurrentAssets'),

            ('Long Term Investments', 'longTermInvestments'),
            ('Property Plant and Equipment', 'propertyPlantEquipment'),
            ('Goodwill', 'goodWill'),
            ('Intangible Assets', 'intangibleAssets'),
            ('Accumulated Amortization', '???'),
            ('Other Assets', 'otherAssets'),
            ('Deferred Long Term Asset Charges', '???'),
            ('Total Assets', 'totalAssets')
        ],
        'Liabilities': [
            ('Accounts Payable', 'accountsPayable'),
            ('Short/Current Long Term Debt', 'shortLongTermDebt'),
            ('Other Current Liabilities', 'otherCurrentLiab'),
            ('Total Current Liabilities', 'totalCurrentLiabilities'),
            ('Long Term Debt', 'longTermDebt'),
            ('Other Liabilities', 'otherLiab'),
            ('Deferred Long Term Liability Charges', '???'),
            ('Minority Interest', '???'),
            ('Negative Goodwill', '???'),
            ('Total Liabilities', 'totalLiab')
        ],
        'Equity': [
            ('Misc. Stocks Options Warrants', '???'),
            ('Redeemable Preferred Stock', '???'),
            ('Preferred Stock', '???'),
            ('Common Stock', 'commonStock'),
            ('Retained Earnings', 'retainedEarnings'),
            ('Treasury Stock', 'treasuryStock'),
            ('Capital Surplus', '???'),
            ('Other Stockholder Equity', 'otherStockholderEquity'),
            ('Total Stockholder Equity', 'totalStockholderEquity'),
            ('Net Tangible Assets', 'netTangibleAssets')
        ]
    }

    def __init__(self, stock, locale=Locale.US):
        super().__init__(locale)
        url = self._base_url + '/{}/financials'.format(stock)
        fin_data = self._fetch_quote_summary(url)

        self.BalanceSheet = self._extract_BalanceSheet(fin_data)
        self.BalanceSheet.sort(key=lambda x: x['endDate']['raw'], reverse=True)

    def to_csv(self, path=None, sep=',', data_format=DataFormat.RAW, csv_dialect='excel'):
        """Generates a CSV file.

        :param path: The path to a file location. If it is `None`, this method returns the
            CSV as a string.
        :param sep: The separator between elements in the new line.
        :param data_format: A :class:`DataFormat` constant to determine how the data is
            exported.
        :param csv_dialect: The dialect to write the CSV file. See Python in-built :class:`csv`.

        :return: `None` or :class:`string`
        :rtype: `None` or `string`
        """

        if path is None:
            file_handle = StringIO()
            self._write_csv(file_handle, csv_dialect, sep, data_format)
            return file_handle.getvalue()

        # Path provided
        with open(path, 'w') as file_handle:
            self._write_csv(file_handle, csv_dialect, sep, data_format)

    def to_dfs(self, data_format=DataFormat.RAW):
        """Generates a dictionary containing :class:`pandas.DataFrame`.

        :param data_format: A :class:`DataFormat` constant to determine how the data is exported.

        :return: :class:`pandas.DataFrame`
        :rtype: `pandas.DataFrame`

        Dictionary keys ::

            Cash Flow
            Overall
            Operating activities
            Investment activities
            Financing activities
            Changes in Cash
        """

        cols = [i['endDate']['fmt'] for i in self.BalanceSheet]
        multiindex = []
        data = []
        for k, v in self._df_mapping.items():
            for name, key in v:
                index = (k, name)
                multiindex.append(index)
                data.append(self._df_row(self.BalanceSheet, key, data_format))

        idx = pd.MultiIndex.from_tuples(multiindex, names=('Subject', 'Item'))
        df = pd.DataFrame(data, idx, cols)
        df_dict = {
            x: df.xs(x) for x in self._df_mapping.keys()
        }
        df_dict['Cash Flow'] = df
        return df_dict

    def _extract_BalanceSheet(self, fin_data):
        return fin_data['balanceSheetHistory']['balanceSheetStatements']

    def _write_csv(self, file_handle, dialect, sep, data_format):
        csv_handle = csv.writer(file_handle, dialect=dialect, delimiter=sep)

        csv_rows = [self._csv_row(self.BalanceSheet, 'Period ending', 'endDate', 'fmt')]
        for k, v in self._df_mapping.items():
            csv_rows.append([])
            csv_rows.append([k])
            for name, key in v:
                csv_rows.append(self._csv_row(self.BalanceSheet, name, key, data_format))
        csv_handle.writerows(csv_rows)


class BalanceSheetQuarterly(BalanceSheet):
    """Retrieves quarterly balance sheet information from Yahoo Finance.

    :param stock: The a stock code to query.
    :param locale: A `Locale` constant to determine which domain to query from. Default: `Locale.US`.

    :return: :class:`BalanceSheetQuarterly` object
    :rtype: `BalanceSheetQuarterly`

    E.g. https://finance.yahoo.com/quote/AAPL/balance-sheet

    Usage::

      >>> from yahoofinance import BalanceSheetQuarterly
      >>> req = BalanceSheetQuarterly('AAPL')
      Object<BalanceSheetQuarterly>
    """

    def _extract_BalanceSheet(self, fin_data):
        return fin_data['balanceSheetHistoryQuarterly']['balanceSheetStatements']