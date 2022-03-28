from espeakng import ESpeakNG
import wave
import io

voice_synthesizer = ESpeakNG(voice='mb-es3',pitch=70,word_gap=1, speed=170,)
for voice in voice_synthesizer.voices :
    print(voice['voice_name'])
wav_bytes = voice_synthesizer.synth_wav('Hola, ¿qué tal?. Me llamo Arcadia y seré tu Asistente. ¡Encantada de conocerte!')

wav_out = wave.open('espeak.wav','wb')
wav_in = wave.open(io.BytesIO(wav_bytes),'rb')

wav_out.setnchannels(wav_in.getnchannels())
wav_out.setframerate(wav_in.getframerate())
wav_out.setnframes(wav_in.getnframes())
wav_out.setsampwidth(wav_in.getsampwidth())
wav_out.writeframes(wav_bytes)
wav_out.close()
wav_in.close()