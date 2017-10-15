
import json
import urllib.request
import time
import numpy as np

# for macbook python3
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


walletBitcoin = 0.0
walletDollar = 100000.0
transection = 0.002
oldPrice = []
buyPrice = []
sellPrice = []
coeffBuy = 0.5
coeffSell = 0.5
timeLoop = 1

print ('Starting simulator...')
def getMidPrice():
    with urllib.request.urlopen('https://api.bitfinex.com/v1/pubticker/btcusd') as response:
        html = response.read()
    return float(json.loads(html)['mid'])

def getSellPrice():
    with urllib.request.urlopen('https://api.bitfinex.com/v1/pubticker/btcusd') as response:
        html = response.read()
    return float(json.loads(html)['last_price'])

currentPrice = getSellPrice()
midPrice = getMidPrice()

def getTransectionfee():
    return transection * currentPrice

buyPrice.append(currentPrice + getTransectionfee())
sellPrice.append(currentPrice - getTransectionfee())
currentSell =  currentPrice - getTransectionfee()
currentBuy =  currentPrice + getTransectionfee()
arverageBuy = sum(buyPrice)/len(buyPrice)
arverageSell = sum(sellPrice)/len(sellPrice)

def getTotalNetWorth():
    return walletDollar + (walletBitcoin * currentPrice)

def showTotalNetWorth():
    print ('MidPrice:', midPrice)
    print ('Total bitcoin:', walletBitcoin, 'walletDollar', walletDollar)
    print ('Total networth:', getTotalNetWorth(), 'profit', getTotalNetWorth() - totalNetWorthStart )
    print ("Arverage buy price:", sum(buyPrice)/len(buyPrice))
    print ("Arverage sell price:", sum(sellPrice)/len(sellPrice))

totalNetWorthStart = getTotalNetWorth()

while True:
    timeLoop = 1 + timeLoop
    currentPrice = getSellPrice()
    midPrice = getMidPrice()
    oldPrice.append(currentPrice)
    previousPrice = np.mean(oldPrice)
    currentBuy  =  currentPrice + getTransectionfee()
    currentSell =  currentPrice - getTransectionfee()
    arverageBuy = sum(buyPrice)/len(buyPrice)
    arverageSell = sum(sellPrice)/len(sellPrice)
    profit = getTotalNetWorth() - totalNetWorthStart
    print ('---------timeLoop: ',timeLoop)
    print ('previousPrice: ',previousPrice,'currentPrice: ',currentPrice)
    print ('currentBuy: ',currentBuy,'currentSell: ',currentSell)


    if  profit > 0 and currentSell > previousPrice and walletBitcoin > 0:
        print ("sell....")
        sellPrice.append(currentPrice - getTransectionfee())
        print ("Arverage sell price:", arverageSell)

        walletBitcoin = walletBitcoin - coeffSell
        walletDollar = walletDollar + coeffSell * currentSell
    elif currentBuy < previousPrice  * 1.001 and walletDollar > currentBuy:
        print ("buy......")
        buyPrice.append(currentPrice + getTransectionfee())
        print ("Arverage buy price:", arverageBuy)

        walletBitcoin = walletBitcoin + coeffBuy
        walletDollar = walletDollar - coeffBuy * currentBuy
    showTotalNetWorth()

    time.sleep(3)
