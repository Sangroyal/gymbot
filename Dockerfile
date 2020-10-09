FROM python:3.8

WORKDIR /home

ENV TELEGRAM_API_TOKEN="1202070076:AAHCDBf0bIm4A9xmqRKf5726Ux9EKS0gYok"
ENV TELEGRAM_ACCESS_ID="545679284"

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN pip install -U pip aiogram pytz && apt-get update && apt-get install sqlite3
COPY *.py ./
COPY *.sql ./

ENTRYPOINT ["python", "server.py"]

