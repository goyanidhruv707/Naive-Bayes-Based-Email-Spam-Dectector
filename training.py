import math
import os
import re

setOfWords = []
dictionaryOfWords = {}
dictionaryModel = {}

wordDictionaryHam = {}
wordDictionarySpam = {}

hamCount = 0
spamCount = 0
hamFileCount = 0
spamFileCount = 0

trainingSetFilePath = 'Input/Project2-Train/train'
trainingFiles = os.listdir(trainingSetFilePath)

#########################Training The Model#############################
def trainModel():
    readTrainingFiles(trainingFiles)
    countHamSpam()
    calculateProbabilityAndWriteOutput()
    print("Training Completed.\n")
    

def readTrainingFiles(trainingFiles):
    global setOfWords
    global dictionaryOfWords
    global wordDictionaryHam
    global wordDictionarySpam
    global hamFileCount
    global spamFileCount
    
    print("Prosessing Training Files...")
    
    for f in trainingFiles:
        if f[6] == "h":
            hamFileCount += 1
        elif f[6] == "s":
            spamFileCount += 1
        
        file = open(trainingSetFilePath + "/" + f)
        lines = file.readlines()

        for line in lines:
            string = re.split('[^a-zA-Z]',line)
            temp = list(filter(None,string))
            words = re.split(" ", " ".join(temp).lower())
            
            for word in words:
                if word == "" or word == " ":
                    continue
                if word in dictionaryOfWords:
                    dictionaryOfWords[word] += 1
                elif word not in dictionaryOfWords:
                    dictionaryOfWords[word] = 1
                    setOfWords.append(word)
                
                if f[6] == "h":
                    if word in wordDictionaryHam:
                        wordDictionaryHam[word] += 1
                    else:
                        wordDictionaryHam[word] = 1
                    
                if f[6] == "s":
                    if word in wordDictionarySpam:
                        wordDictionarySpam[word] += 1
                    else:
                        wordDictionarySpam[word] = 1
    print("Finished Prosessing Training Files.\n")


def countHamSpam():
    global hamCount
    global spamCount
    
    for wordHam in wordDictionaryHam:
        hamCount += wordDictionaryHam[wordHam]
        
    for wordSpam in wordDictionarySpam:
        spamCount += wordDictionarySpam[wordSpam]
    
    
    print("Total Words:", len(setOfWords))
    print("Ham Words:", len(wordDictionaryHam))
    print("Spam Words:", len(wordDictionarySpam),"\n")


def calculateProbabilityAndWriteOutput():
    global setOfWords
    lineCount = 1
    setOfWords = sorted(setOfWords)
    outputModelFile = open("Output/model.txt","w")
    #Smoothening
    for word in setOfWords:
        if wordDictionaryHam.get(word) == None:
            tempHamCount = 0
            smoothHamProbability = math.log10((0.5) / (hamCount + (0.5)*len(setOfWords)))
        else:
            tempHamCount = wordDictionaryHam.get(word)
            smoothHamProbability = math.log10((tempHamCount + 0.5) / (hamCount + (0.5)*len(setOfWords)))
        
        
        if wordDictionarySpam.get(word) == None:
            tempSpamCount = 0
            smoothSpamProbability = math.log10((0.5) / (spamCount + (0.5)*len(setOfWords)))
        else:
            tempSpamCount = wordDictionarySpam.get(word)
            smoothSpamProbability = math.log10((tempSpamCount + 0.5) / (spamCount + (0.5)*len(setOfWords)))
        
        dictionaryModel[word] = [tempHamCount, smoothHamProbability, tempSpamCount, smoothSpamProbability]
        outputString = str(lineCount), str(word), str(tempHamCount), str(smoothHamProbability), str(tempSpamCount), str(smoothSpamProbability)
        finalOutputString = "  ".join(list(outputString))
        outputModelFile.write(finalOutputString+"\n")
        lineCount += 1
    outputModelFile.close()