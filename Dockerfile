FROM python:3

RUN pip install dumb-init

RUN mkdir /opt/openteamstatus
WORKDIR /opt/openteamstatus

COPY requirements.txt /opt/openteamstatus/requirements.txt
RUN pip install -r requirements.txt

ADD openteamstatus /opt/openteamstatus/openteamstatus
ADD core /opt/openteamstatus/core
ADD checkins /opt/openteamstatus/checkins
ADD manage.py /opt/openteamstatus/manage.py

RUN ./manage.py collectstatic --no-input

ENV PYTHONPATH=/opt/openteamstatus/
ENV DEBUG=false

ENTRYPOINT ["dumb-init", "--"]
CMD ["gunicorn", "openteamstatus.wsgi:application", "--bind=0:80", \
     "--access-logfile=-", "--error-logfile=-"]

