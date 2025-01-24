# 이게 실전!

import pandas as pd
import os
import matplotlib.pyplot as plt
plt.rc('font',family='malgun gothic')

def DataOpen():
    path='data/'
    file_list=os.listdir(path)

    df=pd.DataFrame()
    keywords=['감기','눈병','천식','피부염']
    for i in file_list:
        if i.endswith("_시도.csv"):
            data=pd.read_csv(path+i,encoding='euc_kr')
            for key in keywords:
                if key in i:
                    data['구분']=key
                    break

            df=pd.concat([df,data])

    sido=pd.read_csv('data\시도지역코드.csv',encoding='euc_kr')
    return df, sido

def DataPreprocessing(df,sido):
    data_merge=pd.merge(df,sido,how='left',on='시도지역코드')
    data_merge['연/월']=data_merge['날짜'].str[:7]

    dfdata=data_merge[data_merge['지역명']!='전국']
    dfdata.dropna(axis=0,how='any',inplace=True)

    yearmonthdf=dfdata.groupby(['연/월','구분'],as_index=False)[['발생건수(건)']].mean()

    return dfdata, yearmonthdf

def Visualization(dfdata,yearmonthdf):
    datedata=list(dfdata['연/월'].unique())
    print(f"조회 가능한 연도와 월: {datedata}")
    yearmonthin=input("조회하고자 하는 연도와 월을 입력하세요(형식: 2025-01) ")
    yearmonthsearch=yearmonthdf[yearmonthdf['연/월']==yearmonthin]
    print(yearmonthsearch)
    yearmonthsearch.plot(kind='bar',x='구분',title=yearmonthin.split('-')[0]+'년 '+yearmonthin.split('-')[-1]+'월 '+'질병 현황',rot=0)
    plt.show()

if __name__=='__main__':
    df, sido=DataOpen()
    dfdata,yearmonthdf=DataPreprocessing(df,sido)
    Visualization(dfdata,yearmonthdf)
