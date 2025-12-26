#!/usr/bin/env python3
"""
Music Splitter App - Executable Version
Simplified main entry point that works without complex dependencies
"""

import sys
import argparse
import tkinter as tk
from pathlib import Path

def main():
    """Main entry point for the Music Splitter executable."""
    parser = argparse.ArgumentParser(
        description="Music Splitter - Separate vocals and instrumentals from audio",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    MusicSplitter.exe                                 # Launch GUI
    MusicSplitter.exe --split audio.wav              # Split WAV file
    MusicSplitter.exe --help                         # Show help
        """
    )
    
    parser.add_argument('--split', metavar='FILE', 
                       help='Split audio file (WAV format)')
    parser.add_argument('--output', '-o', metavar='DIR',
                       help='Output directory for processed files')
    parser.add_argument('--info', action='store_true',
                       help='Show file information only')
    parser.add_argument('--version', action='version', version='Music Splitter 1.0')
    
    args = parser.parse_args()
    
    # Handle command line splitting
    if args.split:
        run_cli_split(args)
    else:
        run_gui_mode()

def run_gui_mode():
    """Launch the simplified GUI application."""
    try:
        print("🚀 Launching Music Splitter GUI...")
        from simple_gui import main as gui_main
        gui_main()
    except ImportError as e:
        print(f"❌ Error importing GUI components: {e}")
        print("The executable may be missing required files.")
        input("Press Enter to exit...")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error launching GUI: {e}")
        input("Press Enter to exit...")
        sys.exit(1)

def run_cli_split(args):
    """Run command line splitting."""
    try:
        from simple_audio_splitter import SimpleAudioSplitter
        
        splitter = SimpleAudioSplitter()
        
        if args.info:
            info = splitter.get_audio_info(args.split)
            if info:
                print("\n📊 Audio Information:")
                print(f"   Duration: {info['duration']:.2f} seconds")
                print(f"   Sample Rate: {info['sample_rate']} Hz")
                print(f"   Channels: {info['channels']}")
                print(f"   Total Frames: {info['frames']}")
        
        vocal_path, instrumental_path = splitter.split_audio_simple(
            args.split, 
            args.output
        )
        
        print("\n🎉 Audio splitting completed successfully!")
        print("📂 Files created:")
        print(f"   🎤 Vocals: {vocal_path}")
        print(f"   🎸 Instrumental: {instrumental_path}")
        
        input("\nPress Enter to exit...")
        
    except ImportError as e:
        print(f"❌ Error importing required modules: {e}")
        input("Press Enter to exit...")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()
