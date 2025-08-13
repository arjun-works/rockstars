#!/usr/bin/env python3
"""
Test script to verify the enhanced Image Similarity Metrics definitions in HTML report.
"""

import sys
import os
import tempfile

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from report_generator import ReportGenerator

def test_enhanced_metrics_definitions():
    """Test the enhanced Image Similarity Metrics with definitions"""
    print("🧪 Testing Enhanced Image Similarity Metrics Definitions...")
    
    # Create test analysis results with various metric values
    test_results = {
        'comparisons': {
            'ssim': 0.876,  # Good similarity
            'mse': 120.5,   # Moderate differences
            'pixel_diff_percentage': 3.2  # Minor change
        },
        'screenshots': {
            'url1': 'test_ref.png',
            'url2': 'test_comp.png'
        },
        'summary_dict': {
            'similarity_score': 0.876,
            'layout_differences': 2,
            'color_differences': 1,
            'element_changes': 0,
            'ai_anomalies': 1
        }
    }
    
    test_config = {
        'url1': 'https://example.com/reference',
        'url2': 'https://example.com/test',
        'browser': 'chrome',
        'resolution': '1920x1080',
        'layout_shift': True,
        'font_color': True,
        'element_detection': True,
        'ai_analysis': True,
        'wcag_analysis': False
    }
    
    # Generate HTML report
    report_gen = ReportGenerator()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        html_path = os.path.join(temp_dir, 'enhanced_metrics_test.html')
        
        try:
            report_gen.generate_enhanced_html_report(test_results, test_config, html_path)
            
            # Read the generated HTML
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            print("✅ HTML report generated successfully")
            
            # Check for enhanced features
            enhancements_found = []
            
            if 'Metric Definitions:' in html_content:
                enhancements_found.append("📚 Metric definitions section")
            
            if 'SSIM (Structural Similarity Index):' in html_content:
                enhancements_found.append("🔍 SSIM explanation")
            
            if 'MSE (Mean Squared Error):' in html_content:
                enhancements_found.append("📊 MSE explanation")
            
            if 'Pixel Difference:' in html_content:
                enhancements_found.append("🎯 Pixel difference explanation")
            
            if 'grid-template-columns' in html_content:
                enhancements_found.append("📱 Enhanced visual layout")
            
            if 'Interpretation Guide:' in html_content:
                enhancements_found.append("💡 Interpretation guide")
            
            if 'Good similarity' in html_content:
                enhancements_found.append("🎯 SSIM interpretation (Good)")
            
            if 'Moderate differences' in html_content:
                enhancements_found.append("📈 MSE interpretation (Moderate)")
            
            if 'Minor change' in html_content:
                enhancements_found.append("📊 Pixel interpretation (Minor)")
            
            print("\n🎉 Enhanced Features Found:")
            for enhancement in enhancements_found:
                print(f"  ✅ {enhancement}")
            
            if len(enhancements_found) >= 6:
                print(f"\n🌟 SUCCESS: {len(enhancements_found)}/9 enhancements detected!")
            else:
                print(f"\n⚠️  PARTIAL: {len(enhancements_found)}/9 enhancements detected")
            
            # Check specific metric values and interpretations
            print("\n📊 Metric Values Verification:")
            if '0.8760' in html_content:
                print("  ✅ SSIM value correctly displayed (0.8760)")
            if '120.50' in html_content:
                print("  ✅ MSE value correctly displayed (120.50)")
            if '3.20%' in html_content:
                print("  ✅ Pixel difference correctly displayed (3.20%)")
            
            # Save test report for manual inspection
            final_path = 'enhanced_metrics_test_report.html'
            with open(final_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"\n📄 Enhanced report saved for inspection: {final_path}")
            
            return len(enhancements_found) >= 6
            
        except Exception as e:
            print(f"❌ Error generating HTML report: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

def test_different_metric_ranges():
    """Test interpretations with different metric value ranges"""
    print("\n🔬 Testing Different Metric Value Ranges...")
    
    test_cases = [
        {
            'name': 'Excellent Similarity',
            'ssim': 0.98, 'mse': 25.0, 'pixel_diff': 0.5,
            'expected': ['Excellent similarity', 'Minimal differences', 'Minimal change']
        },
        {
            'name': 'Poor Similarity', 
            'ssim': 0.65, 'mse': 800.0, 'pixel_diff': 25.0,
            'expected': ['Poor similarity', 'Major differences', 'Major change']
        }
    ]
    
    report_gen = ReportGenerator()
    
    for i, test_case in enumerate(test_cases):
        print(f"\n  Test {i+1}: {test_case['name']}")
        
        test_results = {
            'comparisons': {
                'ssim': test_case['ssim'],
                'mse': test_case['mse'],
                'pixel_diff_percentage': test_case['pixel_diff']
            },
            'screenshots': {'url1': 'test1.png', 'url2': 'test2.png'},
            'summary_dict': {'similarity_score': test_case['ssim']}
        }
        
        config = {'layout_shift': False, 'font_color': False, 'element_detection': False, 'ai_analysis': False}
        
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                html_path = os.path.join(temp_dir, f'test_{i+1}.html')
                report_gen.generate_enhanced_html_report(test_results, config, html_path)
                
                with open(html_path, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                # Check if expected interpretations are present
                found_interpretations = []
                for expected in test_case['expected']:
                    if expected in html_content:
                        found_interpretations.append(expected)
                
                print(f"    📊 SSIM: {test_case['ssim']:.3f}, MSE: {test_case['mse']:.1f}, Pixel: {test_case['pixel_diff']:.1f}%")
                print(f"    ✅ Found interpretations: {len(found_interpretations)}/{len(test_case['expected'])}")
                for interp in found_interpretations:
                    print(f"      • {interp}")
                
        except Exception as e:
            print(f"    ❌ Error in test case {i+1}: {str(e)}")

if __name__ == "__main__":
    print("🚀 Enhanced Image Similarity Metrics Test")
    print("=" * 50)
    
    # Test 1: Basic enhancement verification
    success = test_enhanced_metrics_definitions()
    
    # Test 2: Different metric ranges
    test_different_metric_ranges()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Enhanced Image Similarity Metrics definitions successfully added to HTML report!")
        print("📝 Users will now see clear explanations and interpretations for all metrics.")
    else:
        print("⚠️ Some enhancements may not be working correctly. Check the output above.")
    
    print("📄 Check 'enhanced_metrics_test_report.html' to see the enhanced display.")
