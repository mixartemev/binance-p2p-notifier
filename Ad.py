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
        # b = list(set(banks) & set(self.tms))[0]  # best available bank
        return ':'.join([self.advNo, self.tradeType, self.asset, self.fiat, str(self.price)])
