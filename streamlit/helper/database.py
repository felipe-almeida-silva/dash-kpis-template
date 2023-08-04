import time
import mysql.connector
import pandas as pd
from datetime import datetime

class MySQLDatabase:
    def __init__(self, host: str, user: str, password: str, database: str, port: int = 3306):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port

    def connect_mysql_db(self):
        cnx = mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            database=self.database,
            password=self.password)
        cur = cnx.cursor()
        return cnx, cur

    def query_mysql_db(self, query: str, *args: tuple):
        cnx, cur = self.connect_mysql_db()

        cur.execute(query, *args)
        result = cur.fetchall()
        result_columns = cur.description
        columns = [i[0] for i in result_columns]
        cnx.close()

        return columns, result

    def dataframe_from_query(self, query: str, *args: tuple):
        start_time = time.time()
        print(f'Query started! - {datetime.now()}')

        query_result = self.query_mysql_db(query, *args)

        columns = query_result[0]
        result = query_result[1]
        df = pd.DataFrame(result,columns=columns)
        df = df.fillna('n/a')

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f'Query finished in {round(elapsed_time)} seconds')
        n_rows, n_columns = df.shape[0], df.shape[1]
        print(f'{n_rows} rows retrieved; {n_columns} columns retrieved')

        return df
