# OpenTeamStatus - an opensource StatusHero clone
OpenTeamStatus is built by [Threde](http://threde.com) for small teams like our
own. It was built out of a desire for a free and open source (thus guaranteed to
be free forever) clone of [StatusHero](http://statushero.com).

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

## Super-easy FREE deploy! :tada: :100:
OpenTeamStatus comes with a supervisor config for running gunicorn & celery as
from a single process. This is launched by the `Procfile` and the Celery worker
*automatically* detects that it's running on a heroku dyno and makes an HTTP
request to itself every 15 minutes to keep the dyno alive forever.

## Configuration
Configuration is done through environment variables. Variables not prefixed
with `OPEN_TEAM_STATUS_` are
[Django settings](https://docs.djangoproject.com/en/1.9/ref/settings/). The
possible settings are:

 * `SECRET_KEY` - a Django secret key
 * `DEBUG`
 * `ALLOWED_HOSTS` - `:` delimited
 * `DATABASE_URL`
 * `TIME_ZONE`
 * `EMAIL_HOST'
 * `EMAIL_PORT'
 * `EMAIL_HOST_PASSWORD'
 * `EMAIL_HOST_USER'
 * `EMAIL_SUBJECT_PREFIX'
 * `EMAIL_USE_TLS'
 * `EMAIL_USE_SSL'
 * `EMAIL_SSL_CERTFILE'
 * `EMAIL_SSL_KEYFILE'
 * `EMAIL_TIMEOUT'
 * `DEFAULT_FROM_EMAIL`
 * `OPEN_TEAM_STATUS_NAME` - name to display in nav
 * `OPEN_TEAM_STATUS_LOGO` - a logo to display in the nav
 * `OPEN_TEAM_STATUS_REMINDER_HOUR` - hour of the day to send reminders,
    default: 9
 * `OPEN_TEAM_STATUS_REMINDER_DAYS` - days of the week to send reminders,
    default: mon,tue,wed,thu,fri
 * `OPEN_TEAM_STATUS_REMINDER_SUBJECT`
 * `OPEN_TEAM_STATUS_REMINDER_BODY`



## Docker!
There's a basic Dockerfile, here's a basic example of running it..
```
docker pull registry.gitlab.com/threde/open-team-status
docker run -it --rm -v $PWD/db.sqlite3:/opt/openteamstatus/db.sqlite3:z registry.gitlab.com/threde/open-team-status ./manage.py migrate
docker run -it --rm -v $PWD/db.sqlite3:/opt/openteamstatus/db.sqlite3:z registry.gitlab.com/threde/open-team-status ./manage.py createsuperuser
docker run -it --rm -e ALLOWED_HOSTS=localhost -p 8000:80 -v $PWD/db.sqlite3:/opt/openteamstatus/db.sqlite3:z registry.gitlab.com/threde/open-team-status
```
