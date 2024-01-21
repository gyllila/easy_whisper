About Easy Whisper
===================

The python library *easy_whisper* is an easy to use adaptation of the popular *OpenAI Whisper* for transcribing audio files. The main features are:

* both CLI and (tkinter) GUI user interface
* faster processing of long audio even on CPU
* output in .txt format with time stamps in milliseconds precision

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

in tmp
-------

By default, *easy_whisper* splits the audio file into sentences and stores the interim files in a folder named *tmp*.  If the source audio file has the path *folder1/file1.mp3*, then the *tmp* folder has the path *folder1/tmp*.

Sometimes, you may want to split the file manually. One example is that you have recorded the file and processed it with *Audacity* (https://www.audacity.de) to trim the start and end part, then it is convenient to split the file subsequently there. For this purpose, go in *Audacity* to "Analyze/Stille-Finder", then click "OK", this way you can see immediately how the file is split. If you are satisfied with the result, go to "File/Export/Export Multiple", select "Include audio before first label" and change "First file name" to "S", set file format to WAV, then choose the *tmp* folder you have created and click "Export".

After this is done, you can select the option "in tmp" in the *tkinter* window so that *easy_whisper* knows it doesn't have to split the file again. If you forget to do so, *easy_whisper* still works, the only drawback is it will unnecessarily spend time to split the file.

*Audacity* also uses *FFmpeg* to process non-standard audio files. However, the *FFmpeg* you installed for *OpenAI Whisper* possibly doesn't work for *Audacity*. If so, you can download the proper *FFmpeg* from `Audacity Support`_:

.. _Audacity Support: https://support.audacityteam.org/basics/installing-ffmpeg

del tmp
--------

By default, the *tmp* folder with its content remains after transcription is done. If any interim audio file causes error during the transcription, a report *.txt* file will be placed next to the audio file for inspection. For example, if the interim file *02-S.wav* causes error, then a report file *02-S_report.txt* will be placed in the same *tmp* folder. If you see no need for keeping the *tmp* folder, you can check the "del tmp" option and the folder will be automatically deleted after the transcription job is done.

short
------

*easy_whisper* is rather for transcribing audiobooks ranging from few minutes to more than an hour. To transcribe short dialogues with one sentence you don't need this library. But of course you can still use *easy_whisper* if you want. In this case, you can check this option to tell *easy_whisper* not to split the audio in sentences. It still works if you leave this option unchecked, the only drawback is *easy_whisper* will unnecessarily spend additional time.

MSL
----

*easy_whisper* enhances speed for transcribing longer audio by splitting the speech into sentences, which are detected at the pause between them. The pause, or *MSL* (*minimum silence length*), can be adjusted here. It is recommended to leave the default of 900ms unchanged, but for speakers tending to pause significantly longer or shorter between sentences/clauses you can also adjust this parameter up or down, respectively.

STH
----

The silence is detected at the specified threshold, or *STH* (*silence threshold*). The default value is -16dB and it is recommended to leave it unchanged.

save setting
-------------

Preselected by default, only unselect if necessary. If selected, settings for Path/Language/Model/task(transcribe or translate)/MSL/STH/in_tmp/del_tmp from last usage will be saved for the use next time. It is practical to leave this option selected if the user intends to transcribe files with similar settings over a longer time period. The default models for English and other Languages (including *Auto*) are stored separately - one for English only and one for other languages.

Reset
------

Click this button if you want to reset Path/Language/Model/task(transcribe or translate)/MSL/STH/in_tmp/del_tmp to the system default values, which are current folder/Auto (detection)/small or base.en/transcribe/900ms/-16dB/no/no

transcribe/translate
---------------------

By default, *easy_whisper* transcribes the audio file, but you can also switch to "translate", in which case the (non-English) speech will be translated into English. Click the "Run" button to start transcription/translation, the window is then minimised and you can do something else while waiting. When the job is done, the window reappears to regain your attention. The result is a *.txt* file with the same name and put in the same folder as the audio file. For example, if the path to the audio file is *folder2/audio2.wav*, then the path to the *.txt* file will be *folder2/audio2.txt*. In case of translation, the suffix "_English" will be added, so the output path is then *folder2/audio2_English.txt*. The *.txt* file contains the transcription/translation with time stamps, which looks like below:

[00:00:00,000 --> 00:00:04,000] Chapter 1. Title.
[00:00:04,140 --> 00:00:08,900] Sentence one.
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
 -i, --intmp                in tmp
 -p, --deltmp               del tmp
 -s, --short                short
 -e, --slength              MSL
 -d, --sthreshold           STH
 -v, --sdefault             NOT save setting
 -u, --udefault             Reset
 -t, --task                 transcribe/translate
 -c, --cli  
====================     =========================

Use --help or -h to see help information.

Disclaimer
===========

I wrote *easy_whisper* for my personal use and published it for others who may also find it useful. If you have any question, feel free to ask, but keep in mind that I can only reply in my spare time.
