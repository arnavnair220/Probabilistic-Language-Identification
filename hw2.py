import sys
import math


def get_parameter_vectors():
    '''
    This function parses e.txt and s.txt to get the  26-dimensional multinomial
    parameter vector (characters probabilities of English and Spanish) as
    descibed in section 1.2 of the writeup

    Returns: tuple of vectors e and s
    '''
    #Implementing vectors e,s as lists (arrays) of length 26
    #with p[0] being the probability of 'A' and so on
    e=[0]*26
    s=[0]*26

    with open('e.txt',encoding='utf-8') as f:

        for line in f:
            #strip: removes the newline character
            #split: split the string on space character
            char,prob=line.strip().split(" ")
            #ord('E') gives the ASCII (integer) value of character 'E'
            #we then subtract it from 'A' to give array index
            #This way 'A' gets index 0 and 'Z' gets index 25.
            e[ord(char)-ord('A')]=float(prob)
    f.close()

    with open('s.txt',encoding='utf-8') as f:
        for line in f:
            char,prob=line.strip().split(" ")
            s[ord(char)-ord('A')]=float(prob)
    f.close()

    return (e,s)

def shred(filename):
    #Using a dictionary here. You may change this to any data structure of
    #your choice such as lists (X=[]) etc. for the assignment
    X=dict()

    for asciiVal in range(ord('A'), ord('Z')+1):
        X[chr(asciiVal)] = 0

    with open (filename,encoding='utf-8') as f:
        text = (f.read()).upper()
        for letter in range(0, len(text)):
            if text[letter] in X:
                X[text[letter]] = X[text[letter]] + 1

    return X



#Not needed
def BayesRule(X, e, s):
    CXTop = (math.factorial(sum(X.values())))
    CXBottom = 1
    for Xi in X.values():
        CXBottom = CXBottom*(math.factorial(Xi))
    CX = CXTop/CXBottom

    pEng = 0.6
    PIEng = 1
    for ind in range(0,26):
        PIEng = PIEng*(e[ind]**X[chr(ord('A')+ind)])
    pXYEng = CX*PIEng

    pSpan = 0.4
    PISpan = 1
    for ind in range(0,26):
        PISpan = PISpan*(s[ind]**X[chr(ord('A')+ind)])
    pXYSpan = CX*PISpan

    pYXEng = (pXYEng * pEng)/((pXYEng * pEng)+(pXYSpan*pSpan)) 
    pYXSpan = (pXYSpan * pSpan)/((pXYEng * pEng)+(pXYSpan*pSpan)) 

    twoNumsOutput = [pYXEng,pYXSpan]

    return twoNumsOutput


def Fy(X, e, s):

    pEng = 0.6
    engSum = 0
    for ind in range(0, 26):
        engSum = engSum + (X[chr(ord('A')+ind)] * math.log(e[ind]))
    FyEng = math.log(pEng) + engSum

    pSpan = 0.4
    spanSum = 0
    for ind in range(0, 26):
        spanSum = spanSum + (X[chr(ord('A')+ind)] * math.log(s[ind]))
    FySpan = math.log(pSpan) + spanSum

    twoNumsOutput = [FyEng,FySpan]

    return twoNumsOutput

def PLang(FyLangs):
    P = None

    if FyLangs[1] - FyLangs[0] >= 100:
        P = 0
    elif FyLangs[1] - FyLangs[0] <= -100:
        P = 1
    else:
        P = 1/(1 + math.e**(FyLangs[1]-FyLangs[0]))

    return P

def main():
    e,s = get_parameter_vectors()

    Q1 = shred(input("Enter file name (must be in same folder as .py file): "))
    FyList = Fy(Q1, e, s)
    print("English Probability: ")
    print(round(PLang(FyList), 4))

if __name__=="__main__":
    main()

