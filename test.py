import tkinter as tk
from tkinter import ttk, filedialog
import customtkinter as ctk
from pytube import YouTube
import subprocess
import os
from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer
import threading

# Replace 'D:\TTS\TTS\.models.json' with the correct path
path = "F:\\TTS\\TTS\\.models.json"

model_manager = ModelManager(path)

model_path, config_path, model_item = model_manager.download_model("tts_models/en/ljspeech/tacotron2-DDC")

voc_path, voc_config_path, _ = model_manager.download_model(model_item["default_vocoder"])
syn = Synthesizer(
    tts_checkpoint=model_path,
    tts_config_path=config_path,
    vocoder_checkpoint=voc_path,
    vocoder_config=voc_config_path
)

class AudioTranslatorApp:
    def __init__(self, master):
        self.master = master
        self.video_path = tk.StringVar()
        custom_font = ctk.CTkFont(family="Barlow", size=1)
        master.title("Audio Translator App")    

        # Language dropdown
        self.languages = {
            "af": "Afrikaans", "sq": "Albanian", "am": "Amharic", "ar": "Arabic", "hy": "Armenian",
            "az": "Azerbaijani", "eu": "Basque", "be": "Belarusian", "bn": "Bengali", "bs": "Bosnian",
            "bg": "Bulgarian", "ca": "Catalan", "ceb": "Cebuano", "ny": "Chichewa", "zh-cn": "Chinese (Simplified)",
            "zh-tw": "Chinese (Traditional)", "co": "Corsican", "hr": "Croatian", "cs": "Czech",
            "da": "Danish", "nl": "Dutch", "en": "English", "eo": "Esperanto", "et": "Estonian",
            "tl": "Filipino", "fi": "Finnish", "fr": "French", "fy": "Frisian", "gl": "Galician",
            "ka": "Georgian", "de": "German", "el": "Greek", "gu": "Gujarati", "ht": "Haitian Creole",
            "ha": "Hausa", "haw": "Hawaiian", "iw": "Hebrew", "hi": "Hindi", "hmn": "Hmong",
            "hu": "Hungarian", "is": "Icelandic", "ig": "Igbo", "id": "Indonesian", "ga": "Irish",
            "it": "Italian", "ja": "Japanese", "jw": "Javanese", "kn": "Kannada", "kk": "Kazakh",
            "km": "Khmer", "ko": "Korean", "ku": "Kurdish (Kurmanji)", "ky": "Kyrgyz", "lo": "Lao",
            "la": "Latin", "lv": "Latvian", "lt": "Lithuanian", "lb": "Luxembourgish", "mk": "Macedonian",
            "mg": "Malagasy", "ms": "Malay", "ml": "Malayalam", "mt": "Maltese", "mi": "Maori",
            "mr": "Marathi", "mn": "Mongolian", "my": "Burmese", "ne": "Nepali", "no": "Norwegian",
            "ps": "Pashto", "fa": "Persian", "pl": "Polish", "pt": "Portuguese", "pa": "Punjabi",
            "ro": "Romanian", "ru": "Russian", "sm": "Samoan", "gd": "Scots Gaelic", "sr": "Serbian",
            "st": "Sesotho", "sn": "Shona", "sd": "Sindhi", "si": "Sinhala", "sk": "Slovak",
            "sl": "Slovenian", "so": "Somali", "es": "Spanish", "su": "Sundanese", "sw": "Swahili",
            "sv": "Swedish", "tg": "Tajik", "ta": "Tamil", "te": "Telugu", "th": "Thai", "tr": "Turkish",
            "uk": "Ukrainian", "ur": "Urdu", "ug": "Uyghur", "uz": "Uzbek", "vi": "Vietnamese",
            "cy": "Welsh", "xh": "Xhosa", "yi": "Yiddish", "yo": "Yoruba", "zu": "Zulu"
        }
        self.top_frame = tk.Frame(self.master, bg='#f2ece2')
        self.middle_frame = tk.Frame(self.master, bg='#e4d9c5')
        self.bottom_frame = tk.Frame(self.master, bg='#586e6b')

        # Store the initial window size
        self.prev_width = self.master.winfo_width()
        self.prev_height = self.master.winfo_height()

        # Configure row and column weights for each frame
        self.master.grid_rowconfigure(0, weight=0)
        self.master.grid_rowconfigure(1, weight=0)
        self.master.grid_rowconfigure(2, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)

        self.top_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.middle_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")
        self.bottom_frame.grid(row=2, column=0, columnspan=2, sticky="nsew")

        self.add_top_frame_content()
        self.add_middle_frame_content()
        self.add_bottom_frame_content()

        # Center the window
        self.master.update_idletasks()
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width - self.master.winfo_width()) 
        y = (screen_height - self.master.winfo_height()) 
        self.master.geometry("+{}+{}".format(x, y))

        # Bind the window resize event
        self.master.bind("<Configure>", self.on_window_configure)
        
    
    def on_window_configure(self, event):
        # Check if the window is being resized larger
        if event.width > self.prev_width or event.height > self.prev_height or event.width < self.prev_width or event.height < self.prev_height:
            # Update button and entry heights based on the window size
            button_height = int(self.master.winfo_height() / 7)
            entry_font_size = int(self.master.winfo_height() / 40)

            self.download_button.configure(height=button_height)
            self.select_button.configure(height=button_height)
            self.translate_button.configure(height=button_height)
            self.input_entry.configure(font=("TkDefaultFont", entry_font_size))

            # Update the previous window size
            self.prev_width = event.width
            self.prev_height = event.height

    def add_top_frame_content(self):
        custom_font = ctk.CTkFont(family="Barlow", size=1)

        self.video_path = tk.StringVar()
        self.download_button = ctk.CTkButton(self.top_frame, text="Download Audio", command=self.download_audio,
                                             fg_color='#005900')
        self.download_button.grid(row=0, column=0, columnspan=1, rowspan=1, pady=10, padx=10, sticky="nsew")
        self.select_button = ctk.CTkButton(self.top_frame, text="Select File", command=self.select_file,
                                           fg_color='#005900')
        self.select_button.grid(row=0, column=1, pady=10, sticky="nsew")
        self.input_entry = tk.Entry(self.top_frame, textvariable=self.video_path, width=40)
        self.input_entry.insert(0, 'Link or video location')
        self.input_entry.grid(row=0, column=2, columnspan=2, sticky=tk.E + tk.W, padx=10)

        # Configure column weights for the top frame
        self.top_frame.grid_columnconfigure(0, weight=1)
        self.top_frame.grid_columnconfigure(1, weight=1)
        self.top_frame.grid_columnconfigure(2, weight=1)
        self.top_frame.grid_columnconfigure(3, weight=1)

    def add_middle_frame_content(self):
        self.selected_language = ctk.StringVar()
        self.language_label = ctk.CTkLabel(self.middle_frame, text="Select input language:", text_color="black",font=("Barlow",25))
        self.language_label.grid(row=0, column=0, padx=120, sticky=tk.W)
        self.language_dropdown = ttk.Combobox(self.middle_frame, textvariable=self.selected_language,width=50,font="Barlow")
        self.language_dropdown['values'] = list(self.languages.values())
        self.language_dropdown.grid(row=1, column=0, padx=30, pady=0, sticky=tk.W)
        self.translate_button = ctk.CTkButton(self.middle_frame, text="Start", command=self.translate,
                                              fg_color='#005900')
        self.translate_button.grid(column=1, rowspan=2, row=0, sticky="nsew", padx=30, pady=10)

        # Configure column weights for the middle frame
        self.middle_frame.grid_columnconfigure(0, weight=1)
        self.middle_frame.grid_columnconfigure(1, weight=1)

    def add_bottom_frame_content(self):
        self.output_text = tk.Text(self.bottom_frame, height=8, width=50, bg='#b6c2aa', borderwidth=0)
        self.output_text.pack(pady=20, padx=20, side="bottom", fill="both", expand=True)

        # Configure row weight for the bottom frame
        self.bottom_frame.grid_rowconfigure(0, weight=1)

    def download_audio(self):
        video_url = self.input_entry.get().strip()
        if not video_url.startswith("https://www.youtube.com/"):
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, "Please enter a valid YouTube link.")
            return

        try:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, "Downloading audio...")

            audio_path = self.download_youtube_audio(video_url)

            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f"Audio downloaded successfully: {audio_path}")

        except ValueError as e:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f"Error: {e}")

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.mp3;*.wav;*.ogg")])
        if file_path:
            self.video_path.set(file_path)

    def download_youtube_audio(self, video_url):
        try:
            yt = YouTube(video_url)
            audio_stream = yt.streams.filter(only_audio=True).first()
            audio_path = os.path.join(os.getcwd(), "temp_audio.mp3")
            audio_stream.download(output_path=os.getcwd(), filename="temp_audio.mp3")
            return audio_path
        except Exception as e:
            raise ValueError(f"Error downloading audio from YouTube: {e}")

    def translate_threaded(self):
        try:
            input_text = self.video_path.get().strip()
            if not input_text or (
                    not input_text.startswith("https://www.youtube.com/") and not os.path.isfile(input_text)):
                raise ValueError("Please provide a valid YouTube link or select an existing audio file.")

            if input_text.startswith("https://www.youtube.com/"):
                audio_path = os.path.join(os.getcwd(), "temp_audio.mp3")
                if not os.path.isfile(audio_path):
                    raise ValueError("Please download the audio first.")
            else:
                audio_path = input_text

            if not os.path.isfile(audio_path):
                raise ValueError(f"Audio file not found: {audio_path}")

            input_lang_code = [code for code, lang in self.languages.items() if lang == self.selected_language.get()][0]
            translation_command = f'whisper "{audio_path}" --task translate --language {input_lang_code} --model medium'
            translation_output = subprocess.check_output(translation_command, shell=False, text=True)
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, translation_output)

            translation_file_path = os.path.splitext(audio_path)[0] + ".txt"
            # Read the translated text from the file
            with open(translation_file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                # Keep only the text from the first line and remove new lines
                text = ''.join(lines).replace('\n', '')

            # Generate a new audio file
            outputs = syn.tts(text)
            syn.save_wav(outputs, "audio-1.wav")

        except subprocess.CalledProcessError as e:
            self.output_text.delete(1.0, tk.END)  # Clear previous output
            self.output_text.insert(tk.END, f"Error during translation: {e}")
        except ValueError as e:
            self.output_text.delete(1.0, tk.END)  # Clear previous output
            self.output_text.insert(tk.END, f"Error: {e}")

    def translate(self):
        # Create a new thread for translation
        translation_thread = threading.Thread(target=self.translate_threaded)
        translation_thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('1000x550')
    root.resizable(False,False)
    app = AudioTranslatorApp(root)
    root.mainloop()
