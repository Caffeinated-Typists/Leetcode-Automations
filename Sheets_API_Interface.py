import json, os
import traceback
import sys
import logging
import time
import typing
import gspread 
from oauth2client.service_account import ServiceAccountCredentials
import LC_Data_Scraper

WEEKLY_SHEET_ROW_OFFSET:int = 2
ALL_SHEET_ROW_OFFSET:int = 1

logging.basicConfig(filename="logs/Sheets_API_Interface.log", level=logging.WARNING)
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
# credentials = ServiceAccountCredentials.from_json_keyfile_name("creds.json", SCOPE)
env_creds = eval(os.environ["GOOGLE_API_CRED"])
# f = open(r'C:\Users\dell\Desktop\Projects\Leetcode-Automations\creds.json', 'r')
# env_creds = json.load(f)
credentials = ServiceAccountCredentials.from_json_keyfile_dict(env_creds, SCOPE)
client = gspread.authorize(credentials)

# opening the entire document
sheet = client.open("LC Automated").worksheets()

weeklyChart = sheet[0]  # Open the sheet for keeping track of questions each week
questionsTracking = sheet[1] # Sheet for keeping track of questions already done
weeklyQues = weeklyChart.col_values(1)[ALL_SHEET_ROW_OFFSET::]  # Get a list of all questions in this week

# list of all questions
All_questions = questionsTracking.col_values(1)[WEEKLY_SHEET_ROW_OFFSET::]
# creating hashmap of the questions
Question_index = {}
for i in range(len(All_questions)):
    Question_index[All_questions[i]] = i + ALL_SHEET_ROW_OFFSET
# Creating hashmap for questions of this week
weekly_question_index = {}
for i in range(len(weeklyQues)):
    weekly_question_index[weeklyQues[i]] = i + WEEKLY_SHEET_ROW_OFFSET

def A1_notation(col:int, row:int) -> str:
    """Function to convert the index to A1 notation"""
    return f"{chr(col + 64)}{row}"


def add_to_sheet(username: str) -> None:
    """Function to add the questions done by the user to the sheet"""
    # get the questions done by the user
    questions:list[str] = LC_Data_Scraper.get_questions(username)
    # add the questions to the sheet
    for question in questions:
        # check if the question is already present
        if question not in Question_index:
            # update the hashmap
            Question_index[question] = len(Question_index) + ALL_SHEET_ROW_OFFSET
            # adding to the questions tracking sheet
            questionsTracking.insert_row([question], index=Question_index[question])
            All_questions.insert(len(All_questions), question)

        if question not in weekly_question_index:
            weekly_question_index[question] = len(weekly_question_index) + WEEKLY_SHEET_ROW_OFFSET
            # add the question to the weekly sheet
            weeklyChart.insert_row([question, "", "", "", "", "", "", "", "", "", ""], index=weekly_question_index[question])
            weeklyQues.insert(len(weeklyQues), question)

        # update the sheet
        weeklyChart.update(A1_notation(USERNAME_TO_INDEX[username], weekly_question_index[question]), "✔")
        weeklyChart.format(A1_notation(USERNAME_TO_INDEX[username], weekly_question_index[question]), GREEN_CELL)
        # time.sleep(5)

# adding weekly questions
def add_weekly_questions() -> None:
    for i in USERNAME_TO_INDEX:
        add_to_sheet(i)
        # Sleep to not blow up API write rate limit
        time.sleep(0.3)
        
    LC_Data_Scraper.browser.quit()

if __name__ == "__main__":
    try:
        add_weekly_questions()
    except Exception as e:
        logger.exception(e)
    logger.info("\nLast Run at %s \n --------------------------------------- \n", time.ctime())
