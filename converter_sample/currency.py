from bs4 import BeautifulSoup
from decimal import Decimal


def convert(amount, cur_from_, cur_to_, date, request):
    class Currency:
        def __init__(self, XML_daily, charcode='RUR', ID=None, nominal=1, value=1):
            self.charcode = charcode
            self.ID = ID
            self.nominal = nominal
            self.value = value
            self.from_cbr_XML(XML_daily)

        def from_cbr_XML(self, XML_daily):
            if 'RUR' != self.charcode:
                for currency in XML_daily.find_all('valute'):
                    if self.charcode in currency.charcode.text:
                        self.ID = currency.attrs['id']
                        self.nominal = Decimal(currency.nominal.text)
                        self.value = Decimal(currency.value.text.replace(',', '.'))

        def __repr__(self):
            return 'charcode={}, ID={}, nominal={}, value={}'.format(self.charcode,
                                                                     self.ID,
                                                                     self.nominal,
                                                                     self.value)

        def to_currency(self, amount):
            return Decimal(amount) * self.nominal / self.value

        def from_currency(self, amount):
            return Decimal(amount) * self.value / self.nominal

    host = 'https://www.cbr.ru/scripts/XML_daily.asp'
    params = dict(date_req=date)
    XML_daily = BeautifulSoup(request.get(host, params=params).text, 'lxml').valcurs

    result = Currency(XML_daily, charcode=cur_to_).to_currency(
        Currency(XML_daily, charcode=cur_from_).from_currency(amount)
    )

    return result.quantize(Decimal('.0001'))  # не забыть про округление до 4х знаков после запятой
