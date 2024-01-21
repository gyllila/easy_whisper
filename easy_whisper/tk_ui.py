from tkinter import filedialog, Toplevel, Label, Entry, Radiobutton, Button, Checkbutton, OptionMenu, BooleanVar, StringVar, LEFT, SOLID, END, Tk
from .trans import transcribe_chunks_m
from .ui_share import default_params, parse_path, usr_par_path, init_params
import os

had_action = False
if init_params['init_file_directory'] is None:
    input_dir = default_params['file_directory']
else:
    input_dir = init_params['init_file_directory']
if init_params['init_language'] is None:
    language = default_params['language']
else:
    language = init_params['init_language']
if init_params['init_task'] is None:
    task = default_params['task']
else:
    task = init_params['init_task']
if init_params['init_model_en'] is None:
    default_model_en = default_params['model_en']
else:
    default_model_en = init_params['init_model_en']
if init_params['init_model'] is None:
    default_model = default_params['model']
else:
    default_model = init_params['init_model']
if language == 'English' or language == 'en':
    model = default_model_en
else:
    model = default_model
if init_params['init_min_silence_len'] is None:
    slength = default_params['min_silence_len']
else:
    slength = init_params['init_min_silence_len']
if init_params['init_silence_thresh'] is None:
    sthreshold = default_params['silence_thresh']
else:
    sthreshold = init_params['init_silence_thresh']
if init_params['init_in_tmp'] is None:
    intmp = default_params['in_tmp']
else:
    intmp = init_params['init_in_tmp']
if init_params['init_del_tmp'] is None:
    deltmp = default_params['del_tmp']
else:
    deltmp = init_params['init_del_tmp']
try:
    input_file, input_dir = parse_path(input_dir)
    file_path = os.path.join(input_dir, input_file)
except FileNotFoundError as fe:
    input_file = ''
    input_dir = ''
    file_path = f"{fe} Select an audio file with the button right."
        
class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() # + 57
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT, fg='#000',
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

class MainWindow(object):
    def __init__(self):
        self.root = Tk()
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        w = 1150
        h = 500
        x = (ws/2)-(w/2)
        y=(hs/2)-(h/2)
        self.root.geometry('%dx%d+%d+%d' % (w,h,x,y)) 
        self.root.title("Easy_Whisper")

        self.entry_path_label = Label(self.root, text="Path:")
        self.entry_path_label.grid(row=0, column=0, padx=10, pady=10)

        self.path_content = StringVar()
        self.path_content.set(file_path)

        self.entry_path = Entry(self.root, width=95, textvariable=self.path_content, state='readonly')
        self.entry_path.grid(row=0, column=1, columnspan=10, padx=10, pady=10)
        CreateToolTip(self.entry_path, text = 'The path to the audio file')

        self.button_choose_file = Button(self.root, width=8, text="Choose File", command=self.get_directory_from_user)
        self.button_choose_file.grid(row=0, column=11, padx=10, pady=10)
        CreateToolTip(self.button_choose_file, text = 'Choose audio file path')

        self.lang_var_label = Label(self.root, text="Language:", anchor="e")
        self.lang_var_label.grid(row=1, column=0, padx=10, pady=10)

        self.lang_var = StringVar()
        self.lang_var.set(language)
        self.lang_var.trace("w", self.set_default_model)
        self.langs_menu = OptionMenu(self.root, self.lang_var, 'Auto', 'Afrikaans','Albanian','Amharic','Arabic','Armenian','Assamese','Azerbaijani','Bashkir','Basque','Belarusian','Bengali','Bosnian','Breton','Bulgarian','Burmese','Castilian','Catalan','Chinese','Croatian','Czech','Danish','Dutch','English','Estonian','Faroese','Finnish','Flemish','French','Galician','Georgian','German','Greek','Gujarati','Haitian','Haitian Creole','Hausa','Hawaiian','Hebrew','Hindi','Hungarian','Icelandic','Indonesian','Italian','Japanese','Javanese','Kannada','Kazakh','Khmer','Korean','Lao','Latin','Latvian','Letzeburgesch','Lingala','Lithuanian','Luxembourgish','Macedonian','Malagasy','Malay','Malayalam','Maltese','Maori','Marathi','Moldavian','Moldovan','Mongolian','Myanmar','Nepali','Norwegian','Nynorsk','Occitan','Panjabi','Pashto','Persian','Polish','Portuguese','Punjabi','Pushto','Romanian','Russian','Sanskrit','Serbian','Shona','Sindhi','Sinhala','Sinhalese','Slovak','Slovenian','Somali','Spanish','Sundanese','Swahili','Swedish','Tagalog','Tajik','Tamil','Tatar','Telugu','Thai','Tibetan','Turkish','Turkmen','Ukrainian','Urdu','Uzbek','Valencian','Vietnamese','Welsh','Yiddish','Yoruba')
        self.langs_menu.grid(row=1, column=1, padx=10, pady=10)
        CreateToolTip(self.langs_menu, text = 'Choose language of the audio file. If unknown, choose Auto for auto detection.')

        self.model_var_label = Label(self.root, text="Model:", anchor="e")
        self.model_var_label.grid(row=1, column=2, padx=10, pady=10)

        self.model_var = StringVar()
        self.model_var.set(model)
        self.models_menu = OptionMenu(self.root, self.model_var, "tiny.en", "base.en", "small.en", "medium.en", "tiny", "base", "small", "medium", "large-v1", "large-v2", "large")
        self.models_menu.grid(row=1, column=3, padx=10, pady=10)
        CreateToolTip(self.models_menu, text = 'Choose model. Smaller model is faster, larger one is of higher quality.')

        self.split_var = BooleanVar()
        if intmp == 'true':
            self.split_var.set(True)
        else:
            self.split_var.set(False)
        self.checkbox_split = Checkbutton(self.root, text="in tmp", variable=self.split_var)
        self.checkbox_split.grid(row=1, column=7, padx=10, pady=10)
        CreateToolTip(self.checkbox_split, text = 'Check if the audio file is already split in sentences and stored in the tmp folder.')

        self.deltmp_var = BooleanVar()
        if deltmp == 'true':
            self.deltmp_var.set(True)
        else:
            self.deltmp_var.set(False)
        self.checkbox_deltmp = Checkbutton(self.root, text="del tmp", variable=self.deltmp_var)
        self.checkbox_deltmp.grid(row=1, column=10, padx=10, pady=10)
        CreateToolTip(self.checkbox_deltmp, text = 'Check to delete the tmp folder after job done.')

        self.short_var = BooleanVar()
        self.short_var.set(False)
        self.checkbox_short = Checkbutton(self.root, text="short", variable=self.short_var)
        self.checkbox_short.grid(row=1, column=11, padx=10, pady=10)
        CreateToolTip(self.checkbox_short, text = "Check if the audio file is short (<1m)\nand doesn't need to be split in sentences.")

        self.entry_msl_label = Label(self.root, text="MSL:", anchor="e")
        self.entry_msl_label.grid(row=2, column=0, padx=10, pady=10)

        self.entry_msl = Entry(self.root, width=10)
        self.entry_msl.insert(0, str(slength))
        self.entry_msl.grid(row=2, column=1, padx=10, pady=10)
        CreateToolTip(self.entry_msl, text = 'Minimum silence length in milliseconds to split audio file.')

        self.entry_sth_label = Label(self.root, text="STH:", anchor="e")
        self.entry_sth_label.grid(row=2, column=2, padx=10, pady=10)

        self.entry_sth = Entry(self.root, width=10)
        self.entry_sth.insert(0, str(sthreshold))
        self.entry_sth.grid(row=2, column=3, padx=10, pady=10)
        CreateToolTip(self.entry_sth, text = 'Silence threshold for detecting silence, default is -16dB.')

        self.save_var = BooleanVar()
        self.save_var.set(True)
        self.checkbox_save = Checkbutton(self.root, text="save setting", variable=self.save_var)
        self.checkbox_save.grid(row=2, column=7, padx=10, pady=10)
        CreateToolTip(self.checkbox_save, text = 'Check to save most recently used settings for\npath, lang, model, task, MSL, STH, in_tmp and del_tmp.')

        self.button_use_sysd = Button(self.root, width=8, text="Reset", command=self.reset_default_values)
        self.button_use_sysd.grid(row=2, column=10, padx=10, pady=10)
        CreateToolTip(self.button_use_sysd, text = 'Reset path, lang, model, task, MSL, STH, in_tmp and del_tmp')

        self.task_var = StringVar(self.root, task)
        self.task1 = Radiobutton(self.root, text='transcribe', value='transcribe', variable=self.task_var)
        self.task1.grid(row=3, column=1, pady=10)
        CreateToolTip(self.task1, text = 'Check to transcribe audio file by pressing "Run" button.')
        self.task2 = Radiobutton(self.root, text='translate', value='translate', variable=self.task_var)
        self.task2.grid(row=3, column=2, pady=10)
        CreateToolTip(self.task2, text = 'Check to translate audio file (into English) by pressing "Run" button.')
        self.button_run = Button(self.root, width=8, text="Run", command=self.transcribe_chunks_m_gui)
        self.button_run.grid(row=3, column=3, pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.good_bye)

    def good_bye(self):
        self.root.withdraw()
        if had_action and self.save_var.get():
            import json
            if language == 'English':
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
                'init_model_en': this_model_en, 
                'init_min_silence_len': slength, 
                'init_silence_thresh': sthreshold, 
                'init_in_tmp': intmp, 
                'init_del_tmp': deltmp
            }
            with open(usr_par_path, 'w') as f:
                json.dump(json_params, f, indent=4)
        self.root.destroy()

    def set_default_model(self, *args):
        if self.lang_var.get()=="English":
            self.model_var.set(default_model_en)
        else:
            self.model_var.set(default_model)

    def get_directory_from_user(self):
    
        global input_dir, input_file
        directory = filedialog.askopenfilename(title="Select File to Transcribe or Translate", filetypes=[("audio files",".mp3 .mp4 .mpeg .mpga .m4a .wav .webm .wma")], parent=self.root, initialdir=input_dir)
        
        if not directory:
            return

        self.path_content.set(directory)
        input_dir = os.path.dirname(directory)
        input_file = os.path.basename(directory)

    def reset_default_values(self):
        global input_file, input_dir, file_path
        global language, task, default_model_en, default_model, model, slength, sthreshold, intmp, deltmp
        input_dir = default_params['file_directory']
        language = default_params['language']
        task = default_params['task']
        default_model_en = default_params['model_en']
        default_model = default_params['model']
        if language == 'English' or language == 'en':
            model = default_model_en
        else:
            model = default_model
        slength = default_params['min_silence_len']
        sthreshold = default_params['silence_thresh']
        intmp = default_params['in_tmp']
        deltmp = default_params['del_tmp']
        try:
            input_file, input_dir = parse_path(input_dir)
            file_path = os.path.join(input_dir, input_file)
        except FileNotFoundError as fe:
            input_file = ''
            input_dir = ''
            file_path = f"{fe} Select an audio file with the button right."
        self.path_content.set(file_path)
        self.lang_var.set(language)
        self.task_var.set(task)
        self.model_var.set(model)
        self.entry_msl.delete(0, END)
        self.entry_msl.insert(0, str(slength))
        self.entry_sth.delete(0, END)
        self.entry_sth.insert(0, str(sthreshold))
        if intmp == 'true':
            self.split_var.set(True)
        else:
            self.split_var.set(False)
        if deltmp == 'true':
            self.deltmp_var.set(True)
        else:
            self.deltmp_var.set(False)

    def get_tk_values(self):
        global input_file, input_dir, file_path
        global language, task, model, slength, sthreshold, intmp, deltmp, short # sdefault,
        file_path = self.entry_path.get()
        if file_path.endswith("Select an audio file with the button right."):
            input_dir = ""
            input_file = ""
        else:
            input_dir = os.path.dirname(file_path)
            input_file = os.path.basename(file_path)
        language = self.lang_var.get()
        task = self.task_var.get()
        model = self.model_var.get()
        slength = int(self.entry_msl.get())
        sthreshold = int(self.entry_sth.get())
        intmpb = self.split_var.get()
        if intmpb:
            intmp = "true"
        else:
            intmp = "false"
        deltmpb = self.deltmp_var.get()
        if deltmpb:
            deltmp = "true"
        else:
            deltmp = "false"
        short = self.short_var.get()
        
    def transcribe_chunks_m_gui(self):
        self.get_tk_values()
        if input_file == "":
            return
        self.root.iconify()
        transcribe_chunks_m(input_dir=input_dir, input_file=input_file, language=language, task=task, model=model, slength=slength, sthreshold=sthreshold, short=short, intmp=intmp, deltmp=deltmp)
        global had_action
        had_action = True
        self.root.deiconify()
    
w = MainWindow()
w.root.mainloop()



