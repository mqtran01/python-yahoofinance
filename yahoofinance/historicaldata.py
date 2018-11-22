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

class HistoricalPrices(IYahooData):
    """Retrieves historical data from Yahoo Finance.

    :param instrument: The a stock instrument code to query.
    :param start_date: The start date for the query (inclusive).
    :param end_date: The end date for the query (inclusive).
    :param date_format_string: If `start_date` or `end_date` is not a :class:`DateTime` object,
        the object passed in (string) will be parsed to the format string. Default: `%Y-%m-%d`.
    :param event: A `DataEvent` constant to determine what event to query for. Default: `DataEvent.HISTORICAL_PRICES`.
    :param frequency: A `DataFrequency` constant to determine the interval between records. Default: `DataFrequency.DAILY`.
    :param locale: A `Locale` constant to determine which domain to query from. Default: `Locale.US`.

    :return: :class:`HistoricalPrices` object
    :rtype: `HistoricalPrices`

    E.g. https://finance.yahoo.com/quote/AAPL/history

    Usage::

      >>> from yahoofinance import HistoricalPrices
      >>> req = HistoricalPrices('AAPL')
      Object<HistoricalPrices>
    """
    _min_date = date(1970,1,1)

    def __init__(
            self, instrument, start_date, end_date, date_format_string="%Y-%m-%d",
            event=DataEvent.HISTORICAL_PRICES, frequency=DataFrequency.DAILY, locale=Locale.US):

        if not isinstance(start_date, date):
            start_date = datetime.strptime(start_date, date_format_string).date()

        if not isinstance(end_date, date):
            end_date = datetime.strptime(end_date, date_format_string).date()

        start_period = int((start_date - self._min_date).total_seconds())
        end_period = int((end_date - self._min_date).total_seconds())

        cookie, crumb = self._find_cookie_crumb_pair(locale)

        url = 'https://query1.finance.yahoo.com/v7/finance/download/{i}'
        r= requests.get(url.format(i=instrument),
            cookies={'B': cookie},
            params={
                "period1": start_period,
                "period2": end_period,
                "interval": frequency,
                "event": event,
                "crumb": crumb
            }
        )

        self.prices = r.text

    def _find_cookie_crumb_pair(self, locale):
        url = Locale.locale_url(locale) + '/AAPL/history'
        res = requests.get(url)
        try:
            cookie = res.cookies['B']
        except KeyError:
            raise ValueError("Cookie not found")

        # TODO: Consider bs4 to make processing faster?
        pattern = r'"CrumbStore":{"crumb":"(.+?)"}'
        matcher = re.search(pattern, res.text)
        if matcher:
            crumb = matcher.group(1)
        else:
            raise ValueError("Crumb not found")

        # Handles the slash encoding as the character is allowed
        crumb = crumb.replace('\\u002F', '/')

        return cookie, crumb

    def to_csv(self, path=None, sep=',', data_format=DataFormat.RAW, csv_dialect='excel'):
        """Generates a CSV file.

        :param path: The path to a file location. If it is `None`, this method returns the
            CSV as a string.
        :param sep: The separator between elements in the new line. NOT USED
        :param data_format: A :class:`DataFormat` constant to determine how the data is
            exported. NOT USED
        :param csv_dialect: The dialect to write the CSV file. See Python in-built :class:`csv`.

        :return: `None` or :class:`string`
        :rtype: `None` or `string`

        """
        csv_data = self.prices
        # HACK: To reverse the new line encoding provided. Find a better way to handle this
        if csv_dialect == 'excel':
            csv_data.replace('\n', '\r\n')

        if path is None:
            return self.prices

        with open(path, 'w') as file_handle:
            file_handle.write(csv_data)

    def to_dfs(self, data_format=DataFormat.RAW):
        """Generates a dictionary containing :class:`pandas.DataFrame`.

        :param data_format: A :class:`DataFormat` constant to determine how the data is exported.
            NOT USED

        :return: :class:`pandas.DataFrame`
        :rtype: `pandas.DataFrame`

        Dictionary keys ::

            Historical Prices
        """

        # This is not affected by the data format
        return {'Historical Prices': pd.read_csv(StringIO(self.prices), index_col=['Date'])}
