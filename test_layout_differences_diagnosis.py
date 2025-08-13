#!/usr/bin/env python3
"""
Test script to diagnose layout differences mismatch between GUI and HTML report.
"""

import sys
import os
import tempfile
import json

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from visual_ai_regression import VisualAIRegression
from report_generator import ReportGenerator

def diagnose_layout_differences():
    """Diagnose where the layout differences mismatch occurs"""
    print("🔍 Diagnosing Layout Differences Mismatch...")
    
    # Create test results that simulate the GUI showing 9 layout differences
    test_results = {
        'similarity_score': 0.85,
        'layout_shifts': [
            'Element 1 moved',
            'Element 2 shifted', 
            'Element 3 repositioned',
            'Element 4 displaced',
            'Element 5 moved',
            'Element 6 shifted',
            'Element 7 repositioned', 
            'Element 8 displaced',
            'Element 9 moved'
        ],  # 9 layout shifts
        'color_differences': ['color1', 'color2'],
        'missing_elements': ['elem1'],
        'new_elements': ['elem2'],
        'ai_analysis': {
            'anomaly_detected': True,
            'semantic_analysis': {
                'layout_changes': ['change1'],
                'content_changes': [], 
                'style_changes': [],
                'structural_changes': []
            }
        },
        'wcag_analysis': {
            'url1': {'compliance_score': 90},
            'url2': {'compliance_score': 85}
        }
    }
    
    test_config = {
        'layout_shift': True,
        'font_color': True,
        'element_detection': True,
        'ai_analysis': True,
        'wcag_analysis': True,
        'url1': 'https://example.com/ref',
        'url2': 'https://example.com/test'
    }
    
    # Test 1: Check _generate_summary_dict
    print("\n📊 Testing summary_dict generation...")
    regression = VisualAIRegression()
    summary_dict = regression._generate_summary_dict(test_results, test_config)
    
    layout_diffs = summary_dict.get('layout_differences', 'NOT FOUND')
    print(f"summary_dict['layout_differences']: {layout_diffs}")
    
    if layout_diffs == 9:
        print("✅ summary_dict correctly has 9 layout differences")
    else:
        print(f"❌ summary_dict has {layout_diffs}, expected 9")
        print("This means the GUI is getting the value from somewhere else")
    
    # Test 2: Check what gets passed to HTML report
    print("\n📄 Testing HTML report generation...")
    
    # Add summary_dict to results like the actual code does
    test_results['summary_dict'] = summary_dict
    
    # Generate HTML report
    report_gen = ReportGenerator()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        html_path = os.path.join(temp_dir, 'layout_diff_test.html')
        
        try:
            report_gen.generate_enhanced_html_report(test_results, test_config, html_path)
            
            # Read and check the HTML
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Find Layout Differences section
            import re
            layout_match = re.search(r'<h3>Layout Differences</h3>\s*<div class="number">(\d+)</div>', html_content)
            if layout_match:
                layout_value = layout_match.group(1)
                print(f"HTML report Layout Differences: {layout_value}")
                
                if layout_value == "9":
                    print("✅ HTML report correctly shows 9 layout differences")
                else:
                    print(f"❌ HTML report shows {layout_value}, expected 9")
            else:
                print("❌ Could not find Layout Differences in HTML")
                
                # Try to find any references to layout
                layout_refs = re.findall(r'layout[^<]*(\d+)', html_content, re.IGNORECASE)
                print(f"Found layout references: {layout_refs}")
            
            # Save debug file
            debug_path = 'layout_differences_debug.html'
            with open(debug_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"Debug HTML saved: {debug_path}")
            
        except Exception as e:
            print(f"Error generating HTML: {e}")
            import traceback
            traceback.print_exc()
    
    # Test 3: Check what might be happening in the actual analysis
    print("\n🔍 Checking data structure assumptions...")
    
    print("test_results keys:", list(test_results.keys()))
    print("layout_shifts in test_results:", 'layout_shifts' in test_results)
    print("len(layout_shifts):", len(test_results.get('layout_shifts', [])))
    
    # Test what happens if layout_shifts is not in the top level
    nested_results = {
        'layout_analysis': {
            'layout_shifts': test_results['layout_shifts']
        },
        'similarity_score': test_results['similarity_score'],
        'color_differences': test_results['color_differences'],
        'missing_elements': test_results['missing_elements'],
        'new_elements': test_results['new_elements'],
        'ai_analysis': test_results['ai_analysis'],
        'wcag_analysis': test_results['wcag_analysis']
    }
    
    print("\n🧪 Testing with nested structure...")
    nested_summary = regression._generate_summary_dict(nested_results, test_config)
    nested_layout_diffs = nested_summary.get('layout_differences', 'NOT FOUND')
    print(f"With nested structure, layout_differences: {nested_layout_diffs}")
    
    if nested_layout_diffs == 'NOT FOUND' or nested_layout_diffs == 0:
        print("⚠️ This could be the issue - layout_shifts might be nested under layout_analysis")

if __name__ == "__main__":
    diagnose_layout_differences()
