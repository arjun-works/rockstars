"""
Test script to reproduce and verify the 'status' error fix
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from visual_ai_regression import VisualAIRegression


def test_status_error_fix():
    """Test the fix for the 'status' error"""
    print("🔧 Testing Status Error Fix")
    print("=" * 40)
    
    try:
        # Initialize the regression module
        print("📋 Initializing Visual AI Regression module...")
        regression = VisualAIRegression()
        
        # Test configuration (you can modify URLs if needed)
        config = {
            'url1': 'https://example.com',
            'url2': 'https://httpbin.org/html',
            'browser': 'chrome',
            'resolution': '1920x1080',
            'layout_shift': True,
            'font_color': True,
            'element_detection': True,
            'ai_analysis': True,
            'wcag_analysis': True  # This was causing the status error
        }
        
        print("🚀 Running analysis with WCAG testing enabled...")
        print("   (This should NOT produce a 'status' error)")
        
        def progress_callback(message):
            print(f"   {message}")
        
        # Run the analysis
        results = regression.run_analysis(config, progress_callback)
        
        print("\n✅ SUCCESS! Analysis completed without 'status' error")
        print(f"📊 Results Summary:")
        
        # Access the summary data correctly
        analysis_results = results.get('analysis_results', {})
        summary_data = results.get('details', {})  # The details contain the summary info
        
        similarity_score = analysis_results.get('similarity_score', 0)
        layout_differences = len(analysis_results.get('layout_shifts', []))
        ai_anomalies = len(analysis_results.get('ai_analysis', {}).get('anomalies', []))
        
        print(f"   • Similarity Score: {similarity_score:.1%}")
        print(f"   • Layout Differences: {layout_differences}")
        print(f"   • AI Anomalies: {ai_anomalies}")
        
        # Check WCAG results
        wcag_analysis = results.get('analysis_results', {}).get('wcag_analysis', {})
        if wcag_analysis:
            print(f"   • WCAG Analysis: ✅ Completed successfully")
            if 'url1' in wcag_analysis:
                score1 = wcag_analysis['url1'].get('compliance_score', 0)
                print(f"     - URL1 WCAG Score: {score1:.1f}%")
            if 'url2' in wcag_analysis:
                score2 = wcag_analysis['url2'].get('compliance_score', 0)
                print(f"     - URL2 WCAG Score: {score2:.1f}%")
        else:
            print(f"   • WCAG Analysis: ❌ Not found in results")
        
        print(f"\n🎉 Status error has been RESOLVED!")
        return True
        
    except Exception as e:
        error_str = str(e)
        if "'status'" in error_str:
            print(f"\n❌ Status error still exists: {error_str}")
            print("🔧 This needs additional debugging...")
            return False
        else:
            print(f"\n⚠️  Different error occurred: {error_str}")
            print("🔧 This may be a separate issue...")
            return False


if __name__ == "__main__":
    success = test_status_error_fix()
    if success:
        print("\n✅ Test PASSED - Status error has been fixed!")
    else:
        print("\n❌ Test FAILED - Status error still exists or other issues found")
        sys.exit(1)
