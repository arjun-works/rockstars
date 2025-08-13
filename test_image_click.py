#!/usr/bin/env python3
"""
Test script to verify image click functionality in HTML reports
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from report_generator import ReportGenerator

def test_image_click_functionality():
    """Test that images have proper click functionality"""
    print("🧪 Testing image click functionality in HTML reports...")
    
    # Create a test image file
    test_image_path = "test_click_image.png"
    with open(test_image_path, 'w') as f:
        f.write("test image content")
    
    # Create mock analysis results
    mock_analysis_results = {
        'similarity_score': 0.8838,
        'screenshots': {
            'url1': test_image_path,
            'url2': test_image_path
        },
        'reports': {
            'sidebyside': test_image_path,
            'visual': test_image_path,
            'heatmap': test_image_path
        },
        'summary_dict': {
            'similarity_score': 0.8838,
            'layout_differences': 1,
            'color_differences': 1,
            'element_changes': 1,
            'ai_anomalies': 0
        }
    }
    
    # Mock config
    mock_config = {
        'layout_shift': True,
        'font_color': True,
        'element_detection': True,
        'ai_analysis': True
    }
    
    # Create report generator
    report_gen = ReportGenerator()
    
    # Generate HTML report
    output_path = "test_image_click_report.html"
    report_gen.generate_enhanced_html_report(mock_analysis_results, mock_config, output_path)
    
    print(f"✅ HTML report generated: {output_path}")
    
    # Check the HTML for click functionality
    with open(output_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    print("\n🔍 Checking for image click functionality:")
    
    # Check for openImage function
    if 'function openImage(' in html_content:
        print("✅ openImage function found in HTML")
    else:
        print("❌ openImage function NOT found in HTML")
    
    # Check for onclick attributes
    onclick_count = html_content.count('onclick="openImage(this.src)"')
    print(f"✅ Found {onclick_count} images with onclick handlers")
    
    # Check for modal functionality
    if 'modal' in html_content and 'position: fixed' in html_content:
        print("✅ Modal functionality found")
    else:
        print("❌ Modal functionality NOT found")
    
    # Check for cursor pointer style
    if 'cursor: pointer' in html_content:
        print("✅ Pointer cursor styling found")
    else:
        print("❌ Pointer cursor styling NOT found")
    
    # Check for hover effects
    if 'onmouseover' in html_content and 'scale(1.02)' in html_content:
        print("✅ Hover effects found")
    else:
        print("❌ Hover effects NOT found")
    
    print(f"\n🌐 Open {output_path} in a browser and click on images to test!")
    print("💡 Images should open in a modal overlay with close button")
    
    # Clean up
    try:
        os.remove(test_image_path)
        print("\n🧹 Test files cleaned up")
    except:
        pass
    
    return output_path

if __name__ == "__main__":
    test_image_click_functionality()
