FROM python:3.11.1-buster

WORKDIR /app/omen

ADD . .

ENV PYTHONPATH="$PYTHONPATH:/usr/lib/python3.10/site-packages"

RUN apt-get install cmake

RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "src/omen/omen_bot.py" ]
