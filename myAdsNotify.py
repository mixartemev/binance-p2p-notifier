# from deta import app
from httpx import Response, post, get
from loader import hds, tgu, URL_OL, URL_TG
from tg_send import tg_my_ads, _tg_send

ads = []


# @app.lib.cron()
def cron_job(event):
    resp: Response = post(URL_OL, headers=hds, json={"orderStatusList": [0, 1, 3, 5], "page": 1, "rows": 999})
    if resp.status_code == 200:
        for d in resp.json().get('data'):
            if d['advNo'] not in ads:
                resp: Response = await tg_my_ads(d)
                if resp.status_code == 200:
                    ads.append(d['advNo'])
        print('.', end='')
    else:
        txt = f'ERROR: {resp.status_code}'
        _tg_send(txt)
        print(txt)
