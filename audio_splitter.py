import os
import librosa
import soundfile as sf
import numpy as np
import argparse
import sys
from pathlib import Path

class AudioSplitter:
    def __init__(self):
        """Initialize the audio splitter with librosa-based separation."""
        print("✓ Audio splitter initialized (using librosa)")
    
    def split_audio(self, input_path, output_dir=None):
        """
        Split audio file into vocal and instrumental tracks using librosa.
        
        Args:
            input_path (str): Path to the input audio file
            output_dir (str): Directory to save output files (optional)
        
        Returns:
            tuple: Paths to vocal and instrumental files
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
            
            # Load audio file
            print("📖 Loading audio file...")
            y, sr = librosa.load(str(input_path), sr=None, mono=False)
            
            print("🔧 Separating audio sources...")
            
            # Handle stereo vs mono
            if y.ndim == 2:
                # Stereo file - use center/side extraction
                left = y[0]
                right = y[1]
                
                # Center channel (vocals) - difference between channels
                center = (left - right) * 0.5
                
                # Sides (instrumental) - sum of channels
                sides = (left + right) * 0.5
                
                # Apply some processing to enhance separation
                vocals = librosa.effects.preemphasis(center)
                instrumental = sides
                
                # Apply harmonic-percussive separation for better results
                vocals_harmonic, _ = librosa.effects.hpss(vocals)
                _, instrumental_percussive = librosa.effects.hpss(instrumental)
                
                # Combine for final result
                vocals = vocals_harmonic * 0.7 + vocals * 0.3
                instrumental = instrumental_percussive * 0.7 + instrumental * 0.3
                
            else:
                # Mono file - use harmonic-percussive separation
                vocals, instrumental = librosa.effects.hpss(y)
                
                # Apply additional filtering
                vocals = librosa.effects.preemphasis(vocals)
            
            # Normalize audio
            vocals = librosa.util.normalize(vocals)
            instrumental = librosa.util.normalize(instrumental)
            
            # Apply noise gate to reduce artifacts
            vocals = self._apply_noise_gate(vocals, threshold=0.01)
            instrumental = self._apply_noise_gate(instrumental, threshold=0.01)
            
            # Generate output filenames
            base_name = input_path.stem
            vocal_path = output_dir / f"{base_name}_vocals.wav"
            instrumental_path = output_dir / f"{base_name}_instrumental.wav"
            
            # Save separated tracks
            print("💾 Saving separated tracks...")
            sf.write(str(vocal_path), vocals, sr)
            sf.write(str(instrumental_path), instrumental, sr)
            
            print(f"✓ Vocal track saved: {vocal_path}")
            print(f"✓ Instrumental track saved: {instrumental_path}")
            
            return str(vocal_path), str(instrumental_path)
            
        except Exception as e:
            print(f"✗ Error during audio splitting: {e}")
            raise e
    
    def _apply_noise_gate(self, audio, threshold=0.01):
        """Apply a simple noise gate to reduce low-level noise."""
        gate = np.abs(audio) > threshold
        return audio * gate
    
    def get_audio_info(self, file_path):
        """Get basic information about an audio file."""
        try:
            audio, sr = librosa.load(file_path, sr=None)
            duration = len(audio) / sr
            
            return {
                'duration': duration,
                'sample_rate': sr,
                'channels': 1 if len(audio.shape) == 1 else audio.shape[0],
                'samples': len(audio)
            }
        except (OSError, ValueError, librosa.util.exceptions.ParameterError) as e:
            print(f"Error getting audio info: {e}")
            return None

def main():
    """Command line interface for audio splitting."""
    parser = argparse.ArgumentParser(description='Split audio into vocal and instrumental tracks')
    parser.add_argument('--input', '-i', required=True, help='Input audio file path')
    parser.add_argument('--output', '-o', help='Output directory (optional)')
    parser.add_argument('--info', action='store_true', help='Show audio file information')
    
    args = parser.parse_args()
    
    try:
        splitter = AudioSplitter()
        
        if args.info:
            info = splitter.get_audio_info(args.input)
            if info:
                print("\n📊 Audio Information:")
                print(f"   Duration: {info['duration']:.2f} seconds")
                print(f"   Sample Rate: {info['sample_rate']} Hz")
                print(f"   Channels: {info['channels']}")
                print(f"   Total Samples: {info['samples']}")
        
        vocal_path, instrumental_path = splitter.split_audio(args.input, args.output)
        
        print("\n🎉 Audio splitting completed successfully!")
        print("📂 Files created:")
        print(f"   🎤 Vocals: {vocal_path}")
        print(f"   🎸 Instrumental: {instrumental_path}")
        
    except (FileNotFoundError, ValueError, OSError) as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
