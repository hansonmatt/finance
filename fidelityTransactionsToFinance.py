import getopt
import argparse
import csv
import datetime
import uuid
import mysql.connector
import configparser

def validateBuy(transactionDict):
    validationErrors = []
    if (transactionDict['brokerage_account_number'] != smaAccount and transactionDict['brokerage_account_number'] != brokerageAccount):
       validationErrors.append("Bad brokerage account number")
     
    if (transactionDict['transaction_type'] != 'BUY'):
       validationErrors.append("Transaction type '" + transactionDict['transaction_type'] + "' must be BUY")

    if (not transactionDict['transaction_date']):
       validationErrors.append("Transaction date '" + transactionDict['transaction_date'] + "' is empty")

    if (not transactionDict['transaction_desc']):
        validationErrors.append("Transaction desc '" + transactionDict['transaction_desc'] + "' is empty")

    if (not transactionDict['name']):
        validationErrors.append("Transaction equity name '" + transactionDict['name'] + "' is empty")
    
    if (not transactionDict['symbol']):
        validationErrors.append("Symbol '" + transactionDict['symbol'] + "' is empty")

    if (float(transactionDict['source_shares']) <= 0):
        validationErrors.append("Shares '" + str(transactionDict['source_shares']) + "' must be positive decimal")

    if (float(transactionDict['source_price_per_share']) <= 0):
        validationErrors.append("Price per share '" + str(transactionDict['source_price_per_share']) + "' must be positive decimal")

    if (float(transactionDict['source_transaction_amount']) >= 0):
        validationErrors.append("Transaction amount '" + str(transactionDict['source_transaction_amount']) + "' must be negative decimal")

    if (len(validationErrors) > 0):
        return False, validationErrors

    return True, validationErrors

def validateSell(transactionDict):
    validationErrors = []
    if (transactionDict['brokerage_account_number'] != smaAccount and transactionDict['brokerage_account_number'] != brokerageAccount):
       validationErrors.append("Bad brokerage account number")
     
    if (transactionDict['transaction_type'] != 'SELL'):
       validationErrors.append("Transaction type '" + transactionDict['transaction_type'] + "' must be SELL")

    if (not transactionDict['transaction_date']):
       validationErrors.append("Transaction date '" + transactionDict['transaction_date'] + "' is empty")

    if (not transactionDict['transaction_desc']):
        validationErrors.append("Transaction desc '" + transactionDict['transaction_desc'] + "' is empty")

    if (not transactionDict['name']):
        validationErrors.append("Transaction equity name '" + transactionDict['name'] + "' is empty")
    
    if (not transactionDict['symbol']):
        validationErrors.append("Symbol '" + transactionDict['symbol'] + "' is empty")

    if (float(transactionDict['source_shares']) >= 0):
        validationErrors.append("Shares '" + str(transactionDict['source_shares']) + "' must be negative decimal")

    if (float(transactionDict['source_price_per_share']) <= 0):
        validationErrors.append("Price per share '" + str(transactionDict['source_price_per_share']) + "' must be positive decimal")

    if (float(transactionDict['source_transaction_amount']) <= 0):
        validationErrors.append("Transaction amount '" + str(transactionDict['source_transaction_amount']) + "' must be positive decimal")

    if (transactionDict['source_fees'] and float(transactionDict['source_fees']) <= 0):
        validationErrors.append("Fees '" + str(transactionDict['source_fees']) + "' must be empty or a positive decimal")

    if (len(validationErrors) > 0):
        return False, validationErrors

    return True, validationErrors

def validateDividendCash(transactionDict):
    validationErrors = []
    if (transactionDict['brokerage_account_number'] != smaAccount and transactionDict['brokerage_account_number'] != brokerageAccount):
       validationErrors.append("Bad brokerage account number")
     
    if (transactionDict['transaction_type'] != 'DIV-CASH'):
       validationErrors.append("Transaction type '" + transactionDict['transaction_type'] + "' must be DIV-CASH")

    #if (len(transactionDict['transaction_date']) < 1):
    if (not transactionDict['transaction_date']):
       validationErrors.append("Transaction date '" + transactionDict['transaction_date'] + "' is empty")

    if (not transactionDict['transaction_desc']):
        validationErrors.append("Transaction desc '" + transactionDict['transaction_desc'] + "' is empty")

    if (not transactionDict['name']):
        validationErrors.append("Transaction equity name '" + transactionDict['name'] + "' is empty")
    
    if (not transactionDict['symbol']):
        validationErrors.append("Cash dividend symbol '" + transactionDict['symbol'] + "' is empty")

    if (transactionDict['source_shares']):
        validationErrors.append("Cash dividend should not have shares '" + transactionDict['source_shares'] + "'")

    if (transactionDict['source_price_per_share']):
        validationErrors.append("Cash dividend should not have price/share '" + transactionDict['source_price_per_share'] + "'")

    if (float(transactionDict['source_transaction_amount']) <= 0):
        validationErrors.append("Transaction amount '" + str(transactionDict['source_transaction_amount']) + "' must be positive decimal")

    if (len(validationErrors) > 0):
        return False, validationErrors

    return True, validationErrors

def validateFee(transactionDict):
    validationErrors = []
    if (transactionDict['brokerage_account_number'] != smaAccount and transactionDict['brokerage_account_number'] != brokerageAccount):
       validationErrors.append("Bad brokerage account number")
     
    if (transactionDict['transaction_type'] != 'FEE'):
       validationErrors.append("Transaction type '" + transactionDict['transaction_type'] + "' must be FEE")

    #if (len(transactionDict['transaction_date']) < 1):
    if (not transactionDict['transaction_date']):
       validationErrors.append("Transaction date '" + transactionDict['transaction_date'] + "' is empty")

    if (not transactionDict['transaction_desc']):
        validationErrors.append("Transaction desc '" + transactionDict['transaction_desc'] + "' is empty")

    if (not transactionDict['name']):
        validationErrors.append("Transaction equity name '" + transactionDict['name'] + "' is empty")
    
    if (transactionDict['symbol']):
        validationErrors.append("Fee symbol '" + transactionDict['symbol'] + "' must be empty")

    if (transactionDict['source_shares']):
        validationErrors.append("Fee should not have shares '" + transactionDict['source_shares'] + "'")

    if (transactionDict['source_price_per_share']):
        validationErrors.append("Fee should not have price/share '" + transactionDict['source_price_per_share'] + "'")

    if (float(transactionDict['source_transaction_amount']) >= 0):
        validationErrors.append("Transaction amount '" + str(transactionDict['source_transaction_amount']) + "' must be negative decimal")

    if (len(validationErrors) > 0):
        return False, validationErrors

    return True, validationErrors

def validateETFIn(transactionDict):
    validationErrors = []
    if (transactionDict['brokerage_account_number'] != smaAccount and transactionDict['brokerage_account_number'] != brokerageAccount):
       validationErrors.append("Bad brokerage account number")
     
    if (transactionDict['transaction_type'] != 'EFT-IN'):
       validationErrors.append("Transaction type '" + transactionDict['transaction_type'] + "' must be EFT-IN")

    if (not transactionDict['transaction_date']):
       validationErrors.append("Transaction date '" + transactionDict['transaction_date'] + "' is empty")

    if (not transactionDict['transaction_desc']):
        validationErrors.append("Transaction desc '" + transactionDict['transaction_desc'] + "' is empty")

    if (not transactionDict['name']):
        validationErrors.append("Transaction equity name '" + transactionDict['name'] + "' is empty")
    
    if (transactionDict['symbol']):
        validationErrors.append("ETF in symbol '" + transactionDict['symbol'] + "' must be empty")

    if (transactionDict['source_shares']):
        validationErrors.append("ETF in should not have shares '" + transactionDict['source_shares'] + "'")

    if (transactionDict['source_price_per_share']):
        validationErrors.append("ETF in should not have price/share '" + transactionDict['source_price_per_share'] + "'")

    if (float(transactionDict['source_transaction_amount']) <= 0):
        validationErrors.append("Transaction amount '" + str(transactionDict['source_transaction_amount']) + "' must be positive decimal")

    if (len(validationErrors) > 0):
        return False, validationErrors

    return True, validationErrors

def validateSplit_MergerIn(transactionDict):
    validationErrors = []
    if (transactionDict['brokerage_account_number'] != smaAccount and transactionDict['brokerage_account_number'] != brokerageAccount):
       validationErrors.append("Bad brokerage account number")
     
    if (not (transactionDict['transaction_type'] != 'MERGR-AQUIS-IN' or transactionDict['transaction_type'] != 'SPLIT')):
       validationErrors.append("Transaction type '" + transactionDict['transaction_type'] + "' must be SPLIT or MERGR-AQUIS-IN")

    if (not transactionDict['transaction_date']):
       validationErrors.append("Transaction date '" + transactionDict['transaction_date'] + "' is empty")

    if (not transactionDict['transaction_desc']):
        validationErrors.append("Transaction desc '" + transactionDict['transaction_desc'] + "' is empty")

    if (not transactionDict['name']):
        validationErrors.append("Transaction equity name '" + transactionDict['name'] + "' is empty")
    
    if (not transactionDict['symbol']):
        validationErrors.append("Symbol '" + transactionDict['symbol'] + "' is empty")

    if ((not transactionDict['source_shares']) or float(transactionDict['source_shares']) <= 0):
        validationErrors.append("Shares '" + transactionDict['source_shares'] + "' is empty or negative")

    if (transactionDict['source_price_per_share']):
        validationErrors.append("Price/share '" + transactionDict['source_price_per_share'] + "' must be empty")

    if (transactionDict['source_transaction_amount']):
        validationErrors.append("Transaction amount '" + str(transactionDict['source_transaction_amount']) + "' must be empty")

    if (len(validationErrors) > 0):
        return False, validationErrors

    return True, validationErrors

def validateMergerOut(transactionDict):
    validationErrors = []
    if (transactionDict['brokerage_account_number'] != smaAccount and transactionDict['brokerage_account_number'] != brokerageAccount):
       validationErrors.append("Bad brokerage account number")
     
    if (transactionDict['transaction_type'] != 'MERGR-AQUIS-OUT'):
       validationErrors.append("Transaction type '" + transactionDict['transaction_type'] + "' must be MERGR-AQUIS-OUT")

    if (not transactionDict['transaction_date']):
       validationErrors.append("Transaction date '" + transactionDict['transaction_date'] + "' is empty")

    if (not transactionDict['transaction_desc']):
        validationErrors.append("Transaction desc '" + transactionDict['transaction_desc'] + "' is empty")

    if (not transactionDict['name']):
        validationErrors.append("Transaction equity name '" + transactionDict['name'] + "' is empty")
    
    if (not transactionDict['symbol']):
        validationErrors.append("Symbol '" + transactionDict['symbol'] + "' is empty")

    if ((not transactionDict['source_shares']) or float(transactionDict['source_shares']) >= 0):
        validationErrors.append("Shares '" + transactionDict['source_shares'] + "' is empty or positive")

    if (transactionDict['source_price_per_share']):
        validationErrors.append("Price/share '" + transactionDict['source_price_per_share'] + "' must be empty")

    if (transactionDict['source_transaction_amount']):
        validationErrors.append("Transaction amount '" + str(transactionDict['source_transaction_amount']) + "' must be empty")

    if (len(validationErrors) > 0):
        return False, validationErrors

    return True, validationErrors

def validateForeignTax(transactionDict):
    validationErrors = []
    if (transactionDict['brokerage_account_number'] != smaAccount and transactionDict['brokerage_account_number'] != brokerageAccount):
       validationErrors.append("Bad brokerage account number")
     
    if (transactionDict['transaction_type'] != 'TAX-FOREIGN'):
       validationErrors.append("Transaction type '" + transactionDict['transaction_type'] + "' must be TAX-FOREIGN")

    if (not transactionDict['transaction_date']):
       validationErrors.append("Transaction date '" + transactionDict['transaction_date'] + "' is empty")

    if (not transactionDict['transaction_desc']):
        validationErrors.append("Transaction desc '" + transactionDict['transaction_desc'] + "' is empty")

    if (not transactionDict['name']):
        validationErrors.append("Transaction equity name '" + transactionDict['name'] + "' is empty")
    
    if (not transactionDict['symbol']):
        validationErrors.append("Foreign tax symbol '" + transactionDict['symbol'] + "' is empty")

    if (transactionDict['source_shares']):
        validationErrors.append("Foreign tax should not have shares '" + transactionDict['source_shares'] + "'")

    if (transactionDict['source_price_per_share']):
        validationErrors.append("Foreign tax should not have price/share '" + transactionDict['source_price_per_share'] + "'")

    if (float(transactionDict['source_transaction_amount']) >= 0):
        validationErrors.append("Transaction amount '" + str(transactionDict['source_transaction_amount']) + "' must be negative decimal")

    if (len(validationErrors) > 0):
        return False, validationErrors

    return True, validationErrors

def validateMiscIn(transactionDict):
    validationErrors = []
    if (transactionDict['brokerage_account_number'] != smaAccount and transactionDict['brokerage_account_number'] != brokerageAccount):
       validationErrors.append("Bad brokerage account number")
     
    if (transactionDict['transaction_type'] != 'MISC-IN'):
       validationErrors.append("Transaction type '" + transactionDict['transaction_type'] + "' must be MISC-IN")

    if (not transactionDict['transaction_date']):
       validationErrors.append("Transaction date '" + transactionDict['transaction_date'] + "' is empty")

    if (not transactionDict['transaction_desc']):
        validationErrors.append("Transaction desc '" + transactionDict['transaction_desc'] + "' is empty")

    if (not transactionDict['name']):
        validationErrors.append("Transaction equity name '" + transactionDict['name'] + "' is empty")
    
    if (not transactionDict['symbol']):
        validationErrors.append("Symbol '" + transactionDict['symbol'] + "' is empty")

    if (transactionDict['source_shares']):
        validationErrors.append("Shares '" + transactionDict['source_shares'] + "' must be empty")

    if (transactionDict['source_price_per_share']):
        validationErrors.append("Price/share '" + transactionDict['source_price_per_share'] + "' must be empty")

    if ((not transactionDict['source_transaction_amount']) or float(transactionDict['source_transaction_amount']) <= 0):
        validationErrors.append("Transaction amount '" + str(transactionDict['source_transaction_amount']) + "' must be positive")

    if (len(validationErrors) > 0):
        return False, validationErrors

    return True, validationErrors

def validateReinvestDividend(transactionDict):
    validationErrors = []
    if (transactionDict['brokerage_account_number'] != smaAccount and transactionDict['brokerage_account_number'] != brokerageAccount):
       validationErrors.append("Bad brokerage account number")
     
    if (transactionDict['transaction_type'] != 'DIV-REINVEST'):
       validationErrors.append("Transaction type '" + transactionDict['transaction_type'] + "' must be DIV-REINVEST")

    if (not transactionDict['transaction_date']):
       validationErrors.append("Transaction date '" + transactionDict['transaction_date'] + "' is empty")

    if (not transactionDict['transaction_desc']):
        validationErrors.append("Transaction desc '" + transactionDict['transaction_desc'] + "' is empty")

    if (not transactionDict['name']):
        validationErrors.append("Transaction equity name '" + transactionDict['name'] + "' is empty")
    
    if (not transactionDict['symbol']):
        validationErrors.append("Symbol '" + transactionDict['symbol'] + "' is empty")

    if (float(transactionDict['source_shares']) <= 0):
        validationErrors.append("Shares '" + str(transactionDict['source_shares']) + "' must be positive decimal")

    if (float(transactionDict['source_price_per_share']) <= 0):
        validationErrors.append("Price per share '" + str(transactionDict['source_price_per_share']) + "' must be positive decimal")

    if (float(transactionDict['source_transaction_amount']) >= 0):
        validationErrors.append("Transaction amount '" + str(transactionDict['source_transaction_amount']) + "' must be negative decimal")

    if (len(validationErrors) > 0):
        return False, validationErrors

    return True, validationErrors

def validateTrue(transactionDict):
    return True, []

def validateFalse(transactionDict):
    return False, ["Validation error always return false"]

# Initialize parser
parser = argparse.ArgumentParser()
# Adding optional argument
parser.add_argument("-i", "--input", type=open, required=True, help="Transaction input csv file")
parser.add_argument("-o", "--output", type=str, required=True, help="Transaction output csv file")
parser.add_argument("-e", "--error", type=str, default="error.csv", help="Path to error output file")
parser.add_argument("-a", "--account", type=str, required=True, help="SMA or Brokerage")
parser.add_argument("-c", "--config", type=str, default="config.ini", help="Path to configuration file")
parser.add_argument("-d", "--dryrun", type=bool, default=True, help="Dry run only, no DB inserts (default to dry run)")
# Read arguments from command line
args = parser.parse_args()
print("Program arguments = " + str(args))

smaAccount = 'Y80057518'
smatransactionTypeMap = {
    "YOU BOUGHT" : "BUY",
    "YOU SOLD" : "SELL",
    "DIVIDEND RECEIVED" : "DIV-CASH",
    "TRANSFERRED FROM" : "EFT-IN",
    "DISTRIBUTION" : "SPLIT",
    "ADVISORY FEE" : "FEE",
    "MERGER MER PAYOUT" : "MERGR-AQUIS-OUT",
    "FOREIGN TAX PAID" : "TAX-FOREIGN",
    "MERGER MER FROM" : "MERGR-AQUIS-IN",
    "IN LIEU OF FRX SHARE" : "MISC-IN"
}
smaColumnNameMap = {
     'priceColName' : 'Price ($)',
     'sourceFeesColName' : 'Fees ($)',
     'sourceCommissionColName' : 'Commission ($)',
     'sourceTransactionAmountColName' : 'Amount ($)',
}

brokerageAccount = 'X94896365'
brokeragetransactionTypeMap = {
    "YOU BOUGHT" : "BUY",
    "YOU SOLD" : "SELL",
    "DIVIDEND RECEIVED" : "DIV-CASH",
    "REINVESTMENT" : "DIV-REINVEST",
    "TRANSFERRED FROM" : "EFT-IN"
}
brokerageColumnNameMap = {
     'priceColName' : 'Price',
     'sourceFeesColName' : 'Fees',
     'sourceCommissionColName' : 'Commission',
     'sourceTransactionAmountColName' : 'Amount',
}

transactionValidationMap = {
    "BUY" : validateBuy,
    "SELL" : validateSell,
    "DIV-CASH" : validateDividendCash,
    "DIV-REINVEST" : validateReinvestDividend,
    "EFT-IN" : validateETFIn,
    "FEE" : validateFee,
    "SPLIT" : validateSplit_MergerIn,
    "TAX-FOREIGN" : validateForeignTax,
    "MERGR-AQUIS-IN" : validateSplit_MergerIn,
    "MERGR-AQUIS-OUT" : validateMergerOut,
    "MISC-IN" : validateMiscIn
}

if args.account == 'SMA':
     accountNumber = smaAccount
     transactionTypeMap = smatransactionTypeMap
     columnNameMap = smaColumnNameMap
elif args.account == 'Brokerage':
     accountNumber = brokerageAccount
     transactionTypeMap = brokeragetransactionTypeMap
     columnNameMap = brokerageColumnNameMap
else:
     raise RuntimeError("Unknown account " + args.account)

fieldnames = ['brokerage_account_number',
'transaction_id',
'transaction_date',
'transaction_type',
'transaction_desc',
'symbol',
'name',
'source_shares',
'currency','source_price_per_share','source_fees','source_commissions','source_transaction_amount',
'normalized_shares','normalized_transaction_amount','transaction_notes'
]
outputFile = open(args.output, 'w', newline='')
writer = csv.DictWriter(outputFile, fieldnames=fieldnames)
writer.writeheader()

errorfieldnames = ['brokerage_account_number',
'transaction_id',
'transaction_date',
'transaction_type',
'transaction_desc',
'symbol',
'name',
'source_shares',
'currency','source_price_per_share','source_fees','source_commissions','source_transaction_amount',
'normalized_shares','normalized_transaction_amount','transaction_notes','errors'
]
errorFile = open(args.error, 'w', newline='')
errorWriter = csv.DictWriter(errorFile, fieldnames=errorfieldnames)
errorWriter.writeheader()

config = configparser.ConfigParser()
config.read(args.config)
mySqlHost = config['mysql-config']['host']
mySqlUser = config['mysql-config']['user']
mySqlPwd = config['mysql-config']['password']
print("Config parameters = " + str(config))
# mysql
mysqlConnection = mysql.connector.connect(
  host=mySqlHost,
  user=mySqlUser,
  password=mySqlPwd
)
print(mysqlConnection)
cursor = mysqlConnection.cursor()
#insertStatement = ("insert into finance.transactions_staging "
#                   "(brokerage_account_number,transaction_id,transaction_date,transaction_type,transaction_desc,symbol,name,source_shares,currency,source_price_per_share,source_fees,source_commission,source_transaction_amount,normalized_shares,normalized_transaction_amount,transaction_notes) "
#                   "values (%(brokerage_account_number)s,%(transaction_id)s,%(transaction_date)s,%(transaction_type)s,%(transaction_desc)s,%(symbol)s,%(name)s,%(source_shares)s,%(currency)s,%(source_price_per_share)s,%(source_fees)s,%(source_commission)s,%(source_transaction_amount)s,%(normalized_shares)s,%(normalized_transaction_amount)s,%(transaction_notes)s)"
#)
insertStatement = ("insert into finance.transactions_staging "
                   "(brokerage_account_number,transaction_id,transaction_date,transaction_type,transaction_desc,symbol,name,source_shares,source_price_per_share,source_fees,source_commissions,source_transaction_amount) "
                   "values (%(brokerage_account_number)s,%(transaction_id)s,%(transaction_date)s,%(transaction_type)s,%(transaction_desc)s,%(symbol)s,%(name)s,%(source_shares)s,%(source_price_per_share)s,%(source_fees)s,%(source_commissions)s,%(source_transaction_amount)s)"
)

numRows = 0
numProcessed = 0
numErrors = 0
numInserted = 0
reader = csv.DictReader(args.input)
for row in reader:
        numRows += 1
        #  Fidelity run date sample date = ' 03/27/2023'
        runDate = datetime.datetime.strptime(row['Run Date'], " %m/%d/%Y").strftime("%Y-%m-%d")
        # Fidelity output transaction date format = '2023-03-27'

        rowWriter = writer
        transactionTypeMatch = 0
        valid = False
        errorsList = []
        
        for key in transactionTypeMap:
            if key in row['Action']:
                transactionType = transactionTypeMap[key]
                foundTransType = True
                transactionTypeMatch += 1

        if (transactionTypeMatch == 1):
            valid = True
        else:
            transactionType = 'ERROR'
            if (transactionTypeMatch == 0):
                errorsList.append("UNKNOWN TRANSACTION TYPE")
            else:
                errorsList.append("MULTIPLE TRANSACTION TYPE MATCHES")

        #theUUID = uuid.uuid4()
        transactionDict = {'brokerage_account_number' : accountNumber,
                'transaction_id' : str(uuid.uuid4()),
                'transaction_date': runDate,
                'transaction_desc' : row['Action'].strip(),
                'transaction_type' : transactionType,
                'symbol' : row['Symbol'].strip(),
                'name' : row['Security Description'].strip(),
                'source_shares' : row['Quantity'],
                'source_price_per_share' : row[columnNameMap['priceColName']],
                'source_fees' : row[columnNameMap['sourceFeesColName']],
                'source_commissions' : row[columnNameMap['sourceCommissionColName']],
                'source_transaction_amount' : row[columnNameMap['sourceTransactionAmountColName']]}


        if (valid):
            valid, errorsList = transactionValidationMap[transactionType](transactionDict)

        if (valid):
            numProcessed += 1
        else:
            numErrors += 1
            errorString = ""
            for theError in errorsList:
                errorString = errorString.join(theError)

            transactionDict['errors'] = errorString
            rowWriter = errorWriter

        if (valid):
            # insert
            try:
                symbol = row['Symbol'].strip() if row['Symbol'].strip() else None
                sourceShares = float(row['Quantity']) if row['Quantity'] else None
                sourcePricePerShare = float(row[columnNameMap['priceColName']]) if row[columnNameMap['priceColName']] else None
                sourceFees = float(row[columnNameMap['sourceFeesColName']]) if row[columnNameMap['sourceFeesColName']] else None
                sourceCommissions = float(row[columnNameMap['sourceCommissionColName']]) if row[columnNameMap['sourceCommissionColName']] else None
                sourceTransactionAmt = float(row[columnNameMap['sourceTransactionAmountColName']]) if row[columnNameMap['sourceTransactionAmountColName']] else None

                insertTransactionDict = {'brokerage_account_number' : accountNumber,
                    'transaction_id' : str(uuid.uuid4()),
                    'transaction_date': runDate,
                    'transaction_desc' : row['Action'].strip(),
                    'transaction_type' : transactionType,
                    #'symbol' : row['Symbol'].strip(),
                    'symbol' : symbol,
                    'name' : row['Security Description'].strip(),
                    #'source_shares' : row['Quantity'],
                    'source_shares' : sourceShares,
                    #'source_price_per_share' : row[columnNameMap['priceColName']],
                    'source_price_per_share' : sourcePricePerShare,
                    #'source_fees' : row[columnNameMap['sourceFeesColName']],
                    'source_fees' : sourceFees,
                    #'source_commissions' : row[columnNameMap['sourceCommissionColName']],
                    'source_commissions' : sourceCommissions,
                    #'source_transaction_amount' : row[columnNameMap['sourceTransactionAmountColName']]
                    'source_transaction_amount' : sourceTransactionAmt
                    }
                
                print("inserting " + str(insertTransactionDict))
                cursor.execute(insertStatement, insertTransactionDict)
                numInserted += 1
                print("MySQL table insert SUCCESSFUl!!!")
            except mysql.connector.Error as error:
                print("Unable to insert " + str(insertTransactionDict))
                print("Insert error" + str(error))
                numErrors += 1
                transactionDict['errors'] = str(error)
                rowWriter = errorWriter

        rowWriter.writerow(transactionDict)

print("Found '" + str(numRows) + "' rows in input file. Processed '" + str(numProcessed) + "' rows, encountered '" + str(numErrors) + "' errors")

outputFile.close()
errorFile.close()

if (args.dryrun):
    print("This is a dryrun, rolling back inserts")
    mysqlConnection.rollback()
else:
    if (numInserted == numRows):
        print("All good, committing inserts")
        mysqlConnection.commit()
    else:
        print("Rows inserted '" + str(numInserted) + "' not equal to rows processed '" + str(numRows)+ "'. Rolling back inserts")
        mysqlConnection.rollback()

cursor.close()
mysqlConnection.close()