#!/usr/bin/env python3
"""
Test script to debug WCAG display issues
"""

import tkinter as tk
from tkinter import ttk
import json
import os
import sys

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import VisualRegressionGUI

def test_wcag_display():
    """Test WCAG display with sample data"""
    print("🔍 Testing WCAG display functionality...")
    
    # Load sample WCAG data from a recent report
    sample_report_path = "reports/visual_regression_report_20250807_185843.json"
    
    if not os.path.exists(sample_report_path):
        print("❌ Sample report not found. Running a quick analysis first...")
        return
    
    with open(sample_report_path, 'r') as f:
        report_data = json.load(f)
    
    # Extract WCAG analysis
    wcag_data = report_data.get('wcag_analysis', {})
    
    print(f"🔍 Report keys: {list(report_data.keys())}")
    print(f"🔍 Analysis results keys: {list(report_data.get('analysis_results', {}).keys())}")
    
    if not wcag_data:
        # Try to find WCAG data in analysis_results
        wcag_data = report_data.get('analysis_results', {}).get('wcag_analysis', {})
        
    if not wcag_data:
        print("❌ No WCAG data found in report")
        print(f"📋 Available data: {json.dumps(report_data, indent=2)[:500]}...")
        return
    
    print(f"✅ Found WCAG data: {list(wcag_data.keys())}")
    
    # Print sample data structure
    for url_key, url_data in wcag_data.items():
        if isinstance(url_data, dict) and 'compliance_score' in url_data:
            print(f"📊 {url_key}: Score={url_data.get('compliance_score')}, Level={url_data.get('compliance_level')}")
    
    # Create GUI instance
    root = tk.Tk()
    root.withdraw()  # Hide main window for testing
    
    app = VisualRegressionGUI(root)
    
    # Test the update_wcag_display method directly
    print("🧪 Testing update_wcag_display method...")
    
    try:
        app.update_wcag_display(wcag_data)
        print("✅ WCAG display updated successfully")
        
        # Check if scores frame has children
        children_count = len(app.wcag_scores_frame.winfo_children())
        print(f"📈 WCAG scores frame has {children_count} child widgets")
        
        # Check WCAG text content
        wcag_text_content = app.wcag_text.get(1.0, tk.END)
        wcag_lines = len(wcag_text_content.strip().split('\n'))
        print(f"📝 WCAG text has {wcag_lines} lines of content")
        
        if children_count > 0 and wcag_lines > 1:
            print("✅ WCAG display appears to be working correctly!")
        else:
            print("⚠️ WCAG display may have issues - empty content")
            
    except Exception as e:
        print(f"❌ Error testing WCAG display: {e}")
        import traceback
        traceback.print_exc()
    
    root.destroy()

if __name__ == "__main__":
    test_wcag_display()
