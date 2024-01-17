import os
import json
from math import floor as floor
import whisper
  
sys_par_path = os.path.join(os.path.dirname(__file__), 'sys_par.json')
with open(sys_par_path, 'r') as f:
  json_data = json.load(f)
  use_fp16 = json_data["use_fp16"]
if use_fp16 is None:
  import torch
  use_fp16 = True if torch.cuda.is_available() else False
  with open(sys_par_path, 'w') as f:
    json_data = {"use_fp16": use_fp16}
    json.dump(json_data, f, indent=4)

total_dur = 0

def format_seconds_to_srt(seconds):
    hours = floor(seconds) // 3600
    seconds -= 3600 * hours
    minutes = floor(seconds) // 60
    seconds -= 60 * minutes
    intseconds = floor(seconds)
    seconds -= intseconds
    seconds = round(seconds*1000)
    if seconds == 1000:
      seconds = 0
      intseconds += 1
    if intseconds == 60:
      intseconds = 0
      minutes += 1
    if minutes == 60:
      minutes = 0
      hours += 1
    return "%02i:%02i:%02i,%003i" % (hours, minutes, intseconds, seconds)

def transcribe_tmp_m(idx, input_dir, Sprache, task="transcribe"):
  global model_tr
  sentences = []
  tmp_dir = os.path.join(input_dir,'tmp')
  
  try:
    if Sprache == "Auto":
      result = model_tr.transcribe(os.path.join(tmp_dir,f'{idx:02d}-S.wav'), task=task, fp16 = use_fp16)
    else:
      result = model_tr.transcribe(os.path.join(tmp_dir,f'{idx:02d}-S.wav'), language=Sprache, task=task, fp16 = use_fp16)
  except Exception as e:
    print(f'{idx}: error')
    with open(os.path.join(tmp_dir,f'{idx:02d}-S_report.txt'), 'w') as f:
      f.write(str(e))
  else:
    for segment in result["segments"]:
      sentences.append([segment["start"], segment["end"], segment["text"]])
    return sentences

def transcribe_chunks_m(input_dir:str, input_file:str, language:str, task:str, model:str, slength:int, sthreshold:int, short:bool, intmp:str, deltmp:str) -> None:
  input_base, input_extension = os.path.splitext(input_file)
  input_path = os.path.join(input_dir,input_file)
  global model_tr
  last_model = ""
  if model != last_model:
    model_tr = whisper.load_model(model)
    last_model = model
  if short:
    sentences = []
    try:
      if Sprache == "Auto":
        result = model_tr.transcribe(input_path, fp16 = use_fp16)
      else:
        result = model_tr.transcribe(input_path, language=Sprache, fp16 = use_fp16)
    except Exception as e:
      print(f'Error: {str(e)}')
      with open(os.path.join(input_dir,f'{input_base}_report.txt'), 'w') as f:
        f.write(str(e))
    else:
      for segment in result["segments"]:
        sentences.append([segment["start"], segment["end"], segment["text"]])
      with open(os.path.join(input_dir,f'{input_base}.txt'), 'w') as outfile:
        for sentence in sentences:
          if sentence[2] == '':
            continue
          start_seconds = sentence[0]
          end_seconds = sentence[1]
          outfile.write(f"[{format_seconds_to_srt(start_seconds)} --> {format_seconds_to_srt(end_seconds)}]{sentence[2]}\n")
  else:
    from .wavlen import wav_length
    tmp_dir = os.path.join(input_dir,'tmp') 
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)  
    if intmp == 'false':
      from .sabs import split_audio_by_silence
      msl = slength
      sth = sthreshold
      split_audio_by_silence(input_path, input_dir, msl, sth)
    
    global total_dur
    num_files = len([name for name in os.listdir(tmp_dir) if name[-4:]=='.wav'])
    with open(os.path.join(input_dir,f'{input_base}.txt'), 'w') as outfile:
      for idx in range(num_files):
        this_length = wav_length(os.path.join(tmp_dir,f'{idx:02d}-S.wav'))
        sentences = transcribe_tmp_m(idx, input_dir, language, task)
        if sentences == []:
          print(f"Error in {idx}")
          total_dur += this_length
          continue
        for sentence in sentences:
          if sentence[2] == '':
            continue
          start_seconds = sentence[0]
          end_seconds = sentence[1]
          start_seconds += total_dur
          if end_seconds > this_length:
            end_seconds = this_length
          end_seconds += total_dur
          outfile.write(f"[{format_seconds_to_srt(start_seconds)} --> {format_seconds_to_srt(end_seconds)}]{sentence[2]}\n")
        total_dur += this_length
    if deltmp == 'true':
      tmplist = [ f for f in os.listdir(tmp_dir)]
      for f in tmplist:
          os.remove(os.path.join(tmp_dir, f))
      os.rmdir(tmp_dir)
    



