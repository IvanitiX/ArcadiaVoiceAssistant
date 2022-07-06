FROM python:3.9-slim

COPY ./ /code
WORKDIR /code

RUN apt update && apt install -y --no-install-recommends ffmpeg portaudio19-dev git gcc g++ make \
libtool autotools-dev automake autoconf alsa-utils pulseaudio

RUN pip install -U pip
RUN pip install -r requirements.txt

RUN python -V

RUN git clone https://github.com/gmn/nanotts.git
RUN cd nanotts && make

ENV PATH="/code/nanotts/:$PATH"
RUN mkdir /usr/share/pico/
RUN cp -r nanotts/lang /usr/share/pico/

ENV RASA_IP="172.19.0.2"

ENTRYPOINT ["tail", "-f", "/dev/null"]



