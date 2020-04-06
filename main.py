
from stocks import Stock
from etfdb import ETFDBCSV
import graphs

etf = ETFDBCSV('data/SPY-holdings-2020-03.csv')

stocks = []

for holding in etf.components[:200]:
    stock = Stock(holding.symbol)
    print(stock)
    stocks.append(stock)

res = graphs.plot_divYield_PE(stocks)
res.savefig('divYield_PE.png', dpi=1000)
res.show()
