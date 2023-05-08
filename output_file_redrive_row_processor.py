import json
import uuid
import transaction_row_processor
import transactionsUtil

class RedriveTransactionRowProcessor(transaction_row_processor.TransactionRowProcessor):
    def __init__(self, theConfig):
        self.config = theConfig
        self.transactionUUID = str(uuid.uuid4())

    # return a transaction dictionary from input row
    def transactionDictionaryFromRow(self, theRow, theTransitionUUID):
        fieldnames = json.loads(self.config['application-config']['output.file.header.columnnames'])
        insertTransactionDict = {}
        for field in fieldnames:
            fieldValue = transactionsUtil.anyToAnyOrNone(theRow[field])
            insertTransactionDict[field] = fieldValue
        
        insertTransactionDict['transaction_id'] = 'REDRIVE-' + self.transactionUUID

        print(f"RedriveTransactionRowProcessor.transactionDictionaryFromRow, insert row = {insertTransactionDict}")
        return True, [], insertTransactionDict