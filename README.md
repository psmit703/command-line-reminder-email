# CLI Reminder Emails

## Description

This tool is designed to facilitate a programmatic way of creating and emailing reminders. I created it to use as part of a remote Ubuntu 22.04 instance in order to better keep track of bandwidth usage, renewing access tokens, and other important things that may be needed as part of developing programs. It requires a small amount of configuration in order to properly set up, but should be a reliable way of sending reminders via email so that they are external to the remote development server.

&copy; 2024 [Pete Smith](https://www.psmit.dev/). This tool is licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).

## Usage

The tool has four commands:
* `remindme add -d <date> -s <subject> -m <message>`
* `remindme remove <id>`
* `remindme list [--all]`
* `remindme help`

Firstly, please note that `remindme` being used as a command is dependent on the user's configuration, described later. Similar ways of using the tool may be `remindme.py ...`, `python remindme.py ...`, `python3 remindme.py`, etc.

`add` adds a new reminder to the tool's records. `<date>` should be inputted as either YYYY-MM-DD or YYYY-MM, which are both in the ISO 8601 standard. If no day is provided, it will be interpreted as the first of the month. It is the user's responsibility to provide a date in the future, otherwise the reminder will never be sent. `<subject>` defines what the subject of the email will be, and `<message>` defines what the body of the email will be. Neither may be empty strings. Once added, each reminder will be assigned a random integer from 0 inclusive to 99,999 inclusive as its ID.

`remove` removes a reminder from the tool's records. This may be used either on reminders which have already been sent as an email or reminders which have not yet been sent as an email. `<id>` should be the reminder's ID. (described in the `add` section above and in the `list` section below)

`list` shows a list of the data for each reminder that has not yet been sent as an email, including its ID. Including the `--all` flag at the end will displays all reminders, including those that have already been sent as an email.

`help` displays each of the four possible commands, including `help`.

## Configuration

Configuring the script to work as desired will depend to an extent on user preference. My goal was to make it callable in a similar manner to a command like `mkdir` on the command line. A helpful guide to set this up is available here:

<https://stackoverflow.com/q/6163087>

If desired, the script can simply be called manually instead by using its full (or relative) directory path as an argument to the Python interpreter.

Regarding `mailer.py`, the script depends on vnStat, Postfix, and Mailutils already being installed. (to note, Postfix is probably interchangeable with similar mail transport agents, however Postfix is the only one I have tested with) The script is intended to be used as the target of a cron job, however this must be set up by the user or may be changed at the user's preference. Depending on the time of day selected in the cron job, the subject of the bandwidth report in `mailer.py` might need to be changed to something other than "nightly".

Calls to open() in both `remindme.py` and `mailer.py` may need to be changed depending on the user's configuration. The full/relative directories of `reminders.json` and `config.json` in the open() calls of both scripts should be changed accordingly so that the scripts can access the files.

Lastly, `config.json` defines various parameters that `mailer.py` uses. It has four fields:
* `"deliverTo"` should be assigned a string, which is the intended recipient of the reminder emails
* `"sendFrom"` should be assigned a string, which is the sender that will be listed on the reminder emails
* `"rateLimitTimer"` should be assigned an integer, which is the number of seconds that the `mailer.py` will wait in between sending reminder emails, in order to avoid issues with rate limits
* `"server"` should be assigned a string, which should be the name of the server that will be displayed at the end of the subject line of reminder emails
