import json
import traceback
import sys
import logging
import time
import typing
import gspread 
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import LC_Data_Scraper


logging.basicConfig(filename="Sheets_API_Interface.log", level=logging.DEBUG)
logger = logging.getLogger(__name__)

GREEN_CELL:dict[str:dict[str:float]] = {"backgroundColor": 
                                            {"red": 0.0, 
                                            "green": 1.0, 
                                            "blue": 0.0},
                                        "horizontalAlignment": "CENTER",
                                        }
USERNAME_TO_INDEX:dict[str:int] = json.load(open("usernames.json", "r"))




#getting and loading the sheet
SCOPE = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("creds.json", SCOPE)
client = gspread.authorize(credentials)

# opening the entire document
sheet = client.open("LC Automated").worksheets()

weeklyChart = sheet[0]  # Open the sheet for keeping track of questions each week
questionsTracking = sheet[1] # Sheet for keeping track of questions already done
data = weeklyChart.col_values(1)  # Get a list of all questions in this week

# list of all questions
All_questions = (questionsTracking.col_values(1)[1:])
# creating hashmap of the questions
Question_index = {}
for i in range(len(All_questions)):
    Question_index[All_questions[i]] = i + 2

def A1_notation(col:int, row:int) -> str:
    """Function to convert the index to A1 notation"""
    return f"{chr(col + 64)}{row}"


def add_to_sheet(username: str) -> None:
    """Function to add the questions done by the user to the sheet"""
    # get the questions done by the user
    questions = LC_Data_Scraper.get_questions(username)
    # add the questions to the sheet
    for question in questions:
        # check if the question is already present
        if question not in Question_index:
            # update the hashmap
            Question_index[question] = len(Question_index) + 2
            # add the question to the sheet
            weeklyChart.insert_row([question, "", "", "", "", "", "", "", "", ""], index=Question_index[question])

        # update the sheet
        weeklyChart.update(A1_notation(1, Question_index[question]), question)
        weeklyChart.update(A1_notation(USERNAME_TO_INDEX[username], Question_index[question]), "✔")
        weeklyChart.format(A1_notation(USERNAME_TO_INDEX[username], Question_index[question]), GREEN_CELL)
        # time.sleep(5)

# adding weekly questions
def add_weekly_questions() -> None:
    for i in USERNAME_TO_INDEX:
        add_to_sheet(i)

    # adding to the questions tracking sheet
    for index, record in enumerate(Question_index):
        if record not in All_questions:
            questionsTracking.insert_row([record], index=len(All_questions) + 2)
            All_questions.insert(0, record)
    LC_Data_Scraper.browser.quit()

if __name__ == "__main__":
    try:
        add_weekly_questions()
    except Exception as e:
        logger.exception(e)
    logger.info("\nLast Run at %s \n --------------------------------------- \n", time.ctime())