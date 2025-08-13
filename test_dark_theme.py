#!/usr/bin/env python3
"""
Test Dark Theme GUI Colors
Quick test to preview the new dark theme
"""

import tkinter as tk
from main import VisualRegressionGUI

def test_dark_theme():
    """Test the new dark theme GUI"""
    print("=" * 50)
    print("Testing Dark Theme GUI Colors")
    print("=" * 50)
    
    # Create the GUI
    root = tk.Tk()
    
    try:
        # Initialize the GUI with dark theme
        app = VisualRegressionGUI(root)
        
        print("✅ Dark theme GUI created successfully!")
        print("\nNew Color Scheme:")
        print("  🎨 Main Background: Dark Blue-Gray (#2c3e50)")
        print("  🎨 Text Areas: Darker Gray (#34495e)")
        print("  🎨 Text Color: Light Gray (#ecf0f1)")
        print("  🎨 Selections: Blue (#3498db)")
        print("  🎨 Canvas: Dark Gray (#34495e)")
        
        print("\nGUI is now running with the new dark theme!")
        print("Close the GUI window to complete the test.")
        
        # Run the GUI
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Error testing dark theme: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 50)
    print("Dark Theme Test Completed")
    print("=" * 50)

if __name__ == "__main__":
    test_dark_theme()
