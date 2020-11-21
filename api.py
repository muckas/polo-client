from poloniex import Poloniex

with open('key') as f:
  api_key = f.read().rstrip('\n')
with open('secret') as f:
  api_secret = f.read().rstrip('\n')

polo = Poloniex(key=api_key, secret=api_secret)

def getAllBalances(total=False):
  balances = polo.returnCompleteBalances()
  for currency in balances.copy():
    if balances[currency]['btcValue'] == '0.00000000':
      balances.pop(currency)
  if total:
    totalBtc = 0.0
    for currency in balances:
      totalBtc += float(balances[currency]['btcValue'])
    return f'{totalBtc:.8f}'
  else:
    return balances

# TESTING
if __name__ == '__main__':
  output = getAllBalances(True)
  print(output)
