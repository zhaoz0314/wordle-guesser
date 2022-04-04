import random

# import words
with open("wordle-nyt-all.txt", "r") as txtfile:
    words= txtfile.read().split("\n")
if words[-1]== "":
    words.remove("")
with open("wordle-nyt-answers-alphabetical.txt", "r") as txtfile:
    wordsFewer= txtfile.read().split("\n")
if wordsFewer[-1]== "":
    wordsFewer.remove("")

# generate answer
# answer= words[random.randint(1,len(words))-1]
answer= wordsFewer[random.randint(1,len(wordsFewer))-1]
# print(answer) # for debugging

# guessing
guess= "" # initialize
cue= [0, 0, 0, 0, 0]
guessNum=0
while cue!= [2, 2, 2, 2, 2]: # start guessing
    guess= input("your guess: ") # make guesses
    if guess in words:
        for idx in range(5): # generate cues
            if guess[idx] in answer:
                if guess[idx]== answer[idx]:
                    cue[idx]= 2
                else:
                    cue[idx]= 1
            else:
                cue[idx]=0
        # print(cue) # return cues
        print("            "+str(cue[0])+str(cue[1])+str(cue[2])+str(cue[3])+str(cue[4]))
        guessNum= guessNum+ 1 # record number of guesses
    else:
        print("invalid guess")
print(str(guessNum)+ " guesses were made\n")
