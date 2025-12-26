# Setup script for Music Splitter App
import subprocess
import sys
from pathlib import Path

def install_ffmpeg():
    """Instructions for installing FFmpeg."""
    print("🔧 FFmpeg Installation Required")
    print("=" * 40)
    print("FFmpeg is required for audio processing. Please install it:")
    print("\nWindows:")
    print("1. Download from: https://ffmpeg.org/download.html")
    print("2. Extract to C:\\ffmpeg")
    print("3. Add C:\\ffmpeg\\bin to your system PATH")
    print("\nAlternatively, use chocolatey:")
    print("choco install ffmpeg")
    print("\nOr use winget:")
    print("winget install FFmpeg")

def check_dependencies():
    """Check if required dependencies are available."""
    print("🔍 Checking dependencies...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    else:
        print("✓ Python version OK")
    
    # Check if FFmpeg is available
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, check=False)
        if result.returncode == 0:
            print("✓ FFmpeg is available")
        else:
            print("⚠️  FFmpeg not found in PATH")
            install_ffmpeg()
    except FileNotFoundError:
        print("⚠️  FFmpeg not found")
        install_ffmpeg()
    
    return True

def create_directories():
    """Create necessary directories."""
    dirs = ['downloads', 'output', 'split_output']
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"✓ Created directory: {dir_name}")

def main():
    print("🎵 Music Splitter Setup")
    print("=" * 30)
    
    if check_dependencies():
        create_directories()
        print("\n✅ Setup completed!")
        print("\nYou can now run the application:")
        print("python main.py          # Launch GUI")
        print("python main.py --cli    # Use CLI mode")
    else:
        print("\n❌ Setup failed. Please install missing dependencies.")

if __name__ == "__main__":
    main()
