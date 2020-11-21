from poloniex import Poloniex

with open('key') as f:
  api_key = f.read().rstrip('\n')
with open('secret') as f:
  api_secret = f.read().rstrip('\n')

polo = Poloniex(key=api_key, secret=api_secret)
