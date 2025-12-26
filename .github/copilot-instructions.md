# Music Splitter App - Copilot Instructions

This is a Python-based music splitter application that can:
- Split audio files into vocal and instrumental tracks using librosa
- Download music from YouTube links and automatically split them
- Provide both GUI and CLI interfaces

## Technology Stack
- Python 3.8+
- librosa for audio processing
- yt-dlp for YouTube downloading
- tkinter for GUI interface
- numpy and scipy for numerical operations
- soundfile for audio I/O

## Project Structure
- `main.py` - Main application entry point with CLI argument parsing
- `audio_splitter.py` - Core audio splitting functionality using librosa
- `youtube_downloader.py` - YouTube download and integration
- `gui.py` - Tkinter-based GUI interface
- `test_installation.py` - Installation verification script
- `setup.py` - Setup and dependency checking
- `requirements.txt` - Python dependencies
- `run_app.bat/ps1` - Windows launch scripts

## Key Features Implemented
✅ Audio source separation using librosa harmonic-percussive separation
✅ Center/side extraction for stereo files  
✅ YouTube video downloading with yt-dlp
✅ Cross-platform GUI with tkinter
✅ Command-line interface with multiple modes
✅ Error handling and user feedback
✅ VS Code tasks integration
✅ Installation testing and verification

## Development Guidelines
- Use librosa for audio processing (primary approach)
- Handle both mono and stereo audio files
- Provide clear user feedback for long operations
- Follow PEP 8 style guidelines
- Include comprehensive error handling
- Support multiple audio formats (WAV, MP3, FLAC)

## Usage Patterns
1. **GUI Mode**: `python main.py` (default)
2. **CLI Mode**: `python main.py --cli`
3. **Direct Split**: `python main.py --split file.mp3`
4. **YouTube**: `python main.py --youtube "URL"`

## Quality Notes
- Best results with stereo recordings and centered vocals
- Uses spectral processing and harmonic separation
- For advanced AI separation, users can optionally install TensorFlow/Spleeter
