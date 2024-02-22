from .ui_share import default_params, parse_path, usr_par_path, init_params, all_langs

import argparse
import os
parser = argparse.ArgumentParser(prog='easy_whisper', description='makes OpenAi Whisper easy to use')
parser.add_argument("filepath", metavar='Path', nargs='?', help="the directory or path of audio file, if only dir is specified then the most recent audio file in that dir is used")
parser.add_argument('-l', '--language', nargs='?', help="language spoken in the audio, 'Auto' for unknown language auto detection (slower)", choices=['Auto','af','am','ar','as','az','ba','be','bg','bn','bo','br','bs','ca','cs','cy','da','de','el','en','es','et','eu','fa','fi','fo','fr','gl','gu','ha','haw','he','hi','hr','ht','hu','hy','id','is','it','ja','jw','ka','kk','km','kn','ko','la','lb','ln','lo','lt','lv','mg','mi','mk','ml','mn','mr','ms','mt','my','ne','nl','nn','no','oc','pa','pl','ps','pt','ro','ru','sa','sd','si','sk','sl','sn','so','sq','sr','su','sv','sw','ta','te','tg','th','tk','tl','tr','tt','uk','ur','uz','vi','yi','yo','zh','Afrikaans','Albanian','Amharic','Arabic','Armenian','Assamese','Azerbaijani','Bashkir','Basque','Belarusian','Bengali','Bosnian','Breton','Bulgarian','Burmese','Castilian','Catalan','Chinese','Croatian','Czech','Danish','Dutch','English','Estonian','Faroese','Finnish','Flemish','French','Galician','Georgian','German','Greek','Gujarati','Haitian','Haitian Creole','Hausa','Hawaiian','Hebrew','Hindi','Hungarian','Icelandic','Indonesian','Italian','Japanese','Javanese','Kannada','Kazakh','Khmer','Korean','Lao','Latin','Latvian','Letzeburgesch','Lingala','Lithuanian','Luxembourgish','Macedonian','Malagasy','Malay','Malayalam','Maltese','Maori','Marathi','Moldavian','Moldovan','Mongolian','Myanmar','Nepali','Norwegian','Nynorsk','Occitan','Panjabi','Pashto','Persian','Polish','Portuguese','Punjabi','Pushto','Romanian','Russian','Sanskrit','Serbian','Shona','Sindhi','Sinhala','Sinhalese','Slovak','Slovenian','Somali','Spanish','Sundanese','Swahili','Swedish','Tagalog','Tajik','Tamil','Tatar','Telugu','Thai','Tibetan','Turkish','Turkmen','Ukrainian','Urdu','Uzbek','Valencian','Vietnamese','Welsh','Yiddish','Yoruba'])
parser.add_argument('-t', '--task', nargs='?', help="transcribe or translate (to English)", choices=['transcribe', 'translate'])
parser.add_argument('-m', '--model', nargs='?', help="smaller model runs faster, larger model is more powerful", choices=['tiny.en', 'tiny', 'base.en', 'base', 'small.en', 'small', 'medium.en', 'medium', 'large-v1', 'large-v2', 'large'])
parser.add_argument('-u', '--udefault', action='store_false', help="not use the stored user default values")
parser.add_argument('-v', '--sdefault', action='store_false', help="not save the current setting as user default values")
parser.add_argument('-c', '--cli', action='store_true', help="use CLI (unnecessary if any other parameter is specified)")
parser.add_argument('-i', '--api', action='store_true', help="use OpenAI Whisper API")
args = parser.parse_args()
filepath = args.filepath
language = args.language
task = args.task
model = args.model
if not args.udefault:
    if filepath is None:
        filepath = default_params['file_directory']
    if language is None:
        language = default_params['language']
    if task is None:
        task = default_params['task']
    if model is None:
        if language == 'English' or language == 'en':
            model = default_params['model_en']
        else:
            model = default_params['model']
else:
    if filepath is None:
        if init_params['init_file_directory'] is None:
            filepath = default_params['file_directory']
        else:
            filepath = init_params['init_file_directory']
    if language is None:
        if init_params['init_language'] is None:
            language = default_params['language']
        else:
            language = init_params['init_language']
    if task is None:
        if init_params['init_task'] is None:
            task = default_params['task']
        else:
            task = init_params['init_task']
    if model is None:
        if language == 'English' or language == 'en':
            if init_params['init_model_en'] is None:
                model = default_params['model_en']
            else:
                model = init_params['init_model_en']
        else:
            if init_params['init_model'] is None:
                model = default_params['model']
            else:
                model = init_params['init_model']


input_file, input_dir = parse_path(filepath, input='Auto')

if args.api:
    from .api_trans import transcribe_api
    src_lang = transcribe_api(input_dir=input_dir, input_file=input_file, task=task)
else:
    from .trans import transcribe_chunks_m
    src_lang = transcribe_chunks_m(input_dir=input_dir, input_file=input_file, language=language, task=task, model=model)

if language == "Auto":
    print(f"Detected source language: {all_langs[src_lang]}")

if args.sdefault:
    import json
    if language == 'English' or language == 'en':
        this_model = init_params['init_model']
        this_model_en = model
    else:
        this_model = model
        this_model_en = init_params['init_model_en']
    json_params = {
        'init_file_directory': input_dir, 
        'init_language': language, 
        'init_task': task, 
        'init_model': this_model, 
        'init_model_en': this_model_en
    }
    with open(usr_par_path, 'w') as f:
        json.dump(json_params, f, indent=4)
