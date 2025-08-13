#!/usr/bin/env python3
"""
Debug script to test the actual analysis flow and see the structure of analysis_results
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from visual_ai_regression import VisualAIRegression
import json

def debug_real_analysis():
    """Debug the real analysis flow to see what structure is passed to report generator"""
    print("🔍 Debugging real analysis flow...")
    
    # Create analyzer
    analyzer = VisualAIRegression()
    
    # Test config with simple URLs
    config = {
        'url1': 'https://www.google.com',
        'url2': 'https://www.bing.com',
        'layout_shift': True,
        'font_color': True,
        'element_detection': True,
        'ai_analysis': True
    }
    
    def progress_callback(message):
        print(f"📊 {message}")
    
    try:
        # Run the actual analysis
        print("🚀 Starting real analysis...")
        results = analyzer.run_analysis(config, progress_callback)
        
        print("\n🔍 Analysis Results Structure:")
        print("="*50)
        
        # Print top-level keys
        print(f"Top-level keys: {list(results.keys())}")
        
        # Check for metrics at various levels
        metrics_to_check = ['ssim', 'mse', 'psnr', 'pixel_metrics']
        
        print("\n📊 Checking metrics locations:")
        for metric in metrics_to_check:
            if metric in results:
                print(f"✅ {metric} found at top level: {results[metric]}")
            else:
                print(f"❌ {metric} NOT found at top level")
        
        # Check if metrics are in analysis_results sub-key
        if 'analysis_results' in results:
            print("\n📊 Checking metrics in analysis_results:")
            analysis_results = results['analysis_results']
            for metric in metrics_to_check:
                if metric in analysis_results:
                    print(f"✅ {metric} found in analysis_results: {analysis_results[metric]}")
                else:
                    print(f"❌ {metric} NOT found in analysis_results")
        
        # Save the structure to a file for inspection
        with open('debug_analysis_structure.json', 'w') as f:
            # Convert numpy arrays to lists for JSON serialization
            serializable_results = {}
            for key, value in results.items():
                try:
                    json.dumps(value)  # Test if serializable
                    serializable_results[key] = value
                except (TypeError, ValueError):
                    serializable_results[key] = str(value)  # Convert to string if not serializable
            
            json.dump(serializable_results, f, indent=2, default=str)
        
        print(f"\n💾 Full structure saved to debug_analysis_structure.json")
        
        # Check what's actually passed to generate_comprehensive_report
        print(f"\n🎯 What would be passed to generate_comprehensive_report:")
        if 'analysis_results' in results:
            report_data = results['analysis_results']
            print(f"Data type: {type(report_data)}")
            if isinstance(report_data, dict):
                print(f"Keys in report data: {list(report_data.keys())}")
                for metric in metrics_to_check:
                    if metric in report_data:
                        print(f"✅ {metric}: {report_data[metric]}")
                    else:
                        print(f"❌ {metric}: Missing")
        
    except Exception as e:
        print(f"❌ Error during analysis: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_real_analysis()
