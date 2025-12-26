# 🎵 Music Splitter



































































































































































































































































































































































































































































































































































































































































































































    main()if __name__ == "__main__":    root.mainloop()    app = ModernMusicSplitterGUI(root)    root = tk.Tk()    """Launch the application"""def main():        messagebox.showerror("Error", f"Batch processing failed:\n{error_message}")        self.update_status("Batch processing failed")        """Handle batch error"""    def batch_error(self, error_message):            messagebox.showinfo("Success", f"Successfully processed {total_files} files!")        self.update_status(f"✓ Processed {total_files} files successfully")        """Handle batch completion"""    def batch_complete(self, total_files):                self.root.after(0, self.batch_error, str(e))        except Exception as e:                        self.root.after(0, self.batch_complete, total_files)                                self.audio_splitter.split_audio_simple(file_path)                else:                    self.audio_splitter.split_audio_enhanced(file_path)                if hasattr(self.audio_splitter, 'split_audio_enhanced'):                                              f"Processing {i+1}/{total_files}: {Path(file_path).name}")                self.root.after(0, self.update_status,             for i, file_path in enumerate(self.batch_files):            total_files = len(self.batch_files)        try:        """Batch processing task"""    def process_batch_task(self):            thread.start()        thread.daemon = True        thread = threading.Thread(target=self.process_batch_task)                self.update_status(f"Processing {len(self.batch_files)} files...")                    return            messagebox.showerror("Error", "No files selected!")        if not self.batch_files:        """Process batch files"""    def process_batch_thread(self):            messagebox.showerror("Error", f"Operation failed:\n{error_message}")        self.update_status("Operation failed")        self.yt_progress_label.config(text="✗ Failed", fg=self.ERROR_RED)        """Handle download and split error"""    def download_split_error(self, error_message):            messagebox.showinfo("Success", "Download and split completed successfully!")        self.update_status("YouTube download and split completed")        self.yt_progress_label.config(text="✓ Completed!", fg=self.SUCCESS_GREEN)        """Handle download and split completion"""    def download_split_complete(self, vocal_path, instrumental_path):                self.root.after(0, self.download_split_error, str(e))        except Exception as e:                        self.root.after(0, self.download_split_complete, vocal_path, instrumental_path)                            vocal_path, instrumental_path = self.audio_splitter.split_audio_simple(downloaded_file)            else:                vocal_path, instrumental_path = self.audio_splitter.split_audio_enhanced(downloaded_file)            if hasattr(self.audio_splitter, 'split_audio_enhanced'):            # Split                        downloaded_file = self.youtube_downloader.download(url, str(output_dir))            output_dir.mkdir(exist_ok=True)            output_dir = Path("downloads")            # Download        try:        """Download and split task"""    def download_and_split_task(self, url):            thread.start()        thread.daemon = True        thread = threading.Thread(target=self.download_and_split_task, args=(url,))                self.update_status("Downloading and splitting...")        self.yt_progress_label.config(text="Downloading and splitting...", fg=self.WARNING_ORANGE)                    return            messagebox.showerror("Error", "Please enter a YouTube URL!")        if not url:        url = self.youtube_url_var.get()        """Download and split in one operation"""    def download_and_split_thread(self):            messagebox.showerror("Error", f"Download failed:\n{error_message}")        self.update_status("Download failed")        self.yt_progress_label.config(text="✗ Download failed", fg=self.ERROR_RED)        """Handle download error"""    def download_error(self, error_message):            messagebox.showinfo("Success", f"Downloaded: {Path(file_path).name}")        self.update_status(f"Downloaded: {Path(file_path).name}")        self.yt_progress_label.config(text="✓ Download completed!", fg=self.SUCCESS_GREEN)        """Handle download completion"""    def download_complete(self, file_path):                self.root.after(0, self.download_error, str(e))        except Exception as e:                        self.root.after(0, self.download_complete, downloaded_file)            downloaded_file = self.youtube_downloader.download(url, str(output_dir))                        output_dir.mkdir(exist_ok=True)            output_dir = Path("downloads")        try:        """YouTube download task"""    def download_youtube_task(self, url):            thread.start()        thread.daemon = True        thread = threading.Thread(target=self.download_youtube_task, args=(url,))                self.update_status("Downloading from YouTube...")        self.yt_progress_label.config(text="Downloading...", fg=self.WARNING_ORANGE)                    return            messagebox.showerror("Error", "Please enter a YouTube URL!")        if not url:        url = self.youtube_url_var.get()        """Download from YouTube"""    def download_youtube_thread(self):            messagebox.showerror("Error", f"Failed to split audio:\n{error_message}")                self.update_status("Error")        self.progress_label.config(text="✗ Split failed", fg=self.ERROR_RED)        self.animate_progress(False)        self._animating = False        """Handle split error"""    def split_error(self, error_message):                              f"Instrumental: {Path(instrumental_path).name}")                          f"Vocals: {Path(vocal_path).name}\n"                          f"Audio split successfully!\n\n"        messagebox.showinfo("Success",                 self.update_status("Split complete")        self.progress_label.config(text="✓ Split completed successfully!", fg=self.SUCCESS_GREEN)        self.animate_progress(False)        self._animating = False        """Handle split completion"""    def split_complete(self, vocal_path, instrumental_path):                self.root.after(0, self.split_error, str(e))        except Exception as e:                        self.root.after(0, self.split_complete, vocal_path, instrumental_path)                            )                    file_path, output_dir                vocal_path, instrumental_path = self.audio_splitter.split_audio_simple(            else:                )                    file_path, output_dir                vocal_path, instrumental_path = self.audio_splitter.split_audio_enhanced(            if hasattr(self.audio_splitter, 'split_audio_enhanced'):                        output_dir = self.output_path_var.get() or None        try:        """Audio splitting task"""    def split_audio_task(self, file_path):            thread.start()        thread.daemon = True        thread = threading.Thread(target=self.split_audio_task, args=(file_path,))                self.progress_label.config(text="Splitting audio...", fg=self.WARNING_ORANGE)        self.animate_progress(True)        self._animating = True                    return            messagebox.showerror("Error", "File does not exist!")        if not os.path.exists(file_path):                    return            messagebox.showerror("Error", "Please select an audio file!")        if not file_path:        file_path = self.file_path_var.get()        """Start audio splitting in thread"""    def split_audio_thread(self):    # Processing operations            self.update_status("Batch list cleared")        self.batch_listbox.delete(0, tk.END)        self.batch_files.clear()        """Clear batch file list"""    def clear_batch_files(self):            self.update_status(f"Added {len(filenames)} files • Total: {len(self.batch_files)}")                        self.batch_listbox.insert(tk.END, Path(filename).name)                self.batch_files.append(filename)            if filename not in self.batch_files:        for filename in filenames:        )            ]                ("All Files", "*.*")                ("Audio Files", "*.mp3 *.wav *.flac *.m4a *.ogg"),            filetypes=[            title="Select Audio Files",        filenames = filedialog.askopenfilenames(        """Add files to batch list"""    def add_batch_files(self):                self.update_status(f"Output: {directory}")            self.output_path_var.set(directory)        if directory:        directory = filedialog.askdirectory(title="Select Output Directory")        """Browse for output directory"""    def browse_output_dir(self):                self.update_status(f"Selected: {Path(filename).name}")            self.file_path_var.set(filename)        if filename:        )            ]                ("All Files", "*.*")                ("Audio Files", "*.mp3 *.wav *.flac *.m4a *.ogg"),            filetypes=[            title="Select Audio File",        filename = filedialog.askopenfilename(        """Browse for audio file"""    def browse_file(self):    # File operations            self.root.after(10, lambda: self._animate_progress_step(step + 1))        self.progress_bar.coords(self.progress_rect, x, 0, x + width/4, 4)        x = (width * position) / 100                    position = 200 - position        if position > 100:        position = (step % 200)        width = self.progress_bar.winfo_width()                    return        if not hasattr(self, '_animating') or not self._animating:        """Progress animation step"""    def _animate_progress_step(self, step):                self.progress_bar.coords(self.progress_rect, 0, 0, 0, 4)        else:            self._animate_progress_step(0)            self.progress_bar.coords(self.progress_rect, 0, 0, 100, 4)        if start:        """Animate progress bar"""    def animate_progress(self, start=True):            self.status_label.config(text=message)        """Update status bar"""    def update_status(self, message):            return btn        btn.bind('<Leave>', lambda e: btn.config(bg=self.ACCENT_BLUE))        btn.bind('<Enter>', lambda e: btn.config(bg=self.ACCENT_HOVER))        btn.bind('<Button-1>', lambda e: command())                      pady=10)                      padx=30,                      cursor="hand2",                      fg=self.TEXT_PRIMARY,                      bg=self.ACCENT_BLUE,                      font=('Segoe UI', 11, 'bold'),                      text=text,        btn = tk.Label(parent,        """Create an accent (primary) button"""    def create_accent_button(self, parent, text, command):            return btn        btn.bind('<Leave>', lambda e: btn.config(bg=self.BG_LIGHT))        btn.bind('<Enter>', lambda e: btn.config(bg=self.BG_MEDIUM))        btn.bind('<Button-1>', lambda e: command())                      pady=8)                      padx=20,                      cursor="hand2",                      fg=self.TEXT_PRIMARY,                      bg=self.BG_LIGHT,                      font=('Segoe UI', 10),                      text=text,        btn = tk.Label(parent,        """Create a standard button"""    def create_button(self, parent, text, command):            return inner        inner.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)        inner = tk.Frame(card, bg=self.BG_MEDIUM)        card = tk.Frame(parent, bg=self.BG_MEDIUM)        """Create a card container"""    def create_card(self, parent):            self.status_label.pack(side=tk.LEFT, padx=20)                                     anchor=tk.W)                                     fg=self.TEXT_SECONDARY,                                     bg=self.BG_MEDIUM,                                     font=('Segoe UI', 9),                                     text="Ready",        self.status_label = tk.Label(status_frame,                status_frame.pack_propagate(False)        status_frame.pack(fill=tk.X, side=tk.BOTTOM)        status_frame = tk.Frame(self.root, bg=self.BG_MEDIUM, height=30)        """Create status bar"""    def create_status_bar(self):            self.create_accent_button(btn_frame, "⚡ Process All", self.process_batch_thread).pack(side=tk.LEFT, padx=5)        self.create_button(btn_frame, "🗑️ Clear", self.clear_batch_files).pack(side=tk.LEFT, padx=5)        self.create_button(btn_frame, "➕ Add Files", self.add_batch_files).pack(side=tk.LEFT, padx=5)                btn_frame.pack(pady=10)        btn_frame = tk.Frame(container, bg=self.BG_DARK)        # Buttons                self.batch_files = []                self.batch_listbox.pack(fill=tk.BOTH, expand=True)                                        font=('Segoe UI', 9))                                        highlightbackground=self.BORDER_COLOR,                                        highlightthickness=1,                                        bd=0,                                        relief='flat',                                        selectforeground=self.TEXT_PRIMARY,                                        selectbackground=self.ACCENT_BLUE,                                        fg=self.TEXT_PRIMARY,                                        bg=self.BG_DARK,        self.batch_listbox = tk.Listbox(list_card,                        fg=self.TEXT_PRIMARY).pack(anchor=tk.W, pady=(0, 10))                bg=self.BG_MEDIUM,                font=('Segoe UI', 11, 'bold'),                text="Selected Files",        tk.Label(list_card,                list_card.pack(fill=tk.BOTH, expand=True, pady=(0, 20))        list_card = self.create_card(container)        # Files list card                        fg=self.TEXT_SECONDARY).pack(anchor=tk.W, pady=(0, 20))                bg=self.BG_DARK,                font=('Segoe UI', 10),                text="Select multiple audio files to process them all at once",        tk.Label(container,        # Info                        fg=self.TEXT_PRIMARY).pack(anchor=tk.W, pady=(0, 20))                bg=self.BG_DARK,                font=('Segoe UI', 18, 'bold'),                text="Batch Audio Processing",        tk.Label(container,        # Title                container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)        container = tk.Frame(frame, bg=self.BG_DARK)                self.notebook.add(frame, text="📦 Batch Process")        frame = tk.Frame(self.notebook, bg=self.BG_DARK)        """Create batch processing tab"""    def create_batch_tab(self):                self.yt_progress_label.pack(pady=10)                                         fg=self.TEXT_SECONDARY)                                         bg=self.BG_DARK,                                         font=('Segoe UI', 10),                                         text="Enter YouTube URL to start",        self.yt_progress_label = tk.Label(container,        # Progress                self.create_accent_button(btn_frame, "📥 Download & Split", self.download_and_split_thread).pack(side=tk.LEFT, padx=5)        self.create_button(btn_frame, "📥 Download Only", self.download_youtube_thread).pack(side=tk.LEFT, padx=5)                btn_frame.pack(pady=20)        btn_frame = tk.Frame(container, bg=self.BG_DARK)        # Buttons                url_entry.pack(fill=tk.X, ipady=8)                            highlightcolor=self.ACCENT_BLUE)                            highlightbackground=self.BORDER_COLOR,                            highlightthickness=1,                            bd=0,                            relief='flat',                            insertbackground=self.TEXT_PRIMARY,                            fg=self.TEXT_PRIMARY,                            bg=self.BG_DARK,                            font=('Segoe UI', 10),                            textvariable=self.youtube_url_var,        url_entry = tk.Entry(url_card,        self.youtube_url_var = tk.StringVar()                        fg=self.TEXT_PRIMARY).pack(anchor=tk.W, pady=(0, 10))                bg=self.BG_MEDIUM,                font=('Segoe UI', 11, 'bold'),                text="YouTube URL",        tk.Label(url_card,                url_card.pack(fill=tk.X, pady=(0, 20))        url_card = self.create_card(container)        # URL card                        fg=self.TEXT_PRIMARY).pack(anchor=tk.W, pady=(0, 30))                bg=self.BG_DARK,                font=('Segoe UI', 18, 'bold'),                text="YouTube Music Downloader & Splitter",        tk.Label(container,        # Title                container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)        container = tk.Frame(frame, bg=self.BG_DARK)                self.notebook.add(frame, text="📺 YouTube")        frame = tk.Frame(self.notebook, bg=self.BG_DARK)        """Create YouTube download tab"""    def create_youtube_tab(self):                split_btn.pack(pady=10)        split_btn = self.create_accent_button(container, "🎵 SPLIT AUDIO", self.split_audio_thread)        # Split button                                                                        width=0)                                                                fill=self.ACCENT_BLUE,         self.progress_rect = self.progress_bar.create_rectangle(0, 0, 0, 4,         self.progress_bar.pack(fill=tk.X, pady=(0, 20))                                     highlightthickness=0)                                     bg=self.BG_MEDIUM,                                      height=4,         self.progress_bar = tk.Canvas(container,         # Progress bar                self.progress_label.pack(pady=(20, 10))                                      fg=self.TEXT_SECONDARY)                                      bg=self.BG_DARK,                                      font=('Segoe UI', 10),                                      text="Ready to split audio",        self.progress_label = tk.Label(container,        # Progress section                self.create_button(output_input_frame, "📁 Browse", self.browse_output_dir).pack(side=tk.RIGHT)                output_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, ipady=8, padx=(0, 10))                               highlightcolor=self.ACCENT_BLUE)                               highlightbackground=self.BORDER_COLOR,                               highlightthickness=1,                               bd=0,                               relief='flat',                               insertbackground=self.TEXT_PRIMARY,                               fg=self.TEXT_PRIMARY,                               bg=self.BG_DARK,                               font=('Segoe UI', 10),                               textvariable=self.output_path_var,        output_entry = tk.Entry(output_input_frame,        self.output_path_var = tk.StringVar()                output_input_frame.pack(fill=tk.X)        output_input_frame = tk.Frame(output_card, bg=self.BG_MEDIUM)                        fg=self.TEXT_PRIMARY).pack(anchor=tk.W, pady=(0, 10))                bg=self.BG_MEDIUM,                font=('Segoe UI', 11, 'bold'),                text="Output Directory (Optional)",        tk.Label(output_card,                output_card.pack(fill=tk.X, pady=(0, 20))        output_card = self.create_card(container)        # Output directory card                self.create_button(file_input_frame, "📁 Browse", self.browse_file).pack(side=tk.RIGHT)                file_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, ipady=8, padx=(0, 10))                             highlightcolor=self.ACCENT_BLUE)                             highlightbackground=self.BORDER_COLOR,                             highlightthickness=1,                             bd=0,                             relief='flat',                             insertbackground=self.TEXT_PRIMARY,                             fg=self.TEXT_PRIMARY,                             bg=self.BG_DARK,                             font=('Segoe UI', 10),                             textvariable=self.file_path_var,        file_entry = tk.Entry(file_input_frame,        self.file_path_var = tk.StringVar()                file_input_frame.pack(fill=tk.X, pady=(0, 10))        file_input_frame = tk.Frame(file_card, bg=self.BG_MEDIUM)                        fg=self.TEXT_PRIMARY).pack(anchor=tk.W, pady=(0, 10))                bg=self.BG_MEDIUM,                font=('Segoe UI', 11, 'bold'),                text="Select Audio File",        tk.Label(file_card,                file_card.pack(fill=tk.X, pady=(0, 20))        file_card = self.create_card(container)        # File selection card                        fg=self.TEXT_PRIMARY).pack(anchor=tk.W, pady=(0, 30))                bg=self.BG_DARK,                font=('Segoe UI', 18, 'bold'),                text="Audio Vocal/Instrumental Splitter",        tk.Label(container,        # Title                container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)        container = tk.Frame(frame, bg=self.BG_DARK)        # Content container                self.notebook.add(frame, text="🎤 Split Audio")        frame = tk.Frame(self.notebook, bg=self.BG_DARK)        """Create audio splitting tab"""    def create_split_tab(self):                           background=self.BG_DARK)        style.configure('TFrame',                         foreground=[('selected', self.TEXT_PRIMARY)])                 background=[('selected', self.BG_DARK)],        style.map('TNotebook.Tab',                               focuscolor='')                       borderwidth=0,                       padding=[20, 12],                       foreground=self.TEXT_SECONDARY,                       background=self.BG_MEDIUM,        style.configure('TNotebook.Tab',                               tabmargins=[0, 0, 0, 0])                       borderwidth=0,                       background=self.BG_DARK,        style.configure('TNotebook',                style.theme_use('default')        style = ttk.Style()        """Apply custom style to notebook"""    def apply_notebook_style(self):            self.create_batch_tab()        self.create_youtube_tab()        self.create_split_tab()        # Tab pages                self.notebook.pack(fill=tk.BOTH, expand=True)        self.apply_notebook_style()        self.notebook = ttk.Notebook(main_frame)        # Create tabs                main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)        main_frame = tk.Frame(self.root, bg=self.BG_DARK)        """Create main content area"""    def create_main_content(self):            close_btn.bind('<Leave>', lambda e: close_btn.config(bg=self.BG_DARK))        close_btn.bind('<Enter>', lambda e: close_btn.config(bg=self.ERROR_RED))        close_btn.bind('<Button-1>', lambda e: self.root.quit())        close_btn.pack(side=tk.LEFT)                            pady=0)                            padx=15,                            cursor="hand2",                            fg=self.TEXT_SECONDARY,                            bg=self.BG_DARK,                            font=('Segoe UI', 14),                            text="✕",        close_btn = tk.Label(controls,        # Close button                minimize_btn.bind('<Leave>', lambda e: minimize_btn.config(bg=self.BG_DARK))        minimize_btn.bind('<Enter>', lambda e: minimize_btn.config(bg=self.BG_LIGHT))        minimize_btn.bind('<Button-1>', lambda e: self.root.iconify())        minimize_btn.pack(side=tk.LEFT)                               pady=0)                               padx=15,                               cursor="hand2",                               fg=self.TEXT_SECONDARY,                               bg=self.BG_DARK,                               font=('Segoe UI', 16),                               text="−",        minimize_btn = tk.Label(controls,        # Minimize button                controls.pack(side=tk.RIGHT, padx=10)        controls = tk.Frame(titlebar, bg=self.BG_DARK)        # Window controls                        fg=self.TEXT_PRIMARY).pack(side=tk.LEFT)                bg=self.BG_DARK,                font=('Segoe UI', 12, 'bold'),                text="Music Splitter Pro",        tk.Label(title_left,                        fg=self.TEXT_PRIMARY).pack(side=tk.LEFT, padx=(0, 10))                bg=self.BG_DARK,                font=('Segoe UI', 18),                text="🎵",         tk.Label(title_left,                 title_left.pack(side=tk.LEFT, padx=20)        title_left = tk.Frame(titlebar, bg=self.BG_DARK)        # App title and icon                titlebar.pack_propagate(False)        titlebar.pack(fill=tk.X, side=tk.TOP)        titlebar = tk.Frame(self.root, bg=self.BG_DARK, height=50)        """Create custom title bar with window controls"""    def create_title_bar(self):            self.create_status_bar()        # Status bar                self.create_main_content()        # Main content                self.create_title_bar()        # Custom title bar        """Create modern interface"""    def create_widgets(self):                self.root.geometry(f"+{x}+{y}")            y = self.root.winfo_y() + event.y - self._drag_data["y"]            x = self.root.winfo_x() + event.x - self._drag_data["x"]        if hasattr(self, '_drag_data'):        """Handle window drag"""    def on_drag(self, event):                self._drag_data = {"x": event.x, "y": event.y}        """Start window drag"""    def start_drag(self, event):                self.root.bind('<B1-Motion>', self.on_drag)        self.root.bind('<Button-1>', self.start_drag)        # Make window draggable                self.root.configure(bg=self.BG_DARK)        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")                y = (screen_height - window_height) // 2        x = (screen_width - window_width) // 2        screen_height = self.root.winfo_screenheight()        screen_width = self.root.winfo_screenwidth()        # Center on screen                window_height = 650        window_width = 900        # Window properties                self.root.overrideredirect(True)        # Remove default window decorations        """Setup borderless window with custom controls"""    def setup_custom_window(self):                self.youtube_downloader = YouTubeDownloader()        self.audio_splitter = EnhancedAudioSplitter()        self.create_widgets()        self.setup_custom_window()        self.root = root    def __init__(self, root):        BORDER_COLOR = "#3a3a3a"     # Subtle borders        WARNING_ORANGE = "#ff9500"   # Warnings    ERROR_RED = "#ff3b30"        # Error messages    SUCCESS_GREEN = "#20c933"    # Success messages        ACCENT_PRESSED = "#1557b0"   # Pressed state    ACCENT_HOVER = "#1e6edb"     # Hover state    ACCENT_BLUE = "#2d7ff9"      # Primary accent        TEXT_DISABLED = "#666666"    # Disabled text    TEXT_SECONDARY = "#b0b0b0"   # Secondary text (light gray)    TEXT_PRIMARY = "#ffffff"     # Main text (white for visibility)        BG_LIGHT = "#2d2d2d"         # Hover states    BG_MEDIUM = "#252525"        # Cards/panels    BG_DARK = "#1a1a1a"          # Main background    # Beautiful color scheme with high contrast        """Modern dark theme music splitter with beautiful UI"""class ModernMusicSplitterGUI:            raise Exception("YouTube downloader not available")        def download(self, url, output_dir):    class YouTubeDownloader:except ImportError:    from youtube_downloader import YouTubeDownloadertry:    from simple_audio_splitter import SimpleAudioSplitter as EnhancedAudioSplitterexcept ImportError:    from enhanced_audio_splitter import EnhancedAudioSplittertry:from pathlib import Pathimport osimport threadingfrom tkinter import ttk, filedialog, messageboximport tkinter as tk"""Fixed text visibility, no borders, embedded window controls**AI-powered vocal and instrumental separation tool with YouTube integration**

Extract vocals and instrumentals from any audio file using advanced audio processing algorithms. Download music directly from YouTube and split it automatically.

## ✨ Features

- 🎤 **Vocal/Instrumental Separation** - Advanced audio processing for clean splits
- 📺 **YouTube Integration** - Download and split music from YouTube URLs
- 🎵 **Multiple Formats** - MP3, WAV, FLAC, and more
- 🎨 **Modern Dark UI** - Beautiful, intuitive interface
- ⚡ **Batch Processing** - Split multiple files at once
- 🖥️ **Cross-Platform** - Windows, macOS, Linux

## Installation

### Prerequisites

1. **Python 3.8 or higher** - Download from [python.org](https://python.org)
2. **FFmpeg** (recommended for YouTube downloads):
   - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html) or use `winget install FFmpeg`
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt install ffmpeg` (Ubuntu/Debian) or equivalent

### Setup

1. **Clone/Download this repository**
2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the test script** to verify installation:
   ```bash
   python test_installation.py
   ```

### Quick Start (Windows)

- Double-click `run_app.bat` or `run_app.ps1` to launch the GUI
- Or use VS Code tasks: `Ctrl+Shift+P` → "Tasks: Run Task" → "Launch Music Splitter GUI"

## Usage

### GUI Mode (Recommended)

Launch the graphical interface:
```bash
python main.py
```

**Features:**
- **Local Files Tab**: Browse and split audio files from your computer
- **YouTube Tab**: Enter a YouTube URL to download and split automatically
- **Settings Tab**: Configure output format and quality

### Command Line Mode

#### Split a local audio file:
```bash
python main.py --split "path/to/audio.mp3" --output "output_folder"
```

#### Download and split from YouTube:
```bash
python main.py --youtube "https://youtube.com/watch?v=..." --output "output_folder"
```

#### Interactive CLI mode:
```bash
python main.py --cli
```

#### Get audio file information:
```bash
python audio_splitter.py --input "audio.mp3" --info
```

### Advanced Usage

#### Direct module usage:
```bash
# Audio splitting only
python audio_splitter.py --input "song.mp3" --output "results"

# YouTube download only  
python youtube_downloader.py --url "https://youtube.com/watch?v=..." --info
```

## How It Works

This application uses **librosa**, a powerful audio analysis library, to perform source separation:

1. **Stereo Separation**: For stereo files, it uses center/side extraction where vocals (typically centered) are isolated from the instrumental parts
2. **Harmonic-Percussive Separation**: Separates tonal (harmonic) components from rhythmic (percussive) elements
3. **Spectral Processing**: Applies frequency-domain filtering to enhance separation quality

### Output Quality Notes

- **Best results**: Stereo recordings with centered vocals and wide instrumental mix
- **Good for**: Pop, rock, and most commercial music
- **Limitations**: May not work well with mono recordings or heavily processed audio

For professional-grade separation, consider:
- **Spleeter** (AI-based, requires TensorFlow)
- **LALAL.AI** (online service)
- **Ultimate Vocal Remover** (desktop app)

## Output Files

The app creates two files for each input:
- `{filename}_vocals.wav` - Isolated vocal track
- `{filename}_instrumental.wav` - Isolated instrumental track

## Troubleshooting

### Common Issues

1. **"FFmpeg not found"**: Install FFmpeg for YouTube download support
2. **"Python not found"**: Ensure Python is installed and in your system PATH
3. **Poor separation quality**: Try different source material; stereo files work best
4. **Memory errors**: Use shorter audio files or reduce quality settings

### Getting Help

1. Run `python test_installation.py` to check your setup
2. Check the console output for detailed error messages
3. Ensure all dependencies are installed correctly

## Development

### Project Structure
```
music_spliter/
├── main.py                 # Main application entry point
├── audio_splitter.py       # Core audio processing
├── youtube_downloader.py   # YouTube integration
├── gui.py                  # Tkinter GUI interface
├── requirements.txt        # Python dependencies
├── test_installation.py    # Installation verification
└── README.md              # This file
```

### Adding Features

- Audio processing: Modify `audio_splitter.py`
- GUI improvements: Update `gui.py`
- YouTube features: Enhance `youtube_downloader.py`

## License

MIT License - see LICENSE file for details.

## Acknowledgments

- **librosa** - Audio analysis library
- **yt-dlp** - YouTube downloading
- **tkinter** - GUI framework
- **FFmpeg** - Audio processing backend
