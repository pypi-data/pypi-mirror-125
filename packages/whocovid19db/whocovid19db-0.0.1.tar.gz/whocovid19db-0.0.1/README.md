# WHO Covid-19 Database
Export the [WHO Covid-19 Database](https://search.bvsalud.org/global-literature-on-novel-coronavirus-2019-ncov/) to a Pandas DataFrame.

## Installation
```$ pip install whocovid19db```

## Usage
```# Import the Exporter class:
from whocovid19db import Exporter

# Create a new instance:
exp = Exporter()

# Export 5 documents from 2021/Oct/29 to 2021/Oct/30:
df = exp.get_df(date_interval=(20211029, 20211030), count=5)
```