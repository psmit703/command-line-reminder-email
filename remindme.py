import sys
import re
from datetime import datetime as dt
import json
import random

if len(sys.argv) == 1:
    print("Invalid command usage\nPlease use \"remindme help\" for usage information")
    sys.exit(1)

if sys.argv[1] == "help":
    print("Usage:")
    print("\tremindme add -d <date> -s <subject> -m <message>")
    print("\tremindme remove <id>")
    print("\tremindme list [--all]")
    print("\tremindme help")
    print("")
    print("The date should be in the format YYYY-MM-DD or YYYY-MM, from the ISO 8601 standard")
    print("Dates without a day field provided will be interpreted as the first day of the month")
    print("The subject and message fields should not be empty")
    print("The --all flag can be used with the list command to see all reminders, including those that have already been completed")
    print("Reminders will be emailed nightly at midnight server time")
    print("")

elif sys.argv[1] == "remove":
    if len(sys.argv) < 3:
        print("Usage: remindme remove <id>\nTo see a list of reminders and their IDs, use \"remindme list\" or \"remindme list --all\"")
        sys.exit(1)

    with open("reminders.json", "r") as f:
        currData = json.load(f)

    try:
        idToRemove = int(sys.argv[2])
    except ValueError:
        print("Invalid ID provided\nPlease provide a valid integer ID")
        sys.exit(1)

    if idToRemove not in [x["id"] for x in currData["reminders"]]:
        print(f"No reminder with ID {idToRemove} found")
        sys.exit(0)

    currData["reminders"] = [
        x for x in currData["reminders"] if x["id"] != idToRemove]

    with open("reminders.json", "w") as f:
        json.dump(currData, f)

    print("Reminder with ID " + str(idToRemove) +
          " has been successfully removed")

elif sys.argv[1] == "list":
    with open("reminders.json", "r") as f:
        currData = json.load(f)

    if len(currData["reminders"]) == 0:
        print("No reminders found")
        sys.exit(0)

    if len(sys.argv) > 2 and sys.argv[2] == "--all":
        print("There are " +
              str(len(currData["reminders"])) + " total reminders:\n")
        for reminder in currData["reminders"]:
            print("\tRandom Unique ID: " + str(reminder["id"]) + "\n\tDate: " + reminder["date"] + "\n\tSubject: " +
                  reminder["subject"] + "\n\tMessage: " + reminder["message"] + "\n\tAlready Completed: " + str(reminder["completed"]) + "\n")
    else:
        print("There are currently " +
              str(len([x for x in currData["reminders"] if not x["completed"]])) + " reminders that have not yet been run:\n")
        for reminder in currData["reminders"]:
            if not reminder["completed"]:
                print("\tRandom Unique ID: " + str(reminder["id"]) + "\n\tDate: " + reminder["date"] + "\n\tSubject: " +
                      reminder["subject"] + "\n\tMessage: " + reminder["message"] + "\n\tAlready Completed: " + str(reminder["completed"]) + "\n")

elif sys.argv[1] == "add":
    if "-d" not in sys.argv or "-s" not in sys.argv or "-m" not in sys.argv:
        print("Usage: remindme add -d <date> -s <subject> -m <message>")
        sys.exit(1)

    if max(sys.argv.index("-d"), sys.argv.index("-s"), sys.argv.index("-m")) == len(sys.argv) - 1:
        print("Usage: remindme add -d <date> -s <subject> -m <message>")
        sys.exit(1)

    date = sys.argv[sys.argv.index("-d") + 1]
    subject = sys.argv[sys.argv.index("-s") + 1]
    message = sys.argv[sys.argv.index("-m") + 1]

    dateMatches = re.match(r"^(\d{4})-(\d{2})-(\d{2})$",
                           date) or re.match(r"^(\d{4})-(\d{2})$", date)

    if dateMatches is None:
        raise ValueError("Invalid date format\nPlease use YYYY-MM-DD or YYYY-MM, from the ISO 8601 standard\n"
                         + "Dates without a day field provided will be interpreted as the first day of the month\n"
                         + "Data provided by user: " + date)

    if len(dateMatches.groups()) == 2:
        myDate = "".join(list(dateMatches.groups())) + "01"

    else:  # len(dateMatches.groups()) == 3
        myDate = "".join(list(dateMatches.groups()))

    try:
        dt(year=int(myDate[0:4]), month=int(myDate[4:6]), day=int(myDate[6:8]))
    except ValueError as e:
        raise ValueError("Invalid date\nError: " + str(e) +
                         "\nData provided by user: " + date)

    myDate = myDate[0:4] + "-" + myDate[4:6] + "-" + myDate[6:8]

    if len(subject) == 0:
        raise ValueError("Subject cannot be empty")

    if len(message) == 0:
        raise ValueError("Message cannot be empty")

    dct = {"date": myDate, "subject": subject, "message": message}

    with open("reminders.json", "r") as f:
        currData = json.load(f)

    currIds = [x["id"] for x in currData["reminders"]]
    thisId = random.choice([x for x in range(1, 100000) if x not in currIds])

    dct["id"] = thisId
    dct["completed"] = False
    currData["reminders"].append(dct)

    with open("reminders.json", "w") as f:
        json.dump(currData, f)

    print("The following reminder has been successfully added:\n\n"
          + "\tRandom Unqiue ID: " + str(thisId) + "\n\tDate: " + myDate + "\n\tSubject: " + subject + "\n\tMessage: " + message + "\n\tAlready Completed: False" + "\n")

else:
    print("Invalid command usage\nPlease use \"remindme help\" for usage information")
    sys.exit(1)
