from openai import OpenAI
from config import OPENAI_API_KEY
import os
from whisper.utils import (
    format_timestamp,
    make_safe,
)

def transcribe_api(input_dir:str, input_file:str, task:str):
    print(f"Uploading {input_file} in {input_dir}, wait ...")
    
    input_path = os.path.join(input_dir, input_file)
    input_base, input_extension = os.path.splitext(input_file)
  
    client = OpenAI(api_key=OPENAI_API_KEY)

    with open(input_path, "rb") as audio_file
        if task=="transcribe":
            task_type = "Transcription"
            transcript = client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-1",
            response_format="verbose_json",
            timestamp_granularities=["word"]
            )
        else:
            task_type = "Translation"
            transcript = client.audio.translations.create(
            file=audio_file,
            model="whisper-1",
            response_format="verbose_json",
            timestamp_granularities=["word"]
            ) 

    if task == "translate":
        outfile_name = f'{input_base}_English.txt'
    else:
        outfile_name = f'{input_base}.txt'
    with open(os.path.join(input_dir,outfile_name), 'w') as outfile:
        for segment in transcript["segments"]:
            start, end, text = segment["start"], segment["end"], segment["text"]
            line = f"[{format_timestamp(start)} --> {format_timestamp(end)}] {text}\n"
            outfile.write(make_safe(line))

    print(f"{task_type} saved as {outfile_name} in {input_dir}.")
    return transcript["language"]