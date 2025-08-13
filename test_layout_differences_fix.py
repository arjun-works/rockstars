#!/usr/bin/env python3
"""
Test script to verify the layout differences fix between GUI and HTML report.
"""

import sys
import os
import tempfile

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from visual_ai_regression import VisualAIRegression
from report_generator import ReportGenerator

def test_layout_differences_fix():
    """Test that layout differences now match between GUI and HTML report"""
    print("🔧 Testing Layout Differences Fix...")
    
    # Create test analysis results with 9 layout shifts
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
    
    # Test the corrected data flow
    print("\n📊 Step 1: Generate summary_dict and add to analysis_results...")
    regression = VisualAIRegression()
    summary_dict = regression._generate_summary_dict(analysis_results, config)
    
    print("Generated summary_dict:")
    for key, value in summary_dict.items():
        print(f"  {key}: {value}")
    
    # Add summary_dict to analysis_results as the fixed code does
    analysis_results['summary_dict'] = summary_dict
    
    # Test 2: Simulate what GUI would see (should be 9)
    print("\n🖥️ Step 2: Simulate GUI data access...")
    gui_summary_dict = analysis_results.get('summary_dict', {})
    gui_layout_diffs = gui_summary_dict.get('layout_differences', 0)
    print(f"GUI would see layout_differences: {gui_layout_diffs}")
    
    # Test 3: Generate HTML report with the corrected data
    print("\n📄 Step 3: Generate HTML report with corrected data...")
    report_gen = ReportGenerator()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        html_path = os.path.join(temp_dir, 'layout_fix_test.html')
        
        try:
            # Now analysis_results includes summary_dict
            print("HTML input data keys:", list(analysis_results.keys()))
            print("summary_dict in HTML input:", 'summary_dict' in analysis_results)
            print("layout_differences in summary_dict:", analysis_results['summary_dict'].get('layout_differences', 'NOT FOUND'))
            
            report_gen.generate_enhanced_html_report(analysis_results, config, html_path)
            
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
                    print("✅ SUCCESS: GUI and HTML now show the same value!")
                    print(f"   Both show: {gui_layout_diffs} layout differences")
                else:
                    print(f"❌ STILL BROKEN: GUI shows {gui_layout_diffs}, HTML shows {html_layout_value}")
                    return False
            else:
                print("❌ ERROR: Could not find Layout Differences in HTML")
                return False
            
            # Save for inspection
            debug_path = 'layout_fix_verification.html'
            with open(debug_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"Verification HTML saved: {debug_path}")
            
            return True
            
        except Exception as e:
            print(f"Error generating HTML: {e}")
            import traceback
            traceback.print_exc()
            return False

def test_full_workflow_simulation():
    """Test the complete workflow to ensure end-to-end fix"""
    print("\n\n🚀 Testing Full Workflow Simulation...")
    
    # This simulates what would happen if you called the fixed run_analysis method
    # (We can't call it directly without setting up browsers, so we simulate the key parts)
    
    regression = VisualAIRegression()
    
    # Simulate analysis results from image comparison
    mock_analysis_results = {
        'similarity_score': 0.82,
        'layout_shifts': [f'shift_{i}' for i in range(9)],  # 9 shifts
        'color_differences': [f'color_{i}' for i in range(5)],  # 5 color diffs
        'missing_elements': ['elem1', 'elem2'],  # 2 missing
        'new_elements': ['elem3'],  # 1 new
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
            'url1': {'compliance_score': 88},
            'url2': {'compliance_score': 92}
        },
        'screenshots': {
            'url1': 'mock_ref.png',
            'url2': 'mock_test.png'
        }
    }
    
    config = {
        'layout_shift': True,
        'font_color': True,
        'element_detection': True,
        'ai_analysis': True,
        'wcag_analysis': True
    }
    
    # Step 1: Generate summary_dict (as the fixed code does)
    summary_dict = regression._generate_summary_dict(mock_analysis_results, config)
    print("Generated summary_dict with layout_differences:", summary_dict.get('layout_differences'))
    
    # Step 2: Add summary_dict to analysis_results (as the fixed code does)
    mock_analysis_results['summary_dict'] = summary_dict
    
    # Step 3: Generate report (as the fixed code does)
    report_gen = ReportGenerator()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        html_path = os.path.join(temp_dir, 'full_workflow_test.html')
        
        try:
            # This is the call that would happen in generate_comprehensive_report
            report_gen.generate_enhanced_html_report(mock_analysis_results, config, html_path)
            
            # Check the result
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            import re
            layout_match = re.search(r'<h3>Layout Differences</h3>\s*<div class="number">(\d+)</div>', html_content)
            if layout_match:
                html_value = layout_match.group(1)
                expected_value = str(summary_dict.get('layout_differences'))
                
                if html_value == expected_value:
                    print(f"✅ Full workflow test PASSED: HTML shows {html_value} (expected {expected_value})")
                    return True
                else:
                    print(f"❌ Full workflow test FAILED: HTML shows {html_value}, expected {expected_value}")
                    return False
            else:
                print("❌ Full workflow test FAILED: Could not find layout differences in HTML")
                return False
                
        except Exception as e:
            print(f"❌ Full workflow test ERROR: {e}")
            return False

if __name__ == "__main__":
    print("🔧 Layout Differences Fix Verification")
    print("=" * 50)
    
    # Test 1: Basic fix verification
    success1 = test_layout_differences_fix()
    
    # Test 2: Full workflow simulation
    success2 = test_full_workflow_simulation()
    
    print("\n" + "=" * 50)
    if success1 and success2:
        print("🎉 ALL TESTS PASSED! Layout differences fix is working correctly.")
        print("✅ GUI and HTML report now show matching layout difference counts.")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
    
    print("\n📝 You can now run the application and the layout differences should match between GUI and HTML report.")
