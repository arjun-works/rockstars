#!/usr/bin/env python3
"""
Test Fixed Analysis Results Display
This script tests that the analysis results are now properly displayed
"""

import tkinter as tk
from main import VisualRegressionGUI

def test_display_results():
    """Test the display results with sample data"""
    print("=" * 60)
    print("Testing Fixed Display Results")
    print("=" * 60)
    
    # Create a temporary GUI instance
    root = tk.Tk()
    root.withdraw()  # Hide the window
    
    try:
        gui = VisualRegressionGUI(root)
        
        # Create sample results in the correct structure
        sample_results = {
            'analysis_results': {
                'similarity_score': 0.803,
                'layout_shifts': [
                    {
                        'original_position': (813, 152, 18, 16),
                        'new_position': (840, 184, 31, 9),
                        'distance': 43.278170016764804,
                        'shift_x': 27,
                        'shift_y': 32
                    },
                    {
                        'original_position': (833, 151, 26, 17),
                        'new_position': (840, 184, 31, 9),
                        'distance': 30.364452901377952,
                        'shift_x': 7,
                        'shift_y': 33
                    }
                ],
                'color_differences': [
                    {
                        'position': (647, 144, 282, 33),
                        'color1': [186.01, 186.01, 187.45],
                        'color2': [211.12, 211.04, 211.12],
                        'color_distance': 42.63,
                        'area': 5170.5
                    },
                    {
                        'position': (986, 203, 184, 43),
                        'color1': [223.70, 223.81, 225.60],
                        'color2': [205.18, 205.36, 205.24],
                        'color_distance': 33.14,
                        'area': 3106.5
                    }
                ],
                'missing_elements': [
                    {'position': (133, 309, 77, 13), 'area': 583.5},
                    {'position': (55, 307, 74, 15), 'area': 556.0}
                ],
                'new_elements': [],
                'overlapping_elements': [
                    {'point1': (1036.8, 228.0), 'point2': (448.0, 131.0), 'distance': 596.7, 'match_quality': 12.0}
                ],
                'ai_analysis': {
                    'anomaly_detected': False,
                    'feature_distance': 22.6274,
                    'confidence': 0.92,
                    'semantic_analysis': {
                        'layout_changes': 77,
                        'content_changes': 6,
                        'style_changes': 84,
                        'structural_changes': 38
                    }
                },
                'wcag_analysis': {
                    'url1': {'compliance_score': 92.5, 'compliance_level': 'AA'},
                    'url2': {'compliance_score': 90.0, 'compliance_level': 'AA'},
                    'comparison': {'assessment': 'Both sites meet AA standards'}
                }
            },
            'summary': "Overall structural similarity: 80.3%\\n✗ Images have significant differences\\n⚠ 4 layout shifts detected\\n⚠ 583 color differences detected\\n⚠ 472 missing, 0 new elements detected\\n🤖 AI analysis: No anomalies detected\\n♿ WCAG Compliance: URL 1 - AA (92.5%), URL 2 - AA (90.0%)",
            'summary_dict': {
                'similarity_score': 0.803,
                'layout_differences': 4,
                'color_differences': 583,
                'missing_elements': 472,
                'new_elements': 0,
                'ai_anomalies': 0
            },
            'reports': {
                'html': 'reports/test_report.html',
                'pdf': 'reports/test_report.pdf',
                'json': 'reports/test_report.json'
            }
        }
        
        print("Testing display_results with sample data...")
        
        # Test the display method
        gui.display_results(sample_results)
        
        # Get the displayed text
        displayed_text = gui.results_text.get(1.0, tk.END)
        
        print("\\nDisplayed Results:")
        print("-" * 40)
        print(displayed_text)
        print("-" * 40)
        
        # Check if key elements are present
        checks = [
            ("Analysis completed", "🎉 ANALYSIS COMPLETED" in displayed_text),
            ("Summary section", "📊 SUMMARY" in displayed_text),
            ("Detailed results", "📋 DETAILED RESULTS" in displayed_text),
            ("Layout shifts", "🔄 Layout Shifts" in displayed_text),
            ("Color changes", "🎨 Color Changes" in displayed_text),
            ("Element changes", "🔍 Element Changes" in displayed_text),
            ("AI analysis", "🤖 AI Analysis" in displayed_text),
            ("WCAG summary", "♿ ACCESSIBILITY SUMMARY" in displayed_text),
            ("Generated reports", "📁 GENERATED REPORTS" in displayed_text)
        ]
        
        print("\\nValidation Results:")
        all_passed = True
        for check_name, result in checks:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"  {status}: {check_name}")
            if not result:
                all_passed = False
        
        print(f"\\nOverall Test Result: {'✅ ALL CHECKS PASSED' if all_passed else '❌ SOME CHECKS FAILED'}")
        
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        root.destroy()
    
    print("\\n" + "=" * 60)
    print("Test Completed")
    print("=" * 60)

if __name__ == "__main__":
    test_display_results()
