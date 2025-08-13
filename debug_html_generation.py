#!/usr/bin/env python3
"""
Debug script to test HTML report generation and identify the exact issue.
"""

import os
import sys
from datetime import datetime

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from report_generator import ReportGenerator

def debug_html_generation():
    """Debug the HTML generation process"""
    print("🐛 Debugging HTML Report Generation...")
    
    # Create minimal test data
    analysis_results = {
        'screenshots': {
            'url1': 'test_url1.png',
            'url2': 'test_url2.png'
        },
        'reports': {
            'sidebyside': 'test_sidebyside.png',
            'heatmap': 'test_heatmap.png',
            'visual': 'test_visual.png'
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
            'url1_score': 92.5,
            'url2_score': 90.0
        },
        'summary_dict': {
            'similarity_score': 85,
            'layout_differences': 4,
            'color_differences': 583,
            'ai_anomalies': 0
        },
        'duration': '45 seconds'
    }
    
    config = {
        'url1': 'https://example.com',
        'url2': 'https://httpbin.org/html',
        'viewport_width': 1920,
        'viewport_height': 1080
    }
    
    try:
        report_generator = ReportGenerator(output_dir="debug_reports")
        
        # Test each step individually
        print("📋 Testing pre-generation steps...")
        
        # Test image HTML generation
        print("🖼️ Testing image HTML generation...")
        url1_html = report_generator._generate_image_html(analysis_results, 'url1_screenshot', 'Original screenshot')
        print(f"   URL1 HTML: {url1_html[:100]}..." if len(url1_html) > 100 else f"   URL1 HTML: {url1_html}")
        
        # Test section generation
        print("📊 Testing section HTML generation...")
        try:
            analysis_sections_html = report_generator._generate_analysis_sections_html(analysis_results, analysis_results.get('ai_analysis', {}), config)
            print(f"   Analysis sections: {len(analysis_sections_html)} characters")
        except Exception as e:
            print(f"   ❌ Analysis sections error: {e}")
        
        try:
            wcag_section_html = report_generator._generate_wcag_section_html(analysis_results, config)
            print(f"   WCAG section: {len(wcag_section_html)} characters")
        except Exception as e:
            print(f"   ❌ WCAG section error: {e}")
        
        # Test full report generation
        print("📝 Testing full HTML report generation...")
        output_path = "debug_reports/debug_test_report.html"
        report_generator.generate_enhanced_html_report(analysis_results, config, output_path)
        
        if os.path.exists(output_path):
            print(f"✅ Report generated successfully: {output_path}")
            
            # Check content
            with open(output_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print(f"📏 Report size: {len(content)} characters")
            
            # Check for key elements
            checks = {
                'Tab buttons': 'tab-button' in content,
                'Visual Comparison tab': 'visual-comparison' in content,
                'OpenImage function': 'openImage' in content,
                'Image tags': '<img' in content,
                'Tab panels': 'tab-panel' in content
            }
            
            print("🔍 Content checks:")
            for check, passed in checks.items():
                status = "✅" if passed else "❌"
                print(f"   {status} {check}")
            
            # If there are issues, save a minimal working example
            if not all(checks.values()):
                print("🔧 Creating minimal working example...")
                minimal_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Test Image Click</title>
    <style>
        .test-image { max-width: 300px; cursor: pointer; border: 2px solid blue; }
    </style>
</head>
<body>
    <h1>Test Image Click</h1>
    <img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICA8cmVjdCB3aWR0aD0iMzAwIiBoZWlnaHQ9IjIwMCIgZmlsbD0iIzAwN2JmZiIvPgogIDx0ZXh0IHg9IjE1MCIgeT0iMTA1IiBmb250LWZhbWlseT0iQXJpYWwsIHNhbnMtc2VyaWYiIGZvbnQtc2l6ZT0iMjAiIGZpbGw9IndoaXRlIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj5DbGljayBNZTwvdGV4dD4KICA8L3N2Zz4K"
         class="test-image" onclick="openImage(this.src)" alt="Test Image">
    
    <script>
        function openImage(src) {
            alert('Image click works! URL: ' + src);
            console.log('openImage called with:', src);
        }
    </script>
</body>
</html>
"""
                minimal_path = "debug_reports/minimal_test.html"
                with open(minimal_path, 'w', encoding='utf-8') as f:
                    f.write(minimal_html)
                print(f"💡 Created minimal test: {minimal_path}")
            
            return output_path
            
        else:
            print("❌ Report generation failed - file not created")
            return None
            
    except Exception as e:
        print(f"❌ Error during generation: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Main debug function"""
    print("🚀 Starting HTML Generation Debug")
    print("=" * 50)
    
    result = debug_html_generation()
    
    print("\n" + "=" * 50)
    if result:
        print(f"✅ Debug completed. Check: {result}")
    else:
        print("❌ Debug failed. Check the error messages above.")

if __name__ == "__main__":
    main()
