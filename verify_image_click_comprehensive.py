#!/usr/bin/env python3
"""
Comprehensive test to verify image click functionality with actual screenshots.
This script will check the most recent analysis report and test the image modal functionality.
"""

import os
import sys
import webbrowser
import shutil
from datetime import datetime

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def find_latest_report():
    """Find the most recent HTML report"""
    reports_dir = "reports"
    if not os.path.exists(reports_dir):
        return None
    
    html_files = [f for f in os.listdir(reports_dir) if f.endswith('.html') and 'visual_regression_report_' in f]
    if not html_files:
        return None
    
    # Sort by modification time and get the latest
    html_files.sort(key=lambda f: os.path.getmtime(os.path.join(reports_dir, f)), reverse=True)
    return os.path.join(reports_dir, html_files[0])

def verify_image_click_functionality():
    """Verify image click functionality in the latest report"""
    print("🔍 Verifying Image Click Functionality in Latest Report...")
    
    # Find the latest report
    latest_report = find_latest_report()
    if not latest_report:
        print("❌ No HTML reports found in the reports directory")
        return False
    
    print(f"📄 Testing report: {latest_report}")
    
    # Check if the report exists and read it
    if not os.path.exists(latest_report):
        print(f"❌ Report file not found: {latest_report}")
        return False
    
    try:
        with open(latest_report, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        print(f"📏 Report size: {len(html_content)} characters")
        
        # Check for essential image click functionality components
        checks = {
            'JavaScript openImage function': 'function openImage(src)' in html_content,
            'Modal CSS styling': 'position: fixed' in html_content and 'z-index: 10000' in html_content,
            'Close button implementation': 'closeBtn.innerHTML = \'✕\'' in html_content,
            'Tab navigation': 'tab-button' in html_content,
            'Visual Comparison tab': 'visual-comparison' in html_content,
            'Image click handlers': 'onclick="openImage(' in html_content,
            'Image containers': 'image-container' in html_content,
            'Cursor pointer styling': 'cursor: pointer' in html_content
        }
        
        print("\n🔍 Functionality Checks:")
        all_passed = True
        for check_name, passed in checks.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"   {status}: {check_name}")
            if not passed:
                all_passed = False
        
        # Check for actual images vs placeholders
        image_checks = {}
        image_types = ['url1_screenshot', 'url2_screenshot', 'sidebyside', 'heatmap', 'visual']
        
        print("\n🖼️ Image Content Analysis:")
        for img_type in image_types:
            has_actual_img = f'<img src=' in html_content and img_type in html_content
            has_placeholder = 'This image will be available after running' in html_content
            
            if has_actual_img:
                print(f"   ✅ {img_type}: Actual image tag found")
                image_checks[img_type] = 'actual'
            elif has_placeholder:
                print(f"   📦 {img_type}: Placeholder shown (expected if files don't exist)")
                image_checks[img_type] = 'placeholder'
            else:
                print(f"   ❌ {img_type}: Neither image nor placeholder found")
                image_checks[img_type] = 'missing'
                all_passed = False
        
        # Check if actual image files exist in the reports directory
        report_dir = os.path.dirname(latest_report)
        base_name = os.path.splitext(os.path.basename(latest_report))[0]
        
        print(f"\n📁 Checking for actual image files in {report_dir}:")
        image_files = {
            'sidebyside': f"{base_name}_side_by_side.png",
            'heatmap': f"{base_name}_difference_heatmap.png",
            'visual': f"{base_name}_visual_comparison.png"
        }
        
        existing_images = []
        for img_type, filename in image_files.items():
            filepath = os.path.join(report_dir, filename)
            if os.path.exists(filepath):
                print(f"   ✅ {filename}: Exists ({os.path.getsize(filepath)} bytes)")
                existing_images.append(img_type)
            else:
                print(f"   ❌ {filename}: Not found")
        
        # Test the report in browser
        print(f"\n🌐 Opening report for manual testing...")
        try:
            webbrowser.open(f'file://{os.path.abspath(latest_report)}')
            print(f"✅ Report opened in browser")
        except Exception as e:
            print(f"⚠️ Could not open browser: {e}")
        
        # Create a test HTML with working image click if images exist
        if existing_images:
            print(f"\n🧪 Creating test HTML with actual images...")
            create_test_html_with_images(report_dir, existing_images, image_files)
        
        # Summary
        print(f"\n📋 SUMMARY:")
        if all_passed:
            print("✅ All image click functionality checks passed!")
            if existing_images:
                print(f"🖼️ Found {len(existing_images)} actual image files that can be clicked")
            else:
                print("📦 Only placeholders shown (normal when no image files exist)")
            print("🔧 Manual test: Open the report and click on the Visual Comparison tab")
            if existing_images:
                print("   Try clicking on the actual images to test the modal functionality")
            return True
        else:
            print("❌ Some functionality checks failed!")
            return False
            
    except Exception as e:
        print(f"❌ Error reading report: {e}")
        return False

def create_test_html_with_images(report_dir, existing_images, image_files):
    """Create a test HTML file with actual images for click testing"""
    try:
        test_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image Click Test - Actual Images</title>
    <style>
        body {{ font-family: Arial, sans-serif; padding: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        .image-gallery {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 20px; }}
        .image-container {{ background: #f9f9f9; padding: 20px; border-radius: 8px; text-align: center; }}
        .test-image {{ max-width: 100%; height: auto; border-radius: 5px; cursor: pointer; transition: transform 0.3s; border: 2px solid #007bff; }}
        .test-image:hover {{ transform: scale(1.02); }}
        h1 {{ color: #333; text-align: center; }}
        h3 {{ color: #666; margin-bottom: 15px; }}
        .instructions {{ background: #e3f2fd; padding: 15px; border-radius: 8px; margin-bottom: 20px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🖼️ Image Click Functionality Test</h1>
        <div class="instructions">
            <h3>📖 Instructions:</h3>
            <p><strong>Click on any image below to test the modal functionality.</strong></p>
            <p>Expected behavior:</p>
            <ul>
                <li>Image opens in a full-screen modal overlay</li>
                <li>Dark background (90% opacity)</li>
                <li>Close button (✕) in top-right corner</li>
                <li>Click outside image or close button to close</li>
                <li>Body scroll disabled when modal is open</li>
            </ul>
        </div>
        
        <div class="image-gallery">
"""
        
        for img_type in existing_images:
            filename = image_files[img_type]
            test_html += f"""
            <div class="image-container">
                <h3>🎯 {img_type.replace('_', ' ').title()}</h3>
                <img src="{filename}" 
                     alt="{img_type} comparison" 
                     class="test-image"
                     onclick="openImage(this.src)">
                <p style="font-size: 12px; color: #666; margin-top: 10px;">
                    Click the image above to test modal functionality
                </p>
            </div>
"""
        
        test_html += """
        </div>
    </div>
    
    <script>
        function openImage(src) {
            console.log('Opening image:', src);
            
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
            
            console.log('Modal created and added to page');
        }
        
        // Log when page is ready
        window.addEventListener('load', function() {
            console.log('Image click test page loaded. Ready for testing!');
        });
    </script>
</body>
</html>
"""
        
        test_path = os.path.join(report_dir, "image_click_test_with_actual_images.html")
        with open(test_path, 'w', encoding='utf-8') as f:
            f.write(test_html)
        
        print(f"✅ Test HTML created: {test_path}")
        
        # Open the test HTML
        try:
            webbrowser.open(f'file://{os.path.abspath(test_path)}')
            print(f"🌐 Test HTML opened in browser")
        except Exception as e:
            print(f"⚠️ Could not open test HTML: {e}")
            
    except Exception as e:
        print(f"❌ Error creating test HTML: {e}")

def main():
    """Main verification function"""
    print("🚀 Comprehensive Image Click Functionality Verification")
    print("=" * 65)
    
    success = verify_image_click_functionality()
    
    print("\n" + "=" * 65)
    if success:
        print("✅ SUCCESS: Image click functionality is properly implemented!")
        print("🔧 Continue with manual testing in the opened browser windows")
    else:
        print("❌ ISSUES DETECTED: Please review the functionality checks above")

if __name__ == "__main__":
    main()
