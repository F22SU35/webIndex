# coding=utf-8
from django.shortcuts import render
import webIndex.stock_func as sto


def runoob(request):
    sList = []
    SHARE_HOLDER_INIT = 0

    s1 = sto.ShareHolder('F22', 60000)
    s2 = sto.ShareHolder('Success', 40000)
    s3 = sto.ShareHolder('Mr', 40000)
    s4 = sto.ShareHolder('UFO', 20000)

    sList.append(s1)
    sList.append(s2)
    sList.append(s3)
    sList.append(s4)

    for s in sList:
        SHARE_HOLDER_INIT += s.INITCAPITAL
    cash_floap, cash_divided = sto.get_cash_floap()
    position = sto.Position(SHARE_HOLDER_INIT, cash_floap)

    position.buy_stock("hk03690", 500, 254.73)
    position.buy_stock("hk01810", 800, 27.39)
    position.update()

    for s in sList:
        s.cash_divided = round(cash_divided / SHARE_HOLDER_INIT * s.INITCAPITAL, 2)
        s.profit = round((position.equity - SHARE_HOLDER_INIT) / SHARE_HOLDER_INIT * s.INITCAPITAL, 2)
        s.profit_total = round(s.profit + s.cash_divided, 2)

    percent = round((position.equity - SHARE_HOLDER_INIT + cash_divided) / SHARE_HOLDER_INIT * 100, 2)

    stockList = position.stockList
    context = {'position_profit': position.profit,
               'percent': percent,
               'stocks': stockList,
               'share_holders': sList,
               'cash': position.cash,
               'equity': position.equity}

    return render(request, 'runoob.html', context)
