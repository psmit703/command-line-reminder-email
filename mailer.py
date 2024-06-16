import os
import json
import time

config = json.load(open("config.json"))
deliverTo = config["deliverTo"]
sendFrom = config["sendFrom"]
rateLimitTimer = config["rateLimitTimer"]
server = config["server"]

# start with bandwidth report
report = os.popen("vnstat").read()
mail = os.popen(
    f"""echo "{report}" | mail -s "Nightly Bandwidth Report | {server}" -a "From: {sendFrom}" {deliverTo}""")

reminders = json.load(open("reminders.json"))["reminders"]

for each in reminders:
    # avoid potential rate limiting with email relay
    time.sleep(rateLimitTimer)

    if each["completed"]:
        continue

    if time.strftime("%Y-%m-%d") == each["date"]:
        mail = os.popen(
            f"""echo "{each['message']}" | mail -s "{each['subject']} | {server}" -a "From: {sendFrom}" {deliverTo}""")

        each["completed"] = True

json.dump({"reminders": reminders}, open("reminders.json", "w"))
