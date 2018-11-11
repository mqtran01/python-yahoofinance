Yahoo Finance Data for Python
=============================

Python module to get data readily available from Yahoo Finance. The data is retrieved directly from the website with no data changes.

**Warning: This package is undergoing development and implementation and interfaces may change drastically without notice.**

Installation
------------

Until the package is uploaded onto PyPi, this package will need to just be cloned and used.

For now, you will need to independently install the following packages:
- requests
- beautifulsoup4
- pandas (once it is implemented)

Usage
-----

To export the Profile data to CSV, it is simple!

If we are looking to export [Apple's Asset Profile](https://finance.yahoo.com/quote/AAPL/profile) we can do the following:
``` {.sourceCode .python}
>>> from yahoo_finance import yahoo_data as yd
>>> profile = yd.AssetProfile('AAPL')
>>> profile.to_csv('AAPL-profile.csv')
```
You can now find the profile information in a CSV file called `AAPL-profile.csv`.

Next steps include exporting other to a Pandas Dataframe, which would be the main reason why this project exists!

Optional Usage
-------------
We can add in a locale to choose a specific region to query from. For example, from Australia, we can query from the Australian Yahoo Finance website to get *marginally* faster query times. Using the Asset Profile example previously:

``` {.sourceCode .python}
>>> from yahoo_finance import yahoo_data as yd
>>> profile = yd.AssetProfile('AAPL', locale=Locale.AU)
>>> profile.to_csv('AAPL-profile.csv')
```

Current locales include:
- `Locale.AU` (Australia)
- `Locale.CA` (Canada)
- `Locale.US` (United States)


Documentation
-------------
Coming soon!


FAQs
----
1. Why did you make this?

I felt that financial data information is often restricted.

2. Can you make custom data manipulation filters to make the data more tailored to my use?

I do not intend to. My ethos is to enable financial data users to retrieve the data and use it their own way. I do not want to steal the data provided by

3. What happens when their website data changes and/or this project breaks?

Let me know and I'll do my best to fix it. Or even better, fork and make a pull request!

4. I want to contribute to this amazing project!

Fork and make a pull request!


5. I like you, I want to support you financially.

I don't have a support link yet (because this project just started), but if enough people are interested, I'll set one up someday.