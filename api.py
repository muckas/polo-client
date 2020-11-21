from poloniex import Poloniex

with open('key') as f:
  api_key = f.read().rstrip('\n')
with open('secret') as f:
  api_secret = f.read().rstrip('\n')

polo = Poloniex(key=api_key, secret=api_secret)

def getTotalBTC():
  data = polo.returnCompleteBalances()
  for currency in data.copy():
    if data[currency]['btcValue'] == '0.00000000':
      data.pop(currency)
  totalBtc = 0.0
  for currency in data:
    totalBtc += float(data[currency]['btcValue'])
  return totalBtc

# TESTING
if __name__ == '__main__':
  output = getTotalBalance()
  print(output)
