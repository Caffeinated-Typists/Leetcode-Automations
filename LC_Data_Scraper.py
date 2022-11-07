import os, sys
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import selenium.common.exceptions
import time
import parsedatetime as pdt
from datetime import datetime, timedelta

TIME_DELTA_HOUR:int = 5
TIME_DELTA_DAY:int = 6

cal = pdt.Calendar()
options = Options()
firefox_options = Options()
options = [
    "--headless",
    "--disable-gpu",
    "--window-size=1920,1200",
    "--ignore-certificate-errors",
    "--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage"
]

for option in options:
    firefox_options.add_argument(option)

browser = webdriver.Firefox(options=firefox_options)

# getting the questions done in the past 24 hours
def get_questions(username: str) -> list[str]:
    rval:list[str] = []
    
    url:str = f"https://leetcode.com/{username}/"
    browser.get(url)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

    try:
        Table = browser.find_element("xpath",
                                r'/html/body/div[1]/div/div/div/div[2]/div[5]/div/div/div[2]')
    except selenium.common.exceptions.NoSuchElementException:
        Table = browser.find_element("xpath",
                                r'/html/body/div[1]/div/div/div/div[2]/div[3]/div/div/div[2]')
    
    Containers = Table.find_elements("xpath", "*")

    for container in Containers:
        Child = (container.find_elements("xpath", "*")
                [0]).find_elements("xpath", "*")
        
        # making sure that the questions were done only in the last one hour
        datetime_obj = cal.parseDT(Child[1].text)[0]
        cutoff = timedelta(hours=TIME_DELTA_HOUR, days=TIME_DELTA_DAY)
        if (datetime.now() - datetime_obj < cutoff):
            if Child[0].text:
                rval.append(Child[0].text)
    return rval




if __name__ == "__main__":
    print(get_questions("aakarsh_11235"))
    print(get_questions("vartika_7"))
    browser.quit()
