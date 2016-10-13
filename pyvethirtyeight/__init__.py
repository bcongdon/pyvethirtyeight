import requests
from bs4 import BeautifulSoup
import re
import json
from datetime import timedelta, datetime
from collections import namedtuple
import dateparser

Forecast = namedtuple('Forecast', ['date', 'party', 'candidate', 'models'])


class FiveThirtyEight:

    forecast_url = 'http://projects.fivethirtyeight.com/2016-election-forecast'

    def __init__(self):
        self._data = None
        self._updated_at = None

    def _get_soup(self):
        html = requests.get(FiveThirtyEight.forecast_url).text
        self._soup = BeautifulSoup(html, 'html.parser')
        return self._soup

    def _get_data(self):
        soup = self._get_soup()
        race_re = re.compile(r'race\.stateData')
        script = soup.find_all('script', text=race_re)[0]
        json_str = race_re.split(script.text)[1].split(';')[0]
        json_str = json_str[json_str.find('{') - 1:]
        return json.loads(json_str)

    def _dict_to_forcast(self, forecast_dict):
        return Forecast(date=dateparser.parse(forecast_dict['date']),
                        party=forecast_dict['party'],
                        candidate=forecast_dict['candidate'],
                        models=forecast_dict['models'])

    def latest_forecasts(self):
        return [self._dict_to_forcast(x) for x in
                self.data['latest'].values()]

    def all_forecasts(self):
        return [self._dict_to_forcast(x) for x in
                self.data['forecasts']['all']]

    def current_leader(self, model='polls'):
        return max(self.latest_forecasts(),
                   key=lambda x: x.models[model]['winprob'])

    @property
    def data(self):
        if (not self._data or not self._updated_at or
                datetime.now() - timedelta(minutes=10) > self._updated_at):
            self._data = self._get_data()
        return self._data
