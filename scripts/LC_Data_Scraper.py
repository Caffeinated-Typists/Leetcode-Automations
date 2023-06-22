from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from datetime import datetime, timedelta
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
import selenium.common.exceptions
import time
import parsedatetime as pdt


TIME_DELTA_HOUR:int = 4
TIME_DELTA_DAY:int = 1
LOG_PATH:str = "./geckodriver.log"
EXE_PATH:str = "./geckodriver.exe"

cal = pdt.Calendar()
edge_options = EdgeOptions()
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
    edge_options.add_argument(option)

browser = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=edge_options)

# getting the questions done in the past 24 hours
def get_questions(username: str) -> list[str]:
    rval:list[str] = []
    
    url:str = f"https://leetcode.com/{username}/"
    browser.get(url)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

    try:
        Table = browser.find_element("xpath",
                                r'/html/body/div[1]/div/div[2]/div/div[2]/div[5]/div/div/div[2]')
    except selenium.common.exceptions.NoSuchElementException:
        Table = browser.find_element("xpath",
                                r'/html/body/div[1]/div/div[2]/div/div[2]/div[3]/div/div/div[2]')
    
    Containers = Table.find_elements("xpath", "*")

    for container in Containers:
        Child = (container.find_elements("xpath", "*")
                [0]).find_elements("xpath", "*")
        
        # making sure that the questions were done only in the last one hour
        datetime_obj = cal.parseDT(Child[1].text)[0]
        # A hack to make sure that the questions done at 11:50 PM on Sunday are not counted on Monday
        # if((datetime_obj.hour == 1) and (datetime_obj.minute == 0)):
        #     datetime_obj.hour = 2
        cutoff = min(timedelta(hours=TIME_DELTA_HOUR, days=TIME_DELTA_DAY), timedelta(days=datetime.now().weekday(), hours=datetime.now().hour, minutes=datetime.now().minute, seconds=datetime.now().second, microseconds=datetime.now().microsecond))
        if (datetime.now() - datetime_obj < cutoff):
            if Child[0].text:
                rval.append(Child[0].text)

    return rval

if __name__ == "__main__":
    print(get_questions("aakarsh_11235"))
    # print(get_questions("vartika_7"))
    browser.quit()
