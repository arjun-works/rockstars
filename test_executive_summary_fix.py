#!/usr/bin/env python3
"""
Test script to verify that the Executive Summary in HTML reports shows correct values.
This test ensures the fix for using summary_dict instead of summary in the HTML report.
"""

import os
import sys
import tempfile
import shutil
from datetime import datetime
from PIL import Image, ImageDraw

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from report_generator import ReportGenerator

def create_test_screenshot(filename, text, color='white', text_color='black'):
    """Create a test screenshot with specific text and background"""
    img = Image.new('RGB', (800, 600), color)
    draw = ImageDraw.Draw(img)
    
    # Draw text in the center
    text_width = len(text) * 10
    text_height = 20
    x = (800 - text_width) // 2
    y = (600 - text_height) // 2
    
    draw.text((x, y), text, fill=text_color)
    
    # Add a border to make it visually distinct
    draw.rectangle([10, 10, 790, 590], outline=text_color, width=3)
    
    img.save(filename, 'PNG')
    return filename

def test_executive_summary_fix():
    """Test that Executive Summary shows correct values from summary_dict"""
    print("🔧 Testing Executive Summary Fix")
    print("=" * 60)
    
    # Create temporary directory for test
    temp_dir = tempfile.mkdtemp(prefix="executive_summary_test_")
    
    try:
        # Create test screenshots
        url1_screenshot = os.path.join(temp_dir, "reference.png")
        url2_screenshot = os.path.join(temp_dir, "test.png")
        
        create_test_screenshot(url1_screenshot, "REFERENCE PAGE", 'lightblue', 'darkblue')
        create_test_screenshot(url2_screenshot, "TEST PAGE", 'lightgreen', 'darkgreen')
        
        print(f"✅ Created test screenshots")
        
        # Create comprehensive test analysis results with summary_dict
        analysis_results = {
            'screenshots': {
                'url1': url1_screenshot,
                'url2': url2_screenshot
            },
            'comparisons': {
                'overall_similarity': 0.85,
                'differences_found': 15,
                'layout_shifts': [
                    {'element': 'header', 'distance': 5.2},
                    {'element': 'sidebar', 'distance': 3.1}
                ],
                'color_differences': [
                    {'element': 'background', 'old_color': '#f0f0f0', 'new_color': '#e0e0e0'},
                    {'element': 'button', 'old_color': '#0066cc', 'new_color': '#0055bb'}
                ]
            },
            'ai_analysis': {
                'anomalies': [
                    {'type': 'layout', 'confidence': 0.9, 'description': 'Header position shift detected'},
                    {'type': 'color', 'confidence': 0.8, 'description': 'Background color change detected'},
                    {'type': 'content', 'confidence': 0.7, 'description': 'Text content modified'}
                ],
                'anomaly_detected': True,
                'semantic_analysis': {
                    'layout_changes': ['header_shift'],
                    'content_changes': ['text_update'],
                    'style_changes': ['color_change'],
                    'structural_changes': []
                }
            },
            'wcag_analysis': {
                'url1': {
                    'compliance_score': 82.5,
                    'compliance_level': 'AA',
                    'total_issues': 8,
                    'critical_issues': 2
                },
                'url2': {
                    'compliance_score': 78.3,
                    'compliance_level': 'A',
                    'total_issues': 12,
                    'critical_issues': 3
                }
            },
            'summary': "Analysis completed with 85% similarity. Found 2 layout shifts and 2 color differences.",
            'summary_dict': {
                'similarity_score': 0.85,
                'layout_differences': 2,
                'color_differences': 2,
                'missing_elements': 1,
                'new_elements': 0,
                'element_changes': 1,
                'ai_anomalies': 4,
                'wcag_url1_score': 82.5,
                'wcag_url2_score': 78.3,
                'wcag_url1_level': 'AA',
                'wcag_url2_level': 'A',
                'wcag_url1_issues': 8,
                'wcag_url2_issues': 12
            }
        }
        
        print(f"✅ Created test analysis data with summary_dict containing:")
        print(f"   📊 Similarity Score: {analysis_results['summary_dict']['similarity_score']:.1%}")
        print(f"   📐 Layout Differences: {analysis_results['summary_dict']['layout_differences']}")
        print(f"   🎨 Color Differences: {analysis_results['summary_dict']['color_differences']}")
        print(f"   🤖 AI Anomalies: {analysis_results['summary_dict']['ai_anomalies']}")
        print(f"   ♿ WCAG URL1 Score: {analysis_results['summary_dict']['wcag_url1_score']:.1f}%")
        
        # Initialize report generator
        report_generator = ReportGenerator(output_dir=temp_dir)
        
        # Test configuration
        config = {
            'url1': 'http://reference.example.com',
            'url2': 'http://test.example.com',
            'layout_shift': True,
            'font_color': True,
            'element_analysis': True,
            'ai_analysis': True,
            'wcag_compliance': True
        }
        
        print("\n🔄 Generating HTML report...")
        
        # Generate HTML report directly
        html_path = os.path.join(temp_dir, "test_executive_summary.html")
        report_generator.generate_enhanced_html_report(analysis_results, config, html_path)
        
        print(f"✅ HTML report generated: {html_path}")
        
        # Verify HTML content contains correct values from summary_dict
        print("\n🔍 Verifying Executive Summary content...")
        
        if os.path.exists(html_path):
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Check for expected values from summary_dict
            expected_values = [
                ('85.0%', 'Overall Similarity percentage'),
                ('2', 'Layout Differences count'),
                ('2', 'Color Changes count'),
                ('4', 'AI Anomalies count'),
                ('80%', 'WCAG Compliance score (average of 82.5 and 78.3)'),
                ('status-warning', 'Similarity status class'),
                ('WARNING', 'Similarity status text'),
                ('WARNING', 'Layout differences status (2 differences = WARNING)'),
                ('WARNING', 'Color changes status'),
                ('FAIL', 'AI anomalies status')
            ]
            
            found_values = []
            missing_values = []
            
            for expected_value, description in expected_values:
                if expected_value in html_content:
                    found_values.append((expected_value, description))
                    print(f"   ✅ Found: {expected_value} ({description})")
                else:
                    missing_values.append((expected_value, description))
                    print(f"   ❌ Missing: {expected_value} ({description})")
            
            # Check for Executive Summary section
            if "📊 Executive Summary" in html_content:
                print(f"   ✅ Executive Summary section found")
            else:
                print(f"   ❌ Executive Summary section missing")
            
            # Check for summary cards structure
            if "summary-cards" in html_content:
                print(f"   ✅ Summary cards structure found")
            else:
                print(f"   ❌ Summary cards structure missing")
            
            # Test results
            success_rate = len(found_values) / len(expected_values)
            print(f"\n📈 Test Results:")
            print(f"   🎯 Values Found: {len(found_values)}/{len(expected_values)} ({success_rate:.1%})")
            print(f"   📋 HTML Report Size: {len(html_content):,} characters")
            
            if len(missing_values) == 0:
                print(f"\n🎉 SUCCESS: Executive Summary fix is working correctly!")
                print(f"   All expected values from summary_dict are present in the HTML report.")
                return True
            else:
                print(f"\n⚠️ PARTIAL SUCCESS: {len(missing_values)} values still missing:")
                for value, desc in missing_values:
                    print(f"     ❌ {value} ({desc})")
                return False
        else:
            print(f"❌ HTML report file not found: {html_path}")
            return False
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Keep files for manual inspection
        print(f"\n📁 Test files preserved for inspection:")
        print(f"   Directory: {temp_dir}")
        if 'html_path' in locals():
            print(f"   HTML Report: {html_path}")

if __name__ == "__main__":
    print("🧪 Executive Summary Fix Test")
    print("Testing that HTML report shows correct values from summary_dict")
    print("=" * 60)
    
    success = test_executive_summary_fix()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 TEST PASSED: Executive Summary fix is working correctly!")
    else:
        print("❌ TEST FAILED: Executive Summary still showing incorrect values")
    
    print("🔍 Check the generated HTML file manually to verify the Executive Summary section.")
