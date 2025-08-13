#!/usr/bin/env python3
"""
Test GUI Launch - Simple verification that the GUI opens correctly
"""

import tkinter as tk
import sys
import os

def test_gui_launch():
    """Test if the GUI can be launched successfully"""
    print("=" * 50)
    print("Testing GUI Launch Fix")
    print("=" * 50)
    
    try:
        # Test tkinter availability
        print("1. Testing Tkinter availability...")
        root = tk.Tk()
        root.withdraw()  # Hide test window
        print("   ✅ Tkinter is available")
        root.destroy()
        
        # Test main.py import
        print("2. Testing main.py import...")
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import main
        print("   ✅ main.py imports successfully")
        
        # Test GUI class creation
        print("3. Testing GUI class creation...")
        test_root = tk.Tk()
        test_root.withdraw()  # Hide test window
        app = main.VisualRegressionGUI(test_root)
        print("   ✅ VisualRegressionGUI class creates successfully")
        test_root.destroy()
        
        print("\n🎉 ALL TESTS PASSED!")
        print("\nThe GUI should now open when you run:")
        print("   • launch_gui.bat")
        print("   • python main.py")
        print("   • venv\\Scripts\\python.exe main.py")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    test_gui_launch()
