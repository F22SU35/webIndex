# coding=utf-8
from django.shortcuts import render

import urllib.request
import pandas as pd
from django.http import HttpResponse


class Stock:
    def __init__(self, code, shares, costPrice):
        self.code = code
        self.shares = shares
        self.costPrice = costPrice
        self.value = self.shares * self.costPrice
        self.cost = self.shares * self.costPrice
        self.profit = 0
        self.name = ""
        self.tableString = ""
        self.price = 0
        self.priceRMB = self.price

    def updateValue(self):
        url = "http://hq.sinajs.cn/list=" + self.code
        content = urllib.request.urlopen(url).read()
        # content2 = content.decode('gbk')
        x = content.decode('utf-8', 'ignore').split(',')
        self.price = float(x[4])
        self.valueRMB = self.shares * self.priceRMB
        self.name = x[1].encode("utf-8")
        #self.tableString = self.code + " | " + self.name + " | " + str(self.price) + " | " + str(self.profit)
        url = "http://hq.sinajs.cn/list=HKDCNY"
        content = urllib.request.urlopen(url).read()
        # content2 = content.decode('gbk')
        x = content.decode('utf-8', 'ignore').split(',')
        exchange = float(x[7])
        self.priceRMB = self.price * exchange
        self.valueRMB = self.priceRMB * self.shares
        self.profit = self.valueRMB - self.cost


def print_table2html():
    columns = ['代码', '名称', '当前股价', '当前股价RMB', '成本股价RMB', '数量', '利润/元']
    df = pd.DataFrame(columns=columns)

    stock1 = Stock("hk03690", 500, 254.734)
    stock2 = Stock("hk01810", 800, 27.394)
    stockList = []
    profitSum = 0

    stockList.append(stock1)
    stockList.append(stock2)

    for stock in stockList:
        stock.updateValue()
        profitSum += stock.profit

        df = df.append(
            pd.DataFrame({'代码': [stock.code],
                          '名称': [stock.name],
                          '当前股价': [stock.price],
                          '当前股价RMB': [stock.priceRMB],
                          '成本股价RMB': [stock.costPrice],
                          '数量': [stock.shares],
                          '利润/元': [stock.profit]}),
            ignore_index=True)

    df = df[['代码', '名称', '当前股价', '当前股价RMB', '成本股价RMB', '数量', '利润/元']]
    return profitSum, df.to_html(table_id='customers')


def print_web():
    title = "<div align=\"center\"><font size=\"6\"><b><br/>Fund Position<b></font></div>"
    tableStyle = "<head><style type=\"text/css\">#customers  {  font-family:\"Trebuchet MS\", Arial, Helvetica, sans-serif;  width:100%;  border-collapse:collapse;  }#customers td, #customers th   {  font-size:1em;  border:1px solid #88CFDB;  padding:3px 7px 2px 7px;  }#customers th   {  font-size:1.1em;  text-align:left;  padding-top:5px;  padding-bottom:4px;  background-color:#88CFDB;  color:#ffffff;  }#customers tr.alt td   {  color:#000000;  background-color:##88CFDB;  }</style></head>"

    profitSum, tableHtml = print_table2html()
    profitStr = "ProfitSum: " + str(profitSum) + "RMB"
    s1 = "<font size = \"5\" color = \"red\" ><b><br/>"
    s2 = "<b></font>"
    s3 = s1 + profitStr + s2

    timeStr = "<div id=\"linkweb\"></div><script>setInterval(\"linkweb.innerHTML=new Date().toLocaleString()+\' Week\'+\'0123456\'.charAt(new Date().getDay());\",1000);</script>"
    return tableStyle + title + timeStr + tableHtml + s3


def runoob(request):
    #strr = print_table2html()
    #context = {}
    #context['hello'] = strr
    #return render(request, 'runoob.html', context)
    return HttpResponse(bytes(print_web(), encoding = "utf8"))
