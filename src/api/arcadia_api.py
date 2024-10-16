"""
Archivo de definición de los métodos de API.
@author Iván Valero Rodríguez
"""

from fastapi import FastAPI
from fastapi import UploadFile
from fastapi.responses import FileResponse
from time import sleep

from arcadia import settings,instances
from api.utils import read_audio
from api.arcadia_api_models import ArcadiaPetition, TTSQuery, \
                                AVAILABLE_SR_MODELS, AVAILABLE_TTS_MODELS

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "¡Hola! Tu instancia de Arcadia está vivita y coleando"}

@app.post("/ask-arcadia-text")
async def ask_to_arcadia_text(question: ArcadiaPetition):
    """
        Endpoint para interactuar con el chatbot de Rasa 
        a través de texto
    """
    chatbot = instances.CHATBOT
    chatbot.make_petition(question.query)
    return {"response": chatbot.get_last_result()}

@app.post("/sr")
async def transcript_audio(audio: UploadFile):
    """
        Endpoint para transcribir un audio a texto.
    """

    sr = instances.SPEECH_RECOGNIZER

    audio = read_audio(audio)

    return {"transcript": sr.recognize(audio.filename)}

@app.post("/sr/{method}")
async def alternative_transcript_audio(method:str, audio: UploadFile):
    """
        Endpoint para transcribir un audio a texto.
    """
    if method not in AVAILABLE_SR_MODELS.keys():
        return {'error': 'El modelo no está entre nuestras opciones.'}
    
    sr = AVAILABLE_SR_MODELS[method]

    audio = read_audio(audio)

    return {"transcript": sr.recognize(audio.filename)}

@app.post("/tts")
async def text_to_speech(query: TTSQuery):
    """
        Endpoint para convertir un texto a voz
    """
    tts = instances.TEXT_TO_SPEECH_GENERATOR
    tts.generate_voice(query.text_to_read)

    sleep(2)

    headers = {'Content-Disposition': 'attachment; filename="nano.wav"'}
    return FileResponse(f"{settings.TESTING_FILES}/nano.wav", headers=headers, media_type='audio/wav')

@app.post("/tts/{method}")
async def alternative_text_to_speech(method:str, query: TTSQuery):
    """
        Endpoint para convertir un texto a voz
    """
    if method not in AVAILABLE_TTS_MODELS.keys():
        return {'error': 'El modelo no está entre nuestras opciones.'}
    tts = AVAILABLE_TTS_MODELS[method]
    tts.generate_voice(query.text_to_read)

    sleep(2)

    headers = {'Content-Disposition': 'attachment; filename="nano.wav"'}
    return FileResponse(f"{settings.TESTING_FILES}/nano.wav", headers=headers, media_type='audio/wav')

@app.post("/ask-arcadia-audio")
async def ask_to_arcadia_audio(audio: UploadFile):
    """
        Endpoint unión de las tres anteriores. Primero
        convierte el audio en texto, luego lo pasa por
        el chatbot para generar una respuesta, y finalmente
        lo lee.
    """

    try:
        contents = audio.file.read()
        with open(audio.filename, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        audio.file.close()

    transcript = instances.SPEECH_RECOGNIZER.recognize(audio.filename)
    keyword_separator = ''
    transcript = transcript.replace(',','')
    for keyword in settings.BOT_NAME_VARIANTS:
        if  keyword in transcript and keyword_separator == '':
            keyword_separator = keyword
    if keyword_separator != '':
        transcript = transcript.split(keyword_separator,1)[-1]
        response = instances.CHATBOT.make_petition(transcript)
        talk_text = ''.join(response)
        print("Resultado:")
        print(talk_text)
        instances.TEXT_TO_SPEECH_GENERATOR.generate_voice(talk_text)
    
    sleep(2)
        
    headers = {'Content-Disposition': 'attachment; filename="nano.wav"'}
    return FileResponse(f"{settings.TESTING_FILES}/nano.wav", headers=headers, media_type='audio/wav')