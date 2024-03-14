from datetime import datetime, timedelta
import requests as rq
from bs4 import BeautifulSoup

# # https://pypi.org/project/facebook-scraper/
# # https://pypi.org/project/twitter-scraper/

# # r = rq.get('https://currency-strength.com/en')
# # print(r.status_code)
# # soup = BeautifulSoup(r.content, "html.parser")

# -------------------------------------------------------------------------------
tod = datetime.now()
d = timedelta(days=3)
a = tod - d
millisec = a.timestamp() * 1000
print(millisec)
print(str(millisec).split('.')[0])

# 1645376812340.995
# 1645635948994
# -------------------------------------------------------------------------------
# start = '2022-02-23 05:00:00'

# dt_object = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
# print(type(dt_object))

# -------------- auto get increasing 5 minutes --------------
timestamps = [1645567200000, 1645694000818, 1645434908135, 1645567500000, 1644830953113]

for timestamp in timestamps:
    dt_object = datetime.fromtimestamp(timestamp/1000.0)
    print("dt_object =", dt_object)