from database.CRUD_tx import CRUD_tx
import datetime as dt
import pandas as pd
import numpy as np

def get_data(token, user_start, user_end, user_min, n):
    crud = CRUD_tx()
    sql = " SELECT (from_address, to_address, value, datetime) from {schema}.{table} WHERE TO_TIMESTAMP(datetime,'YYYY-MM-DD HH24:MI:SS')>='{user_start}' AND TO_TIMESTAMP(datetime,'YYYY-MM-DD HH24:MI:SS')<='{user_end}' AND value>{user_min} ORDER BY value DESC LIMIT {n}".format(schema='testschema',table=token, user_start=user_start, user_end=user_end, user_min=user_min,n=n)
    return crud.getDF(sql)

def getDateRange(token):
    if token == "Select token":
        return dt.date(2022, 11, 20), dt.date(2022, 12, 1)
    crud = CRUD_tx()

    minsql = "SELECT MIN(datetime) from {schema}.{table}".format(schema="testschema", table=token)
    maxsql = "SELECT MAX(datetime) from {schema}.{table}".format(schema="testschema", table=token)
    
    min = crud.readDateDB(minsql).split('-')
    max = crud.readDateDB(maxsql).split('-')

    return dt.date(int(min[0]), int(min[1]), int(min[2])), dt.date(int(max[0]), int(max[1]), int(max[2]))

def getWhaleData(token, from_date, to_date, interval, threshold):
    crud = CRUD_tx()
    df = pd.DataFrame()
    
    while from_date != to_date:
        from_date_start = np.datetime64(from_date)
        from_date_end = np.datetime64(from_date+interval)
        
        sql = " SELECT COUNT(*) from {schema}.{table} WHERE TO_TIMESTAMP(datetime,'YYYY-MM-DD HH24:MI:SS')>='{from_date}' AND TO_TIMESTAMP(datetime,'YYYY-MM-DD HH24:MI:SS')<'{from_date_end}' AND value>{threshold}".format(schema='testschema',table=token,from_date=from_date,from_date_end=from_date_end,threshold=threshold)
    
        try:
            crud.cursor.execute(sql)
            result = crud.cursor.fetchall()
        except Exception as e :
            result = (" read DB err",e)
        newdf = pd.DataFrame({'count':[result[0][0]]}, index=[np.datetime64(from_date)])
        df = pd.concat([df, newdf])
        from_date = from_date + interval

    return df