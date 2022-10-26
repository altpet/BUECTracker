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


def cupScraper(cupPage, standings):
    table = pd.read_csv(standings)
    teams = table["WEBSITE NAME:"]
    
    r = requests.get(cupPage) 
    soup = BeautifulSoup(r.content, 'lxml')



w = "2"

#scrapeGame("https://tournaments.nse.gg/tournaments/overwatch-winter-22/stage-1#round-5342", "data/Ow/Ow_week"+w+".csv") #camdu punters to cam
#scrapeGame("https://tournaments.nse.gg/tournaments/rainbow-6-siege-winter-22/stage-1#round-5341", "data/R6/R6_week"+w+".csv")
#scrapeGame("https://tournaments.nse.gg/tournaments/dota-2-winter-22/stage-1#round-5308", "data/Dota/Dota_week"+w+".csv")
#scrapeGame("https://tournaments.nse.gg/tournaments/valorant-winter-22/stage-1#round-5311", "data/Val/Val_week"+w+".csv") #wattare u doing to watt
#scrapeGame("https://tournaments.nse.gg/tournaments/csgo-winter-22/stage-1#round-5307", "data/CS/CS_week"+w+".csv") #remove bye match loser
#scrapeGame("https://tournaments.nse.gg/tournaments/rocket-league-winter-22-north/stage-1#round-5328", "data/RL/RLN_week"+w+".csv") 
#scrapeGame("https://tournaments.nse.gg/tournaments/rocket-league-winter-22-south/stage-1#round-5330", "data/RL/RLS_week"+w+".csv")
#scrapeGame("https://tournaments.nse.gg/tournaments/league-of-legends-winter-22-north/stage-1#round-5326", "data/LOL/LOLN_week"+w+".csv") #Washington redskins to nott trent, remove 2match bye loser
#scrapeGame("https://tournaments.nse.gg/tournaments/league-of-legends-winter-22-south/stage-1#round-5327", "data/LOL/LOLS_week"+w+".csv")


#todo: smash, tft matches? multiversus
#todo: cups
#todo: affiliate
#todo: make this fast by saving teams's unis, rather than scraping them each time!
#todo: auto remove "match losers"



#standings = "https://docs.google.com/spreadsheets/d/1ei_at6MfVtV5oBZwkVzPXAP1Bwd-rQCydq-FenfVI-g/gviz/tq?tqx=out:csv&sheet=LEADERBOARD"
#cupPage = "https://nse.gg/tournaments/buec-winter-2022/nse-winter-cup-featuring-fortnite/"
#cupScraper(cupPage,standings)