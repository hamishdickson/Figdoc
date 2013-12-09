__author__ = "TalbotJ"

import os
import ftplib
import time
import figconfig.figconfig as figconfig


class Grabber():
    """Fetch files over from the iSeries.

    Basically, this will just poll some directory on TRACEY, copy
    anything that's in there over to this machine, wait for a bit and
    then repeat.
    """

    def __init__(self):

        self._config = figconfig.get_config("grabber")
        self._outdir = self._config["todir"]
        self._fromdir = self._config["fromdir"]
        self._wait_time = self._config["interval"]
        self._user = self._config["user"]
        self._passwd = self._config["password"]
        self._iseries = self._config["iseries"]
        try:
            self._ftp = ftplib.FTP(self._iseries)
            print("connection made")
            self._ftp.login(user=self._user, passwd=self._passwd)
            print("logged in")
            self._ftp.sendcmd('site namefmt 1')
            print("changed format")
            self._ftp.cwd(self._fromdir)
            print("changed directory")
        except Exception as e:
            print("error connecting: " + str(e))
            raise e

    def go(self, outLocation=self._outdir):

        try:
            while True:
                self._transfer_files(outLocation)
                time.sleep(self._wait_time)
        except KeyboardInterrupt:
            print("exiting due to keyboard interruption")
        except Exception as e:
            print("exiting due to unknown exception: " + str(e))

    def _transfer_files(self, outLocation):
        """Find out what's on the iSeries, then copy it across"""

        files = self._ftp.nlst()
        if len(files) > 0:
            for fil in files:
                print("File on the i: " + str(fil))
                # HWD outfil = open(os.path.join(self._outdir, fil), "w")
                outfil = open(os.path.join(outLocation, fil), "w")
                print("New local file: " + str(outfil))
                self._ftp.retrbinary("RETR " + fil, outfil.write)
                outfil.close()
                self._ftp.delete(fil)
        else:
            print("no files found")
