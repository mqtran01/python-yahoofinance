class Locale:
    """Provides locale information to any :class:`IYahooData` implementations.

    By using your local domain, it may speed up queries by a `miniscule` amount or bypass
        certain country domain filters and restrictions.
    """

    #: Uses the Australian domain. E.g. https://au.finance.yahoo.com/quote/AAPL/
    AU = "au"
    #: Uses the United States domain. E.g. https://finance.yahoo.com/quote/AAPL/
    US = ""
    #: Uses the Canadian domain. E.g. https://ca.finance.yahoo.com/quote/AAPL/
    CA = "ca"

    @staticmethod
    def locale_url(locale):
        """This is an auxilary method to determine the domain url for a locale.

        :param locale: A :class:`Locale` string constant. A hard coded string can also be used
            if the 2 letter domain is known.
        :return: :class:`string` object
        :rtype: `string`
        """
        if locale == Locale.US:
            # Special case because the US is special
            return "https://finance.yahoo.com/quote"
        else:
            return "https://{}.finance.yahoo.com/quote".format(locale)

class DataEvent:
    """Provides data event information for :class:`HistoricalData`.

    Yahoo provides 3 different types of historical data sets.
    """

    #: Used to retrieve historical data.
    # E.g. https://finance.yahoo.com/quote/AAPL/history
    HISTORICAL_PRICES = "history"

    #: Used to retrieve dividend information.
    # E.g. https://finance.yahoo.com/quote/AAPL/history?filter=div
    DIVIDENDS = "div"

    #: Used to retrieve company stock split information. (Very rare in reality)
    # E.g. https://finance.yahoo.com/quote/AAPL/history?filter=split
    SPLITS = "splits"

class DataFrequency:
    """Provides data frequency information for :class:`HistoricalData`.

    Yahoo provides data at 3 different time granuarities.
    """

    #: Retrieve data at daily intervals.
    DAILY = "1d"

    #: Retrieve data at weekly intervals.
    WEEKLY = "1wk"

    #: Retrieve data at montly intervals.
    MONTHLY = "1mo"

class DataFormat:
    """Selects the way data is formatted for :class:`IYahooData` implementations."""

    #: Provides a raw numerical value. E.g. 1000000.0
    RAW = 'raw'

    #: Provides a shorter formatted value. E.g. 1.0M
    SHORT = 'fmt'

    #: Provides a longer formatted value. E.g. 1,000,000.0
    LONG = 'longFmt'

    _FORMATS = (RAW, SHORT, LONG)