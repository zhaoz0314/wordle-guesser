import time
import math
# import numpy as np

# startTime= time.time()

# import words
with open("wordle-nyt-all.txt", "r") as txtfile:
    words= txtfile.read().split("\n")
if words[-1]== "":
    words.remove("")
with open("wordle-nyt-answers-alphabetical.txt", "r") as txtfile:
    wordsFewer= txtfile.read().split("\n")
if wordsFewer[-1]== "":
    wordsFewer.remove("")

# list out all possible cues
cues=[[None for idx2 in range(5)] for idx1 in range(3**5)]
for idx in range(3**5):
    cues[idx][4]= idx//(3**4)
    cues[idx][3]= (idx-cues[idx][4]*(3**4))//(3**3)
    cues[idx][2]= (idx-cues[idx][4]*(3**4)-cues[idx][3]*(3**3))//(3**2)
    cues[idx][1]= (idx-cues[idx][4]*(3**4)-cues[idx][3]*(3**3)-cues[idx][2]*(3**2))//(3**1)
    cues[idx][0]= (idx-cues[idx][4]*(3**4)-cues[idx][3]*(3**3)-cues[idx][2]*(3**2)-cues[idx][1]*3)

# index every cue
def cueIndexing(fCue):
    return(fCue[0]+fCue[1]*(3**1)+fCue[2]*(3**2)+fCue[3]*(3**3)+fCue[4]*(3**4))
    
# find the cue for a guess
def generateCue(fAnswer, fGuess):
    fCue= [0, 0, 0, 0, 0]
    for idx in range(5): # generate cues
        if fGuess[idx] in fAnswer:
            if fGuess[idx]== fAnswer[idx]:
                fCue[idx]= 2
            else:
                fCue[idx]= 1
        else:
            fCue[idx]=0
    return(fCue)

# find the average resulting entropy of a word
# for a minimax algorithm, simply change this to taking the max
def averageEntropy(fRemaining,fGuess):
    fTotalLen= len(fRemaining)
    fExpEntropies= [0 for idx in range(3**5)]
    for idx in fRemaining:
        fCueIndex= cueIndexing(generateCue(idx, fGuess))
        fExpEntropies[fCueIndex]= fExpEntropies[fCueIndex]+1
    for idx in range(3**5):
        if fExpEntropies[idx]!= 0:
            fExpEntropies[idx]= fExpEntropies[idx]/fTotalLen*math.log(fExpEntropies[idx]) # fWeightedEntropies pS
    return(sum(fExpEntropies))

# find the guess that will narrow down the answer the most
# for ordinary algorithm, use min average S
# for minimax algorithm, use min max S
def minEntropy(fChoices, fRemaining):
    fOutput= ""
    fEntropy= math.log(len(fRemaining))
    for idx in fChoices:
        fTempEntropy= averageEntropy(fRemaining, idx)
        if fTempEntropy<= fEntropy:
            fOutput= idx
            fEntropy= fTempEntropy
    return([fOutput, fEntropy])

# test
# print(minEntropy(wordsFewer,wordsFewer)) # ['raise', 3.6700406885840637] # 3.901350498199463
# print(minEntropy(words,words)) # ['tares', 5.173857809125834] # 120.65073323249817
# print(minEntropy(words,wordsFewer)) # ['soare', 3.665258120124318] # 21.697190761566162

# find the new remaining words given the last guess and cue
def consistentWords(fRemaining,fGuess,fCue):
    fNewWords= [None for idx in range(len(fRemaining))]
    fCount=0
    for idx in range(len(fRemaining)):
        if generateCue(fRemaining[idx], fGuess)== fCue:
            fNewWords[fCount]= fRemaining[idx]
            fCount= fCount+1
    return(fNewWords[0:fCount])

def string2Cue(string):
    return[int(string[0]),int(string[1]),int(string[2]),int(string[3]),int(string[4])]

# using all words possible
guess= "soare" # initialize
print(['soare', 3.665258120124318])
cue= string2Cue(input("the cue given the guess: "))
remaining= consistentWords(wordsFewer, guess, cue)
# guess= None
# cue= [None for idx in range(5)]
# remaining= wordsFewer
while cue!= [2, 2, 2, 2, 2]:
    if len(remaining)== 1:
        guess= [remaining[0], 0]
    else:
        guess= minEntropy(words,remaining)
    print(guess)
    cue= string2Cue(input("the cue given the guess: "))
    remaining = consistentWords(remaining, guess[0], cue)

# # using only remaining words
# guess= "raise" # initialize
# print(['raise', 3.6700406885840637])
# cue= string2Cue(input("the cue given the guess: "))
# remaining= consistentWords(wordsFewer, guess, cue)
# # guess= None
# # cue= [None for idx in range(5)]
# # remaining= wordsFewer
# while cue!= [2, 2, 2, 2, 2]:
#     if len(remaining)== 1:
#         guess= [remaining[0], 0]
#     else:
#         guess= minEntropy(remaining,remaining)
#     print(guess)
#     cue= string2Cue(input("the cue given the guess: "))
#     remaining = consistentWords(remaining, guess[0], cue)
#     print(remaining)

# endTime= time.time()
# print(endTime- startTime)