# -*- coding: utf-8 -*-
# !/usr/bin/env python
# author: zhnlk

"""
利用个股一分钟数据，写一个合成任意分钟的通用函数，使用000001.SZ平安银行的数据。

要点提炼：
1. 获取数据
2. 合成K线
3. pd与np的使用
"""

import numpy as np
import pandas as pd
from mootdx.quotes import Quotes


def get_1min_k_line() -> pd.DataFrame:
    client = Quotes.factory(market='std')
    k_line = client.bars(symbol='000001', frequency=7, offset=100)
    return k_line


def generate_n_min_k(df: pd.DataFrame, n: int) -> pd.DataFrame:
    data_list = []
    for i in range(0, df.index.size, n):
        _high = max(df.iloc[i:i + n]['high'])
        _low = min(df.iloc[i:i + n]['low'])
        _open = df.iloc[i]['open']
        _close = df.iloc[i]['close']
        _vol = sum(df.iloc[i:i + n]['vol'])
        _amount = sum(df.iloc[i:i + n]['amount'])
        _year = df.iloc[i]['year']
        _month = df.iloc[i]['month']
        _day = df.iloc[i]['day']
        _hour = df.iloc[i + n - 1]['hour']
        _minute = df.iloc[i + n - 1]['minute']
        _datetime = df.iloc[i + n - 1]['datetime']
        data_list.append([_open, _close, _high, _low, _vol, _amount, _year, _month, _day, _hour, _minute, _datetime])

    dff = pd.DataFrame(np.array(data_list),
                       columns=df.columns)
    return dff


def generate_5min_k(df: pd.DataFrame):
    print(generate_n_min_k(df, 5))


if __name__ == '__main__':
    k_1min = get_1min_k_line()
    print(k_1min)
    generate_5min_k(k_1min)
