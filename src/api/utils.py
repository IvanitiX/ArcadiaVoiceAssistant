from fastapi import UploadFile

def read_audio(audio: UploadFile):
    try:
        contents = audio.file.read()
        with open(audio.filename, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "Ha habido un error al subir el archivo."}
    finally:
        audio.file.close()