FROM python:3.9-slim

COPY chatbot/ /code
COPY rasa_requirements.txt /code
COPY action_requirements.txt /code
WORKDIR /code

RUN pip install -U pip
RUN pip install -r action_requirements.txt

RUN python -V
RUN rasa --version

ENTRYPOINT ["python","-m","rasa", "run", "actions"]