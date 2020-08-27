import pandas as pd
import yfinance as yf
import operator
import io
import urllib, base64
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('agg')
import matplotlib.dates as mdates
from datetime import date, time, datetime

from .models import Stock, DetailPage, Price

def stock_find_single(stk_name, lower_day, lowest_day, lower_control, lowest_control, allow_duplicates):
    stk = Stock.objects.get(stock=stk_name)
    historical_data = stk.get_prices().all()
    historical_data = pd.DataFrame.from_dict(historical_data.values())
    young = []
    l = len(historical_data)
    i = -1
    while i < l - 1:
        i += 1
        if ((historical_data.iloc[i]["close_price"] - historical_data.iloc[i]["open_price"]) > 0):
            m = "Rise"
        else:
            m = "Fall"
        if (m == "Fall"):
            open_price_at_fall = historical_data.iloc[i]["open_price"]
            id_list = [ historical_data.iloc[i]["id"] ]
            for k in range(i + 1, l):
                id_list.append(historical_data.iloc[k]["id"])
                open_price_today = historical_data.iloc[k]["open_price"]
                open_price_at_fall = max(open_price_today, open_price_at_fall)
                if ((historical_data.iloc[k]["close_price"] - historical_data.iloc[k]["open_price"]) > 0):
                    m1 = "Rise"
                else:
                    m1 = "Fall"
                if (k - i < lower_day):
                    if (m1 == "Rise"):
                        i = k + 1
                        break

                if (m1 == "Rise"):
                    if (lowest_control == True):
                        if (k >= lowest_day):
                            b = []
                            for m in range(1, lowest_day + 1):
                                b.append(
                                    historical_data.iloc[k - m]["low_price"])
                            bmin = min(b)
                            if (open_price_today >= bmin):
                                continue
                    if (lower_control == False):
                        a = [-1]
                        for s in range(k + 1, min(k + 8, l)):
                            a.append(historical_data.iloc[s]["high_price"])
                        a = max(a)
                        young.append(
                            [historical_data.iloc[k]["date"],
                             historical_data.iloc[k]["close_price"], a, id_list])
                    else:
                        if ((historical_data.iloc[k]["close_price"] - open_price_at_fall) > 0):
                            a = [-1]
                            for s in range(k + 1, min(k + 8, l)):
                                a.append(historical_data.iloc[s]["high_price"])
                            a = max(a)
                            young.append([historical_data.iloc[k]["date"],
                                          historical_data.iloc[k]["close_price"], a, id_list])
                    if (not allow_duplicates):
                        i = k + 1
                    break
    return young

def create_stock_bar_chart(dates, y_open, y_close):
    y_open = list(y_open)
    print(y_open)
    y_close = list(y_close)
    print(type(y_close))
    
    height_list = list(map(operator.sub, y_close, y_open))
    color_list = list(map(lambda x: 'red' if x >= 0 else 'green', 
                height_list))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.bar(x=dates, height=height_list, bottom=y_open, color=color_list)
    fig = plt.gcf()
    # convert into dtring buffer
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string =base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return uri
