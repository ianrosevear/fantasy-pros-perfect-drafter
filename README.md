# Requirements
- Google Chrome
- Python 3
# Setup
- Clone this project
  - `git clone https://github.com/ianrosevear/cdc-query-tool cdc-query-tool`
  - `cd cdc-query-tool`
- Create virtual environment
  - `python3 -m venv venv`
- Activate virtual environment (remember to deactivate when you are done)
  - `source venv/bin/activate` (Mac/Linux)
  - `venv\Scripts\activate` (Windows)
- Install Selenium (this will only install Selenium into your virtual environment, so it won't affect anything else)
  - `pip3 install selenium`
- Download chrome webdriver
  - Older Chrome versions: https://chromedriver.chromium.org/downloads
  - Newer Chrome versions: https://googlechromelabs.github.io/chrome-for-testing/
  - Place the downloaded `chromedriver` file into your workspace folder (it will be called `chromedriver.exe` on Windows)
- Remove chromedriver from Mac quarantine (this should not require admin access)
  - `xattr -d com.apple.quarantine chromedriver`
- Deactivate virtual environment
  - `deactivate`

# Usage
- Navigate terminal to workspace folder
  - `cd cdc-query-tool`
- Activate virtual environment (remember to deactivate when you are done)
  - `source venv/bin/activate`
  - `venv\Scripts\activate` (Windows)
- Add rosters to `rosters.py` as shown in the examples
- Modify values in the "MODIFY VALUES HERE" section at the top of `main.py` as needed
- Run the tool
  - `python3 main.py`
- Deactivate virtual environment
  - `deactivate`
