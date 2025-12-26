"""
Enhanced audio splitter with improved vocal separation algorithms
"""

import os
import wave
import numpy as np
from pathlib import Path
import argparse
import sys
import scipy.signal
from scipy.fft import fft, ifft

class EnhancedAudioSplitter:
    def __init__(self):
        """Initialize enhanced audio splitter."""
        print("✓ Enhanced audio splitter initialized")
    
    def apply_spectral_subtraction(self, audio, noise_factor=0.5):
        """Apply spectral subtraction to reduce noise and improve separation."""
        # Perform FFT
        spectrum = fft(audio)
        magnitude = np.abs(spectrum)
        phase = np.angle(spectrum)
        
        # Estimate noise from the first and last 10% of the signal
        noise_start = magnitude[:len(magnitude)//10]
        noise_end = magnitude[-len(magnitude)//10:]
        noise_estimate = np.mean([np.mean(noise_start), np.mean(noise_end)])
        
        # Spectral subtraction
        clean_magnitude = magnitude - noise_factor * noise_estimate
        clean_magnitude = np.maximum(clean_magnitude, 0.1 * magnitude)  # Floor to prevent artifacts
        
        # Reconstruct signal
        clean_spectrum = clean_magnitude * np.exp(1j * phase)
        clean_audio = np.real(ifft(clean_spectrum))
        
        return clean_audio.astype(audio.dtype)
    
    def apply_bandpass_filter(self, audio, sample_rate, low_freq=80, high_freq=8000):
        """Apply bandpass filter to focus on vocal frequency range."""
        nyquist = sample_rate / 2
        low = low_freq / nyquist
        high = high_freq / nyquist
        
        # Design bandpass filter
        b, a = scipy.signal.butter(4, [low, high], btype='band')
        filtered_audio = scipy.signal.filtfilt(b, a, audio)
        
        return filtered_audio.astype(audio.dtype)
    
    def enhanced_vocal_isolation(self, left, right, sample_rate):
        """Enhanced vocal isolation using multiple techniques."""
        # Method 1: Center channel extraction with improved algorithm
        center = (left - right)
        
        # Method 2: Apply spectral subtraction to clean up the signal
        center_clean = self.apply_spectral_subtraction(center, noise_factor=0.3)
        
        # Method 3: Apply bandpass filter for vocal frequencies (80Hz - 8kHz)
        center_filtered = self.apply_bandpass_filter(center_clean, sample_rate, 80, 8000)
        
        # Method 4: Dynamic range compression to enhance vocals
        center_compressed = self.apply_compression(center_filtered)
        
        # Method 5: Stereo widening for instrumental
        # Use mid-side technique for better instrumental separation
        mid = (left + right) / 2
        side = (left - right) / 2
        
        # Enhance stereo field for instrumental
        instrumental = mid + 0.5 * side
        instrumental_clean = self.apply_spectral_subtraction(instrumental, noise_factor=0.2)
        
        return center_compressed, instrumental_clean
    
    def apply_compression(self, audio, threshold=0.3, ratio=4.0):
        """Apply dynamic range compression to enhance vocals."""
        # Simple compression algorithm
        compressed = np.copy(audio).astype(np.float32)
        
        # Normalize to work with values between -1 and 1
        max_val = np.max(np.abs(compressed))
        if max_val > 0:
            compressed = compressed / max_val
        
        # Apply compression
        mask = np.abs(compressed) > threshold
        compressed[mask] = np.sign(compressed[mask]) * (
            threshold + (np.abs(compressed[mask]) - threshold) / ratio
        )
        
        # Restore original scale
        if max_val > 0:
            compressed = compressed * max_val
        
        return compressed.astype(audio.dtype)
    
    def split_audio_enhanced(self, input_path, output_dir=None):
        """
        Enhanced vocal/instrumental separation with multiple algorithms.
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
            
            # Only process WAV files for now
            if input_path.suffix.lower() != '.wav':
                raise ValueError("This version supports WAV files. Please convert your file to WAV format first.")
            
            # Load WAV file
            print("📖 Loading WAV file...")
            with wave.open(str(input_path), 'rb') as wav_file:
                frames = wav_file.readframes(-1)
                sample_rate = wav_file.getframerate()
                channels = wav_file.getnchannels()
                sample_width = wav_file.getsampwidth()
                
                if channels != 2:
                    raise ValueError("This version requires stereo (2-channel) WAV files for best results.")
                
                # Convert to numpy array
                if sample_width == 1:
                    dtype = np.uint8
                    max_val = 127
                elif sample_width == 2:
                    dtype = np.int16
                    max_val = 32767
                elif sample_width == 4:
                    dtype = np.int32
                    max_val = 2147483647
                else:
                    raise ValueError(f"Unsupported sample width: {sample_width}")
                
                audio_data = np.frombuffer(frames, dtype=dtype)
                audio_data = audio_data.reshape(-1, 2)
                
                left = audio_data[:, 0].astype(np.float32)
                right = audio_data[:, 1].astype(np.float32)
                
                print("🔧 Applying enhanced vocal separation algorithms...")
                print("   • Center channel extraction")
                print("   • Spectral noise reduction")
                print("   • Vocal frequency filtering")
                print("   • Dynamic range compression")
                print("   • Stereo field enhancement")
                
                # Apply enhanced vocal isolation
                vocals_enhanced, instrumental_enhanced = self.enhanced_vocal_isolation(
                    left, right, sample_rate
                )
                
                # Normalize and convert back to original format
                vocals_norm = np.clip(vocals_enhanced, -max_val, max_val).astype(dtype)
                instrumental_norm = np.clip(instrumental_enhanced, -max_val, max_val).astype(dtype)
                
                # Generate output filenames
                base_name = input_path.stem
                vocal_path = output_dir / f"{base_name}_vocals_enhanced.wav"
                instrumental_path = output_dir / f"{base_name}_instrumental_enhanced.wav"
                
                # Save separated tracks
                print("💾 Saving enhanced separated tracks...")
                
                # Save vocals (mono)
                with wave.open(str(vocal_path), 'w') as vocal_wav:
                    vocal_wav.setnchannels(1)
                    vocal_wav.setsampwidth(sample_width)
                    vocal_wav.setframerate(sample_rate)
                    vocal_wav.writeframes(vocals_norm.tobytes())
                
                # Save instrumental (mono)
                with wave.open(str(instrumental_path), 'w') as inst_wav:
                    inst_wav.setnchannels(1)
                    inst_wav.setsampwidth(sample_width)
                    inst_wav.setframerate(sample_rate)
                    inst_wav.writeframes(instrumental_norm.tobytes())
                
                print(f"✓ Enhanced vocal track saved: {vocal_path}")
                print(f"✓ Enhanced instrumental track saved: {instrumental_path}")
                
                return str(vocal_path), str(instrumental_path)
                
        except Exception as e:
            print(f"✗ Error during enhanced audio splitting: {e}")
            raise e
    
    def get_audio_info(self, file_path):
        """Get detailed information about a WAV file."""
        try:
            with wave.open(file_path, 'rb') as wav_file:
                frames = wav_file.getnframes()
                sample_rate = wav_file.getframerate()
                channels = wav_file.getnchannels()
                sample_width = wav_file.getsampwidth()
                duration = frames / sample_rate
                
                return {
                    'duration': duration,
                    'sample_rate': sample_rate,
                    'channels': channels,
                    'frames': frames,
                    'sample_width': sample_width,
                    'bitrate': sample_rate * channels * sample_width * 8
                }
        except Exception as e:
            print(f"Error getting audio info: {e}")
            return None

def main():
    """Command line interface for enhanced audio splitting."""
    parser = argparse.ArgumentParser(description='Enhanced audio splitter with improved vocal separation')
    parser.add_argument('--input', '-i', required=True, help='Input WAV file path')
    parser.add_argument('--output', '-o', help='Output directory (optional)')
    parser.add_argument('--info', action='store_true', help='Show detailed audio file information')
    
    args = parser.parse_args()
    
    try:
        splitter = EnhancedAudioSplitter()
        
        if args.info:
            info = splitter.get_audio_info(args.input)
            if info:
                print("\n📊 Detailed Audio Information:")
                print(f"   Duration: {info['duration']:.2f} seconds")
                print(f"   Sample Rate: {info['sample_rate']} Hz")
                print(f"   Channels: {info['channels']}")
                print(f"   Sample Width: {info['sample_width']} bytes")
                print(f"   Bitrate: {info['bitrate']} bps")
                print(f"   Total Frames: {info['frames']}")
        
        vocal_path, instrumental_path = splitter.split_audio_enhanced(args.input, args.output)
        
        print("\n🎉 Enhanced audio splitting completed successfully!")
        print("📂 Files created:")
        print(f"   🎤 Enhanced Vocals: {vocal_path}")
        print(f"   🎸 Enhanced Instrumental: {instrumental_path}")
        
        print("\n💡 Enhancement Features Applied:")
        print("   ✓ Advanced center/side extraction")
        print("   ✓ Spectral noise reduction")
        print("   ✓ Vocal frequency band optimization")
        print("   ✓ Dynamic range compression")
        print("   ✓ Stereo field enhancement")
        
    except (FileNotFoundError, ValueError, OSError) as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
