from landscape4 import makeUnits, initLandscape, sortRect, showLabels
from vpython import label
from getQuestions import getQuestions

from math import sqrt, ceil
from getQuestions import getQuestions

questions = getQuestions()
numQs = len(questions)
Rows=Cols= ceil(sqrt(numQs))
showLabels=False 

units = makeUnits(Rows,Cols, showLabels)
initLandscape(  units, Rows, Cols)


ukeys = list(units.keys())
for i, k in enumerate(ukeys):
    u = units[k]
    if i < numQs:
        q=questions[i]    
        u.change(height=   q['agreement'],
                  size =    q['participationNormalized'],
                  #boxSize = 1,
                  text =    q['label']
        )
        u.change(boxSize=q['involvement']) #for some reaso this needs to be a separate call
        questions[i]['unit'] = u
    else:
        u.change(height=0, size=1, boxSize=1)
        u.change(text='')
        ###PROBLEM IS HERE: CHANGING THE WRONG GUYS


from pprint import pprint
def getQ(searchStr):
    q = [q for q in questions if q['label'].startswith(searchStr)][0]
    return q, q['unit'].__dict__
    
q,u = getQ('Unanimity')

sortRect(units, Rows, Cols)
