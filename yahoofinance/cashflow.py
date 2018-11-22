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


class CashFlow(IYahooData):
    """Retrieves annual cash flow information from Yahoo Finance.

    :param stock: The a stock code to query.
    :param locale: A `Locale` constant to determine which domain to query from. Default: `Locale.US`.

    :return: :class:`CashFlow` object
    :rtype: `CashFlow`

    E.g. https://finance.yahoo.com/quote/AAPL/cash-flow

    Usage::

      >>> from yahoofinance import CashFlow
      >>> req = CashFlow('AAPL')
      Object<CashFlow>
    """

    _df_mapping = {
        'Overall': [
            ('Net Income', 'netIncome')
        ],
        'Operating activities': [
            ('Depreciation', 'depreciation'),
            ('Adjustments to net income', 'changeToNetincome'),
            ('Changes in accounts receivable', 'changeToAccountReceivables'),
            ('Changes in liabilities', 'changeToLiabilities'),
            ('Changes in inventory', 'changeToInventory'),
            ('Changes in other operating activities', 'changeToOperatingActivities'),
            ('Total cash flow from operating activities', 'totalCashFromOperatingActivities')
        ],
        'Investment activities': [
            ('Capital expenditure', 'capitalExpenditures'),
            ('Investments', 'investments'),
            ('Other cash flow from investment activities', 'otherCashflowsFromInvestingActivities'),
            ('Total cash flow from investment activities', 'totalCashflowsFromInvestingActivities'),
        ],
        'Financing activities': [
            ('Dividends paid', 'dividendsPaid'),
            # TODO: Find the correct header for this item
            ('Sale purchase of stock', '???'),
            ('Net borrowings', 'netBorrowings'),
            ('Other cash flow from financing activities', 'otherCashflowsFromFinancingActivities'),
            ('Total cash flow from financing activities', 'totalCashFromFinancingActivities')
        ],
        'Changes in Cash': [
            # TODO: Find the correct header for this item
            ('Effect of exchange rate changes', '???'),
            ('Change in cash and cash equivalents', 'changeInCash')
        ]
    }

    def __init__(self, stock, locale=Locale.US):
        super().__init__(locale)
        url = self._base_url + '/{}/financials'.format(stock)
        fin_data = self._fetch_quote_summary(url)

        self.cashflow = self._extract_cashflow(fin_data)
        self.cashflow.sort(key=lambda x: x['endDate']['raw'], reverse=True)

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

        cols = [i['endDate']['fmt'] for i in self.cashflow]
        multiindex = []
        data = []
        for k, v in self._df_mapping.items():
            for name, key in v:
                index = (k, name)
                multiindex.append(index)
                data.append(self._df_row(self.cashflow, key, data_format))

        idx = pd.MultiIndex.from_tuples(multiindex, names=('Subject', 'Item'))
        df = pd.DataFrame(data, idx, cols)
        df_dict = {
            x: df.xs(x) for x in self._df_mapping.keys()
        }
        df_dict['Cash Flow'] = df
        return df_dict

    def _header_text(self):
        return 'Cash Flow (Annual)'

    def _extract_cashflow(self, fin_data):
        return fin_data['cashflowStatementHistory']['cashflowStatements']

    def _write_csv(self, file_handle, dialect, sep, data_format):
        csv_handle = csv.writer(file_handle, dialect=dialect, delimiter=sep)

        csv_rows = [self._csv_row(self.cashflow, 'Period ending', 'endDate', 'fmt')]
        for k, v in self._df_mapping.items():
            csv_rows.append([])
            csv_rows.append([k])
            for name, key in v:
                csv_rows.append(self._csv_row(self.cashflow, name, key, data_format))
        csv_handle.writerows(csv_rows)


class CashFlowQuarterly(CashFlow):
    """Retrieves quarterly cash flow information from Yahoo Finance.

    :param stock: The a stock code to query.
    :param locale: A `Locale` constant to determine which domain to query from. Default: `Locale.US`.

    :return: :class:`CashFlowQuarterly` object
    :rtype: `CashFlowQuarterly`

    E.g. https://finance.yahoo.com/quote/AAPL/cash-flow

    Usage::

      >>> from yahoofinance import CashFlowQuarterly
      >>> req = CashFlowQuarterly('AAPL')
      Object<CashFlowQuarterly>
    """

    def _header_text(self):
        return 'Cash Flow (Quarterly)'

    def _extract_cashflow(self, fin_data):
        return fin_data['cashflowStatementHistoryQuarterly']['cashflowStatements']