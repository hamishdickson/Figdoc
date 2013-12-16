__author__ = 'TalbotJ'

from xml.etree.ElementTree import parse


class ContractNote():

    def __init__(self, datafile):

        tree = parse(datafile)
        pack = tree.getroot()
        self.account = pack.findtext("./Routing[1]/Header1[1]/ClientNumber[1]")
        self.r1 = pack.findtext("./Print[1]/ContractNoteLine2[1]/StockIssuer[1]")
        self.r2 = pack.findtext("./Print[1]/ContractNoteLine3[1]/SecurityDescription")
        self.quantity = pack.findtext("./Print[1]/ContractNoteC1Line[1]/Quantity[1]")
        self.contract_ref = pack.findtext("./Print[1]/ContractNoteLine1[1]/AccountLetter[1]") + pack.\
            findtext("./Print[1]/ContractNoteLine1[1]/ContractNumber[1]")
        self.contract_date = pack.findtext("./Print[1]/ContractNoteLine2[1]/BargainDate[1]")
        self.contract_time = pack.findtext("./Print[1]/ContractNoteLine2[1]/RunTime[1]")
        self.sedol = pack.findtext("./Print[1]/ContractNoteLine2[1]/Sedol[1]")
        self.account_name = pack.findtext("./Print[1]/ContractNoteLine1[1]/ClientFullName[1]")
        self.business_getter = pack.findtext("./Print[1]/ContractNoteLine1[1]/BusinessGetter[1]")
        self.venue = pack.findtext("./Print[1]/ContractNoteC1Line[1]/LineVenueDesc[1]")
        self.counterparty = pack.findtext("./Print[1]/ContractNoteLine5[1]/SecondParty[1]")
        self.service_category = self.parse_serv(pack.findtext(
            "./Print[1]/ContractNoteHeader[1]/TsaCategory[1]"))
        self.address = self.retrieve_address(pack)
        #TODO: do this properly!
        self.order_type = 'Market Order'
        self.price = pack.findtext("./Print[1]/ContractNoteC1Line[1]/Price[1]")
        self.price_currency = pack.findtext("./Print[1]/ContractNoteC1Line[1]/LineCurrency[1]")
        self.consideration = pack.findtext("./Print[1]/ContractNoteC1Line[1]/RightField[1]")
        self.charges = self.retrieve_charges(pack)
        self.settlement_date = pack.findtext("./Print[1]/ContractNoteLine3[1]/SettlementDate[1]")
        self.credit_or_debit, self.total_payment = self.retrieve_payment(pack)

    @staticmethod
    def retrieve_payment(pack):
        pay = []
        for line in pack.iter('ContractNoteC2Line'):
            if line.find('GbpEquivalent') is not None:
                if line.find('GbpEquivalent').text in ('Total Credit', 'Total Debit'):
                    if line.find('GbpEquivalent').text == 'Total Credit':
                        pay.append('credit')
                    else:
                        pay.append('debit')
                    pay.append(line.find('GbpEquivalent2').text)
                    break
        return pay

    @staticmethod
    def retrieve_charges(pack):
        charges = []
        i = 1
        while pack.findtext("./Print[1]/ContractNoteC2Line[%d]/GbpEquivalent[1]" % i) is not None:
            charges.append({'label': pack.findtext("./Print[1]/ContractNoteC2Line[%d]/GbpEquivalent[1]" % i),
                            'value': pack.findtext("./Print[1]/ContractNoteC2Line[%d]/GbpEquivalent2[1]" % i),
                            'currency': pack.findtext("./Print[1]/ContractNoteC2Line[%d]/LineCurrency[1]" % i)})
            i += 1
        return charges

    @staticmethod
    def retrieve_address(pack):
        addr = []
        for i in range(1, 6):
            addr.append(pack.findtext(
                "./Routing[1]/DeliveryAddress[1]/NameAndAddress[1]/Address"+str(i)+"[1]"))
        return addr

    @staticmethod
    def parse_serv(code):
        if code == 'X':
            return 'Execution Only'
        else:
            return ''

if __name__ == '__main__':
    testcn = ContractNote(r"C:\Users\talbotj\desktop\testftp\inputxml\CONTBD.09213F0211U.PO.20131205.130119.xml")
    print testcn.account
    print testcn.quantity
    print testcn.r1
    print testcn.r2
    print testcn.address
    print testcn.service_category
    print testcn.business_getter