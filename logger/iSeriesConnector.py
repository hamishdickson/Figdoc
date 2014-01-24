__author__ = 'hamishdickson'

#
# Connection to iSeries (proper)
#

# This class has been built with logging in mind - write success logs back to the iSeries

# This class uses pyodbc to do the hard work here. If this is ported to Jython (as at this
# point planned), then this will probably become redundent in favour of jt400 shizzle

# pyodbc docs can be found at https://code.google.com/p/pyodbc/wiki/

import pyodbc
import figconfig as figConfig


class ISeriesComs():
    _DRIVER = 'iSeries Access ODBC Driver'
    _SYSTEM = '10.0.0.1'
    _UID = 'XXXX'
    _PWD = 'XXXX'
    _DBQ = 'DEFAULTSCHEMA'
    _EXTCOLINFO = '1'

    _instance = None

    # todo: I'm not sure how much I trust this implementation of a singleton ... test it ...
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ISeriesComs, cls).__new__(cls, *args, **kwargs)
            return cls._instance

    def __init__(self):
        # set up coms link
        # todo: at the moment, if this fails it will try to use the default config. Sort that out
        try:
            self._config = figConfig.get_config("odbc")
            ISeriesComs._SYSTEM = self._config["system"]
            ISeriesComs._UID = self._config["username"]
            ISeriesComs._PWD = self._config["password"]
        except IOError as e:
            # decide something sensible to happen here
            print "There was an error getting the iSeries sign on configuration"

        connection_string = 'DRIVER=' + ISeriesComs._DRIVER + ';SYSTEM=' + ISeriesComs._SYSTEM + ';UID=' + ISeriesComs._UID + ';PWD=' + ISeriesComs._PWD + ';DBQ=' + ISeriesComs._DBQ + ';EXTCOLINFO=' + ISeriesComs._EXTCOLINFO
        con = pyodbd.connect(connection_string)
        self.cur = con.cursor()

    def run_sql_on_i_series(self, in_statement):
        # takes a record to write :)
        self.cur.execute(in_statement)

    def close_down_connection(self):
        # according to the official docs for pyodbc (https://code.google.com/p/pyodbc/wiki/Cursor), you don't actually
        # need this ... but ... it's a nice to have
        self.cur.close()