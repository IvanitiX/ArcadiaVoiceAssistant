FROM python:3.9-slim

RUN pip install -U pip
RUN pip install rasa
RUN pip install wikipedia
RUN pip install python-dotenv

COPY chatbot/ /code
WORKDIR /code

RUN python -V
RUN rasa --version

ENTRYPOINT ["python","-m","rasa", "run", "actions"]