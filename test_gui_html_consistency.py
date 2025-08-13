#!/usr/bin/env python3
"""
Test script to verify that HTML report shows the same summary percentages and values as GUI.
This test ensures consistency between GUI display and HTML report Executive Summary.
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

def test_gui_html_summary_consistency():
    """Test that HTML report shows the same summary values as GUI would display"""
    print("🔧 Testing GUI vs HTML Summary Consistency")
    print("=" * 60)
    
    # Create temporary directory for test
    temp_dir = tempfile.mkdtemp(prefix="gui_html_consistency_test_")
    
    try:
        # Create test screenshots
        url1_screenshot = os.path.join(temp_dir, "reference.png")
        url2_screenshot = os.path.join(temp_dir, "test.png")
        
        create_test_screenshot(url1_screenshot, "REFERENCE PAGE", 'lightblue', 'darkblue')
        create_test_screenshot(url2_screenshot, "TEST PAGE", 'lightgreen', 'darkgreen')
        
        print(f"✅ Created test screenshots")
        
        # Create test analysis results that match what both GUI and HTML should display
        analysis_results = {
            'screenshots': {
                'url1': url1_screenshot,
                'url2': url2_screenshot
            },
            'comparisons': {
                'overall_similarity': 0.87,
                'differences_found': 18,
                'layout_shifts': [
                    {'element': 'header', 'distance': 5.2},
                    {'element': 'sidebar', 'distance': 3.1},
                    {'element': 'footer', 'distance': 2.8}
                ],
                'color_differences': [
                    {'element': 'background', 'old_color': '#f0f0f0', 'new_color': '#e0e0e0'},
                    {'element': 'button', 'old_color': '#0066cc', 'new_color': '#0055bb'},
                    {'element': 'text', 'old_color': '#333333', 'new_color': '#444444'}
                ],
                'missing_elements': [
                    {'element': 'nav-item', 'xpath': '/html/body/nav/ul/li[3]'}
                ],
                'new_elements': [
                    {'element': 'banner', 'xpath': '/html/body/header/div[2]'},
                    {'element': 'icon', 'xpath': '/html/body/footer/span'}
                ]
            },
            'ai_analysis': {
                'anomalies': [
                    {'type': 'layout', 'confidence': 0.9, 'description': 'Header position shift detected'},
                    {'type': 'color', 'confidence': 0.8, 'description': 'Background color change detected'},
                    {'type': 'content', 'confidence': 0.7, 'description': 'Text content modified'},
                    {'type': 'element', 'confidence': 0.85, 'description': 'New navigation element added'},
                    {'type': 'structural', 'confidence': 0.75, 'description': 'Footer structure changed'}
                ],
                'anomaly_detected': True,
                'semantic_analysis': {
                    'layout_changes': ['header_shift', 'footer_change'],
                    'content_changes': ['text_update'],
                    'style_changes': ['color_change', 'font_change'],
                    'structural_changes': ['nav_element']
                }
            },
            'wcag_analysis': {
                'url1': {
                    'compliance_score': 88.5,
                    'compliance_level': 'AA',
                    'total_issues': 5,
                    'critical_issues': 1
                },
                'url2': {
                    'compliance_score': 84.7,
                    'compliance_level': 'AA',
                    'total_issues': 7,
                    'critical_issues': 2
                }
            },
            'summary': "Analysis completed with 87% similarity. Found 3 layout shifts, 3 color differences, and 5 AI anomalies.",
            'summary_dict': {
                'similarity_score': 0.87,  # Should show as 87.0%
                'layout_differences': 3,    # Should show as 3
                'color_differences': 3,     # Should show as 3
                'missing_elements': 1,      # Part of element_changes
                'new_elements': 2,          # Part of element_changes
                'element_changes': 3,       # Should show as 3 (1 + 2)
                'ai_anomalies': 5,          # Should show as 5
                'wcag_url1_score': 88.5,
                'wcag_url2_score': 84.7,
                'wcag_url1_level': 'AA',
                'wcag_url2_level': 'AA',
                'wcag_url1_issues': 5,
                'wcag_url2_issues': 7
            }
        }
        
        print(f"✅ Created test analysis data with summary_dict:")
        print(f"   📊 Similarity Score: {analysis_results['summary_dict']['similarity_score']:.1%}")
        print(f"   📐 Layout Differences: {analysis_results['summary_dict']['layout_differences']}")
        print(f"   🎨 Color Differences: {analysis_results['summary_dict']['color_differences']}")
        print(f"   🔄 Element Changes: {analysis_results['summary_dict']['element_changes']}")
        print(f"   🤖 AI Anomalies: {analysis_results['summary_dict']['ai_anomalies']}")
        print(f"   ♿ WCAG Score Average: {(analysis_results['summary_dict']['wcag_url1_score'] + analysis_results['summary_dict']['wcag_url2_score']) / 2:.1f}%")
        
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
        
        # Generate HTML report
        html_path = os.path.join(temp_dir, "gui_html_consistency_test.html")
        report_generator.generate_enhanced_html_report(analysis_results, config, html_path)
        
        print(f"✅ HTML report generated: {html_path}")
        
        # Define expected values that should match between GUI and HTML
        print("\n🔍 Verifying HTML report contains GUI-equivalent values...")
        
        if os.path.exists(html_path):
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Expected values that GUI shows and HTML should also show
            expected_gui_values = [
                ('87.0%', 'Overall Similarity percentage (GUI shows as 87.0%)'),
                ('3', 'Layout Differences count'),
                ('3', 'Color Changes count'),
                ('3', 'Element Changes count (missing + new = 1 + 2)'),
                ('5', 'AI Anomalies count (from summary_dict.ai_anomalies)'),
                ('87%', 'WCAG Compliance rounded percentage'),
                ('status-warning', 'Similarity status class (87% = WARNING)'),
                ('WARNING', 'Similarity status text'),
                ('WARNING', 'Layout differences status (3 differences = WARNING)'),
                ('WARNING', 'Color changes status (3 changes = WARNING)'),
                ('WARNING', 'Element changes status (3 changes = WARNING)'),
                ('FAIL', 'AI anomalies status (5 anomalies = FAIL)')
            ]
            
            found_values = []
            missing_values = []
            
            for expected_value, description in expected_gui_values:
                if expected_value in html_content:
                    found_values.append((expected_value, description))
                    print(f"   ✅ Found: {expected_value} ({description})")
                else:
                    missing_values.append((expected_value, description))
                    print(f"   ❌ Missing: {expected_value} ({description})")
            
            # Check for Executive Summary section structure
            structure_checks = [
                ("📊 Executive Summary", "Executive Summary section header"),
                ("Overall Similarity", "Similarity card"),
                ("Layout Differences", "Layout card"),
                ("Color Changes", "Color card"),
                ("Element Changes", "Element changes card"),
                ("AI Anomalies", "AI anomalies card"),
                ("WCAG Compliance", "WCAG card"),
                ("summary-cards", "Summary cards container")
            ]
            
            structure_found = []
            structure_missing = []
            
            for check_text, description in structure_checks:
                if check_text in html_content:
                    structure_found.append((check_text, description))
                    print(f"   ✅ Structure: {description}")
                else:
                    structure_missing.append((check_text, description))
                    print(f"   ❌ Missing Structure: {description}")
            
            # Calculate success rates
            values_success_rate = len(found_values) / len(expected_gui_values)
            structure_success_rate = len(structure_found) / len(structure_checks)
            overall_success_rate = (len(found_values) + len(structure_found)) / (len(expected_gui_values) + len(structure_checks))
            
            print(f"\n📈 Test Results:")
            print(f"   🎯 Values Found: {len(found_values)}/{len(expected_gui_values)} ({values_success_rate:.1%})")
            print(f"   🏗️ Structure Found: {len(structure_found)}/{len(structure_checks)} ({structure_success_rate:.1%})")
            print(f"   📊 Overall Success: {overall_success_rate:.1%}")
            print(f"   📋 HTML Report Size: {len(html_content):,} characters")
            
            if len(missing_values) == 0 and len(structure_missing) == 0:
                print(f"\n🎉 SUCCESS: HTML report shows same summary values as GUI!")
                print(f"   Perfect consistency between GUI display and HTML report.")
                return True
            else:
                print(f"\n⚠️ ISSUES FOUND:")
                if missing_values:
                    print(f"   📊 Missing Values:")
                    for value, desc in missing_values:
                        print(f"     ❌ {value} ({desc})")
                if structure_missing:
                    print(f"   🏗️ Missing Structure:")
                    for check, desc in structure_missing:
                        print(f"     ❌ {desc}")
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
    print("🧪 GUI vs HTML Summary Consistency Test")
    print("Testing that HTML report shows same summary percentages as GUI")
    print("=" * 60)
    
    success = test_gui_html_summary_consistency()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 TEST PASSED: GUI and HTML summary values are consistent!")
    else:
        print("❌ TEST FAILED: HTML report doesn't match GUI summary display")
    
    print("🔍 Check the generated HTML file manually to verify Executive Summary matches GUI.")
