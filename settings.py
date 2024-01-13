# -------- MODIFY VALUES HERE --------

# position to draft from, from 1 to 12
DRAFT_POSITION = 7

# which roster to use, first roster is 0, second is 1, etc.
ROSTER_NUM = 1

# maximum attempts per roster
MAX_ATTEMPTS = 10000

# maximum attempts between driver restarts (my version of chromedriver seems to run out of memory around 1600 attempts)
RESTART_THRESHOLD = 1300

# how many drafts occur between stats displays
DRAFTS_BETWEEN_STATS = 50

# modify this path to point to where you put the chromedriver file
# if chromedriver is in the same folder as this file, use './chromedriver' ('./chromedriver.exe' on windows)
CHROMEDRIVER_PATH = './chromedriver.exe'

# site url
SITE_URL = 'https://draftwizard.fantasypros.com/football/mock-draft-simulator/perfect-draft/?userPos='