
import argparse
import csv
import uuid
import mysql.connector
import configparser
import json

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
#print("Config parameters = " + str(config))

try:
    module = __import__(config[args.account + '-processor']['row.processor.module'])
    rowProcessorClass = getattr(module, config[args.account + '-processor']['row.processor.class'])(config)
    print(f"Transaction row processor = '{rowProcessorClass}'")
except Exception as error:
    raise RuntimeError("Config parsing exception for account = " + args.account + "', error = " + str(error))

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
print(f"MySQL host = '{mySqlHost}', user = '{mySqlUser}'")
cursor = mysqlConnection.cursor()
insertStatement = config['mysql-app-config']['mysql.transactions_stage_unique.insert']

thisRunTransactionUUID = str(uuid.uuid4())
numRows = 0
numProcessed = 0
numErrors = 0
numInserted = 0
reader = csv.DictReader(args.input)
for row in reader:
        numRows += 1

        rowWriter = writer
        valid = False
        errorsList = []

        valid, errorsList, insertTransactionDict = rowProcessorClass.transactionDictionaryFromRow(row, thisRunTransactionUUID)

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