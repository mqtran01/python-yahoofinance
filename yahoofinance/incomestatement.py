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


class IncomeStatement(IYahooData):
    """Retrieves annual balance sheet information from Yahoo Finance.

    :param stock: The a stock code to query.
    :param locale: A `Locale` constant to determine which domain to query from. Default: `Locale.US`.

    :return: :class:`IncomeStatement` object
    :rtype: `IncomeStatement`

    E.g. https://finance.yahoo.com/quote/AAPL/financials

    Usage::

      >>> from yahoofinance import IncomeStatement
      >>> req = IncomeStatement('AAPL')
      Object<IncomeStatement>
    """

    _df_mapping = {
        'Revenue': [
            ('Total Revenue', 'totalRevenue'),
            ('Cost of Revenue', 'costOfRevenue'),
            ('Gross Profit', 'grossProfit')
        ],
        'Operating Expenses': [
            ('Research Development', 'researchDevelopment'),
            ('Selling General and Administrative', ''),
            ('Non Recurring', 'nonRecurring'),
            ('Others', 'otherOperatingExpenses'),
            ('Total Operating Expenses', 'totalOperatingExpenses'),
            ('Operating Income or Loss', 'operatingIncome')
        ],
        'Income from Continuing Operations': [
            ('Total Other Income/Expenses Net', 'totalOtherIncomeExpenseNet'),
            ('Earnings Before Interest and Taxes', 'ebit'),
            ('Interest Expense', 'interestExpense'),
            ('Income Before Tax', 'incomeBeforeTax'),
            ('Income Tax Expense', 'incomeTaxExpense'),
            ('Minority Interest', 'minorityInterest'),
            ('Net Income From Continuing Ops', 'netIncomeFromContinuingOps')
        ],
        'Non-recurring Events': [
            ('Discontinued Operations', 'discontinuedOperations'),
            ('Extraordinary Items', 'extraordinaryItems'),
            ('Effect Of Accounting Changes', 'effectOfAccountingCharges'),
            ('Other Items', 'otherItems')
        ],
        'Net Income': [
            ('Net Income', 'netIncome'),
            ('Preferred Stock And Other Adjustments', '???'),
            ('Net Income Applicable To Common Shares', 'netIncomeApplicableToCommonShares')
        ]
    }

    def __init__(self, stock, locale=Locale.US):
        super().__init__(locale)
        url = self._base_url + '/{}/financials'.format(stock)
        fin_data = self._fetch_quote_summary(url)

        self.IncomeStatement = self._extract_IncomeStatement(fin_data)
        self.IncomeStatement.sort(key=lambda x: x['endDate']['raw'], reverse=True)

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

        cols = [i['endDate']['fmt'] for i in self.IncomeStatement]
        multiindex = []
        data = []
        for k, v in self._df_mapping.items():
            for name, key in v:
                index = (k, name)
                multiindex.append(index)
                data.append(self._df_row(self.IncomeStatement, key, data_format))

        idx = pd.MultiIndex.from_tuples(multiindex, names=('Subject', 'Item'))
        df = pd.DataFrame(data, idx, cols)
        df_dict = {
            x: df.xs(x) for x in self._df_mapping.keys()
        }
        df_dict['Cash Flow'] = df
        return df_dict

    def _extract_IncomeStatement(self, fin_data):
        return fin_data['incomeStatementHistory']['incomeStatementHistory']

    def _write_csv(self, file_handle, dialect, sep, data_format):
        csv_handle = csv.writer(file_handle, dialect=dialect, delimiter=sep)

        csv_rows = [self._csv_row(self.IncomeStatement, 'Period ending', 'endDate', 'fmt')]
        for k, v in self._df_mapping.items():
            csv_rows.append([])
            csv_rows.append([k])
            for name, key in v:
                csv_rows.append(self._csv_row(self.IncomeStatement, name, key, data_format))
        csv_handle.writerows(csv_rows)


class IncomeStatementQuarterly(IncomeStatement):
    """Retrieves quarterly balance sheet information from Yahoo Finance.

    :param stock: The a stock code to query.
    :param locale: A `Locale` constant to determine which domain to query from. Default: `Locale.US`.

    :return: :class:`IncomeStatementQuarterly` object
    :rtype: `IncomeStatementQuarterly`

    E.g. https://finance.yahoo.com/quote/AAPL/financials

    Usage::

      >>> from yahoofinance import IncomeStatementQuarterly
      >>> req = IncomeStatementQuarterly('AAPL')
      Object<IncomeStatementQuarterly>
    """

    def _extract_IncomeStatement(self, fin_data):
        return fin_data['incomeStatementHistoryQuarterly']['incomeStatementHistory']
