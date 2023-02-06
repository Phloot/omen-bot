FROM python:3.10.9-alpine3.16

WORKDIR /app/omen

ADD . .

RUN apk --no-cache add postgresql-dev gcc g++ musl-dev py3-scikit-learn

ENV PYTHONPATH="$PYTHONPATH:/usr/lib/python3.10/site-packages"

RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "src/omen/omen_bot.py" ]
