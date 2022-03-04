# Binance p2p notifier
Alerts p2p orders to telegram.
Hosted at free cloud [deta](https://deta.sh).
### Install
```bash
git clone git@github.com:mixartemev/binance-p2p-notifier.git
cd binance-p2p-notifier
pip install -r requirements.txt
cp .env.sample .env
# add env values to .env
```
### Deploy
```bash
curl -fsSL https://get.deta.dev/cli.sh | sh  # deta-cli install
deta --python --name p2pn .
deta update -e .env
data cron set "1 minute"
```
