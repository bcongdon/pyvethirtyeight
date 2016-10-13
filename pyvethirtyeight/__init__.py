"""
A Python wrapper for the 2016 FiveThirtyEight Presidential Election Forecast
"""

import requests
from bs4 import BeautifulSoup
import re
import json
from datetime import timedelta, datetime
from collections import namedtuple
import dateparser

__version__ = '1.0.2'


Forecast = namedtuple('Forecast', ['date', 'party', 'candidate', 'models'])


class FiveThirtyEight:

    forecast_url = 'http://projects.fivethirtyeight.com/2016-election-forecast'

    def __init__(self):
        self._data = None
        self._updated_at = None

    def _get_soup(self):
        """
        Requests the FiveThirtyEight forecaster page and returns a
        BeautifulSoup object
        """
        html = requests.get(FiveThirtyEight.forecast_url).text
        self._soup = BeautifulSoup(html, 'html.parser')
        return self._soup

    def _extract_data(self, soup):
        """
        Extracts the JSON payload from a FiveThirtyEight forecast tracker soup.
        Returns a dict
        """
        race_re = re.compile(r'race\.stateData')

        # Searches for the script tag that contains the JSON data
        script = soup.find_all('script', text=race_re)[0]

        # Select the 'race.stateData' line of javascript
        json_str = race_re.split(script.text)[1].split(';')[0]
        # Slice only the JSON component of the data line
        json_str = json_str[json_str.find('{') - 1:]

        # Return the JSON data as a dict
        return json.loads(json_str)

    def _dict_to_forcast(self, forecast_dict):
        """
        Returns a Forecast namedtuple from a FiveThirtyEight forecast dict
        """
        return Forecast(date=dateparser.parse(forecast_dict['date']),
                        party=forecast_dict['party'],
                        candidate=forecast_dict['candidate'],
                        models=forecast_dict['models'])

    def latest_forecasts(self):
        """
        Returns a list of most-recent Forecasts
        """
        return [self._dict_to_forcast(x) for x in
                self.data['latest'].values()]

    def all_forecasts(self):
        """
        Returns a list containing all known Forecasts
        """
        return [self._dict_to_forcast(x) for x in
                self.data['forecasts']['all']]

    def current_leader(self, model='polls'):
        """
        Returns the Forecast of the candidate with the highest win probability
        in the latest set of Forecasts.

        The model argument can be:
            * 'polls' for the polls-only model
            * 'plus' for the pulls-plus model
            * 'now' for the now-cast model
        """
        return max(self.latest_forecasts(),
                   key=lambda x: x.models[model]['winprob'])

    @property
    def data(self):
        """
        Property to hold the current JSON dict of the FiveThirtyEight
        forecaster

        Caches for 10 minutes
        """
        if (not self._data or not self._updated_at or
                datetime.now() - timedelta(minutes=10) > self._updated_at):
            self._data = self._extract_data(self._get_soup())
        return self._data
