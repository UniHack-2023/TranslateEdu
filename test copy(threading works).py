import threading
import tkinter as tk
from tkinter import ttk, filedialog
import customtkinter as ctk
from pytube import YouTube
import subprocess
import os
from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer

# Replace 'D:\TTS\TTS\.models.json' with the correct path
path = "D:\\TTS\\TTS\\.models.json"

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
        btn_color = '#005900'
        sidebar_frame = tk.Frame(self.master, width=250)
        sidebar_frame.config(bg='#e4d9c5')
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
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
        self.label = ctk.CTkLabel(sidebar_frame, text="Enter a YouTube link and download the audio:", text_color="black").pack(pady=10)
        self.input_entry = tk.Entry(sidebar_frame, width=50)
        self.input_entry.pack()
        self.download_button = ctk.CTkButton(sidebar_frame, text="Download Audio", command=self.download_audio,
                                             fg_color=btn_color).pack(pady=10)
        self.label = ctk.CTkLabel(sidebar_frame, text="Or select an existing audio file:", text_color="black").pack(pady=10)
        self.select_button = ctk.CTkButton(sidebar_frame, text="Select File", command=self.select_file,
                                           fg_color=btn_color).pack(pady=10)
        self.selected_language = ctk.StringVar()
        self.language_label = ctk.CTkLabel(sidebar_frame, text="Select input language:", text_color="black").pack(
            pady=10)
        self.language_dropdown = ttk.Combobox(sidebar_frame, textvariable=self.selected_language)
        self.language_dropdown['values'] = list(self.languages.values())
        self.language_dropdown.pack()
        self.translate_button = ctk.CTkButton(sidebar_frame, text="Translate", command=self.translate,
                                              fg_color=btn_color).pack(pady=10)

        self.output_text = tk.Text(master, height=25, width=60)
        self.output_text.pack(pady=30, padx=30)

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
    root.configure(bg='#f2ece2')
    root.geometry("800x500")
    app = AudioTranslatorApp(root)
    root.mainloop()