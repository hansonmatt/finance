import datetime
# application modules
import transaction_row_processor
import fidelityValidation
import transactionsUtil

class FidelityTransactionRowProcessor(transaction_row_processor.TransactionRowProcessor):
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

    def __init__(self, theConfig):
        self.config = theConfig

    # get the transaction type mapping dictionary
    def getTransactionsTypesDictionary(self):
        raise NotImplementedError('TransactionRowProcessor does not implement getTransactionsTypesDictionary')
    
    # get the Fidelity account number
    def getFidelityAccountNumber(self):
        raise NotImplementedError('TransactionRowProcessor does not implement getFidelityAccountNumber')

    # get the transaction date column name
    def getTransactionDateColumnName(self):
        return "Run Date"
    # get the transaction date column name
    def getTransactionDescriptionColumnName(self):
        return "Action"
    # get the transaction symbol column name
    def getSymbolColumnName(self):
        return "Symbol"
    # get the transaction symbol column name
    def getSecurityNameColumnName(self):
        return "Security Description"
    # get the source shares column name
    def getSourceSharesColumnName(self):
        return "Quantity"
    # get the price column name
    def getPricePerShareColumnName(self):
        return "Price"
    # get the source fees column name
    def getSourceFeesColumnName(self):
        return "Fees"
    # get the source commission column name
    def getSourceCommissionColumnName(self):
        return "Commission"
    # get the source commission column name
    def getTransactionAmountColumnName(self):
        return "Amount"

    # return a transaction dictionary from input row
    def transactionDictionaryFromRow(self, theRow, theTransitionUUID):

        valid = False
        errorsList = []
        transactionTypeMatch = 0
        transactionTypeMap = self.getTransactionsTypesDictionary()

        for key in transactionTypeMap:
            if key in theRow[self.getTransactionDescriptionColumnName()]:
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

        #  Fidelity run date sample date = ' 03/27/2023'
        runDate = datetime.datetime.strptime(theRow[self.getTransactionDateColumnName()], " %m/%d/%Y").strftime("%Y-%m-%d")
        # Fidelity output transaction date format = '2023-03-27'
        sourceShares = transactionsUtil.stringToFloatOrNone(theRow[self.getSourceSharesColumnName()])
        sourcePricePerShare = transactionsUtil.stringToFloatOrNone(theRow[self.getPricePerShareColumnName()])
        sourceFees = transactionsUtil.stringToFloatOrNone(theRow[self.getSourceFeesColumnName()])
        sourceCommissions = transactionsUtil.stringToFloatOrNone(theRow[self.getSourceCommissionColumnName()])
        sourceTransactionAmt = transactionsUtil.stringToFloatOrNone(theRow[self.getTransactionAmountColumnName()])

        insertTransactionDict = {
            'brokerage_account_number' : self.getFidelityAccountNumber(),
            'transaction_id' : theTransitionUUID,
            'transaction_date': runDate,
            'transaction_desc' : theRow[self.getTransactionDescriptionColumnName()].strip(),
            'transaction_type' : transactionType,
            'symbol' : theRow[self.getSymbolColumnName()].strip(),
            'name' : theRow[self.getSecurityNameColumnName()].strip(),
            'source_shares' : sourceShares,
            'source_price_per_share' : sourcePricePerShare,
            'source_fees' : sourceFees,
            'source_commissions' : sourceCommissions,
            'source_transaction_amount' : sourceTransactionAmt,
            'transaction_notes' : None
        }

        if (valid):
            valid, errorsList = self.transactionValidationMap[transactionType](insertTransactionDict)

        #print(f"TransactionRowProcessor.transactionDictionaryFromRow: transaction dictionary = {insertTransactionDict}")
        return valid, errorsList, insertTransactionDict

class BrokerageTransactionRowProcessor(FidelityTransactionRowProcessor):
    brokeragetransactionTypeMap = {
    "YOU BOUGHT" : "BUY",
    "YOU SOLD" : "SELL",
    "DIVIDEND RECEIVED" : "DIV-CASH",
    "REINVESTMENT" : "DIV-REINVEST",
    "TRANSFERRED FROM" : "EFT-IN",
    "REDEMPTION PAYOUT UNITED STATES TREAS BILLS" : "SELL"
    }

    def __init__(self, theConfig):
        super().__init__(theConfig)
        print("BrokerageTransactionRowProcessor constructor")

    # get the transaction type mapping dictionary
    def getTransactionsTypesDictionary(self):
        return self.brokeragetransactionTypeMap
    
    # get the Fidelity account number
    def getFidelityAccountNumber(self):
        return self.config['fidelity-account-config']['brokerage.account']

class SMATransactionRowProcessor(FidelityTransactionRowProcessor):
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

    def __init__(self, theConfig):
        super().__init__(theConfig)

    # get the transaction type mapping dictionary
    def getTransactionsTypesDictionary(self):
        return self.smatransactionTypeMap
    
    # get the Fidelity account number
    def getFidelityAccountNumber(self):
        return self.config['fidelity-account-config']['sma.account']
    
    # get the price column name
    def getPricePerShareColumnName(self):
        return "Price ($)"
    # get the source fees column name
    def getSourceFeesColumnName(self):
        return "Fees ($)"
    # get the source commission column name
    def getSourceCommissionColumnName(self):
        return "Commission ($)"
    # get the source commission column name
    def getTransactionAmountColumnName(self):
        return "Amount ($)"