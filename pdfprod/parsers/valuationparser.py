__author__ = 'TalbotJ'

from xml.etree.ElementTree import parse


class ValuationData():

    def __init__(self, datafile):

        # no way this logic should be in here - the constructor should
        # probably just be passed the relevant print tag
        tree = parse(datafile)
        pack = tree.getroot()
        for printtag in pack:
            if printtag.findtext("./PrintCode[1]") == 'VALUATION ':
                for datatype in printtag:
                    if datatype.tag == 'Valuation':
                        self.holdings = self.parse_sector(datatype)
                        self.valuation_date = datatype.findtext("./ValHeader/Date")
                        self.valuation_cash = self.parse_cash(datatype)
                    elif datatype.tag == 'NameAndAddress':
                        self.add_na_data(datatype)
                    elif datatype.tag == 'BusinessGetterDetails':
                        self.business_getter = datatype.findtext('./BusinessGetterCode')
            elif printtag.tag == 'Routing':
                self.person_code = printtag.findtext("./Header1/PersonCode")

    def add_na_data(self, data):

        self.name_and_address = {
            "client_name": data.findtext("./ClientName"),
            "account_number": data.findtext("./AccountNumber"),
            "account_type": data.findtext("./Product")
        }


    def parse_cash(self, data):

        cash = []

        for element in data:
            if element.tag == 'CashLine':
                curr = {'currency': element.findtext('./CashCurrency'),
                        'balance': element.findtext('./CashBalance'),
                        'balance_val_cur': element.findtext('./BalanceInValCur'),
                        'account_number': element.findtext('./AccountNumber'),
                        'exchange_rate': element.findtext('./ExchangeRate'),
                        'account_type': ValuationData.convert_cash_type(element.findtext('./CashType'))}
                cash.append(curr)

        return cash

    @staticmethod
    def convert_cash_type(typ):
        if typ == 'CA':
            return 'Capital'
        elif typ == 'IN':
            return 'Income'
        else:
            return 'Unknown'

    @staticmethod
    def retrieve_holdings(data):

        holdings = []

        for element in data:
            if element.tag[0: 6] == 'Sector':
                holdings.append(element.findtext("./Description"))
                holdings.append(ValuationData.parse_sector(element))

        return holdings

    @staticmethod
    def parse_sector(sector):

        holdings = []
        for sub in sector:
            if sub.tag[0: 6] == 'Sector' and sub.tag[-5:] != 'Total':
                holdings.append(sub.findtext("./Description"))
                holdings.append(ValuationData.parse_sector(sub))
            elif sub.tag == 'ValDetail':
                holdings.append(ValuationData.parse_holding(sub))

        return holdings

    @staticmethod
    def parse_holding(hold):

        hold = {"sedol": hold.findtext("./Sedol"),
                "r1": hold.findtext("./StockIssuer"),
                "r2": hold.findtext("./SecurityDescription"),
                "book_cost": hold.findtext("./Cost"),
                "holding": hold.findtext("./Holding"),
                "price": hold.findtext("./Price"),
                "value": hold.findtext("./Value"),
                "income": hold.findtext("./Income"),
                "yield": hold.findtext("./Yield")}

        return hold

if __name__ == "__main__":

    import pprint
    val = ValuationData(r"C:\Users\user\Desktop\testftp\inputxml\TESTVALUATION.xml")
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(val.holdings)
    pp.pprint(val.valuation_cash)