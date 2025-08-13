#!/usr/bin/env python3
"""
Test script to verify the enhanced image descriptions in HTML reports
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from report_generator import ReportGenerator
import json

def test_enhanced_descriptions():
    """Test the enhanced image descriptions in HTML reports"""
    print("🧪 Testing enhanced image descriptions in HTML reports...")
    
    # Create mock analysis results
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
        'screenshots': {
            'url1': 'test_url1_screenshot.png',
            'url2': 'test_url2_screenshot.png'
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
    
    # Generate the HTML report with enhanced descriptions
    output_path = "test_enhanced_descriptions_report.html"
    report_gen.generate_enhanced_html_report(mock_analysis_results, mock_config, output_path)
    
    print(f"✅ HTML report with enhanced descriptions generated: {output_path}")
    
    # Check the HTML for the new descriptions
    with open(output_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    print("\n🔍 Checking for enhanced descriptions:")
    
    # Check for specific description elements
    descriptions_to_check = [
        "Full-page screenshot of the original URL",
        "Direct side-by-side view of both screenshots",
        "Color-coded heatmap showing pixel-level differences",
        "AI-powered analysis with automated difference detection",
        "Green rectangles highlight areas"
    ]
    
    found_descriptions = 0
    for desc in descriptions_to_check:
        if desc in html_content:
            print(f"✅ Found: '{desc[:40]}...'")
            found_descriptions += 1
        else:
            print(f"❌ Missing: '{desc[:40]}...'")
    
    if found_descriptions == len(descriptions_to_check):
        print(f"\n🎉 SUCCESS: All {found_descriptions}/{len(descriptions_to_check)} enhanced descriptions found!")
    else:
        print(f"\n⚠️  Only {found_descriptions}/{len(descriptions_to_check)} descriptions found")
    
    # Check for color-coded elements
    color_elements = ["Red areas", "orange/yellow areas", "blue areas", "Green rectangles"]
    color_found = sum(1 for color in color_elements if color in html_content)
    
    print(f"\n🎨 Color coding descriptions: {color_found}/{len(color_elements)} found")
    
    print(f"\n🌐 Open {output_path} in a browser to see the enhanced Visual Comparison tab!")
    
    return output_path

if __name__ == "__main__":
    test_enhanced_descriptions()
