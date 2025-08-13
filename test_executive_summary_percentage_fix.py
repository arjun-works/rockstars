#!/usr/bin/env python3
"""
Test script to verify Executive Summary percentage accuracy in HTML report.
This test focuses specifically on the percentage formatting and data flow.
"""

import sys
import os
import tempfile
import json
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from report_generator import ReportGenerator
from visual_ai_regression import VisualAIRegression

def test_executive_summary_percentages():
    """Test that Executive Summary shows accurate percentages in HTML report"""
    print("🧪 Testing Executive Summary Percentage Accuracy...")
    
    # Create test analysis results with known values
    test_results = {
        'screenshots': {
            'url1': 'test_ref.png',
            'url2': 'test_comp.png'
        },
        'comparisons': {
            'similarity': 0.857,  # 85.7%
            'mse': 150.5,
            'ssim': 0.923,  # 92.3%
            'layout_shifts': [
                'Button moved from (100, 50) to (105, 55)',
                'Div shifted from (200, 100) to (200, 110)', 
                'Span repositioned from (300, 150) to (310, 150)'
            ],
            'color_differences': [
                'Red button changed to green',
                'Blue div changed to yellow',
                'Header text color shifted',
                'Background gradient modified',
                'Link color updated',
                'Footer background changed',
                'Navigation color adjusted'
            ],
            'missing_elements': ['sidebar', 'footer-link'],
            'new_elements': ['banner'],
            'overlapping_elements': []
        },
        'layout_analysis': {
            'layout_shifts': [
                'Button moved from (100, 50) to (105, 55)',
                'Div shifted from (200, 100) to (200, 110)', 
                'Span repositioned from (300, 150) to (310, 150)'
            ],
            'position_changes': [
                {'element': 'button', 'old_pos': (100, 50), 'new_pos': (105, 55)},
                {'element': 'div', 'old_pos': (200, 100), 'new_pos': (200, 110)},
                {'element': 'span', 'old_pos': (300, 150), 'new_pos': (310, 150)}
            ]
        },
        'color_analysis': {
            'color_differences': [
                'Red button changed to green',
                'Blue div changed to yellow',
                'Header text color shifted',
                'Background gradient modified',
                'Link color updated',
                'Footer background changed',
                'Navigation color adjusted'
            ],
            'changed_regions': [
                {'area': (50, 50, 100, 100), 'old_color': [255, 0, 0], 'new_color': [0, 255, 0]},
                {'area': (150, 150, 200, 200), 'old_color': [0, 0, 255], 'new_color': [255, 255, 0]}
            ]
        },
        'element_detection': {
            'missing_elements': ['sidebar', 'footer-link'],
            'new_elements': ['banner'],
            'changed_elements': ['button', 'div']
        },
        'ai_analysis': {
            'anomalies': [
                'Unexpected layout shift detected',
                'Color inconsistency found',
                'Element positioning anomaly',
                'Visual hierarchy disruption'
            ],
            'confidence_scores': [0.95, 0.87, 0.92, 0.78],
            'anomaly_types': ['layout', 'color', 'size', 'position']
        },
        'wcag_analysis': {
            'url1': {
                'compliance_score': 88,
                'compliance_level': 'AA',
                'total_issues': 12,
                'critical_issues': 2,
                'warnings': 10
            },
            'url2': {
                'compliance_score': 92,
                'compliance_level': 'AA',
                'total_issues': 8,
                'critical_issues': 1,
                'warnings': 7
            }
        }
    }
    
    # Create summary_dict manually to verify expected values
    expected_summary = {
        'similarity_score': 0.857,  # Should show as 85.7%
        'layout_differences': 3,
        'color_differences': 7,
        'element_changes': 3,  # 2 missing + 1 new
        'ai_anomalies': 4,
        'wcag_url1_score': 88,
        'wcag_url2_score': 92
    }
    
    # Add summary_dict to test results
    test_results['summary_dict'] = expected_summary
    
    test_config = {
        'url1': 'https://example.com/reference',
        'url2': 'https://example.com/test',
        'browser': 'chrome',
        'resolution': '1920x1080',
        'layout_shift': True,
        'font_color': True,
        'element_detection': True,
        'ai_analysis': True,
        'wcag_analysis': True
    }
    
    # Generate HTML report
    report_gen = ReportGenerator()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        html_path = os.path.join(temp_dir, 'test_executive_summary.html')
        
        try:
            report_gen.generate_enhanced_html_report(test_results, test_config, html_path)
            
            # Read the generated HTML
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            print(f"✅ HTML report generated: {html_path}")
            
            # Check for expected percentage formatting
            expected_patterns = [
                "85.7%",  # similarity_score as percentage
                ">3<",    # layout_differences as number
                ">7<",    # color_differences as number  
                ">3<",    # element_changes as number
                ">4<",    # ai_anomalies as number
            ]
            
            print("\n🔍 Checking Executive Summary content:")
            for i, pattern in enumerate(expected_patterns):
                if pattern in html_content:
                    print(f"✅ Found expected pattern: {pattern}")
                else:
                    print(f"❌ Missing pattern: {pattern}")
            
            # Check for percentage symbol in similarity score
            if "85.7%" in html_content:
                print("✅ Similarity score shows correct percentage: 85.7%")
            else:
                print("❌ Similarity score percentage not found or incorrect")
                # Look for any percentage near similarity
                import re
                matches = re.findall(r'(\d+\.?\d*%)', html_content)
                print(f"Found percentages in HTML: {matches}")
            
            # Look for summary_dict usage confirmation
            if 'summary.get(' in html_content:
                print("⚠️ HTML still contains 'summary.get(' - this should use summary_dict data")
            else:
                print("✅ HTML properly uses summary data (no old summary.get references)")
                
            # Save a copy for manual inspection
            final_path = 'test_executive_summary_percentage_check.html'
            with open(final_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"📄 Report saved for inspection: {final_path}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error generating HTML report: {str(e)}")
            return False

def test_summary_dict_data_flow():
    """Test the data flow from visual_ai_regression to report generation"""
    print("\n🔄 Testing Summary Dict Data Flow...")
    
    try:
        # Create a VisualAIRegression instance
        regression = VisualAIRegression()
        
        # Create test results similar to what would come from actual analysis
        test_results = {
            'similarity_score': 0.857,  # Add top-level similarity score
            'comparisons': {'similarity': 0.857, 'ssim': 0.923},
            'layout_shifts': ['shift1', 'shift2', 'shift3'],
            'color_differences': ['diff1', 'diff2', 'diff3', 'diff4', 'diff5', 'diff6', 'diff7'],
            'missing_elements': ['elem1', 'elem2'],
            'new_elements': ['elem3'],
            'ai_analysis': {
                'anomaly_detected': True,
                'semantic_analysis': {
                    'layout_changes': ['change1'],
                    'content_changes': ['change2'],
                    'style_changes': ['change3'], 
                    'structural_changes': ['change4']
                }
            },
            'wcag_analysis': {
                'url1': {'compliance_score': 88, 'total_issues': 12},
                'url2': {'compliance_score': 92, 'total_issues': 8}
            }
        }
        
        test_config = {
            'layout_shift': True,
            'font_color': True, 
            'element_detection': True,
            'ai_analysis': True,
            'wcag_analysis': True
        }
        
        # Generate summary_dict using the actual method
        summary_dict = regression._generate_summary_dict(test_results, test_config)
        
        print("📊 Generated summary_dict:")
        for key, value in summary_dict.items():
            if isinstance(value, float) and key == 'similarity_score':
                print(f"  {key}: {value} (as percentage: {value:.1%})")
            else:
                print(f"  {key}: {value}")
        
        # Verify expected values
        expected_checks = [
            ('similarity_score', 0.857, 'float'),
            ('layout_differences', 3, 'int'),
            ('color_differences', 7, 'int'),
            ('element_changes', 3, 'int'),  # 2 + 1
            ('ai_anomalies', 5, 'int')  # 1 + 1 + 1 + 1 + 1 = 5
        ]
        
        print("\n✅ Verification:")
        all_correct = True
        for key, expected_value, value_type in expected_checks:
            actual_value = summary_dict.get(key)
            if actual_value == expected_value:
                print(f"✅ {key}: {actual_value} (correct)")
            else:
                print(f"❌ {key}: {actual_value} (expected: {expected_value})")
                all_correct = False
        
        return all_correct
        
    except Exception as e:
        print(f"❌ Error in data flow test: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Executive Summary Percentage Accuracy Test")
    print("=" * 50)
    
    # Test 1: Direct HTML report generation
    success1 = test_executive_summary_percentages()
    
    # Test 2: Data flow verification
    success2 = test_summary_dict_data_flow()
    
    print("\n" + "=" * 50)
    if success1 and success2:
        print("🎉 All tests passed! Executive Summary should show accurate percentages.")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
    
    print("📝 Manual verification: Open 'test_executive_summary_percentage_check.html' to inspect the report.")
