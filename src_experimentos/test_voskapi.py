#!/usr/bin/env python3

from vosk import Model, KaldiRecognizer
import jiwer
import sys
import json
import os

if(len(sys.argv) != 6):
    print (u"Faltan argumentos. Uso: {0} AUDIO MODELO ARCHIVO_TRANSCRIPCION_ORIGINAL ARCHIVO_TEXTO_OUTPUT ARCHIVO_ESTADISTICAS_OUTPUT".format(sys.argv[0]))
    exit(1)


AUDIO = sys.argv[1]
MODEL_FOLDER = sys.argv[2]
TRANSCRIPTION_FILE  = sys.argv[3]
TRANSCRIBED_FILE = sys.argv[4]
STATS_FILE = sys.argv[5]

if not os.path.exists(MODEL_FOLDER):
    print ("Modelo no válido. Descárgate uno en https://alphacephei.com/vosk/models y descomprímelo. Pasa el nombre de la carpeta como argumento")
    exit (2)


model = Model(MODEL_FOLDER)

# Large vocabulary free form recognition
rec = KaldiRecognizer(model, 16000)

# You can also specify the possible word list
#rec = KaldiRecognizer(model, 16000, "zero oh one two three four five six seven eight nine")

wf = open(sys.argv[1], "rb")
#wf.read(44) # skip header

res = ""

while True:
    data = wf.read(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        res = res + json.loads(rec.Result())['text'] + " "

res = res + json.loads(rec.FinalResult())['text']

transcripcion_original = open(TRANSCRIPTION_FILE,'r').read()

transcripcion_buffer = open(TRANSCRIBED_FILE,'w')
transcripcion_buffer.write(res)
transcripcion_buffer.close()

stats_buffer = open(STATS_FILE, 'w')
stats_buffer.write(u"WER = {0}\n".format(jiwer.wer(transcripcion_original, res)))
stats_buffer.write(u"CER = {0}\n".format(jiwer.cer(transcripcion_original, res)))