# -------- MODIFY VALUES HERE --------

# position to draft from, from 1 to 12
DRAFT_POSITION = 7

# which roster to use, first roster is 0, second is 1, etc.
ROSTER_NUM = 1

# maximum attempts per roster (my version of chromedriver seems to run out of memory around 1600 attempts)
MAX_ATTEMPTS = 10000

# modify this path to point to where you put the chromedriver file
# if chromedriver is in the same folder as this file, use './chromedriver' ('./chromedriver.exe' on windows)
CHROMEDRIVER_PATH = './chromedriver.exe'

# site url
SITE_URL = 'https://draftwizard.fantasypros.com/football/mock-draft-simulator/perfect-draft/?userPos='