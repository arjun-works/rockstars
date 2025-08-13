#!/usr/bin/env python3
"""
Quick debug test to see what's in the summary_dict being passed to HTML generation
"""

import sys
import os
import tempfile
import json

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from report_generator import ReportGenerator

def debug_summary_dict():
    """Debug what's actually in the summary_dict"""
    
    # Create exact test data that should work
    test_results = {
        'summary_dict': {
            'similarity_score': 0.857,
            'layout_differences': 3,
            'color_differences': 7,
            'element_changes': 3,
            'ai_anomalies': 5,  # This should show as 5
            'wcag_url1_score': 88,
            'wcag_url2_score': 92
        },
        'screenshots': {'url1': 'test1.png', 'url2': 'test2.png'},
        'comparisons': {
            'similarity': 0.857,
            'layout_shifts': ['shift1', 'shift2', 'shift3'],
            'color_differences': ['diff1', 'diff2', 'diff3', 'diff4', 'diff5', 'diff6', 'diff7'],
            'missing_elements': ['elem1', 'elem2'],
            'new_elements': ['elem3'],
            'overlapping_elements': []
        },
        'ai_analysis': {
            'anomalies': ['anom1', 'anom2', 'anom3', 'anom4']  # This has 4 items
        },
        'wcag_analysis': {
            'url1': {'compliance_score': 88},
            'url2': {'compliance_score': 92}
        }
    }
    
    test_config = {
        'url1': 'https://example.com/reference',
        'url2': 'https://example.com/test',
        'browser': 'chrome'
    }
    
    # Generate HTML and see what gets used
    report_gen = ReportGenerator()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        html_path = os.path.join(temp_dir, 'debug_summary.html')
        
        try:
            report_gen.generate_enhanced_html_report(test_results, test_config, html_path)
            
            # Read and check the HTML
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Find AI Anomalies section
            import re
            ai_match = re.search(r'<h3>AI Anomalies</h3>\s*<div class="number">(\d+)</div>', html_content)
            if ai_match:
                ai_value = ai_match.group(1)
                print(f"AI Anomalies value in HTML: {ai_value}")
                
                if ai_value == "5":
                    print("✅ AI Anomalies correctly shows 5 (from summary_dict)")
                else:
                    print(f"❌ AI Anomalies shows {ai_value}, but should be 5")
                    print("This suggests summary_dict is not being used correctly or the value is wrong")
            
            # Check what summary_dict actually contains
            summary = test_results.get('summary_dict', {})
            print(f"summary_dict['ai_anomalies']: {summary.get('ai_anomalies', 'NOT FOUND')}")
            
            # Save debug file
            debug_path = 'debug_ai_anomalies.html'
            with open(debug_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"Debug HTML saved: {debug_path}")
            
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    debug_summary_dict()
