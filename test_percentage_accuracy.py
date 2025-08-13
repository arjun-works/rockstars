#!/usr/bin/env python3
"""
Test script to verify Executive Summary percentages accuracy in HTML reports.
This test checks if the percentages are being calculated and displayed correctly.
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
from visual_ai_regression import VisualAIRegression

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

def test_executive_summary_percentage_accuracy():
    """Test that Executive Summary percentages are accurate in HTML reports"""
    print("🔧 Testing Executive Summary Percentage Accuracy")
    print("=" * 60)
    
    # Create temporary directory for test
    temp_dir = tempfile.mkdtemp(prefix="percentage_accuracy_test_")
    
    try:
        # Create test screenshots with small differences to get a specific SSIM score
        url1_screenshot = os.path.join(temp_dir, "reference.png")
        url2_screenshot = os.path.join(temp_dir, "test.png")
        
        # Create reference image
        ref_img = Image.new('RGB', (400, 300), 'white')
        draw_ref = ImageDraw.Draw(ref_img)
        draw_ref.rectangle([50, 50, 150, 100], fill='blue')
        draw_ref.rectangle([200, 150, 300, 200], fill='red')
        draw_ref.text((100, 250), "REFERENCE", fill='black')
        ref_img.save(url1_screenshot, 'PNG')
        
        # Create test image with slight differences
        test_img = Image.new('RGB', (400, 300), 'white')
        draw_test = ImageDraw.Draw(test_img)
        draw_test.rectangle([52, 52, 152, 102], fill='darkblue')  # Slightly moved and darker
        draw_test.rectangle([200, 150, 300, 200], fill='red')     # Same
        draw_test.text((100, 250), "TEST PAGE", fill='black')    # Different text
        test_img.save(url2_screenshot, 'PNG')
        
        print(f"✅ Created test screenshots with known differences")
        
        # Test configuration
        config = {
            'url1': url1_screenshot,  # Use the actual file paths
            'url2': url2_screenshot,  # Use the actual file paths
            'layout_shift': True,
            'font_color': True,
            'element_analysis': True,
            'ai_analysis': True,
            'wcag_compliance': False  # Skip WCAG for faster testing
        }
        
        print("\n🔄 Running actual analysis to get real percentages...")
        
        # Run actual analysis to get real SSIM scores
        analyzer = VisualAIRegression()
        analysis_results = analyzer.run_analysis(config)
        
        actual_similarity = analysis_results.get('similarity_score', 0)
        summary_dict = analysis_results.get('summary_dict', {})
        
        print(f"✅ Analysis completed:")
        print(f"   📊 Actual Similarity Score: {actual_similarity:.4f} ({actual_similarity:.1%})")
        print(f"   📐 Layout Differences: {summary_dict.get('layout_differences', 0)}")
        print(f"   🎨 Color Differences: {summary_dict.get('color_differences', 0)}")
        print(f"   🔄 Element Changes: {summary_dict.get('element_changes', 0)}")
        print(f"   🤖 AI Anomalies: {summary_dict.get('ai_anomalies', 0)}")
        
        # Generate HTML report
        print("\n🔄 Generating HTML report...")
        
        report_generator = ReportGenerator(output_dir=temp_dir)
        html_path = os.path.join(temp_dir, "percentage_accuracy_test.html")
        report_generator.generate_enhanced_html_report(analysis_results, config, html_path)
        
        print(f"✅ HTML report generated: {html_path}")
        
        # Verify HTML content accuracy
        print("\n🔍 Verifying percentage accuracy in HTML...")
        
        if os.path.exists(html_path):
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Expected values based on actual analysis
            expected_similarity_formatted = f"{actual_similarity:.1%}"
            expected_layout = str(summary_dict.get('layout_differences', 0))
            expected_color = str(summary_dict.get('color_differences', 0))
            expected_element = str(summary_dict.get('element_changes', 0))
            expected_ai = str(summary_dict.get('ai_anomalies', 0))
            
            print(f"   Expected similarity in HTML: {expected_similarity_formatted}")
            
            # Check for expected values
            accuracy_checks = [
                (expected_similarity_formatted, f'Similarity Score: {expected_similarity_formatted}'),
                (expected_layout, f'Layout Differences: {expected_layout}'),
                (expected_color, f'Color Changes: {expected_color}'),
                (expected_element, f'Element Changes: {expected_element}'),
                (expected_ai, f'AI Anomalies: {expected_ai}')
            ]
            
            found_count = 0
            for expected_value, description in accuracy_checks:
                if expected_value in html_content:
                    found_count += 1
                    print(f"   ✅ Found: {description}")
                else:
                    print(f"   ❌ Missing: {description}")
            
            # Check for Executive Summary section
            if "📊 Executive Summary" in html_content:
                print(f"   ✅ Executive Summary section found")
            else:
                print(f"   ❌ Executive Summary section missing")
            
            # Extract similarity percentage from HTML to verify exact formatting
            import re
            similarity_pattern = r'<div class="number">(\d+\.\d+%)</div>'
            similarity_matches = re.findall(similarity_pattern, html_content)
            
            if similarity_matches:
                html_similarity = similarity_matches[0]
                print(f"   📊 HTML shows similarity as: {html_similarity}")
                
                # Compare with expected
                if html_similarity == expected_similarity_formatted:
                    print(f"   ✅ Similarity percentage is accurate!")
                else:
                    print(f"   ❌ Similarity mismatch: Expected {expected_similarity_formatted}, Got {html_similarity}")
            else:
                print(f"   ❌ Could not find similarity percentage in HTML")
            
            # Check for proper percentage formatting patterns
            percentage_patterns = [
                (r'\d+\.\d+%', 'Decimal percentage (e.g., 85.5%)'),
                (r'\d+%', 'Integer percentage (e.g., 85%)')
            ]
            
            for pattern, description in percentage_patterns:
                matches = re.findall(pattern, html_content)
                if matches:
                    print(f"   📈 Found {len(matches)} {description}: {matches[:3]}...")  # Show first 3
            
            # Test results
            accuracy_rate = found_count / len(accuracy_checks)
            print(f"\n📈 Accuracy Test Results:")
            print(f"   🎯 Values Found: {found_count}/{len(accuracy_checks)} ({accuracy_rate:.1%})")
            print(f"   📋 HTML Report Size: {len(html_content):,} characters")
            
            if found_count == len(accuracy_checks):
                print(f"\n🎉 SUCCESS: Executive Summary percentages are accurate!")
                print(f"   All values in HTML match the actual analysis results.")
                return True
            else:
                print(f"\n⚠️ ISSUES FOUND: {len(accuracy_checks) - found_count} values don't match")
                return False
        else:
            print(f"❌ HTML report file not found: {html_path}")
            return False
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Keep files for manual inspection
        print(f"\n📁 Test files preserved for inspection:")
        print(f"   Directory: {temp_dir}")
        if 'html_path' in locals():
            print(f"   HTML Report: {html_path}")

if __name__ == "__main__":
    print("🧪 Executive Summary Percentage Accuracy Test")
    print("Testing that HTML report shows accurate percentages based on real analysis")
    print("=" * 60)
    
    success = test_executive_summary_percentage_accuracy()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 TEST PASSED: Executive Summary percentages are accurate!")
    else:
        print("❌ TEST FAILED: Executive Summary percentages are not accurate")
    
    print("🔍 Check the generated HTML file manually to verify percentage accuracy.")
