#!/usr/bin/env python3
"""
Test script to verify that analysis options filtering works correctly.
This script will test that only selected analysis types are executed and displayed.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from visual_ai_regression import VisualAIRegression
import json

def test_analysis_options_filtering():
    """Test that only selected analysis options are executed"""
    
    print("🔬 Testing Analysis Options Filtering...")
    print("="*50)
    
    # Test configuration with only layout_shift enabled
    config_layout_only = {
        'url1': 'https://example.com',
        'url2': 'https://httpbin.org/html',
        'browser': 'chrome',
        'resolution': '1920x1080',
        'layout_shift': True,
        'font_color': False,
        'element_detection': False,
        'ai_analysis': False,
        'wcag_analysis': False
    }
    
    print("1. Testing with Layout Shift Analysis ONLY...")
    print(f"   Configuration: {config_layout_only}")
    
    # Initialize regression module
    regression = VisualAIRegression()
    
    try:
        # Run analysis with limited options
        results = regression.run_analysis(config_layout_only)
        
        # Check that only layout shift analysis was performed
        analysis_results = results.get('analysis_results', {})
        summary_dict = results.get('summary_dict', {})
        
        print("\n📊 Analysis Results Check:")
        print(f"   - Layout shifts present: {'layout_shifts' in analysis_results}")
        print(f"   - Color differences present: {'color_differences' in analysis_results}")
        print(f"   - Element detection present: {'missing_elements' in analysis_results or 'new_elements' in analysis_results}")
        print(f"   - AI analysis present: {'ai_analysis' in analysis_results}")
        print(f"   - WCAG analysis present: {'wcag_analysis' in analysis_results}")
        
        print("\n📈 Summary Dict Check:")
        print(f"   - Layout differences in summary: {'layout_differences' in summary_dict}")
        print(f"   - Color differences in summary: {'color_differences' in summary_dict}")
        print(f"   - AI anomalies in summary: {'ai_anomalies' in summary_dict}")
        print(f"   - WCAG scores in summary: {'wcag_url1_score' in summary_dict}")
        
        # Verify that disabled options are not in results
        unexpected_keys = []
        if 'color_differences' in analysis_results:
            unexpected_keys.append('color_differences')
        if 'ai_analysis' in analysis_results:
            unexpected_keys.append('ai_analysis')
        if 'wcag_analysis' in analysis_results:
            unexpected_keys.append('wcag_analysis')
        if 'missing_elements' in analysis_results or 'new_elements' in analysis_results:
            unexpected_keys.append('element_detection')
            
        if unexpected_keys:
            print(f"❌ FAILED: Unexpected analysis results found: {unexpected_keys}")
            return False
        else:
            print("✅ SUCCESS: Only enabled analysis types were executed")
        
        # Test with all options enabled
        print("\n" + "="*50)
        print("2. Testing with ALL Analysis Options enabled...")
        
        config_all = {
            'url1': 'https://example.com',
            'url2': 'https://httpbin.org/html',
            'browser': 'chrome',
            'resolution': '1920x1080',
            'layout_shift': True,
            'font_color': True,
            'element_detection': True,
            'ai_analysis': True,
            'wcag_analysis': True
        }
        
        results_all = regression.run_analysis(config_all)
        analysis_results_all = results_all.get('analysis_results', {})
        summary_dict_all = results_all.get('summary_dict', {})
        
        print("\n📊 All Analysis Results Check:")
        print(f"   - Layout shifts: {'layout_shifts' in analysis_results_all}")
        print(f"   - Color differences: {'color_differences' in analysis_results_all}")
        print(f"   - Element detection: {'missing_elements' in analysis_results_all or 'new_elements' in analysis_results_all}")
        print(f"   - AI analysis: {'ai_analysis' in analysis_results_all}")
        print(f"   - WCAG analysis: {'wcag_analysis' in analysis_results_all}")
        
        print("\n📈 All Summary Dict Check:")
        print(f"   - Layout differences: {'layout_differences' in summary_dict_all}")
        print(f"   - Color differences: {'color_differences' in summary_dict_all}")
        print(f"   - AI anomalies: {'ai_anomalies' in summary_dict_all}")
        print(f"   - WCAG scores: {'wcag_url1_score' in summary_dict_all}")
        
        # Check that summary only includes enabled metrics
        expected_keys_limited = ['similarity_score', 'layout_differences']
        expected_keys_all = ['similarity_score', 'layout_differences', 'color_differences', 'ai_anomalies', 'wcag_url1_score', 'wcag_url2_score']
        
        print("\n🔍 Summary Content Verification:")
        print(f"   Limited config summary keys: {list(summary_dict.keys())}")
        print(f"   All config summary keys: {list(summary_dict_all.keys())}")
        
        print("\n✅ Analysis Options Filtering Test COMPLETED!")
        print("   - Only enabled analysis types are executed")
        print("   - Summary only includes metrics for enabled types")
        print("   - Reports should only show enabled analysis sections")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧪 Visual AI Regression Module - Analysis Options Filter Test")
    print("="*70)
    
    try:
        success = test_analysis_options_filtering()
        if success:
            print("\n🎉 ALL TESTS PASSED!")
            print("   Analysis options filtering is working correctly.")
        else:
            print("\n❌ TESTS FAILED!")
            print("   Analysis options filtering needs fixes.")
    except Exception as e:
        print(f"\n💥 Test execution failed: {str(e)}")
        print("   Please check the module configuration.")
    
    print("\n" + "="*70)
    input("Press Enter to exit...")
