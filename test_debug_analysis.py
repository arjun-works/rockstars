#!/usr/bin/env python3
"""
Debug Test for Analysis Results and Configuration
Tests the analysis pipeline to debug empty results tab and missing element detection
"""

import tkinter as tk
from main import VisualRegressionGUI

def test_analysis_config():
    """Test the analysis configuration and results generation"""
    print("=" * 60)
    print("DEBUG: Testing Analysis Configuration and Results")
    print("=" * 60)
    
    # Create a temporary GUI instance to test configuration
    root = tk.Tk()
    root.withdraw()  # Hide the window
    
    try:
        gui = VisualRegressionGUI(root)
        
        # Test 1: Check default configuration
        print("\n1. Testing Default Configuration:")
        print(f"   Layout Shift: {gui.layout_shift_var.get()}")
        print(f"   Font/Color: {gui.font_color_var.get()}")
        print(f"   Element Detection: {gui.element_detection_var.get()}")
        print(f"   AI Analysis: {gui.ai_analysis_var.get()}")
        print(f"   WCAG Analysis: {gui.wcag_analysis_var.get()}")
        
        # Test 2: Check if element detection variable exists
        try:
            element_detection = getattr(gui, 'element_detection_var', None)
            if element_detection:
                print(f"   Element Detection (verified): {element_detection.get()}")
            else:
                print("   Element Detection: NOT FOUND - This is the issue!")
        except Exception as e:
            print(f"   Element Detection Error: {e}")
        
        # Test 3: Test configuration dictionary generation
        print("\n2. Testing Configuration Dictionary:")
        config = {
            'layout_shift': gui.layout_shift_var.get(),
            'font_color': gui.font_color_var.get(),
            'element_detection': gui.element_detection_var.get(),
            'ai_analysis': gui.ai_analysis_var.get(),
            'wcag_analysis': gui.wcag_analysis_var.get()
        }
        
        for key, value in config.items():
            print(f"   {key}: {value}")
        
        # Test 4: Check if results display methods exist
        print("\n3. Testing Results Display Methods:")
        methods_to_check = [
            'display_results',
            'update_summary_display',
            'update_visual_analysis_display',
            'update_ai_detection_display',
            'update_layout_analysis_display',
            'update_color_analysis_display',
            'update_wcag_display'
        ]
        
        for method_name in methods_to_check:
            if hasattr(gui, method_name):
                print(f"   ✓ {method_name}: EXISTS")
            else:
                print(f"   ✗ {method_name}: MISSING")
        
        print("\n4. Testing Sample Results Structure:")
        # Create a sample results structure to test display
        sample_results = {
            'summary': {
                'overall_similarity': 85.5,
                'layout_shift_score': 2.3,
                'color_difference_score': 1.8,
                'ai_confidence': 92.1
            },
            'layout_shift': {'enabled': True, 'data': 'sample'},
            'font_color': {'enabled': True, 'data': 'sample'},
            'element_detection': {'enabled': True, 'data': 'sample'},
            'ai_analysis': {'enabled': True, 'data': 'sample'},
            'wcag_analysis': {'enabled': True, 'data': 'sample'}
        }
        
        for analysis_type, data in sample_results.items():
            print(f"   {analysis_type}: {data}")
        
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        root.destroy()
    
    print("\n" + "=" * 60)
    print("DEBUG TEST COMPLETED")
    print("=" * 60)

if __name__ == "__main__":
    test_analysis_config()
