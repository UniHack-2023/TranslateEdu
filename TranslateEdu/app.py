import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import pygame
import customtkinter as ctk
from customtkinter import *

class VideoApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Modern Video App")
        self.video_path = tk.StringVar()
        self.export_path = tk.StringVar()
        self.selected_language_var = tk.StringVar()
        self.selected_language_to_translate_var = tk.StringVar()

        # Initialize Pygame for audio
        pygame.init()

        self.create_widgets()

    def create_widgets(self):
        custom_font = ctk.CTkFont(family="Barlow", size=15)
        btn_color = '#005900'
        sidebar_frame = tk.Frame(self.master, width=250)
        sidebar_frame.config(bg='#e4d9c5')
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
        logo = Image.open("./logoTransedu.png")
        res_logo = logo.resize((128, 13))

        languages = {
            # ... (existing code)
        }
        language_values = list(languages.keys()) + list(languages.values())

        # Set the default language to "Select language"
        default_language = "Select language"
        default_language2 = "Select Language to translate to:"
        self.selected_language_var.set(default_language)
        self.selected_language_to_translate_var.set(default_language2)

        img = Image.open("./png-transparent-line-triangle-brand-play-button-play-button-icon-angle-text-rectangle-thumbnail.png")
        res_img = img.resize((100, 100))
        img = ImageTk.PhotoImage(res_img)
        video_player_frame = ctk.CTkFrame(self.master)
        video_player_frame.pack(side=tk.RIGHT, padx=40, pady=40, fill=tk.BOTH, expand=True)
        self.video_player_label = ctk.CTkLabel(video_player_frame, text='')
        self.video_player_label.pack()
        self.play_logo = ctk.CTkLabel(video_player_frame, image=img, text="")
        self.play_logo.pack(pady=150)

        logo = ImageTk.PhotoImage(res_logo)
        ctk.CTkLabel(sidebar_frame, text='', image=logo).pack(pady=15)
        ctk.CTkButton(sidebar_frame, text="Select video file", corner_radius=15, command=self.browse_video,
                      font=custom_font, fg_color=btn_color).pack(pady=5)
        ctk.CTkEntry(sidebar_frame, textvariable=self.video_path, state="readonly", font=custom_font).pack(pady=5)
        ctk.CTkButton(sidebar_frame, text="Export Location", corner_radius=15, command=self.browse_export_location,
                      font=custom_font, fg_color=btn_color).pack(pady=5, padx=10)
        ctk.CTkEntry(sidebar_frame, textvariable=self.export_path, state="readonly", font=custom_font).pack(pady=5)
        self.language_menu_to_translate = ctk.CTkComboBox(sidebar_frame, variable=self.selected_language_to_translate_var,
                                                          values=language_values, font=custom_font).pack(pady=5)
        self.language_menu = ctk.CTkComboBox(sidebar_frame, variable=self.selected_language_var,
                                             values=language_values, font=custom_font).pack(pady=5)
        ctk.CTkButton(sidebar_frame, text="Update", corner_radius=15, command=self.apply_changes, font=custom_font,
                      fg_color=btn_color).pack(pady=20)

        # Add a play button for audio
        play_audio_button = ctk.CTkButton(video_player_frame, text="Play Audio", corner_radius=15, command=self.play_audio,
                                          font=custom_font, fg_color=btn_color)
        play_audio_button.pack(pady=10)

    def browse_video(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mkv")])
        if file_path:
            self.video_path.set(file_path)
            self.play_video(file_path)

    def browse_export_location(self):
        export_location = filedialog.askdirectory()
        if export_location:
            self.export_path.set(export_location)

    def play_video(self, file_path):
        cap = cv2.VideoCapture(file_path)

        def update_video():
            ret, frame = cap.read()

            if ret:
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image_tk = ImageTk.PhotoImage(Image.fromarray(image))
                self.video_player_label.configure(image=image_tk)
                self.video_player_label.image = image_tk

                self.master.after(15, update_video)
            else:
                cap.release()

        update_video()

    def play_audio(self):
        audio_path = self.video_path.get()  # You might need to modify this to point to your audio file
        if audio_path:
            # Load and play the audio
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()

    def apply_changes(self):
        selected_language = self.selected_language_var.get()
        selected_language_to_translate = self.selected_language_to_translate_var.get()

        languages = {
            "Afrikaans": "af", "Albanian": "sq", "Amharic": "am", "Arabic": "ar", "Armenian": "hy",
            "Azerbaijani": "az", "Basque": "eu", "Belarusian": "be", "Bengali": "bn", "Bosnian": "bs",
            "Bulgarian": "bg", "Catalan": "ca", "Cebuano": "ceb", "Chichewa": "ny", "Chinese (Simplified)": "zh-cn",
            "Chinese (Traditional)": "zh-tw", "Corsican": "co", "Croatian": "hr", "Czech": "cs",
            "Danish": "da", "Dutch": "nl", "English": "en", "Esperanto": "eo", "Estonian": "et",
            "Filipino": "tl", "Finnish": "fi", "French": "fr", "Frisian": "fy", "Galician": "gl",
            "Georgian": "ka", "German": "de", "Greek": "el", "Gujarati": "gu", "Haitian Creole": "ht",
            "Hausa": "ha", "Hawaiian": "haw", "Hebrew": "iw", "Hindi": "hi", "Hmong": "hmn",
            "Hungarian": "hu", "Icelandic": "is", "Igbo": "ig", "Indonesian": "id", "Irish": "ga",
            "Italian": "it", "Japanese": "ja", "Javanese": "jw", "Kannada": "kn", "Kazakh": "kk",
            "Khmer": "km", "Korean": "ko", "Kurdish (Kurmanji)": "ku", "Kyrgyz": "ky", "Lao": "lo",
            "Latin": "la", "Latvian": "lv", "Lithuanian": "lt", "Luxembourgish": "lb", "Macedonian": "mk",
            "Malagasy": "mg", "Malay": "ms", "Malayalam": "ml", "Maltese": "mt", "Maori": "mi",
            "Marathi": "mr", "Mongolian": "mn", "Burmese": "my", "Nepali": "ne", "Norwegian": "no",
            "Pashto": "ps", "Persian": "fa", "Polish": "pl", "Portuguese": "pt", "Punjabi": "pa",
            "Romanian": "ro", "Russian": "ru", "Samoan": "sm", "Scots Gaelic": "gd", "Serbian": "sr",
            "Sesotho": "st", "Shona": "sn", "Sindhi": "sd", "Sinhala": "si", "Slovak": "sk",
            "Slovenian": "sl", "Somali": "so", "Spanish": "es", "Sundanese": "su", "Swahili": "sw",
            "Swedish": "sv", "Tajik": "tg", "Tamil": "ta", "Telugu": "te", "Thai": "th", "Turkish": "tr",
            "Ukrainian": "uk", "Urdu": "ur", "Uyghur": "ug", "Uzbek": "uz", "Vietnamese": "vi",
            "Welsh": "cy", "Xhosa": "xh", "Yiddish": "yi", "Yoruba": "yo", "Zulu": "zu"
        }
        selected_language_code = languages.get(selected_language, "")
        selected_language_to_translate_code = languages.get(selected_language_to_translate, "")

        print("Selected Video:", self.video_path.get())
        print("Export Location:", self.export_path.get())
        print("Selected Language:", selected_language_code)
        print("Selected Language to translate to:", selected_language_to_translate_code)

if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg='#f2ece2')
    app = VideoApp(root)
    root.geometry("800x500")
    root.mainloop()
