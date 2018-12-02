from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import json
import requests
import re

from .dataconfigs import Locale, DataEvent, DataFormat, DataFrequency


class IYahooData(ABC):
    """This is the base interface.

    Each class in this library inherits implements this interface.

    **This class is NOT instantiable.**

    :param locale: a :class:`yahoofinance.Locale` constant to determine which domain to query from.
    """

    # This is the default row
    _default_row = {
        x: '-' for x in DataFormat._FORMATS
    }

    def __init__(self, locale):
        self._base_url = Locale.locale_url(locale)

    @abstractmethod
    def to_csv(self):
    # def to_csv(self, path, sep, data_format, csv_dialect):
        """Generates a CSV file."""
        pass

    @abstractmethod
    def to_dfs(self):
    # def to_dfs(self, data_format):
        """Generates a dictionary containing :class:`pandas.DataFrame`."""
        pass

    @staticmethod
    def _csv_row(dataset, heading, index, data_fmt):
        return [heading, ''] + [(data[index] if data.get(index) else IYahooData._default_row)[data_fmt] for data in dataset]

    @staticmethod
    def _df_row(dataset, index, data_fmt):
        return [(data[index] if data.get(index) else IYahooData._default_row)[data_fmt] for data in dataset]

    @staticmethod
    def _fetch_quote_summary(url):
        html = requests.get(url).text
        soup = BeautifulSoup(html,'html.parser')

        soup_script = soup.find("script",text=re.compile("root.App.main")).text
        json_script = json.loads(re.search(r"root.App.main\s+=\s+(\{.*\})",soup_script)[1])
        # return json_script
        return json_script['context']['dispatcher']['stores']['QuoteSummaryStore']
