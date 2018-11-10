class Locale:
    AU = "au"
    US = ""
    CA = "ca"

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