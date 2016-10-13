from pyvethirtyeight import FiveThirtyEight
import unittest


class TestStringMethods(unittest.TestCase):
    def setUp(self):
        self.fte = FiveThirtyEight()

    def validate_forcast(self, forecast):
        assert forecast
        assert forecast.date
        assert forecast.candidate
        for model in ['polls', 'plus', 'now']:
            assert model in forecast.models

    def test_latest_models(self):
        forecasts = self.fte.latest_forecasts()
        for x in forecasts:
            self.validate_forcast(x)

    def test_all_models(self):
        forecasts = self.fte.all_forecasts()
        for x in forecasts:
            self.validate_forcast(x)

    def test_current_leader(self):
        self.validate_forcast(self.fte.current_leader())

if __name__ == '__main__':
    unittest.main()
