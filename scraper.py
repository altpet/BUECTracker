import requests
import lxml
import pandas as pd
   


def getTeams(html):#Returns table with names of teams in ranking order
    df = pd.read_html(html, extract_links = "body")
    d = df[-1]#gets the most recent ranking 
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
def scrapeGame(url, outDir):

    r = requests.get(url) 
    c = (r.content)

    table = getTeams(c)
    teams = table["Team 1"]#gets the teams


    uniNames = []
    print (teams)

    for team in teams:
        teamUni = getTeamUni(getTeamSoup(team[1]))
        uniNames.append(teamUni)
        print(teamUni)
        
    table["University"] = uniNames
    table["Team 1"] = table["Team 1"].apply(lambda x: x[0])

    table.to_csv(outDir,columns = ["Team 1","University"])

#scrapeGame("https://tournaments.nse.gg/tournaments/overwatch-winter-22/stage-1#round-5342", "data/Ow/Ow_week1.csv") #camdu punters to cam
#scrapeGame("https://tournaments.nse.gg/tournaments/rainbow-6-siege-winter-22/stage-1#round-5341", "data/R6/R6_week1.csv")
#scrapeGame("https://tournaments.nse.gg/tournaments/dota-2-winter-22/stage-1#round-5308", "data/Dota/Dota_week1.csv")
#scrapeGame("https://tournaments.nse.gg/tournaments/valorant-winter-22/stage-1#round-5311", "data/Val/Val_week1.csv") #wattare u doing to watt
scrapeGame("https://tournaments.nse.gg/tournaments/csgo-winter-22/stage-1#round-5307", "data/CS/CS_week1.csv") #remove bye match loser


#todo: smash, league and rl north south, tft matches? multiversus
#todo: cups
#todo: affiliate