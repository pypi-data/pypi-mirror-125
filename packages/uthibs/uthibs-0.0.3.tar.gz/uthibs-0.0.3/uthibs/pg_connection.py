# For postgres information
# https://www.postgresqltutorial.com/

# Imports
import sys
import time
import psycopg2
import requests
import numpy as np
import pandas as pd

  

class pgSqlManipulation():
    """ This class aims to facilitate connections to postrgre platforms
    """
    
    def __init__(self, env=None):
        
        # Connection to Postgre
        self.get_params()
        self.instanciate_connection()
        

    #####################################################################################
    #                              SQL Part (POSTGRES)
    #####################################################################################


    def get_params(self, env=None):
        """ Used to get the environment connection to postgres database
        """
        self.host = '172.17.0.1'
        self.db = 'postgres'
        self.user = 'admin'
        self.pwd = 'password'


    def instanciate_connection(self):
        self.conn = psycopg2.connect(host=self.host, database=self.db, user=self.user, password=self.pwd)
        self.cur = self.conn.cursor()


    def sql(self, sql_request):
        """ Execute an sql request on the specified dev environment
        """
        try:
            self.cur.execute(sql_request)
            self.conn.commit()
            print("Request executed: {}...".format(sql_request[:30]))
        except:
            self.reset_connection()
            raise


    def drop_table(self,table, cascade=False):
        request = 'drop table {};'.format(table)
        if cascade:
            print('WARNING: print CASCADE executed.')
            request = 'drop table {} cascade;'.format(table)
        

        rep = self.sql(request)
        # print(rep.status_code)


    def extract_table_from_request(self, request):
        post_from = request.lower().split('from')[1]
        table_name = post_from.split()[0]
        return table_name
        

    def sql_to_df(self, sql_request, with_col=False, index=None):
        """Converts an SQL request into a dataFrame
        - with_col : If True, send an other requests to get the column names of the table and set it to the DataFrame
        - index : if specified, set the selected column as index of the DataFrame 
        """
        self.cur.execute(sql_request)
        rows = self.cur.fetchall()
        df = pd.DataFrame(rows)

        if not with_col:
            return df

        table_name = self.extract_table_from_request(sql_request)
        columns = self.get_column_names(table_name)
        df.columns = columns

        return df if index is None else df.set_index(index)
    

    def get_df_with_id_as_index(self, sql_request):
        """Use the sql_to_df functions with specific parameters (Get column names = True, index=id)
        - Warning : will not work with materialized view (only table)
        """
        return self.sql_to_df(sql_request, with_col=True, index='id')


    def get_column_names(self, table_name):
        """ This function gets the column names of a table reqeusting its schema
        - Warning : will not work with materialized view (only classical table)
        """
        sql = """select column_name
        from INFORMATION_SCHEMA.COLUMNS
        where TABLE_NAME='{}';""".format(table_name)
        self.cur.execute(sql)
        columns = self.cur.fetchall()
        return [col[0] for col in columns]


    def reset_connection(self):
        """In case of problem in a request, there might be a connection issue.
            This function reset the connection and allows to keep the object alive.
        """
        self.conn.close()
        self.conn = psycopg2.connect(
            host=self.host,
            database=self.db,
            user=self.user,
            password=self.pwd
            )
        self.cur = self.conn.cursor()


    def create_sql_request_header(self, dataframe, table_name):
        """ (1/2) Used in the process of inserting data into a pocoto database.
            This is the creation of the header of the request
            Part 2 is 'create_sql_request_row' function
        """
        s = "INSERT INTO "
        s += table_name + "("
        for col in dataframe.columns:
            s+=col.lower() + ","
        s = s[:-1] + ") VALUES ("
        for i in range(len(dataframe.columns)):
            s+= "%s,"
        s = s[:-1] + ");"
        return s


    def create_sql_request_row(self, dataframe_row):
        """ (2/2) Used in the process of inserting data into a pocoto database.
            This is the creation of the content of the request
            Part 1 is 'create_sql_request_header' function
        """
        y = []
        for i in range(len(dataframe_row)):
            if pd.isnull(dataframe_row[i]) or dataframe_row[i] == "":
                y.append(None)
            else:
                val = dataframe_row[i]

                y.append(val)
        return y


    def df_2_table(self, df, table_name, create_table=False):
        """ Used to insert data into a pocoto DataBase, given a DataFrame and a table_name.
            NB : The table must have the columns of the DataFrame as fields.
        """
        if create_table:
            self.create_table_from_df(df, table_name)

        sql_request = self.create_sql_request_header(df, table_name)
        print(sql_request)

        for index, rows in df.iterrows():
            my_sql_row = self.create_sql_request_row(rows)
            # print(my_sql_row)
            self.cur.execute(sql_request,my_sql_row)
        self.conn.commit()
        print('> {} : dataframe correctly inserted.'.format(table_name))





    def create_table_from_df(self, df, table_name):
        cols = df.dtypes.apply(str)

        #########################################################
        # !!!!! Fulfill it. Only done for so far needeed types
        #########################################################
        cols = cols.replace('object', 'text')
        cols = cols.replace('int64', 'int8')
        cols = cols.replace('float64', 'float8')
        #########################################################
        cols = cols.to_dict()
        
        structure_table = ''
        for k, v in cols.items():
            structure_table += k + ' ' + v + ','

        structure_table = 'CREATE TABLE ' + table_name + '(' + structure_table[:-1] + ');'
        self.sql(structure_table)

    

    def get_tables(self):
        request = "SELECT * FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema';"
        return self.sql_to_df(request)

    def test(self):
        print('Salut les amis')
        