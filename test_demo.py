#!/usr/bin/env python3
"""
Demo script to test local audio splitting functionality
"""

import sys
import os
from pathlib import Path

# Add the current directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from audio_splitter_librosa import AudioSplitter

def create_test_audio():
    """Create a simple test audio file using numpy and soundfile."""
    try:
        import numpy as np
        import soundfile as sf
        
        # Create a simple stereo test signal
        sample_rate = 22050
        duration = 3  # 3 seconds
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        
        # Create a simple melody (left channel) and bass (right channel)
        melody = np.sin(2 * np.pi * 440 * t)  # A4 note
        bass = np.sin(2 * np.pi * 220 * t)    # A3 note
        
        # Create stereo signal
        stereo_signal = np.column_stack((melody, bass))
        
        # Save as test file
        test_file = Path("test_audio.wav")
        sf.write(str(test_file), stereo_signal, sample_rate)
        
        print(f"✓ Created test audio file: {test_file}")
        return str(test_file)
        
    except ImportError as e:
        print(f"✗ Cannot create test audio: {e}")
        return None

def test_audio_splitting():
    """Test the audio splitting functionality."""
    print("🧪 Testing Audio Splitter")
    print("=" * 30)
    
    # Create test audio
    test_file = create_test_audio()
    if not test_file:
        print("❌ Cannot proceed without test audio file")
        return False
    
    try:
        # Initialize splitter
        splitter = AudioSplitter()
        
        # Test file info
        print("\n📊 Getting audio information...")
        info = splitter.get_audio_info(test_file)
        if info:
            print(f"   Duration: {info['duration']:.2f} seconds")
            print(f"   Sample Rate: {info['sample_rate']} Hz")
            print(f"   Channels: {info['channels']}")
        
        # Test splitting
        print("\n🎵 Testing audio splitting...")
        vocal_path, instrumental_path = splitter.split_audio(test_file, "test_output")
        
        print(f"\n✅ Test completed successfully!")
        print(f"📂 Output files:")
        print(f"   🎤 Vocals: {vocal_path}")
        print(f"   🎸 Instrumental: {instrumental_path}")
        
        # Check if files exist
        if Path(vocal_path).exists() and Path(instrumental_path).exists():
            print("\n✅ All output files created successfully!")
            
            # Show file sizes
            vocal_size = Path(vocal_path).stat().st_size
            instrumental_size = Path(instrumental_path).stat().st_size
            print(f"   Vocal file size: {vocal_size} bytes")
            print(f"   Instrumental file size: {instrumental_size} bytes")
            
            return True
        else:
            print("\n❌ Some output files are missing")
            return False
            
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return False
    
    finally:
        # Clean up test file
        if test_file and Path(test_file).exists():
            Path(test_file).unlink()
            print(f"\n🧹 Cleaned up test file: {test_file}")

def main():
    """Main test function."""
    print("🎵 Music Splitter - Local File Test")
    print("=" * 40)
    
    success = test_audio_splitting()
    
    if success:
        print("\n🎉 All tests passed! The audio splitter is working correctly.")
        print("\nYou can now:")
        print("  1. Run the GUI: python main.py")
        print("  2. Use CLI: python main.py --cli")
        print("  3. Split files directly: python main.py --split 'your_file.mp3'")
    else:
        print("\n❌ Tests failed. Please check the error messages above.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
