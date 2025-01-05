import requests
from bs4 import BeautifulSoup
import pandas as pd
response = requests.get("https://muhlenbergsports.com/sports/football/stats")
parser = BeautifulSoup(response.text,'html.parser')
parser.prettify()
def scrape_individual_stats(parser:BeautifulSoup):
    offense_player_stats = ["individual-offense-passing","individual-offense-rushing","individual-offense-receiving"]
    defense_player_stats = ["individual-defense"]
    sp_player_stats  = ["individual-special-kicking","individual-special-returns"]
    for label in offense_player_stats + defense_player_stats + sp_player_stats:
        section = parser.find("section",{"id":label})
        label = label.replace("-","_")
        html_tables = section.find_all("table")
        for idx , table in enumerate(list(html_tables)):
            df = pd.read_html(table.decode())[0]
            df.to_csv("stats/{}.csv".format(label + str(idx) if idx != 0 else label))
            print("csv saved successfully")
def scrape_team_stats(parser:BeautifulSoup):
    section = parser.find("section",{"id":"team"})
    html_tables = section.find_all("table")
    label = "team"
    for idx , table in enumerate(list(html_tables)):
        df = pd.read_html(table.decode())[0]
        df.to_csv("stats/{}.csv".format(label + str(idx) if idx != 0 else label))
        print("csv saved successfully")
    #for game by game
    label = "gbg_results"
    section = parser.find("section",{"id":label})
    html_tables = section.find_all("table")
    for idx , table in enumerate(list(html_tables)):
        df = pd.read_html(table.decode())[0]
        df.to_csv("stats/{}.csv".format(label + str(idx) if idx != 0 else label))
        print("csv saved successfully")
scrape_team_stats(parser)
    
                