#!/usr/bin/env python3
"""
Test script to verify all dependencies are properly installed
"""

import sys
import os

def test_dependencies():
    """Test if all required dependencies are available"""
    dependencies = [
        'tkinter',
        'PIL',
        'cv2',
        'numpy',
        'sklearn',
        'selenium',
        'matplotlib',
        'reportlab'
    ]
    
    missing = []
    
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✅ {dep} - OK")
        except ImportError as e:
            print(f"❌ {dep} - MISSING: {e}")
            missing.append(dep)
    
    if missing:
        print(f"\n❌ Missing dependencies: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False
    else:
        print("\n🎉 All dependencies are installed!")
        return True

if __name__ == "__main__":
    print("Testing Visual AI Regression Module Dependencies...")
    print("=" * 50)
    
    success = test_dependencies()
    
    if success:
        print("\n✅ Ready to run the application!")
        sys.exit(0)
    else:
        print("\n❌ Please install missing dependencies first.")
        sys.exit(1)
