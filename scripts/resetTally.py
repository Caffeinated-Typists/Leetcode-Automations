from pprint import pprint
from datetime import datetime
import time
import pytz
import logging
import Sheets_API_Interface as Sheets

NUMBER_OF_PEOPLE:int = len(Sheets.USERNAME_TO_INDEX)

logging.basicConfig(filename="../logs/resetTally.log", level=logging.INFO)
logger = logging.getLogger(__name__)

IDENTIFYING_CHARACTER:str = "✔"
Tally = Sheets.sheet[2]
WeeklyChart = Sheets.sheet[0]

def clear_and_tally() -> None:
    """Takes the tally of all individuals and clears the sheet for the next week"""

    # making the tally for this week
    week_number = len(Tally.col_values(1)[1:]) + 1
    Tally.update(Sheets.A1_notation(1, week_number+1), f"Week {week_number}")
    for i in range(2, NUMBER_OF_PEOPLE+2):
        records = WeeklyChart.col_values(i)
        logging.info((records))
        Tally.update(Sheets.A1_notation(i, week_number + 1), records[2])

    # clearing the sheet for the next week
    for i in range(2, NUMBER_OF_PEOPLE+2):
        WeeklyChart.update(Sheets.A1_notation(i, 2), 0)
    WeeklyChart.delete_rows(3, 1000)

if __name__ == "__main__":
    try:
        clear_and_tally()
    except Exception as e:
        logger.exception(e)

    logger.info("\nLast Run at %s \n --------------------------------------- \n", (datetime.now(pytz.timezone('Asia/Kolkata'))).strftime("%a %b %d %H:%M:%S %Y"))
