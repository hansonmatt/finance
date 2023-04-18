import getopt
import argparse
import csv
import datetime
import uuid
import mysql.connector
import configparser
import json

# application modules
import fidelityValidation
import transactionsUtil

# Initialize parser
parser = argparse.ArgumentParser()
# Adding optional argument
parser.add_argument("-i", "--input", type=open, required=True, help="Transaction input csv file")
parser.add_argument("-o", "--output", type=str, required=True, help="Transaction output csv file")
parser.add_argument("-e", "--error", type=str, default="error.csv", help="Path to error output file")
parser.add_argument("-a", "--account", type=str, required=True, help="SMA or Brokerage")
parser.add_argument("-c", "--config", type=str, default="config.ini", help="Path to configuration file")
parser.add_argument("-w", "--writedb", action='store_true', help="Write inserts to DB (default is dry run)")
# Read arguments from command line
args = parser.parse_args()
print("Program arguments = " + str(args))

config = configparser.ConfigParser()
config.read([args.config, 'application.ini'])
print("Config parameters = " + str(config))

smaAccount = config['fidelity-account-config']['sma.account']
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

brokerageAccount = config['fidelity-account-config']['brokerage.account']
brokeragetransactionTypeMap = {
    "YOU BOUGHT" : "BUY",
    "YOU SOLD" : "SELL",
    "DIVIDEND RECEIVED" : "DIV-CASH",
    "REINVESTMENT" : "DIV-REINVEST",
    "TRANSFERRED FROM" : "EFT-IN"
}

transactionValidationMap = {
    "BUY" : fidelityValidation.validateBuy,
    "SELL" : fidelityValidation.validateSell,
    "DIV-CASH" : fidelityValidation.validateDividendCash,
    "DIV-REINVEST" : fidelityValidation.validateReinvestDividend,
    "EFT-IN" : fidelityValidation.validateETFIn,
    "FEE" : fidelityValidation.validateFee,
    "SPLIT" : fidelityValidation.validateSplit_MergerIn,
    "TAX-FOREIGN" : fidelityValidation.validateForeignTax,
    "MERGR-AQUIS-IN" : fidelityValidation.validateSplit_MergerIn,
    "MERGR-AQUIS-OUT" : fidelityValidation.validateMergerOut,
    "MISC-IN" : fidelityValidation.validateMiscIn
}

if args.account == 'SMA':
     accountNumber = smaAccount
     transactionTypeMap = smatransactionTypeMap
     inOutColumnMap = json.loads(config['column-mapping-config']['sma.input.output.columnmap'])
elif args.account == 'Brokerage':
     accountNumber = brokerageAccount
     transactionTypeMap = brokeragetransactionTypeMap
     inOutColumnMap = json.loads(config['column-mapping-config']['brokerage.input.output.columnmap'])
else:
     raise RuntimeError("Unknown account " + args.account)

fieldnames = json.loads(config['application-config']['output.file.header.columnnames'])
outputFile = open(args.output, 'w', newline='')
writer = csv.DictWriter(outputFile, fieldnames=fieldnames)
writer.writeheader()

errorfieldnames = json.loads(config['application-config']['error.file.header.columnnames'])
errorFile = open(args.error, 'w', newline='')
errorWriter = csv.DictWriter(errorFile, fieldnames=errorfieldnames)
errorWriter.writeheader()

mySqlHost = config['mysql-connection-config']['host']
mySqlUser = config['mysql-connection-config']['user']
mySqlPwd = config['mysql-connection-config']['password']

# mysql
mysqlConnection = mysql.connector.connect(
  host=mySqlHost,
  user=mySqlUser,
  password=mySqlPwd
)
print(mysqlConnection)
cursor = mysqlConnection.cursor()
insertStatement = config['mysql-app-config']['mysql.transactions_stage_unique.insert']

numRows = 0
numProcessed = 0
numErrors = 0
numInserted = 0
reader = csv.DictReader(args.input)
for row in reader:
        numRows += 1
        #  Fidelity run date sample date = ' 03/27/2023'
        runDate = datetime.datetime.strptime(row[inOutColumnMap['transaction_date']], " %m/%d/%Y").strftime("%Y-%m-%d")
        # Fidelity output transaction date format = '2023-03-27'

        rowWriter = writer
        transactionTypeMatch = 0
        valid = False
        errorsList = []
        
        for key in transactionTypeMap:
            if key in row['Action']:
                transactionType = transactionTypeMap[key]
                transactionTypeMatch += 1

        if (transactionTypeMatch == 1):
            valid = True
        else:
            transactionType = 'ERROR'
            if (transactionTypeMatch == 0):
                errorsList.append("UNKNOWN TRANSACTION TYPE")
            else:
                errorsList.append("MULTIPLE TRANSACTION TYPE MATCHES")

        sourceShares = transactionsUtil.stringToFloatOrNone(row[inOutColumnMap['source_shares']])
        sourcePricePerShare = transactionsUtil.stringToFloatOrNone(row[inOutColumnMap['source_price_per_share']])
        sourceFees = transactionsUtil.stringToFloatOrNone(row[inOutColumnMap['source_fees']])
        sourceCommissions = transactionsUtil.stringToFloatOrNone(row[inOutColumnMap['source_commissions']])
        sourceTransactionAmt = transactionsUtil.stringToFloatOrNone(row[inOutColumnMap['source_transaction_amount']])

        insertTransactionDict = {'brokerage_account_number' : accountNumber,
                    'transaction_id' : '1',
                    'transaction_date': runDate,
                    'transaction_desc' : row[inOutColumnMap['transaction_desc']].strip(),
                    'transaction_type' : transactionType,
                    'symbol' : row[inOutColumnMap['symbol']].strip(),
                    'name' : row[inOutColumnMap['name']].strip(),
                    'source_shares' : sourceShares,
                    'source_price_per_share' : sourcePricePerShare,
                    'source_fees' : sourceFees,
                    'source_commissions' : sourceCommissions,
                    'source_transaction_amount' : sourceTransactionAmt
                    }

        if (valid):
            valid, errorsList = transactionValidationMap[transactionType](insertTransactionDict)

        if (valid):
            numProcessed += 1
        else:
            numErrors += 1
            errorString = ""
            for theError in errorsList:
                errorString = errorString.join(theError)

            insertTransactionDict['errors'] = errorString
            rowWriter = errorWriter

        if (valid):
            # insert
            try:
                print("Inserting row '" + str(insertTransactionDict) + "'")
                cursor.execute(insertStatement, insertTransactionDict)
                numInserted += 1
                print("MySQL table insert successful")
            except mysql.connector.Error as error:
                print("Unable to insert '" + str(insertTransactionDict) + "'")
                print("Insert error '" + str(error) + "'")
                numErrors += 1
                insertTransactionDict['errors'] = str(error)
                rowWriter = errorWriter

        rowWriter.writerow(insertTransactionDict)

print("Found '" + str(numRows) + "' rows in input file. Processed '" + str(numProcessed) + "' rows, encountered '" + str(numErrors) + "' errors")

outputFile.close()
errorFile.close()

if (args.writedb):
    if (numInserted == numRows):
        print("All good, committing inserts")
        mysqlConnection.commit()
    else:
        print("Rows inserted '" + str(numInserted) + "' not equal to rows processed '" + str(numRows)+ "'. Rolling back inserts")
        mysqlConnection.rollback()
else:
    print("This is a dryrun, rolling back inserts")
    mysqlConnection.rollback()

cursor.close()
mysqlConnection.close()