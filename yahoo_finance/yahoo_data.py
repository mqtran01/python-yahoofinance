from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import json
import csv
import requests

from data_configs import DataFormat, Locale

class IYahooData(ABC):
    _default_row = {
        x: '-' for x in DataFormat._FORMATS
    }

    def __init__(self, stock, locale):
        if locale == Locale.US:
            # Special case because the US is special
            self._base_url = "https://finance.yahoo.com"
        else:
            self._base_url = "https://{}.finance.yahoo.com".format(locale)

    @abstractmethod
    def to_csv(self, path, line_terminator, sep):
        pass

    @staticmethod
    def _csv_row(dataset, heading, index, data_fmt):
        default_row = {
            x: '-' for x in DataFormat._FORMATS
        }
        return [heading, ''] + [data.get(index, IYahooData._default_row)[data_fmt] for data in dataset]

    @staticmethod
    def _fetch_quote_summary(url):
        html = requests.get(url).text
        soup = BeautifulSoup(html,'html.parser')

        soup_script = soup.find("script",text=re.compile("root.App.main")).text
        json_script = json.loads(re.search("root.App.main\s+=\s+(\{.*\})",soup_script)[1])
        # return json_script
        return json_script['context']['dispatcher']['stores']['QuoteSummaryStore']


class CashFlow(IYahooData):
    _table_mapping = (
        {
            'header': 'Operating activities, cash flow provided by or used in',
            'data_map': [
                ('Depreciation', 'depreciation'),
                ('Adjustments to net income', 'changeToNetincome'),
                ('Changes in accounts receivable', 'changeToAccountReceivables'),
                ('Changes in liabilities', 'changeToLiabilities'),
                ('Changes in inventory', 'changeToInventory'),
                ('Changes in other operating activities', 'changeToOperatingActivities'),
                ('Total cash flow from operating activities', 'totalCashFromOperatingActivities')
            ]
        },
        {
            'header': 'Investment activities, cash flow provided by or used in',
            'data_map': [
                ('Capital expenditure', 'capitalExpenditures'),
                ('Investments', 'investments'),
                ('Other cash flow from investment activities', 'otherCashflowsFromInvestingActivities'),
                ('Total cash flow from investment activities', 'totalCashflowsFromInvestingActivities'),
            ]
        },
        {
            'header': 'Financing activities, cash flow provided by or used in',
            'data_map': [
                ('Dividends paid', 'dividendsPaid'),
                # TODO: Find the correct header for this item
                ('Sale purchase of stock', '???'),
                ('Net borrowings', 'netBorrowings'),
                ('Other cash flow from financing activities', 'otherCashflowsFromFinancingActivities'),
                ('Total cash flow from financing activities', 'totalCashFromFinancingActivities')
            ]
        }
    )

    def __init__(self, stock, locale=Locale.US):
        super().__init__(stock, locale)
        url = self._base_url + '/{}/financials'.format(stock)
        fin_data = self._fetch_quote_summary(url)

        self.cashflow = self._extract_cashflow(fin_data)
        self.cashflow.sort(key=lambda x: x['endDate']['raw'], reverse=True)

    def to_csv(self, path, line_terminator='\n', sep=',', data_format=DataFormat.RAW):
        with open(path, 'w') as file_handle:
            csv_handle = csv.writer(file_handle, delimiter=sep)

            csv_handle.writerow([self._header_text()])
            csv_handle.writerow(self._csv_row(self.cashflow, 'Period ending', 'endDate', 'fmt'))

            csv_handle.writerow(self._csv_row(self.cashflow, 'Net income', 'netIncome', data_format))

            for header_mapping in self._table_mapping:
                csv_handle.writerow([])
                csv_handle.writerow([header_mapping['header']])
                for data_mapping in header_mapping['data_map']:
                    csv_handle.writerow(self._csv_row(self.cashflow, data_mapping[0], data_mapping[1], data_format))
                    
            
            csv_handle.writerow([])
            # TODO: Find the correct header for this item
            csv_handle.writerow(self._csv_row(self.cashflow, 'Effect of exchange rate changes', '???', data_format))
            
            csv_handle.writerow([])
            csv_handle.writerow(self._csv_row(self.cashflow, 'Change in cash and cash equivalents', 'changeInCash', data_format))

    def _header_text(self):
        return 'Cash Flow (Annual)'
    
    def _extract_cashflow(self, fin_data):
        return fin_data['cashflowStatementHistory']['cashflowStatements']


class CashFlowQuarterly(CashFlow):
    def _header_text(self):
        return 'Cash Flow (Quarterly)'
    
    def _extract_cashflow(self, fin_data):
        return fin_data['cashflowStatementHistoryQuarterly']['cashflowStatements']


class AssetProfile(IYahooData):
    _info_mapping = {
        ()
    }

    _exec_mapping = {
        ('Name', 'name'),
        ('Age', 'age'),
        ('Year Born', 'yearBorn'),
        ('Exercised Value', 'exercised')
    }

    def __init__(self, stock, locale=Locale.US):
        super().__init__(stock, locale)

        url = self._base_url + '/{}/profile'.format(stock)
        fin_data = self._fetch_quote_summary(url)

        self.profile = fin_data['assetProfile']

    def to_csv(self, path, line_terminator='\n', sep=',', data_format=DataFormat.RAW):
        with open(path, 'w') as file_handle:
            csv_handle = csv.writer(file_handle, delimiter=sep)

            csv_handle.writerow(['Profile'])
            csv_handle.writerow(self._csv_row(self.cashflow, 'Period ending', 'endDate', 'fmt'))

            csv_handle.writerow(self._csv_row(self.cashflow, 'Net income', 'netIncome', data_format))

            for header_mapping in self._table_mapping:
                csv_handle.writerow([])
                csv_handle.writerow([header_mapping['header']])
                for data_mapping in header_mapping['data_map']:
                    csv_handle.writerow(self._csv_row(self.cashflow, data_mapping[0], data_mapping[1], data_format))
                    
            
            csv_handle.writerow([])
            # TODO: Find the correct header for this item
            csv_handle.writerow(self._csv_row(self.cashflow, 'Effect of exchange rate changes', '???', data_format))
            
            csv_handle.writerow([])
            csv_handle.writerow(self._csv_row(self.cashflow, 'Change in cash and cash equivalents', 'changeInCash', data_format))

