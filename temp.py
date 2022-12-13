import datetime as dt
import numpy as np
import pandas as pd
from data import getDateRange, getWhaleData

a, b = getDateRange('ETH')
print(np.datetime64(a))
print(a+dt.timedelta(days=1))

whale_data = getWhaleData('ETH', from_date=a, to_date=b, interval=dt.timedelta(days=1), threshold=1000)
print(whale_data)
