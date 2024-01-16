import datetime
# application modules
import transaction_row_processor
import transactionsUtil

class VanguardTransactionRowProcessor(transaction_row_processor.TransactionRowProcessor):
    transactionDescriptionToTypeMap = {
        'Contribution' : transactionsUtil.EFTIN,
        'Buy' : transactionsUtil.BUY,
        'Conversion (outgoing)' : transactionsUtil.ROLLOVEROUT,
        'Conversion (incoming)' : transactionsUtil.ROLLOVERIN,
        'Capital gain (LT)' : transactionsUtil.LTCAPGAIN,
        'Reinvestment (LT gain)' : transactionsUtil.LTCAPGAIN,
        'Reinvestment' : transactionsUtil.DIVREINVEST,
        'Dividend' : transactionsUtil.DIVCASH
    }

    def validateETFIn(transactionDict):
        print("ETF validation...")

        validationErrors = []
        validTransaction = True

        if (transactionDict['transaction_type'] != transactionsUtil.EFTIN):
            validationErrors.append("Transaction type '" + transactionDict['transaction_type'] + "' must be " + transactionsUtil.EFTIN)
            validTransaction = False

        if (not float(transactionDict['source_shares']) == 0):
            validationErrors.append("Shares '" + transactionDict['source_shares'] + "' must be 0")
            validTransaction = False

        if (not float(transactionDict['source_price_per_share']) == 0):
            validationErrors.append("Price per share '" + transactionDict['source_price_per_share'] + "' must be 0")
            validTransaction = False
        
        if (float(transactionDict['source_transaction_amount']) <= 0):
            validationErrors.append("Transaction amount '" + transactionDict['source_transaction_amount'] + "' must be positive")
            validTransaction = False
    
        print("ETF validation complete...")
        return validTransaction, validationErrors
    
    def validateBuy(transactionDict):
        print("Buy validation...")
        
        validationErrors = []
        validTransaction = True

        if (transactionDict['transaction_type'] != transactionsUtil.BUY):
            validationErrors.append("Transaction type '" + transactionDict['transaction_type'] + "' must be " + transactionsUtil.BUY)
            validTransaction = False

        if (float(transactionDict['source_shares']) <= 0):
            validationErrors.append("Shares '" + transactionDict['source_shares'] + "' must be positive")
            validTransaction = False

        if (float(transactionDict['source_price_per_share']) <= 0):
            validationErrors.append("Price per share '" + transactionDict['source_price_per_share'] + "' must be positive")
            validTransaction = False
        
        if (float(transactionDict['source_transaction_amount']) >= 0):
            validationErrors.append("Transaction amount '" + transactionDict['source_transaction_amount'] + "' must be negative")
            validTransaction = False
    
        print("Buy validation complete...")
        return validTransaction, validationErrors
    
    def validateRolloverOut(transactionDict):
        print("Rollover out validation...")

        validationErrors = []
        validTransaction = True

        if (transactionDict['transaction_type'] != transactionsUtil.ROLLOVEROUT):
            validationErrors.append("Transaction type '" + transactionDict['transaction_type'] + "' must be " + transactionsUtil.ROLLOVEROUT)
            validTransaction = False

        if (float(transactionDict['source_shares']) >= 0):
            validationErrors.append("Shares '" + transactionDict['source_shares'] + "' must be negative")
            validTransaction = False

        if (not float(transactionDict['source_price_per_share']) == 0):
            validationErrors.append("Price per share '" + transactionDict['source_price_per_share'] + "' must be 0")
            validTransaction = False
        
        if (float(transactionDict['source_transaction_amount']) >= 0):
            validationErrors.append("Transaction amount '" + transactionDict['source_transaction_amount'] + "' must be negative")
            validTransaction = False
    
        print("Rollover out validation complete...")
        return validTransaction, validationErrors
    
    def validateRolloverIn(transactionDict):
        print("Rollover in validation...")
        
        validationErrors = []
        validTransaction = True

        if (transactionDict['transaction_type'] != transactionsUtil.ROLLOVERIN):
            validationErrors.append("Transaction type '" + transactionDict['transaction_type'] + "' must be " + transactionsUtil.ROLLOVERIN)
            validTransaction = False

        if (float(transactionDict['source_shares']) <= 0):
            validationErrors.append("Shares '" + transactionDict['source_shares'] + "' must be positive")
            validTransaction = False

        if (not float(transactionDict['source_price_per_share']) == 0):
            validationErrors.append("Price per share '" + transactionDict['source_price_per_share'] + "' must be 0")
            validTransaction = False
        
        if (float(transactionDict['source_transaction_amount']) <= 0):
            validationErrors.append("Transaction amount '" + transactionDict['source_transaction_amount'] + "' must be positive")
            validTransaction = False
    
        print("Rollover out validation complete and valid...")
        return validTransaction, validationErrors
    
    def validateDivCash(transactionDict):
        print("Dividend validation...")

        validationErrors = []
        validTransaction = True

        if (transactionDict['transaction_type'] != transactionsUtil.DIVCASH):
            validationErrors.append("Transaction type '" + transactionDict['transaction_type'] + "' must be " + transactionsUtil.DIVCASH)
            validTransaction = False

        if (not float(transactionDict['source_shares']) == 0):
            validationErrors.append("Shares '" + transactionDict['source_shares'] + "' must be 0")
            validTransaction = False

        if (not float(transactionDict['source_price_per_share']) == 1):
            validationErrors.append("Price per share '" + transactionDict['source_price_per_share'] + "' must be 0")
            validTransaction = False
        
        if (float(transactionDict['source_transaction_amount']) <= 0):
            validationErrors.append("Transaction amount '" + transactionDict['source_transaction_amount'] + "' must be positive")
            validTransaction = False
    
        print("ETF validation complete...")
        return validTransaction, validationErrors
    
    def validateDividendReinvestment(transactionDict):
        print("Dividend reinvestment validation...")
        
        validationErrors = []
        validTransaction = True

        if (transactionDict['transaction_type'] != transactionsUtil.DIVREINVEST):
            validationErrors.append("Transaction type '" + transactionDict['transaction_type'] + "' must be " + transactionsUtil.DIVREINVEST)
            validTransaction = False

        if (float(transactionDict['source_shares']) <= 0):
            validationErrors.append("Shares '" + transactionDict['source_shares'] + "' must be positive")
            validTransaction = False

        if (float(transactionDict['source_price_per_share']) <= 0):
            validationErrors.append("Price per share '" + transactionDict['source_price_per_share'] + "' must be positive")
            validTransaction = False
        
        if (float(transactionDict['source_transaction_amount']) >= 0):
            validationErrors.append("Transaction amount '" + transactionDict['source_transaction_amount'] + "' must be negative")
            validTransaction = False
    
        print("Buy validation complete...")
        return validTransaction, validationErrors
    
    def validateNotImplemented(transactionDict):
        validationErrors = []
        validationErrors.append("Validation for transaction type '" + transactionDict['transaction_type'] + "' not yet implemented")
        return False, validationErrors

    transactionValidationMap = {
        transactionsUtil.EFTIN : validateETFIn,
        transactionsUtil.BUY : validateBuy,
        transactionsUtil.ROLLOVEROUT : validateRolloverOut,
        transactionsUtil.ROLLOVERIN : validateRolloverIn,
        transactionsUtil.LTCAPGAIN : validateNotImplemented,
        transactionsUtil.DIVREINVEST : validateDividendReinvestment,
        transactionsUtil.DIVCASH : validateDivCash
    }

    def __init__(self, theConfig):
        self.config = theConfig

    def transactionDictionaryFromRow(self, theRow, theTransitionUUID):
        valid = True
        errorsList = []

        print(f"VanguardTransactionRowProcessor process row = '{theRow}'")

        transactionType = self.transactionDescriptionToTypeMap[theRow['Transaction Type']]
        if not transactionType:
            errorsList.append(f"Unknown Vanguard transaction type/source = '{transactionType}'")
            valid = False

        validTradeDate, tradeDate = transactionsUtil.getDateFromFormats(theRow['Trade Date'], {'%m/%d/%Y','%Y-%m-%d'})
        if (not validTradeDate):
            valid = False
            errorsList.append("Invalid Trade Date '" + tradeDate + "'")

        validCommissionFees = False
        for commissionFeesColumnName in {'Commissions and Fees', 'Commission Fees'}:
            if commissionFeesColumnName in theRow.keys():
                commissionsFees = theRow[commissionFeesColumnName]
                validCommissionFees = True

        if not validCommissionFees:
            errorsList.append("Unable to find valid Vanguard commissions and fees column")
            valid = False

        insertTransactionDict = {
            'brokerage_account_number' : theRow['Account Number'],
            'transaction_id' : theTransitionUUID,
            'transaction_date': tradeDate,
            'transaction_desc' : theRow['Transaction Description'],
            'transaction_type' : transactionType,
            'symbol' : theRow['Symbol'],
            'name' : theRow['Investment Name'],
            'source_shares' : theRow['Shares'],
            'source_price_per_share' : theRow['Share Price'],
            'source_fees' : commissionsFees,
            'source_commissions' : commissionsFees,
            'source_transaction_amount' : theRow['Net Amount'],
            'transaction_notes' : None
        }

        if (insertTransactionDict['brokerage_account_number'] == None
            or insertTransactionDict['transaction_id'] == None
            or insertTransactionDict['transaction_date'] == None
            or insertTransactionDict['transaction_desc'] == None
            or insertTransactionDict['transaction_type'] == None
            or insertTransactionDict['symbol'] == None
            or insertTransactionDict['name'] == None
            or insertTransactionDict['source_shares'] == None
            or insertTransactionDict['source_price_per_share'] == None
            or insertTransactionDict['source_transaction_amount'] == None
            or insertTransactionDict['source_fees'] == None
            or insertTransactionDict['source_commissions'] == None
            ):
            valid = False
            errorsList.append("Encountered unexpected null values in Vanguard row")

        validTransaction, transactionErrorsList = self.transactionValidationMap[transactionType](insertTransactionDict)
        if not validTransaction:
            errorsList.append(transactionErrorsList)
            valid = False

        return valid, errorsList, insertTransactionDict