import os
import json
            
usr_par_path = os.path.join(os.path.dirname(__file__), 'usr_par.json')
if not os.path.exists(usr_par_path):
    init_params = {
        'init_file_directory': None, 
        'init_language': None, 
        'init_task': None, 
        'init_model': None, 
        'init_model_en': None
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
    "model_en": "base.en"
}

all_langs = {
    "en": "English",
    "zh": "Chinese",
    "de": "German",
    "es": "Spanish",
    "ru": "Russian",
    "ko": "Korean",
    "fr": "French",
    "ja": "Japanese",
    "pt": "Portuguese",
    "tr": "Turkish",
    "pl": "Polish",
    "ca": "Catalan",
    "nl": "Dutch",
    "ar": "Arabic",
    "sv": "Swedish",
    "it": "Italian",
    "id": "Indonesian",
    "hi": "Hindi",
    "fi": "Finnish",
    "vi": "Vietnamese",
    "he": "Hebrew",
    "uk": "Ukrainian",
    "el": "Greek",
    "ms": "Malay",
    "cs": "Czech",
    "ro": "Romanian",
    "da": "Danish",
    "hu": "Hungarian",
    "ta": "Tamil",
    "no": "Norwegian",
    "th": "Thai",
    "ur": "Urdu",
    "hr": "Croatian",
    "bg": "Bulgarian",
    "lt": "Lithuanian",
    "la": "Latin",
    "mi": "Maori",
    "ml": "Malayalam",
    "cy": "Welsh",
    "sk": "Slovak",
    "te": "Telugu",
    "fa": "Persian",
    "lv": "Latvian",
    "bn": "Bengali",
    "sr": "Serbian",
    "az": "Azerbaijani",
    "sl": "Slovenian",
    "kn": "Kannada",
    "et": "Estonian",
    "mk": "Macedonian",
    "br": "Breton",
    "eu": "Basque",
    "is": "Icelandic",
    "hy": "Armenian",
    "ne": "Nepali",
    "mn": "Mongolian",
    "bs": "Bosnian",
    "kk": "Kazakh",
    "sq": "Albanian",
    "sw": "Swahili",
    "gl": "Galician",
    "mr": "Marathi",
    "pa": "Punjabi",
    "si": "Sinhala",
    "km": "Khmer",
    "sn": "Shona",
    "yo": "Yoruba",
    "so": "Somali",
    "af": "Afrikaans",
    "oc": "Occitan",
    "ka": "Georgian",
    "be": "Belarusian",
    "tg": "Tajik",
    "sd": "Sindhi",
    "gu": "Gujarati",
    "am": "Amharic",
    "yi": "Yiddish",
    "lo": "Lao",
    "uz": "Uzbek",
    "fo": "Faroese",
    "ht": "Haitian Creole",
    "ps": "Pashto",
    "tk": "Turkmen",
    "nn": "Nynorsk",
    "mt": "Maltese",
    "sa": "Sanskrit",
    "lb": "Luxembourgish",
    "my": "Myanmar",
    "bo": "Tibetan",
    "tl": "Tagalog",
    "mg": "Malagasy",
    "as": "Assamese",
    "tt": "Tatar",
    "haw": "Hawaiian",
    "ln": "Lingala",
    "ha": "Hausa",
    "ba": "Bashkir",
    "jw": "Javanese",
    "su": "Sundanese",
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
            raise FileNotFoundError(f"Error: no supported audio file in {fpath}.")
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
