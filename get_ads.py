import asyncio

from httpx import AsyncClient, Response
from Ad import Ad
from loader import banks, URL_SRC, hds
from reqs import tg_offers, _tg_send

ads = []


async def get_ads(asset: str = 'USDT', threshold: float = None, sell: bool = False, fiat: str = 'RUB', amount: int = None):
    payload = {"page": 1, "rows": 20, "payTypes": banks, "asset": asset, "tradeType": "SELL" if sell else "BUY", "fiat": fiat, "transAmount": amount}
    async with AsyncClient() as client:
        resp: Response = await client.post(URL_SRC, headers=hds, json=payload)
        if resp.status_code == 200:
            for d in resp.json().get('data'):
                ad = Ad(d['adv'])
                cond: bool = (ad.price >= threshold if sell else ad.price <= threshold) if threshold else True  # profitability
                cond = cond and ad.advNo not in ads  # no repeat
                if cond:  # or d['advertiser']['nickName'] == 'Hasy':
                    await tg_offers(ad)
                    ads.append(ad.advNo)
            print('.', end='')
        else:
            txt = f'ERROR: {resp.status_code}'
            await _tg_send(txt)
            print(txt)


async def main():
    while True:
        await get_ads(asset='USDT', threshold=72.5, amount=1000)
        await get_ads(asset='BUSD', threshold=72)
        await get_ads(asset='RUB', threshold=1.07)
        await get_ads(asset='ETH', threshold=130000)
        await get_ads(asset='BTC', threshold=2000000)
        await get_ads(asset='BNB', threshold=22000)
        # await get_ads(asset='SHIB', threshold=0.0007)  #

        await get_ads(asset='USDT', threshold=73, sell=True)
        await get_ads(asset='BUSD', threshold=73, sell=True)
        await get_ads(asset='RUB', threshold=1.15, sell=True)
        await get_ads(asset='ETH', threshold=136000, sell=True)
        await get_ads(asset='BTC', threshold=2160000, sell=True)
        await get_ads(asset='BNB', threshold=23000, sell=True)
        # await get_ads(asset='SHIB', threshold=0.0008, sell=True)  #
        # await get_ads(asset='USDT', threshold=0.9, sell=False, fiat='EUR')
        # await get_ads(asset='ETH', threshold=2350, sell=False, fiat='EUR')
        # await get_ads(asset='BTC', threshold=35500, sell=False, fiat='EUR')
        # await get_ads(asset='BNB', threshold=335, sell=False, fiat='EUR')

        # await asyncio.sleep(1)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print('Stopped.')
