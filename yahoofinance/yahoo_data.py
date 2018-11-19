from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import json
import csv
import requests
import re
import pandas as pd
from io import StringIO
from datetime import date, datetime

from .data_configs import DataFormat, Locale, DataEvent, DataFrequency

class IYahooData(ABC):
    """Test docstring"""

    #: This is the default row
    _default_row = {
        x: '-' for x in DataFormat._FORMATS
    }

    def __init__(self, stock, locale):
        self._base_url = Locale.locale_url(locale)

    @abstractmethod
    def to_csv(self, path, sep, data_format, csv_dialect):
        pass

    @abstractmethod
    def to_dfs(self, data_format):
        pass

    @staticmethod
    def _csv_row(dataset, heading, index, data_fmt):
        return [heading, ''] + [data.get(index, IYahooData._default_row)[data_fmt] for data in dataset]

    @staticmethod
    def _df_row(dataset, index, data_fmt):
        return [data.get(index, IYahooData._default_row)[data_fmt] for data in dataset]

    @staticmethod
    def _fetch_quote_summary(url):
        html = requests.get(url).text
        soup = BeautifulSoup(html,'html.parser')

        soup_script = soup.find("script",text=re.compile("root.App.main")).text
        json_script = json.loads(re.search(r"root.App.main\s+=\s+(\{.*\})",soup_script)[1])
        # return json_script
        return json_script['context']['dispatcher']['stores']['QuoteSummaryStore']


class CashFlow(IYahooData):
    """Hello world?"""
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
        super().__init__(stock, locale)
        url = self._base_url + '/{}/financials'.format(stock)
        fin_data = self._fetch_quote_summary(url)

        self.cashflow = self._extract_cashflow(fin_data)
        self.cashflow.sort(key=lambda x: x['endDate']['raw'], reverse=True)

    def to_csv(self, path=None, sep=',', data_format=DataFormat.RAW, csv_dialect='excel'):
        if path is None:
            file_handle = StringIO()
            self._write_csv(file_handle, csv_dialect, sep, data_format)
            return file_handle.getvalue()

        # Path provided
        with open(path, 'w') as file_handle:
            self._write_csv(file_handle, csv_dialect, sep, data_format)

    def to_dfs(self, data_format=DataFormat.RAW):
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
    def _header_text(self):
        return 'Cash Flow (Quarterly)'

    def _extract_cashflow(self, fin_data):
        return fin_data['cashflowStatementHistoryQuarterly']['cashflowStatements']


class AssetProfile(IYahooData):
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
        super().__init__(stock, locale)

        url = self._base_url + '/{}/profile'.format(stock)
        fin_data = self._fetch_quote_summary(url)

        self.profile = fin_data['assetProfile']

    def to_csv(self, path, sep=',', data_format=DataFormat.RAW, csv_dialect='excel'):
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

class HistoricalPrices(IYahooData):
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
        csv_data = self.prices
        # HACK: To reverse the new line encoding provided. Find a better way to handle this
        if csv_dialect == 'excel':
            csv_data.replace('\n', '\r\n')

        if path is None:
            return self.prices

        with open(path, 'w') as file_handle:
            file_handle.write(csv_data)

    def to_dfs(self, data_format=DataFormat.RAW):
        # This is not affected by the data format
        return {'Historical Prices': pd.read_csv(StringIO(self.prices), index_col=['Date'])}
