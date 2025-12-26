# 🎵 Music Splitter

<img width="1339" height="973" alt="image" src="https://github.com/user-attachments/assets/2bb69294-af67-492a-bd04-07d183cb34ed" />

Extract vocals and instrumentals from any audio file using advanced audio processing algorithms. Download music directly from YouTube and split it automatically.

## ✨ Features

- 🎤 **Vocal/Instrumental Separation** - Advanced audio processing for clean splits
- 📺 **YouTube Integration** - Download and split music from YouTube URLs
<img width="650" height="400" alt="image" src="https://github.com/user-attachments/assets/c61da2a4-d30e-45e6-9065-f0db74a55363" />

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
