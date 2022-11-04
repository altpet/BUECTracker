import numpy as np
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

def pointsMultiplier(numberOfTeams,cup = False, singleAndTeamsEvent = False, singlePlayerChamp = False, teamChamp = False  ):#Whether the game receives a point penalty (eg too few teams) #needs implementations for diff types of games
    pointsMultiplier = 1
    if singlePlayerChamp:
        pointsMultiplier *= 1/2
    
    if singleAndTeamsEvent:
        if singlePlayerChamp:
            pointsMultiplier *= 4/5
        elif teamChamp:
            pointsMultiplier *=2/3
    
        pointsMultiplier *= 1/3
    
    elif numberOfTeams<32:
        pointsMultiplier *= 2/3
        
    if cup:
        print("cup")
        pointsMultiplier *= 1/3
        
        
    return pointsMultiplier

def sortAndReducePointsTable(numberOfTeams,reducedDict,pointsMultiplier):#Creates a custom points allocation table based on the number of teams participating
    print(pointsMultiplier)     
    if numberOfTeams<192:
        for i in range(numberOfTeams,192,1):
            reducedDict.pop(i+1)
    
    sortedPoints = []
    for i in reducedDict:
        sortedPoints.append(reducedDict[i])

    sortedPoints.sort(reverse=True)
    print(sortedPoints)
    sortedPoints = np.multiply(sortedPoints, pointsMultiplier)
    sortedPoints = sortedPoints.tolist()
    return sortedPoints

points = makePoints()
reducedPoints = makeReducedPoints()


import pandas as pd
import numpy as np

def loadDF(path):#Loads dataframe from a csv on path
    return pd.read_csv(path, index_col=0, dtype = {"Team 1" : str,"University": str})

def numberOfTeams(df):#Calculate number of teams (by ignoring NONE entries used to denote a different swiss division
    df2 = df.copy(deep=True)
    df2.dropna(axis = 0, how = "any",inplace=True)
    numberOfTeams = (len(df2.index))
    return numberOfTeams
  
def elligibleTeams(numberOfTeams):#calculate number of teams elligible to receive poitnts
    compare = ((numberOfTeams-64)*(2/3))+64
    elligibleTeams = min(compare,numberOfTeams,256)
    return elligibleTeams   

def bucketTeams(df):#Take the swiss rankings and bucket teams into their relevent swiss divisions
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

def doNothing(df):#Don't bucket teams, just order as they are
    unis = df["University"]
    buckets = []
    tempBucket = []
    
    for i in unis:
        
        tempBucket = []
        tempBucket.append(i)
        buckets.append(tempBucket)
    return buckets
    

def pointsByCurrentRankings(numberOfTeams,buckets,sortedPoints, regional = False, regionalOffset = 0):#allocates BUEC Points, given bucketed Swiss rankings
    ellTeams = elligibleTeams(numberOfTeams)
    print(ellTeams)
    pointsSum = {}
    counter = 0
    for bucket in buckets:
        if counter < ellTeams - regionalOffset:#only award points to elligible teams
            temp = 0
            for team in bucket:#award points to teams in bucket
                counter +=1
                if regional:
                    counter +=1
                if counter <= 192:#if there are still points available to be given (occurs when there are ties that make elligible teams > 192)
                    temp += sortedPoints.pop(0)
                    if regional:
                        temp += sortedPoints.pop(0)
            print(bucket)
            if regional:
                temp = temp/(len(bucket)*2)#if regional, avg over 2x the size
            else:
                temp = temp/len(bucket) #average
            for team in bucket:
                pointsSum[team] = pointsSum.setdefault(team,0) + temp
        print(counter)    
    return pointsSum, sortedPoints



def gamePointsByCurrentRankings(sourceDir, outDir, orderingAlg,  regional = False,  cup = False ):#runs the pointsByCurrentRankings algorithm
    if regional:
        #loading data, and making the custom points allocation table
        df = loadDF(sourceDir)
        split = sourceDir.split("/")
        split2 = split[2].split("_")
        nDir = split[0]+"/"+split[1]+"/"+"North/"+split2[0] +"N_"+split2[1]
        sDir = split[0]+"/"+split[1]+"/"+"South/"+split2[0] +"S_"+split2[1]
        dfN = loadDF(nDir)
        dfS = loadDF(sDir)
        nNumOfTeams = numberOfTeams(dfN)
        sNumOfTeams = numberOfTeams(dfS)
        natNumOfTeams = numberOfTeams(df)
        numOfTeams = nNumOfTeams+sNumOfTeams+natNumOfTeams

        reducedDict = {}
        for i in range(192):
            reducedDict[reducedPoints[i]] = points[i]
        sortedPoints = sortAndReducePointsTable(numOfTeams,reducedDict,pointsMultiplier(numOfTeams,cup))
        #allocating points given the swiss rankings
        uniPoints,sortedPoints = pointsByCurrentRankings(numOfTeams,orderingAlg(df),sortedPoints, False)
        print(uniPoints)
        reducedDict = {}
        for i in range(192):
            reducedDict[reducedPoints[i]] = points[i]
        sortedPointsS = sortAndReducePointsTable(numOfTeams+sNumOfTeams*2,reducedDict,pointsMultiplier(numOfTeams,cup))
        for i in range(natNumOfTeams):
            sortedPointsS.pop()
        #allocating points given the swiss rankings
        uniPoints2,sortedPointsS = pointsByCurrentRankings(numOfTeams+sNumOfTeams*2,orderingAlg(dfS),sortedPointsS, regional, natNumOfTeams)
        print(uniPoints2)
        
        reducedDict = {}
        for i in range(192):
            reducedDict[reducedPoints[i]] = points[i]
        sortedPointsN = sortAndReducePointsTable(numOfTeams+nNumOfTeams*2,reducedDict,pointsMultiplier(numOfTeams,cup))
        for i in range(natNumOfTeams):
            sortedPointsN.pop()
        #allocating points given the swiss rankings
        uniPoints3,sortedPointsN = pointsByCurrentRankings(numOfTeams+nNumOfTeams*2,orderingAlg(dfN),sortedPointsN, regional, natNumOfTeams)
        print(uniPoints3)
        
        for i in uniPoints2:
            uniPoints[i] = uniPoints.setdefault(i,0) + uniPoints2[i]
        for i in uniPoints3:
            uniPoints[i] = uniPoints.setdefault(i,0) + uniPoints3[i]
    else:
            
        #loading data, and making the custom points allocation table
        df = loadDF(sourceDir)
        numOfTeams = numberOfTeams(df)
        if regional:#if regional leagues, we need to double the num of teams
            numOfTeams = numOfTeams * 2
        print(numOfTeams)
        reducedDict = {}
        for i in range(192):
            reducedDict[reducedPoints[i]] = points[i]
        sortedPoints = sortAndReducePointsTable(numOfTeams,reducedDict,pointsMultiplier(numOfTeams,cup))
        #allocating points given the swiss rankings
        uniPoints,sortedPoints = pointsByCurrentRankings(numOfTeams,orderingAlg(df),sortedPoints, regional)
    
    #printing and saving the points table for that game
    uniPointsFrame = pd.DataFrame.from_dict(uniPoints, orient = "index", columns = ["Points"])
    nniPointsFrame = uniPointsFrame.rename_axis( index = "University" )
    uniPointsFrame = uniPointsFrame.sort_values(by = "Points", ascending = False)
    print(uniPointsFrame)
    uniPointsFrame.to_csv(outDir)
    

    
    
#data directories (can update the week num to save new set of data for new week)    
week = "3"
dirs = ["Ow","R6","Dota","CS","Val","RL","LOL"]
inputs = []
for g in dirs:
    inputs.append(g+"/"+g+"_week"+ week + ".csv")
    
#inputs[0] ="Ow/Ow_week" + "2"+ ".csv"
#inputs[1] = "R6/R6_week" + "2"+ ".csv"
    
outputs = []
for g in dirs:
    outputs.append(g + "/" + g + "_week" + week + "_currentRankings.csv")
    
#outputs[0] = "Ow/Οw_week" + "2"+ "_currentRankings.csv"
#outputs[1] = "R6/R6_week" + "2"+ "_currentRankings.csv"

games = ["Overwatch", "R6: Siege", "DOTA 2", "CS:GO", "VALORANT" , "Rocket League", "League of Legends"]
regionalBitmap = [False,False,False,False,False,True,True]



#Calculate Points tables for each game/dataset
for i in range(len(inputs)):       
    gamePointsByCurrentRankings("data/"+inputs[i], "data/"+outputs[i], bucketTeams, regionalBitmap[i])

#Calculate Points tables for each cup
gamePointsByCurrentRankings("data/Fortnite/Fortnite Week 2.csv", "data/Fortnite/Fortnite_finalRankings.csv", doNothing, False, True)



#Sum the point tables across each game into a "total points table"
totalPointsByCurrentRanking = pd.read_csv("data/Ow/Οw_week" + "2"+ "_currentRankings.csv",index_col=0)#manually change 
for i in range(1,len(inputs)):
    b = pd.read_csv("data/" + outputs[i],index_col=0)
    totalPointsByCurrentRanking = totalPointsByCurrentRanking.add(b,fill_value=0)


#cups
b = pd.read_csv("data/Fortnite/Fortnite_finalRankings.csv",index_col=0)
totalPointsByCurrentRanking = totalPointsByCurrentRanking.add(b,fill_value=0)


totalPointsByCurrentRanking = totalPointsByCurrentRanking.sort_values(by = "Points", ascending = False)
totalPointsByCurrentRanking = totalPointsByCurrentRanking.rename_axis( index = "University" )
print(totalPointsByCurrentRanking)
totalPointsByCurrentRanking.to_csv("data/total/total_week"+week+"_currentRankings.csv")






#Merging all of the points table into one big table with totals, and each individual game total
totalPointsByCurrentRanking = totalPointsByCurrentRanking.rename(columns = {"Points": "Total Points"})
case = True
for i in range(len(inputs)):
    temp = pd.read_csv("data/" + outputs[i],index_col=0)
    temp = temp.rename(columns={"Points": games[i]})
    temp = temp.rename_axis( index = "University" )

    if False:#if regional league (reduntant code)
        if case:
            #combine the North and south tables
            temp2 = pd.read_csv("data/" + outputs[i+1],index_col=0)
            temp2 = temp2.rename(columns={"Points": games[i]})
            temp2 = temp2.rename_axis( index = "University" )
            temp = pd.concat([temp,temp2], axis = 0, sort = False)
            temp = temp.rename_axis( index = "University" )
            
            totalPointsByCurrentRanking = totalPointsByCurrentRanking.merge(temp, how = "outer", left_on = ["University"], right_on = ["University"])
            case = False
        else:#ignore the second regional time
            case = True
    else:
        totalPointsByCurrentRanking = totalPointsByCurrentRanking.merge(temp, how = "outer", left_on = "University", right_on = "University")

temp = pd.read_csv("data/Fortnite/Fortnite_finalRankings.csv",index_col=0)
temp = temp.rename(columns={"Points": "Fortnite"})
temp = temp.rename_axis( index = "University" )
totalPointsByCurrentRanking = totalPointsByCurrentRanking.merge(temp, how = "outer", left_on = "University", right_on = "University")



print(totalPointsByCurrentRanking)
totalPointsByCurrentRanking.to_csv("data/total/week"+week+"_all_games.csv")


#todo move points allocation calculator into separate file, and algos into separate files

#make pgm for total combinations, and time series

#make cups non 1-off