#!/usr/bin/env python3
"""
Test script to generate a quick HTML report with the new tabbed interface
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from report_generator import ReportGenerator
import json

def test_tabbed_html_report():
    """Test the new tabbed HTML report interface"""
    print("🧪 Testing tabbed HTML report interface...")
    
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
            'url1_screenshot': 'test_image1.png',
            'url2_screenshot': 'test_image2.png'
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
    
    # Generate the tabbed HTML report
    output_path = "test_tabbed_report.html"
    report_gen.generate_enhanced_html_report(mock_analysis_results, mock_config, output_path)
    
    print(f"✅ Tabbed HTML report generated: {output_path}")
    print("🎯 New features:")
    print("   • Tab navigation for each section")
    print("   • Executive Summary tab")
    print("   • Visual Comparison tab")
    print("   • Detailed Analysis tab")
    print("   • WCAG Compliance tab")
    print("   • Detailed Findings tab")
    print("   • Export Options tab")
    print("   • Report Info tab")
    print()
    print("🌐 Open the HTML file in a browser to see the tabbed interface!")
    
    return output_path

if __name__ == "__main__":
    test_tabbed_html_report()
