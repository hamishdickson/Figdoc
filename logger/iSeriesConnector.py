__author__ = 'hamishdickson'

import pyodbc


class ISeriesComs():
    _DRIVER = 'iSeries Access ODBC Driver'
    _SYSTEM = '10.0.0.1'
    _UID = 'XXXX'
    _PWD = 'XXXX'
    _DBQ = 'DEFAULTSCHEMA'
    _EXTCOLINFO = '1'

    def __init__(self):
        # set up coms link - this should be a singleton
        # todo: get config
        connection_string = 'DRIVER=' + self._DRIVER + ';SYSTEM=' + self._SYSTEM + ';UID=' + self._UID + ';PWD=' + self._PWD + ';DBQ=' + self._DBQ + ';EXTCOLINFO=' + self._EXTCOLINFO
        con = pyodbd.connect(connection_string)
        self.cur = con.cursor()

    def run_sql_on_i_series(self, in_statement):
        # takes a record to write :)
        self.cur.execute(in_statement)

    def close_down_connection(self):
        # according to the official docs for pyodbc (https://code.google.com/p/pyodbc/wiki/Cursor), you don't actually
        # need this ... but ... it's a nice to have
        self.cur.close()