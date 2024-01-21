import os
import json
            
usr_par_path = os.path.join(os.path.dirname(__file__), 'usr_par.json')
if not os.path.exists(usr_par_path):
    init_params = {
        'init_file_directory': None, 
        'init_language': None, 
        'init_task': None, 
        'init_model': None, 
        'init_model_en': None, 
        'init_min_silence_len': None, 
        'init_silence_thresh': None, 
        'init_in_tmp': None, 
        'init_del_tmp': None
    }
    with open(usr_par_path, 'w') as f:
        json.dump(init_params, f, indent=4)
else:
    with open(usr_par_path, 'r') as f:
        init_params = json.load(f)

default_params = {
    "file_directory": ".",
    "language": "Auto",
    "task": "transcribe",
    "model": "small",
    "model_en": "base.en",
    "min_silence_len": 900,
    "silence_thresh": -16,
    "in_tmp": 'false',
    "del_tmp": 'false'
}

def is_audio_file(bname):
    if bname.endswith('.mp3'):
        return True
    elif bname.endswith('.wav'):
        return True
    elif bname.endswith('.mp4'):
        return True
    elif bname.endswith('.mpeg'):
        return True
    elif bname.endswith('.mpga'):
        return True
    elif bname.endswith('.m4a'):
        return True
    elif bname.endswith('.webm'):
        return True
    elif bname.endswith('.wma'):
        return True

def parse_path(filepath, input='dir'):
    if input=='dir':
        all_files = os.listdir(filepath)
        paths = [os.path.join(filepath, bname) for bname in all_files if is_audio_file(bname)]
        if len(paths)<1:
            if filepath == ".":
                fpath = "the current folder"
            else:
                fpath = filepath
            raise FileNotFoundError(f"Error: no supported audio file in {fpath}.") # (.mp3, .mp4, .mpeg, .mpga, .m4a, .wav, .webm, .wma)
        else:
            input_path = max(paths, key=os.path.getctime)
            input_dir = filepath
            input_file = os.path.basename(input_path)
    elif input=='Auto':
        if os.path.isfile(filepath):
            if is_audio_file(filepath):
                input_dir = os.path.dirname(filepath)
                input_file = os.path.basename(filepath)
            else:
                exit("Error: only .mp3, .mp4, .mpeg, .mpga, .m4a, .wav, .webm, .wma are supported.")
        elif os.path.isdir(filepath):
            input_file, input_dir = parse_path(filepath)
        else:
            exit(f"Error: {filepath} is not a valid file or dir path")
    return input_file, input_dir
