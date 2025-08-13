#!/usr/bin/env python3
"""
Test script to verify WCAG AA-only compliance analysis
"""

import os
import sys

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from wcag_checker import WCAGCompliantChecker
from report_generator import ReportGenerator

def test_wcag_aa_only():
    """Test that WCAG analysis only returns AA or Non-compliant levels"""
    
    print("🧪 Testing WCAG AA-Only Compliance Analysis")
    print("=" * 50)
    
    # Test compliance level determination
    checker = WCAGCompliantChecker()
    
    # Test different scores and their compliance levels
    test_scores = [95, 90, 85, 80, 75, 70, 65, 50, 30]
    
    print("📊 Testing compliance level determination:")
    
    for score in test_scores:
        # Simulate score calculation
        checker.compliance_score = score
        checker.wcag_results = {
            'compliance_score': score,
            'categories': {
                'perceivable': {'score': score, 'issues': []},
                'operable': {'score': score, 'issues': []},
                'understandable': {'score': score, 'issues': []},
                'robust': {'score': score, 'issues': []}
            },
            'critical_issues': 0,
            'total_issues': 0
        }
        
        # Calculate compliance level
        checker._calculate_compliance_score()
        level = checker.wcag_results['compliance_level']
        
        print(f"  Score {score}%: {level}")
        
        # Verify only AA or Non-compliant
        if level not in ['AA', 'Non-compliant']:
            print(f"  ❌ ERROR: Unexpected compliance level '{level}'")
            return False
    
    print("\n✅ All compliance levels are AA-only compliant!")
    
    # Test report generator status text
    print("\n📄 Testing report generator WCAG status text:")
    
    generator = ReportGenerator()
    
    for score in test_scores:
        mock_results = {
            'wcag_analysis': {
                'url1': {'compliance_score': score},
                'url2': {'compliance_score': score}
            }
        }
        
        status_text = generator._get_wcag_status_text(mock_results)
        status_class = generator._get_wcag_status_class(mock_results)
        
        print(f"  Score {score}%: {status_text} ({status_class})")
        
        # Verify status text is AA-focused
        aa_statuses = ['AA COMPLIANT', 'APPROACHING AA', 'NEEDS IMPROVEMENT', 'NON-COMPLIANT']
        if status_text not in aa_statuses:
            print(f"  ❌ ERROR: Unexpected status text '{status_text}'")
            return False
    
    print("\n✅ All status texts are AA-focused!")
    
    # Test badge class for compliance levels
    print("\n🏷️  Testing compliance badge classes:")
    
    test_levels = ['AA', 'Non-compliant', 'aa', 'non-compliant', '', None]
    
    for level in test_levels:
        badge_class = generator._get_compliance_badge_class(level)
        print(f"  Level '{level}': {badge_class}")
        
        # Verify only pass or fail classes
        if badge_class not in ['status-pass', 'status-fail']:
            print(f"  ❌ ERROR: Unexpected badge class '{badge_class}'")
            return False
    
    print("\n✅ All badge classes are AA-only compliant!")
    
    return True

if __name__ == "__main__":
    print("🔧 WCAG AA-Only Compliance Test")
    print("=" * 35)
    
    success = test_wcag_aa_only()
    
    if success:
        print("\n🎉 TEST PASSED! WCAG analysis now uses AA standard only!")
        print("\n📋 Summary of changes:")
        print("  ✅ Compliance levels: Only 'AA' or 'Non-compliant'")
        print("  ✅ Status text: AA-focused descriptions")
        print("  ✅ Badge classes: Pass/fail based on AA threshold (85%)")
        print("  ✅ Removed AAA target size requirements")
        print("  ✅ Simplified compliance determination")
    else:
        print("\n⚠️  TEST FAILED! Check output above for details.")
    
    exit(0 if success else 1)
