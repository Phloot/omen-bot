FROM python:3.10.5-alpine3.16

ADD . .

RUN pip install -r requirements.txt

CMD [ "python", "src/omen/omen_bot.py" ]