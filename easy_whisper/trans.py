import time
import os
import json
from math import floor as floor
import whisper
import torch
from whisper.audio import (
    HOP_LENGTH,
    N_FRAMES,
    N_SAMPLES,
    SAMPLE_RATE,
    log_mel_spectrogram,
    pad_or_trim,
)
from whisper.decoding import DecodingOptions, DecodingResult
from whisper.tokenizer import get_tokenizer 
from whisper.utils import (
    exact_div,
    format_timestamp,
    make_safe,
)
  
sys_par_path = os.path.join(os.path.dirname(__file__), 'sys_par.json')
if not os.path.exists(sys_par_path):
  import torch
  if torch.cuda.is_available():
    use_fp16 = True
    sys_device = "cuda"
  else:
    use_fp16 = False
    sys_device = "cpu"
  with open(sys_par_path, 'w') as f:
    json_data = {"use_fp16": use_fp16, "sys_device": sys_device}
    json.dump(json_data, f, indent=4)
else:
  with open(sys_par_path, 'r') as f:
    json_data = json.load(f)
    use_fp16 = json_data["use_fp16"]
    sys_device = json_data["sys_device"]

detected_lang = ""
def transcribe_chunks_m(input_dir:str, input_file:str, language:str, task:str, model:str):
  start_time = time.time()
  print(f"Processing {input_file} in {input_dir}, wait ...")
  input_base, input_extension = os.path.splitext(input_file)
  input_path = os.path.join(input_dir,input_file)
  source_lang = language
  decode_options = {"fp16": use_fp16}
  global model_tr
  model_tr = whisper.load_model(model, device=sys_device)
  cur_start_time = time.time()
  print(f"{cur_start_time - start_time} seconds preparing time for {input_file}.")
  start_time = cur_start_time
  dtype = torch.float16 if use_fp16 else torch.float32
  mel = log_mel_spectrogram(input_path, padding=N_SAMPLES)
  content_frames = mel.shape[-1] - N_FRAMES
  if language == "Auto":
        if model.endswith(".en"):
            source_lang = "en"
        else:
            mel_segment = pad_or_trim(mel, N_FRAMES).to(model_tr.device).to(dtype)
            _, probs = model_tr.detect_language(mel_segment)
            source_lang = max(probs, key=probs.get)
  tokenizer = get_tokenizer(model_tr.is_multilingual, language=source_lang, task=task)
  seek = 0
  input_stride = exact_div(
      N_FRAMES, model_tr.dims.n_audio_ctx
  )
  time_precision = (
      input_stride * HOP_LENGTH / SAMPLE_RATE
  )
  all_tokens = []
  all_segments = []
  prompt_reset_since = 0
  def new_segment(
        *, start: float, end: float, tokens: torch.Tensor, result: DecodingResult
    ):
        tokens = tokens.tolist()
        text_tokens = [token for token in tokens if token < tokenizer.eot]
        return {
            "seek": seek,
            "start": start,
            "end": end,
            "text": tokenizer.decode(text_tokens),
            "tokens": tokens,
        }
  decode_options["language"] = source_lang
  decode_options["task"] = task
  decode_options["temperature"] = 0.0
  last_speech_timestamp = 0.0
  while seek < content_frames:
      time_offset = float(seek * HOP_LENGTH / SAMPLE_RATE)
      mel_segment = mel[:, seek : seek + N_FRAMES]
      segment_size = min(N_FRAMES, content_frames - seek)
      segment_duration = segment_size * HOP_LENGTH / SAMPLE_RATE
      mel_segment = pad_or_trim(mel_segment, N_FRAMES).to(model_tr.device).to(dtype)

      decode_options["prompt"] = all_tokens[prompt_reset_since:]
      current_options = DecodingOptions(**decode_options)
      result: DecodingResult = model_tr.decode(mel_segment, current_options)
      tokens = torch.tensor(result.tokens)

      if result.avg_logprob < -1.2:
          seek += segment_size
          prompt_reset_since = len(all_tokens)
          continue

      current_segments = []

      timestamp_tokens: torch.Tensor = tokens.ge(tokenizer.timestamp_begin)
      single_timestamp_ending = timestamp_tokens[-2:].tolist() == [False, True]

      consecutive = torch.where(timestamp_tokens[:-1] & timestamp_tokens[1:])[0]
      consecutive.add_(1)
      if len(consecutive) > 0:
          slices = consecutive.tolist()
          if single_timestamp_ending:
              slices.append(len(tokens))

          last_slice = 0
          for current_slice in slices:
              sliced_tokens = tokens[last_slice:current_slice]
              start_timestamp_pos = (
                  sliced_tokens[0].item() - tokenizer.timestamp_begin
              )
              end_timestamp_pos = (
                  sliced_tokens[-1].item() - tokenizer.timestamp_begin
              )
              current_segments.append(
                  new_segment(
                      start=time_offset + start_timestamp_pos * time_precision,
                      end=time_offset + end_timestamp_pos * time_precision,
                      tokens=sliced_tokens,
                      result=result,
                  )
              )
              last_slice = current_slice

          if single_timestamp_ending:
              seek += segment_size
          else:
              last_timestamp_pos = (
                  tokens[last_slice - 1].item() - tokenizer.timestamp_begin
              )
              seek += last_timestamp_pos * input_stride
      else:
          duration = segment_duration
          timestamps = tokens[timestamp_tokens.nonzero().flatten()]
          if (
              len(timestamps) > 0
              and timestamps[-1].item() != tokenizer.timestamp_begin
          ):
              last_timestamp_pos = (
                  timestamps[-1].item() - tokenizer.timestamp_begin
              )
              duration = last_timestamp_pos * time_precision

          current_segments.append(
              new_segment(
                  start=time_offset,
                  end=time_offset + duration,
                  tokens=tokens,
                  result=result,
              )
          )
          seek += segment_size

      for i, segment in enumerate(current_segments):
          if segment["start"] == segment["end"] or segment["text"].strip() == "":
              segment["text"] = ""
              segment["tokens"] = []
              segment["words"] = []

      all_segments.extend(
          [
              {"id": i, **segment}
              for i, segment in enumerate(
                  current_segments, start=len(all_segments)
              )
          ]
      )
      all_tokens.extend(
          [token for segment in current_segments for token in segment["tokens"]]
      )

  if task == "translate":
    outfile_name = f'{input_base}_English.txt'
  else:
    outfile_name = f'{input_base}.txt'
  with open(os.path.join(input_dir,outfile_name), 'w') as outfile:
    for segment in all_segments:
      start, end, text = segment["start"], segment["end"], segment["text"]
      line = f"[{format_timestamp(start)} --> {format_timestamp(end)}] {text}\n"
      outfile.write(make_safe(line))
  print(f"{time.time() - start_time} seconds processing time for {input_file}")
  return source_lang
    



