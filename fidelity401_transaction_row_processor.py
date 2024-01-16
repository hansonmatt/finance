import datetime
# application modules
import transaction_row_processor
import transactionsUtil

class Fidelity401KTransactionRowProcessor(transaction_row_processor.TransactionRowProcessor):
    transactionDescriptionToTypeMap = {
        'Contributions' : transactionsUtil.CONTRIBUTION,
        'Balance Forward' : transactionsUtil.ROLLOVERIN,
        'RECORDKEEPING FEE' : transactionsUtil.FEE
    }

    def __init__(self, theConfig):
        self.config = theConfig
        self.accountNumber = self.config['fidelity-apple-401k-account-config']['fidelity-401k.account']

    def transactionDictionaryFromRow(self, theRow, theTransitionUUID):
        valid = True
        errorsList = []

        print(f"Fidelity401KTransactionRowProcessor process row = '{theRow}'")
        effectiveDate = datetime.datetime.strptime(theRow['Date'], "%m/%d/%y").strftime("%Y-%m-%d")
        shares = transactionsUtil.stringToFloatOrNone(theRow['Shares/Unit'])
        transactionAmount = transactionsUtil.stringToFloatOrNone(theRow['Amount ($)'])
        pricePerShare = transactionAmount / shares

        transactionType = self.transactionDescriptionToTypeMap[theRow['Transaction Type']]
        if not transactionType:
            errorsList.append(f"Unknown Fidelity 401K transaction type/source = '{transactionType}'")
            valid = False

        #empowerTransactionDescription = theRow['TRANSACTION DESCRIPTION']

        # after-tax roth conversion: each after-tax contribution has 3 transactions
        # 1 - after-tax contribution with 'payroll contribution' transaction description 
        # 2 - after-tax contribution with 'account withdrawal' transaction description 
        # 3 - in-place roth conversion with 'additional deposit' transaction description
        # use the source column to identify the withdrawal
        #if (theRow['SOURCE'] == 'After-tax Contribution'):
        #    if (empowerTransactionDescription == 'Account Withdrawal'):
        #        transactionType = transactionsUtil.EXCHANGEOUT

        insertTransactionDict = {
            'brokerage_account_number' : self.accountNumber,
            'transaction_id' : theTransitionUUID,
            'transaction_date': effectiveDate,
            'transaction_desc' : theRow['Transaction Type'],
            'transaction_type' : transactionType,
            'symbol' : theRow['Investment'],
            'name' : theRow['Investment'],
            'source_shares' : shares,
            'source_price_per_share' : pricePerShare,
            'source_fees' : None,
            'source_commissions' : None,
            'source_transaction_amount' : transactionAmount,
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
            or insertTransactionDict['source_transaction_amount'] == None
            #or insertTransactionDict['transaction_notes'] == None
            ):
            valid = False
            errorsList.append("Encountered unexpected null values in Empower row")

        # exchange out withdrawal for roth conversion will have negative shares and amount
        #if (insertTransactionDict['transaction_type'] == transactionsUtil.EXCHANGEOUT):
        #    if (not (shares < 0 and transactionAmount < 0)):
        #        valid = False
        #        errorsList.append('Expected negative shares and transaction amount for EXCHANGE-OUT')
        # all other transactions will have positive shares and amount
        #elif (not (shares > 0 and transactionAmount > 0)):
        #    valid = False
        #    errorsList.append(f"Expected positive shares and transaction amount for {insertTransactionDict['transaction_type']}")

        return valid, errorsList, insertTransactionDict