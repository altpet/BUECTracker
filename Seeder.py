import pandas as pd
import requests
import lxml
from os.path import isfile
from scraper import getTeams, getTeamUni, getTeamSoup
import numpy as np

def getTeams(html):#Returns table with names of teams in ranking order
    df = pd.read_html(html, extract_links = "body")
    d = df[-1]#gets the most recent ranking 
    return d


def getSeedings(url, outDir):
    r = requests.get(url) 
    c = (r.content)

    table = getTeams(c)
    teams = table["Team 1"]#gets the teams
    df = pd.DataFrame.from_records(teams)
    df.columns = ["Team Name", "Team url"]
    uniNames = []
    if (isfile("data/"+ outDir + "/seedings.csv")):
        currentData = pd.read_csv("data/"+ outDir + "/seedings.csv", index_col = 0)
    for team in teams:
        if ((isfile("data/"+ outDir + "/seedings.csv"))):
            mask = currentData["Team url"] == team[1]
            currentTeam = currentData[mask]
            if (any(mask)):
                teamUni = currentTeam["University"].to_numpy()[0] 
            else:
                print("a")
                print(team)
                teamUni = getTeamUni(getTeamSoup(team[1]))
        else:
            print("b")
            teamUni = getTeamUni(getTeamSoup(team[1]))
        uniNames.append(teamUni)
        
    df["University"] = uniNames
    
    df.columns = ["Team Name", "Team url", "University"]
    print(df.head(n=10))
    df.to_csv("data/"+ outDir + "/seedings.csv")  



#getSeedings("https://tournaments.nse.gg/tournaments/overwatch-winter-22/stage-1#round-5384","Ow")
#getSeedings("https://tournaments.nse.gg/tournaments/rainbow-6-siege-winter-22/stage-1#round-5341", "R6")
#getSeedings("https://tournaments.nse.gg/tournaments/dota-2-winter-22/stage-1#round-5308", "Dota")
#getSeedings("https://tournaments.nse.gg/tournaments/valorant-winter-22/stage-1#round-5411", "Val") #wattare u doing to watt
#getSeedings("https://tournaments.nse.gg/tournaments/csgo-winter-22/stage-1#round-5307", "CS") #remove bye match loser
#getSeedings("https://tournaments.nse.gg/tournaments/rocket-league-winter-22-north/stage-1#round-5328", "RL/North") 
#getSeedings("https://tournaments.nse.gg/tournaments/rocket-league-winter-22-south/stage-1#round-5330", "RL/South")
#getSeedings("https://tournaments.nse.gg/tournaments/league-of-legends-winter-22-north/stage-1#round-5326", "LOL/North") #Washington redskins to nott trent, remove 2match bye loser
#getSeedings("https://tournaments.nse.gg/tournaments/league-of-legends-winter-22-south/stage-1#round-5327", "LOL/South")