from pprint import pprint
import Sheets_API_Interface as Sheets
import time

IDENTIFYING_CHARACTER:str = "✔"
Tally = Sheets.sheet[2]

def clear_and_tally() -> None:
    """Takes the tally of all individuals and clears the sheet for the next week"""
    # making the tally for this week
    week_number = len(Tally.col_values(1)[1:]) + 1
    Tally.update(Sheets.A1_notation(1, week_number+1), f"Week {week_number}")
    for i in range(2, 11):
        records = Sheets.weeklyChart.col_values(i)
        print(records)
        Tally.update(Sheets.A1_notation(i, week_number + 1), sum([1 for record in records if record == IDENTIFYING_CHARACTER]))

    # clearing the sheet for the next week
    Sheets.weeklyChart.delete_rows(2, 100)

if __name__ == "__main__":
    clear_and_tally()
    with open("resetTallyLog.txt", "a") as f:
        f.write(f"Last run at {time.ctime()}\n")
