#!/usr/bin/env python3
"""
Debug test to check data flow mismatch between GUI and HTML report for layout differences.
This test simulates the actual application structure.
"""

import sys
import os
import tempfile

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from visual_ai_regression import VisualAIRegression
from report_generator import ReportGenerator

def debug_data_flow_mismatch():
    """Debug the exact data flow to find layout differences mismatch"""
    print("🔍 Debugging Layout Differences Data Flow Mismatch...")
    
    # Create simulated analysis results as they would come from actual analysis
    analysis_results = {
        'similarity_score': 0.85,
        'layout_shifts': [
            {'distance': 10.0, 'shift_x': 5, 'shift_y': 5},
            {'distance': 15.0, 'shift_x': 8, 'shift_y': 7},
            {'distance': 12.0, 'shift_x': 6, 'shift_y': 6},
            {'distance': 18.0, 'shift_x': 9, 'shift_y': 9},
            {'distance': 14.0, 'shift_x': 7, 'shift_y': 7},
            {'distance': 11.0, 'shift_x': 5, 'shift_y': 6},
            {'distance': 16.0, 'shift_x': 8, 'shift_y': 8},
            {'distance': 13.0, 'shift_x': 6, 'shift_y': 7},
            {'distance': 17.0, 'shift_x': 9, 'shift_y': 8}
        ],  # 9 layout shifts
        'color_differences': [
            {'position': (100, 100, 150, 150), 'color_distance': 25.0, 'area': 2500},
            {'position': (200, 200, 250, 250), 'color_distance': 30.0, 'area': 2500}
        ],
        'missing_elements': [
            {'type': 'div', 'position': (300, 300, 400, 400)}
        ],
        'new_elements': [
            {'type': 'span', 'position': (500, 500, 600, 600)}
        ],
        'ai_analysis': {
            'anomaly_detected': True,
            'confidence': 0.95,
            'feature_distance': 0.23,
            'semantic_analysis': {
                'layout_changes': ['header moved'],
                'content_changes': [],
                'style_changes': [],
                'structural_changes': []
            }
        },
        'wcag_analysis': {
            'url1': {'compliance_score': 90, 'compliance_level': 'AA'},
            'url2': {'compliance_score': 85, 'compliance_level': 'AA'}
        },
        'screenshots': {
            'url1': 'test_ref.png',
            'url2': 'test_comp.png'
        }
    }
    
    config = {
        'layout_shift': True,
        'font_color': True,
        'element_detection': True,
        'ai_analysis': True,
        'wcag_analysis': True,
        'url1': 'https://example.com/ref',
        'url2': 'https://example.com/test'
    }
    
    # Test 1: Check what summary_dict gets generated
    print("\n📊 Step 1: Generate summary_dict...")
    regression = VisualAIRegression()
    summary_dict = regression._generate_summary_dict(analysis_results, config)
    
    print("summary_dict contents:")
    for key, value in summary_dict.items():
        print(f"  {key}: {value}")
    
    layout_diffs_in_summary = summary_dict.get('layout_differences', 'NOT FOUND')
    print(f"\nlayout_differences in summary_dict: {layout_diffs_in_summary}")
    
    # Test 2: Create the final_results structure as run_analysis would
    print("\n📦 Step 2: Create final_results structure...")
    final_results = {
        'analysis_results': analysis_results,
        'summary': regression._generate_summary(analysis_results, config),
        'summary_dict': summary_dict,
        'details': regression._generate_details(analysis_results),
        'reports': {}  # Will be filled by report generator
    }
    
    print("final_results keys:", list(final_results.keys()))
    print("analysis_results keys:", list(final_results['analysis_results'].keys()))
    print("summary_dict keys:", list(final_results['summary_dict'].keys()))
    
    # Test 3: Simulate what the GUI would see
    print("\n🖥️ Step 3: Simulate GUI data access...")
    gui_analysis_results = final_results.get('analysis_results', {})
    gui_summary_dict = final_results.get('summary_dict', {})
    
    # GUI checks for layout_differences in summary_dict
    gui_layout_diffs = gui_summary_dict.get('layout_differences', 0)
    print(f"GUI would see layout_differences: {gui_layout_diffs}")
    
    # GUI also checks layout_shifts in analysis_results for detailed display
    gui_layout_shifts = gui_analysis_results.get('layout_shifts', [])
    print(f"GUI would see layout_shifts count: {len(gui_layout_shifts)}")
    
    # Test 4: Simulate what the HTML report would get
    print("\n📄 Step 4: Generate HTML report...")
    
    # The HTML report gets the final_results with all the analysis data
    report_gen = ReportGenerator()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        html_path = os.path.join(temp_dir, 'data_flow_test.html')
        
        try:
            # This is what gets passed to the HTML generator
            html_input_data = {
                **analysis_results,  # All the raw analysis data
                'summary_dict': summary_dict  # The processed summary
            }
            
            print("HTML report input data keys:", list(html_input_data.keys()))
            print("summary_dict in HTML input:", 'summary_dict' in html_input_data)
            print("layout_differences in HTML summary_dict:", html_input_data['summary_dict'].get('layout_differences', 'NOT FOUND'))
            
            report_gen.generate_enhanced_html_report(html_input_data, config, html_path)
            
            # Read and check the HTML
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Find Layout Differences section
            import re
            layout_match = re.search(r'<h3>Layout Differences</h3>\s*<div class="number">(\d+)</div>', html_content)
            if layout_match:
                html_layout_value = layout_match.group(1)
                print(f"HTML report shows layout_differences: {html_layout_value}")
                
                if html_layout_value == str(gui_layout_diffs):
                    print("✅ GUI and HTML show the same value")
                else:
                    print(f"❌ MISMATCH: GUI shows {gui_layout_diffs}, HTML shows {html_layout_value}")
            else:
                print("❌ Could not find Layout Differences in HTML")
            
            # Save debug file
            debug_path = 'data_flow_debug.html'
            with open(debug_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"Debug HTML saved: {debug_path}")
            
        except Exception as e:
            print(f"Error generating HTML: {e}")
            import traceback
            traceback.print_exc()
    
    # Test 5: Check if there might be two different calculation paths
    print("\n🔍 Step 5: Check alternative calculation paths...")
    
    # Maybe the GUI is calculating layout differences differently?
    # Check if GUI might be reading from analysis_results directly
    gui_direct_count = len(gui_analysis_results.get('layout_shifts', []))
    print(f"Direct count from analysis_results['layout_shifts']: {gui_direct_count}")
    
    if gui_direct_count != gui_layout_diffs:
        print("⚠️ POTENTIAL ISSUE: GUI might be using direct count instead of summary_dict")
        print(f"  summary_dict['layout_differences']: {gui_layout_diffs}")
        print(f"  len(analysis_results['layout_shifts']): {gui_direct_count}")
    
    return {
        'gui_layout_diffs': gui_layout_diffs,
        'html_layout_diffs': html_layout_value if 'html_layout_value' in locals() else 'ERROR',
        'direct_count': gui_direct_count
    }

if __name__ == "__main__":
    debug_data_flow_mismatch()
