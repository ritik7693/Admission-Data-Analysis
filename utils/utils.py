import pandas as pd
import numpy as np
from flask import current_app,url_for
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import os


rvp=pd.read_csv("data/percentileXrank_csv_file.csv")
print('Create regressors', flush=True)

def create_regressor(rvp_):
    X=rvp_['PERCENTILE'].values.reshape(-1,1)
    y=rvp_['RANK'].values.reshape(-1,1)
    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=0)
    regressor = LinearRegression()
    regressor.fit(X_train, y_train)
    return regressor

categories = ['GEN', 'EWS', 'SC', 'ST', 'OBC-NCL']
regressors = {
     category : [
         create_regressor(rvp[rvp['CATEGORY']==category]),
         create_regressor(rvp[rvp['CATEGORY']==category + '-PwD'])
     ] for category in categories
}

def pvr(perc,pwd,category):
    x=pd.Series([perc])
    z=regressors[category][pwd=='YES'].predict(x.values.reshape(-1,1))
    k=float(np.round(z))
    if(k<=0):
        k=15
    return k

def finalList(rank1,perc,category,state,gender,pwd,sortby):
    import pandas as pd
    import numpy as np
    import csv
    from pathlib import Path
    import os


    file_path ="data/round1_cleaned.csv"
    df = pd.read_csv(file_path)

    # The algorithm showed some anomaly when %tile was 100.
    # Hence the following condition.

    if(rank1 == '-1'):
        rank = float(pvr(perc,pwd,category))
    else:
        rank = rank1

    if(pwd == 'YES'):
        if(gender == 'M'):
            catg = category+'-PwD'
            p = df[(df['Closing Rank']>=rank)&((df['Category']==catg)|(df['Category']=='OPEN-PwD'))&(df['Seat Pool']=='Gender-Neutral')]
        else:
            catg = category+'-PwD'
            p = df[(df['Closing Rank']>=rank)&((df['Category']==catg)|(df['Category']=='OPEN-PwD'))]
    else:
        if(gender == 'M'):
            p = df[(df['Closing Rank']>=rank)&((df['Category']==category)|(df['Category']=='OPEN'))&(df['Seat Pool']=='Gender-Neutral')]
        else:
             p = df[(df['Closing Rank']>=rank)&((df['Category']==category)|(df['Category']=='OPEN'))]

    v = []
    for i in p.index:
        if(p['State'][i] == state):
            if(p['Quota'][i] == 'OS'):
                v.append(i)
        elif((p['State'][i]!='All India')&(p['State'][i]!=state)):
            if(p['Quota'][i] == 'HS'):
                v.append(i)

    q = p.drop(index = v)
    q = q.sort_values(sortby)
    x = q.drop(['Quota','Category','Seat Pool','Opening Rank','Closing Rank','State','Round No'],axis=1).drop_duplicates()
    x.reset_index(inplace = True, drop = True)
    return x