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

class AssetProfile(IYahooData):
    """Retrieves the asset profile from Yahoo Finance.

    :param stock: The stock ticker
    :param locale: A `Local` constant to determine which domain to query from. Default: `Locale.US`.

    :return: :class:`AssetProfile` object
    :rtype: `AssetProfile`

    E.g. https://finance.yahoo.com/quote/AAPL/profile

    Usage::

      >>> from yahoofinance import AssetProfile
      >>> req = AssetProfile('AAPL')
      Object<AssetProfile>

    """

    _info_mapping = (
        ('Address', 'address1'),
        # TODO: Will there be address2, 3 etc.?
        ('City', 'city'),
        ('State', 'CA'),
        ('Country', 'country'),
        ('Phone', 'phone'),
        ('Website', 'website'),
        ('Sector', 'sector'),
        ('Industry', 'industry'),
        ('Full Time Employees', 'fullTimeEmployees')
    )

    _exec_mapping = (
        ('Name', 'name'),
        ('Title', 'title'),
        ('Pay', 'totalPay'),
        ('Exercised', 'exercisedValue'),
        ('Year Born', 'yearBorn'),
    )

    def __init__(self, stock, locale=Locale.US):
        super().__init__(locale)

        url = self._base_url + '/{}/profile'.format(stock)
        fin_data = self._fetch_quote_summary(url)

        self.profile = fin_data['assetProfile']

    def to_csv(self, path, sep=',', data_format=DataFormat.RAW, csv_dialect='excel'):
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

        # TODO: Streamline this
        with open(path, 'w') as file_handle:
            csv_handle = csv.writer(file_handle, delimiter=sep)

            csv_handle.writerow(['Profile'])

            for mapping in self._info_mapping:
                csv_handle.writerow([mapping[0], self.profile.get(mapping[1], '-')])

            csv_handle.writerow([])
            csv_handle.writerow(['Key Executives'])
            csv_handle.writerow([i[0] for i in self._exec_mapping])

            for executive in self.profile.get('companyOfficers', []):
                csv_handle.writerow([
                    executive.get('name'),
                    executive.get('title'),
                    executive.get('totalPay', IYahooData._default_row)[data_format],
                    executive.get('exercisedValue', IYahooData._default_row)[data_format],
                    executive.get('yearBorn')
                    ])

    def to_dfs(self, data_format=DataFormat.RAW):
        raise NotImplementedError()