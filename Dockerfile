FROM python:3

RUN mkdir /opt/openteamstatus
WORKDIR /opt/openteamstatus

COPY requirements.txt /opt/openteamstatus/requirements.txt
RUN pip install -r requirements.txt

ADD . /opt/openteamstatus/

ENV PYTHONPATH=/opt/openteamstatus/

CMD ["gunicorn", "openteamstatus.wsgi:application", "--bind=0:80", \
     "--access-logfile=-", "--error-logfile=-"]

