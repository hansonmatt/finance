def validateBuy(transactionDict):
    validationErrors = []
    if (not transactionDict['brokerage_account_number']):
       validationErrors.append("Brokerage account number + '" + transactionDict['brokerage_account_number'] + "' is null")
     
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
    if (not transactionDict['brokerage_account_number']):
       validationErrors.append("Brokerage account number + '" + transactionDict['brokerage_account_number'] + "' is null")
     
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
    if (not transactionDict['brokerage_account_number']):
       validationErrors.append("Brokerage account number + '" + transactionDict['brokerage_account_number'] + "' is null")
     
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
    if (not transactionDict['brokerage_account_number']):
       validationErrors.append("Brokerage account number + '" + transactionDict['brokerage_account_number'] + "' is null")
     
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
    if (not transactionDict['brokerage_account_number']):
       validationErrors.append("Brokerage account number + '" + transactionDict['brokerage_account_number'] + "' is null")
     
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
    if (not transactionDict['brokerage_account_number']):
       validationErrors.append("Brokerage account number + '" + transactionDict['brokerage_account_number'] + "' is null")
     
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
    if (not transactionDict['brokerage_account_number']):
       validationErrors.append("Brokerage account number + '" + transactionDict['brokerage_account_number'] + "' is null")
     
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
        validationErrors.append("Price/share '" + str(transactionDict['source_price_per_share']) + "' must be empty")

    if (transactionDict['source_transaction_amount']):
        validationErrors.append("Transaction amount '" + str(transactionDict['source_transaction_amount']) + "' must be empty")

    if (len(validationErrors) > 0):
        return False, validationErrors

    return True, validationErrors

def validateForeignTax(transactionDict):
    validationErrors = []
    if (not transactionDict['brokerage_account_number']):
       validationErrors.append("Brokerage account number + '" + transactionDict['brokerage_account_number'] + "' is null")
     
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
    if (not transactionDict['brokerage_account_number']):
       validationErrors.append("Brokerage account number + '" + transactionDict['brokerage_account_number'] + "' is null")
     
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
    if (not transactionDict['brokerage_account_number']):
       validationErrors.append("Brokerage account number + '" + transactionDict['brokerage_account_number'] + "' is null")
     
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