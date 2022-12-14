import requests
import lxml
import pandas as pd
from bs4 import BeautifulSoup     


def getTeams(html, regional = False, region = None):#Returns table of team standings
    #regional leagues sort teams by "points" 
    if regional:
        df = pd.read_html(html, extract_links = "body", match = "Points" )
        if region == "*":#national leagues need dummy teams added to distinguish different divisions
            for i in range (len(df)-1):
                print(i)
                print(df[i])
                df2 = pd.DataFrame.from_dict({"Team 1": ["Team 25"], "University": [None]})
                
                print(df2)
                df[i] = pd.concat([df[i],df2])
    else:#non regional leagues sort teams by standings
        df = pd.read_html(html, extract_links = "body", match = "Standings" ) 
     
    print(df)
    d = pd.concat(df,ignore_index = True) #the standings may be multiple different tables for each division, so we have to concat them

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

#only needed if a team isn't found in our local database
def getTeamSoup(teamLink):#requesting the team page
    if teamLink == None:
        return None
    r = requests.get("https://tournaments.nse.gg/" + teamLink) 
    teamSoup = BeautifulSoup(r.content, 'lxml')
    return teamSoup

#only needed if a team isn't found in our local database
def getTeamUni(teamSoup):#scraping a team's university from its team page
    if teamSoup == None:
        return None
    names = str(teamSoup.find("h1", class_ = "university-title center"))
    names = names.partition('\n')[2]#get rid of first line
    name = names.partition('\n')[0]#take (new) first line
    name = name.strip()
    return name


def scrapeGame(sourceDir, outDir, region = None):
    
    w = "4" #week number
    
    r = requests.get(sourceDir) 
    c = (r.content)
    
    #tag for regional leagues
    regional = False
    if region !=None:
        regional = True


    
    table = getTeams(c, regional, region)#gets the table from the nse website of the standings for that week
    teams = table["Team 1"]#gets the teams column of the standings table


    uniNames = []
    print (teams)
    
    #load the seedings database to quickly map team names to universities and seedings, without having to make web requests
    seedings = pd.read_csv("data/"+ outDir + "/seedings.csv", index_col = 0)
    
    
    #mapping all the teams in the standings to their respective university in the 
    for team in teams:
        #Find the team in the seedings database
        mask = seedings["Team url"] == team[1]
        currentTeam = seedings[mask]
        #if the team is found in the seedings database, use the stored values for team uni and seed
        if (any(mask)):
            teamUni = currentTeam["University"].to_numpy()[0]
            #seed = currentTeam["Seeds"].to_numpy()[0]
            uniNames.append(teamUni)
            print(teamUni)
                    
        else:#if we cant find the team in our database, scrape its university from its nse page
            teamUni = getTeamUni(getTeamSoup(team[1]))
            uniNames.append(teamUni)
            print(teamUni)
    
    table["University"] = uniNames
    table["Team 1"] = table["Team 1"].apply(lambda x: x[0])


    #output format is different depending on if we are dealing with a regional league
    if region == None:
        table.to_csv("data/"+outDir+"/"+outDir+"_week"+w+".csv",columns = ["Team 1","University"])  
    elif region == "N":
        table.to_csv("data/"+outDir+"/North/"+outDir+"N_week"+w+".csv",columns = ["Team 1","University"])
    elif region == "S":
        table.to_csv("data/"+outDir+"/South/"+outDir+"S_week"+w+".csv",columns = ["Team 1","University"])
    elif region == "*":
        table.to_csv("data/"+outDir+"/"+outDir+"_week"+w+".csv",columns = ["Team 1","University"])    
        
        

def cupScraper(cupPage, standings):
    table = pd.read_csv(standings)
    teams = table["WEBSITE NAME:"]
    
    r = requests.get(cupPage) 
    soup = BeautifulSoup(r.content, 'lxml')



#uncomment a line when you want to scrape that game - you may need to update the URL



#scrapeGame("https://tournaments.nse.gg/tournaments/overwatch-winter-22/stage-1#round-5342", "Ow") 
#scrapeGame("https://tournaments.nse.gg/tournaments/rainbow-6-siege-winter-22/stage-1#round-5341", "R6")
#scrapeGame("https://tournaments.nse.gg/tournaments/dota-2-winter-22/stage-1#round-5308", "Dota")
#scrapeGame("https://tournaments.nse.gg/tournaments/valorant-winter-22/stage-1#round-5311", "Val") #hull hornets vs beehave unreported
#scrapeGame("https://tournaments.nse.gg/tournaments/csgo-winter-22/stage-1#round-5307", "CS") #remove bye match loser
#scrapeGame("https://tournaments.nse.gg/tournaments/rocket-league-winter-22-north/week-3#round-5439", "RL", "N") 
#scrapeGame("https://tournaments.nse.gg/tournaments/rocket-league-winter-22-south/week-3#round-5440", "RL", "S") 
#scrapeGame("https://tournaments.nse.gg/tournaments/rocket-league-winter-22-national/week-3#round-5418", "RL", "*") 

#scrapeGame("https://tournaments.nse.gg/tournaments/league-of-legends-winter-22-north/week-3#round-5441", "LOL", "N") #3 unreported
#scrapeGame("https://tournaments.nse.gg/tournaments/league-of-legends-winter-22-south/week-3#round-5442", "LOL", "S") #6 unreported
#scrapeGame("https://tournaments.nse.gg/tournaments/league-of-legends-winter-22-national/week-3#round-5423", "LOL", "*") #2 unreported games

#todo: smash, tft matches? multiversus
#todo: cups
#todo: affiliate
#todo: make this fast by saving teams's unis, rather than scraping them each time!
#todo: auto remove "match losers"



#standings = "https://docs.google.com/spreadsheets/d/1ei_at6MfVtV5oBZwkVzPXAP1Bwd-rQCydq-FenfVI-g/gviz/tq?tqx=out:csv&sheet=LEADERBOARD"
#cupPage = "https://nse.gg/tournaments/buec-winter-2022/nse-winter-cup-featuring-fortnite/"
#cupScraper(cupPage,standings)

#tft
#https://docs.google.com/spreadsheets/d/1yitJXmJ2RnNvOh6LzunZVZjfgRHkg9ca9sRCeqb_CzY/gviz/tq?tqx=out:csv&sheet=LEADERBOARD


#smash
#https://docs.google.com/spreadsheets/d/1wg9O0Y8pGpzmZnmra5K7WKGfxBDqI4vsahuLgiR-Bu4/gviz/tq?tqx=out:csv&sheet=Week 3

#UFG
#https://docs.google.com/spreadsheets/d/1o45nqHoQhwo7claNvMLbyerEq_32xPUJXPM7VJndK4w/gviz/tq?tqx=out:csv&sheet=Street Fighter V
#https://docs.google.com/spreadsheets/d/1o45nqHoQhwo7claNvMLbyerEq_32xPUJXPM7VJndK4w/gviz/tq?tqx=out:csv&sheet=Tekken 7
#https://docs.google.com/spreadsheets/d/1o45nqHoQhwo7claNvMLbyerEq_32xPUJXPM7VJndK4w/gviz/tq?tqx=out:csv&sheet=Guilty Gear Strive
sheet_id = "1o45nqHoQhwo7claNvMLbyerEq_32xPUJXPM7VJndK4w"
sheet_name = "Guilty Gear Strive"

#url = f???https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
#url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
#print(url)
#x = pd.read_csv(url)
#x.to_csv("data/UFG/GGS/UFG/GGS_week3_positions.csv")

UFG = ["UFG/GGS","UFG/Tekken", "UFG/SFV"]
for game in UFG:
    w="3"
    df = pd.read_csv("data/"+game + "/" + game + "_week3_positions.csv", header = 0)
    df.rename(columns={ df.columns[0]: "position" }, inplace = True)
    print(df)
    df = df[(df["position"] == df["position"] ) & ( df["University"] == df["University"])]

    size = len(df)
    
    unis = df[["position","University"]]
    unis.rename(columns = {"position":"Team 1"}, inplace=True)
    print(unis)
    unis.to_csv("data/"+game+"/"+game+"_week"+w+".csv",columns = ["Team 1","University"]) 




def teamScraper(teamLink, positionsLink, outDir):
    w = "3"
    d = []
    for i in range(1,7):
        link = teamLink + "/sort/name?page=" + str(i)
        print(link)
        df = pd.read_html(link, extract_links = "body", match = "Confirmed" )
        d.append(df[0])

    d = pd.concat(d,ignore_index = True)
    teams = d["Name"]
    print (teams)
    
    teams["Team"] = teams[0]

    
    positions = pd.read_csv(positionsLink, header = 0, index_col = 0, usecols = ["Standings", "Team"])
    positions = positions.rename(columns = {0:"Team 1"})
    positions = positions.rename(columns = {"Team":"Team 1"})
    print("positions")
    print(positions)
    unis = []
    for team in positions["Team 1"]:
        print(team)
        for i in teams:
        
            if i[0] == team:
                print(i[0])
                print(i[1])
                uni = i[1]
        unis.append(uni)
    positions["University"] = unis
    
    positions["University"] = positions["University"].apply(lambda x: getTeamUni(getTeamSoup(x)))

    positions.to_csv("data/"+outDir+"/"+outDir+"_week"+w+".csv",columns = ["Team 1","University"])


#teamScraper("https://tournaments.nse.gg/tournaments/teamfight-tactics-winter-22/teams", "data/TFT/TFT Week_3_positions.csv", "TFT")
#teamScraper("https://tournaments.nse.gg/tournaments/super-smash-bros-ultimate-teams-winter-22/teams", "data/Smash/Teams/Week 3 positions.csv", "Smash/Teams")




#todo: remove teams with 0 wins (inelligible)
#todo: ceil