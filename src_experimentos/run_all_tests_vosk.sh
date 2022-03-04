#!/bin/bash
python=$(pyenv which python)
for i in {1..8}
do
    $python test_voskapi.py Audios/Ivan/Arcadia_Frase$i.wav Modelos/model Transcripciones/Arcadia_Frase$i.txt TranscripcionesHipotesis/Ivan/Vosk/Arcadia_Frase$i.txt Resultados/Arcadia_Frase${i}_Vosk.txt
    $python test_voskapi.py Audios/Ivan/Lumina_Frase$i.wav Modelos/model Transcripciones/Lumina_Frase$i.txt TranscripcionesHipotesis/Ivan/Vosk/Lumina_Frase$i.txt Resultados/Lumina_Frase${i}_Vosk.txt
done

$python test_voskapi.py Audios/Ivan/TextoLargo.wav Modelos/model Transcripciones/TextoLargo.txt TranscripcionesHipotesis/Ivan/Vosk/TextoLargo.txt Resultados/TextoLargo_Vosk.txt