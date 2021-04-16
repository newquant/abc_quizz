# -*- coding: utf-8 -*-
# !/usr/bin/env python
# author: zhnlk

"""
用TA-Lib中的MACD技术指标，根据最新的股票池数据，选出指标中MACD值向上突破0的股票池
要点提炼：
1. 使用ta-lib的MACD指标
2. 根据最新的股票池
3. MACD值向上突破的股票池


'''
MACD算法：（异同移动平均线 Moving Average Convergence / Divergence） Gerald Appel@1979-02-04
MACD=2*(DIF-DEA)

利用收盘价的快慢线之间的聚合与分离，对买卖时机做出研判的技术指标
1.计算EMA
    EMA(12) = 前一日EMA（12）×11/13+今日收盘价×2/13, 快线：快速移动平均线,一般取12日,
    EMA(26) = 前一日EMA（26）×25/27+今日收盘价×2/27, 慢线：慢速移动平均线,一般取26日
2.计算DIF
    DIF,差离值：EMA(12)-EMA(26)
3.计算IDF的9日EMA
    根据离差值计算其9日的EMA，即离差平均值，是所求的MACD值。为了不与指标原名相混淆，此值又名DEA或DEM
    今日DEA(MACD) = 前一日DEA×8/10+今日DIF×2/10
    计算出的DIF和DEA的数值均为正值或负值, 用(DIF-DEA)*2即为MACD柱状图。
'''
"""

import pandas as pd
import talib

from mootdx.quotes import Quotes

sz_50_csv = "../data/sz50_stocks.csv"


def get_macd(code: str):
    client = Quotes.factory(market='std')
    k_line = client.bars(symbol=code, frequency=9, offset=100)
    macd, signal, hist = talib.MACD(k_line['close'], fastperiod=12, slowperiod=26, signalperiod=9)
    if macd[-1:].values[0] > 0:
        return code


def stock_pool():
    sz50 = pd.read_csv(sz_50_csv)

    for s in [str(i[0]) for i in sz50.values]:
        ss = get_macd(s)
        if ss:
            print(ss)


if __name__ == '__main__':
    stock_pool()
