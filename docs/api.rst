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


**Note: All of the below classes below are experimental (and for now archived into legacy) and results may
vary significantly as they data is scraped from the website.
Use at your own risk!**

Balance Sheet
-------------

.. autoclass:: yahoofinance.legacy.BalanceSheet
    :members:

.. autoclass:: yahoofinance.legacy.BalanceSheetQuarterly
    :members:


Cash Flow
---------

.. autoclass:: yahoofinance.legacy.CashFlow
    :members:

.. autoclass:: yahoofinance.legacy.CashFlowQuarterly
    :members:


Income Statement
----------------

.. autoclass:: yahoofinance.legacy.IncomeStatement
    :members:

.. autoclass:: yahoofinance.legacy.IncomeStatementQuarterly
    :members:

Asset Profile
-------------

.. autoclass:: yahoofinance.legacy.AssetProfile
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
