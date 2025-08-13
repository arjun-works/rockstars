#!/usr/bin/env python3
"""
Test script to verify that the 0 results fix is working properly.
This script will run a visual regression analysis and print the actual values
to help diagnose why similarity, layout, color, and AI anomalies show 0.
"""

import os
import sys
import logging
from datetime import datetime

# Add current directory to path for local imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from visual_ai_regression import VisualAIRegression

def test_zero_results_fix():
    """Test the fix for zero results display"""
    print("=" * 60)
    print("TESTING ZERO RESULTS FIX")
    print("=" * 60)
    
    # Test configuration with different URLs to ensure some differences
    config = {
        'url1': 'https://httpbin.org/html',  # Simple HTML page
        'url2': 'https://httpbin.org/json',  # JSON response page - should be different
        'browser': 'chrome',
        'resolution': '1280x720',  # Smaller resolution for faster testing
        'layout_shift': True,
        'font_color': True, 
        'element_detection': True,
        'ai_analysis': True,
        'wcag_analysis': False  # Disable WCAG for faster testing
    }
    
    print(f"Testing with URLs:")
    print(f"  URL 1: {config['url1']}")
    print(f"  URL 2: {config['url2']}")
    print()
    
    # Setup logging to see detailed output
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    try:
        # Initialize regression tester
        regression = VisualAIRegression()
        
        def progress_callback(message):
            print(f"🔄 {message}")
        
        # Run analysis
        print("Starting analysis...")
        results = regression.run_analysis(config, progress_callback)
        
        print("\n" + "=" * 60)
        print("ANALYSIS COMPLETED - EXAMINING RESULTS")
        print("=" * 60)
        
        # Check analysis results directly
        analysis_results = results.get('analysis_results', {})
        summary_dict = results.get('summary_dict', {})
        
        print("\n📊 STRUCTURED SUMMARY DATA:")
        if summary_dict:
            print(f"  Similarity Score: {summary_dict.get('similarity_score', 'MISSING'):.1%}")
            print(f"  Layout Differences: {summary_dict.get('layout_differences', 'MISSING')}")
            print(f"  Color Changes: {summary_dict.get('color_differences', 'MISSING')}")
            print(f"  AI Anomalies: {summary_dict.get('ai_anomalies', 'MISSING')}")
            print(f"  Status: {summary_dict.get('status', 'MISSING')}")
        else:
            print("  ❌ No structured summary data found!")
        
        print("\n🔍 RAW ANALYSIS RESULTS:")
        print(f"  Similarity Score: {analysis_results.get('similarity_score', 'MISSING')}")
        print(f"  Layout Shifts Count: {len(analysis_results.get('layout_shifts', []))}")
        print(f"  Color Differences Count: {len(analysis_results.get('color_differences', []))}")
        print(f"  Missing Elements Count: {len(analysis_results.get('missing_elements', []))}")
        print(f"  New Elements Count: {len(analysis_results.get('new_elements', []))}")
        print(f"  Overlapping Elements Count: {len(analysis_results.get('overlapping_elements', []))}")
        
        # Check AI analysis
        ai_analysis = analysis_results.get('ai_analysis', {})
        if ai_analysis:
            print(f"  AI Anomaly Detected: {ai_analysis.get('anomaly_detected', 'MISSING')}")
            print(f"  AI Feature Distance: {ai_analysis.get('feature_distance', 'MISSING')}")
            print(f"  AI Confidence: {ai_analysis.get('confidence', 'MISSING')}")
            if 'semantic_analysis' in ai_analysis:
                semantic = ai_analysis['semantic_analysis']
                print(f"  Semantic Layout Changes: {len(semantic.get('layout_changes', []))}")
                print(f"  Semantic Content Changes: {len(semantic.get('content_changes', []))}")
                print(f"  Semantic Style Changes: {len(semantic.get('style_changes', []))}")
                print(f"  Semantic Structural Changes: {len(semantic.get('structural_changes', []))}")
        else:
            print("  ❌ No AI analysis results found!")
        
        print("\n📄 TEXT SUMMARY:")
        text_summary = results.get('summary', '')
        if text_summary:
            print(f"  {text_summary}")
        else:
            print("  ❌ No text summary found!")
        
        # Check if images were actually different
        print("\n🖼️ IMAGE ANALYSIS:")
        if 'screenshots' in analysis_results:
            screenshots = analysis_results['screenshots']
            print(f"  Screenshot 1: {screenshots.get('url1', 'MISSING')}")
            print(f"  Screenshot 2: {screenshots.get('url2', 'MISSING')}")
            
            # Check if files exist and get their sizes
            for name, path in screenshots.items():
                if path and os.path.exists(path):
                    size = os.path.getsize(path)
                    print(f"  {name} file size: {size} bytes")
                else:
                    print(f"  {name} file: NOT FOUND")
        
        print("\n✅ Test completed successfully!")
        
        # Provide diagnosis
        print("\n🩺 DIAGNOSIS:")
        similarity = analysis_results.get('similarity_score', 0)
        if similarity > 0.99:
            print("  ⚠️  Very high similarity detected - images might be identical or very similar")
            print("  💡 Try testing with more visually different URLs")
        elif similarity == 0:
            print("  ❌ Similarity score is 0 - there may be an issue with image comparison")
        else:
            print(f"  ✅ Normal similarity score detected: {similarity:.1%}")
        
        layout_count = len(analysis_results.get('layout_shifts', []))
        color_count = len(analysis_results.get('color_differences', []))
        
        if layout_count == 0 and color_count == 0:
            print("  ⚠️  No layout or color differences detected")
            print("  💡 This could be expected if the pages are very similar")
        else:
            print(f"  ✅ Differences detected: {layout_count} layout, {color_count} color")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Visual AI Regression - Zero Results Fix Test")
    print("This script tests whether the fix for 0 results display is working.")
    print()
    
    success = test_zero_results_fix()
    
    if success:
        print("\n🎉 Test completed! Check the output above for analysis results.")
    else:
        print("\n💥 Test failed! Check the error messages above.")
    
    input("\nPress Enter to exit...")
