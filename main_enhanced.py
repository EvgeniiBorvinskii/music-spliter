"""
Main entry point for enhanced Music Splitter Pro with modern dark theme
"""

import sys
import argparse
from pathlib import Path

def run_gui():
    """Launch the modern dark theme GUI"""
    try:
        import tkinter as tk
        from modern_gui import ModernMusicSplitterGUI
        
        print("🎵 Launching Music Splitter Pro - Dark Edition...")
        
        root = tk.Tk()
        app = ModernMusicSplitterGUI(root)
        root.mainloop()
        
    except ImportError as e:
        print(f"Error importing GUI components: {e}")
        print("Falling back to simple GUI...")
        
        try:
            from simple_gui import SimpleMusicSplitterGUI
            import tkinter as tk
            
            root = tk.Tk()
            app = SimpleMusicSplitterGUI(root)
            root.mainloop()
            
        except ImportError:
            print("❌ GUI not available. Please install tkinter.")
            sys.exit(1)

def run_cli():
    """Launch CLI interface"""
    print("🎵 Music Splitter Pro - CLI Mode")
    print("=" * 50)
    
    try:
        from enhanced_audio_splitter import EnhancedAudioSplitter
        splitter_class = EnhancedAudioSplitter
        print("✓ Using Enhanced Audio Splitter")
    except ImportError:
        try:
            from simple_audio_splitter import SimpleAudioSplitter
            splitter_class = SimpleAudioSplitter
            print("✓ Using Simple Audio Splitter")
        except ImportError:
            print("❌ No audio splitter available!")
            sys.exit(1)
    
    # Interactive CLI
    splitter = splitter_class()
    
    while True:
        print("\n📋 Options:")
        print("1. 🎵 Split audio file")
        print("2. 📺 Download from YouTube")
        print("3. ⬇️🎵 Download from YouTube and split")
        print("4. ❌ Exit")
        
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == "1":
            file_path = input("Enter audio file path: ").strip()
            if not file_path:
                print("❌ No file path provided!")
                continue
            
            try:
                if hasattr(splitter, 'split_audio_enhanced'):
                    vocal_path, instrumental_path = splitter.split_audio_enhanced(file_path)
                else:
                    vocal_path, instrumental_path = splitter.split_audio_simple(file_path)
                
                print(f"\n✅ Split completed!")
                print(f"🎤 Vocals: {vocal_path}")
                print(f"🎸 Instrumental: {instrumental_path}")
                
            except Exception as e:
                print(f"❌ Error: {e}")
        
        elif choice == "2":
            try:
                from youtube_downloader import YouTubeDownloader
                downloader = YouTubeDownloader()
                
                url = input("Enter YouTube URL: ").strip()
                if not url:
                    print("❌ No URL provided!")
                    continue
                
                output_dir = Path("downloads")
                output_dir.mkdir(exist_ok=True)
                
                downloaded_file = downloader.download(url, str(output_dir))
                print(f"✅ Downloaded: {downloaded_file}")
                
            except ImportError:
                print("❌ YouTube downloader not available!")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        elif choice == "3":
            try:
                from youtube_downloader import YouTubeDownloader
                downloader = YouTubeDownloader()
                
                url = input("Enter YouTube URL: ").strip()
                if not url:
                    print("❌ No URL provided!")
                    continue
                
                print("⬇️ Downloading from YouTube...")
                output_dir = Path("downloads")
                output_dir.mkdir(exist_ok=True)
                
                downloaded_file = downloader.download(url, str(output_dir))
                print(f"✅ Downloaded: {downloaded_file}")
                
                print("🎵 Splitting audio...")
                if hasattr(splitter, 'split_audio_enhanced'):
                    vocal_path, instrumental_path = splitter.split_audio_enhanced(downloaded_file)
                else:
                    vocal_path, instrumental_path = splitter.split_audio_simple(downloaded_file)
                
                print(f"\n✅ Download and split completed!")
                print(f"🎤 Vocals: {vocal_path}")
                print(f"🎸 Instrumental: {instrumental_path}")
                
            except ImportError:
                print("❌ YouTube downloader not available!")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        elif choice == "4":
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid option! Please select 1-4.")

def split_direct(file_path, output_dir=None):
    """Direct splitting function for command line use"""
    try:
        from enhanced_audio_splitter import EnhancedAudioSplitter
        splitter = EnhancedAudioSplitter()
        return splitter.split_audio_enhanced(file_path, output_dir)
    except ImportError:
        from simple_audio_splitter import SimpleAudioSplitter
        splitter = SimpleAudioSplitter()
        return splitter.split_audio_simple(file_path, output_dir)

def main():
    """Main entry point with argument parsing"""
    parser = argparse.ArgumentParser(description='🎵 Music Splitter Pro - Enhanced Edition')
    parser.add_argument('--cli', action='store_true', help='Run in CLI mode')
    parser.add_argument('--split', help='Split audio file directly')
    parser.add_argument('--output', '-o', help='Output directory')
    parser.add_argument('--youtube', help='Download and split YouTube video')
    parser.add_argument('--version', action='version', version='Music Splitter Pro v2.0 Enhanced')
    
    args = parser.parse_args()
    
    # Print banner
    print("=" * 60)
    print("🎵 MUSIC SPLITTER PRO - ENHANCED EDITION v2.0")
    print("🌙 Dark Theme • Enhanced Algorithms • YouTube Integration")
    print("=" * 60)
    
    if args.split:
        # Direct split mode
        try:
            print(f"🎵 Splitting: {args.split}")
            vocal_path, instrumental_path = split_direct(args.split, args.output)
            print(f"\n✅ Split completed!")
            print(f"🎤 Vocals: {vocal_path}")
            print(f"🎸 Instrumental: {instrumental_path}")
        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)
    
    elif args.youtube:
        # YouTube mode
        try:
            from youtube_downloader import YouTubeDownloader
            from enhanced_audio_splitter import EnhancedAudioSplitter
            
            downloader = YouTubeDownloader()
            splitter = EnhancedAudioSplitter()
            
            print(f"📺 Downloading from YouTube: {args.youtube}")
            output_dir = Path(args.output) if args.output else Path("downloads")
            output_dir.mkdir(exist_ok=True)
            
            downloaded_file = downloader.download(args.youtube, str(output_dir))
            print(f"✅ Downloaded: {downloaded_file}")
            
            print("🎵 Splitting audio...")
            vocal_path, instrumental_path = splitter.split_audio_enhanced(downloaded_file)
            
            print(f"\n✅ YouTube download and split completed!")
            print(f"🎤 Vocals: {vocal_path}")
            print(f"🎸 Instrumental: {instrumental_path}")
            
        except ImportError as e:
            print(f"❌ Feature not available: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)
    
    elif args.cli:
        # CLI mode
        run_cli()
    
    else:
        # Default: GUI mode
        run_gui()

if __name__ == "__main__":
    main()
