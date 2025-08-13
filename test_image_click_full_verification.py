#!/usr/bin/env python3
"""
Test script to verify the image click functionality for full view in HTML reports.
This script creates a test HTML report and tests the image modal functionality.
"""

import os
import sys
import tempfile
import shutil
import webbrowser
from datetime import datetime

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from report_generator import ReportGenerator

def create_test_images():
    """Create test images for verification"""
    import numpy as np
    from PIL import Image
    
    # Create test images directory
    test_dir = "test_images"
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
    
    # Create test images
    images = {}
    
    # Create a simple test image (red)
    img1 = Image.new('RGB', (800, 600), color='red')
    img1_path = os.path.join(test_dir, 'test_url1_screenshot.png')
    img1.save(img1_path)
    images['url1_screenshot'] = img1_path
    
    # Create another test image (blue)
    img2 = Image.new('RGB', (800, 600), color='blue')
    img2_path = os.path.join(test_dir, 'test_url2_screenshot.png')
    img2.save(img2_path)
    images['url2_screenshot'] = img2_path
    
    # Create a side-by-side comparison image
    sidebyside = Image.new('RGB', (1600, 600), color='green')
    sidebyside_path = os.path.join(test_dir, 'test_sidebyside.png')
    sidebyside.save(sidebyside_path)
    images['sidebyside'] = sidebyside_path
    
    # Create a heatmap image
    heatmap = Image.new('RGB', (800, 600), color='yellow')
    heatmap_path = os.path.join(test_dir, 'test_heatmap.png')
    heatmap.save(heatmap_path)
    images['heatmap'] = heatmap_path
    
    # Create a visual comparison image
    visual = Image.new('RGB', (800, 600), color='purple')
    visual_path = os.path.join(test_dir, 'test_visual.png')
    visual.save(visual_path)
    images['visual'] = visual_path
    
    return images

def test_image_click_functionality():
    """Test the image click functionality in HTML reports"""
    print("🧪 Testing Image Click Functionality for Full View...")
    
    # Create test images
    test_images = create_test_images()
    
    # Create test analysis results
    analysis_results = {
        'screenshots': {
            'url1': test_images['url1_screenshot'],
            'url2': test_images['url2_screenshot']
        },
        'reports': {
            'sidebyside': test_images['sidebyside'],
            'heatmap': test_images['heatmap'],
            'visual': test_images['visual']
        },
        'metrics': {
            'ssim': 0.85,
            'mse': 125.5,
            'psnr': 28.9,
            'pixel_difference_percentage': 12.3
        },
        'ai_analysis': {
            'layout_differences': [],
            'color_differences': [],
            'text_differences': [],
            'element_differences': []
        },
        'wcag_analysis': {
            'contrast_ratio': 'AA',
            'color_difference': 'Pass',
            'accessibility_score': 'Good'
        }
    }
    
    # Test configuration
    config = {
        'url1': 'https://example.com/page1',
        'url2': 'https://example.com/page2',
        'viewport_width': 1920,
        'viewport_height': 1080
    }
    
    # Create report generator
    report_generator = ReportGenerator(output_dir="test_reports")
    
    # Copy test images to reports directory to simulate real scenario
    for image_type, image_path in test_images.items():
        if os.path.exists(image_path):
            dest_filename = f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{image_type}.png"
            dest_path = os.path.join("test_reports", dest_filename)
            shutil.copy2(image_path, dest_path)
            print(f"✅ Copied {image_type} to {dest_path}")
    
    # Generate HTML report
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        html_filename = f"test_visual_regression_report_{timestamp}.html"
        html_path = os.path.join("test_reports", html_filename)
        report_generator.generate_enhanced_html_report(analysis_results, config, html_path)
        print(f"✅ HTML report generated: {html_path}")
        
        # Verify the HTML contains the necessary elements
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Check for image click functionality
        checks = {
            'Modal CSS': 'position: fixed' in html_content and 'z-index: 10000' in html_content,
            'openImage function': 'function openImage(src)' in html_content,
            'onclick handlers': 'onclick="openImage(this.src)"' in html_content,
            'Cursor pointer': 'cursor: pointer' in html_content,
            'Modal close button': 'closeBtn.innerHTML = \'✕\'' in html_content,
            'Image scaling': 'max-width: 95%' in html_content and 'max-height: 95%' in html_content
        }
        
        print("\n🔍 Verification Results:")
        all_passed = True
        for check_name, passed in checks.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"   {status}: {check_name}")
            if not passed:
                all_passed = False
        
        # Check for actual images in the HTML
        image_checks = {
            'url1_screenshot': 'url1_screenshot' in html_content,
            'url2_screenshot': 'url2_screenshot' in html_content,
            'sidebyside': 'sidebyside' in html_content,
            'heatmap': 'heatmap' in html_content,
            'visual': 'visual' in html_content
        }
        
        print("\n🖼️ Image Presence Check:")
        for image_type, present in image_checks.items():
            status = "✅ FOUND" if present else "❌ MISSING"
            print(f"   {status}: {image_type}")
            if not present:
                all_passed = False
        
        # Test the JavaScript functionality manually
        print(f"\n📖 Manual Testing Instructions:")
        print(f"1. Open the HTML report: {html_path}")
        print(f"2. Navigate to the 'Visual Comparison' tab")
        print(f"3. Click on any image to test the modal functionality")
        print(f"4. Verify that:")
        print(f"   - Images open in a full-screen modal overlay")
        print(f"   - Modal has a dark background (90% opacity)")
        print(f"   - Images are properly scaled (max 95% of viewport)")
        print(f"   - Close button (✕) appears in top-right corner")
        print(f"   - Clicking outside the image or on close button closes modal")
        print(f"   - Body scroll is disabled when modal is open")
        
        # Open the report for manual testing
        try:
            webbrowser.open(f'file://{os.path.abspath(html_path)}')
            print(f"🌐 Opened report in default browser for manual testing")
        except Exception as e:
            print(f"⚠️ Could not open browser automatically: {e}")
        
        if all_passed:
            print(f"\n✅ All automated checks passed! Image click functionality is properly implemented.")
        else:
            print(f"\n❌ Some checks failed. Please review the implementation.")
        
        return html_path, all_passed
        
    except Exception as e:
        print(f"❌ Error generating HTML report: {e}")
        import traceback
        traceback.print_exc()
        return None, False

def test_javascript_execution():
    """Create a minimal test HTML to verify JavaScript execution"""
    print("\n🧪 Testing JavaScript Modal Functionality...")
    
    test_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image Click Test</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        .test-image { 
            max-width: 300px; 
            height: auto; 
            border: 2px solid #007bff; 
            border-radius: 8px; 
            cursor: pointer; 
            margin: 10px;
            transition: transform 0.3s;
        }
        .test-image:hover { transform: scale(1.05); }
    </style>
</head>
<body>
    <h1>🖼️ Image Click Modal Test</h1>
    <p>Click on the images below to test the modal functionality:</p>
    
    <img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICA8cmVjdCB3aWR0aD0iMzAwIiBoZWlnaHQ9IjIwMCIgZmlsbD0iIzAwN2JmZiIvPgogIDx0ZXh0IHg9IjE1MCIgeT0iMTA1IiBmb250LWZhbWlseT0iQXJpYWwsIHNhbnMtc2VyaWYiIGZvbnQtc2l6ZT0iMjAiIGZpbGw9IndoaXRlIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj5UZXN0IEltYWdlIDE8L3RleHQ+Cjwvc3ZnPg==" 
         alt="Test Image 1" 
         class="test-image"
         onclick="openImage(this.src)">
    
    <img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICA8cmVjdCB3aWR0aD0iMzAwIiBoZWlnaHQ9IjIwMCIgZmlsbD0iIzI4YTc0NSIvPgogIDx0ZXh0IHg9IjE1MCIgeT0iMTA1IiBmb250LWZhbWlseT0iQXJpYWwsIHNhbnMtc2VyaWYiIGZvbnQtc2l6ZT0iMjAiIGZpbGw9IndoaXRlIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj5UZXN0IEltYWdlIDI8L3RleHQ+Cjwvc3ZnPg==" 
         alt="Test Image 2" 
         class="test-image"
         onclick="openImage(this.src)">
    
    <script>
        function openImage(src) {
            // Create modal overlay
            const modal = document.createElement('div');
            modal.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.9);
                z-index: 10000;
                display: flex;
                justify-content: center;
                align-items: center;
                cursor: pointer;
            `;
            
            // Create image element
            const img = document.createElement('img');
            img.src = src;
            img.style.cssText = `
                max-width: 95%;
                max-height: 95%;
                object-fit: contain;
                border-radius: 8px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
            `;
            
            // Create close button
            const closeBtn = document.createElement('button');
            closeBtn.innerHTML = '✕';
            closeBtn.style.cssText = `
                position: absolute;
                top: 20px;
                right: 20px;
                background: rgba(255, 255, 255, 0.9);
                border: none;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                font-size: 20px;
                cursor: pointer;
                z-index: 10001;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
            `;
            
            // Add elements to modal
            modal.appendChild(img);
            modal.appendChild(closeBtn);
            
            // Add event listeners
            modal.addEventListener('click', function(e) {
                if (e.target === modal || e.target === closeBtn) {
                    document.body.removeChild(modal);
                    document.body.style.overflow = 'auto';
                }
            });
            
            // Prevent clicking on image from closing modal
            img.addEventListener('click', function(e) {
                e.stopPropagation();
            });
            
            // Add to page
            document.body.appendChild(modal);
            
            // Prevent body scroll
            document.body.style.overflow = 'hidden';
        }
        
        // Test function
        function testModal() {
            console.log('Testing modal functionality...');
            alert('Click on the images to test the modal functionality!');
        }
        
        // Auto-test after page load
        window.addEventListener('load', function() {
            console.log('Page loaded. Image click functionality ready for testing.');
        });
    </script>
    
    <div style="margin-top: 30px; padding: 15px; background: #f8f9fa; border-radius: 8px;">
        <h3>🧪 Test Instructions:</h3>
        <ol>
            <li>Click on either test image above</li>
            <li>Verify the modal opens with a dark overlay</li>
            <li>Check that the image is centered and properly scaled</li>
            <li>Confirm the close button (✕) appears in the top-right</li>
            <li>Test closing by clicking the close button</li>
            <li>Test closing by clicking outside the image</li>
            <li>Verify body scrolling is disabled when modal is open</li>
        </ol>
    </div>
</body>
</html>
    """
    
    # Save test HTML
    test_path = "test_reports/image_click_test.html"
    os.makedirs("test_reports", exist_ok=True)
    
    with open(test_path, 'w', encoding='utf-8') as f:
        f.write(test_html)
    
    print(f"✅ Created standalone test HTML: {test_path}")
    
    try:
        webbrowser.open(f'file://{os.path.abspath(test_path)}')
        print(f"🌐 Opened standalone test in browser")
    except Exception as e:
        print(f"⚠️ Could not open browser: {e}")
    
    return test_path

def main():
    """Main test function"""
    print("🚀 Starting Image Click Full View Verification Test")
    print("=" * 60)
    
    # Test 1: Full HTML report with image click functionality
    html_path, automated_passed = test_image_click_functionality()
    
    # Test 2: Standalone JavaScript test
    test_path = test_javascript_execution()
    
    print("\n" + "=" * 60)
    print("📋 SUMMARY:")
    print(f"✅ Full HTML Report: {'PASS' if automated_passed else 'FAIL'}")
    print(f"✅ Standalone Test: CREATED")
    
    if html_path:
        print(f"\n📁 Generated Files:")
        print(f"   - Full Report: {html_path}")
        print(f"   - Test HTML: {test_path}")
    
    print(f"\n🔧 Manual Testing Required:")
    print(f"   Open the generated HTML files and click on images to verify")
    print(f"   the modal functionality works as expected.")
    
    # Cleanup test images
    if os.path.exists("test_images"):
        shutil.rmtree("test_images")
        print(f"\n🧹 Cleaned up test images directory")

if __name__ == "__main__":
    main()
