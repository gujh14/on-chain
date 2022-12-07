from database.CRUD import CRUD
import pandas as pd
from io import StringIO

class CRUD_tx(CRUD):
    def insertDB(self, schema, table, data):
        sql = " INSERT INTO {schema}.{table}(from_address, to_address, value, datetime, blocknumber) VALUES ('{data[0]}', '{data[1]}', '{data[2]}', '{data[3]}', {data[4]}) ;".format(schema=schema,table=table,data=data)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e :
            print(" insert DB err ",e) 
            
    def readDB(self,schema,table):
        sql = " SELECT (from_address, to_address, value, datetime) from {schema}.{table}".format(schema=schema,table=table)
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
        except Exception as e :
            result = (" read DB err",e)
        
        return result

    def getDF(self,sql):
        try:
            self.cursor.execute(sql)
            lines = self.cursor.fetchall()
        except Exception as e :
            lines = (" read DB err",e)
            print(lines)

        df = 'From,To,Value,Date\n'

        for line in lines:
            line = str(line)
            line = line.lstrip('(\'(').rstrip(')\',)').replace('"', '')
            df += line + '\n'

        df = StringIO(df)
        df = pd.read_csv(df, sep=",")

        return df
    

if __name__ == "__main__":
    db = CRUD_tx()
    data = ['a'*42, 'b'*42, 3.2342, '2022-01-23 11:23:12'] 
    db.insertDB(schema='testschema',table='test_tb',data=data)
    #print(db.readDB(schema='testschema',table='test_tb',colum='from_address'))
    db.deleteDB(schema='testschema',table='test_tb',condition ="from_address != 'd'")