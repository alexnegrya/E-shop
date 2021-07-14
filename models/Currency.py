class Currency:
    def __init__(self, id_, code, nominal, rate):
        self.id = id_
        self.code = code
        self.nominal = nominal
        self.rate = rate

    def __str__(self):
        title = '--- Currency ---'
        id_ = f'Id: {self.id}'
        code = f'Code: {self.code}'
        nominal = f'Nominal: {self.nominal}'
        rate = f'Rate: {self.rate}'
        out = f'\n{title}\n{id_}\n{code}\n{nominal}\n{rate}\n'
        return out

    def __repr__(self):
        return str(self)

class CurrencyService:
    def getCurrencies(self):
        # Getting current date
        from datetime import date
        d = str(date.today()).split('-')
        d.reverse()
        current_date = ''
        for n in range(len(d)):
            if n == 0:
                current_date = current_date + d[n]
            else:
                current_date = current_date + '.' + d[n]
        # Parcing currencies
        import requests
        url = f'https://www.bnm.md/ru/official_exchange_rates?get_xml=1&date={current_date}'
        res = requests.get(url)
        data = res.text
        # Getting data from xml
        from xml.etree import ElementTree
        root = ElementTree.fromstring(data)
        out = []
        for i in range(len(root)):
            out.append(
                Currency(root[i].find('NumCode').text, root[i].find('CharCode').text,
                root[i].find('Nominal').text, root[i].find('Value').text)
                )
        return out
