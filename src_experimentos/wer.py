import jiwer
import sys

def wer(original, hipotesis):
    return jiwer.wer(original,hipotesis)

def cer(original,hipotesis):
    return jiwer.cer(original,hipotesis)

def leer_texto(archivo):
    buffer = open(archivo, "r")
    return buffer.read()

def main():
    if(len(sys.argv) != 3):
        raise "Necesitamos el texto original y el hipotetico"
    print ("Leyendo archivo original : ")
    original = leer_texto(sys.argv[1])
    print(original)

    print ("Leyendo archivo de hipotesis : ")
    hipotesis = leer_texto(sys.argv[2])
    print(hipotesis)

    print("WER = " + str(wer(original,hipotesis)))
    print("CER = " + str(cer(original,hipotesis)))

main()
