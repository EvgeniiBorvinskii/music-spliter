"""
Simple audio splitter using basic Python libraries
Compatible with Python 3.13
"""

import os
import sys
import wave
import numpy as np
from pathlib import Path
import argparse

class SimpleAudioSplitter:
    def __init__(self):
        """Initialize simple audio splitter."""
        print("✓ Simple audio splitter initialized")
    
    def split_audio_simple(self, input_path, output_dir=None):
        """
        Simple vocal/instrumental separation using center/side technique.
        Works best with stereo files where vocals are centered.
        """
        try:
            input_path = Path(input_path)
            
            if not input_path.exists():
                raise FileNotFoundError(f"Input file not found: {input_path}")
            
            # Set output directory
            if output_dir is None:
                output_dir = input_path.parent / "split_output"
            else:
                output_dir = Path(output_dir)
            
            output_dir.mkdir(exist_ok=True)
            
            print(f"🎵 Processing: {input_path.name}")
            print(f"📁 Output directory: {output_dir}")
            
            # Only process WAV files for now (simpler)
            if input_path.suffix.lower() != '.wav':
                raise ValueError("This simplified version only supports WAV files. Please convert your file to WAV format first.")
            
            # Load WAV file
            print("📖 Loading WAV file...")
            with wave.open(str(input_path), 'rb') as wav_file:
                frames = wav_file.readframes(-1)
                sample_rate = wav_file.getframerate()
                channels = wav_file.getnchannels()
                sample_width = wav_file.getsampwidth()
                
                if channels != 2:
                    raise ValueError("This simplified version requires stereo (2-channel) WAV files.")
                
                # Convert to numpy array
                if sample_width == 1:
                    dtype = np.uint8
                elif sample_width == 2:
                    dtype = np.int16
                elif sample_width == 4:
                    dtype = np.int32
                else:
                    raise ValueError(f"Unsupported sample width: {sample_width}")
                
                audio_data = np.frombuffer(frames, dtype=dtype)
                audio_data = audio_data.reshape(-1, 2)  # Reshape to stereo
                
                print("🔧 Separating audio using center/side technique...")
                
                # Simple center/side extraction
                left = audio_data[:, 0].astype(np.float32)
                right = audio_data[:, 1].astype(np.float32)
                
                # Center channel (vocals) - difference between channels
                center = (left - right) / 2
                
                # Sides (instrumental) - average of channels
                sides = (left + right) / 2
                
                # Normalize
                center = np.clip(center, -32767, 32767).astype(np.int16)
                sides = np.clip(sides, -32767, 32767).astype(np.int16)
                
                # Generate output filenames
                base_name = input_path.stem
                vocal_path = output_dir / f"{base_name}_vocals.wav"
                instrumental_path = output_dir / f"{base_name}_instrumental.wav"
                
                # Save separated tracks
                print("💾 Saving separated tracks...")
                
                # Save vocals (mono)
                with wave.open(str(vocal_path), 'w') as vocal_wav:
                    vocal_wav.setnchannels(1)
                    vocal_wav.setsampwidth(2)
                    vocal_wav.setframerate(sample_rate)
                    vocal_wav.writeframes(center.tobytes())
                
                # Save instrumental (mono)
                with wave.open(str(instrumental_path), 'w') as inst_wav:
                    inst_wav.setnchannels(1)
                    inst_wav.setsampwidth(2)
                    inst_wav.setframerate(sample_rate)
                    inst_wav.writeframes(sides.tobytes())
                
                print(f"✓ Vocal track saved: {vocal_path}")
                print(f"✓ Instrumental track saved: {instrumental_path}")
                
                return str(vocal_path), str(instrumental_path)
                
        except Exception as e:
            print(f"✗ Error during audio splitting: {e}")
            raise e
    
    def get_audio_info(self, file_path):
        """Get basic information about a WAV file."""
        try:
            with wave.open(file_path, 'rb') as wav_file:
                frames = wav_file.getnframes()
                sample_rate = wav_file.getframerate()
                channels = wav_file.getnchannels()
                duration = frames / sample_rate
                
                return {
                    'duration': duration,
                    'sample_rate': sample_rate,
                    'channels': channels,
                    'frames': frames
                }
        except Exception as e:
            print(f"Error getting audio info: {e}")
            return None

def main():
    """Command line interface for simple audio splitting."""
    parser = argparse.ArgumentParser(description='Simple audio splitter for WAV files')
    parser.add_argument('--input', '-i', required=True, help='Input WAV file path')
    parser.add_argument('--output', '-o', help='Output directory (optional)')
    parser.add_argument('--info', action='store_true', help='Show audio file information')
    
    args = parser.parse_args()
    
    try:
        splitter = SimpleAudioSplitter()
        
        if args.info:
            info = splitter.get_audio_info(args.input)
            if info:
                print("\n📊 Audio Information:")
                print(f"   Duration: {info['duration']:.2f} seconds")
                print(f"   Sample Rate: {info['sample_rate']} Hz")
                print(f"   Channels: {info['channels']}")
                print(f"   Total Frames: {info['frames']}")
        
        vocal_path, instrumental_path = splitter.split_audio_simple(args.input, args.output)
        
        print("\n🎉 Audio splitting completed successfully!")
        print("📂 Files created:")
        print(f"   🎤 Vocals: {vocal_path}")
        print(f"   🎸 Instrumental: {instrumental_path}")
        
        print("\n💡 Note: This is a simplified splitter for WAV files.")
        print("   For best results:")
        print("   - Use stereo recordings with centered vocals")
        print("   - Convert MP3/other formats to WAV first")
        
    except (FileNotFoundError, ValueError, OSError) as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
