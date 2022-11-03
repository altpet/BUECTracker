import requests
import lxml
import pandas as pd
   


def getTeams(html, regional = False):#Returns table with names of teams in ranking order
    
    if regional:
        df = pd.read_html(html, extract_links = "body", match = "Points" )
    else:
        df = pd.read_html(html, extract_links = "body", match = "Standings" ) 
    d = pd.concat(df,ignore_index = True)#gets the most recent ranking 

    return d





#Deprecated
def getTeamLink(teamName):#gets team link, or outputs None if not a valid team
    team = soup.find("a", title = teamName)
    if team == None:
        print(teamName)
        return None
    else:
        teamLink = team["href"]
    return teamLink


def getTeamSoup(teamLink):#requesting the team page
    if teamLink == None:
        return None
    r = requests.get("https://tournaments.nse.gg/" + teamLink) 
    teamSoup = BeautifulSoup(r.content, 'lxml')
    return teamSoup

def getTeamUni(teamSoup):
    if teamSoup == None:
        return None
    names = str(teamSoup.find("h1", class_ = "university-title center"))
    names = names.partition('\n')[2]#get rid of first line
    name = names.partition('\n')[0]#take (new) first line
    name = name.strip()
    return name

from bs4 import BeautifulSoup   
def scrapeGame(url, outDir, region = None):
    
    w = "3"
    r = requests.get(url) 
    c = (r.content)
    regional = False
    if region !=None:
        regional = True



    table = getTeams(c, regional)
    teams = table["Team 1"]#gets the teams


    uniNames = []
    print (teams)

    seedings = pd.read_csv("data/"+ outDir + "/seedings.csv", index_col = 0)
    
    for team in teams:
    
        mask = seedings["Team url"] == team[1]
        currentTeam = seedings[mask]
        if (any(mask)):
            teamUni = currentTeam["University"].to_numpy()[0]
            #seed = currentTeam["Seeds"].to_numpy()[0]
            uniNames.append(teamUni)
            print(teamUni)
                    
        else:

    
            teamUni = getTeamUni(getTeamSoup(team[1]))
            uniNames.append(teamUni)
            print(teamUni)
    
    table["University"] = uniNames
    table["Team 1"] = table["Team 1"].apply(lambda x: x[0])



    if region == "N":
        table.to_csv("data/"+outDir+"/North/"+outDir+"N_week"+w+".csv",columns = ["Team 1","University"])
    elif region == "S":
        table.to_csv("data/"+outDir+"/South/"+outDir+"S_week"+w+".csv",columns = ["Team 1","University"])
    else:
        table.to_csv("data/"+outDir+"/"+outDir+"_week"+w+".csv",columns = ["Team 1","University"])    
        
        

def cupScraper(cupPage, standings):
    table = pd.read_csv(standings)
    teams = table["WEBSITE NAME:"]
    
    r = requests.get(cupPage) 
    soup = BeautifulSoup(r.content, 'lxml')




#scrapeGame("https://tournaments.nse.gg/tournaments/overwatch-winter-22/stage-1#round-5342", "Ow") #camdu punters to cam
#scrapeGame("https://tournaments.nse.gg/tournaments/rainbow-6-siege-winter-22/stage-1#round-5341", "R6")
#scrapeGame("https://tournaments.nse.gg/tournaments/dota-2-winter-22/stage-1#round-5308", "Dota")
#scrapeGame("https://tournaments.nse.gg/tournaments/valorant-winter-22/stage-1#round-5311", "Val") #wattare u doing to watt
#scrapeGame("https://tournaments.nse.gg/tournaments/csgo-winter-22/stage-1#round-5307", "CS") #remove bye match loser
#scrapeGame("https://tournaments.nse.gg/tournaments/rocket-league-winter-22-north/week-3#round-5439", "RL", "N") 
#scrapeGame("https://tournaments.nse.gg/tournaments/rocket-league-winter-22-south/week-3#round-5440", "RL", "S")
#scrapeGame("https://tournaments.nse.gg/tournaments/rocket-league-winter-22-national/week-3#round-5418", "RL", "*")

scrapeGame("https://tournaments.nse.gg/tournaments/league-of-legends-winter-22-north/week-3#round-5441", "LOL", "N") #Washington redskins to nott trent, remove 2match bye loser
scrapeGame("https://tournaments.nse.gg/tournaments/league-of-legends-winter-22-south/week-3#round-5442", "LOL", "S")
scrapeGame("https://tournaments.nse.gg/tournaments/league-of-legends-winter-22-national/week-3#round-5423", "LOL", "*")

#todo: smash, tft matches? multiversus
#todo: cups
#todo: affiliate
#todo: make this fast by saving teams's unis, rather than scraping them each time!
#todo: auto remove "match losers"



#standings = "https://docs.google.com/spreadsheets/d/1ei_at6MfVtV5oBZwkVzPXAP1Bwd-rQCydq-FenfVI-g/gviz/tq?tqx=out:csv&sheet=LEADERBOARD"
#cupPage = "https://nse.gg/tournaments/buec-winter-2022/nse-winter-cup-featuring-fortnite/"
#cupScraper(cupPage,standings)