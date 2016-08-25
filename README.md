# OpenTeamStatus - an opensource StatusHero clone
OpenTeamStatus is built by [Threde](http://threde.com) for small teams like our
own. It was built out of a desire for a free and open source (thus guaranteed to
be free forever) clone of [StatusHero](http://statushero.com).

**NOTE: This is still BETA quality and under development, but we are using it
ourselves :smiley:**

```
mkvirtualenv --python=/usr/bin/python3 status
pip install -r requirements.txt
./manage.py migrate
./manage.py createsuperuser
./manage.py runserver
```

Avatars made with gravatar/robohash. Because robohash is awesome.

## Screenshot
![screenshot](.screenshot.png)

## Super-easy FREE Heroku deploy! :tada: :100:
OpenTeamStatus comes with a supervisor config for running gunicorn & celery as
from a single process. This is launched by the `Procfile` and the Celery worker
*automatically* detects that it's running on a heroku dyno and makes an HTTP
request to itself every 15 minutes to keep the dyno alive forever.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

## Configuration
Configuration is done through environment variables. Variables not prefixed
with `OPEN_TEAM_STATUS_` are
[Django settings](https://docs.djangoproject.com/en/1.9/ref/settings/). The
possible settings are:

 * `SECRET_KEY` - a Django secret key
 * `DEBUG`
 * `ALLOWED_HOSTS` - `:` delimited
 * `DATABASE_URL`
 * `TIME_ZONE` - note, you'll also want to set `TZ` if deploying to Heroku
 * `EMAIL_HOST`
 * `EMAIL_PORT`
 * `EMAIL_HOST_PASSWORD`
 * `EMAIL_HOST_USER`
 * `EMAIL_SUBJECT_PREFIX`
 * `EMAIL_USE_TLS`
 * `EMAIL_USE_SSL`
 * `EMAIL_SSL_CERTFILE`
 * `EMAIL_SSL_KEYFILE`
 * `EMAIL_TIMEOUT`
 * `DEFAULT_FROM_EMAIL`
 * `OPEN_TEAM_STATUS_NAME` - name to display in nav
 * `OPEN_TEAM_STATUS_LOGO` - a logo to display in the nav
 * `OPEN_TEAM_STATUS_PUBLIC` - if true, the checkin summary page visible with
   out logging in
 * `OPEN_TEAM_STATUS_REMINDER_HOUR` - hour of the day to send reminders,
    default: 9
 * `OPEN_TEAM_STATUS_REMINDER_MINUTE` - minute of the hour to send reminders,
    default: 0
 * `OPEN_TEAM_STATUS_REMINDER_DAYS` - days of the week to send reminders,
    default: mon,tue,wed,thu,fri
 * `OPEN_TEAM_STATUS_REMINDER_SUBJECT`
 * `OPEN_TEAM_STATUS_REMINDER_BODY`
 * `OPEN_TEAM_STATUS_REMINDER_TASK` - celery task to user for to send
   reminders with
 * `OPEN_TEAM_STATUS_REPORT_HOUR` - hour of the day to send reports,
    default: 12
 * `OPEN_TEAM_STATUS_REPORT_MINUTE` - minute of the hour to send reports,
    default: 0
 * `OPEN_TEAM_STATUS_REPORT_DAYS` - days of the week to send reports,
    default: mon,tue,wed,thu,fri
 * `OPEN_TEAM_STATUS_REPORT_SUBJECT`
 * `OPEN_TEAM_STATUS_REPORT_BODY`
 * `OPEN_TEAM_STATUS_REPORT_TASK` - celery task to user for to send
   reminders with
 * `OPEN_TEAM_STATUS_SLACK_WEBHOOK` - slack webhook to use when using
   slack for reminders and reports
 * `OPEN_TEAM_STATUS_REPORT_SLACK_CHANNEL` - slack channel to use when using
   slack for reports, default: `#general`
 * `OPEN_TEAM_STATUS_CHECKIN_TASK` - celery task to user for to send
   checkins with
 * `OPEN_TEAM_STATUS_CHECKIN_SLACK_CHANNEL` - slack channel to use when using
   slack for delivering checkins, default: `#general`
 * `OPEN_TEAM_STATUS_CHECKIN_BODY`: checkin message body


## Pluggable reminder backend!
OpenTeamStatus features a pluggable system for sending reminders. It currently
supports email and can be configured using the standard Django email config
variables.

The backend is configured via the `OPEN_TEAM_STATUS_REMINDER_TASK`,
`OPEN_TEAM_STATUS_REPORT_TASK`, and `OPEN_TEAM_STATUS_CHECKIN_TASK`
environment variables.
variable. The available reminder backends are:
 * Email - `checkins.tasks.email_reminder`
 * Slack - `checkins.tasks.slack_reminder` - **NOTE**: slack usernames must
   must match OpenTeamStatus usernames.
The available Report backends are:
 * Email - `checkins.tasks.email_report`
 * Slack - `checkins.tasks.slack_report`
The available Check backends are:
 * Slack - `checkins.tasks.slack_checkin`


## Docker!
This project's repo automatically builds a docker image and stores it in a
registry(isn't gitlab neat!)
```
docker pull registry.gitlab.com/threde/open-team-status
docker run -it --rm -v $PWD/db.sqlite3:/opt/openteamstatus/db.sqlite3:z registry.gitlab.com/threde/open-team-status ./manage.py migrate
docker run -it --rm -v $PWD/db.sqlite3:/opt/openteamstatus/db.sqlite3:z registry.gitlab.com/threde/open-team-status ./manage.py createsuperuser
docker run -it --rm -e ALLOWED_HOSTS=localhost -p 8000:80 -v $PWD/db.sqlite3:/opt/openteamstatus/db.sqlite3:z registry.gitlab.com/threde/open-team-status
```
