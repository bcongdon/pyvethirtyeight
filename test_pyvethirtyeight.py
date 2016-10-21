from pyvethirtyeight import President, Senate
import unittest


class TestPresidentialForecasts(unittest.TestCase):
    def setUp(self):
        self.fte = President()

    def validate_forecast(self, forecast):
        assert forecast
        assert forecast.date
        assert forecast.candidate
        for model in ['polls', 'plus', 'now']:
            assert model in forecast.models

    def test_latest_models(self):
        forecasts = self.fte.latest_forecasts()
        for x in forecasts:
            self.validate_forecast(x)

    def test_all_models(self):
        forecasts = self.fte.all_forecasts()
        for x in forecasts:
            self.validate_forecast(x)

    def test_current_leader(self):
        d = self.fte.data
        self.validate_forecast(self.fte.current_leader())


class TestSenateForecasts(unittest.TestCase):
    def setUp(self):
        self.fte = Senate()

    def test_senate_latest(self):
        d = self.fte.data
        import json
        with open('out.json', 'w+') as f:
            f.write(json.dumps(d))

if __name__ == '__main__':
    unittest.main()
