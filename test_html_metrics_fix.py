#!/usr/bin/env python3
"""
Test script to verify HTML report metrics are displaying correctly
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from report_generator import ReportGenerator
import json

def test_html_report_metrics():
    """Test that the HTML report displays the new metrics correctly"""
    print("🧪 Testing HTML report metrics display...")
    
    # Create mock analysis results with the new metrics
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
        'summary_dict': {
            'similarity_score': 0.8838,
            'ssim': 0.8838,
            'mse': 0.089806,
            'psnr': 10.47,
            'pixel_difference_percentage': 87.46,
            'layout_differences': 1,
            'color_differences': 1,
            'missing_elements': 0,
            'new_elements': 1,
            'element_changes': 1,
            'ai_anomalies': 0
        }
    }
    
    mock_config = {
        'url1': 'https://example.com',
        'url2': 'https://saucedemo.com',
        'browser': 'chrome',
        'resolution': '1920x1080',
        'layout_shift': True,
        'font_color': True,
        'element_detection': True,
        'ai_analysis': True,
        'wcag_analysis': False
    }
    
    try:
        # Create report generator
        generator = ReportGenerator()
        
        # Generate HTML report
        test_html_path = "test_metrics_report.html"
        generator.generate_enhanced_html_report(mock_analysis_results, mock_config, test_html_path)
        
        # Read the generated HTML and check for metrics
        with open(test_html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Check if the metrics are present in the HTML
        ssim_present = "0.8838" in html_content
        mse_present = "0.089806" in html_content  
        psnr_present = "10.47 dB" in html_content
        pixel_diff_present = "87.46%" in html_content
        
        print(f"✅ HTML report generated: {test_html_path}")
        print(f"📊 Metrics found in HTML:")
        print(f"   • SSIM (0.8838): {'✅' if ssim_present else '❌'}")
        print(f"   • MSE (0.089806): {'✅' if mse_present else '❌'}")
        print(f"   • PSNR (10.47 dB): {'✅' if psnr_present else '❌'}")
        print(f"   • Pixel Diff (87.46%): {'✅' if pixel_diff_present else '❌'}")
        
        if ssim_present and mse_present and psnr_present and pixel_diff_present:
            print("\n🎉 SUCCESS: All metrics are now correctly displayed in the HTML report!")
            print(f"🌐 Open {test_html_path} in a browser to view the report")
            return True
        else:
            print("\n❌ Some metrics are still missing from the HTML report")
            return False
            
    except Exception as e:
        print(f"❌ ERROR during HTML report testing: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_html_report_metrics()
    if success:
        print("\n🚀 The HTML report metrics display issue has been fixed!")
    else:
        print("\n⚠️ There may still be issues with the HTML report metrics display.")
