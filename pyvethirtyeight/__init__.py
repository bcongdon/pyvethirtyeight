import requests
from bs4 import BeautifulSoup
import re
import json

models = {
          'polls_only': '',
          'polls_plus': '#plus',
          'now_cast': '#now'
          }


class FiveThirtyEight:
    def __init__(self, model='polls_only'):
        self.model = model

    def _get_soup(self):
        html = requests.get('http://projects.fivethirtyeight.com/2016-election-forecast/').text
        self._soup = BeautifulSoup(html, 'html.parser')
        return self._soup

    def _extract_data(self):
        soup = self._get_soup()
        race_re = re.compile(r'race\.stateData')
        script = soup.find_all('script', text=race_re)[0]
        json_data = race_re.split(script.text)[1].split(';')[0][2:]
        print json.loads(json_data).keys()

    @property
    def model(self):
        return self._model

    @model.setter
    def x(self, model):
        if model not in models:
            raise ValueError('Unsupported model', model)
        self._get_soup()
