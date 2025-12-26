#!/usr/bin/env python3
"""
Test script to verify Music Splitter installation
"""

import sys
import importlib

def test_import(module_name, package_name=None):
    """Test if a module can be imported."""
    try:
        importlib.import_module(module_name)
        print(f"✓ {package_name or module_name}")
        return True
    except ImportError as e:
        print(f"✗ {package_name or module_name} - {str(e)}")
        return False

def main():
    print("🔍 Testing Music Splitter Dependencies")
    print("=" * 40)
    
    # Test Python version
    if sys.version_info >= (3, 8):
        print(f"✓ Python {sys.version.split()[0]}")
    else:
        print(f"✗ Python {sys.version.split()[0]} (3.8+ required)")
        return False
    
    # Test required packages
    packages = [
        ('numpy', 'NumPy'),
        ('scipy', 'SciPy'),
        ('librosa', 'Librosa'),
        ('soundfile', 'SoundFile'),
        ('tensorflow', 'TensorFlow'),
        ('spleeter', 'Spleeter'),
        ('yt_dlp', 'yt-dlp'),
        ('PIL', 'Pillow'),
        ('matplotlib', 'Matplotlib'),
        ('tkinter', 'Tkinter (GUI)')
    ]
    
    all_good = True
    for module, name in packages:
        if not test_import(module, name):
            all_good = False
    
    print("\n" + "=" * 40)
    if all_good:
        print("🎉 All dependencies are installed correctly!")
        print("\nYou can now run the application:")
        print("  python main.py       # Launch GUI")
        print("  python main.py --cli # Command line mode")
    else:
        print("❌ Some dependencies are missing.")
        print("Run: pip install -r requirements.txt")
    
    return all_good

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
