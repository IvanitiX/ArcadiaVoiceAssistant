import festival
import nanotts
import wave

frase = 'Hola, ¿qué tal?. Me llamo Arcadia y seré tu Asistente. ¡Encantada de conocerte!'

fest_wav = wave.open(festival.textToWavFile(frase),'rb')
wave_buffer = wave.open('fest.wav','wb')

wave_buffer.setnchannels(fest_wav.getnchannels())
wave_buffer.setframerate(fest_wav.getframerate())
wave_buffer.setnframes(fest_wav.getnframes())
wave_buffer.setsampwidth(fest_wav.getsampwidth())
wave_buffer.writeframes(fest_wav.readframes(fest_wav.getnframes()))
wave_buffer.close()
fest_wav.close()

nano_tts = nanotts.NanoTTS(voice='es-ES',outputFile='nano.wav',speed=1.25, pitch=1.1)

nano_wav = nano_tts.speaks(frase)

