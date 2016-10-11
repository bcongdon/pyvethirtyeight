from pyvethirtyeight import FiveThirtyEight
import re

def test_get_soup():
    f = FiveThirtyEight()
    print f._extract_data()
    assert False