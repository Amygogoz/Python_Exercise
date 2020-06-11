# Data Source: https://www.kaggle.com/dgawlik/nyse#prices-split-adjusted.csv

import pandas as pd

"""题目一"""
# 1. 从fundemantals.csv开始！fundemantals.csv 是这些股票的年报数据

sp_data = pd.read_csv('fundamentals.csv',index_col=0)
# print(sp_data.info())

#     S&P500股票在2015年net income的均值是多少？最大值比最小值多多少？

avg_net_income = sp_data[sp_data['For Year']==2015]['Net Income'].mean()
print('The average net income is {}.'.format(avg_net_income))

max_min = sp_data[sp_data['For Year']==2015]['Net Income'].max() - sp_data[sp_data['For Year']==2015]['Net Income'].min()
print('The difference of max and min net income is {}.'.format(max_min))

#     S&P500股票在2016年的固定资产（fixed assets）占总资产(total assets)比例的均值是多少？固定资产占总资产比例最小的股票的代码（ticker symbol）是什么？
avg_ratio = sp_data[sp_data['For Year']==2016]['Fixed Assets'].sum() / sp_data[sp_data['For Year']==2016]['Total Assets'].sum()
print('The average fixed assets ratio is {}'.format(avg_ratio))

sp_data['Fixed Assets Ratio'] = sp_data[sp_data['For Year']==2016]['Fixed Assets'] / sp_data[sp_data['For Year']==2016]['Total Assets']
min_ratio = sp_data['Fixed Assets Ratio'].min()
min_ticker_sym = sp_data[sp_data['Fixed Assets Ratio']==min_ratio]['Ticker Symbol']
print('The ticker symbol with minimum fixed ratio is {}.\nThe ratio is {}.'.format(min_ticker_sym, min_ratio))


"""题目二"""
# 2. 加入securities.csv~ securities.csv包含了这些股票的基本信息

secu_data = pd.read_csv('securities.csv')
print(secu_data.columns)

#     请列举出各个sector中的加入时间最早的股票名称

secu_data['Date first added'] = pd.to_datetime(secu_data['Date first added'])          # secu_data['Date first added'].astype('datetime64[ns]')
secu_data['Rank_by_Sector'] = secu_data.groupby('GICS Sector')['Date first added'].rank(method='dense')
first_added = secu_data[secu_data['Rank_by_Sector']==1]
print(first_added[['GICS Sector','Security','Date first added']])

#     请列举出每一个州中加入时间最晚的股票名称

secu_data['State'] = secu_data['Address of Headquarters'].apply(lambda x:x.split(',')[-1])
secu_data['Rank_by_State'] = secu_data.groupby('State')['Date first added'].rank(method='dense',ascending=False)
last_added = secu_data[secu_data['Rank_by_State']==1]
print(last_added[['State','Security']])

"""题目三"""
# 3. merge! 现在你需要同时处理来自两个表中的信息了

#     请思考，合并两个表的信息的时候，我们应该用什么样的准则对齐它们

merge_data = pd.merge(sp_data,secu_data,on='Ticker Symbol')

#     请列举每个sector在2013-2016年累计Research&Development的总投入

df1 = merge_data[merge_data['Period Ending'].apply(lambda x:x.split('-')[0] in ['2013','2014','2015','2016'])]
rd_by_sec = df1.groupby('GICS Sector')['Research and Development'].sum()

print(rd_by_sec)

#     请列举出每个sector中，在2013-2016年累计Research&development投入最大的3家公司的名称以及投入的数值

rd_by_sec_comp = df1.groupby(['GICS Sector','Ticker Symbol'])['Research and Development'].sum()
rd_by_sec_comp = rd_by_sec_comp.reset_index()
rd_by_sec_comp['Rank'] = rd_by_sec_comp.groupby('GICS Sector')['Research and Development'].rank(method='dense',ascending=False)

top_rd = rd_by_sec_comp[(rd_by_sec_comp['Rank']<=3) & (rd_by_sec_comp['Research and Development'] != 0)]

print(top_rd)

"""题目四"""
# 4. 现在让我们来看看更加复杂的数据。请导入price.csv，然后结合你的聪明才智回答以下问题

price_data = pd.read_csv('prices.csv')
price_data = price_data[price_data['date'].apply(lambda x:x.split('-')[0])=='2016']

# 假设你是某基金公司的老板，现在对于每只股票，你都专门安排了一位负责它的交易员。公司规定每一位交易员手中的资金要么全部买入要么全部卖出（空仓，转化为现金）。假设2016年每一位交易员手中都有10000美元，假设他们都能够看到2016年全年的数据，假设他们都能抓住每一次机会，那么请问2016年底时，赚钱最多的股票是哪一只，赚了多少钱？

def daily_trade(principal, low, high, c_price, o_price):
    if high - o_price >= c_price - low:
        highest = high
        lowest = o_price
    else:
        highest = c_price
        lowest = low

    shares = principal // lowest
    margin = (highest - lowest) * shares
    principal = principal + margin
    return principal

stock_list = list(price_data['symbol'].unique())
price_data.sort_values('date',inplace=True)

final_principal = {}
for stock in stock_list:
    principal = 10000
    for index, row in price_data[price_data['symbol'] == stock].iterrows():
        o_price = row['open']
        c_price = row['close']
        low = row['low']
        high = row['high']
        principal = daily_trade(principal, low, high, c_price, o_price)

    final_principal[stock] = principal

max_return = max(zip(final_principal.values(),final_principal.keys()))
print(max_return[0]-10000,max_return[1])