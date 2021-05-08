import requests
import pandas as pd 
from flask import Flask, redirect, url_for, request
import numpy as np

app = Flask(__name__)

def getDataCDKT(type1, year, quarter, count, mack):
    CDKT = requests.get('https://www.fireant.vn/api/Data/Finance/LastestFinancialReports?type='+type1+'&year='+year+'&quarter='+quarter+'&count='+count+'&symbol='+mack)
    dataframe = pd.read_json(CDKT.content)
    data = dataframe[["Name", "Values"]]
    header = [item.get('Period') for item in data["Values"][1]]
    value = []
    df = pd.DataFrame ([], columns = header)
    for i in range(len(data)):
        val = []
        for item in data["Values"][i]:
            it = item.get('Value')
            val.append(it)
        value.append(val)
        del val   
    for i in range(len(value)):
        df.loc[i] = value[i]
    name = data['Name']
    res_cdkt = pd.concat([name, df], axis=1)
    res_cdkt = res_cdkt.set_index('Name')
    return res_cdkt

####### Canslim
@app.route('/api/cd-kt')
def CDKT():
    type1 = request.args.get('type') 
    year = request.args.get('year')
    quarter = request.args.get('quarter')
    count = request.args.get('count')
    mack = request.args.get('symbol')
    res_cdkt = getDataCDKT(type1,year,quarter,count, mack)
    # res_cdkt = res_cdkt.reset_index()
    return res_cdkt.to_json()

def getDataCSTC(fromYear,toYear,symbol):
    resp1 = requests.get('https://www.fireant.vn/api/Data/Finance/YearlyFinancialInfo?symbol='+symbol+'&fromYear='+fromYear+'&toYear='+toYear)
    cstc = pd.read_json(resp1.content)
    cstc = cstc[['Year', 'DilutedEPS', 'ROE', 'ROA', 'ROIC', 'BookValuePerShare', 'TotalAssets', 'Sales', 'ProfitAfterTax']]
    cstc = cstc.T
    new_header = cstc.iloc[0]
    new_header =new_header.astype(int)
    cstc = cstc[1:]
    cstc = cstc.rename(columns=new_header)
    cstc.loc['Effectiveness']= cstc.loc['Sales'] / cstc.loc['TotalAssets']
    cstc.loc['Effeciency']= cstc.loc['ProfitAfterTax'] / cstc.loc['Sales']
    return cstc


@app.route('/api/cs-tc')
def CSTC():
    fromYear = request.args.get('fromYear')
    toYear = request.args.get('toYear')
    symbol = request.args.get('symbol')
    cstc = getDataCSTC(fromYear,toYear,symbol)
    # cstc =cstc.reset_index()
    return cstc.to_json()


def getDataKQKD(type2, year, quarter, count,symbol):
    KQKD = requests.get('https://www.fireant.vn/api/Data/Finance/LastestFinancialReports?type='+type2+'&year='+year+
    '&quarter='+quarter+'&count='+count+'&symbol='+symbol)
    dataframe2 = pd.read_json(KQKD.content)
    data2 = dataframe2[["Name", "Values"]]
    header2 = [item.get('Period') for item in data2["Values"][1]]
    value2 = []
    df2 = pd.DataFrame ([], columns = header2)
    for i in range(len(data2)):
        val = []
        for item in data2["Values"][i]:
            it = item.get('Value')
            val.append(it)
        value2.append(val)
        del val
    for i in range(len(value2)):
        df2.loc[i] = value2[i]
    name2 = data2['Name']
    res_kqkd = pd.concat([name2, df2], axis=1)
    res_kqkd = res_kqkd.set_index('Name')
    return res_kqkd


@app.route('/api/kq-kd')
def KQKD():
    type1 = request.args.get('type')
    year = request.args.get('year')
    quarter = request.args.get('quarter')
    count = request.args.get('count')
    symbol = request.args.get('symbol')
    res_kqkd = getDataKQKD(type1,year,quarter,count,symbol)
    # res_kqkd = res_kqkd.reset_index()
    return res_kqkd.to_json()

def getDataLCTT(type3, year,quarter,count,mack):
    LCTT = requests.get('https://www.fireant.vn/api/Data/Finance/LastestFinancialReports?type='+type3+'&year='+year+'&quarter='+quarter+'&count='+count+'&symbol='+mack)
    dataframe3 = pd.read_json(LCTT.content)
    data3 = dataframe3[["Name", "Values"]]
    header3 = [item.get('Period') for item in data3["Values"][1]]
    value3 = []
    df3 = pd.DataFrame ([], columns = header3)
    for i in range(len(data3)):
        val = []
        for item in data3["Values"][i]:
            it = item.get('Value')
            val.append(it)
        value3.append(val)
        del val
    for i in range(len(value3)):
        df3.loc[i] = value3[i]
    name3 = data3['Name']
    res_lctt = pd.concat([name3, df3], axis=1)
    res_lctt = res_lctt.set_index('Name')
    return res_lctt


@app.route('/api/lc-tt')
def LCTT():
    type3 = request.args.get('type')
    year = request.args.get('year')
    quarter = request.args.get('quarter')
    count = request.args.get('count')
    mack = request.args.get('symbol')
    res_lctt = getDataLCTT(type3,year,quarter,count,mack)
    # res_lctt= res_lctt.reset_index()
    return res_lctt.to_json()

#4M
@app.route('/api/4m')
def _4M():
    year = request.args.get('year')
    quarter = request.args.get('quarter')
    count = request.args.get('count')
    symbol = request.args.get('symbol')
    res_kqkd = getDataKQKD('2',year,quarter,count,symbol) # get data KQKD type =2
    res_cdkt = getDataCDKT('1',year,quarter,count,symbol) # get data CDKT type =1
    res_lctt = getDataLCTT('4',year,quarter,count,symbol) # get data LCTT type =4
    cstc = getDataCSTC('2014','2021',symbol)
    df4m = pd.read_json('https://e.cafef.vn/fi.ashx?symbol='+symbol)
    df4m = df4m[df4m['Year'] >=2015]
    df4m = df4m[['Year', 'EPS', 'BV', 'ROA', 'ROE']]
    df4m.sort_values(by=['Year'], inplace=True)
    df4m['Sales']= res_kqkd.loc["3. Doanh thu thuần (1)-(2)"].values
    roic = res_kqkd.loc['19. Lợi nhuận sau thuế thu nhập doanh nghiệp (15)-(18)']/(res_cdkt.loc['II. Nợ dài hạn'] + res_cdkt.loc['I. Vốn chủ sở hữu'] - \
                                 res_cdkt.loc['I. Tiền và các khoản tương đương tiền'] - res_cdkt.loc['VII. Lợi thế thương mại'])
    df4m['ROIC'] = roic.values
    effectiveness= res_kqkd.loc['3. Doanh thu thuần (1)-(2)'] / res_cdkt.loc['TỔNG CỘNG TÀI SẢN']
    df4m['Effectiveness'] = effectiveness.values
    effeciency = res_kqkd.loc['19. Lợi nhuận sau thuế thu nhập doanh nghiệp (15)-(18)']/res_kqkd.loc['3. Doanh thu thuần (1)-(2)']
    df4m['Effeciency'] = effeciency.values
    lctt = res_lctt.loc['Lưu chuyển tiền thuần từ hoạt động kinh doanh']
    productivity= lctt / cstc.loc['ProfitAfterTax'].values
    df4m['Productivity'] = productivity.values
    df4m['Luu chuyen tien thuan tu HDKD'] = lctt.values
    df4m = df4m.T
    new_header = df4m.iloc[0]
    new_header = new_header.astype(int)
    df4m = df4m[1:]
    df4m = df4m.rename(columns=new_header)
    df4m.loc['No dai han nam gan nhat', '2019'] = res_cdkt.loc['II. Nợ dài hạn', '2019']
    ind4m = ['Chi so','Sales Growth Rate', 'EPS Growth Rate', 'BVPS Growth Rate', 'Luu chuyen tien thuan tu HDKD', 'No dai han nam gan nhat', 'Effectiveness', 'Efficiency'\
         , 'Productivity', 'ROA', 'ROE', 'ROIC']
    df = pd.DataFrame ([], columns = [1,3, 5, 'Tham chieu', 'Ty trong', 'Diem TP', 'Tong'], index=ind4m)
    df.loc['Chi so'] = [0.3, 0.3, 0.4, 0, 0, 0, 0] 
    df['Tham chieu'] = [0 ,0.2 ,0.2 ,0.15 ,0.15 ,0 ,0.1 ,0.1 ,0.1 ,0.15 ,0.2 ,0.15]
    df['Ty trong'] = [0 ,0.15 ,0.2 ,0.05 ,0.15 , 0 ,0.05 ,0.05 ,0.05 ,0.1 ,0.05 ,0.15]
    index= ['Sales', 'EPS', 'BV', 'Luu chuyen tien thuan tu HDKD', 'Effectiveness', 'Effeciency', 'Productivity', 'ROA', 'ROE', 'ROIC']
    index_res = ['Sales Growth Rate', 'EPS Growth Rate', 'BVPS Growth Rate', 'Luu chuyen tien thuan tu HDKD', 'Effectiveness', 'Efficiency', 'Productivity',\
                'ROA', 'ROE', 'ROIC']
    arr = [1, 3, 5]
    year_start = [2019,2017,2015]
    year_end = [2020,2020,2020]
    for a in range(len(arr)):
        for i in range(len(index)):
            re1 = np.rate(arr[a] ,0,-df4m.loc[index[i], year_start[a]], df4m.loc[index[i], year_end[a]])
            df.loc[index_res[i], arr[a]] = re1
    for i in range(len(index)):
        val = []
        for a in range(len(arr)):
            if df.loc[index_res[i], arr[a]] > df.loc[index_res[i], 'Tham chieu']:
             a = df.loc['Chi so', arr[a]]
            else: a = (df.loc[index_res[i], arr[a]]/ df.loc[index_res[i], 'Tham chieu'])*df.loc['Chi so', arr[a]]
            val.append(a)
        df.loc[index_res[i], 'Diem TP'] = sum(val)
        del val
    df.loc['No dai han nam gan nhat', 1] = df4m.loc['No dai han nam gan nhat', '2019']
    df.loc['No dai han nam gan nhat', 'Tham chieu'] = cstc.loc['ProfitAfterTax'].values[-1] * 3
    if df4m.loc['No dai han nam gan nhat', '2019'] > cstc.loc['ProfitAfterTax'].values[-1] * 3:
        df.loc['No dai han nam gan nhat', 'Diem TP'] = 0
    else: df.loc['No dai han nam gan nhat', 'Diem TP'] = 10
    df.loc['Chi so', 'Tong'] = round(sum(df['Ty trong']*df['Diem TP'])*100, 2)
    total = 0
    for i in range(len(df.index)-2):
        total += (df.loc[index_res[i], 'Ty trong'] * df.loc[index_res[i], 'Diem TP'])
    total += df.loc['No dai han nam gan nhat', 'Diem TP']
    df.loc['Chi so', 'Tong'] = round(total*100, 2)
    df = df.reset_index()
    return df.to_json()

if __name__ == '__main__':
    app.run()
