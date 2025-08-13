"""
Test the PDF and JSON export links fix in HTML reports
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from report_generator import ReportGenerator
from PIL import Image, ImageDraw

def test_export_links_fix():
    """Test that PDF and JSON export links work correctly in HTML reports"""
    
    print("🧪 Testing PDF and JSON Export Links Fix...")
    
    # Ensure directories exist
    os.makedirs("screenshots", exist_ok=True)
    os.makedirs("reports", exist_ok=True)
    
    # Create test images
    print("📸 Creating test screenshots...")
    width, height = 800, 600
    
    # Image 1
    img1 = Image.new('RGB', (width, height), color='lightcyan')
    draw1 = ImageDraw.Draw(img1)
    draw1.rectangle([150, 150, 350, 250], fill='blue', outline='black', width=2)
    draw1.text((50, 50), "Reference Page", fill='black')
    img1_path = "screenshots/export_test_ref.png"
    img1.save(img1_path)
    
    # Image 2
    img2 = Image.new('RGB', (width, height), color='lightcyan')
    draw2 = ImageDraw.Draw(img2)
    draw2.rectangle([170, 170, 370, 270], fill='darkblue', outline='black', width=2)  # Slightly different
    draw2.text((50, 50), "Test Page", fill='black')
    img2_path = "screenshots/export_test_test.png"
    img2.save(img2_path)
    
    print(f"✅ Created test images: {img1_path}, {img2_path}")
    
    # Create comprehensive test data
    mock_analysis_results = {
        'screenshots': {
            'url1': img1_path,
            'url2': img2_path
        },
        'comparisons': {
            'ssim': 0.92,
            'mse': 65.3,
            'pixel_diff_percentage': 5.8,
            'layout_shifts': [],
            'color_differences': [
                {'color_distance': 15.2, 'area': 400, 'position': [170, 170, 200, 100]}
            ],
            'element_changes': [],
            'missing_elements': []
        },
        'ai_analysis': {
            'anomalies': [
                {'type': 'minor_shift', 'confidence': 0.82, 'location': [170, 170, 200, 100]}
            ],
            'confidence': 0.82
        },
        'summary': {
            'similarity_score': 0.92,
            'layout_differences': 0,
            'color_differences': 1
        },
        'wcag_analysis': {
            'url1': {
                'url': 'https://example.com/reference',
                'compliance_score': 88.5,
                'total_issues': 2,
                'critical_issues': 0,
                'compliance_level': 'AA'
            },
            'url2': {
                'url': 'https://example.com/test',
                'compliance_score': 91.2,
                'total_issues': 1,
                'critical_issues': 0,
                'compliance_level': 'AA'
            }
        }
    }
    
    config = {
        'url1': 'https://example.com/reference',
        'url2': 'https://example.com/test',
        'browser': 'chrome',
        'resolution': '800x600',
        'layout_shift': True,
        'font_color': True,
        'ai_analysis': True,
        'wcag_analysis': True
    }
    
    # Generate comprehensive report
    generator = ReportGenerator()
    
    try:
        print("🚀 Generating comprehensive report with fixed export links...")
        reports = generator.generate_comprehensive_report(mock_analysis_results, config)
        
        print(f"✅ Generated {len(reports)} report files:")
        
        # Check each generated file
        files_check = []
        for report_type, report_path in reports.items():
            if os.path.exists(report_path):
                file_size = os.path.getsize(report_path)
                print(f"   ✅ {report_type}: {file_size:,} bytes")
                files_check.append((report_type, report_path, file_size, True))
            else:
                print(f"   ❌ {report_type}: File not found - {report_path}")
                files_check.append((report_type, report_path, 0, False))
        
        # Check HTML report specifically for export links
        html_report = reports.get('html')
        if html_report and os.path.exists(html_report):
            print(f"\n🔍 Analyzing HTML report export links...")
            
            with open(html_report, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Check for export section
            export_checks = [
                ('Export Options section', '💾 Export Options' in html_content),
                ('PDF link present', '.pdf' in html_content and 'PDF Report' in html_content),
                ('JSON link present', '.json' in html_content and 'JSON Data' in html_content),
                ('ZIP package link', '_complete_package.zip' in html_content),
                ('File size info', 'KB' in html_content or 'MB' in html_content or 'B)' in html_content),
                ('Export note present', 'Files are generated alongside' in html_content)
            ]
            
            export_results = []
            for check_name, passed in export_checks:
                status = "✅" if passed else "❌"
                print(f"   {status} {check_name}")
                export_results.append(passed)
            
            # Check if the actual PDF and JSON files exist and can be referenced
            base_name = os.path.splitext(os.path.basename(html_report))[0]
            pdf_file = os.path.join(os.path.dirname(html_report), f"{base_name}.pdf")
            json_file = os.path.join(os.path.dirname(html_report), f"{base_name}.json")
            zip_file = os.path.join(os.path.dirname(html_report), f"{base_name}_complete_package.zip")
            
            print(f"\n📁 Checking export file accessibility:")
            file_accessibility = [
                ('PDF file exists', os.path.exists(pdf_file), pdf_file),
                ('JSON file exists', os.path.exists(json_file), json_file),
                ('ZIP package exists', os.path.exists(zip_file), zip_file)
            ]
            
            accessibility_results = []
            for check_name, exists, file_path in file_accessibility:
                if exists:
                    file_size = os.path.getsize(file_path)
                    print(f"   ✅ {check_name}: {file_size:,} bytes")
                    accessibility_results.append(True)
                else:
                    print(f"   ❌ {check_name}: Not found - {file_path}")
                    accessibility_results.append(False)
            
            # Summary
            total_checks = len(export_results) + len(accessibility_results)
            passed_checks = sum(export_results) + sum(accessibility_results)
            
            print(f"\n📊 Export Links Test Results: {passed_checks}/{total_checks} checks passed")
            
            if passed_checks == total_checks:
                print("🎉 All export link tests passed! PDF and JSON downloads should work correctly.")
                return True
            else:
                print(f"❌ {total_checks - passed_checks} tests failed. Export links may not work properly.")
                return False
        else:
            print("❌ HTML report not found or not generated")
            return False
            
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_export_links_fix()
    print(f"\n{'✅ SUCCESS' if success else '❌ FAILURE'}: Export links test {'passed' if success else 'failed'}")
