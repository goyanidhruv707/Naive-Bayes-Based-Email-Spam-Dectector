import os
import re
import math
import training

def testModel():
    print("Processing \"model.txt\" file for Testing...")
    modelDictionary = readingModel()
    testingModel(modelDictionary)
    print("Testing Complete.\n")

#reading the model.txt and storing in dictionary
def readingModel():
    modelDict={}
    with open("Output/model.txt","r") as f:
        for line in f:
            line=line.replace("\n","")
            splitLine=line.split("  ")
            modelDict[splitLine[1]]=splitLine[2:]
    return modelDict

#reading the file and splitting
def readFile(pathTestData,fileName):
    with open(os.path.join(pathTestData, fileName), 'r',encoding="utf8",errors="ignore") as f:
        return re.split('[^a-zA-Z]',f.read().lower())

#testing the model by calculating scores
def testingModel(modelDict):
    
    probHam=math.log10(training.hamFileCount/(training.hamFileCount+training.spamFileCount))
    probSpam=math.log10(training.spamFileCount/(training.hamFileCount+training.spamFileCount))
    scoreHam=probHam
    scoreSpam=probSpam
    counter=1
    pathTestData="Input/Project2-Test/test"
    writeFile=open("Output/result.txt","w")
    for fileName in os.listdir(pathTestData):
        r=readFile(pathTestData,fileName)
        r=[i for i in r if i]
        for word in r:
            scoreHam+=0.0 if modelDict.get(word) is None else float(modelDict.get(word)[1])
            scoreSpam+=0.0 if modelDict.get(word) is None else float(modelDict.get(word)[3])
        if "ham" in fileName:
            actualLabel="ham"
        else:
            actualLabel="spam"
        if scoreHam>scoreSpam:
            expectedLabel="ham"
        else:
            expectedLabel="spam"
        if actualLabel==expectedLabel:
            result="right"
        else:
            result="wrong"
        writeFile.write(str(counter)+"  "+fileName+"  "+actualLabel+"  "+str(scoreHam)+"  "+str(scoreSpam)+ \
                        "  "+expectedLabel+"  "+result+"\n")
        counter+=1
        scoreHam=probHam
        scoreSpam=probSpam
    writeFile.close()