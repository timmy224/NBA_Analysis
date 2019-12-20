from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from io import StringIO
import csv
import time

#chrome browser options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--incognito')
chrome_options.add_argument('--headless')

driver = webdriver.Chrome(options=chrome_options)
action = ActionChains(driver)

def Player_data(): 
    """ Scrapes player data from ESPN 
    Output: CSV file 
    """
    with open('2002-2019-Regular-PlayerStats-raw.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(['Rank', 'Player', 'Season' , 'Team', 'MPG', 'PER'])

        for season in range(2003, 2020):
            url = 'http://insider.espn.com/nba/hollinger/statistics/_/year/{}'.format(season)
            driver.get(url)

            button_number_xpath = '//*[@id="my-players-table"]/div[1]/div[2]/div[1]/div[2]/div[2]'
            button_elem = driver.find_element_by_xpath(button_number_xpath)
            button_text = button_elem.text
            last_page_num = int(button_text.split()[-1])
            print('{} - Total pages:'.format(season), last_page_num)

            for page_num in range(1, last_page_num+1):
                time.sleep(5)
                WebDriverWait(driver, 5)

                url = 'http://insider.espn.com/nba/hollinger/statistics/_/page/{}/year/{}'.format(page_num, season)
                driver.get(url)
                time.sleep(5)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                my_table = soup.find('table', {'class':'tablehead'})

                check_len = my_table.findAll('tr')
                prevRank = 0
                rank = 0
                player = ''
                team_raw = ''
                team = ''

                for each in check_len:
                    try: 
                        int_check = each.findChildren()[0].contents[0]
                        try:
                            int(int_check)
                            rank = int_check
                            prevRank = rank
                        except ValueError:
                            rank = prevRank
                    except IndexError:
                        pass
                    
                    try:
                        player = each.findChildren()[1].contents[0].text
                    except:
                        player = ''
                    
                    try:
                        team_raw = each.findChildren()[1].contents
                        if len(team_raw) == 2:
                            team = team_raw[1]
                            # need to clean
                            raw = team.split(" ")
                            team = raw[-1]
                        else:
                            team = ''
                    except:
                        team = ''

                    try:
                        MPG = each.findChildren()[3].contents[0]
                        float(MPG)
                    except:
                        MPG = 0
                    
                    try: 
                        PER = each.findChildren()[12].contents[0]
                        float(PER)
                    except:
                        PER = 0
                    
                    #print(MPG)
                    print(rank, player, team, MPG, PER)
                    writer.writerow([rank, player, season, team, MPG, PER])
                
Player_data()


        