# Music Splitter Pro - Modern GUI
# Beautiful dark theme with custom window controls and high visibility
# All text in English

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
from pathlib import Path

try:
    from enhanced_audio_splitter import EnhancedAudioSplitter
except ImportError:
    from simple_audio_splitter import SimpleAudioSplitter as EnhancedAudioSplitter

try:
    from youtube_downloader import YouTubeDownloader
except ImportError:
    class YouTubeDownloader:
        def download(self, url, output_dir):
            raise Exception('YouTube downloader not available')


class MusicSplitterApp:
    # Beautiful dark theme colors with high contrast for text visibility
    BG_DARK = '#1a1a1a'
    BG_MEDIUM = '#252525'
    BG_LIGHT = '#2d2d2d'
    
    TEXT_WHITE = '#ffffff'
    TEXT_GRAY = '#b0b0b0'
    TEXT_DARK_GRAY = '#666666'
    
    ACCENT_BLUE = '#2d7ff9'
    ACCENT_HOVER = '#1e6edb'
    SUCCESS_GREEN = '#20c933'
    ERROR_RED = '#ff3b30'
    WARNING_ORANGE = '#ff9500'
    
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.create_ui()
        self.audio_splitter = EnhancedAudioSplitter()
        self.youtube_downloader = YouTubeDownloader()
        
    def setup_window(self):
        self.root.overrideredirect(True)
        w, h = 900, 650
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.root.geometry(f'{w}x{h}+{x}+{y}')
        self.root.configure(bg=self.BG_DARK)
        self.root.bind('<Button-1>', self.start_drag)
        self.root.bind('<B1-Motion>', self.on_drag)
        
    def start_drag(self, event):
        self._drag = {'x': event.x, 'y': event.y}
        
    def on_drag(self, event):
        if hasattr(self, '_drag'):
            x = self.root.winfo_x() + event.x - self._drag['x']
            y = self.root.winfo_y() + event.y - self._drag['y']
            self.root.geometry(f'+{x}+{y}')
    
    def create_ui(self):
        # Title bar with controls
        titlebar = tk.Frame(self.root, bg=self.BG_DARK, height=50)
        titlebar.pack(fill=tk.X, side=tk.TOP)
        titlebar.pack_propagate(False)
        
        tk.Label(titlebar, text=' Music Splitter Pro', font=('Segoe UI', 12, 'bold'),
                bg=self.BG_DARK, fg=self.TEXT_WHITE).pack(side=tk.LEFT, padx=20)
        
        controls = tk.Frame(titlebar, bg=self.BG_DARK)
        controls.pack(side=tk.RIGHT, padx=10)
        
        min_btn = tk.Label(controls, text='', font=('Segoe UI', 16),
                          bg=self.BG_DARK, fg=self.TEXT_GRAY,
                          cursor='hand2', padx=15)
        min_btn.pack(side=tk.LEFT)
        min_btn.bind('<Button-1>', lambda e: self.root.iconify())
        min_btn.bind('<Enter>', lambda e: min_btn.config(bg=self.BG_LIGHT))
        min_btn.bind('<Leave>', lambda e: min_btn.config(bg=self.BG_DARK))
        
        close_btn = tk.Label(controls, text='', font=('Segoe UI', 14),
                            bg=self.BG_DARK, fg=self.TEXT_GRAY,
                            cursor='hand2', padx=15)
        close_btn.pack(side=tk.LEFT)
        close_btn.bind('<Button-1>', lambda e: self.root.quit())
        close_btn.bind('<Enter>', lambda e: close_btn.config(bg=self.ERROR_RED))
        close_btn.bind('<Leave>', lambda e: close_btn.config(bg=self.BG_DARK))
        
        # Main content
        main = tk.Frame(self.root, bg=self.BG_DARK)
        main.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.notebook = ttk.Notebook(main)
        self.style_notebook()
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        self.create_split_tab()
        self.create_youtube_tab()
        self.create_batch_tab()
        
        # Status bar
        status = tk.Frame(self.root, bg=self.BG_MEDIUM, height=30)
        status.pack(fill=tk.X, side=tk.BOTTOM)
        status.pack_propagate(False)
        
        self.status_label = tk.Label(status, text='Ready', font=('Segoe UI', 9),
                                     bg=self.BG_MEDIUM, fg=self.TEXT_GRAY, anchor=tk.W)
        self.status_label.pack(side=tk.LEFT, padx=20)
    
    def style_notebook(self):
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TNotebook', background=self.BG_DARK, borderwidth=0)
        style.configure('TNotebook.Tab', background=self.BG_MEDIUM,
                       foreground=self.TEXT_GRAY, padding=[20, 12], borderwidth=0)
        style.map('TNotebook.Tab',
                 background=[('selected', self.BG_DARK)],
                 foreground=[('selected', self.TEXT_WHITE)])
        style.configure('TFrame', background=self.BG_DARK)
    
    def create_split_tab(self):
        frame = tk.Frame(self.notebook, bg=self.BG_DARK)
        self.notebook.add(frame, text=' Split Audio')
        
        cont = tk.Frame(frame, bg=self.BG_DARK)
        cont.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        tk.Label(cont, text='Audio Vocal/Instrumental Splitter',
                font=('Segoe UI', 18, 'bold'),
                bg=self.BG_DARK, fg=self.TEXT_WHITE).pack(anchor=tk.W, pady=(0,30))
        
        # File card
        card1 = self.card(cont)
        card1.pack(fill=tk.X, pady=(0,20))
        
        tk.Label(card1, text='Select Audio File', font=('Segoe UI', 11, 'bold'),
                bg=self.BG_MEDIUM, fg=self.TEXT_WHITE).pack(anchor=tk.W, pady=(0,10))
        
        f = tk.Frame(card1, bg=self.BG_MEDIUM)
        f.pack(fill=tk.X)
        
        self.file_var = tk.StringVar()
        tk.Entry(f, textvariable=self.file_var, font=('Segoe UI', 10),
                bg=self.BG_DARK, fg=self.TEXT_WHITE, insertbackground=self.TEXT_WHITE,
                relief='flat', bd=0).pack(side=tk.LEFT, fill=tk.X, expand=True,
                                         ipady=8, padx=(0,10))
        
        self.btn(f, ' Browse', self.browse_file).pack(side=tk.RIGHT)
        
        # Output card
        card2 = self.card(cont)
        card2.pack(fill=tk.X, pady=(0,20))
        
        tk.Label(card2, text='Output Directory (Optional)',
                font=('Segoe UI', 11, 'bold'),
                bg=self.BG_MEDIUM, fg=self.TEXT_WHITE).pack(anchor=tk.W, pady=(0,10))
        
        f2 = tk.Frame(card2, bg=self.BG_MEDIUM)
        f2.pack(fill=tk.X)
        
        self.output_var = tk.StringVar()
        tk.Entry(f2, textvariable=self.output_var, font=('Segoe UI', 10),
                bg=self.BG_DARK, fg=self.TEXT_WHITE, insertbackground=self.TEXT_WHITE,
                relief='flat', bd=0).pack(side=tk.LEFT, fill=tk.X, expand=True,
                                         ipady=8, padx=(0,10))
        
        self.btn(f2, ' Browse', self.browse_output).pack(side=tk.RIGHT)
        
        # Progress
        self.progress_label = tk.Label(cont, text='Ready to split audio',
                                      font=('Segoe UI', 10),
                                      bg=self.BG_DARK, fg=self.TEXT_GRAY)
        self.progress_label.pack(pady=(20,10))
        
        self.progress_canvas = tk.Canvas(cont, height=4, bg=self.BG_MEDIUM,
                                        highlightthickness=0)
        self.progress_canvas.pack(fill=tk.X, pady=(0,20))
        self.progress_rect = self.progress_canvas.create_rectangle(
            0, 0, 0, 4, fill=self.ACCENT_BLUE, width=0)
        
        self.accent_btn(cont, ' SPLIT AUDIO', self.split_audio).pack(pady=10)
    
    def create_youtube_tab(self):
        frame = tk.Frame(self.notebook, bg=self.BG_DARK)
        self.notebook.add(frame, text=' YouTube')
        
        cont = tk.Frame(frame, bg=self.BG_DARK)
        cont.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        tk.Label(cont, text='YouTube Music Downloader & Splitter',
                font=('Segoe UI', 18, 'bold'),
                bg=self.BG_DARK, fg=self.TEXT_WHITE).pack(anchor=tk.W, pady=(0,30))
        
        card = self.card(cont)
        card.pack(fill=tk.X, pady=(0,20))
        
        tk.Label(card, text='YouTube URL', font=('Segoe UI', 11, 'bold'),
                bg=self.BG_MEDIUM, fg=self.TEXT_WHITE).pack(anchor=tk.W, pady=(0,10))
        
        self.yt_url_var = tk.StringVar()
        tk.Entry(card, textvariable=self.yt_url_var, font=('Segoe UI', 10),
                bg=self.BG_DARK, fg=self.TEXT_WHITE, insertbackground=self.TEXT_WHITE,
                relief='flat', bd=0).pack(fill=tk.X, ipady=8)
        
        btns = tk.Frame(cont, bg=self.BG_DARK)
        btns.pack(pady=20)
        
        self.btn(btns, ' Download Only', self.download_yt).pack(side=tk.LEFT, padx=5)
        self.accent_btn(btns, ' Download & Split', self.download_split).pack(side=tk.LEFT, padx=5)
        
        self.yt_status = tk.Label(cont, text='Enter YouTube URL to start',
                                 font=('Segoe UI', 10),
                                 bg=self.BG_DARK, fg=self.TEXT_GRAY)
        self.yt_status.pack(pady=10)
    
    def create_batch_tab(self):
        frame = tk.Frame(self.notebook, bg=self.BG_DARK)
        self.notebook.add(frame, text=' Batch Process')
        
        cont = tk.Frame(frame, bg=self.BG_DARK)
        cont.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        tk.Label(cont, text='Batch Audio Processing',
                font=('Segoe UI', 18, 'bold'),
                bg=self.BG_DARK, fg=self.TEXT_WHITE).pack(anchor=tk.W, pady=(0,20))
        
        tk.Label(cont, text='Select multiple audio files to process them all at once',
                font=('Segoe UI', 10),
                bg=self.BG_DARK, fg=self.TEXT_GRAY).pack(anchor=tk.W, pady=(0,20))
        
        card = self.card(cont)
        card.pack(fill=tk.BOTH, expand=True, pady=(0,20))
        
        tk.Label(card, text='Selected Files', font=('Segoe UI', 11, 'bold'),
                bg=self.BG_MEDIUM, fg=self.TEXT_WHITE).pack(anchor=tk.W, pady=(0,10))
        
        self.batch_list = tk.Listbox(card, bg=self.BG_DARK, fg=self.TEXT_WHITE,
                                     selectbackground=self.ACCENT_BLUE,
                                     selectforeground=self.TEXT_WHITE,
                                     relief='flat', bd=0, font=('Segoe UI', 9))
        self.batch_list.pack(fill=tk.BOTH, expand=True)
        
        self.batch_files = []
        
        btns = tk.Frame(cont, bg=self.BG_DARK)
        btns.pack(pady=10)
        
        self.btn(btns, ' Add Files', self.add_batch).pack(side=tk.LEFT, padx=5)
        self.btn(btns, ' Clear', self.clear_batch).pack(side=tk.LEFT, padx=5)
        self.accent_btn(btns, ' Process All', self.process_batch).pack(side=tk.LEFT, padx=5)
    
    def card(self, parent):
        c = tk.Frame(parent, bg=self.BG_MEDIUM)
        inner = tk.Frame(c, bg=self.BG_MEDIUM)
        inner.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        return inner
    
    def btn(self, parent, text, cmd):
        b = tk.Label(parent, text=text, font=('Segoe UI', 10),
                    bg=self.BG_LIGHT, fg=self.TEXT_WHITE,
                    cursor='hand2', padx=20, pady=8)
        b.bind('<Button-1>', lambda e: cmd())
        b.bind('<Enter>', lambda e: b.config(bg=self.BG_MEDIUM))
        b.bind('<Leave>', lambda e: b.config(bg=self.BG_LIGHT))
        return b
    
    def accent_btn(self, parent, text, cmd):
        b = tk.Label(parent, text=text, font=('Segoe UI', 11, 'bold'),
                    bg=self.ACCENT_BLUE, fg=self.TEXT_WHITE,
                    cursor='hand2', padx=30, pady=10)
        b.bind('<Button-1>', lambda e: cmd())
        b.bind('<Enter>', lambda e: b.config(bg=self.ACCENT_HOVER))
        b.bind('<Leave>', lambda e: b.config(bg=self.ACCENT_BLUE))
        return b
    
    def status(self, msg):
        self.status_label.config(text=msg)
    
    def browse_file(self):
        f = filedialog.askopenfilename(
            title='Select Audio File',
            filetypes=[('Audio Files', '*.mp3 *.wav *.flac *.m4a *.ogg'),
                      ('All Files', '*.*')])
        if f:
            self.file_var.set(f)
            self.status(f'Selected: {Path(f).name}')
    
    def browse_output(self):
        d = filedialog.askdirectory(title='Select Output Directory')
        if d:
            self.output_var.set(d)
            self.status(f'Output: {d}')
    
    def split_audio(self):
        fp = self.file_var.get()
        if not fp:
            messagebox.showerror('Error', 'Please select an audio file!')
            return
        if not os.path.exists(fp):
            messagebox.showerror('Error', 'File does not exist!')
            return
        
        self.progress_label.config(text='Splitting audio...', fg=self.WARNING_ORANGE)
        self.status('Splitting audio...')
        threading.Thread(target=self._split_task, args=(fp,), daemon=True).start()
    
    def _split_task(self, fp):
        try:
            od = self.output_var.get() or None
            if hasattr(self.audio_splitter, 'split_audio_enhanced'):
                vp, ip = self.audio_splitter.split_audio_enhanced(fp, od)
            else:
                vp, ip = self.audio_splitter.split_audio_simple(fp, od)
            self.root.after(0, self._split_done, vp, ip)
        except Exception as e:
            self.root.after(0, self._split_error, str(e))
    
    def _split_done(self, vp, ip):
        self.progress_label.config(text=' Split completed!', fg=self.SUCCESS_GREEN)
        self.status('Split complete')
        messagebox.showinfo('Success', f'Audio split successfully!\\n\\n' +
                          f'Vocals: {Path(vp).name}\\nInstrumental: {Path(ip).name}')
    
    def _split_error(self, err):
        self.progress_label.config(text=' Split failed', fg=self.ERROR_RED)
        self.status('Error')
        messagebox.showerror('Error', f'Failed to split audio:\\n{err}')
    
    def download_yt(self):
        url = self.yt_url_var.get()
        if not url:
            messagebox.showerror('Error', 'Please enter a YouTube URL!')
            return
        self.yt_status.config(text='Downloading...', fg=self.WARNING_ORANGE)
        self.status('Downloading from YouTube...')
        threading.Thread(target=self._download_task, args=(url,), daemon=True).start()
    
    def _download_task(self, url):
        try:
            od = Path('downloads')
            od.mkdir(exist_ok=True)
            df = self.youtube_downloader.download(url, str(od))
            self.root.after(0, self._download_done, df)
        except Exception as e:
            self.root.after(0, self._download_error, str(e))
    
    def _download_done(self, fp):
        self.yt_status.config(text=' Download completed!', fg=self.SUCCESS_GREEN)
        self.status(f'Downloaded: {Path(fp).name}')
        messagebox.showinfo('Success', f'Downloaded: {Path(fp).name}')
    
    def _download_error(self, err):
        self.yt_status.config(text=' Download failed', fg=self.ERROR_RED)
        self.status('Download failed')
        messagebox.showerror('Error', f'Download failed:\\n{err}')
    
    def download_split(self):
        url = self.yt_url_var.get()
        if not url:
            messagebox.showerror('Error', 'Please enter a YouTube URL!')
            return
        self.yt_status.config(text='Downloading and splitting...', fg=self.WARNING_ORANGE)
        self.status('Downloading and splitting...')
        threading.Thread(target=self._download_split_task, args=(url,), daemon=True).start()
    
    def _download_split_task(self, url):
        try:
            od = Path('downloads')
            od.mkdir(exist_ok=True)
            df = self.youtube_downloader.download(url, str(od))
            
            if hasattr(self.audio_splitter, 'split_audio_enhanced'):
                vp, ip = self.audio_splitter.split_audio_enhanced(df)
            else:
                vp, ip = self.audio_splitter.split_audio_simple(df)
            
            self.root.after(0, self._download_split_done, vp, ip)
        except Exception as e:
            self.root.after(0, self._download_split_error, str(e))
    
    def _download_split_done(self, vp, ip):
        self.yt_status.config(text=' Completed!', fg=self.SUCCESS_GREEN)
        self.status('YouTube download and split completed')
        messagebox.showinfo('Success', 'Download and split completed successfully!')
    
    def _download_split_error(self, err):
        self.yt_status.config(text=' Failed', fg=self.ERROR_RED)
        self.status('Operation failed')
        messagebox.showerror('Error', f'Operation failed:\\n{err}')
    
    def add_batch(self):
        files = filedialog.askopenfilenames(
            title='Select Audio Files',
            filetypes=[('Audio Files', '*.mp3 *.wav *.flac *.m4a *.ogg'),
                      ('All Files', '*.*')])
        for f in files:
            if f not in self.batch_files:
                self.batch_files.append(f)
                self.batch_list.insert(tk.END, Path(f).name)
        self.status(f'Added {len(files)} files  Total: {len(self.batch_files)}')
    
    def clear_batch(self):
        self.batch_files.clear()
        self.batch_list.delete(0, tk.END)
        self.status('Batch list cleared')
    
    def process_batch(self):
        if not self.batch_files:
            messagebox.showerror('Error', 'No files selected!')
            return
        self.status(f'Processing {len(self.batch_files)} files...')
        threading.Thread(target=self._batch_task, daemon=True).start()
    
    def _batch_task(self):
        try:
            total = len(self.batch_files)
            for i, fp in enumerate(self.batch_files):
                self.root.after(0, self.status,
                              f'Processing {i+1}/{total}: {Path(fp).name}')
                
                if hasattr(self.audio_splitter, 'split_audio_enhanced'):
                    self.audio_splitter.split_audio_enhanced(fp)
                else:
                    self.audio_splitter.split_audio_simple(fp)
            
            self.root.after(0, self._batch_done, total)
        except Exception as e:
            self.root.after(0, self._batch_error, str(e))
    
    def _batch_done(self, total):
        self.status(f' Processed {total} files successfully')
        messagebox.showinfo('Success', f'Successfully processed {total} files!')
    
    def _batch_error(self, err):
        self.status('Batch processing failed')
        messagebox.showerror('Error', f'Batch processing failed:\\n{err}')


if __name__ == '__main__':
    root = tk.Tk()
    app = MusicSplitterApp(root)
    root.mainloop()
