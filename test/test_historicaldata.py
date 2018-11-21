import unittest
from unittest import TestCase, mock, main
from yahoofinance import HistoricalPrices
from test.mock_framework import MockResponse


def mock_requests_get(*args, **kwargs):
    if 'history' in args[0]:
        with open('test/resources/Cookie.html') as file:
            return MockResponse(file.read())
    elif 'download' in args[0]:
        with open('test/resources/HistoricalData.csv') as file:
            return MockResponse(file.read())
    raise NotImplementedError('How did you even reach here?')


class TestHistoricalPrices(TestCase):

    @mock.patch('yahoofinance.historicaldata.requests.get', side_effect=mock_requests_get)
    def test_to_csv(self, mock_get):
        prices = HistoricalPrices('AAPL', '2018-10-10', '2018-10-16')
        csv = prices.to_csv()
        expected = """Date,Open,High,Low,Close,Adj Close,Volume
2018-11-09,205.550003,206.009995,202.250000,204.470001,204.470001,34365800
2018-11-12,199.000000,199.850006,193.789993,194.169998,194.169998,51135500
2018-11-13,191.630005,197.179993,191.449997,192.229996,192.229996,46882900
2018-11-14,193.899994,194.479996,185.929993,186.800003,186.800003,60801000
2018-11-15,188.389999,191.970001,186.899994,191.410004,191.410004,46478800
2018-11-16,190.500000,194.970001,189.460007,193.529999,193.529999,36208500
"""
        self.assertEqual(csv, expected)


    @mock.patch('yahoofinance.historicaldata.requests.get', side_effect=mock_requests_get)
    def test_to_csv_unix_delim(self, mock_get):
        prices = HistoricalPrices('AAPL', '2018-10-10', '2018-10-16')
        csv = prices.to_csv(csv_dialect='unix')
        expected = """Date,Open,High,Low,Close,Adj Close,Volume
2018-11-09,205.550003,206.009995,202.250000,204.470001,204.470001,34365800
2018-11-12,199.000000,199.850006,193.789993,194.169998,194.169998,51135500
2018-11-13,191.630005,197.179993,191.449997,192.229996,192.229996,46882900
2018-11-14,193.899994,194.479996,185.929993,186.800003,186.800003,60801000
2018-11-15,188.389999,191.970001,186.899994,191.410004,191.410004,46478800
2018-11-16,190.500000,194.970001,189.460007,193.529999,193.529999,36208500
"""
        self.assertEqual(csv, expected)

    @mock.patch('yahoofinance.historicaldata.requests.get', side_effect=mock_requests_get)
    def test_to_dfs(self, mock_get):
        prices = HistoricalPrices('AAPL', '2018-10-10', '2018-10-16')
        dfs = prices.to_dfs()
        self.assertIn('Historical Prices', dfs.keys())


if __name__ == '__main__':
    main()