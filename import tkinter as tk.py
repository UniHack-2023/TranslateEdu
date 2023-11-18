import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
from customtkinter import *
import cv2
from PIL import Image, ImageTk

class VideoApp:
    def _init_(self, master):
        self.master = master
        self.master.title("Modern Video App")

        self.video_path = tk.StringVar()
        self.export_path = tk.StringVar()
        self.selected_language_var = tk.StringVar()
        self.selected_language_to_translate_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        # Create a sidebar frame to hold all widgets
        sidebar_frame = ctk.CTkFrame(self.master, width=200)
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Video Selection
        ctk.CTkLabel(sidebar_frame, text="Select Video File:", font=("Arial", 12)).pack(pady=10)
        ctk.CTkEntry(sidebar_frame, textvariable=self.video_path, state="readonly", font=("Arial", 10)).pack(pady=5)
        ctk.CTkButton(sidebar_frame, text="Browse", command=self.browse_video, font=("Arial", 10)).pack(pady=5)

        # Export Location
        ctk.CTkLabel(sidebar_frame, text="Export Location:", font=("Arial", 12)).pack(pady=10)
        ctk.CTkEntry(sidebar_frame, textvariable=self.export_path, state="readonly", font=("Arial", 10)).pack(pady=5)
        ctk.CTkButton(sidebar_frame, text="Select Export Location", command=self.browse_export_location, font=("Arial", 10)).pack(pady=5)

        # Language Selection
        ctk.CTkLabel(sidebar_frame, text="Select Language:", font=("Arial", 12)).pack(pady=10)
        languages = ["English", "Spanish", "French", "German", "Other"]
        self.language_menu = ctk.CTkComboBox(sidebar_frame, variable=self.selected_language_var, values=languages)
        self.language_menu.pack(pady=5)
        ctk.CTkLabel(sidebar_frame, text="Select Language to translate to:", font=("Arial", 12)).pack(pady=10)
        self.language_menu_to_translate = ctk.CTkComboBox(sidebar_frame, variable=self.selected_language_to_translate_var, values=languages)
        self.language_menu_to_translate.pack(pady=5)

        # Apply Button
        ctk.CTkButton(sidebar_frame, text="Update", corner_radius=15, command=self.apply_changes, font=("Arial", 12, "bold")).pack(pady=20)

        # Create a frame for the video player on the right side
        video_player_frame = ctk.CTkFrame(self.master)
        video_player_frame.pack(side=tk.RIGHT, padx=40, pady=40, fill=tk.BOTH, expand=True)

        # Canvas for displaying video frames
        self.video_player_label = ctk.CTkLabel(video_player_frame,text='')
        self.video_player_label.pack()


    def browse_video(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video files", ".mp4;.avi;*.mkv")])
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
                # Convert OpenCV BGR image to Pillow (PIL) RGB image
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Convert to ImageTk format
                image_tk = ImageTk.PhotoImage(Image.fromarray(image))
                self.video_player_label.configure(image=image_tk)
                self.video_player_label.image = image_tk

                self.master.after(10, update_video)
            else:
                cap.release()

        update_video()

    def apply_changes(self):
        print("Selected Video:", self.video_path.get())
        print("Export Location:", self.export_path.get())
        print("Selected Language:", self.selected_language_var.get())
        print("Selected Language to translate to:", self.selected_language_to_translate_var.get())

if _name_ == "_main_":
    root = ctk.CTk()
    app = VideoApp(root)
    root.geometry("800x500")  # Adjust the window size as needed
    root.mainloop()