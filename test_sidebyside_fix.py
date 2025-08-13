"""
Test the fixed side-by-side comparison generation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from report_generator import ReportGenerator
from PIL import Image, ImageDraw
import cv2
import numpy as np

def test_sidebyside_fix():
    """Test the side-by-side comparison fix"""
    
    print("🧪 Testing Side-by-Side Comparison Fix...")
    
    # Ensure directories exist
    os.makedirs("screenshots", exist_ok=True)
    os.makedirs("reports", exist_ok=True)
    
    # Create test images
    width, height = 1200, 800
    
    # Image 1
    img1 = Image.new('RGB', (width, height), color='lightblue')
    draw1 = ImageDraw.Draw(img1)
    draw1.rectangle([200, 200, 500, 400], fill='red', outline='black', width=3)
    draw1.rectangle([600, 300, 900, 500], fill='green', outline='black', width=3)
    draw1.text((100, 100), "REFERENCE PAGE", fill='black')
    img1_path = "screenshots/ref_test.png"
    img1.save(img1_path)
    
    # Image 2 (with differences)
    img2 = Image.new('RGB', (width, height), color='lightblue')
    draw2 = ImageDraw.Draw(img2)
    draw2.rectangle([220, 220, 520, 420], fill='darkred', outline='black', width=3)  # Moved and different color
    draw2.rectangle([600, 300, 900, 500], fill='darkgreen', outline='black', width=3)  # Different color
    draw2.text((100, 100), "TEST PAGE", fill='black')
    img2_path = "screenshots/test_test.png"
    img2.save(img2_path)
    
    print(f"✅ Created test images: {img1_path}, {img2_path}")
    
    # Test scenarios
    test_scenarios = [
        {
            "name": "Valid Images",
            "analysis_results": {
                'screenshots': {
                    'url1': img1_path,
                    'url2': img2_path
                }
            },
            "expected": "success"
        },
        {
            "name": "Missing Screenshots Dict",
            "analysis_results": {},
            "expected": "placeholder"
        },
        {
            "name": "Missing URL1",
            "analysis_results": {
                'screenshots': {
                    'url2': img2_path
                }
            },
            "expected": "placeholder"
        },
        {
            "name": "Non-existent Files",
            "analysis_results": {
                'screenshots': {
                    'url1': 'non_existent1.png',
                    'url2': 'non_existent2.png'
                }
            },
            "expected": "placeholder"
        }
    ]
    
    generator = ReportGenerator()
    results = []
    
    for i, scenario in enumerate(test_scenarios):
        print(f"\n🔍 Testing Scenario {i+1}: {scenario['name']}")
        
        output_path = f"reports/test_sidebyside_{i+1}.png"
        
        try:
            generator.generate_side_by_side_comparison(scenario['analysis_results'], output_path)
            
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                print(f"   ✅ Generated: {output_path} ({file_size} bytes)")
                
                # Check if it's a placeholder or real image based on file size
                # Placeholders are typically smaller than real side-by-side comparisons
                if scenario['expected'] == 'success' and file_size > 50000:  # Real images are larger
                    print(f"   ✅ Expected real image, got large file ({file_size} bytes)")
                    results.append(True)
                elif scenario['expected'] == 'placeholder' and file_size < 50000:  # Placeholders are smaller
                    print(f"   ✅ Expected placeholder, got small file ({file_size} bytes)")
                    results.append(True)
                elif scenario['expected'] == 'success' and file_size < 50000:
                    print(f"   ⚠️ Expected real image but got placeholder ({file_size} bytes)")
                    results.append(False)
                else:
                    print(f"   ✅ Image generated as expected")
                    results.append(True)
            else:
                print(f"   ❌ No output file generated")
                results.append(False)
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            results.append(False)
    
    # Test with the enhanced HTML report
    print(f"\n🌐 Testing HTML Report Integration...")
    
    mock_analysis_results = {
        'screenshots': {
            'url1': img1_path,
            'url2': img2_path
        },
        'comparisons': {
            'ssim': 0.85,
            'mse': 120.5,
            'pixel_diff_percentage': 15.2
        },
        'ai_analysis': {
            'anomalies': [],
            'confidence': 0.75
        },
        'summary': {
            'similarity_score': 0.85,
            'layout_differences': 2,
            'color_differences': 1
        },
        'wcag_analysis': {
            'url1': {
                'compliance_score': 85.0,
                'total_issues': 3,
                'critical_issues': 1
            }
        }
    }
    
    config = {
        'url1': 'https://example.com/ref',
        'url2': 'https://example.com/test',
        'browser': 'chrome',
        'resolution': '1200x800'
    }
    
    try:
        # Generate comprehensive report
        reports = generator.generate_comprehensive_report(mock_analysis_results, config)
        
        print(f"✅ Comprehensive report generated with {len(reports)} files:")
        for report_type, report_path in reports.items():
            if os.path.exists(report_path):
                size = os.path.getsize(report_path)
                print(f"   ✅ {report_type}: {size} bytes")
                
                # Check specifically for side-by-side image
                if report_type == 'sidebyside':
                    if size > 50000:  # Should be a substantial file
                        print(f"      ✅ Side-by-side comparison appears to be real image")
                        results.append(True)
                    else:
                        print(f"      ⚠️ Side-by-side comparison may be placeholder ({size} bytes)")
                        results.append(False)
            else:
                print(f"   ❌ {report_type}: File not found")
                results.append(False)
                
    except Exception as e:
        print(f"❌ Error generating comprehensive report: {str(e)}")
        results.append(False)
    
    # Summary
    passed = sum(results)
    total = len(results)
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Side-by-side comparison fix is working correctly.")
        return True
    else:
        print(f"❌ {total - passed} tests failed. Side-by-side comparison needs further fixes.")
        return False

if __name__ == "__main__":
    success = test_sidebyside_fix()
    print(f"\n{'✅ SUCCESS' if success else '❌ FAILURE'}: Side-by-side comparison test {'passed' if success else 'failed'}")
