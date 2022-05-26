from dotenv import load_dotenv
from os import getenv as env

load_dotenv()

budget = 1000
tgu = env('tgu')
URL_SRC = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
URL_TG = f'https://api.telegram.org/bot{env("bot")}/'
URL_OL = "https://p2p.binance.com/bapi/c2c/v2/private/c2c/order-match/order-list"
hds = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36',
    'content-type': 'application/json',
    'csrftoken': env('csrf'),
    'cookie': env('cookie'),
    'clienttype': 'web',
}
banks = [
    "Tinkoff",
    "RosBank",
    "YandexMoney",
    "QIWI",
    "PostBankRussia",
    "UralsibBank",
    "RaiffeisenBankRussia",
    "BCSBank",
    "HomeCreditBank",
    "AkBarsBank",
    "VostochnyBank",
    "RussianStandardBank",
    "ABank",
    "MTSBank",
    # "BANK",

    # "RUBfiatbalance",
    # "Advcash",
    # "Payeer",

    # "CitibankRussia",
    # "UniCredit",
    # "CreditEuropeBank(Russia)",
    # "RenaissanceCreditBank",
    # "OTP",
    # "Transferswithspecificbank",
    # "CashinPerson",
    # "CashDeposittoBank",
    # "Mobiletop-up",
    # "SBP-FastBankTransfer",
    # "Sberbank",
    # "Alfa-bank",
    # "BankSaint-Petersburg",
]
