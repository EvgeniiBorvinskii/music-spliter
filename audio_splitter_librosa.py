import os
import librosa
import soundfile as sf
import numpy as np
import argparse
import sys
from pathlib import Path

# Handle Python 3.13+ compatibility issues
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

class AudioSplitter:
    def __init__(self):
        """Initialize the audio splitter with librosa-based separation."""
        print("✓ Audio splitter initialized with librosa")
    
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
            y, sr = librosa.load(str(input_path), sr=None)
            
            print("🔧 Separating audio sources...")
            
            # Use librosa's harmonic-percussive separation
            # This separates harmonic (tonal) and percussive components
            y_harmonic, y_percussive = librosa.effects.hpss(y)
            
            # Use spectral centroid-based separation for vocals
            # Convert to stereo if mono
            if len(y.shape) == 1:
                y_stereo = np.stack([y, y])
            else:
                y_stereo = y
            
            # Use center channel extraction (simple vocal isolation)
            # This works best with stereo recordings where vocals are centered
            if len(y_stereo.shape) > 1 and y_stereo.shape[0] >= 2:
                # Center channel (vocals) - subtract sides
                center = y_stereo[0] - y_stereo[1]
                # Sides (instrumental) - add channels
                sides = (y_stereo[0] + y_stereo[1]) / 2
                
                # Apply some smoothing
                vocals = librosa.effects.preemphasis(center)
                instrumental = sides
            else:
                # Fallback for mono files - use harmonic separation
                vocals = y_harmonic
                instrumental = y_percussive
            
            # Apply some noise reduction
            vocals = librosa.effects.trim(vocals, top_db=20)[0]
            instrumental = librosa.effects.trim(instrumental, top_db=20)[0]
            
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
    
    def split_audio_advanced(self, input_path, output_dir=None):
        """
        Advanced audio separation using STFT and masking.
        """
        try:
            input_path = Path(input_path)
            
            if not input_path.exists():
                raise FileNotFoundError(f"Input file not found: {input_path}")
            
            if output_dir is None:
                output_dir = input_path.parent / "split_output"
            else:
                output_dir = Path(output_dir)
            
            output_dir.mkdir(exist_ok=True)
            
            print(f"🎵 Processing (Advanced): {input_path.name}")
            
            # Load audio
            y, sr = librosa.load(str(input_path), sr=None)
            
            # Compute STFT
            S = librosa.stft(y)
            magnitude = np.abs(S)
            phase = np.angle(S)
            
            # Create masks for separation
            # Vocal mask: emphasize center frequencies and reduce sides
            vocal_mask = np.ones_like(magnitude)
            instrumental_mask = np.ones_like(magnitude)
            
            # Simple frequency-based separation
            # Vocals typically in mid-range frequencies (300-3000 Hz)
            freqs = librosa.fft_frequencies(sr=sr)
            vocal_freq_range = (freqs >= 300) & (freqs <= 3000)
            
            # Enhance vocals in vocal frequency range
            vocal_mask[vocal_freq_range] *= 1.5
            instrumental_mask[vocal_freq_range] *= 0.3
            
            # Apply masks
            S_vocals = magnitude * vocal_mask * np.exp(1j * phase)
            S_instrumental = magnitude * instrumental_mask * np.exp(1j * phase)
            
            # Convert back to time domain
            vocals = librosa.istft(S_vocals)
            instrumental = librosa.istft(S_instrumental)
            
            # Normalize
            vocals = librosa.util.normalize(vocals)
            instrumental = librosa.util.normalize(instrumental)
            
            # Save files
            base_name = input_path.stem
            vocal_path = output_dir / f"{base_name}_vocals_advanced.wav"
            instrumental_path = output_dir / f"{base_name}_instrumental_advanced.wav"
            
            sf.write(str(vocal_path), vocals, sr)
            sf.write(str(instrumental_path), instrumental, sr)
            
            print(f"✓ Advanced vocal track saved: {vocal_path}")
            print(f"✓ Advanced instrumental track saved: {instrumental_path}")
            
            return str(vocal_path), str(instrumental_path)
            
        except Exception as e:
            print(f"✗ Error during advanced audio splitting: {e}")
            raise e
    
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
        except Exception as e:
            print(f"Error getting audio info: {e}")
            return None

def main():
    """Command line interface for audio splitting."""
    parser = argparse.ArgumentParser(description='Split audio into vocal and instrumental tracks')
    parser.add_argument('--input', '-i', required=True, help='Input audio file path')
    parser.add_argument('--output', '-o', help='Output directory (optional)')
    parser.add_argument('--info', action='store_true', help='Show audio file information')
    parser.add_argument('--advanced', action='store_true', help='Use advanced separation method')
    
    args = parser.parse_args()
    
    try:
        splitter = AudioSplitter()
        
        if args.info:
            info = splitter.get_audio_info(args.input)
            if info:
                print(f"\n📊 Audio Information:")
                print(f"   Duration: {info['duration']:.2f} seconds")
                print(f"   Sample Rate: {info['sample_rate']} Hz")
                print(f"   Channels: {info['channels']}")
                print(f"   Total Samples: {info['samples']}")
        
        if args.advanced:
            vocal_path, instrumental_path = splitter.split_audio_advanced(args.input, args.output)
        else:
            vocal_path, instrumental_path = splitter.split_audio(args.input, args.output)
        
        print(f"\n🎉 Audio splitting completed successfully!")
        print(f"📂 Files created:")
        print(f"   🎤 Vocals: {vocal_path}")
        print(f"   🎸 Instrumental: {instrumental_path}")
        
        print(f"\n💡 Note: This uses librosa-based separation.")
        print(f"   For better results, consider using AI-based tools like:")
        print(f"   - Spleeter (requires compatible TensorFlow)")
        print(f"   - LALAL.AI (online service)")
        print(f"   - Ultimate Vocal Remover")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
