import urllib.request
import pandas as pd


class Stock:
    def __init__(self, code, shares, costPrice):
        self.code = code
        self.shares = shares
        self.costPrice = costPrice
        self.valueRMB = self.shares * self.costPrice * 1
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
        x = content.decode('gbk').split(',')
        self.price = float(x[6])
        self.valueRMB = round(self.shares * self.priceRMB, 2)
        self.name = x[1]
        # self.tableString = self.code + " | " + self.name + " | " + str(self.price) + " | " + str(self.profit)
        url = "http://hq.sinajs.cn/list=HKDCNY"
        content = urllib.request.urlopen(url).read()
        # content2 = content.decode('gbk')
        x = content.decode('utf-8', 'ignore').split(',')
        exchange = float(x[7])
        self.priceRMB = round(self.price * exchange, 2)
        self.valueRMB = round(self.priceRMB * self.shares, 2)
        self.profit = round(self.valueRMB - self.cost, 2)


class ShareHolder:
    def __init__(self, name, initCaptical):
        self.name = name
        self.INITCAPITAL = initCaptical
        self.position = 0
        self.profit = self.position - self.INITCAPITAL
        self.percent = self.profit / self.INITCAPITAL


class Position:
    def __init__(self, SHARE_HOLDER_INIT, cash_floap):
        self.stockList = []
        columns = ['代码', '名称', '当前股价', '当前股价RMB', '成本股价RMB', '数量', '市值/元', '利润/元']
        self.df = pd.DataFrame(columns=columns)
        self.cash = round(SHARE_HOLDER_INIT + cash_floap, 2)
        self.equity = 0
        self.profit = 0

    def buy_stock(self, name, shares, price):
        stock = Stock(name, shares, price)
        self.stockList.append(stock)
        self.df = self.df.append(
                pd.DataFrame({'代码': [stock.code],
                              '名称': [stock.name],
                              '当前股价': [stock.price],
                              '当前股价RMB': [stock.priceRMB],
                              '成本股价RMB': [stock.costPrice],
                              '数量': [stock.shares],
                              '市值/元': [stock.valueRMB],
                              '利润/元': [stock.profit]}),
                ignore_index=True)

    def update(self):
        for stock in self.stockList:
            stock.updateValue()
            self.profit += stock.profit
            self.equity += stock.valueRMB
            self.df.loc[self.df['代码'] == stock.code] =\
                pd.DataFrame({'代码': [stock.code],
                              '名称': [stock.name],
                              '当前股价': [stock.price],
                              '当前股价RMB': [stock.priceRMB],
                              '成本股价RMB': [stock.costPrice],
                              '数量': [stock.shares],
                              '市值/元': [stock.valueRMB],
                              '利润/元': [stock.profit]})
        self.equity += self.cash


def get_cash_floap():
    csv_file = "webIndex\\record.csv"
    csv_data = pd.read_csv(csv_file, encoding='gbk')
    csv_df = pd.DataFrame(csv_data)
    cash_floap = csv_df["金额/元"].sum()
    return cash_floap