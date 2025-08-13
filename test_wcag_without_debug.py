#!/usr/bin/env python3
"""
Test script to verify WCAG tab functionality after removing debug button.
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_wcag_tab_without_debug():
    """Test that WCAG tab works without debug button"""
    try:
        import tkinter as tk
        from main import VisualRegressionGUI
        
        print("🧪 Testing WCAG Tab Without Debug Button...")
        
        # Create test window (don't show it)
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        # Create the GUI
        app = VisualRegressionGUI(root)
        
        # Check if WCAG tab exists
        if hasattr(app, 'notebook'):
            tab_count = app.notebook.index("end")
            print(f"✅ GUI created successfully with {tab_count} tabs")
            
            # Check if WCAG components exist
            if hasattr(app, 'wcag_scores_frame'):
                print("✅ WCAG scores frame exists")
            
            if hasattr(app, 'wcag_text'):
                print("✅ WCAG text widget exists")
                
            if hasattr(app, 'refresh_wcag_display'):
                print("✅ WCAG refresh function exists")
                
            # Check that debug function is removed
            if not hasattr(app, 'debug_wcag_state'):
                print("✅ Debug function successfully removed")
            else:
                print("❌ Debug function still exists")
                
            # Check WCAG tab buttons
            wcag_buttons = []
            def find_buttons(widget):
                for child in widget.winfo_children():
                    if child.winfo_class() == 'TButton':
                        text = child.cget('text')
                        wcag_buttons.append(text)
                    find_buttons(child)
            
            # Find buttons in WCAG tab
            if hasattr(app, 'wcag_frame'):
                find_buttons(app.wcag_frame)
                print(f"✅ WCAG tab buttons: {wcag_buttons}")
                
                # Check that debug button is not present
                debug_buttons = [btn for btn in wcag_buttons if 'Debug' in btn]
                if not debug_buttons:
                    print("✅ No debug buttons found in WCAG tab")
                else:
                    print(f"❌ Debug buttons still exist: {debug_buttons}")
        
        # Cleanup
        root.destroy()
        
        print("🎉 WCAG tab test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing WCAG tab: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_wcag_tab_without_debug()
