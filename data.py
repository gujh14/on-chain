from database.CRUD_tx import CRUD_tx

def get_data(token, user_start, user_end, user_min, n):
    crud = CRUD_tx()
    sql = " SELECT (from_address, to_address, value, datetime) from {schema}.{table} WHERE TO_TIMESTAMP(datetime,'YYYY-MM-DD HH24:MI:SS')>='{user_start}' AND TO_TIMESTAMP(datetime,'YYYY-MM-DD HH24:MI:SS')<='{user_end}' AND value>{user_min} ORDER BY value DESC LIMIT {n}".format(schema='testschema',table=token, user_start=user_start, user_end=user_end, user_min=user_min,n=n)
    return crud.getDF(sql)
