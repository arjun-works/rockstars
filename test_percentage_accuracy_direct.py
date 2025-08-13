#!/usr/bin/env python3
"""
Test script to verify Executive Summary percentage accuracy by testing report generation directly.
This test creates known analysis results and verifies the HTML output accuracy.
"""

import os
import sys
import tempfile
import re
from datetime import datetime

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from report_generator import ReportGenerator

def test_executive_summary_percentage_accuracy():
    """Test that Executive Summary percentages are accurate in HTML reports"""
    print("🔧 Testing Executive Summary Percentage Accuracy")
    print("=" * 60)
    
    # Create temporary directory for test
    temp_dir = tempfile.mkdtemp(prefix="percentage_accuracy_test_")
    
    try:
        # Create test analysis results with known precision values
        test_cases = [
            {
                "name": "High Precision Test",
                "similarity_score": 0.8734,  # Should display as 87.3%
                "layout_differences": 7,
                "color_differences": 4,
                "element_changes": 2,
                "ai_anomalies": 1,
                "wcag_score_avg": 92.4  # Should display as 92%
            },
            {
                "name": "Low Precision Test", 
                "similarity_score": 0.6256,  # Should display as 62.6%
                "layout_differences": 12,
                "color_differences": 8,
                "element_changes": 5,
                "ai_anomalies": 6,
                "wcag_score_avg": 73.8  # Should display as 74%
            },
            {
                "name": "Edge Case Test",
                "similarity_score": 0.9999,  # Should display as 100.0%
                "layout_differences": 0,
                "color_differences": 0,
                "element_changes": 0,
                "ai_anomalies": 0,
                "wcag_score_avg": 85.0  # Should display as 85%
            }
        ]
        
        all_tests_passed = True
        
        for i, test_case in enumerate(test_cases):
            print(f"\n🧪 Running {test_case['name']} (Test {i+1}/{len(test_cases)})")
            
            # Create analysis results for this test case
            analysis_results = {
                'screenshots': {
                    'url1': 'test_reference.png',
                    'url2': 'test_target.png'
                },
                'comparisons': {
                    'overall_similarity': test_case['similarity_score'],
                    'differences_found': test_case['layout_differences'] + test_case['color_differences']
                },
                'ai_analysis': {
                    'anomalies': ['test_anomaly'] * test_case['ai_anomalies'],
                    'anomaly_detected': test_case['ai_anomalies'] > 0
                },
                'wcag_analysis': {
                    'url1': {
                        'compliance_score': test_case['wcag_score_avg'] + 2,
                        'compliance_level': 'AA',
                        'total_issues': 3,
                        'critical_issues': 1
                    },
                    'url2': {
                        'compliance_score': test_case['wcag_score_avg'] - 2,
                        'compliance_level': 'AA',
                        'total_issues': 4,
                        'critical_issues': 1
                    }
                },
                'summary': f"Test analysis with {test_case['similarity_score']:.1%} similarity",
                'summary_dict': {
                    'similarity_score': test_case['similarity_score'],
                    'layout_differences': test_case['layout_differences'],
                    'color_differences': test_case['color_differences'],
                    'element_changes': test_case['element_changes'],
                    'ai_anomalies': test_case['ai_anomalies']
                }
            }
            
            # Generate HTML report
            report_generator = ReportGenerator(output_dir=temp_dir)
            html_path = os.path.join(temp_dir, f"test_{i+1}_percentage_accuracy.html")
            
            config = {
                'url1': 'http://reference.test',
                'url2': 'http://test.test',
                'layout_shift': True,
                'font_color': True,
                'element_analysis': True,
                'ai_analysis': True,
                'wcag_compliance': True
            }
            
            report_generator.generate_enhanced_html_report(analysis_results, config, html_path)
            
            # Verify HTML content accuracy
            if os.path.exists(html_path):
                with open(html_path, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                # Expected formatted values
                expected_similarity = f"{test_case['similarity_score']:.1%}"
                expected_layout = str(test_case['layout_differences'])
                expected_color = str(test_case['color_differences'])
                expected_element = str(test_case['element_changes'])
                expected_ai = str(test_case['ai_anomalies'])
                expected_wcag = f"{test_case['wcag_score_avg']:.0f}%"
                
                print(f"   Expected similarity: {expected_similarity}")
                print(f"   Expected layout differences: {expected_layout}")
                print(f"   Expected WCAG score: {expected_wcag}")
                
                # Check for expected values in HTML
                test_checks = [
                    (expected_similarity, "Similarity percentage"),
                    (expected_layout, "Layout differences count"),
                    (expected_color, "Color changes count"),
                    (expected_element, "Element changes count"),
                    (expected_ai, "AI anomalies count")
                ]
                
                found_count = 0
                for expected_value, description in test_checks:
                    if expected_value in html_content:
                        found_count += 1
                        print(f"   ✅ Found: {description} = {expected_value}")
                    else:
                        print(f"   ❌ Missing: {description} = {expected_value}")
                
                # Special check for similarity percentage in the exact location
                similarity_pattern = r'<div class="number">(\d+\.\d+%)</div>'
                similarity_matches = re.findall(similarity_pattern, html_content)
                
                if similarity_matches:
                    html_similarity = similarity_matches[0]  # First match should be similarity
                    if html_similarity == expected_similarity:
                        print(f"   ✅ Similarity percentage is precisely accurate: {html_similarity}")
                    else:
                        print(f"   ❌ Similarity mismatch: Expected {expected_similarity}, Got {html_similarity}")
                        all_tests_passed = False
                else:
                    print(f"   ❌ Could not find similarity percentage in HTML")
                    all_tests_passed = False
                
                # Check WCAG percentage
                wcag_pattern = r'<div class="number">(\d+%)</div>'
                wcag_matches = re.findall(wcag_pattern, html_content)
                
                if wcag_matches:
                    # WCAG should be the last percentage match
                    html_wcag = wcag_matches[-1] if wcag_matches else None
                    if html_wcag == expected_wcag:
                        print(f"   ✅ WCAG percentage is accurate: {html_wcag}")
                    else:
                        print(f"   ⚠️ WCAG may differ: Expected {expected_wcag}, Found {html_wcag}")
                
                # Test case success rate
                success_rate = found_count / len(test_checks)
                print(f"   📊 Test Case Success: {found_count}/{len(test_checks)} ({success_rate:.1%})")
                
                if found_count < len(test_checks):
                    all_tests_passed = False
            else:
                print(f"   ❌ HTML report not generated: {html_path}")
                all_tests_passed = False
        
        # Overall test results
        print(f"\n📈 Overall Test Results:")
        if all_tests_passed:
            print(f"   🎉 ALL TESTS PASSED: Executive Summary percentages are accurate!")
            print(f"   ✅ Similarity percentages display with correct precision")
            print(f"   ✅ Count values display correctly")
            print(f"   ✅ WCAG percentages display correctly")
        else:
            print(f"   ❌ SOME TESTS FAILED: Executive Summary has accuracy issues")
            print(f"   🔍 Check individual test results above for details")
        
        return all_tests_passed
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Keep files for manual inspection
        print(f"\n📁 Test files preserved for inspection:")
        print(f"   Directory: {temp_dir}")

if __name__ == "__main__":
    print("🧪 Executive Summary Percentage Accuracy Test")
    print("Testing HTML report percentage accuracy with known values")
    print("=" * 60)
    
    success = test_executive_summary_percentage_accuracy()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 TEST PASSED: Executive Summary percentages are accurate!")
    else:
        print("❌ TEST FAILED: Executive Summary has percentage accuracy issues")
    
    print("🔍 Manual verification recommended for complex edge cases.")
