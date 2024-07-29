import os
import requests
from pydub import AudioSegment
import json
import docx

url = "https://api.elevenlabs.io/v1/text-to-speech/pqHfZKP75CvOlQylNhV4"
api_key = "YOUR ELEVENLABS API KEY"
model_id = "FM7UaI5pOHuIVlH9duvo" # <-- No genera el archivo pero no se logra reproducir
# model_id = "eleven_multilingual_v2" 

# Función para sacar contenido de un archivo de Word y guardarlo en una variable llamada text
def get_text_from_word_file(file_path):
    doc = docx.Document(file_path)
    text = []
    for para in doc.paragraphs:
        text.append(para.text)
    return "\n".join(text)

# Variable booleana para generar audio de múltiples archivos o no
multiple_docs = False

if multiple_docs:
    # Obtener la lista de archivos en la carpeta "docs"
    doc_files = os.listdir("./docs")
    for file_name in doc_files:
        if file_name.endswith(".docx"):
            # Obtener el texto del archivo de Word
            text = get_text_from_word_file(f"./docs/{file_name}")
            # Generar el nombre del archivo de audio sin extensión
            audio_file_name = os.path.splitext(file_name)[0]

            payload = {
                "text": text,
                "voice_settings": {"stability": 0.35, "similarity_boost": 0.8},
                "model_id": model_id,
            }
            headers = {
                "xi-api-key": api_key,
                "Content-Type": "application/json",
            }

            response = requests.request("POST", url, json=payload, headers=headers)

            audio_data = response.content
            # Guardar el audio en un archivo mp4
            with open(f"audio/multi/{audio_file_name}.mp4", "wb") as f:
                f.write(audio_data)

            print(f"Audio guardado en {audio_file_name}.mp4")
else:
    # Obtener el texto del archivo de Word especificado
    file_name = "texto"
    text = get_text_from_word_file(f"./docs/{file_name}.docx")

    payload = {
        "text": text,
        "voice_settings": {"stability": 0.35, "similarity_boost": 0.8},
        "model_id": model_id,
    }
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    audio_data = response.content
    # Guardar el audio en un archivo mp4 en la carpeta "audio/individual"
    with open(f"audio/individual/{file_name}.mp4", "wb") as f:
        f.write(audio_data)

    print(f"Audio guardado en audio/individual/{file_name}.mp4")
