# Imports
import argparse
import csv
import os
from datetime import date, timedelta
from tabulate import tabulate


# Do not change these lines.
__winc_id__ = 'a2bc36ea784242e4989deb157d527ba0'
__human_name__ = 'superpy'
     
# Your code below this line.
dateFile = 'date.txt'
inFile = 'in.csv'
outFile = 'out.csv'
inList = []
outList = []

def main():
    validateArguments()
    loadIn()
    loadOut()
    if (args.action == 'profit'):
        showProfit()
    if (args.action == 'inventory'):
        showInventory()
    if (args.action == 'buy'):
        buyProduct(args.name, args.amount, args.price, args.expires)
    if (args.action == 'sell'):
        attemptSellProduct()
    if (args.action == 'today'):
        if (args.reset == True):
            todayReset()
        elif (args.setdate != None):
            todaySet(args.setdate)
        elif (args.setdays != None):
            todaySetOffset(args.setdays)
        else:
            print(todayGet())
        

parser = argparse.ArgumentParser()
parser.add_argument('action', choices=['buy', 'sell', 'inventory', 'profit', 'today'], help='The action to perform')
parser.add_argument('--amount', type=int, default=1, help='The amount of the product')
parser.add_argument('--name', type=str, help='The name of the product')
parser.add_argument('--id', type=int, help='The id of the product')
parser.add_argument('--expires', type=str, help='The date on which a product expires (yyyy-mm-dd)')
parser.add_argument('--price', type=float, help="The price of the product")
parser.add_argument('--reset', action="store_true")
parser.add_argument('--setdate', type=str, help='The date to set (yyyy-mm-dd)')
parser.add_argument('--setdays', type=int, help='The date to set, in offset of days from current date')
parser.add_argument('--date', type=str, help='The exact date used for reporting (yyyy-mm-dd OR now)')
parser.add_argument('--mindate', type=str, help='The start date used for reporting (yyyy-mm-dd or now)')
parser.add_argument('--maxdate', type=str, help='The end date used for reporting (yyyy-mm-dd or now)')

args = parser.parse_args()

def validateArguments():
    if args.action == 'buy' and (args.name is None or args.price is None or args.expires is None):
        parser.error('buy requires --name, --price and --expires')
    if args.action == 'sell' and (args.name is None or args.price is None):
        parser.error('sell requires --name, --price')

def showInventory():
    items = filterInventory(args.id, args.name, args.date, args.mindate, args.maxdate)
    items = setAvailability(items)
    items = setExpired(items)
    print (tabulate(items, headers="keys", tablefmt="grid"))

def showProfit():
    amount_out = 0
    amount_in = 0
    items_bought = filterInventory(None, None, args.date, args.mindate, args.maxdate)
    items_sold = filterSold(args.date, args.mindate, args.maxdate)

    for product in items_bought:
        amount_out += product['amount'] * product['price']

    for product in items_sold:
        amount_in += product['amount'] * product['price']

    print("out: " + str(round(amount_out, 2)))
    print("in: " + str(round(amount_in, 2)))
    print("profit: " + str(round(amount_in - amount_out, 2)))

def setAvailability(items):
    for product in items:
        soldItems = list(filter(lambda x: x['in_id'] == product['id'], outList))
        soldItemAmounts = list(map(lambda x: x['amount'], soldItems))
        product['sold'] = sum(soldItemAmounts)
        product['available'] = max(0, product['amount'] - product['sold'])
    return items

def setExpired(items):
    for product in items:
        product['expired'] = product['date_expired'] < todayGet()
    return items

def filterSold(date, mindate, maxdate):
    items = outList
    if (date is not None):
        if (date == 'now'):
            d = todayGet()
        else:
            d = stringToDate(date)
        items = list(filter(lambda x: x['date_sold'] == d, items))
    if (mindate is not None):
        if (mindate == 'now'):
            d = todayGet()
        else:
            d = stringToDate(mindate)
        items = list(filter(lambda x: x['date_sold'] >= d, items))
    if (maxdate is not None):
        if (maxdate == 'now'):
            d = todayGet()
        else:
            d = stringToDate(maxdate)
        items = list(filter(lambda x: x['date_sold'] <= d, items))

    return items

def filterInventory(id, name, date, mindate, maxdate, withExpired = True):
    items = inList
    if (id is not None):
        items = list(filter(lambda x: x['id'] == id, items))
    if (name is not None):
        items = list(filter(lambda x: x['name'].lower() == name.lower(), items))
    if (date is not None):
        if (date == 'now'):
            d = todayGet()
        else:
            d = stringToDate(date)
        items = list(filter(lambda x: x['date_bought'] == d, items))
    if (mindate is not None):
        if (mindate == 'now'):
            d = todayGet()
        else:
            d = stringToDate(mindate)
        items = list(filter(lambda x: x['date_bought'] >= d, items))
    if (maxdate is not None):
        if (maxdate == 'now'):
            d = todayGet()
        else:
            d = stringToDate(maxdate)
        items = list(filter(lambda x: x['date_bought'] <= d, items))
    if (withExpired == False):
        items = list(filter(lambda x: x['date_expired'] < todayGet(), items))

    return items

def todayReset():
    if os.path.exists(dateFile):
        os.unlink(dateFile)

def todaySet(dateString):
    file = open(dateFile, 'w')
    file.write(dateToString(stringToDate(dateString)))

def todaySetOffset(offsetInDays):
    offsetDate = date.today() + timedelta(days=offsetInDays)
    file = open(dateFile, 'w')
    file.write(dateToString(offsetDate))

def todayGet():
    if os.path.exists(dateFile):
        file = open(dateFile, 'r')
        return stringToDate(file.read())
    else:
        return date.today()

def loadIn():
    with open(inFile) as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for row in csvreader:
            product = createInProductFromRow(row)
            inList.append(product)

def loadOut():
    with open(outFile) as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        for row in csvreader:
            product = createOutProductFromRow(row)
            outList.append(product)

def writeToIn(product):
    with open(inFile, 'a', newline='') as csvfile: 
        csvwrite = csv.writer(csvfile, delimiter=',')
        row = createRowFromInProduct(product)
        csvwrite.writerow(row)
    
def writeToOut(product):
    with open(outFile, 'a', newline='') as csvfile: 
        csvwrite = csv.writer(csvfile, delimiter=',')
        row = createRowFromOutProduct(product)
        csvwrite.writerow(row)


def createInProductFromRow(row):
    product = {
        'id': int(row[0]),
        'name': row[1],
        'amount': int(row[2]),
        'price': float(row[3]),
        'date_expired': stringToDate(row[4]),
        'date_bought': stringToDate(row[5])
    }
    return product

def createOutProductFromRow(row):
    product = {
        'id': int(row[0]),
        'in_id': int(row[1]),
        'amount': int(row[2]),
        'price': float(row[3]),
        'date_sold': stringToDate(row[4])
    }
    return product

def createRowFromInProduct(product):
    row = [
        product['id'], 
        product['name'], 
        product['amount'],
        product['price'],
        dateToString(product['date_expired']),
        dateToString(product['date_bought'])
    ]
    return row

def createRowFromOutProduct(product):
    row = [
        product['id'], 
        product['in_id'], 
        product['amount'],
        product['price'],
        dateToString(product['date_sold'])
    ]
    return row

def stringToDate(string):
    dateList = string.split('-')
    if (len(dateList) != 3):
        raise SystemExit("Invalid date: " + string)
    return date(int(dateList[0]), int(dateList[1]), int(dateList[2]))
    
def dateToString(date):
    return date.strftime('%Y-%m-%d')

def buyProduct(name, amount, price, date_expired):
    nextId = 1
    if len(inList) > 0:
        ids = list(map(lambda x: x['id'], inList))
        nextId = max(ids) + 1

    if (date_expired == 'now'):
        dateExpired = todayGet()
    else:
        dateExpired = stringToDate(date_expired)

    product = {
        'id': nextId,
        'name': name,
        'amount': amount,
        'price': price,
        'date_expired': dateExpired,
        'date_bought': todayGet()
    }
    writeToIn(product)
    inList.append(product)

def attemptSellProduct():
    if (args.id is None):
        items = filterInventory(None, args.name, None, None, None, False)
    else: 
        items = filterInventory(args.id, args.name, None, None, None, False)

    items = setAvailability(items)
    items = list(filter(lambda x: x['available'] > 0, items))


    if (len(items) == 0):
        print('Product not available...')
    elif (len(items) == 1):
        if (args.amount <= items[0]['available']):
            sellProduct(items[0]['id'], args.amount, args.price)
        else:
            print('Only ' + str(items[0]['available']) + ' items(s) available...')
    else:
        print('Multiple products found... Please specify the id:')
        print(tabulate(items, headers="keys", tablefmt="grid"))


def sellProduct(in_id, amount, price):
    nextId = 1
    if len(outList) > 0:
        ids = list(map(lambda x: x['id'], outList))
        nextId = max(ids) + 1

    product = {
        'id': nextId,
        'in_id': in_id,
        'amount': amount,
        'price': price,
        'date_sold': todayGet()
    }
    writeToOut(product)
    outList.append(product)

if __name__ == '__main__':
    main()
