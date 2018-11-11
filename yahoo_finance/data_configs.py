class Locale:
    AU = "au"
    US = ""
    CA = "ca"

    @staticmethod
    def locale_url(locale):
        if locale == Locale.US:
            # Special case because the US is special
            return "https://finance.yahoo.com/quote"
        else:
            return "https://{}.finance.yahoo.com/quote".format(locale)

class DataEvent:
    HISTORICAL_PRICES = "history"
    DIVIDENDS = "div"
    SPLITS = "splits"

class DataFrequency:
    DAILY = "1d"
    WEEKLY = "1wk"
    MONTHLY = "1mo"

class DataFormat:
    RAW = 'raw'
    SHORT = 'fmt'
    LONG = 'longFmt'

    _FORMATS = (RAW, SHORT, LONG)