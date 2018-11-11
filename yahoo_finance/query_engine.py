import urllib
from http.cookiejar import CookieJar
import re
from datetime import date, datetime
import requests

from .data_configs import DataFormat, DataEvent, DataFrequency, Locale


class QueryEngine:
    """
    Engine that is able to query historical data from Yahoo.
    """
    def __init__(self, locale=Locale.US):
        self._base_url = Locale.locale_url(locale)

    def fetch_historial_data(self, instrument, start_date, end_date, date_format_string="%Y-%m-%d", event=DataEvent.HISTORICAL_PRICES, frequency=DataFrequency.DAILY):
        min_date = date(1970,1,1)

        if not isinstance(start_date, date):
            start_date = datetime.strptime(start_date, date_format_string).date()
        
        if not isinstance(end_date, date):
            end_date = datetime.strptime(end_date, date_format_string).date()

        start_period = int((start_date - min_date).total_seconds())
        end_period = int((end_date - min_date).total_seconds())

        cookie, crumb = self._find_cookie_crumb_pair()

        url = 'https://query1.finance.yahoo.com/v7/finance/download/{i}'
        r= requests.get(url.format(i=instrument),
            cookies={'B': cookie},
            params={
                "period1": start_period,
                "period2": end_period,
                "interval": frequency,
                "event": event,
                "crumb": crumb
            }
        )

        return r.text
        


    def _find_cookie_crumb_pair(self):
        cj = CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        r = opener.open(self._base_url + "/quote/AAPL")

        cookie_piece = None
        for c in cj:
            if c.name == 'B':
                cookie_piece = c.value
                break
        
        if cookie_piece is None:
            raise ValueError("Cookie not found")
        
        try:
            res = r.read().decode()
        except:
            raise ValueError("Malformed HTML page, check if internet connection is stable")

        crumb = None
        pattern = r'"CrumbStore":{"crumb":"(.+?)"}'
        matcher = re.search(pattern, res)
        if matcher:
            crumb = matcher.group(1)
        else:
            raise ValueError("Crumb not found")

        crumb = crumb.replace('\\u002F', '/')

        return cookie_piece, crumb

