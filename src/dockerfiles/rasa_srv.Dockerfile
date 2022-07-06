FROM python:3.9-slim

RUN pip install -U pip
RUN pip install rasa

COPY chatbot/ /code
WORKDIR /code

RUN python -V
RUN rasa --version
RUN rasa train --force

ENTRYPOINT ["python","-m","rasa", "run"]
