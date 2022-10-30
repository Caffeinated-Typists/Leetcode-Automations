import os, sys
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import parsedatetime as pdt
from datetime import datetime, timedelta

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

    Table = browser.find_element("xpath",
                                r'/html/body/div[1]/div/div/div/div[2]/div[3]/div/div/div[2]')
    Containers = Table.find_elements("xpath", "*")

    for container in Containers:
        Child = (container.find_elements("xpath", "*")
                [0]).find_elements("xpath", "*")
        
        # making sure that the questions were done only in the last one hour
        datetime_obj = cal.parseDT(Child[1].text)[0]
        cutoff = timedelta(hours=1)
        if (datetime.now() - datetime_obj < cutoff):
            if Child[0].text:
                rval.append(Child[0].text)
    return rval




if __name__ == "__main__":
    print(get_questions("aakarsh_11235"))
    browser.quit()