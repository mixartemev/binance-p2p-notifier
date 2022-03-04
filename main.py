from deta import app
import httpx
from httpx import Response
from dotenv import load_dotenv
from os import getenv as env

load_dotenv()  # take environment variables from .env.

URL = "https://p2p.binance.com/bapi/c2c/v2/private/c2c/order-match/order-list"
hds = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36',
    'content-type': 'application/json',
    'csrftoken': env('csrf'),
    'cookie': env('cookie'),
    'clienttype': 'web',
}


def msg(text: str):
    httpx.get(f'https://api.telegram.org/bot{env("bot")}/sendMessage?text={text}&chat_id={env("tgu")}')


@app.lib.cron()
def cron_job(event):
    resp: Response = httpx.post(URL, headers=hds, json={"orderStatusList": [0, 1, 3, 5], "page": 1, "rows": 999})
    if resp.status_code == 200:
        for d in resp.json().get('data'):
            pm = d["payMethods"][0]
            txt = f'{d["tradeType"]} {float(d["price"]):,.2f} {d["asset"]}/{d["fiat"]} ({d["amount"]})\n' \
                  f'{float(d["totalPrice"]):,.2f} {d["fiatSymbol"]} to {pm["identifier"]}\n' \
                  f'{pm["fields"][0]["fieldValue"]}: {pm["fields"][1]["fieldValue"]}'
            msg(txt)
        print('.', end='')
    else:
        txt = f'ERROR: {resp.status_code}'
        msg(txt)
        print(txt)
