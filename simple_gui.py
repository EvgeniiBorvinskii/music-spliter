import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from pathlib import Path
from simple_audio_splitter import SimpleAudioSplitter

class SimpleMusicSplitterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Splitter - Simple Version")
        self.root.geometry("600x400")
        self.root.resizable(True, True)
        
        self.splitter = SimpleAudioSplitter()
        self.current_file = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Create the user interface."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="🎵 Music Splitter", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # File selection
        file_frame = ttk.LabelFrame(main_frame, text="Select WAV Audio File", padding=10)
        file_frame.pack(fill='x', pady=(0, 10))
        
        self.file_path_var = tk.StringVar()
        file_entry = ttk.Entry(file_frame, textvariable=self.file_path_var, state='readonly')
        file_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        browse_btn = ttk.Button(file_frame, text="Browse", command=self.browse_file)
        browse_btn.pack(side='right')
        
        # Output directory
        output_frame = ttk.LabelFrame(main_frame, text="Output Directory", padding=10)
        output_frame.pack(fill='x', pady=(0, 10))
        
        self.output_dir_var = tk.StringVar()
        self.output_dir_var.set(str(Path.cwd() / "split_output"))
        
        output_entry = ttk.Entry(output_frame, textvariable=self.output_dir_var)
        output_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        output_browse_btn = ttk.Button(output_frame, text="Browse", command=self.browse_output)
        output_browse_btn.pack(side='right')
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='x', pady=10)
        
        self.split_btn = ttk.Button(button_frame, text="Split Audio", 
                                   command=self.split_audio)
        self.split_btn.pack(side='left', padx=(0, 10))
        
        info_btn = ttk.Button(button_frame, text="Show Info", 
                             command=self.show_info)
        info_btn.pack(side='left')
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.pack(fill='x', pady=10)
        
        # Status
        self.status_var = tk.StringVar()
        self.status_var.set("Ready - Select a WAV file to split")
        status_label = ttk.Label(main_frame, textvariable=self.status_var)
        status_label.pack(pady=5)
        
        # Info text
        info_text = """
This simplified version works with WAV files only.
Best results with stereo recordings where vocals are centered.

How it works:
• Uses center/side technique to separate vocals from instruments
• Creates two files: vocals and instrumental tracks
        """
        info_label = ttk.Label(main_frame, text=info_text, 
                             justify='left', foreground='gray')
        info_label.pack(pady=10)
    
    def browse_file(self):
        """Browse for WAV file."""
        file_path = filedialog.askopenfilename(
            title="Select WAV Audio File",
            filetypes=[
                ("WAV Files", "*.wav"),
                ("All Files", "*.*")
            ]
        )
        if file_path:
            self.file_path_var.set(file_path)
            self.current_file = file_path
            self.status_var.set(f"Selected: {Path(file_path).name}")
    
    def browse_output(self):
        """Browse for output directory."""
        dir_path = filedialog.askdirectory(title="Select Output Directory")
        if dir_path:
            self.output_dir_var.set(dir_path)
    
    def show_info(self):
        """Show file information."""
        if not self.current_file:
            messagebox.showerror("Error", "Please select a WAV file first.")
            return
        
        try:
            info = self.splitter.get_audio_info(self.current_file)
            if info:
                info_text = f"""Audio File Information:

File: {Path(self.current_file).name}
Duration: {info['duration']:.2f} seconds
Sample Rate: {info['sample_rate']} Hz
Channels: {info['channels']}
Total Frames: {info['frames']}"""
                
                messagebox.showinfo("Audio Information", info_text)
            else:
                messagebox.showerror("Error", "Could not read audio file information.")
        except Exception as e:
            messagebox.showerror("Error", f"Error reading file: {str(e)}")
    
    def split_audio(self):
        """Split the audio file."""
        if not self.current_file:
            messagebox.showerror("Error", "Please select a WAV file first.")
            return
        
        def split_thread():
            try:
                self.progress.start()
                self.split_btn.config(state='disabled')
                self.status_var.set("Splitting audio...")
                
                vocal_path, instrumental_path = self.splitter.split_audio_simple(
                    self.current_file,
                    self.output_dir_var.get()
                )
                
                self.status_var.set("Split completed successfully!")
                
                result_text = f"""Audio splitting completed!

Output files created:
🎤 Vocals: {Path(vocal_path).name}
🎸 Instrumental: {Path(instrumental_path).name}

Location: {Path(vocal_path).parent}"""
                
                messagebox.showinfo("Success", result_text)
                
            except Exception as e:
                self.status_var.set("Error occurred during splitting")
                messagebox.showerror("Error", f"Failed to split audio:\n{str(e)}")
            
            finally:
                self.progress.stop()
                self.split_btn.config(state='normal')
        
        threading.Thread(target=split_thread, daemon=True).start()

def main():
    """Main function to run the GUI application."""
    root = tk.Tk()
    app = SimpleMusicSplitterGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
