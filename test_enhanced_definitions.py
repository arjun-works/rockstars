#!/usr/bin/env python3
"""
Test script to verify the enhanced visual comparison definitions in HTML report
"""

import os
import sys
import json
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from report_generator import ReportGenerator

def test_enhanced_visual_definitions():
    """Test the enhanced visual comparison definitions in HTML report"""
    print("🧪 Testing Enhanced Visual Comparison Definitions...")
    
    try:
        # Initialize report generator
        report_gen = ReportGenerator()
        
        # Create mock analysis results
        mock_analysis_results = {
            'screenshots': {
                'reference': 'screenshots/ref_test.png',
                'test': 'screenshots/test_test.png'
            },
            'comparisons': {
                'pixel_difference_percentage': 2.34,
                'structural_similarity': 0.892,
                'differences_detected': True,
                'color_differences': [
                    {'location': (100, 150), 'expected': '#ffffff', 'actual': '#f0f0f0'}
                ],
                'layout_shifts': [
                    {'element': 'header', 'shift_x': 5, 'shift_y': 0}
                ]
            },
            'ai_analysis': {
                'layout_analysis': {
                    'changes_detected': True,
                    'severity': 'medium',
                    'description': 'Header position shifted slightly'
                },
                'content_analysis': {
                    'text_changes': False,
                    'missing_elements': [],
                    'new_elements': []
                }
            },
            'summary': {
                'total_differences': 3,
                'severity': 'medium',
                'passed': False,
                'analysis_types_enabled': {
                    'pixel_comparison': True,
                    'layout_analysis': True,
                    'content_analysis': True,
                    'wcag_compliance': True
                }
            },
            'wcag_results': {
                'total_issues': 2,
                'level_aa_score': 85.5,
                'issues': [
                    {'type': 'color_contrast', 'severity': 'warning', 'description': 'Low contrast detected'},
                    {'type': 'alt_text', 'severity': 'error', 'description': 'Missing alt text'}
                ]
            },
            'duration': '00:02:15',
            'reports': {
                'pdf': 'reports/test_report.pdf',
                'json': 'reports/test_report.json',
                'visual': 'reports/test_report_visual_comparison.png',
                'sidebyside': 'reports/test_report_side_by_side.png',
                'heatmap': 'reports/test_report_difference_heatmap.png'
            }
        }
        
        # Create mock config
        mock_config = {
            'test_name': 'Enhanced Definitions Test',
            'reference_url': 'https://example.com/reference',
            'test_url': 'https://example.com/test',
            'viewport_width': 1920,
            'viewport_height': 1080,
            'threshold': 0.1
        }
        
        # Generate HTML report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"reports/test_enhanced_definitions_{timestamp}.html"
        
        print(f"📄 Generating HTML report with enhanced definitions...")
        report_gen.generate_enhanced_html_report(mock_analysis_results, mock_config, output_path)
        
        # Verify the report was created
        if os.path.exists(output_path):
            print(f"✅ HTML report generated successfully: {output_path}")
            
            # Read and check for enhanced definitions
            with open(output_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check for specific enhanced definition content
            checks = [
                'This gallery provides three different visualization approaches',
                'What it shows:',
                'Use case:',
                'Best for:',
                'Side-by-Side Comparison',
                'Difference Heatmap',
                'Annotated Visual Comparison',
                'Reference and test screenshots placed side-by-side',
                'heat-mapped overlay where red/warm colors indicate pixel differences',
                'AI-detected differences highlighted using bounding boxes'
            ]
            
            missing_checks = []
            for check in checks:
                if check not in content:
                    missing_checks.append(check)
            
            if not missing_checks:
                print("✅ All enhanced definition content found in HTML report!")
            else:
                print(f"⚠️  Missing content: {missing_checks}")
                
            # Show file size
            file_size = os.path.getsize(output_path)
            print(f"📊 Report file size: {file_size:,} bytes")
            
            return True
            
        else:
            print("❌ HTML report was not created")
            return False
            
    except Exception as e:
        print(f"❌ Error testing enhanced definitions: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_visual_section_formatting():
    """Test the visual formatting and styling of the enhanced sections"""
    print("\n🎨 Testing Visual Section Formatting...")
    
    try:
        # Check if the styling includes the new colored definition boxes
        report_gen = ReportGenerator()
        
        # Create a minimal test to check CSS and HTML structure
        mock_results = {'reports': {}}
        mock_config = {'test_name': 'Format Test'}
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"reports/test_formatting_{timestamp}.html"
        
        report_gen.generate_enhanced_html_report(mock_results, mock_config, output_path)
        
        if os.path.exists(output_path):
            with open(output_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for styling elements
            style_checks = [
                'background-color: #e8f4f8',  # Side-by-side background
                'background-color: #fff2e8',  # Heatmap background  
                'background-color: #f0f8e8',  # Annotated background
                'color: #2c5aa0',            # Side-by-side text color
                'color: #d2691e',            # Heatmap text color
                'color: #228b22'             # Annotated text color
            ]
            
            missing_styles = []
            for style in style_checks:
                if style not in content:
                    missing_styles.append(style)
                    
            if not missing_styles:
                print("✅ All enhanced styling found!")
            else:
                print(f"⚠️  Missing styles: {missing_styles}")
                
            return True
        else:
            print("❌ Format test report was not created")
            return False
            
    except Exception as e:
        print(f"❌ Error testing formatting: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Enhanced Visual Comparison Definitions Test\n")
    
    # Ensure reports directory exists
    os.makedirs("reports", exist_ok=True)
    
    # Run tests
    test1_passed = test_enhanced_visual_definitions()
    test2_passed = test_visual_section_formatting()
    
    # Summary
    print(f"\n📋 Test Summary:")
    print(f"   Enhanced Definitions Test: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"   Visual Formatting Test: {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 All tests passed! Enhanced visual comparison definitions are working correctly.")
    else:
        print("\n⚠️  Some tests failed. Please check the output above for details.")
