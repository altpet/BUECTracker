import pandas as pd
import requests
import lxml
from os.path import isfile
from scraper import getTeams, getTeamUni, getTeamSoup
import numpy as np
import re


#almost identical to the getTeams function in scraper.py. Retrieves the standings of the teams
def getTeams(html, html2 = None, html3 = None):#Returns table with names of teams in ranking order
    
    if html2 != None:
        df = pd.read_html(html, extract_links = "body", match = "Points" )
    else:
        df = pd.read_html(html, extract_links = "body", match = "Standings" ) 
    d = pd.concat(df,ignore_index = True)#gets the most recent ranking 
    if html2 != None:
        df = pd.read_html(html2, extract_links = "body", match = "Points" )
        df.append(d)
        d = pd.concat(df,ignore_index = True)
    if html3 != None:
        df = pd.read_html(html3, extract_links = "body", match = "Points" )
        df.append(d)
        d = pd.concat(df,ignore_index = True)
    return d


def getTeamSeed(teamSoup):
    if teamSoup == None:
        return None
    seed = teamSoup.find("div",string = "Seeding")#
    seed = seed.next_sibling
    seed = str(seed.next_sibling)
    seed = re.findall("\d+|>-<",seed)[0]
    if seed != ">-<":
        return int(seed)
    else:
        return None


#returns how many teams at that uni had a >= seeding than that team        
def getTeamUniSeed( uni, seed, df):

    return (len(df[(df["University"]==uni) & (df["Seeds"] <= seed)]))



#takes the url of the teams in a tournament (usually the most recent standings). Takes 3 urls for regional leagues (for the 3 regions)
#outputs a mapping from said teams to their university, seeding in the tournament, and which team they are for that uni (eg Warwick 1st team, Warwick 2nd team, ...)
def getSeedings(url, outDir, url2 = None, url3 = None):
    r = requests.get(url) 
    c = (r.content)
    #regional league datasets
    c2=None
    c3=None
    if url2 != None:
            r2 = requests.get(url2) 
            c2 = (r2.content)
    if url3 != None:
        r3 = requests.get(url3) 
        c3 = (r3.content)


    #retrives a table of the current standings of teams
    table = getTeams(c,c2,c3)
    teams = table["Team 1"]#gets the teams column of the standings
    df = pd.DataFrame.from_records(teams)
    df.columns = ["Team Name", "Team url"]
    
    uniNames = []
    seeds = []
    if (isfile("data/"+ outDir + "/seedings.csv")):#if we have existing data, load it
        currentData = pd.read_csv("data/"+ outDir + "/seedings.csv", index_col = 0)
    for team in teams:
        if ((isfile("data/"+ outDir + "/seedings.csv"))):#try see if we have data on this team already. 
            mask = currentData["Team url"] == team[1]
            currentTeam = currentData[mask]
            if (any(mask)):#If already have data on a team, we can use that, and dont need to scrape new data
                teamUni = currentTeam["University"].to_numpy()[0]
                seed = currentTeam["Seeds"].to_numpy()[0]
                
            else:#if we dont have data on a team, scrape it
                print("a")
                print(team)
                teamUni = getTeamUni(getTeamSoup(team[1]))
                seed = getTeamSeed(getTeamSoup(team[1]))
                print(seed)
        else:#if we dont have data on a team, scrape it
            print("b")
            print(team[1])
            teamUni = getTeamUni(getTeamSoup(team[1]))
            seed = getTeamSeed(getTeamSoup(team[1]))
            print(teamUni)
            print(seed)
        uniNames.append(teamUni)
        seeds.append(seed)
        
    df["University"] = uniNames
    df["Seeds"] = seeds
    
    
    #uses the existing data to assign each team a uni seeding (eg Warwick 1st team, Warwick 2nd team, etc...)
    uniSeeds = []
    for index, row in df.iterrows():
        uniSeeds.append(getTeamUniSeed(row["University"], row["Seeds"], df))
    df["Uni seeds"] = uniSeeds
    
    df.columns = ["Team Name", "Team url", "University", "Seeds", "Uni seeds"]
    print(df.head(n=10))
    df.to_csv("data/"+ outDir + "/seedings.csv")  

#uncomment a line if you want to remake the database for team seedings

#getSeedings("https://tournaments.nse.gg/tournaments/overwatch-winter-22/stage-1#round-5384","Ow")
#getSeedings("https://tournaments.nse.gg/tournaments/rainbow-6-siege-winter-22/stage-1#round-5341", "R6")
#getSeedings("https://tournaments.nse.gg/tournaments/dota-2-winter-22/stage-1#round-5308", "Dota")  #needs reformatting
#getSeedings("https://tournaments.nse.gg/tournaments/valorant-winter-22/stage-1#round-5411", "Val") #wattare u doing to watt #needs reformatting
#getSeedings("https://tournaments.nse.gg/tournaments/csgo-winter-22/stage-1#round-5307", "CS") #remove bye match loser #needs reformatting
#getSeedings("https://tournaments.nse.gg/tournaments/rocket-league-winter-22-national/week-3#round-5415","RL","https://tournaments.nse.gg/tournaments/rocket-league-winter-22-north/week-3#round-5439","https://tournaments.nse.gg/tournaments/rocket-league-winter-22-south/week-3#round-5440" ) 
#getSeedings("https://tournaments.nse.gg/tournaments/league-of-legends-winter-22-national/week-3#round-5423", "LOL", "https://tournaments.nse.gg/tournaments/league-of-legends-winter-22-north/week-3#round-5441", "https://tournaments.nse.gg/tournaments/league-of-legends-winter-22-south/week-3#round-5442") #Washington redskins to nott trent, remove 2match bye loser