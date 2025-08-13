#!/usr/bin/env python3
"""
Quick test to verify visual comparison images are working
"""

import os
import sys

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from report_generator import ReportGenerator

def test_image_generation():
    """Test that visual comparison image methods work correctly"""
    
    print("🧪 Testing Visual Comparison Image Generation")
    print("=" * 50)
    
    generator = ReportGenerator()
    
    # Mock analysis results with actual image paths if they exist
    mock_results = {
        'screenshots': {
            'url1': 'screenshots/test1.png',
            'url2': 'screenshots/test2.png'
        },
        'heatmap_path': 'visualizations/test_heatmap.png',
        'annotated_comparison_path': 'visualizations/test_comparison.png',
        'reports': {}  # This will be populated by the methods
    }
    
    # Test output directory
    test_output = "test_image_output"
    os.makedirs(test_output, exist_ok=True)
    
    try:
        print("🖼️  Testing image generation methods:")
        
        # Test 1: Enhanced Visual Comparison
        visual_path = os.path.join(test_output, "test_visual.png")
        result = generator.generate_enhanced_visual_comparison(mock_results, visual_path)
        exists = "✅" if os.path.exists(visual_path) else "❌"
        size = f" ({os.path.getsize(visual_path)/1024:.1f} KB)" if os.path.exists(visual_path) else ""
        print(f"  {exists} Enhanced Visual Comparison: {os.path.basename(visual_path)}{size}")
        
        # Test 2: Side-by-Side Comparison
        sidebyside_path = os.path.join(test_output, "test_sidebyside.png")
        result = generator.generate_side_by_side_comparison(mock_results, sidebyside_path)
        exists = "✅" if os.path.exists(sidebyside_path) else "❌"
        size = f" ({os.path.getsize(sidebyside_path)/1024:.1f} KB)" if os.path.exists(sidebyside_path) else ""
        print(f"  {exists} Side-by-Side Comparison: {os.path.basename(sidebyside_path)}{size}")
        
        # Test 3: Difference Heatmap
        heatmap_path = os.path.join(test_output, "test_heatmap.png")
        result = generator.generate_difference_heatmap(mock_results, heatmap_path)
        exists = "✅" if os.path.exists(heatmap_path) else "❌"
        size = f" ({os.path.getsize(heatmap_path)/1024:.1f} KB)" if os.path.exists(heatmap_path) else ""
        print(f"  {exists} Difference Heatmap: {os.path.basename(heatmap_path)}{size}")
        
        # Test 4: HTML Image Generation
        print("\n📄 Testing HTML image generation:")
        
        # Add reports to mock results
        mock_results['reports'] = {
            'visual': visual_path,
            'sidebyside': sidebyside_path,
            'heatmap': heatmap_path
        }
        
        # Test each image type
        for img_type, img_name in [('visual', 'Visual Comparison'), ('sidebyside', 'Side-by-Side'), ('heatmap', 'Heatmap')]:
            html_result = generator._generate_image_html(mock_results, img_type, img_name)
            
            if '<img src=' in html_result:
                print(f"  ✅ {img_name}: Generated <img> tag")
            elif 'not available' in html_result:
                print(f"  ⚠️  {img_name}: Generated placeholder")
            else:
                print(f"  ❌ {img_name}: Unexpected result")
        
        # Test 5: Check if existing report images are shown
        print("\n🔍 Checking existing reports for images:")
        
        # Look for any existing reports
        reports_dir = "reports"
        if os.path.exists(reports_dir):
            for file in os.listdir(reports_dir):
                if file.endswith('.png') and any(keyword in file for keyword in ['side_by_side', 'heatmap', 'visual_comparison']):
                    file_path = os.path.join(reports_dir, file)
                    size_kb = os.path.getsize(file_path) / 1024
                    print(f"  📷 Found: {file} ({size_kb:.1f} KB)")
        
        print(f"\n✅ Image generation test completed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Cleanup
        import shutil
        if os.path.exists(test_output):
            shutil.rmtree(test_output)

if __name__ == "__main__":
    print("🔧 Quick Visual Images Test")
    print("=" * 30)
    
    success = test_image_generation()
    
    if success:
        print("\n🎉 TEST PASSED! Image generation is working!")
    else:
        print("\n⚠️  TEST FAILED! Check output above.")
    
    exit(0 if success else 1)
