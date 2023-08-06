# Basic Openweathermap API wrapper

## Why

This is an extremely simple wrapper around the Openweathermap OneCall API. It currently only supports forecasts. As it
is designed to be simple to use at the expense of features, the data is flattened from the nested structure to a single
dictionary for each forecast. In the process some data points are dropped.

Users that are interested in the complete set of data points are encouraged to open an issue or submit a pull request.

## Setup

1. Obtain an Openweathermap API key at [openweathermap.org](https://www.openweathermap.org/api)
2. Save the api key in a file '.api.txt' or the environment variable 'OPENWEATHERMAP_API_KEY'

## Usage

```python
from openweathermap import get_daily_forecast, APIError

try:
    forecast = get_daily_forecast(49.24966, -123.11934)  # Vancouver, BC, Canada
except APIError as e:
    # Deal with missing/incorrect API key or failed requests
    print(e)
```

Example return value for one day:
```json
{
  "dt": "2021-10-29T13:00:00",
  "sunrise": "2021-10-29T08:56:00",
  "sunset": "2021-10-29T18:56:09",
  "clouds": 28,
  "snow": None,
  "rain": None,
  "pop": 0.26,
  "wind_speed": 5.32,
  "wind_deg": 283,
  "wind_gust": 7.76,
  "humidity": 72,
  "temp_day": 282.15,
  "temp_morn": 281.22,
  "temp_eve": 280.99
}
```