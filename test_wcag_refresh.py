#!/usr/bin/env python3
"""
Test WCAG refresh functionality with existing report data
"""

import tkinter as tk
from tkinter import ttk
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import VisualRegressionGUI

def test_wcag_refresh():
    """Test the WCAG refresh functionality"""
    print("🧪 Testing WCAG refresh functionality...")
    
    # Create GUI
    root = tk.Tk()
    root.title("WCAG Refresh Test")
    root.geometry("1000x800")
    
    app = VisualRegressionGUI(root)
    
    # Add test controls
    test_frame = ttk.Frame(root)
    test_frame.pack(side="bottom", fill="x", padx=10, pady=10)
    
    def test_refresh():
        print("🔄 Testing refresh functionality...")
        app.refresh_wcag_display()
    
    def test_debug():
        print("🔍 Testing debug functionality...")
        app.debug_wcag_state()
    
    # Test buttons
    ttk.Button(test_frame, text="Test Refresh", command=test_refresh).pack(side="left", padx=5)
    ttk.Button(test_frame, text="Test Debug", command=test_debug).pack(side="left", padx=5)
    
    # Instructions
    instructions = tk.Label(
        test_frame,
        text="Instructions: Click 'Test Refresh' to load WCAG data from latest report. Click 'Test Debug' to see current state.",
        wraplength=600
    )
    instructions.pack(side="right", padx=10)
    
    print("📋 WCAG Refresh Test Window:")
    print("1. Click 'Test Refresh' to load WCAG data from the latest report")
    print("2. Check the WCAG Compliance tab to see if data appears")
    print("3. Click 'Test Debug' to see the current state in the console")
    print("4. Close the window when done testing")
    
    # Start with WCAG tab selected
    app.notebook.select(2)  # WCAG is tab index 2
    
    root.mainloop()

if __name__ == "__main__":
    test_wcag_refresh()
