import datetime

CONTRIBUTION = 'CONTRIBUTION'
MATCH = 'MATCH'
EXCHANGEIN = 'EXCHANGE-IN'
EXCHANGEOUT = 'EXCHANGE-OUT'
BUY = 'BUY'
EFTIN = 'EFT-IN'
ROLLOVERIN = 'ROLLOVER-IN'
ROLLOVEROUT = 'ROLLOVER-OUT'
LTCAPGAIN = 'LT-CAP-GAIN'
DIVCASH = 'DIV-CASH'
DIVREINVEST = 'DIV-REINVEST'
FEE = 'FEE'

def stringToFloatOrNone(theString):
    return float(theString) if theString else None

def anyToAnyOrNone(theString):
    return theString if theString else None

def getDateFromFormats(theDate, theFormatList):
    for theFormat in theFormatList:
        try:
            dateFromString = datetime.datetime.strptime(theDate, theFormat)
            return True, dateFromString.strftime('%Y-%m-%d')
        except ValueError:
            print("Exception converting date '" + theDate + "' to format '" + theFormat + "'")

    print("Unable to convert date '" + theDate + "' to any of formats '" + theFormatList + "'")
    return False, None