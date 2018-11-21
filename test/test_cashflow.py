import unittest
from unittest import TestCase, mock, main
from yahoofinance import CashFlow
from test.mock_framework import MockResponse


def mock_requests_get(*args, **kwargs):
    with open('test/resources/Cashflow.html') as file:
        return MockResponse(file.read())


class TestCashFlow(TestCase):

    @mock.patch('yahoofinance.cashflow.requests.get', side_effect=mock_requests_get)
    def test_to_csv(self, mock_get):
        expected = 'Period ending,,2018-09-29,2017-09-30,2016-09-24,2015-09-26\r\n\r\nOverall\r\nNet Income,,59531000000,48351000000,45687000000,53394000000\r\n\r\nOperating activities\r\nDepreciation,,10903000000,10157000000,10505000000,11257000000\r\nAdjustments to net income,,-27694000000,10640000000,9634000000,5353000000\r\nChanges in accounts receivable,,-5322000000,-2093000000,527000000,417000000\r\nChanges in liabilities,,9131000000,8340000000,563000000,6043000000\r\nChanges in inventory,,828000000,-2723000000,217000000,-238000000\r\nChanges in other operating activities,,30057000000,-8447000000,-902000000,5040000000\r\nTotal cash flow from operating activities,,77434000000,64225000000,66231000000,81266000000\r\n\r\nInvestment activities\r\nCapital expenditure,,-13313000000,-12451000000,-12734000000,-11247000000\r\nInvestments,,30845000000,-33542000000,-32022000000,-44417000000\r\nOther cash flow from investment activities,,-745000000,-124000000,-924000000,-26000000\r\nTotal cash flow from investment activities,,16066000000,-46446000000,-45977000000,-56274000000\r\n\r\nFinancing activities\r\nDividends paid,,-13712000000,-12769000000,-12150000000,-11561000000\r\nSale purchase of stock,,-,-,-,-\r\nNet borrowings,,432000000,29014000000,22057000000,29305000000\r\nOther cash flow from financing activities,,-,-,-,749000000\r\nTotal cash flow from financing activities,,-87876000000,-17974000000,-20890000000,-17716000000\r\n\r\nChanges in Cash\r\nEffect of exchange rate changes,,-,-,-,-\r\nChange in cash and cash equivalents,,5624000000,-195000000,-636000000,7276000000\r\n'

        cashflow = CashFlow('AAPL')
        csv = cashflow.to_csv()
        self.assertEqual(expected, csv)

    @mock.patch('yahoofinance.cashflow.requests.get', side_effect=mock_requests_get)
    def test_to_csv_unix_delim(self, mock_get):
        expected = \
'''"Period ending","","2018-09-29","2017-09-30","2016-09-24","2015-09-26"

"Overall"
"Net Income","","59531000000","48351000000","45687000000","53394000000"

"Operating activities"
"Depreciation","","10903000000","10157000000","10505000000","11257000000"
"Adjustments to net income","","-27694000000","10640000000","9634000000","5353000000"
"Changes in accounts receivable","","-5322000000","-2093000000","527000000","417000000"
"Changes in liabilities","","9131000000","8340000000","563000000","6043000000"
"Changes in inventory","","828000000","-2723000000","217000000","-238000000"
"Changes in other operating activities","","30057000000","-8447000000","-902000000","5040000000"
"Total cash flow from operating activities","","77434000000","64225000000","66231000000","81266000000"

"Investment activities"
"Capital expenditure","","-13313000000","-12451000000","-12734000000","-11247000000"
"Investments","","30845000000","-33542000000","-32022000000","-44417000000"
"Other cash flow from investment activities","","-745000000","-124000000","-924000000","-26000000"
"Total cash flow from investment activities","","16066000000","-46446000000","-45977000000","-56274000000"

"Financing activities"
"Dividends paid","","-13712000000","-12769000000","-12150000000","-11561000000"
"Sale purchase of stock","","-","-","-","-"
"Net borrowings","","432000000","29014000000","22057000000","29305000000"
"Other cash flow from financing activities","","-","-","-","749000000"
"Total cash flow from financing activities","","-87876000000","-17974000000","-20890000000","-17716000000"

"Changes in Cash"
"Effect of exchange rate changes","","-","-","-","-"
"Change in cash and cash equivalents","","5624000000","-195000000","-636000000","7276000000"
'''
        cashflow = CashFlow('AAPL')
        csv = cashflow.to_csv(csv_dialect='unix')
        self.assertEqual(expected, csv)


    @mock.patch('yahoofinance.cashflow.requests.get', side_effect=mock_requests_get)
    def test_to_dfs(self, mock_get):
        cashflow = CashFlow('AAPL')
        dfs = cashflow.to_dfs()
        self.assertTrue(all(x in dfs.keys() for x in CashFlow._df_mapping.keys()))
        self.assertIn('Cash Flow', dfs.keys())
        assert(dfs['Cash Flow'].loc['Overall'].equals(dfs['Overall']))
        assert(dfs['Cash Flow'].loc['Operating activities'].equals(dfs['Operating activities']))
        assert(dfs['Cash Flow'].loc['Investment activities'].equals(dfs['Investment activities']))
        assert(dfs['Cash Flow'].loc['Financing activities'].equals(dfs['Financing activities']))
        assert(dfs['Cash Flow'].loc['Changes in Cash'].equals(dfs['Changes in Cash']))


if __name__ == '__main__':
    main()