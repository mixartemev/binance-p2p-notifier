import asyncio
import json

from httpx import AsyncClient, Response
from Ad import Ad
from loader import banks, URL_SRC, hds, gap
from reqs import tg_offers, _tg_send

ads = []
assets = {'USDT': [0, 0],
          'BUSD': [0, 0],
          'ETH':  [0, 0],
          'BTC':  [0, 0],
          'BNB':  [0, 0],
          'RUB':  [0, 0],
          'SHIB': [0, 0]}


async def get_ads(asset: str = 'USDT', threshold: float = None, sell: bool = False, fiat: str = 'RUB', amount: int = None):
    payload = {"page": 1, "rows": 5, "payTypes": list(banks.keys()), "asset": asset, "tradeType": "SELL" if sell else "BUY", "fiat": fiat}  # , "transAmount": amount

    async with AsyncClient() as client:
        resp: Response = await client.post(URL_SRC, headers=hds, json=payload)
        if resp.status_code == 200:
            data = resp.json().get('data')
            threshold = threshold or assets[asset][int(sell)]  # for fixes rate diapasons
            assets[asset][int(sell)] = float(data[0]['adv']['price'])
            if not threshold or assets[asset][0]*(1+gap) > assets[asset][1]:
                return
            for d in data:
                ad = Ad(d['adv'])
                if ad.price < min(threshold, assets[asset][0])*(1+gap) if sell else ad.price > max(threshold, assets[asset][1])*(1-gap):
                    return  # profitability check
                cond: bool = ad.advNo not in ads  # no repeat
                cond = cond and ad.minFiat <= amount
                if cond:  # or d['advertiser']['nickName'] == 'Hasy':
                    ads.append(ad.advNo)
                    return await tg_offers(ad, assets[asset])
            print('.', end='')
        else:
            txt = f'ERROR: {resp.status_code}'
            await _tg_send(txt)
            print(txt)


async def main():
    while True:
        old_assets = json.dumps(assets)
        for ast, prc in assets.items():
            await get_ads(asset=ast, threshold=prc[0], amount=10000)
            await get_ads(asset=ast, threshold=prc[1], sell=True, amount=110000)

        if json.dumps(assets) != old_assets:
            print(assets)

        # await asyncio.sleep(1)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print('Stopped.')
