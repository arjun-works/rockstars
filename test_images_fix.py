"""
Test script to verify image display in HTML reports with actual generated images
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from report_generator import ReportGenerator
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2

def create_test_images():
    """Create sample test images to verify the HTML report image display"""
    
    print("🎨 Creating test images...")
    
    # Create screenshots directory if it doesn't exist
    screenshots_dir = "screenshots"
    if not os.path.exists(screenshots_dir):
        os.makedirs(screenshots_dir)
    
    # Create reports directory if it doesn't exist
    reports_dir = "reports"
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
    
    # Create two slightly different images to simulate screenshots
    width, height = 800, 600
    
    # Image 1 (Original)
    img1 = Image.new('RGB', (width, height), color='lightblue')
    draw1 = ImageDraw.Draw(img1)
    draw1.rectangle([100, 100, 300, 200], fill='red', outline='black', width=2)
    draw1.rectangle([400, 200, 600, 350], fill='green', outline='black', width=2)
    draw1.text((50, 50), "Original Page", fill='black')
    img1_path = os.path.join(screenshots_dir, 'test_original.png')
    img1.save(img1_path)
    
    # Image 2 (Modified - with slight differences)
    img2 = Image.new('RGB', (width, height), color='lightblue')
    draw2 = ImageDraw.Draw(img2)
    draw2.rectangle([110, 110, 310, 210], fill='darkred', outline='black', width=2)  # Slightly moved and different color
    draw2.rectangle([400, 200, 600, 350], fill='green', outline='black', width=2)
    draw2.text((50, 50), "Modified Page", fill='black')
    img2_path = os.path.join(screenshots_dir, 'test_modified.png')
    img2.save(img2_path)
    
    print(f"✅ Created test images: {img1_path}, {img2_path}")
    
    return img1_path, img2_path

def create_comparison_images(img1_path, img2_path):
    """Create side-by-side, heatmap, and visual comparison images"""
    
    print("🔧 Creating comparison images...")
    
    reports_dir = "reports"
    
    # Load images
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)
    
    if img1 is None or img2 is None:
        print("❌ Failed to load test images")
        return {}, {}
    
    # 1. Side-by-side comparison
    sidebyside = np.hstack((img1, img2))
    sidebyside_path = os.path.join(reports_dir, 'test_sidebyside_real.png')
    cv2.imwrite(sidebyside_path, sidebyside)
    
    # 2. Difference heatmap
    diff = cv2.absdiff(img1, img2)
    heatmap = cv2.applyColorMap(diff, cv2.COLORMAP_JET)
    heatmap_path = os.path.join(reports_dir, 'test_heatmap_real.png')
    cv2.imwrite(heatmap_path, heatmap)
    
    # 3. Visual comparison (overlay)
    alpha = 0.7
    overlay = cv2.addWeighted(img1, alpha, img2, 1-alpha, 0)
    visual_path = os.path.join(reports_dir, 'test_visual_real.png')
    cv2.imwrite(visual_path, overlay)
    
    print(f"✅ Created comparison images:")
    print(f"   Side-by-side: {sidebyside_path}")
    print(f"   Heatmap: {heatmap_path}")
    print(f"   Visual overlay: {visual_path}")
    
    return {
        'sidebyside': sidebyside_path,
        'heatmap': heatmap_path,
        'visual': visual_path
    }

def test_html_with_real_images():
    """Test HTML report generation with real images"""
    
    print("🧪 Testing HTML report with real images...")
    
    # Create test images
    img1_path, img2_path = create_test_images()
    
    # Create comparison images
    comparison_images = create_comparison_images(img1_path, img2_path)
    
    # Mock WCAG analysis results
    mock_wcag_analysis = {
        'url1': {
            'url': 'https://example.com/original',
            'timestamp': '2025-01-06T10:30:00',
            'wcag_version': '2.2',
            'compliance_level': 'AA',
            'total_issues': 3,
            'critical_issues': 1,
            'compliance_score': 82.3,
            'categories': {
                'perceivable': {'score': 88, 'issues': []},
                'operable': {'score': 95, 'issues': []},
                'understandable': {'score': 85, 'issues': []},
                'robust': {'score': 90, 'issues': []}
            },
            'wcag_22_features': {
                'target_size_compliant': True,
                'focus_appearance_score': 85.0,
                'dragging_alternative_score': 90.0
            }
        },
        'url2': {
            'url': 'https://example.com/modified',
            'timestamp': '2025-01-06T10:35:00',
            'wcag_version': '2.2',
            'compliance_level': 'AA',
            'total_issues': 2,
            'critical_issues': 0,
            'compliance_score': 88.7,
            'categories': {
                'perceivable': {'score': 92, 'issues': []},
                'operable': {'score': 96, 'issues': []},
                'understandable': {'score': 88, 'issues': []},
                'robust': {'score': 95, 'issues': []}
            },
            'wcag_22_features': {
                'target_size_compliant': True,
                'focus_appearance_score': 90.0,
                'dragging_alternative_score': 95.0
            }
        }
    }
    
    # Create complete mock results with real image paths
    mock_results = {
        'screenshots': {
            'url1': img1_path,
            'url2': img2_path
        },
        'comparisons': {
            'ssim': 0.923,
            'mse': 45.7,
            'pixel_diff_percentage': 8.2,
            'layout_shifts': [],
            'color_differences': [
                {'color_distance': 25.3, 'area': 850, 'position': [110, 110, 200, 100]}
            ],
            'element_changes': [],
            'missing_elements': []
        },
        'ai_analysis': {
            'anomalies': [
                {'type': 'color_shift', 'confidence': 0.87, 'location': [110, 110, 200, 100]}
            ],
            'confidence': 0.87
        },
        'summary': {
            'similarity_score': 0.923,
            'layout_differences': 0,
            'color_differences': 1
        },
        'wcag_analysis': mock_wcag_analysis,
        'reports': {
            'html': 'test_report_with_images.html',
            'pdf': 'test_report_with_images.pdf',
            'json': 'test_report_with_images.json',
            'visual': comparison_images.get('visual', ''),
            'sidebyside': comparison_images.get('sidebyside', ''),
            'heatmap': comparison_images.get('heatmap', ''),
            'package': 'test_package_with_images.zip'
        }
    }
    
    mock_config = {
        'url1': 'https://example.com/original',
        'url2': 'https://example.com/modified',
        'browser': 'chrome',
        'resolution': '800x600',
        'layout_shift': True,
        'font_color': True,
        'ai_analysis': True,
        'wcag_analysis': True
    }
    
    # Generate the HTML report
    generator = ReportGenerator()
    
    try:
        html_output = "test_report_with_real_images.html"
        generator.generate_enhanced_html_report(mock_results, mock_config, html_output)
        
        if os.path.exists(html_output):
            print(f"✅ HTML report with real images generated: {html_output}")
            
            # Verify the content
            with open(html_output, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if images are properly referenced
            checks = [
                ('Side-by-side image', 'test_sidebyside_real.png' in content),
                ('Heatmap image', 'test_heatmap_real.png' in content),
                ('Visual comparison image', 'test_visual_real.png' in content),
                ('WCAG section', '♿ WCAG Accessibility Compliance Analysis' in content),
                ('No broken image placeholders', 'Image will be available after running' not in content)
            ]
            
            print("🔍 Verification results:")
            all_passed = True
            for check_name, passed in checks:
                status = "✅" if passed else "❌"
                print(f"   {status} {check_name}")
                if not passed:
                    all_passed = False
            
            if all_passed:
                print("\n🎉 All image tests passed! Visual comparison screenshots are working correctly.")
                
                # Show file sizes to confirm images were generated
                print(f"\n📊 Generated file sizes:")
                for image_type, image_path in comparison_images.items():
                    if os.path.exists(image_path):
                        size = os.path.getsize(image_path)
                        print(f"   {image_type}: {size} bytes")
                
                return True
            else:
                print("\n❌ Some tests failed.")
                return False
        else:
            print(f"❌ HTML report was not created: {html_output}")
            return False
            
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_html_with_real_images()
    if success:
        print("\n✅ Visual comparison screenshots fix is working correctly!")
    else:
        print("\n❌ There are still issues with the visual comparison screenshots.")
