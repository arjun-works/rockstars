#!/usr/bin/env python3
"""
Test script to verify screenshot paths are correctly handled in HTML reports
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from report_generator import ReportGenerator
import json

def test_screenshot_paths():
    """Test that screenshot paths are correctly identified and displayed"""
    print("🧪 Testing screenshot path handling in HTML reports...")
    
    # Create mock analysis results with screenshot paths
    mock_analysis_results = {
        'similarity_score': 0.8838,
        'ssim': 0.8838,
        'mse': 0.089806,
        'psnr': 10.47,
        'pixel_metrics': {
            'pixel_difference_percentage': 87.46,
            'different_pixels': 1553745,
            'total_pixels': 1776432,
            'avg_pixel_difference': 45.2,
            'max_pixel_difference': 255.0
        },
        'overall_similarity_percentage': 12.54,
        'layout_shifts': [
            {'distance': 25.5, 'shift_x': 10, 'shift_y': 15}
        ],
        'color_differences': [
            {'color_distance': 45.2, 'area': 1250, 'position': [150, 300, 60, 40]}
        ],
        'missing_elements': [],
        'new_elements': [
            {'area': 500, 'position': [200, 300, 80, 50]}
        ],
        'overlapping_elements': [],
        'ai_analysis': {
            'anomaly_detected': False,
            'confidence': 0.65,
            'feature_distance': 21.8174
        },
        'wcag_analysis': {
            'url1_score': 85.5,
            'url2_score': 92.3,
            'url1_violations': ['Color contrast issue', 'Missing alt text'],
            'url2_violations': ['Color contrast issue']
        },
        'summary_dict': {
            'similarity_score': 0.8838,
            'layout_differences': 1,
            'color_differences': 1,
            'element_changes': 1,
            'ai_anomalies': 0
        },
        # Add screenshot paths (the key fix)
        'screenshots': {
            'url1': 'screenshots/test/url1_screenshot.png',
            'url2': 'screenshots/test/url2_screenshot.png'
        },
        'heatmap_path': 'test_heatmap.png',
        'annotated_comparison_path': 'test_comparison.png',
        'reports': {
            'sidebyside': 'test_sidebyside.png',
            'visual': 'test_visual.png',
            'heatmap': 'test_heatmap.png'
        },
        'duration': '45 seconds'
    }
    
    # Mock config
    mock_config = {
        'layout_shift': True,
        'font_color': True,
        'element_detection': True,
        'ai_analysis': True,
        'wcag_analysis': True
    }
    
    # Create report generator
    report_gen = ReportGenerator()
    
    # Test the image HTML generation directly
    print("\n🔍 Testing image path resolution:")
    
    # Test screenshot paths
    url1_html = report_gen._generate_image_html(mock_analysis_results, 'url1_screenshot', 'Original screenshot')
    url2_html = report_gen._generate_image_html(mock_analysis_results, 'url2_screenshot', 'Comparison screenshot')
    
    # Check if paths are correctly resolved
    if 'url1_screenshot.png' in url1_html and 'not available' not in url1_html:
        print("✅ URL1 screenshot path correctly resolved")
    else:
        print("❌ URL1 screenshot path not resolved")
        print(f"   Generated HTML: {url1_html[:100]}...")
    
    if 'url2_screenshot.png' in url2_html and 'not available' not in url2_html:
        print("✅ URL2 screenshot path correctly resolved")
    else:
        print("❌ URL2 screenshot path not resolved")
        print(f"   Generated HTML: {url2_html[:100]}...")
    
    # Generate the full HTML report
    output_path = "test_screenshot_fix_report.html"
    report_gen.generate_enhanced_html_report(mock_analysis_results, mock_config, output_path)
    
    print(f"\n✅ HTML report generated: {output_path}")
    
    # Check the HTML file for screenshot references
    with open(output_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    if 'url1_screenshot.png' in html_content:
        print("✅ URL1 screenshot reference found in HTML")
    else:
        print("❌ URL1 screenshot reference NOT found in HTML")
    
    if 'url2_screenshot.png' in html_content:
        print("✅ URL2 screenshot reference found in HTML")
    else:
        print("❌ URL2 screenshot reference NOT found in HTML")
    
    if 'not available' in html_content:
        print("⚠️  'Not available' messages still present in HTML")
    else:
        print("✅ No 'not available' messages found")
    
    print(f"\n🌐 Open {output_path} in a browser to verify the fix!")
    
    return output_path

if __name__ == "__main__":
    test_screenshot_paths()
