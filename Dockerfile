FROM python:3.10.5-alpine3.16

WORKDIR /app/omen

ADD . .

RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "src/omen/omen_bot.py" ]