import yt_dlp
import os
import sys
from pathlib import Path
import argparse
from audio_splitter_librosa import AudioSplitter

class YouTubeDownloader:
    def __init__(self):
        """Initialize YouTube downloader with optimal settings."""
        self.download_opts = {
            'format': 'bestaudio[ext=m4a]/bestaudio[ext=mp3]/bestaudio',
            'outtmpl': '%(title)s.%(ext)s',
            'extractaudio': True,
            'audioformat': 'mp3',
            'audioquality': '192',
            'noplaylist': True,
            'no_warnings': False,
            'prefer_ffmpeg': True,
            'keepvideo': False,
        }
    
    def download_audio(self, url, output_dir=None):
        """
        Download audio from YouTube URL.
        
        Args:
            url (str): YouTube video URL
            output_dir (str): Directory to save downloaded file
        
        Returns:
            str: Path to downloaded audio file
        """
        try:
            if output_dir is None:
                output_dir = Path.cwd() / "downloads"
            else:
                output_dir = Path(output_dir)
            
            output_dir.mkdir(exist_ok=True)
            
            # Update output template with directory
            self.download_opts['outtmpl'] = str(output_dir / '%(title)s.%(ext)s')
            
            print(f"🌐 Downloading from: {url}")
            print(f"📁 Download directory: {output_dir}")
            
            with yt_dlp.YoutubeDL(self.download_opts) as ydl:
                # Extract video info
                print("📋 Extracting video information...")
                info = ydl.extract_info(url, download=False)
                video_title = info.get('title', 'Unknown')
                duration = info.get('duration', 0)
                
                print(f"🎵 Title: {video_title}")
                print(f"⏱️  Duration: {duration // 60}:{duration % 60:02d}")
                
                # Download the audio
                print("⬇️  Downloading audio...")
                ydl.download([url])
                
                # Find the downloaded file
                downloaded_files = list(output_dir.glob(f"*{video_title[:50]}*"))
                if not downloaded_files:
                    # Fallback: find the most recent file
                    downloaded_files = sorted(output_dir.glob("*"), key=os.path.getctime, reverse=True)
                
                if downloaded_files:
                    downloaded_file = downloaded_files[0]
                    
                    # Check if it's actually an audio file
                    audio_extensions = {'.mp3', '.wav', '.m4a', '.aac', '.ogg', '.flac'}
                    if downloaded_file.suffix.lower() not in audio_extensions:
                        raise ValueError(f"Downloaded file is not a supported audio format: {downloaded_file.suffix}")
                    
                    print(f"✓ Download completed: {downloaded_file.name}")
                    return str(downloaded_file)
                else:
                    raise FileNotFoundError("Downloaded file not found")
                    
        except Exception as e:
            print(f"✗ Download error: {e}")
            raise e
    
    def get_video_info(self, url):
        """Get video information without downloading."""
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    'title': info.get('title', 'Unknown'),
                    'duration': info.get('duration', 0),
                    'uploader': info.get('uploader', 'Unknown'),
                    'view_count': info.get('view_count', 0),
                    'upload_date': info.get('upload_date', 'Unknown')
                }
        except Exception as e:
            print(f"Error getting video info: {e}")
            return None
    
    def download_and_split(self, url, output_dir=None, keep_original=True):
        """
        Download audio from YouTube and automatically split it.
        
        Args:
            url (str): YouTube video URL
            output_dir (str): Directory for output files
            keep_original (bool): Whether to keep the original downloaded file
        
        Returns:
            tuple: Paths to vocal and instrumental files
        """
        try:
            # Download audio
            downloaded_file = self.download_audio(url, output_dir)
            
            # Initialize audio splitter
            print("\n🔧 Initializing audio splitter...")
            splitter = AudioSplitter()
            
            # Split the downloaded audio
            print("🎵 Splitting audio into vocals and instrumentals...")
            vocal_path, instrumental_path = splitter.split_audio(downloaded_file, output_dir)
            
            # Optionally remove original file
            if not keep_original:
                os.remove(downloaded_file)
                print(f"🗑️  Removed original file: {Path(downloaded_file).name}")
            
            return vocal_path, instrumental_path
            
        except Exception as e:
            print(f"✗ Error in download and split process: {e}")
            raise e

def is_valid_youtube_url(url):
    """Check if the URL is a valid YouTube URL."""
    youtube_domains = ['youtube.com', 'youtu.be', 'www.youtube.com', 'm.youtube.com']
    return any(domain in url for domain in youtube_domains)

def main():
    """Command line interface for YouTube downloading and splitting."""
    parser = argparse.ArgumentParser(description='Download audio from YouTube and split into vocal/instrumental')
    parser.add_argument('--url', '-u', required=True, help='YouTube video URL')
    parser.add_argument('--output', '-o', help='Output directory (optional)')
    parser.add_argument('--info', action='store_true', help='Show video information only')
    parser.add_argument('--keep-original', action='store_true', 
                       help='Keep the original downloaded file (default: True)')
    parser.add_argument('--split', action='store_true', 
                       help='Download and automatically split audio (default)')
    
    args = parser.parse_args()
    
    # Validate YouTube URL
    if not is_valid_youtube_url(args.url):
        print("❌ Error: Please provide a valid YouTube URL")
        sys.exit(1)
    
    try:
        downloader = YouTubeDownloader()
        
        if args.info:
            print("📋 Getting video information...")
            info = downloader.get_video_info(args.url)
            if info:
                print(f"\n📊 Video Information:")
                print(f"   🎵 Title: {info['title']}")
                print(f"   👤 Uploader: {info['uploader']}")
                print(f"   ⏱️  Duration: {info['duration'] // 60}:{info['duration'] % 60:02d}")
                print(f"   👀 Views: {info['view_count']:,}")
                print(f"   📅 Upload Date: {info['upload_date']}")
            return
        
        # Default behavior: download and split
        print("🚀 Starting download and split process...\n")
        vocal_path, instrumental_path = downloader.download_and_split(
            args.url, 
            args.output, 
            keep_original=args.keep_original
        )
        
        print(f"\n🎉 Process completed successfully!")
        print(f"📂 Files created:")
        print(f"   🎤 Vocals: {Path(vocal_path).name}")
        print(f"   🎸 Instrumental: {Path(instrumental_path).name}")
        
    except KeyboardInterrupt:
        print("\n⏹️  Process interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
