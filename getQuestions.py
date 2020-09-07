def getQuestions(filename='questions.txt'):
    """
    Define a simple text file format to capture Question, Agrees, Disagrees, and Passes
    Parse it.
    Compute Participation (Agrees + Disagrees + Passes)
    Agreement(-1 to 1)
    Involvement (0 to 1)
    Normalized Participation (0 to 1)
    
    """
    S=open(filename).read()
    SampleQuestions_txt= """
    Initial     This is the initial question.  87 agree, 13 disagree, 19 pass. 87 13 19
    Second      The second question demonstrates that it is the last three numbers that encode agree, disagree, and pass. 40 20 10
    Third_Is_OK 40 40 10
    Bad         No values
    Good    This one is good again 10 10 10
    """

    from collections import OrderedDict
    questions=[]

    lines = [s for s in S.split('\n') if s] # if s: ignore blank lines
    for line in lines:
        line=line.strip()
        firstWord = line.split(' ')[0]
        remainder = ' '.join(line.split(' ')[1:]).strip()
        numwords = line.split(' ')[-3:] #last three words
        try:
            numbers = [int(nw) for nw in numwords]
            agrees, disagrees, passes = numbers
            participation =  agrees + disagrees + passes
            involvement   =  1 - (passes / participation)

            questions.append(OrderedDict(
                firstWord = firstWord,
                remainder = remainder,
                agrees = agrees,
                disagrees = disagrees,
                passes =  passes,
                participation = participation,
                involvement   = involvement,
                agreement = (agrees-disagrees)/(agrees + disagrees),
                label = firstWord + '\n' + ' '.join(numwords),
                numwords = str(numwords)
            ))
        except ValueError:
            print(f'WARNING: bad numwords {numwords} for line "{line}""')

    
    #normalize participation
    mostParticipation = max([q['participation'] for q in questions])
    for i in range(len(questions)):
        questions[i]['participationNormalized'] = questions[i]['participation'] / mostParticipation
    
    return questions



if __name__ == '__main__':    
    from pprint import pprint
    questions = getQuestions()
    for q in questions:
        pprint(q)
        print()        

    from pandas import DataFrame
    DF = DataFrame(questions)[['agrees', 'disagrees', 'passes', 'agreement','involvement', 'participationNormalized']]
