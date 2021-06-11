import requests
import pandas as pd 
from flask import Flask, redirect, url_for, request
import numpy as np
import json
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

def getDataCDKT(type1, year, quarter, mack):
    CDKT = requests.get('https://www.fireant.vn/api/Data/Finance/LastestFinancialReports?type='+type1+'&year='+str(year)+'&quarter='+quarter+'&count='+str(6)+'&symbol='+mack)
    dataframe = pd.read_json(CDKT.content)
    data = dataframe[["Name", "Values"]]
    header = [item.get('Period') for item in data["Values"][1]]
    value = []
    df = pd.DataFrame ([], columns = header)
    value = []
    df = pd.DataFrame ([], columns = header)
    for i in range(len(data)):
        val = []
        for item in data["Values"][i]:
            it = item.get('Value')
            val.append(it if it == None else round(it/10000000,2))
        value.append(val)
        del val
    for i in range(len(value)):
        df.loc[i] = value[i]
    name = data['Name']
    res_cdkt = pd.concat([name, df], axis=1)
    return res_cdkt

####### Canslim
@app.route('/api/cd-kt')
def CDKT():
    type1 = request.args.get('type') 
    year = request.args.get('year')
    quarter = request.args.get('quarter')
    mack = request.args.get('symbol')
    res_cdkt = getDataCDKT(type1,year,quarter, mack)
    return res_cdkt.to_html()


def getDataKQKD(type2, year, quarter, symbol):
    KQKD = requests.get('https://www.fireant.vn/api/Data/Finance/LastestFinancialReports?type='+type2+'&year='+str(year)+'&quarter='+quarter+'&count='+str(6)+'&symbol='+symbol)
    dataframe2 = pd.read_json(KQKD.content)
    data2 = dataframe2[["Name", "Values"]]
    header2 = [item.get('Period') for item in data2["Values"][1]]
    value2 = []
    df2 = pd.DataFrame ([], columns = header2)
    for i in range(len(data2)):
        val = []
        for item in data2["Values"][i]:
            it = item.get('Value')
            val.append(round(it/10000000,2))
        value2.append(val)
        del val
    for i in range(len(value2)):
        df2.loc[i] = value2[i]
    name2 = data2['Name']
    res_kqkd = pd.concat([name2, df2], axis=1)
    return res_kqkd


@app.route('/api/kq-kd')
def KQKD():
    type1 = request.args.get('type')
    year = request.args.get('year')
    quarter = request.args.get('quarter')
    symbol = request.args.get('symbol')
    res_kqkd = getDataKQKD(type1,year,quarter,symbol)
    return res_kqkd.to_html()

def getDataLCTT(type3, year,quarter,mack):
    LCTT = requests.get('https://www.fireant.vn/api/Data/Finance/LastestFinancialReports?type='+type3+'&year='+str(year)+'&quarter='+quarter+'&count='+str(6)+'&symbol='+mack)
    dataframe3 = pd.read_json(LCTT.content)
    data3 = dataframe3[["Name", "Values"]]
    header3 = [item.get('Period') for item in data3["Values"][1]]
    value3 = []
    df3 = pd.DataFrame ([], columns = header3)
    for i in range(len(data3)):
        val = []
        for item in data3["Values"][i]:
            it = item.get('Value')
            val.append(it if it == None else round(it/10000000,2))
        value3.append(val)
        del val
    for i in range(len(value3)):
        df3.loc[i] = value3[i]
    name3 = data3['Name']
    res_lctt = pd.concat([name3, df3], axis=1)
    return res_lctt


@app.route('/api/lc-tt')
def LCTT():
    type3 = request.args.get('type')
    year = request.args.get('year')
    quarter = request.args.get('quarter')
    mack = request.args.get('symbol')
    res_lctt = getDataLCTT(type3,year,quarter,mack)
    return res_lctt.to_html()

#4M
@app.route('/api/4m')
def _4M():
    year = request.args.get('year')
    quarter = request.args.get('quarter')
    symbol = request.args.get('symbol')
    res_kqkd = getDataKQKD('2',year,quarter,symbol) # get data KQKD type =2
    res_kqkd = res_kqkd.set_index('Name')
    res_cdkt = getDataCDKT('1',year,quarter,symbol) # get data CDKT type =1
    res_cdkt = res_cdkt.set_index('Name')
    res_lctt = getDataLCTT('4',year,quarter,symbol) # get data LCTT type =4
    res_lctt = res_lctt.set_index('Name')
    df4m = pd.read_json('https://e.cafef.vn/fi.ashx?symbol='+symbol)
    maxyear = df4m['Year'].max()
    df4m = df4m[df4m['Year'] >=df4m['Year'].max() -5]
    df4m = df4m[['Year', 'EPS', 'BV', 'ROA', 'ROE']]
    df4m.sort_values(by=['Year'], inplace=True)
    year_start = [df4m['Year'].max() - 1,df4m['Year'].max() - 3, df4m['Year'].max() - 5]
    year_end = [df4m['Year'].max(),df4m['Year'].max(),df4m['Year'].max()]
    df4m['Sales']= res_kqkd.loc['3. Doanh thu thuần (1)-(2)'].values
    roic = res_kqkd.loc['19. Lợi nhuận sau thuế thu nhập doanh nghiệp (15)-(18)']/(res_cdkt.loc['II. Nợ dài hạn'] + res_cdkt.loc['I. Vốn chủ sở hữu'] - \
                                 res_cdkt.loc['I. Tiền và các khoản tương đương tiền']) 
                                #  - res_cdkt.loc['VII. Lợi thế thương mại'])
    df4m['ROIC'] = roic.values
    effectiveness= res_kqkd.loc['3. Doanh thu thuần (1)-(2)'] / res_cdkt.loc['TỔNG CỘNG TÀI SẢN']
    df4m['Effectiveness'] = effectiveness.values
    effeciency = res_kqkd.loc['19. Lợi nhuận sau thuế thu nhập doanh nghiệp (15)-(18)']/res_kqkd.loc['3. Doanh thu thuần (1)-(2)']
    df4m['Effeciency'] = effeciency.values
    lctt = res_lctt.loc['Lưu chuyển tiền thuần từ hoạt động kinh doanh']
    productivity= lctt / res_kqkd.loc['19. Lợi nhuận sau thuế thu nhập doanh nghiệp (15)-(18)'].values
    df4m['Productivity'] = productivity.values
    df4m['Luu chuyen tien thuan tu HDKD'] = lctt.values
    df4m = df4m.T
    new_header = df4m.iloc[0]
    new_header = new_header.astype(int)
    df4m = df4m[1:]
    df4m = df4m.rename(columns=new_header)
    df4m.loc['No dai han nam gan nhat', maxyear] = res_cdkt.loc['II. Nợ dài hạn', str(maxyear)]
    ind4m = ['Chi so','Sales Growth Rate', 'EPS Growth Rate', 'BVPS Growth Rate', 'Luu chuyen tien thuan tu HDKD', 'No dai han nam gan nhat', 'Effectiveness', 'Efficiency'\
         , 'Productivity', 'ROA', 'ROE', 'ROIC']
    df = pd.DataFrame ([], columns = [1,3, 5, 'Tham chieu', 'Ty trong', 'Diem TP'], index=ind4m)
    df.loc['Chi so'] = [0.3, 0.3, 0.4, 0, 0, 0] 
    df['Tham chieu'] = [0 ,0.2 ,0.2 ,0.15 ,0.15 ,0 ,0.1 ,0.1 ,0.1 ,0.15 ,0.2 ,0.15]
    df['Ty trong'] = [0 ,0.15 ,0.2 ,0.05 ,0.15 , 0.1 ,0.05 ,0.05 ,0.05 ,0.1 ,0.05 ,0.15]
    index= ['Sales', 'EPS', 'BV', 'Luu chuyen tien thuan tu HDKD', 'Effectiveness', 'Effeciency', 'Productivity', 'ROA', 'ROE', 'ROIC']
    index_res = ['Sales Growth Rate', 'EPS Growth Rate', 'BVPS Growth Rate', 'Luu chuyen tien thuan tu HDKD', 'Effectiveness', 'Efficiency', 'Productivity',\
                'ROA', 'ROE', 'ROIC']
    arr = [1, 3, 5]
    #year_start = [2019,2017,2015]
    #year_end = [2020,2020,2020]
    for a in range(len(arr)):
        for i in range(len(index)):
            re1 = np.rate(arr[a] ,0,-df4m.loc[index[i], year_start[a]], df4m.loc[index[i], year_end[a]])
            df.loc[index_res[i], arr[a]] = re1
    for i in range(len(index)):
      val = []
      for a in range(len(arr)):
            if df.loc[index_res[i], arr[a]] > df.loc[index_res[i], 'Tham chieu']:
              if (df.loc['Chi so', arr[a]] >0):
                 a = df.loc['Chi so', arr[a]]
              else: a = 0
            else: 
              if ((df.loc[index_res[i], arr[a]]/ df.loc[index_res[i], 'Tham chieu'])*df.loc['Chi so', arr[a]]) > 0:
                  a= (df.loc[index_res[i], arr[a]]/ df.loc[index_res[i], 'Tham chieu'])*df.loc['Chi so', arr[a]]
              else: a= 0
            val.append(a*100)
      df.loc[index_res[i], 'Diem TP'] = sum(val)
      del val
    df.loc['No dai han nam gan nhat', 1] = df4m.loc['No dai han nam gan nhat', maxyear]
    df.loc['No dai han nam gan nhat', 'Tham chieu'] = res_kqkd.loc['19. Lợi nhuận sau thuế thu nhập doanh nghiệp (15)-(18)'].values[-1] * 3
    if df4m.loc['No dai han nam gan nhat', maxyear] > res_kqkd.loc['19. Lợi nhuận sau thuế thu nhập doanh nghiệp (15)-(18)'].values[-1] * 3:
        df.loc['No dai han nam gan nhat', 'Diem TP'] = 0
    else: df.loc['No dai han nam gan nhat', 'Diem TP'] = 100
    #Tinh tong
    index_res1 = ['Sales Growth Rate', 'EPS Growth Rate', 'BVPS Growth Rate', 'Luu chuyen tien thuan tu HDKD', 'No dai han nam gan nhat', 'Effectiveness', 'Efficiency', \
                'Productivity', 'ROA', 'ROE', 'ROIC']
    total = 0
    for i in range(len(df.index) -1):
        total += (df.loc[index_res1[i], 'Ty trong'] * df.loc[index_res1[i], 'Diem TP'])
    #total += df.loc['No dai han nam gan nhat', 'Diem TP']
    # df.loc['Chi so', 'Tong'] = round(total, 2)
    return {
        "html":df.to_html(),
        "total":round(total, 2)
    }

@app.route('/api/get-info-cty/<id>')
def getInfoCty(id):
    res = requests.get('http://ezsearch.fpts.com.vn/Services/EzData/ProcessLoadRuntime.aspx?s='+id+'&cGroup=Overview&cPath=Services/EzData/OverviewProfile')
    return res.content

@app.route("/api/canslim")
def getCanSlim():
    mack = request.args.get('mack')
    df = pd.read_csv("canslim.csv")
    header = ['','','','','','','','','','','','Tham chiếu', 'TỶ TRỌNG TỪNG THÀNH PHẦN', 'C', 'A']
    df.columns = header
    df = df.replace(np.nan,'')
    tc = ['',0.25,'', 0.25, '' ,0.2, '',0.2, '', '', 0.25, '', 0.25, '', 0.2, '', 0.2, '']
    tt = ['',0.15,'', 0.1, '' ,0.1, '',0.05, '', '', 0.2, '', 0.15, '', 0.15, '', 0.1, '']
    df['Tham chiếu'] = tc
    df['TỶ TRỌNG TỪNG THÀNH PHẦN'] = tt
    qt = requests.get('https://www.fireant.vn/api/Data/Finance/LastestFinancialReports?symbol='+mack+'&type=2&year=2021&quarter=1&count=9')
    dataframe = pd.read_json(qt.content)
    data = dataframe[["Name", "Values"]]
    header = [item.get('Period') for item in data["Values"][1]]
    value = []
    df2 = pd.DataFrame ([], columns = header)
    for i in range(len(data)):
        val = []
        for item in data["Values"][i]:
            it = item.get('Value')
            # val.append(it)
            val.append(it if it == None else round(it/10000000,2))
        value.append(val)
        del val
    for i in range(len(value)):
      df2.loc[i] = value[i]
    name = data['Name']
    res_kqkd = pd.concat([name, df2], axis=1)
    res_kqkd.set_index('Name', inplace=True)
    df.iloc[2,6] = round(res_kqkd.loc['1. Tổng doanh thu hoạt động kinh doanh',df.iloc[1,6]], 0)
    #1 quý gần nhất (C) - Q1 2020
    df.iloc[2,5] = round(res_kqkd.loc['1. Tổng doanh thu hoạt động kinh doanh',df.iloc[1,5]], 0)
    #1 quý trước đó gần nhất (C) - Q4 2019
    df.iloc[4,5] = round(res_kqkd.loc['1. Tổng doanh thu hoạt động kinh doanh',df.iloc[3,5]],0)
    #1 quý trước đó gần nhất (C) - Q1 2020
    df.iloc[4,6] = round(res_kqkd.loc['1. Tổng doanh thu hoạt động kinh doanh',df.iloc[3,6]],0)
    #trailing 12 tháng gần nhất (A)
    #df.iloc[6,[2,3,4,5,6,7,8,9]] = [1,2,3,4,5,6,7,8]
    df.iloc[6,[2,3,4,5,6,7,8,9]] = round(res_kqkd.loc['1. Tổng doanh thu hoạt động kinh doanh',df.iloc[5,[2,3,4,5,6,7,8,9]]],0).values
    #trailing 12 tháng gần nhất trước đó (A)
    df.iloc[8,[2,3,4,5,6,7,8,9]] = round(res_kqkd.loc['1. Tổng doanh thu hoạt động kinh doanh',df.iloc[7,[2,3,4,5,6,7,8,9]]],0).values
    df.iloc[1,10] = round((df.iloc[2,6] - df.iloc[2,5])/df.iloc[2,5],2)
    df.iloc[3,10] = round((df.iloc[4,6] - df.iloc[4,5])/df.iloc[4,5],2)
    df.iloc[5,10] = round((df.iloc[6,[6,7,8,9]].sum() - df.iloc[6,[2,3,4,5]].sum())/df.iloc[6,[2,3,4,5]].sum(),2)
    df.iloc[7,10] = round((df.iloc[8,[6,7,8,9]].sum() - df.iloc[8,[2,3,4,5]].sum())/df.iloc[8,[2,3,4,5]].sum(),2)
    if df.iloc[1,10] > df.loc[1,"Tham chiếu"] :
      df.loc[1,"C"] = df.loc[1,"TỶ TRỌNG TỪNG THÀNH PHẦN"] * 100
    else: df.loc[1,"C"] = (df.iloc[1,10]/df.loc[1,"Tham chiếu"])*df.loc[1,"TỶ TRỌNG TỪNG THÀNH PHẦN"] *100
    if df.iloc[3,10] > df.loc[3,"Tham chiếu"] :
      df.loc[3,"C"] = df.loc[3,"TỶ TRỌNG TỪNG THÀNH PHẦN"] *100
    else: df.loc[3,"C"] = (df.iloc[3,10]/df.loc[3,"Tham chiếu"])*df.loc[3,"TỶ TRỌNG TỪNG THÀNH PHẦN"] *100
    if df.iloc[5,10] > df.loc[5,"Tham chiếu"] :
      df.loc[5,"A"] = df.loc[5,"TỶ TRỌNG TỪNG THÀNH PHẦN"] *100
    else: df.loc[5,"A"] = (df.iloc[5,10]/df.loc[5,"Tham chiếu"])*df.loc[5,"TỶ TRỌNG TỪNG THÀNH PHẦN"] *100
    if df.iloc[7,10] > df.loc[7,"Tham chiếu"] :
      df.loc[7,"A"] = df.loc[7,"TỶ TRỌNG TỪNG THÀNH PHẦN"] *100
    else: df.loc[7,"A"] = (df.iloc[7,10]/df.loc[7,"Tham chiếu"])*df.loc[7,"TỶ TRỌNG TỪNG THÀNH PHẦN"] *100
    canslim_xml = requests.get('https://www.fireant.vn/api/Data/Finance/QuarterlyFinancialInfo?symbol='+mack+'&fromYear=2019&fromQuarter=1&toYear=2021&toQuarter=1')
    dataframe2 = pd.read_json(canslim_xml.content)
    canslim = dataframe2[['Year', 'Quarter', 'DilutedEPS_MRQ']]
    canslim["Period"] = 'Q'+canslim['Quarter'].astype(str) +' '+ canslim['Year'].astype(str) 
    #Tieu chi EPS
    #1 quý gần nhất (C) - Q1 2021
    df.iloc[11,6] = round(canslim[canslim['Period'] == df.iloc[1,6]],0)['DilutedEPS_MRQ'].values[0]
    #1 quý gần nhất (C) - Q1 2020
    df.iloc[11,5] = round(canslim[canslim['Period'] == df.iloc[1,5]],0)['DilutedEPS_MRQ'].values[0]
    #1 quý trước đó gần nhất (C) - Q4 2019
    df.iloc[13,5] = round(canslim[canslim['Period'] == df.iloc[3,5]],0)['DilutedEPS_MRQ'].values[0] 
    #1 quý trước đó gần nhất (C) - Q1 2020
    df.iloc[13,6] = round(canslim[canslim['Period'] == df.iloc[3,6]],0)['DilutedEPS_MRQ'].values[0] 
    pos = [2,3,4,5,6,7,8,9]
    val = df.iloc[14,pos].values
    for i in range(len(val)):
        df.iloc[15,pos[i]] = round(canslim[canslim['Period'] == val[i]],0)['DilutedEPS_MRQ'].values[0]
    pos = [2,3,4,5,6,7,8,9]
    val = df.iloc[16,pos].values
    for i in range(len(val)):
        df.iloc[17,pos[i]] = round(canslim[canslim['Period'] == val[i]],0)['DilutedEPS_MRQ'].values[0]
    df.iloc[10,10] = round((df.iloc[11,6] - df.iloc[11,5])/df.iloc[11,5],2)
    df.iloc[12,10] = round((df.iloc[13,6] - df.iloc[13,5])/df.iloc[13,5],2)
    df.iloc[14,10] = round((df.iloc[15,[6,7,8,9]].sum() - df.iloc[15,[2,3,4,5]].sum())/df.iloc[15,[2,3,4,5]].sum(),2)
    df.iloc[16,10] = round((df.iloc[17,[6,7,8,9]].sum() - df.iloc[17,[2,3,4,5]].sum())/df.iloc[17,[2,3,4,5]].sum(),2)
    if df.iloc[10,10] > df.loc[10,"Tham chiếu"] :
      df.loc[10,"C"] = df.loc[10,"TỶ TRỌNG TỪNG THÀNH PHẦN"] * 100
    else: df.loc[10,"C"] = (df.iloc[10,10]/df.loc[1,"Tham chiếu"])*df.loc[10,"TỶ TRỌNG TỪNG THÀNH PHẦN"] *100
    if df.iloc[12,10] > df.loc[12,"Tham chiếu"] :
      df.loc[12,"C"] = df.loc[12,"TỶ TRỌNG TỪNG THÀNH PHẦN"] *100
    else: df.loc[12,"C"] = (df.iloc[12,10]/df.loc[12,"Tham chiếu"])*df.loc[12,"TỶ TRỌNG TỪNG THÀNH PHẦN"] *100
    if df.iloc[14,10] > df.loc[14,"Tham chiếu"] :
      df.loc[14,"A"] = df.loc[14,"TỶ TRỌNG TỪNG THÀNH PHẦN"] *100
    else: df.loc[14,"A"] = (df.iloc[14,10]/df.loc[14,"Tham chiếu"])*df.loc[14,"TỶ TRỌNG TỪNG THÀNH PHẦN"] *100
    if df.iloc[16,10] > df.loc[16,"Tham chiếu"] :
      df.loc[16,"A"] = df.loc[16,"TỶ TRỌNG TỪNG THÀNH PHẦN"] *100
    else: df.loc[16,"A"] = (df.iloc[16,10]/df.loc[16,"Tham chiếu"])*df.loc[16,"TỶ TRỌNG TỪNG THÀNH PHẦN"] *100
    df.loc[0, 'C'] = df.loc[[1, 3, 10, 12], 'C'].sum()
    df.loc[0, 'A'] = df.loc[[5, 7, 14, 16], 'A'].sum()
    # df.loc[0,'TỔNG ĐIỂM'] = df.loc[0, 'C'] + df.loc[0, 'A']
    # return df.to_html()
    return  { "html":df.to_html(),
    "total": df.loc[0, 'C'] + df.loc[0, 'A']}

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=os.environ.get('PORT', 5000))
