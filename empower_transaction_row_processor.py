import datetime
# application modules
import transaction_row_processor
import transactionsUtil

class EmpowerTransactionRowProcessor(transaction_row_processor.TransactionRowProcessor):
    transactionDescriptionToTypeMap = {
        'After-tax Contribution' : transactionsUtil.CONTRIBUTION,
        'Apple Match' : transactionsUtil.MATCH,
        'Base-pay Traditional 401(k) Contribution' : transactionsUtil.CONTRIBUTION,
        'Catch-up Traditional 401(k) Contribution' : transactionsUtil.CONTRIBUTION,
        'In-plan Roth After-tax Conversion' : transactionsUtil.EXCHANGEIN
    }

    def __init__(self, theConfig):
        self.config = theConfig
        self.accountNumber = self.config['empower-account-config']['empower.account']

    def transactionDictionaryFromRow(self, theRow, theTransitionUUID):
        valid = True
        errorsList = []

        print(f"EmpowerTransactionRowProcessor process row = '{theRow}'")
        effectiveDate = datetime.datetime.strptime(theRow['EFFECTIVE DATE'], "%m/%d/%y").strftime("%Y-%m-%d")
        shares = transactionsUtil.stringToFloatOrNone(theRow['UNITS/ SHARES'])
        transactionAmount = transactionsUtil.stringToFloatOrNone(theRow['AMOUNT'])
        pricePerShare = transactionAmount / shares

        transactionType = self.transactionDescriptionToTypeMap[theRow['SOURCE']]
        if not transactionType:
            errorsList.append(f"Unknown Empower transaction type/source = '{transactionType}'")
            valid = False

        empowerTransactionDescription = theRow['TRANSACTION DESCRIPTION']

        # after-tax roth conversion: each after-tax contribution has 3 transactions
        # 1 - after-tax contribution with 'payroll contribution' transaction description 
        # 2 - after-tax contribution with 'account withdrawal' transaction description 
        # 3 - in-place roth conversion with 'additional deposit' transaction description
        # use the source column to identify the withdrawal
        if (theRow['SOURCE'] == 'After-tax Contribution'):
            if (empowerTransactionDescription == 'Account Withdrawal'):
                transactionType = transactionsUtil.EXCHANGEOUT

        insertTransactionDict = {
            'brokerage_account_number' : self.accountNumber,
            'transaction_id' : theTransitionUUID,
            'transaction_date': effectiveDate,
            'transaction_desc' : theRow['SOURCE'],
            'transaction_type' : transactionType,
            'symbol' : theRow['OPTION'],
            'name' : theRow['OPTION'],
            'source_shares' : shares,
            'source_price_per_share' : pricePerShare,
            'source_fees' : None,
            'source_commissions' : None,
            'source_transaction_amount' : transactionAmount,
            'transaction_notes' : empowerTransactionDescription
        }
        #print(f"EmpowerTransactionRowProcessor process insert = '{insertTransactionDict}'")

        if (insertTransactionDict['brokerage_account_number'] == None
            or insertTransactionDict['transaction_id'] == None
            or insertTransactionDict['transaction_date'] == None
            or insertTransactionDict['transaction_desc'] == None
            or insertTransactionDict['transaction_type'] == None
            or insertTransactionDict['symbol'] == None
            or insertTransactionDict['name'] == None
            or insertTransactionDict['source_shares'] == None
            or insertTransactionDict['source_transaction_amount'] == None
            or insertTransactionDict['transaction_notes'] == None
            ):
            valid = False
            errorsList.append("Encountered unexpected null values in Empower row")

        # exchange out withdrawal for roth conversion will have negative shares and amount
        if (insertTransactionDict['transaction_type'] == transactionsUtil.EXCHANGEOUT):
            if (not (shares < 0 and transactionAmount < 0)):
                valid = False
                errorsList.append('Expected negative shares and transaction amount for EXCHANGE-OUT')
        # all other transactions will have positive shares and amount
        elif (not (shares > 0 and transactionAmount > 0)):
            valid = False
            errorsList.append(f"Expected positive shares and transaction amount for {insertTransactionDict['transaction_type']}")

        return valid, errorsList, insertTransactionDict