import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
from pathlib import Path
import webbrowser
from audio_splitter_librosa import AudioSplitter
from youtube_downloader import YouTubeDownloader, is_valid_youtube_url

class MusicSplitterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Splitter - Vocal/Instrumental Separator")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Initialize components
        self.audio_splitter = None
        self.youtube_downloader = None
        self.current_file = None
        
        # Create GUI components
        self.setup_ui()
        
        # Initialize backend components in a separate thread
        threading.Thread(target=self.initialize_backend, daemon=True).start()
    
    def setup_ui(self):
        """Create and setup the user interface."""
        # Main notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Tab 1: Local File Processing
        self.file_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.file_frame, text="Local Files")
        self.setup_file_tab()
        
        # Tab 2: YouTube Processing
        self.youtube_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.youtube_frame, text="YouTube")
        self.setup_youtube_tab()
        
        # Tab 3: Settings
        self.settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_frame, text="Settings")
        self.setup_settings_tab()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Initializing...")
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def setup_file_tab(self):
        """Setup the local file processing tab."""
        # File selection frame
        file_select_frame = ttk.LabelFrame(self.file_frame, text="Select Audio File", padding=10)
        file_select_frame.pack(fill='x', padx=10, pady=5)
        
        self.file_path_var = tk.StringVar()
        file_entry = ttk.Entry(file_select_frame, textvariable=self.file_path_var, state='readonly')
        file_entry.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        browse_btn = ttk.Button(file_select_frame, text="Browse", command=self.browse_file)
        browse_btn.pack(side='right')
        
        # Output directory frame
        output_frame = ttk.LabelFrame(self.file_frame, text="Output Directory", padding=10)
        output_frame.pack(fill='x', padx=10, pady=5)
        
        self.output_dir_var = tk.StringVar()
        self.output_dir_var.set(str(Path.cwd() / "output"))
        
        output_entry = ttk.Entry(output_frame, textvariable=self.output_dir_var)
        output_entry.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        output_browse_btn = ttk.Button(output_frame, text="Browse", command=self.browse_output_dir)
        output_browse_btn.pack(side='right')
        
        # Control buttons
        control_frame = ttk.Frame(self.file_frame)
        control_frame.pack(fill='x', padx=10, pady=10)
        
        self.split_btn = ttk.Button(control_frame, text="Split Audio", 
                                   command=self.split_local_file, state='disabled')
        self.split_btn.pack(side='left', padx=(0, 5))
        
        self.play_vocal_btn = ttk.Button(control_frame, text="Play Vocals", 
                                        command=self.play_vocals, state='disabled')
        self.play_vocal_btn.pack(side='left', padx=5)
        
        self.play_instrumental_btn = ttk.Button(control_frame, text="Play Instrumental", 
                                               command=self.play_instrumental, state='disabled')
        self.play_instrumental_btn.pack(side='left', padx=5)
        
        # Progress bar
        self.file_progress = ttk.Progressbar(self.file_frame, mode='indeterminate')
        self.file_progress.pack(fill='x', padx=10, pady=5)
        
        # Log area
        log_frame = ttk.LabelFrame(self.file_frame, text="Processing Log", padding=10)
        log_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.file_log = scrolledtext.ScrolledText(log_frame, height=10, state='disabled')
        self.file_log.pack(fill='both', expand=True)
    
    def setup_youtube_tab(self):
        """Setup the YouTube processing tab."""
        # URL input frame
        url_frame = ttk.LabelFrame(self.youtube_frame, text="YouTube URL", padding=10)
        url_frame.pack(fill='x', padx=10, pady=5)
        
        self.youtube_url_var = tk.StringVar()
        url_entry = ttk.Entry(url_frame, textvariable=self.youtube_url_var)
        url_entry.pack(fill='x', padx=(0, 5))
        
        # Add placeholder functionality manually
        placeholder_text = "Enter YouTube URL here..."
        
        def add_placeholder():
            if not self.youtube_url_var.get():
                url_entry.insert(0, placeholder_text)
                url_entry.config(foreground='grey')
        
        def remove_placeholder(event=None):  # pylint: disable=unused-argument
            if url_entry.get() == placeholder_text:
                url_entry.delete(0, tk.END)
                url_entry.config(foreground='black')
        
        def validate_url(event=None):  # pylint: disable=unused-argument
            if not url_entry.get():
                add_placeholder()
        
        url_entry.bind('<FocusIn>', remove_placeholder)
        url_entry.bind('<FocusOut>', validate_url)
        add_placeholder()
        
        # YouTube control buttons
        yt_control_frame = ttk.Frame(self.youtube_frame)
        yt_control_frame.pack(fill='x', padx=10, pady=10)
        
        self.yt_info_btn = ttk.Button(yt_control_frame, text="Get Info", 
                                     command=self.get_youtube_info, state='disabled')
        self.yt_info_btn.pack(side='left', padx=(0, 5))
        
        self.yt_download_btn = ttk.Button(yt_control_frame, text="Download & Split", 
                                         command=self.download_and_split, state='disabled')
        self.yt_download_btn.pack(side='left', padx=5)
        
        # YouTube settings
        yt_settings_frame = ttk.LabelFrame(self.youtube_frame, text="Download Settings", padding=10)
        yt_settings_frame.pack(fill='x', padx=10, pady=5)
        
        self.keep_original_var = tk.BooleanVar(value=True)
        keep_check = ttk.Checkbutton(yt_settings_frame, text="Keep original downloaded file", 
                                    variable=self.keep_original_var)
        keep_check.pack(anchor='w')
        
        # Progress bar
        self.youtube_progress = ttk.Progressbar(self.youtube_frame, mode='indeterminate')
        self.youtube_progress.pack(fill='x', padx=10, pady=5)
        
        # YouTube log area
        yt_log_frame = ttk.LabelFrame(self.youtube_frame, text="Download Log", padding=10)
        yt_log_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.youtube_log = scrolledtext.ScrolledText(yt_log_frame, height=10, state='disabled')
        self.youtube_log.pack(fill='both', expand=True)
    
    def setup_settings_tab(self):
        """Setup the settings tab."""
        # Audio settings
        audio_settings_frame = ttk.LabelFrame(self.settings_frame, text="Audio Settings", padding=10)
        audio_settings_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(audio_settings_frame, text="Output Format:").pack(anchor='w')
        self.output_format_var = tk.StringVar(value="wav")
        format_combo = ttk.Combobox(audio_settings_frame, textvariable=self.output_format_var,
                                   values=["wav", "mp3", "flac"], state='readonly')
        format_combo.pack(fill='x', pady=(0, 10))
        
        ttk.Label(audio_settings_frame, text="Audio Quality:").pack(anchor='w')
        self.quality_var = tk.StringVar(value="high")
        quality_combo = ttk.Combobox(audio_settings_frame, textvariable=self.quality_var,
                                    values=["low", "medium", "high"], state='readonly')
        quality_combo.pack(fill='x')
        
        # About section
        about_frame = ttk.LabelFrame(self.settings_frame, text="About", padding=10)
        about_frame.pack(fill='x', padx=10, pady=5)
        
        about_text = """Music Splitter v1.0
        
This application uses AI-powered source separation to split audio files into vocal and instrumental tracks.

Technology:
• Spleeter - Source separation model by Deezer
• yt-dlp - YouTube downloading
• librosa - Audio processing

Features:
• Local file processing
• YouTube integration
• Batch processing support"""
        
        about_label = ttk.Label(about_frame, text=about_text, justify='left')
        about_label.pack(anchor='w')
    
    def initialize_backend(self):
        """Initialize audio splitter and YouTube downloader."""
        try:
            self.status_var.set("Loading AI models...")
            self.audio_splitter = AudioSplitter()
            self.youtube_downloader = YouTubeDownloader()
            
            # Enable buttons
            self.root.after(0, self.enable_controls)
            self.status_var.set("Ready")
            
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            messagebox.showerror("Initialization Error", 
                               f"Failed to initialize audio processing:\n{str(e)}")
    
    def enable_controls(self):
        """Enable UI controls after backend initialization."""
        self.split_btn.config(state='normal')
        self.yt_info_btn.config(state='normal')
        self.yt_download_btn.config(state='normal')
    
    def browse_file(self):
        """Browse for audio file."""
        file_path = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=[
                ("Audio Files", "*.mp3 *.wav *.flac *.m4a *.aac"),
                ("MP3 Files", "*.mp3"),
                ("WAV Files", "*.wav"),
                ("All Files", "*.*")
            ]
        )
        if file_path:
            self.file_path_var.set(file_path)
            self.current_file = file_path
    
    def browse_output_dir(self):
        """Browse for output directory."""
        dir_path = filedialog.askdirectory(title="Select Output Directory")
        if dir_path:
            self.output_dir_var.set(dir_path)
    
    def log_message(self, widget, message):
        """Add message to log widget."""
        widget.config(state='normal')
        widget.insert(tk.END, f"{message}\n")
        widget.see(tk.END)
        widget.config(state='disabled')
        self.root.update()
    
    def split_local_file(self):
        """Split local audio file."""
        if not self.current_file:
            messagebox.showerror("Error", "Please select an audio file first.")
            return
        
        def split_thread():
            try:
                self.file_progress.start()
                self.split_btn.config(state='disabled')
                
                self.log_message(self.file_log, f"Starting split process for: {Path(self.current_file).name}")
                
                vocal_path, instrumental_path = self.audio_splitter.split_audio(
                    self.current_file, 
                    self.output_dir_var.get()
                )
                
                self.log_message(self.file_log, f"✓ Vocal track: {Path(vocal_path).name}")
                self.log_message(self.file_log, f"✓ Instrumental track: {Path(instrumental_path).name}")
                
                # Enable play buttons
                self.play_vocal_btn.config(state='normal')
                self.play_instrumental_btn.config(state='normal')
                
                messagebox.showinfo("Success", "Audio splitting completed successfully!")
                
            except Exception as e:
                self.log_message(self.file_log, f"✗ Error: {str(e)}")
                messagebox.showerror("Error", f"Failed to split audio:\n{str(e)}")
            
            finally:
                self.file_progress.stop()
                self.split_btn.config(state='normal')
        
        threading.Thread(target=split_thread, daemon=True).start()
    
    def get_youtube_info(self):
        """Get YouTube video information."""
        url = self.youtube_url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL.")
            return
        
        if not is_valid_youtube_url(url):
            messagebox.showerror("Error", "Please enter a valid YouTube URL.")
            return
        
        def info_thread():
            try:
                self.yt_info_btn.config(state='disabled')
                self.log_message(self.youtube_log, "Getting video information...")
                
                info = self.youtube_downloader.get_video_info(url)
                if info:
                    self.log_message(self.youtube_log, f"Title: {info['title']}")
                    self.log_message(self.youtube_log, f"Duration: {info['duration']//60}:{info['duration']%60:02d}")
                    self.log_message(self.youtube_log, f"Uploader: {info['uploader']}")
                
            except Exception as e:
                self.log_message(self.youtube_log, f"✗ Error: {str(e)}")
                messagebox.showerror("Error", f"Failed to get video info:\n{str(e)}")
            
            finally:
                self.yt_info_btn.config(state='normal')
        
        threading.Thread(target=info_thread, daemon=True).start()
    
    def download_and_split(self):
        """Download from YouTube and split."""
        url = self.youtube_url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL.")
            return
        
        if not is_valid_youtube_url(url):
            messagebox.showerror("Error", "Please enter a valid YouTube URL.")
            return
        
        def download_thread():
            try:
                self.youtube_progress.start()
                self.yt_download_btn.config(state='disabled')
                
                self.log_message(self.youtube_log, f"Starting download and split process...")
                
                vocal_path, instrumental_path = self.youtube_downloader.download_and_split(
                    url,
                    self.output_dir_var.get(),
                    keep_original=self.keep_original_var.get()
                )
                
                self.log_message(self.youtube_log, f"✓ Process completed successfully!")
                self.log_message(self.youtube_log, f"✓ Vocal track: {Path(vocal_path).name}")
                self.log_message(self.youtube_log, f"✓ Instrumental track: {Path(instrumental_path).name}")
                
                messagebox.showinfo("Success", "Download and split completed successfully!")
                
            except Exception as e:
                self.log_message(self.youtube_log, f"✗ Error: {str(e)}")
                messagebox.showerror("Error", f"Failed to download and split:\n{str(e)}")
            
            finally:
                self.youtube_progress.stop()
                self.yt_download_btn.config(state='normal')
        
        threading.Thread(target=download_thread, daemon=True).start()
    
    def play_vocals(self):
        """Open vocals file with default audio player."""
        # This is a placeholder - you would implement actual audio playback
        messagebox.showinfo("Play Vocals", "This would open the vocal track in your default audio player.")
    
    def play_instrumental(self):
        """Open instrumental file with default audio player."""
        # This is a placeholder - you would implement actual audio playback
        messagebox.showinfo("Play Instrumental", "This would open the instrumental track in your default audio player.")

def main():
    """Main function to run the GUI application."""
    root = tk.Tk()
    app = MusicSplitterGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
