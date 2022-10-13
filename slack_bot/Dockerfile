FROM python:3.8-slim

WORKDIR /app

COPY requirements2.txt /app/

RUN pip install --trusted-host pypi.python.org -r requirements2.txt
RUN pip install vaderSentiment
RUN pip3 install pandas

CMD ["python", "slack_bot.py"]
