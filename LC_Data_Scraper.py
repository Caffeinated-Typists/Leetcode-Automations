from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
import time
import parsedatetime as pdt
from datetime import datetime, timedelta
import json
import os

#date time parser object
cal = pdt.Calendar()

# initial configuration
DRIVER_PATH:str = os.path.abspath(r"C:\Users\dell\Desktop\Projects\Leetcode-Automations\msedgedriver")
EDGE_PATH:str = os.path.abspath(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge")
driverService = Service(DRIVER_PATH)


OPTION = Options()
OPTION.binary_location = EDGE_PATH
OPTION.add_argument("--headless")

browser = webdriver.Edge(service=driverService, options=OPTION)




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
        
        # making sure that 
        datetime_obj = cal.parseDT(Child[1].text)[0]
        cutoff = timedelta(hours=1)
        if (datetime.now() - datetime_obj < cutoff):
            if Child[0].text:
                rval.append(Child[0].text)
    return rval




if __name__ == "__main__":
    print(get_questions("zubaida"))
    # print(get_questions("Anirudh-S-Kumar"))
    browser.quit()
