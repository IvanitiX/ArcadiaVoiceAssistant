#Imports
import json
import os
import requests
from ibm_watson import SpeechToTextV1
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Constantes
CLAVE_TTS = '7_Uvgrm5vCuMO5bTGDbaD1L-AbN-AUob3t7Pa29Mntq-'
URL_TTS = 'https://api.eu-gb.text-to-speech.watson.cloud.ibm.com/instances/a80e9756-1c87-414d-afd3-789215909905'
CLAVE_SR ='PnzByCYd57HYCmjDh8tvfbBIxfjlEMePujx5b69ZpKKJ'
URL_SR = 'https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/8ee2b4e2-3ad2-4d69-8a11-f1b5b6db4c12'
#URL_CHATBOT ='http://localhost:5002/webhooks/rest/webhook' 
URL_CHATBOT = 'http://b89e-150-214-205-83.ngrok.io/webhooks/rest/webhook'

MODEL_SR = 'es-ES_BroadbandModel'
VOICE_TTS = 'es-ES_LauraV3Voice'
ALTERNATIVE_THRESHOLD = 0.9

# Métodos de apoyo

def sintetizar(path,reader,text):
    with open(path,'wb') as archivoAudio:
        archivoAudio.write(
            reader.synthesize(
                text,
                accept = 'audio/wav',
                voice = VOICE_TTS
            ).get_result().content
        )

def transcribirAudio(path,recognizer):
    with open(path,'rb') as archivoAudio:
        resultado = recognizer.recognize(
            audio = archivoAudio,
            word_alternatives_threshold = ALTERNATIVE_THRESHOLD,
            model = MODEL_SR
        ).get_result()
    return resultado

def getBestTranscript(alternatives):
    alternativas = alternatives['results'][0]['alternatives']
    mejorTranscripcion = " "
    mejorConfianza = 0.0

    for i in alternativas:
        if (i["confidence"] >= mejorConfianza):
            mejorTranscripcion = i["transcript"]
            mejorConfianza = i["confidence"]
    
    return mejorTranscripcion

# Variables
Audio_Input = 'input_3.wav'
Audio_Output = 'output.wav'

def main():
    WatsonSR = SpeechToTextV1(authenticator=IAMAuthenticator(CLAVE_SR))
    WatsonTTS = TextToSpeechV1(authenticator=IAMAuthenticator(CLAVE_TTS))
    WatsonSR.set_service_url(URL_SR)
    WatsonTTS.set_service_url(URL_TTS)

    #Transcripción, SR
    transcripcion = transcribirAudio(Audio_Input,WatsonSR)
    transcripcion = getBestTranscript(transcripcion)
    print(u'::> Transcripción : {0}'.format(transcripcion))

    #Tratamiento de la pregunta a la respuesta
    r = requests.post(URL_CHATBOT, json={"sender": 'Human', "message": transcripcion})

    print("Bot says, ")
    for i in r.json():
        try:
            bot_message = i['text']
            sintetizar(Audio_Output,WatsonTTS,bot_message)
        except KeyError:
            try:
                bot_message = i['image']
            except KeyError:
                bot_message = ''
        print(f"{bot_message}")
    # Lectura de la respuesta, TTS
    

    return input('¿Probamos de nuevo? (S/N)')

_exit = 'N'
while (_exit != 'S'):
  _exit = main().upper()