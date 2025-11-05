import mysqlconnect
import swconfig as config


class SusseWurstConnect(mysqlconnect.MySQLDatabaseConnect):
    def __init__(self, db_name):
        super().__init__(db_name)



