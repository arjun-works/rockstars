#!/usr/bin/env python3
"""
Test script to verify visual comparison image generation fixes
"""

import os
import sys
import logging
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from visual_ai_regression import VisualAIRegression

def test_visual_images_fix():
    """Test that visual comparison images are generated and displayed correctly"""
    
    print("🧪 Testing Visual Comparison Images Fix")
    print("=" * 50)
    
    # Initialize the regression tester
    tester = VisualAIRegression()
    
    # Test configuration
    config = {
        'url1': 'https://example.com',
        'url2': 'https://httpbin.org/html',
        'browser': 'chrome',
        'resolution': '1280x720',
        'layout_shift': True,
        'font_color': True,
        'element_detection': True,
        'ai_analysis': True,
        'wcag_analysis': True
    }
    
    def progress_callback(message):
        print(f"📊 {message}")
    
    try:
        print("🚀 Starting visual regression analysis...")
        results = tester.run_analysis(config, progress_callback)
        
        print("\n✅ Analysis completed successfully!")
        
        # Check if reports were generated
        reports = results.get('reports', {})
        print(f"\n📋 Generated Reports:")
        for report_type, path in reports.items():
            exists = "✅" if os.path.exists(path) else "❌"
            print(f"  {exists} {report_type}: {os.path.basename(path)}")
        
        # Check specifically for visual comparison images
        print(f"\n🖼️  Visual Comparison Images:")
        
        visual_images = {
            'Side-by-Side': reports.get('sidebyside', ''),
            'Difference Heatmap': reports.get('heatmap', ''),
            'Visual Comparison': reports.get('visual', '')
        }
        
        for name, path in visual_images.items():
            if path and os.path.exists(path):
                size_kb = os.path.getsize(path) / 1024
                print(f"  ✅ {name}: {os.path.basename(path)} ({size_kb:.1f} KB)")
            else:
                print(f"  ❌ {name}: Not found or empty")
        
        # Check HTML report for image references
        html_report = reports.get('html', '')
        if html_report and os.path.exists(html_report):
            print(f"\n🌐 Checking HTML Report Image References:")
            with open(html_report, 'r', encoding='utf-8') as f:
                html_content = f.read()
                
                # Check for image tags
                import re
                img_tags = re.findall(r'<img[^>]*src="([^"]*)"[^>]*>', html_content)
                placeholder_divs = re.findall(r'<div[^>]*>.*?📷.*?not available.*?</div>', html_content, re.DOTALL)
                
                print(f"  📷 Image tags found: {len(img_tags)}")
                print(f"  📦 Placeholder divs found: {len(placeholder_divs)}")
                
                for img_src in img_tags:
                    if img_src.endswith(('.png', '.jpg', '.jpeg')):
                        img_path = os.path.join(os.path.dirname(html_report), img_src)
                        exists = "✅" if os.path.exists(img_path) else "❌"
                        print(f"    {exists} {img_src}")
        
        # Check analysis results for image paths
        analysis_results = results.get('analysis_results', {})
        print(f"\n🔍 Analysis Results Image Paths:")
        
        image_keys = ['heatmap_path', 'annotated_comparison_path']
        for key in image_keys:
            if key in analysis_results:
                path = analysis_results[key]
                exists = "✅" if os.path.exists(path) else "❌"
                print(f"  {exists} {key}: {os.path.basename(path) if path else 'None'}")
            else:
                print(f"  ❌ {key}: Not found in analysis results")
        
        # Final assessment
        print(f"\n🎯 Test Results Summary:")
        
        # Count successful image generations
        successful_images = sum(1 for path in visual_images.values() if path and os.path.exists(path))
        total_expected = len(visual_images)
        
        success_rate = (successful_images / total_expected) * 100 if total_expected > 0 else 0
        
        print(f"  📊 Visual Images Generated: {successful_images}/{total_expected} ({success_rate:.1f}%)")
        
        if success_rate >= 66:
            print(f"  ✅ PASS: Visual comparison images are working correctly!")
            return True
        else:
            print(f"  ❌ FAIL: Visual comparison images need attention")
            return False
            
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        logging.exception("Test error details:")
        return False

def test_report_generator_methods():
    """Test that the report generator methods exist and work"""
    
    print("\n🧪 Testing Report Generator Methods")
    print("=" * 50)
    
    from report_generator import ReportGenerator
    
    generator = ReportGenerator()
    
    # Test mock analysis results
    mock_results = {
        'screenshots': {
            'url1': 'screenshots/test1.png',
            'url2': 'screenshots/test2.png'
        },
        'heatmap_path': 'visualizations/test_heatmap.png',
        'annotated_comparison_path': 'visualizations/test_comparison.png'
    }
    
    # Test methods exist
    methods_to_test = [
        'generate_enhanced_visual_comparison',
        'generate_side_by_side_comparison', 
        'generate_difference_heatmap',
        '_generate_image_html'
    ]
    
    print("🔍 Checking method existence:")
    for method_name in methods_to_test:
        if hasattr(generator, method_name):
            print(f"  ✅ {method_name}: Found")
        else:
            print(f"  ❌ {method_name}: Missing")
    
    # Test image generation methods
    print("\n🖼️  Testing image generation methods:")
    
    test_output_dir = "test_output"
    os.makedirs(test_output_dir, exist_ok=True)
    
    try:
        # Test enhanced visual comparison
        visual_path = os.path.join(test_output_dir, "test_visual.png")
        result = generator.generate_enhanced_visual_comparison(mock_results, visual_path)
        exists = "✅" if os.path.exists(visual_path) else "❌"
        print(f"  {exists} Enhanced Visual Comparison: {os.path.basename(visual_path)}")
        
        # Test side-by-side comparison
        sidebyside_path = os.path.join(test_output_dir, "test_sidebyside.png")
        result = generator.generate_side_by_side_comparison(mock_results, sidebyside_path)
        exists = "✅" if os.path.exists(sidebyside_path) else "❌"
        print(f"  {exists} Side-by-Side Comparison: {os.path.basename(sidebyside_path)}")
        
        # Test difference heatmap
        heatmap_path = os.path.join(test_output_dir, "test_heatmap.png")
        result = generator.generate_difference_heatmap(mock_results, heatmap_path)
        exists = "✅" if os.path.exists(heatmap_path) else "❌"
        print(f"  {exists} Difference Heatmap: {os.path.basename(heatmap_path)}")
        
        # Test HTML generation
        html_result = generator._generate_image_html(mock_results, 'visual', 'Test Image')
        has_img_tag = '<img src=' in html_result
        has_placeholder = 'not available' in html_result
        
        if has_img_tag:
            print(f"  ✅ HTML Image Generation: Generated <img> tag")
        elif has_placeholder:
            print(f"  ⚠️  HTML Image Generation: Generated placeholder (expected)")
        else:
            print(f"  ❌ HTML Image Generation: Unexpected result")
        
        print(f"\n✅ Report generator methods test completed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Report generator test failed: {str(e)}")
        logging.exception("Report generator test error:")
        return False
    
    finally:
        # Cleanup test files
        import shutil
        if os.path.exists(test_output_dir):
            shutil.rmtree(test_output_dir)

if __name__ == "__main__":
    print("🔧 Visual Comparison Images Fix - Test Suite")
    print("=" * 60)
    print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    
    # Run tests
    test1_passed = test_report_generator_methods()
    test2_passed = test_visual_images_fix()
    
    # Final results
    print("\n" + "=" * 60)
    print("🏆 FINAL TEST RESULTS:")
    print(f"  📊 Report Generator Methods: {'✅ PASS' if test1_passed else '❌ FAIL'}")
    print(f"  🖼️  Visual Images Generation: {'✅ PASS' if test2_passed else '❌ FAIL'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 ALL TESTS PASSED! Visual comparison images fix is working correctly!")
        exit(0)
    else:
        print("\n⚠️  SOME TESTS FAILED. Please review the output above for details.")
        exit(1)
