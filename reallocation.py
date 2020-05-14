import csv
import pandas as pd

def match(buy, sell):
    for i in range(len(buy)):
        found = False
        for k in range(len(sell)):
            if buy.iloc[i]['Change Left'] == -sell.iloc[k]['Change']:
                buy.iloc[i]['With'].append(sell.iloc[k]['Symbol'])
                buy.at[i, 'Change Left'] = 0
                sell = sell.drop(k)
                break
    return buy.sort_values(by='Change Left', ascending=False).reset_index(drop=True), sell.sort_values(by='Change', ascending=True).reset_index(drop=True)

def groupMatch(buy, sell):
    for i in range(len(buy)):
        found = False
        for k in range(len(sell)):
            for j in range(k, len(sell)):
                if k != j and k < len(sell) and j < len(sell):
                    if -buy.iloc[i]['Change Left'] == sell.iloc[k]['Change'] + sell.iloc[j]['Change']:
                        buy.iloc[i]['With'].append(sell.iloc[k]['Symbol'])
                        buy.iloc[i]['With'].append(sell.iloc[j]['Symbol'])
                        buy.at[i, 'Change Left'] = 0
                        sell = sell.drop(k)
                        sell = sell.drop(j)
                        break
    return buy.sort_values(by='Change Left', ascending=False).reset_index(drop=True), sell.sort_values(by='Change', ascending=True).reset_index(drop=True)

def bucket(buy, sell):
    max_buy, max_sell = max(buy['Change Left']), -min(sell['Change'])
    if max_buy > max_sell:
        buy.iloc[0]['With'].append(sell.iloc[0]['Symbol'])
        buy.at[0, 'Change Left'] = max_buy - max_sell
        sell = sell.drop(0)
    else:
        buy.iloc[0]['With'].append(sell.iloc[0]['Symbol'])
        buy.at[0, 'Change Left'] = 0
        sell.at[0, 'Change'] = max_buy - max_sell
    return buy.sort_values(by='Change Left', ascending=False).reset_index(drop=True), sell.sort_values(by='Change', ascending=True).reset_index(drop=True)

def setup():
    buy, sell = pd.DataFrame(), pd.DataFrame()

    with open('realloc.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if row[1] == row[2]:
                pass
            elif int(float(row[1]) * 10) - int(float(row[2]) * 10) > 0:
                sell = sell.append(({'Symbol' : row[0], 'Change' : int(float(row[2]) * 10) - int(float(row[1]) * 10)}), ignore_index=True)
            elif  int(float(row[1]) * 10) - int(float(row[2]) * 10) < 0:
                buy = buy.append(({'Symbol' : row[0], 'Change Left' : int(float(row[2]) * 10) - int(float(row[1]) * 10), 'With' : []}), ignore_index=True)

    return buy.sort_values(by='Change Left', ascending=False).reset_index(drop=True), sell.sort_values(by='Change', ascending=True).reset_index(drop=True)

def opt(buy, sell):
    while(len(sell) != 0):
        buy, sell = match(buy, sell)
        if(len(sell) == 0):
            break
        buy, sell = bucket(buy, sell)
    print(buy)

if __name__ == '__main__':
    buy, sell = setup()
    opt(buy, sell)