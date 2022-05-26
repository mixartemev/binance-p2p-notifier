import asyncio
from httpx import AsyncClient, Response, Timeout
from dotenv import load_dotenv

from loader import URL_TG
from reqs import make_order

load_dotenv()


async def main():
    updid = 0
    while True:
        async with AsyncClient() as client:
            resp: Response = await client.get(
                f'{URL_TG}getUpdates?limit=10&offset={updid}&allowed_updates=["callback_query"]',
                timeout=Timeout(connect=5, read=12, write=5, pool=2)
            )
            r = resp.json()
            res = r['result']
            if r['ok'] and res:
                updid = res[-1]['update_id']+1
                cb = res[-1]['callback_query']
                data = cb['data'].split(':')
                res = await make_order(*data)
                # await make_order(ad.advNo, asset, fiat, ad.price, ad.minFiat, sell)
                await client.get(f'{URL_TG}answerCallbackQuery?callback_query_id={cb["id"]}&text={cb["data"]}')  # &url=
                print(data)

        print('.', end='')
        await asyncio.sleep(1)

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print('Stopped.')
