FROM python:3.11.0rc2-alpine3.16

WORKDIR /app/omen

ADD . .

RUN apk --no-cache add gcc musl-dev

RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "src/omen/omen_bot.py" ]