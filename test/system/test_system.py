"""
This is a very sloppy way to do system tests, but just a nice way to sanity check.
Requires internet connectivity.
"""

import pytest
from yahoofinance import *

@pytest.fixture
def asset_profile(scope='module'):
    return AssetProfile('AAPL')

# def test_asset_profile_csv(asset_profile):
#     csv = asset_profile.to_csv()

# def test_asset_profile_dfs(asset_profile):
#     dfs = asset_profile.to_dfs()


#### Cash Flow ####

@pytest.fixture
def cash_flow(scope='module'):
    return CashFlow('AAPL')

@pytest.fixture
def cash_flow_qtr(scope='module'):
    return CashFlowQuarterly('AAPL')


def test_cash_flow_csv(cash_flow):
    csv = cash_flow.to_csv()

def test_cash_flow_dfs(cash_flow):
    dfs = cash_flow.to_dfs()

def test_cash_flow_qtr_csv(cash_flow_qtr):
    csv = cash_flow_qtr.to_csv()

def test_cash_flow_qtr_dfs(cash_flow_qtr):
    dfs = cash_flow_qtr.to_dfs()


#### Balance Sheet ####

@pytest.fixture
def balance_sheet(scope='module'):
    return BalanceSheet('AAPL')

@pytest.fixture
def balance_sheet_qtr(scope='module'):
    return BalanceSheetQuarterly('AAPL')


def test_balance_sheet_csv(balance_sheet):
    csv = balance_sheet.to_csv()

def test_balance_sheet_dfs(balance_sheet):
    dfs = balance_sheet.to_dfs()

def test_balance_sheet_qtr_csv(balance_sheet_qtr):
    csv = balance_sheet_qtr.to_csv()

def test_balance_sheet_qtr_dfs(balance_sheet_qtr):
    dfs = balance_sheet_qtr.to_dfs()


#### Income Statement ####

@pytest.fixture
def income_statement(scope='module'):
    return IncomeStatement('AAPL')

@pytest.fixture
def income_statement_qtr(scope='module'):
    return IncomeStatementQuarterly('AAPL')


def test_income_statement_csv(income_statement):
    csv = income_statement.to_csv()

def test_income_statement_dfs(income_statement):
    dfs = income_statement.to_dfs()

def test_income_statement_qtr_csv(income_statement_qtr):
    csv = income_statement_qtr.to_csv()

def test_income_statement_qtr_dfs(income_statement_qtr):
    dfs = income_statement_qtr.to_dfs()

#### Historical Data ####
@pytest.fixture
def historical_prices(scope='module'):
    return HistoricalPrices('AAPL', '2018-01-01', '2018-01-10')


def test_historical_prices_csv(historical_prices):
    csv = historical_prices.to_csv()

def test_historical_prices_dfs(historical_prices):
    dfs = historical_prices.to_dfs()
