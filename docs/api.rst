.. _api:

API Documentation
=================

Please note that the API is currently under development and things may
change rapidly!

Core Interface
--------------

.. autoclass:: yahoofinance.interfaces.IYahooData
    :members:


Historical Data
---------------

.. autoclass:: yahoofinance.HistoricalPrices
    :members:


**Note: All of the below classes below are experimental and results may
vary significantly as they data is scraped from the website.
Use at your own risk!**

Balance Sheet
-------------

.. autoclass:: yahoofinance.BalanceSheet
    :members:

.. autoclass:: yahoofinance.BalanceSheetQuarterly
    :members:


Cash Flow
---------

.. autoclass:: yahoofinance.CashFlow
    :members:

.. autoclass:: yahoofinance.CashFlowQuarterly
    :members:


Income Statement
----------------

.. autoclass:: yahoofinance.IncomeStatement
    :members:

.. autoclass:: yahoofinance.IncomeStatementQuarterly
    :members:

Asset Profile
-------------

.. autoclass:: yahoofinance.AssetProfile
    :members:


Additional Config
-----------------
.. autoclass:: yahoofinance.Locale
    :members:

.. autoclass:: yahoofinance.DataEvent
    :members:

.. autoclass:: yahoofinance.DataFrequency
    :members:

.. autoclass:: yahoofinance.DataFormat
    :members:
