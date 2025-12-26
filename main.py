#!/usr/bin/env python3
"""
Music Splitter App - Main Entry Point

A Python application that separates vocals and instrumentals from audio files,
with support for YouTube downloads.

Usage:
    python main.py                    # Launch GUI
    python main.py --cli              # Use command line interface
    python main.py --help             # Show help
"""

import sys
import argparse
from pathlib import Path

def main():
    """Main entry point for the Music Splitter application."""
    parser = argparse.ArgumentParser(
        description="Music Splitter - Separate vocals and instrumentals from audio",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python main.py                                    # Launch GUI
    python main.py --cli                              # Command line mode
    python main.py --split audio.mp3                  # Split local file
    python main.py --youtube "https://youtube.com/..." # Download and split from YouTube
        """
    )
    
    parser.add_argument('--cli', action='store_true', 
                       help='Use command line interface instead of GUI')
    parser.add_argument('--split', metavar='FILE', 
                       help='Split audio file (CLI mode)')
    parser.add_argument('--youtube', metavar='URL', 
                       help='Download and split from YouTube URL (CLI mode)')
    parser.add_argument('--output', '-o', metavar='DIR',
                       help='Output directory for processed files')
    parser.add_argument('--keep-original', action='store_true',
                       help='Keep original downloaded file (YouTube mode)')
    parser.add_argument('--info', action='store_true',
                       help='Show file/video information only')
    parser.add_argument('--version', action='version', version='Music Splitter 1.0')
    
    args = parser.parse_args()
    
    # Check if GUI dependencies are available
    gui_available = True
    try:
        import tkinter
    except ImportError:
        gui_available = False
        print("⚠️  GUI not available (tkinter not installed)")
        if not args.cli:
            print("Switching to CLI mode...")
            args.cli = True
    
    # Handle CLI mode
    if args.cli or args.split or args.youtube:
        run_cli_mode(args)
    elif gui_available:
        run_gui_mode()
    else:
        print("❌ Neither GUI nor CLI options specified, and GUI is not available.")
        print("Use --help for usage information.")
        sys.exit(1)

def run_gui_mode():
    """Launch the GUI application."""
    try:
        print("🚀 Launching Music Splitter GUI...")
        # Try modern GUI first, fallback to simple GUI
        try:
            from modern_gui import MusicSplitterApp
            import tkinter as tk
            root = tk.Tk()
            app = MusicSplitterApp(root)
            root.mainloop()
        except ImportError:
            from simple_gui import main as gui_main
            gui_main()
    except ImportError as e:
        print(f"❌ Error importing GUI components: {e}")
        print("Try running in CLI mode with --cli flag")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error launching GUI: {e}")
        sys.exit(1)

def run_cli_mode(args):
    """Run in command line interface mode."""
    try:
        if args.split:
            # Split local file
            from audio_splitter_librosa import main as splitter_main
            sys.argv = ['audio_splitter_librosa.py', '--input', args.split]
            if args.output:
                sys.argv.extend(['--output', args.output])
            if args.info:
                sys.argv.append('--info')
            splitter_main()
            
        elif args.youtube:
            # Download and split from YouTube
            from youtube_downloader import main as youtube_main
            sys.argv = ['youtube_downloader.py', '--url', args.youtube]
            if args.output:
                sys.argv.extend(['--output', args.output])
            if args.keep_original:
                sys.argv.append('--keep-original')
            if args.info:
                sys.argv.append('--info')
            else:
                sys.argv.append('--split')
            youtube_main()
            
        else:
            # Interactive CLI mode
            run_interactive_cli()
            
    except ImportError as e:
        print(f"❌ Error importing required modules: {e}")
        print("Make sure all dependencies are installed: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error in CLI mode: {e}")
        sys.exit(1)

def run_interactive_cli():
    """Run interactive command line interface."""
    print("🎵 Music Splitter - Interactive CLI Mode")
    print("=" * 50)
    
    while True:
        print("\nOptions:")
        print("1. Split local audio file")
        print("2. Download and split from YouTube")
        print("3. Exit")
        
        try:
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == '1':
                file_path = input("Enter path to audio file: ").strip()
                if not Path(file_path).exists():
                    print("❌ File not found!")
                    continue
                
                output_dir = input("Enter output directory (or press Enter for default): ").strip()
                
                from audio_splitter_librosa import AudioSplitter
                splitter = AudioSplitter()
                vocal_path, instrumental_path = splitter.split_audio(
                    file_path, 
                    output_dir if output_dir else None
                )
                print(f"✓ Files created:")
                print(f"  🎤 Vocals: {vocal_path}")
                print(f"  🎸 Instrumental: {instrumental_path}")
                
            elif choice == '2':
                url = input("Enter YouTube URL: ").strip()
                from youtube_downloader import is_valid_youtube_url, YouTubeDownloader
                
                if not is_valid_youtube_url(url):
                    print("❌ Invalid YouTube URL!")
                    continue
                
                output_dir = input("Enter output directory (or press Enter for default): ").strip()
                keep_original = input("Keep original file? (y/N): ").strip().lower() == 'y'
                
                downloader = YouTubeDownloader()
                vocal_path, instrumental_path = downloader.download_and_split(
                    url,
                    output_dir if output_dir else None,
                    keep_original=keep_original
                )
                print(f"✓ Files created:")
                print(f"  🎤 Vocals: {vocal_path}")
                print(f"  🎸 Instrumental: {instrumental_path}")
                
            elif choice == '3':
                print("👋 Goodbye!")
                break
                
            else:
                print("❌ Invalid choice! Please enter 1, 2, or 3.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
