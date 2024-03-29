from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import passwords
import rosters
from settings import *

from datetime import datetime, timedelta
import time
import os



def create_driver():
    options = webdriver.ChromeOptions()

    options.add_argument("start-maximized") # https://stackoverflow.com/a/26283818/1689770
    options.add_argument("enable-automation") # https://stackoverflow.com/a/43840128/1689770
    # options.add_argument("--headless") # only if you are ACTUALLY running headless
    options.add_argument("--no-sandbox") # https://stackoverflow.com/a/50725918/1689770
    options.add_argument("--disable-dev-shm-usage") #https://stackoverflow.com/a/50725918/1689770
    options.add_argument("--disable-browser-side-navigation") # https://stackoverflow.com/a/49123152/1689770
    options.add_argument("--disable-gpu") # https://stackoverflow.com/questions/51959986/how-to-solve-selenium-chromedriver-timed-out-receiving-message-from-renderer-exc

    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("--mute-audio")
    service = Service(executable_path=CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    #driver.implicitly_wait(MAX_LOAD)

    return driver

def login(driver):
    # go to site
    site = f'{SITE_URL}{DRAFT_POSITION-1}'
    driver.get(site)
    #driver.maximize_window()

    # log in
    time.sleep(1)
    username_field = driver.find_element(By.ID, 'username')
    password_field = driver.find_element(By.ID, 'password')
    time.sleep(1)

    username_field.send_keys(passwords.username)
    time.sleep(1.1)
    password_field.send_keys(passwords.password)

    # submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    # submit_button.click()

    input('Please login, then press any key to continue...')

    driver.get(site)
    time.sleep(1)

# ---- CREATING DRIVER ----
driver = create_driver()

# ---- NAVIGATING TO SITE ----
login(driver)

# ---- ATTEMPTING TO DRAFT ----

# -- SET UP STATS --
player_list = rosters.draft_order[ROSTER_NUM].split('\n')

times_drafted = dict(zip(player_list, [0] * len(player_list)))

# -- RUN DRAFTS --
for i in range(MAX_ATTEMPTS):

    # -- RESTART DRIVER AT THRESHOLD --
    if i != 0 and (MAX_ATTEMPTS - 1 - i) % RESTART_THRESHOLD == 0:
        driver.close()
        time.sleep(0.5)
        driver = create_driver()
        login(driver)

    # refresh between attempts
    try_count = 0
    max_try_count = 5
    while(try_count <= max_try_count):
        try:
            try_count += 1
            driver.refresh()
            break
        except Exception as e:
            print('\nERROR: Could not refresh. Retrying...')
            time.sleep(0.1)

    # print stats every 100 attempts
    if (i % 100 == 0) & (i > 0):
        print(f'\n\nStats:\nDrafting from: {DRAFT_POSITION}\nDrafts: {i}\n\n{times_drafted}\n\n')

    print(f'\nDraft #{i+1}')

    # -- LOOP THROUGH PLAYERS --
    for j, player in enumerate(player_list):

        # LOOK FOR PLAYER
        try:
            # get search field
            try_count = 0
            max_try_count = 20
            while(try_count <= max_try_count):
                try:
                    try_count += 1
                    search_field = driver.find_element(By.XPATH, '//input[@ng-model="playerSearchString"]')
                    break
                except Exception as e:
                    time.sleep(0.1)
            
            # search for player
            search_field.clear()
            search_field.send_keys(player)
            print(f'Searching for {player}...')

            # get draft button
            try_count = 0
            max_try_count = 20
            while(try_count <= max_try_count):
                try:
                    try_count += 1
                    draft_button = driver.find_element(By.XPATH, '//input[@class="rdr-search-results__draft-btn"]')
                    break
                except Exception as e:
                    time.sleep(0.1)

            # if player has already been drafted, go to next attempt
            if not draft_button.is_enabled():
                print(f'{player} has already been drafted, moving to next attempt')
                break

            # wait until my turn to draft
            my_turn = False
            while not my_turn:
                if driver.find_element(By.XPATH, '//div[@class="rdr-on-the-clock"]').text != '1:00':
                    my_turn = True

            # click draft button
            draft_button.click()
            print(f'  Drafted {player}')
            times_drafted[player] = times_drafted[player] + 1

        except Exception as e:
            print(f'An error occurred: {e}')
            print(f'Next attempt...')
            break

        # if we've drafted a full team, end program
        if j == len(player_list) - 1:
            print('completed team')
            print(f'Stats:\nDrafting from: {DRAFT_POSITION}\nDrafts: {i}\n\n{times_drafted}')
            input('press any key to close')
            driver.close()
            exit

driver.close()
print(f'\nStats:\n\nDrafting from: {DRAFT_POSITION}\n\nDrafts: {i+1}\n\n{times_drafted}')
exit    

