import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtSql import QSqlDatabase
import settings as st

class Application(QApplication):
    def __init__(self, argv):
        super().__init__(argv)

        self.__db = QSqlDatabase.addDatabase('QPSQL')
        self.__db.setHostName(st.db_params['host'])
        self.__db.setPort(st.db_params['port'])
        self.__db.setDatabaseName(st.db_params['dbname'])
        self.__db.setUserName(st.db_params['user'])
        self.__db.setPassword(st.db_params['password'])
        ok = self.__db.open()
        if ok:
            print('Connected to database', file=sys.stderr)
        else:
            print('Connection FAILED', self.__db.lastError().text(), file=sys.stderr)

    @property
    def db_conn(self):
        return self.__db