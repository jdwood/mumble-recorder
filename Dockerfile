FROM python:3.8

RUN apt-get update \
    && apt-get install -y libopus0 opus-tools yarn

COPY requirements.txt requirements.txt
COPY stenographer/pymumble/requirements.txt pymumble/requirements.txt

RUN pip install -r requirements.txt -r pymumble/requirements.txt

COPY . .

EXPOSE 5000/tcp

ENTRYPOINT ["/bin/sh"]
CMD ["/run_bot.sh"]