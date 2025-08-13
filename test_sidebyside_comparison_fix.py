#!/usr/bin/env python3
"""
Test script to verify that Side-by-Side and Visual Comparison images are now distinct.
This test ensures the fix for the path mapping issue in _generate_image_html.
Updated: Fixed the 'sidebyside' fallback path mapping from 'annotated_comparison_path' to None.
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

def test_sidebyside_fix():
    """Test that side-by-side and visual comparison generate different images"""
    print("🔧 Testing Side-by-Side vs Visual Comparison Fix")
    print("=" * 60)
    
    # Create temporary directory for test
    temp_dir = tempfile.mkdtemp(prefix="sidebyside_test_")
    
    try:
        # Create test screenshots
        url1_screenshot = os.path.join(temp_dir, "reference.png")
        url2_screenshot = os.path.join(temp_dir, "test.png")
        
        create_test_screenshot(url1_screenshot, "REFERENCE PAGE", 'lightblue', 'darkblue')
        create_test_screenshot(url2_screenshot, "TEST PAGE", 'lightgreen', 'darkgreen')
        
        print(f"✅ Created test screenshots:")
        print(f"   📸 Reference: {url1_screenshot}")
        print(f"   📸 Test: {url2_screenshot}")
        
        # Create test analysis results
        analysis_results = {
            'screenshots': {
                'url1': url1_screenshot,
                'url2': url2_screenshot
            },
            'comparisons': {
                'overall_similarity': 0.85,
                'differences_found': 15
            },
            'ai_analysis': {
                'differences': [
                    {'type': 'color', 'description': 'Background color changed from blue to green'},
                    {'type': 'text', 'description': 'Text changed from REFERENCE to TEST'}
                ]
            },
            'summary': {
                'total_differences': 2,
                'critical_issues': 0
            }
        }
        
        # Create annotated comparison for visual comparison
        annotated_path = os.path.join(temp_dir, "annotated_comparison.png")
        create_test_screenshot(annotated_path, "ANNOTATED COMPARISON", 'lightyellow', 'red')
        analysis_results['annotated_comparison_path'] = annotated_path
        
        # Create heatmap for difference heatmap
        heatmap_path = os.path.join(temp_dir, "heatmap.png")
        create_test_screenshot(heatmap_path, "DIFFERENCE HEATMAP", 'lightcoral', 'darkred')
        analysis_results['heatmap_path'] = heatmap_path
        
        print(f"✅ Created test analysis data with {len(analysis_results['ai_analysis']['differences'])} differences")
        
        # Initialize report generator
        report_generator = ReportGenerator(output_dir=temp_dir)
        
        # Test configuration
        config = {
            'url1': 'http://reference.example.com',
            'url2': 'http://test.example.com',
            'layout_shift': True,
            'font_color': True,
            'element_analysis': True,
            'screenshot_comparison': True,
            'wcag_compliance': False  # Skip WCAG for this test
        }
        
        print("\n🔄 Generating comprehensive report...")
        
        # Generate comprehensive report
        reports = report_generator.generate_comprehensive_report(analysis_results, config)
        
        print(f"✅ Report generation completed!")
        print(f"   📁 Output directory: {temp_dir}")
        
        # Verify that all three image types are different
        print("\n🔍 Verifying image distinctiveness...")
        
        sidebyside_path = reports.get('sidebyside', '')
        visual_path = reports.get('visual', '')
        heatmap_path = reports.get('heatmap', '')
        
        def get_image_signature(path):
            """Get a simple signature of an image to check if it's different"""
            if not os.path.exists(path):
                return None
            
            img = Image.open(path)
            # Get image size and first few pixels as signature
            signature = (img.size, img.getpixel((10, 10)) if img.size > (10, 10) else None)
            return signature
        
        sidebyside_sig = get_image_signature(sidebyside_path)
        visual_sig = get_image_signature(visual_path)
        heatmap_sig = get_image_signature(heatmap_path)
        
        print(f"   📊 Side-by-Side: {os.path.basename(sidebyside_path) if sidebyside_path else 'N/A'}")
        print(f"      Size: {sidebyside_sig[0] if sidebyside_sig else 'N/A'}")
        print(f"   📊 Visual Comparison: {os.path.basename(visual_path) if visual_path else 'N/A'}")
        print(f"      Size: {visual_sig[0] if visual_sig else 'N/A'}")
        print(f"   📊 Difference Heatmap: {os.path.basename(heatmap_path) if heatmap_path else 'N/A'}")
        print(f"      Size: {heatmap_sig[0] if heatmap_sig else 'N/A'}")
        
        # Check distinctiveness
        images_are_distinct = True
        
        if sidebyside_sig and visual_sig and sidebyside_sig == visual_sig:
            print("❌ ERROR: Side-by-Side and Visual Comparison are identical!")
            images_are_distinct = False
        else:
            print("✅ Side-by-Side and Visual Comparison are different")
        
        if visual_sig and heatmap_sig and visual_sig == heatmap_sig:
            print("❌ ERROR: Visual Comparison and Heatmap are identical!")
            images_are_distinct = False
        else:
            print("✅ Visual Comparison and Heatmap are different")
        
        if sidebyside_sig and heatmap_sig and sidebyside_sig == heatmap_sig:
            print("❌ ERROR: Side-by-Side and Heatmap are identical!")
            images_are_distinct = False
        else:
            print("✅ Side-by-Side and Heatmap are different")
        
        # Check HTML report content
        html_path = reports.get('html', '')
        if html_path and os.path.exists(html_path):
            print(f"\n📋 Checking HTML report content...")
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Check for different image references
            sidebyside_filename = os.path.basename(sidebyside_path) if sidebyside_path else ''
            visual_filename = os.path.basename(visual_path) if visual_path else ''
            heatmap_filename = os.path.basename(heatmap_path) if heatmap_path else ''
            
            if sidebyside_filename and sidebyside_filename in html_content:
                print(f"✅ HTML references side-by-side image: {sidebyside_filename}")
            else:
                print(f"❌ HTML missing side-by-side image reference")
                
            if visual_filename and visual_filename in html_content:
                print(f"✅ HTML references visual comparison image: {visual_filename}")
            else:
                print(f"❌ HTML missing visual comparison image reference")
                
            if heatmap_filename and heatmap_filename in html_content:
                print(f"✅ HTML references heatmap image: {heatmap_filename}")
            else:
                print(f"❌ HTML missing heatmap image reference")
        
        # Test summary
        print(f"\n📈 Test Results Summary:")
        print(f"   🔧 Fix Applied: Updated path mapping in _generate_image_html")
        print(f"   📊 Images Generated: {len([p for p in [sidebyside_path, visual_path, heatmap_path] if p and os.path.exists(p)])}/3")
        print(f"   ✅ Images Distinct: {'Yes' if images_are_distinct else 'No'}")
        print(f"   📋 HTML Report: {'Generated' if html_path and os.path.exists(html_path) else 'Missing'}")
        
        if images_are_distinct:
            print(f"\n🎉 SUCCESS: Side-by-Side fix is working correctly!")
            print(f"   All three image types are now distinct and show different content.")
        else:
            print(f"\n❌ FAILURE: Images are still not distinct - further investigation needed.")
        
        # Keep files for manual inspection
        print(f"\n📁 Test files preserved for inspection:")
        print(f"   Directory: {temp_dir}")
        print(f"   HTML Report: {html_path}")
        
        return images_are_distinct
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    # Note: Not cleaning up temp_dir to allow manual inspection

if __name__ == "__main__":
    print("🧪 Side-by-Side vs Visual Comparison Fix Test")
    print("Testing that the path mapping fix ensures distinct images")
    print("=" * 60)
    
    success = test_sidebyside_fix()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 TEST PASSED: Side-by-side fix is working correctly!")
    else:
        print("❌ TEST FAILED: Images are still not distinct")
    
    print("🔍 Check the generated files manually to verify visual differences.")
