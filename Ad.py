from loader import banks


class Ad:
    def __init__(self, adv: []):
        self.advNo: str = adv['advNo']
        self.tradeType: str = 'SELL' if adv['tradeType'] == 'BUY' else 'BUY'  # inverse
        self.asset: str = adv['asset']
        self.fiat: str = adv['fiatUnit']
        self.price: float = float(adv['price'])
        self.tms: [str] = [tm['identifier'] for tm in adv['tradeMethods']]
        self.minFiat: float = float(adv['minSingleTransAmount'])
        self.maxFiat: float = float(adv['dynamicMaxSingleTransAmount'])
        self.minAsset: float = float(adv['minSingleTransQuantity'])
        self.maxAsset: float = float(adv['dynamicMaxSingleTransQuantity'])
        self.commission: float = float(adv['commissionRate'])

    def common(self):
        bank = list(set(banks.keys()) & set(self.tms))[0] if self.tradeType == 'SELL' else ''
        pay_id = banks[bank] if self.tradeType == 'SELL' else ''
        return ':'.join([self.advNo, self.tradeType, self.asset, self.fiat, str(self.price), bank, pay_id])
