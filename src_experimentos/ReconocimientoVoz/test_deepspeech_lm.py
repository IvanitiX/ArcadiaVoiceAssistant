from asyncore import write
import deepspeech
import wave
import numpy as np
import jiwer
import sys

if(len(sys.argv) != 13):
    print (u"Faltan argumentos. Uso: {0} AUDIO MODELO SCORER TRANSCRIPCION_REAL ALPHA_MIN ALPHA_PHASE ALPHA_MAX BETA_MIN BETA_PHASE BETA_MAX TRANSCRIPCION_OUTPUT ARCHIVO_RESULTADOS".format(sys.argv[0]))
    exit(1)

LM_ALPHA_MIN = float(sys.argv[5])
LM_ALPHA_MAX = float(sys.argv[7])
LM_BETA_MIN = float(sys.argv[8])
LM_BETA_MAX = float(sys.argv[10])
LM_ALPHA_PHASE = float(sys.argv[6])
LM_BETA_PHASE = float(sys.argv[9])

BEAM_WIDTH = 500

MODEL_PATH = sys.argv[2]
SCORER_PATH = sys.argv[3]
AUDIO_FILE = sys.argv[1]

TEST_FILE = sys.argv[4]
TRANSCRIBED_FILE = sys.argv[11]
CSV_FILE = sys.argv[12]


model = deepspeech.Model(MODEL_PATH)
model.enableExternalScorer(SCORER_PATH)
model.setBeamWidth(BEAM_WIDTH)

file_wav = wave.open(AUDIO_FILE,'r')
buffer_wav = file_wav.readframes(file_wav.getnframes())
buffer_wav_16bit = np.frombuffer(buffer_wav, dtype=np.int16)

original_transcript = open(TEST_FILE, 'r').read()
csv_buffer = open(CSV_FILE, 'w+')

best_alpha = 0.0
best_beta = 0.0
best_cer = 1.0
best_text = ""

print("::> Creando CSV...")
csv_buffer.write("Alpha\tBeta\tWER\tCER\tTexto")
for alpha in np.arange(LM_ALPHA_MIN,LM_ALPHA_MAX+0.1,LM_ALPHA_PHASE):
    for beta in np.arange(LM_BETA_MIN,LM_BETA_MAX+0.1,LM_BETA_PHASE):
        print(u"\t:: Probando con Alpha = {0}, Beta = {1}".format(alpha,beta))
        model.setScorerAlphaBeta(alpha,beta)
        texto = model.stt(buffer_wav_16bit)
        wer = jiwer.wer(original_transcript, texto)
        cer = jiwer.cer(original_transcript, texto)
        if(cer <= best_cer):
            best_alpha = alpha
            best_beta = beta
            best_cer = cer
            best_text = texto
        print("\t:: Escribiendo resultados")
        csv_buffer.write(u"{0}\t{1}\t{2}\t{3}\t{4}\n".format(alpha,beta,wer,cer,texto))

csv_buffer.write("____________________________________________________\n")
csv_buffer.write(u"Mejor combinación: Alpha: {0} / Beta : {1} / CER : {2}\n".format(best_alpha,best_beta,best_cer))
csv_buffer.write("____________________________________________________\n")
csv_buffer.close()

print("::> Escribiendo mejor transcripción...")
hypothesis_transcript = open(TRANSCRIBED_FILE,'w')
hypothesis_transcript.write(best_text)
hypothesis_transcript.close()

print("::> ¡Terminado!")


