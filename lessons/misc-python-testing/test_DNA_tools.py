import DNA_tools

def test_simple():
    inputvalue = 'ATGC'
    outputvalue = DNA_tools.calculate_gc(inputvalue)
    expectedoutput = 0.50
    assert round(outputvalue, ndigits = 2) == expectedoutput

def test_long():
    inputvalue = 'AGCGTCGTCAGTCGT'
    outputvalue = DNA_tools.calculate_gc(inputvalue)
    expectedoutput = 0.60
    assert round(outputvalue, ndigits = 2) == expectedoutput
    
    
def test_mixedCases():
    inputvalue = 'ATaGtTCaAGcTCgATtGaATaGgTAaCt'
    outputvalue = DNA_tools.calculate_gc(inputvalue)
    expectedoutput = 0.34
    assert round(outputvalue, ndigits = 2) == expectedoutput

def test_empty():
    inputvalue = '' # if input is empty this mean that everything was fine before
    outputvalue = DNA_tools.calculate_gc(inputvalue)
    expectedvalue = 1
    assert outputvalue == expectedvalue
