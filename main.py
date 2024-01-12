from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import passwords

from datetime import datetime, timedelta
import time
import os

# -------- MODIFY VALUES HERE --------

# modify this path to point to where you put the chromedriver file
# if chromedriver is in the same folder as this file, use './chromedriver'
CHROMEDRIVER_PATH = './chromedriver.exe'

# modify this path to point to where your downloads folder is
# use an absolute path, e.g. `/Users/username/Downloads`
DOWNLOAD_DIR = '/Users/ianrosevear/Downloads'

# modify this list with arrays containing the options you want to export
# each element of query_list represents one query that will be exported
query_list = [
    # definition:
    # [age_group_type, 
    #  age-group, 
    #  gender, 
    #  hispanic_origin, 
    #  race, 
    #  years,             # either a single year: '2004', a range: '2010-2015', or 'All Dates'
    #  injury_intent, 
    #  injury_mechanism,
    #  filename],         # what you want the file to be renamed to after it is downloaded

    # example arrays:
    # ['Ten-Year', 'All Ages', 'All Genders', 'All Origins', 'All Races', 'All Dates', 'All Causes of Death', 'All Causes of Death', 'all-of-everything'],
    # ['Infant', '< 1', 'Male', 'All Origins', 'All Races', '2010', 'Suicide', 'Firearm', '2010-black-infant-firearm-suicides'],
    # ['Five-Year', '10-14', 'Female', 'Not Hispanic', 'Black', '2011-2020', 'Homicide', 'Firearm', 'test-file-a']
    
    # -- YOUR ARRAYS HERE --

]

# maximum time the driver will wait for something to load, increase if poor connection
MAX_LOAD = 15

# if queries get rate limited, incease this to add delays between queries
QUERY_DELAY = 0

SITE_URL = 'https://draftwizard.fantasypros.com/football/mock-draft-simulator/perfect-draft/?userPos='
DRAFT_POSITION = 5

MAX_ATTEMPTS = 10

# -------- DO NOT TOUCH BELOW CODE --------


# ---- CREATING DRIVER ----
# create driver
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
service = Service(executable_path=CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)
#driver.implicitly_wait(MAX_LOAD)


# ---- NAVIGATING TO SITE ----
# go to site
site = f'{SITE_URL}{DRAFT_POSITION-1}'
driver.get(site)
driver.maximize_window()

# log in
username_field = driver.find_element(By.ID, 'username')
password_field = driver.find_element(By.ID, 'password')

username_field.send_keys(passwords.username)
password_field.send_keys(passwords.password)

submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
submit_button.click()

time.sleep(3)

# ---- ATTEMPTING TO DRAFT ----
player_list = passwords.draft_order.split('\n')
for i in range(MAX_ATTEMPTS):
    driver.refresh()
    print(f'This is attempt #{i+1}')

    # -- LOOP THROUGH PLAYERS --
    for j, player in enumerate(player_list):

        # LOOK FOR PLAYER
        try:
            # get search field
            search_field = driver.find_element(By.XPATH, '//input[@ng-model="playerSearchString"]')
            print('got search')

            # search for player
            search_field.clear()
            search_field.send_keys(player)
            print(f'searched for {player}')
            time.sleep(1)

            # get draft button
            draft_button = driver.find_element(By.XPATH, '//input[@class="rdr-search-results__draft-btn"]')
            # draft_button_locator = (By.XPATH, '//input[@class="rdr-search-results__draft-btn"]')
            # draft_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(draft_button_locator))

            # if draft button is disabled, go to next attempt
            if not draft_button.is_enabled():
                print(f'{player} has already been drafted, moving to next attempt')
                break

            # wait until our turn to draft
            my_turn = False
            while not my_turn:
                if driver.find_element(By.XPATH, '//div[@class="rdr-on-the-clock"]').text != '1:00':
                    my_turn = True

            # click draft button
            draft_button.click()
            print(f'clicked draft button for {player}')
            time.sleep(0.2)

        except Exception as e:
            print(f'An error occurred: {e}')
            print(f'Next attempt...')
            break

        # if we've drafted a full team, end program
        if j == len(player_list) - 1:
            print('completed team')
            driver.close()
            exit

driver.close()
exit    
