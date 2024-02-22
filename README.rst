What's new in 1.1.0
====================

* in case of language auto detection, now the auto detected language is shown for future use. In the GUI, the language selected will be changed from "Auto" to the detected language after transcription/translation is done; in the CLI, the detected language is displayed in the console following the "Done!" message.

* faster than version 1.0.0 by utilising lower-level access to Whisper, splitting in sentences is no longer needed for higher speed and thus removed. The time (in seconds) spent for preparing (mostly for loading the model) and processing the transcription/translation task are displayed in console following the respective sub-job done.

* The option of API is added for those having an OpenAI API key and preferring online instead of offline transcription/translation. For more details, read the section *use API*.

NOTE: This is a major update. If you already have version 1.0.0 installed, you'll have to go to the *easy_whisper* folder in *site-packages* and delete the two *json* files for this version to work.

About Easy Whisper
===================

The python library *easy_whisper* is an easy to use adaptation of the popular *OpenAI Whisper* for transcribing audio files. The main features are:

* both CLI and (tkinter) GUI user interface
* fast processing even on CPU
* output in .txt format with time stamps

Installation
=============

In the terminal, run::

  pip install easy_whisper

*OpenAI Whisper* requires *FFmpeg* to process non-WAV files. A brief installation guide can be found in the Github repository of `OpenAI Whisper`_:

.. _OpenAI Whisper: https://github.com/openai/whisper

Use GUI
========

Simply type in the command line::

  easy_whisper

or::

  python -m easy_whisper

to start the *tkinter* window.

Mouseover a control element to show quick help info.

When used for the first time, it can take longer, as it has to be checked if CUDA (faster) is available or only CPU (slower). Also the modules have to be compiled for faster use later. Moreover, *OpenAI Whisper* models which have not yet been used must first be downloaded. For more info about models, read the section *Model* below.

In the following, I'll briefly explain the control elements one by one.

Path
-----

On the first run, the path is set to the most recent audio file in the current working directory, which, of course, can be changed by clicking on the "Choose File" button on the right. 

If the preselected "save setting" option is not unselected, then on the next start, the folder used last time will be automatically chosen. This is practical if the user adds audio files to the destined folder one at a time to transcribe them immediately after adding.

Language
---------

Specify the language of the audio file can enhance the speed. If the language is unknown, you can also choose *Auto* for auto detection. *Auto* is preselected on the first run. Later, if "save setting" is not unselected, then the language used last time will be preselected.

Model
------

For higher speed, choose a smaller *OpenAI Whisper* model, for higher quality, chose a larger one. The models with the suffix "en" are for English only. I recommend "base.en" for English and "small" for other languages, as the quality is already high enough for most purposes.

To learn more about the models, view  `OpenAI Whisper`_:

.. _OpenAI Whisper: https://github.com/openai/whisper

use API
--------

To use API, you should first set up an environment variable of API to use *OpenAI* services::

  export OPENAI_API_KEY='sk-...'

When using API, there is no need to specify model and language. In CLI, simply specify the path (if the desired audio is not the most recent one in the current working directory) and task (if not the same as last time), then add "--api" or "-i". In GUI, choose file path (if not already auto-recognised), select "use API", select "transcribe" or "translate", then click "Run" (the selected "Language" and "Model" have no effect here).

save setting
-------------

Preselected by default, only unselect if necessary. If selected, settings for Path/Language/Model/task(transcribe or translate) from last usage will be saved for the use next time. It is practical to leave this option selected if the user intends to transcribe files with similar settings over a longer time period. The default models for English and other Languages (including *Auto*) are stored separately - one for English only and one for other languages.

Reset
------

Click this button if you want to reset Path/Language/Model/task(transcribe or translate) to the system default values, which are current folder/Auto (detection)/small or base.en/transcribe

transcribe/translate
---------------------

By default, *easy_whisper* transcribes the audio file, but you can also switch to "translate", in which case the (non-English) speech will be translated into English. Click the "Run" button to start transcription/translation, the window is then minimised and you can do something else while waiting. When the job is done, the window reappears to regain your attention. The result is a *.txt* file with the same name and put in the same folder as the audio file. For example, if the path to the audio file is *folder2/audio2.wav*, then the path to the *.txt* file will be *folder2/audio2.txt*. In case of translation, the suffix "_English" will be added, so the output path is then *folder2/audio2_English.txt*. The *.txt* file contains the transcription/translation with time stamps, which looks like below:

[00:00.000 --> 00:10.880] Chapter 1. Title.
[00:10.880 --> 00:16.680] Sentence one.
... ...

Use CLI
========

To use the CLI (command line interface), simply write "easy_whisper" followed by any argument. For example::

  easy_whisper folder3/audio3.mp4

transcribes *audio3.mp4* or translates it if the setting "translation" was used and saved last time. If you want to use all saved settings including the file path, type::

  easy_whisper --cli

or::

  easy_whisper -c

then the most recent audio file in the folder accessed last time will be processed.

The arguments largely correspond to the *tkinter* GUI control elements, with the addition of the --cli argument. Below is a summary table:

====================     =========================  
        CLI                         GUI   
====================     =========================  
 positional                 Path  
 -l, --language             Language 
 -m, --model                Model  
 -v, --sdefault             NOT save setting
 -u, --udefault             Reset
 -t, --task                 transcribe/translate
 -i, --api                  use API
 -c, --cli  
====================     =========================

Use --help or -h to see help information.

Disclaimer
===========

I wrote *easy_whisper* for my personal use and published it for others who may also find it useful. If you have any question, feel free to ask, but keep in mind that I can only reply in my spare time.
