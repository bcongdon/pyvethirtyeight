# PyveThirtyEight
> A Python wrapper for the 2016 [FiveThirtyEight](projects.fivethirtyeight.com/2016-election-forecast/) Presidential Election Forecast 

[![PyPI version](https://badge.fury.io/py/pyvethirtyeight.svg)](https://badge.fury.io/py/pyvethirtyeight)
[![Build Status](https://travis-ci.org/bcongdon/pyvethirtyeight.svg?branch=master)](https://travis-ci.org/bcongdon/pyvethirtyeight)

## Installation
```
pip install pyvethirtyeight
```

## Usage
```python
from pyvethirtyeight import President, Senate

# Presidential Election Forecasts
f = President()

# Latest Forecasts (Unordered)
latest = f.latest_forecasts()
latest[0].party # 'D'

# Current Leader (returns Forecast of latest leader)
leader = f.current_leader()
print(leader.models['plus']['winprob']) # 83.99

# Current Leader by Model
leader = f.current_leader(model='now')
print(leader.models['now']['winprob']) # 90.4

# All Forecasts
all_forecasts = f.all_forecasts()

# Same methods also work with Senate predictions
s = Senate()
print(s.latest_forecasts()[0].models['polls']['winprob']) # 67.33596
```

#### The Forecast Object
A `Forecast` is the prediction of the FiveThirtyEight model for a particular candidate at a particular moment in time

A `Forecast` has keys:

	- date (datetime) -> Forecast date
	- party (str) -> Candidate's party initial
	- candidate (str) -> Candidate's name
	- models (Dict) -> Dict of model predictions associated with candidate