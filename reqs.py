from httpx import AsyncClient, Response
from Ad import Ad
from loader import URL_TG, tgu, hds, budget


async def _tg_send(txt: str) -> Response:
    async with AsyncClient() as client:
        return await client.get(f'{URL_TG}sendMessage?text={txt}&chat_id={tgu}')


async def tg_offers(ad: Ad, diapason: []) -> Response:
    txt = f'{ad.tradeType} {ad.price} {ad.asset}/{ad.fiat}: {",".join(ad.tms)};\n' \
          f'send: {ad.minFiat} - {ad.maxFiat}.'  # \
    # f'get: {ad["minSingleTransQuantity"]} - {ad["dynamicMaxSingleTransQuantity"]}.'

    txt += f'\n{diapason}'

    cbd = ad.common()
    cmin = f'{cbd}:{ad.minFiat}'
    mxa = min(ad.maxFiat, budget)
    cmax = f'{cbd}:{mxa}'
    txt += '&reply_markup={"inline_keyboard":[[{"text":"'+str(ad.minFiat)+'","callback_data":"'+cmin+'"},{"text":"'+str(mxa)+'","callback_data":"'+cmax+'"}]]}'
    return await _tg_send(txt)


async def tg_my_ads(d: []) -> Response:
    pm = d["payMethods"][0]
    txt = f'{d["tradeType"]} {float(d["price"]):,.2f} {d["asset"]}/{d["fiat"]} ({d["amount"]})\n' \
          f'{float(d["totalPrice"]):,.2f} {d["fiatSymbol"]} to {pm["identifier"]}\n' \
          f'{pm["fields"][0]["fieldValue"]}: {pm["fields"][1]["fieldValue"]}'
    return await _tg_send(txt)


async def make_order(ad_id: str, tt: str, asset: str, fiat: str, price: float, pay_type: str, pay_id: str, amount: float) -> int:
    payload = {"advOrderNumber": ad_id, "asset": asset, "matchPrice": price, "fiatUnit": fiat,
               "buyType": "BY_MONEY", "totalAmount": amount, "tradeType": tt, "origin": "MAKE_TAKE",
               "payType": pay_type or None, "payId": pay_id or None}
    async with AsyncClient() as client:
        resp = await client.post('https://c2c.binance.com/bapi/c2c/v2/private/c2c/order-match/makeOrder', headers=hds, json=payload)
        if (res := resp.status_code) == 200 and (rj := resp.json())['code'] not in ['083685', '083688', '083625', '083022', '100001001']:
            print(f'ORDER {ad_id} MADE!')
            return res  # 200
        txt = f'MAKE ORDER ERROR: {res}\n{rj["message"] if res==200 else ""}'
        await _tg_send(txt)
        print(txt)
        return 0
