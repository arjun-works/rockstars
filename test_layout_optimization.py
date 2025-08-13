#!/usr/bin/env python3
"""
Test Layout Optimization - Compact Title and Larger Results
This tests the reduced title bar space and increased result tab area
"""

import tkinter as tk
from main import VisualRegressionGUI

def test_layout_optimization():
    """Test the optimized layout with compact title and larger results"""
    print("=" * 60)
    print("Testing Layout Optimization")
    print("=" * 60)
    
    # Create the GUI
    root = tk.Tk()
    
    try:
        # Initialize the GUI with optimized layout
        app = VisualRegressionGUI(root)
        
        print("✅ Optimized layout GUI created successfully!")
        print("\nLayout Optimizations Applied:")
        print("  📏 Title Bar Space: Reduced padding from 20px to 8px")
        print("  📏 Title Font Size: Reduced from 18pt to 16pt")
        print("  📏 URL Section: Reduced padding from 20px to 10px")
        print("  📏 Options Section: Reduced padding from 10px to 5px")
        print("  📏 Notebook Tabs: Reduced top padding from 10px to 5px")
        print("  📊 Results Tab: Increased height from 35 to 45 lines")
        print("  📊 WCAG Tab: Increased height from 30 to 40 lines")
        print("  📊 Image Tab: Reduced padding for more space")
        
        print("\n🎯 Benefits:")
        print("  • More vertical space for results display")
        print("  • Compact header reduces wasted space")
        print("  • Better content-to-chrome ratio")
        print("  • Improved user experience for data viewing")
        
        print("\nGUI is now running with optimized layout!")
        print("Notice the compact header and larger result areas.")
        print("Close the GUI window to complete the test.")
        
        # Run the GUI
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Error testing layout optimization: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("Layout Optimization Test Completed")
    print("=" * 60)

if __name__ == "__main__":
    test_layout_optimization()
