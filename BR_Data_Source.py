""" Grabs individual player stats from Basketball-Reference.com """

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from io import StringIO
import csv

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--incognito')
#chrome_options.add_argument('--headless')

driver = webdriver.Chrome(options=chrome_options)
action = ActionChains(driver)

def Player_totals_Scrape():
    """
    Gets individual player stats from years 1999 to 2019 

    Output: {string} of comma-separated values
    """
    data = ''

    for year in range(1999, 2020):

        url = 'https://www.basketball-reference.com/leagues/NBA_{}_totals.html'.format(year)

        driver.get(url)

        WebDriverWait(driver, 5)
        share_button_xpath = '//span[text()[contains(., "Share & more")]]'
        total_button_xpath = '//div[@class="current"]' # header hides view if I don't do this
        share_button = driver.find_element_by_xpath(share_button_xpath)
        total_button = driver.find_element_by_xpath(total_button_xpath)
        driver.execute_script("arguments[0].scrollIntoView();", total_button)
        action.move_to_element(share_button)

        WebDriverWait(driver, 5)
        export_button_xpath = '//button[text()[contains(., "Get table as CSV (for Excel)")]]'
        export_button = driver.find_element_by_xpath(export_button_xpath)
        action.move_to_element(export_button)
        driver.execute_script("arguments[0].click();", export_button)

        data += driver.find_element_by_id('csv_totals_stats').text + "\n"
    print(data)
    return data

def Team_Scrape():
    """
    Gets team total stats from years 1999 to 2019 

    Output: {string} of comma-separated values
    """
    data = ''
    
    for year in range(1999, 2020):

        url = 'https://www.basketball-reference.com/leagues/NBA_{}.html#all_misc_stats'.format(year)

        driver.get(url)

        WebDriverWait(driver, 5)

        header_elem_xpath = '//h2[text()[contains(., "Miscellaneous Stats")]]'
        header_elem = driver.find_element_by_xpath(header_elem_xpath)
        driver.execute_script("arguments[0].scrollIntoView();", header_elem)

        share_button_xpath = '//span[@data-label="Miscellaneous Stats"]//..//div//ul//li//span'
        share_button = driver.find_element_by_xpath(share_button_xpath)
        #driver.execute_script("arguments[0].scrollIntoView();", share_button)
        action.move_to_element(share_button)

        WebDriverWait(driver, 5)

        export_button_xpath = '//span[@data-label="Miscellaneous Stats"]//..//div//ul//li//div//button[text()[contains(., "Get table as CSV (for Excel)")]]'
        export_button = driver.find_element_by_xpath(export_button_xpath)
        action.move_to_element(export_button)
        driver.execute_script("arguments[0].click();", export_button)

        data += driver.find_element_by_id('csv_misc_stats').text + "\n"

    print(data)
    return data

def writeData():
    """ Takes string from ScrapeDate() function and adds it to a csv file 

    Input: ScrapeData() {string}

    Output: CSV file 
    """
    f = StringIO(Player_totals_Scrape())
    reader = csv.reader(f, delimiter=',')
    
    with open('1999-2019-Regular-PlayerStats-raw.csv', 'w') as file:
        for row in reader:
            writer = csv.writer(file)
            writer.writerow(row)

    f = StringIO(Team_Scrape())
    reader = csv.reader(f, delimiter=',')

    with open('1999-2019-Regular-TeamTotals-raw.csv', 'w') as file:
        for row in reader:
            writer = csv.writer(file)
            writer.writerow(row)

writeData()