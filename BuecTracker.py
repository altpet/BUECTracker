
def makePoints():#Make the generic points table
    points = [150,140,135,130,127,124,121,118]
    for i in range(116,48,-2):
        points.append(i)

    for i in range(49,29,-1):
        points.append(i)
        
    points.append(29)    
    points.append(29)  

    for i in range(28,20,-1):
        points.append(i)
        points.append(i)
        points.append(i)
           
           
           
    for i in range(20,6,-1):
        points.append(i)
        points.append(i)
        points.append(i)
        points.append(i)
        
        
    for i in range(6,0,-1):
        points.append(i)
        points.append(i)
        points.append(i)
        points.append(i)
        points.append(i)
        points.append(i)
        points.append(i)
        points.append(i)
       
    return points
    
def makeReducedPoints():#Make the reduced points table


    a = []
    for i in range(97,129,1):
        a.append(i)
    b = []
    for i in range(49,65,1):
        b.append(i)
        
    c = []
    for i in range(25,33,1):
        c.append(i)
        
    d = [1,13,7,14,4,15,8,16]

    reducedPoints = []

    for i in range(8):
        reducedPoints.append(d.pop(0))
        reducedPoints.append(a.pop(0))
        reducedPoints.append(b.pop(0))
        reducedPoints.append(a.pop(0))
        reducedPoints.append(c.pop(0))
        reducedPoints.append(a.pop(0))
        reducedPoints.append(b.pop(0))
        reducedPoints.append(a.pop(0))
        

    reducedPoints.append(2)
    reducedPoints.append(65)



    a = []
    for i in range(129,141,1):
        a.append(i)
        
    d = [33,17,66,67,34,68,9,35,69,70,18,71]    
        
        
    for i in range(4):
        reducedPoints.append(a.pop(0))
        reducedPoints.append(d.pop(0))
        reducedPoints.append(a.pop(0))
        reducedPoints.append(a.pop(0))
        reducedPoints.append(d.pop(0))
        reducedPoints.append(d.pop(0))
        
        
    reducedPoints.append(141)
    reducedPoints.append(142)


    a = []
    for i in range(143,169,1):
        a.append(i)

    b = []
    for i in range(72,85,1):
        b.append(i)

    d = [36,5,37,19,38,10,39,20,40,3,41,21,42]

    for i in range(13):
        reducedPoints.append(d.pop(0))
        reducedPoints.append(b.pop(0))
        reducedPoints.append(a.pop(0))
        reducedPoints.append(a.pop(0))
        


    a = []
    for i in range(169,193,1):
        a.append(i)


    b = []
    for i in range(85,97,1):
        b.append(i)
        
    c = []
    for i in range(43,49,1):
        c.append(i)
        
    d = [11,22,6,23,12,24]


    for i in range(6):
        reducedPoints.append(d.pop(0))
        reducedPoints.append(c.pop(0))
        reducedPoints.append(b.pop(0))
        reducedPoints.append(b.pop(0))
        reducedPoints.append(a.pop(0))
        reducedPoints.append(a.pop(0))
        reducedPoints.append(a.pop(0))
        reducedPoints.append(a.pop(0))
    
    return reducedPoints

points = makePoints()
reducedPoints = makeReducedPoints()


import pandas as pd
import numpy as np
def numberOfTeams(df):
    df2 = df.copy(deep=True)
    df2.dropna(axis = 0, how = "any",inplace=True)
    numberOfTeams = (len(df2.index))
    return numberOfTeams
  
def elligibleTeams(numberOfTeams):
    compare = ((numberOfTeams-64)*(2/3))+64
    elligibleTeams = min(compare,numberOfTeams,256)
    return elligibleTeams
  
def pointsMultiplier(numberOfTeams): #needs implementations for diff types of games
    pointsMultiplier = 1
    singlePlayerChamp = False
    if singlePlayerChamp == True:
        pointsMultiplier *= 1/2
    
    singleAndTeamsEvent = False
    if singleAndTeamsEvent == True:
        single = False
        team = False
        if single == True:
            pointsMultiplier *= 4/5
        elif teams == True:
            pointsMultiplier *=2/3
    
    
    elif numberOfTeams<32:
        pointsMultiplier *= 2/3
        
    return pointsMultiplier
    
def loadDF(path):
    return pd.read_csv(path, index_col=0, dtype = {"Team 1" : str,"University": str})
    

def bucketTeams(df):
    unis = df["University"]
    buckets = []
    tempBucket = []
    
    for i in unis:
        if i != i:
            buckets.append(tempBucket)
            tempBucket = []
        else:
            tempBucket.append(i)
            
    buckets.append(tempBucket)
    return buckets

def sortAndReducePointsTable(numberOfTeams,reducedDict,pointsMultiplier):
         
    if numberOfTeams<192:
        for i in range(numberOfTeams,192,1):
            reducedDict.pop(i+1)
    
    sortedPoints = []
    for i in reducedDict:
        sortedPoints.append(reducedDict[i])

    sortedPoints.sort(reverse=True)
    sortedPoints = sortedPoints * pointsMultiplier
    return sortedPoints

def pointsByCurrentRankings(numberOfTeams,buckets,sortedPoints):

    ellTeams = elligibleTeams(numberOfTeams)
    print(ellTeams)
    pointsSum = {}
    counter = 0
    for bucket in buckets:
        if counter < ellTeams:
            temp = 0
            for team in bucket:
                counter +=1
                if counter <= 192:
                    temp += sortedPoints.pop(0)
                
            temp = temp/len(bucket) #average
            for team in bucket:
                pointsSum[team] = pointsSum.setdefault(team,0) + temp
        print(counter)    
    return pointsSum


def gamePointsByCurrentRankings(sourceDir, outDir):
    df = loadDF(sourceDir)
    numOfTeams = numberOfTeams(df)
    print(numOfTeams)
    reducedDict = {}
    for i in range(192):
        reducedDict[reducedPoints[i]] = points[i]
    sortedPoints = sortAndReducePointsTable(numOfTeams,reducedDict,pointsMultiplier(numOfTeams))

    uniPoints = pointsByCurrentRankings(numOfTeams,bucketTeams(df),sortedPoints)
    uniPointsFrame = pd.DataFrame.from_dict(uniPoints, orient = "index", columns = ["Points"])
    uniPointsFrame = uniPointsFrame.sort_values(by = "Points", ascending = False)

    print(uniPointsFrame)
    uniPointsFrame.to_csv(outDir)
    
week = "1"
inputs = [str("Ow/Ow_week" + week + ".csv"),"R6/R6_week"+ week +".csv","Dota/Dota_week" + week + ".csv", "Val/Val_week" + week + ".csv", "CS/CS_week" + week+ ".csv"]
outputs = ["/Ow/Οw_week" + week + "_currentRankings.csv","R6/R6_week" + week + "_currentRankings.csv","Dota/Dota_week" + week + "_currentRankings.csv", "Val/Val_week" + week + "_currentRankings.csv", "CS/CS_week" + week + "_currentRankings.csv"]
 

for i in range(len(inputs)):
    gamePointsByCurrentRankings("data/"+inputs[i], "data/"+outputs[i])



totalPointsByCurrentRanking = pd.read_csv("data/Ow/Οw_week1_currentRankings.csv",index_col=0)
for i in range(1,len(inputs)):
    b = pd.read_csv("data/" + outputs[i],index_col=0)
    totalPointsByCurrentRanking = totalPointsByCurrentRanking.add(b,fill_value=0)
totalPointsByCurrentRanking = totalPointsByCurrentRanking.sort_values(by = "Points", ascending = False)
print(totalPointsByCurrentRanking)

totalPointsByCurrentRanking.to_csv("data/total/total_week1_currentRankings.csv")


#todo output totals into one weekly csv
#todo move points calculator into separate file, and algos into separate files