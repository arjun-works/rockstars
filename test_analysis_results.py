#!/usr/bin/env python3
"""
Test Analysis Results Generation
This script tests the actual analysis to see what results are being generated
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from visual_ai_regression import VisualAIRegression

def test_analysis_results():
    """Test the analysis with sample URLs to see what results are generated"""
    print("=" * 60)
    print("Testing Analysis Results Generation")
    print("=" * 60)
    
    # Create analysis tool
    tool = VisualAIRegression()
    
    # Sample configuration
    config = {
        'url1': 'https://example.com',
        'url2': 'https://httpbin.org/html',  # Different URL for comparison
        'browser': 'chrome',
        'layout_shift': True,
        'font_color': True,
        'element_detection': True,
        'ai_analysis': True,
        'wcag_analysis': True
    }
    
    print("Configuration:")
    for key, value in config.items():
        print(f"  {key}: {value}")
    
    try:
        print("\n" + "=" * 40)
        print("Starting Analysis...")
        print("=" * 40)
        
        # Run analysis
        results = tool.run_analysis(config)
        
        print("\n" + "=" * 40)
        print("Analysis Results Structure:")
        print("=" * 40)
        
        # Check what's in the results
        if isinstance(results, dict):
            print(f"Results type: {type(results)}")
            print(f"Main keys: {list(results.keys())}")
            
            # Check summary
            if 'summary' in results:
                summary = results['summary']
                print(f"\nSummary type: {type(summary)}")
                if isinstance(summary, dict):
                    print(f"Summary keys: {list(summary.keys())}")
                    for key, value in summary.items():
                        print(f"  {key}: {value}")
                else:
                    print(f"Summary content: {summary}")
            
            # Check individual analysis results
            analysis_types = ['layout_shifts', 'color_differences', 'missing_elements', 
                            'new_elements', 'overlapping_elements', 'ai_analysis', 'wcag_analysis']
            
            for analysis_type in analysis_types:
                if analysis_type in results:
                    data = results[analysis_type]
                    print(f"\n{analysis_type}: {type(data)} - {len(data) if isinstance(data, (list, dict)) else 'N/A'} items")
                    if isinstance(data, dict) and data:
                        print(f"  Keys: {list(data.keys())}")
                    elif isinstance(data, list) and data:
                        print(f"  Sample item: {data[0] if data else 'Empty'}")
                else:
                    print(f"\n{analysis_type}: NOT FOUND")
            
            # Check analysis_results structure
            if 'analysis_results' in results:
                analysis_results = results['analysis_results']
                print(f"\n*** ANALYSIS_RESULTS STRUCTURE ***")
                print(f"Type: {type(analysis_results)}")
                if isinstance(analysis_results, dict):
                    print(f"Keys: {list(analysis_results.keys())}")
                    
                    # Check each analysis type in analysis_results
                    for analysis_type in analysis_types:
                        if analysis_type in analysis_results:
                            data = analysis_results[analysis_type]
                            print(f"\nanalysis_results['{analysis_type}']: {type(data)} - {len(data) if isinstance(data, (list, dict)) else 'N/A'} items")
                            if isinstance(data, dict) and data:
                                print(f"  Keys: {list(data.keys())}")
                            elif isinstance(data, list) and data:
                                print(f"  Sample items: {data[:2] if len(data) >= 2 else data}")
                        else:
                            print(f"\nanalysis_results['{analysis_type}']: NOT FOUND")
            else:
                print(f"\n*** ANALYSIS_RESULTS: NOT FOUND ***")
                
            # Check reports
            if 'reports' in results:
                reports = results['reports']
                print(f"\nReports: {list(reports.keys()) if isinstance(reports, dict) else reports}")
                
        else:
            print(f"Unexpected results type: {type(results)}")
            print(f"Results content: {results}")
            
    except Exception as e:
        print(f"Error during analysis: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("Test Completed")
    print("=" * 60)

if __name__ == "__main__":
    test_analysis_results()
