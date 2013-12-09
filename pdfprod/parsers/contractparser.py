__author__ = 'TalbotJ'

from xml.etree.ElementTree import parse


class ContractNote():

    def __init__(self, datafile):

        tree = parse(datafile)
        pack = tree.getroot()
        self.account = pack.findtext("./Routing[1]/Header1[1]/ClientNumber[1]")
        self.r1 = pack.findtext("./Print[1]/ContractNoteLine2[1]/StockIssuer[1]")
        self.r2 = pack.findtext("./Print[1]/ContractNoteLine3[1]/SecurityDescription")
        self.quantity = pack.findtext("./Print[1]/ContractNoteC1Line[1]/LeftField[1]")

if __name__ == '__main__':
    testcn = ContractNote(r"C:\Users\talbotj\desktop\testftp\CONTBD.09213F0211U.PO.20131205.130119.xml")
    print testcn.account
    print testcn.quantity
    print testcn.r1
    print testcn.r2