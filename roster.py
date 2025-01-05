import requests
from bs4 import BeautifulSoup
import bs4
import pandas as pd
def get_player_info(element:bs4.Tag) -> dict:
    img = "https://muhlenbergsports.com/"
    img_element = element.find("td",{"class":"image_combined_path"})
    if img_element.find("img") == None:
        img = "No picture taken"
    else:
        img+=img_element.find("img").attrs["data-src"]

    jersey_num = -1
    if element.find("td",{"class":"roster_jerseynum"}).text:
        jersey_num = int(element.find("td",{"class":"roster_jerseynum"}).text)
    player_info = {
        "name" : element.find('a').attrs["aria-label"].split("-")[0].strip(),
        "jersey" : jersey_num,
        "class" : element.find('td',{'class':'roster_class'}).text,
        "position" : element.find('td',{"class":"rp_position_short"}).text,
        "height" : float(element.find('td',{"class":"height"}).text.replace("-",".")),
        "weight" : float(element.find('td',{"class":"rp_weight"}).text),
        "hometown" : element.find('td',{"class":"player_hometown"}).text.replace(".","").upper(),
        "hs" : element.find('td',{"class":"player_highschool"}).text,
        'img' : img,
        'stats_page' : "https://muhlenbergsports.com"+element.find("td",{"class":"sidearm-table-player-name"}).a['href']
    }
    return player_info

def get_roster(link:str,year:int) -> list[bs4.Tag]:
    link+=str(year)
    session = requests.Session()
    response = session.get(link)
    parser = BeautifulSoup(response.text,'html.parser')
    return parser.find(name="div",attrs={"class":"sidearm-roster-grid-template-1"}).find("tbody")
def main() -> None:
    player_df = pd.DataFrame()
    link = "https://muhlenbergsports.com/sports/football/roster/"
    year = 2024
    #get the player roster information
    player_roster = get_roster(link,year)
    player_roster = list(filter(lambda x : type(x) == bs4.element.Tag , player_roster))
    for player in player_roster:
        player_df = pd.concat([player_df,pd.DataFrame([get_player_info(player)])])
    player_df.to_csv("players.csv")

if __name__ == "__main__":
    main()