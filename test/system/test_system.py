"""
This is a very sloppy way to do system tests, but just a nice way to sanity check.
Requires internet connectivity.
"""

import pytest
from yahoofinance import *

#### Historical Data ####
@pytest.fixture
def historical_prices(scope='module'):
    return HistoricalPrices('AAPL', '2018-01-01', '2018-01-10')


def test_historical_prices_csv(historical_prices):
    csv = historical_prices.to_csv()

def test_historical_prices_dfs(historical_prices):
    dfs = historical_prices.to_dfs()
