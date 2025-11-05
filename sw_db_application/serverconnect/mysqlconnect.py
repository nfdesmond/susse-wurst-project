import mysql.connector as mysqlconn
from mysql.connector import errorcode
import serverconnect.mysqlconfig as mysqlconfig


class MySQLDatabaseConnect:
    def __init__(self, db_name):
        self.__db_name = db_name

    def mysql_connect(self, 
                      user, 
                      user_pswrd,
                      server_address=mysqlconfig.SERVER,
                      port_num=mysqlconfig.PORT):
    
        cxn_config = {'user': user,
                      'password': user_pswrd,
                      'host': server_address,
                      'database': self.__db_name,
                      'port': port_num}
        try:
            self.__cxn = mysqlconn.connect(**cxn_config)
        
        except mysqlconn.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print(
                    'ERROR: Unable to access the database.' 
                    + ' Please check your username and/or password.'
                    )
                print(f'(See MySQL Error Number {err.errno}: "{err.msg})"')
                
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print('ERROR: The requested database doesn''t exist.')
                print(f'(See MySQL Error Number {err.errno}: "{err.msg}")')
                
            elif err.errno == errorcode.CR_UNKNOWN_HOST:
                print(
                    "ERROR: The server you're trying to reach is unknown."
                    + " Please contact your administrator for assistance."
                    )
                print(f'(See MySQL Error Number {err.errno}: "{err.msg}")')
                
            elif err.errno == errorcode.CR_CONN_HOST_ERROR:
                print(
                    "ERROR: The server can't be contacted using the given port number."
                    + " Please contact your administrator for assistance."
                    )
                print(f'(See MySQL Error Number {err.errno}: "{err.msg}")')
                
            else:
                print(f'ERROR NUMBER: {err.errno}')
                print(f'SERVER MESSAGE: {err.msg}')
        else:
            print(f'Access granted.')
        
        return self.__cxn
    
    
    def cxn_test(self, cxn):
        self.__cxn_test = None
        
        if cxn and cxn.is_connected():
            self.__cxn_test = True
        else:
            self.__cxn_test = False 
            
        return self.__cxn_test
    
    
        
    def create_mysql_cursor(self,
                            cxn,
                            use_buffered=True,
                            use_raw=False,
                            used_prepared=False):
        
        self.__cursor = cxn.cursor(buffered=use_buffered, raw=use_raw, prepared=used_prepared)
        
        return self.__cursor
    
    
    
    def execute_query(self,
                      cursor,
                      sql_query):
        
        cursor.execute(sql_query)
        
        self.__result = cursor.fetchall()
        
        return self.__result 




