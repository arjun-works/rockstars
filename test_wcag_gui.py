#!/usr/bin/env python3
"""
Test WCAG display with actual report data
"""

import tkinter as tk
from tkinter import ttk
import json
import os
import sys

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import VisualRegressionGUI

def test_wcag_display_with_real_data():
    """Test WCAG display with actual report data"""
    print("🔍 Testing WCAG display with real data...")
    
    # Load the latest report
    import glob
    reports = glob.glob('reports/visual_regression_report_*.json')
    if not reports:
        print("❌ No reports found")
        return
    
    latest_report = max(reports, key=os.path.getmtime)
    print(f"📄 Loading report: {os.path.basename(latest_report)}")
    
    with open(latest_report, 'r') as f:
        report_data = json.load(f)
    
    # Extract WCAG data
    wcag_data = report_data.get('analysis_results', {}).get('wcag_analysis', {})
    
    if not wcag_data:
        print("❌ No WCAG data found in report")
        return
    
    print(f"✅ Found WCAG data: {list(wcag_data.keys())}")
    
    # Create GUI for testing
    root = tk.Tk()
    root.title("WCAG Display Test")
    root.geometry("800x600")
    
    app = VisualRegressionGUI(root)
    
    # Test the update directly
    print("🧪 Testing WCAG display update...")
    
    try:
        app.update_wcag_display(wcag_data)
        print("✅ WCAG display updated successfully")
        
        # Check if data is displayed
        children_count = len(app.wcag_scores_frame.winfo_children())
        print(f"📊 WCAG scores frame has {children_count} child widgets")
        
        # Get text content
        wcag_text_content = app.wcag_text.get(1.0, tk.END)
        wcag_lines = len([line for line in wcag_text_content.split('\n') if line.strip()])
        print(f"📝 WCAG text has {wcag_lines} lines of content")
        
        # Print first few lines for verification
        lines = wcag_text_content.split('\n')[:10]
        print("📋 First 10 lines of WCAG text:")
        for i, line in enumerate(lines):
            if line.strip():
                print(f"  {i+1}: {line[:80]}...")
        
        # Show the window for manual verification
        print("👁️ GUI window will appear for manual verification...")
        print("Close the window when done.")
        
        # Start the GUI event loop
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Error testing WCAG display: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_wcag_display_with_real_data()
