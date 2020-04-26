#to display the confusion matrix
def printConfusionMatrix(confusionMatrix):
    dash="-"*25
    print(dash)
    print("Generated Confusion Matrix:")    
    print(dash)
    print('{:>10s}{:^15s}'.format("","Predicted"))
    print('{:<10s}{:<10s}{:<10s}'.format("Actual","ham","spam"))
    print(dash)
    print('{:<10s}{:<10s}{:<10s}'.format("ham",str(confusionMatrix[0][0]),str(confusionMatrix[0][1])))
    print('{:<10s}{:<10s}{:<10s}'.format("spam",str(confusionMatrix[1][0]),str(confusionMatrix[1][1])))

#to display the metrics of the model
def printMetrics(accuracy,precisionHam,precisionSpam,recallHam,recallSpam,f1Ham,f1Spam):
    dash="-"*45
    print(dash)
    print("Metrics:")
    print(dash)
    print("accuracy={}".format(str(accuracy)))
    print()
    print('{:<10s}{:<15s}{:<10s}{:<10s}'.format("","precision","recall","f1-measure"))
    print(dash)
    print('{:<10s}{:<15s}{:<10s}{:<10s}'.format("ham",str(precisionHam),str(recallHam),str(f1Ham)))
    print('{:<10s}{:<15s}{:<10s}{:<10s}'.format("spam",str(precisionSpam),str(recallSpam),str(f1Spam)))

#to analyse the metrics on result.txt
def analysisMain():
    print("Analysing \"result.txt\"...")
    actualResult=[]
    predictedResult=[]
    actualHam=0
    predictedHam=0
    actualSpam=0
    predictedSpam=0
    confusionMatrix=[]
    with open("Output/result.txt","r") as f:
        for line in f:
            line=line.replace("\n","")
            splitLine=line.split("  ")
            if(splitLine[2]=="ham"):
                actualHam+=1
                if(splitLine[5]=="ham"):
                    predictedHam+=1
            else:
                actualSpam+=1
                if(splitLine[5]=="spam"):
                    predictedSpam+=1
            
            actualResult.append(splitLine[2])
            predictedResult.append(splitLine[5])
     
    f.close()
    confusionMatrix=[[predictedHam,(actualHam-predictedHam)],[(actualSpam-predictedSpam),predictedSpam]]
    printConfusionMatrix(confusionMatrix)
    
    accuracy=round((predictedHam+predictedSpam)/(actualHam+actualSpam),2)
    precisionHam=round(confusionMatrix[0][0]/(confusionMatrix[0][0]+confusionMatrix[1][0]),2)
    precisionSpam=round(confusionMatrix[1][1]/(confusionMatrix[1][1]+confusionMatrix[0][1]),2)
    recallHam=round(confusionMatrix[0][0]/(confusionMatrix[0][0]+confusionMatrix[0][1]),2)
    recallSpam=round(confusionMatrix[1][1]/(confusionMatrix[1][1]+confusionMatrix[1][0]),2)
    f1Ham=round((2*precisionHam*recallHam)/(precisionHam+recallHam),2)
    f1Spam=round((2*precisionSpam*recallSpam)/(precisionSpam+recallSpam),2)
    
    printMetrics(accuracy,precisionHam,precisionSpam,recallHam,recallSpam,f1Ham,f1Spam)