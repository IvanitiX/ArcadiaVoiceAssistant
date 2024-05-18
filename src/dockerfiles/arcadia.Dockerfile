FROM python:3.9-slim

COPY ./ /code
WORKDIR /code

RUN apt update && apt install -y --no-install-recommends ffmpeg portaudio19-dev git gcc g++ make \
libtool autotools-dev automake autoconf alsa-utils pulseaudio wget

RUN pip install -U pip
RUN pip install -r requirements.txt


RUN python -V

RUN git clone https://github.com/gmn/nanotts.git
RUN cd nanotts && make

ENV PATH="/code/nanotts/:$PATH"
RUN mkdir /usr/share/pico/
RUN cp -r nanotts/lang /usr/share/pico/

RUN mkdir model_files/ test_files/
RUN cd model_files && apt install -y --no-install-recommends zip unzip && wget --no-check-certificate https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip && unzip vosk-model-small-es-0.42.zip && mv vosk-model-small-es-0.42 model


ENV RASA_IP="172.20.0.2"

RUN echo "Test" | nanotts -c -o test_files/nano.wav


CMD ["python", "-m", "uvicorn", "api.arcadia_api:app", "--host", "0.0.0.0", "--port", "8000"]



