CONTRIBUTION = 'CONTRIBUTION'
MATCH = 'MATCH'
EXCHANGEIN = 'EXCHANGE-IN'
EXCHANGEOUT = 'EXCHANGE-OUT'
BUY = 'BUY'

def stringToFloatOrNone(theString):
    return float(theString) if theString else None

def anyToAnyOrNone(theString):
    return theString if theString else None