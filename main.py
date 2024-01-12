from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

from datetime import datetime, timedelta
import time
import os

# -------- MODIFY VALUES HERE --------

# modify this path to point to where you put the chromedriver file
# if chromedriver is in the same folder as this file, use './chromedriver'
CHROMEDRIVER_PATH = './chromedriver'

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
QUERY_LOAD = 15

# if queries get rate limited, incease this to add delays between queries
QUERY_DELAY = 0


# -------- DO NOT TOUCH BELOW CODE --------


# ---- CREATING DRIVER ----
# create driver
service = Service(executable_path=CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service)
driver.implicitly_wait(QUERY_LOAD)


# ---- NAVIGATING TO SITE ----
# go to site
driver.get('https://wonder.cdc.gov/mcd-icd10.html')
# click "I agree" button
agree_button = driver.find_element(By.NAME, 'action-I Agree')
agree_button.click()


# ---- LOOPING THROUGH QUERIES ----
for i, query in enumerate(query_list):
    [age_group_type,
    age_group,
    gender,
    hispanic_origin,
    race,
    years,
    injury_intent,
    injury_mechanism,
    filename]          = query


    # ---- FILLING OUT FORM ----
    # -- 1. Organize table layout --
    # group results by state
    group_by = Select(driver.find_element(By.ID, 'SB_1'))
    group_by.select_by_visible_text('State')

    # -- 2. Select location --
    # leave at default settings

    # -- 3. Select demographics --
    # select age group type
    if age_group_type.lower() in 'ten-year age groups':
        agt_val = 'D77.V5'
    elif age_group_type.lower() in 'five-year age groups':
        agt_val = 'D77.V51'
    elif age_group_type.lower() in 'single-year ages':
        agt_val = 'D77.V52'
    elif age_group_type.lower() in 'infant age groups':
        agt_val = 'D77.V6'
    else:
        print(f'Invalid age group type: {age_group_type}')
    select_agt = driver.find_element(By.XPATH, f"//input[@value='{agt_val}']")
    select_agt.click()
    # select age group
    ag_id = 'S' + agt_val
    age_group_options = Select(driver.find_element(By.XPATH, f"//select[@id='{ag_id}']"))
    age_group_options.deselect_all()
    ago = age_group_options.options
    for option in ago:
        if age_group.lower() in option.text.lower():
            option.click()
    # select gender
    gender_options = Select(driver.find_element(By.XPATH, "//select[@id='SD77.V7']"))
    gender_options.deselect_all()
    go = gender_options.options
    for option in go:
        if gender.lower() in option.text.lower():
            option.click()
    # select hispanic origin
    hispanic_options = Select(driver.find_element(By.XPATH, "//select[@id='SD77.V17']"))
    hispanic_options.deselect_all()
    ho = hispanic_options.options
    for option in ho:
        if hispanic_origin.lower() in option.text.lower():
            option.click()
    # select race
    race_options = Select(driver.find_element(By.XPATH, "//select[@id='SD77.V8']"))
    race_options.deselect_all()
    ro = race_options.options
    for option in ro:
        if race.lower() in option.text.lower():
            option.click()

    # -- 4. Select year and month --
    year_options = Select(driver.find_element(By.XPATH, "//select[@id='codes-D77.V1']"))
    year_options.deselect_all()
    yo = year_options.options
    if years.lower() in 'all years':
        for option in yo:
            if 'All' in option.text:
                option.click()
    elif '-' in years:
        [start, end] = years.replace(' ', '').split('-')
        found_start = False
        for option in yo:
            if start in option.text:
                option.click()
                found_start = True
            elif end in option.text:
                option.click()
                break
            elif found_start:
                option.click()
    else:
        for option in yo:
            if years in option.text:
                option.click()
    
    # -- 5. Select weekday, autopsy and place of death --
    # leave at default settings

    # -- 6. Select underlying cause of death --
    # select Injury Intent and Mechanism
    icd_code = driver.find_element(By.ID, 'RO_ucdD77.V22')
    icd_code.click()
    # select Injury Intent
    intent_options = Select(driver.find_element(By.XPATH, "//select[@id='SD77.V22']"))
    intent_options.deselect_all()
    io = intent_options.options
    for option in io:
        if injury_intent.lower() in option.text.lower():
            option.click()
    # select Injury Mechanism
    mechanism_options = Select(driver.find_element(By.XPATH, "//select[@id='SD77.V23']"))
    mechanism_options.deselect_all()
    mo = mechanism_options.options
    for option in mo:
        if injury_mechanism.lower() in option.text.lower():
            option.click()

    # -- 7. Select multiple cause of death --
    # leave at default settings

    # -- 8. Other options --
    # deselect Show Totals
    show_totals = driver.find_element(By.ID, 'CO_show_totals')
    if show_totals.is_selected():
        show_totals.click()
    # select Show Suppressed Values
    show_suppressed = driver.find_element(By.ID, 'CO_show_suppressed')
    if not show_suppressed.is_selected():
        show_suppressed.click()

    # -- Send --
    send_button = driver.find_element(By.XPATH, "//div[@class='footer-buttons']/input[@name='action-Send']")
    send_button.click()

    # -- Export --
    export_button = driver.find_element(By.XPATH, "//input[@name='action-Export']")
    export_button.click()


    # ---- RENAMING DOWNLOAD ----
    time.sleep(3)
    newest_file = max([f for f in os.listdir(DOWNLOAD_DIR)], key=lambda xa : os.path.getctime(os.path.join(DOWNLOAD_DIR, xa)))
    time_waited = 0
    while True:
        if time_waited > QUERY_LOAD:
            print(f'Could not rename file {newest_file}')
            break
        elif '.part' in newest_file or '.cr' in newest_file:
            time.sleep(0.5)
            time_waited =+ 0.5
        else: 
            os.rename(os.path.join(DOWNLOAD_DIR, newest_file), f'{os.path.join(DOWNLOAD_DIR, filename)}.txt')
            break


    # ---- DELAYING BEFORE NEXT QUERY ----
    time.sleep(QUERY_DELAY)


    # ---- OPENING A NEW FORM ----
    request_form_tab = driver.find_element(By.XPATH, "//input[@name='tab-request']")
    request_form_tab.click()


# ---- CLOSING BROWSER ----
time.sleep(3)
driver.close()