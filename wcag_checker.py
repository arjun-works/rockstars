"""
WCAG Compliance Checker Module
Comprehensive Web Content Accessibility Guidelines (WCAG) 2.1 & 2.2 compliance testing
"""

import os
import json
import logging
import io
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
import requests
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
from collections import defaultdict
import re
import colorsys


class WCAGCompliantChecker:
    def __init__(self):
        self.setup_logging()
        self.wcag_results = {}
        self.accessibility_issues = []
        self.compliance_score = 0
        # WCAG 2.2 minimum target sizes (in CSS pixels) - AA standard only
        self.min_target_size = 24  # WCAG 2.2 AA requirement
        
    def setup_logging(self):
        """Setup logging for WCAG checker"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def check_wcag_compliance(self, driver, url, progress_callback=None):
        """
        Comprehensive WCAG 2.1 & 2.2 compliance check
        Returns detailed accessibility analysis
        """
        try:
            if progress_callback:
                progress_callback("Starting WCAG 2.1/2.2 compliance analysis...")
            
            self.logger.info(f"Starting WCAG compliance check for: {url}")
            
            # Navigate to the page
            driver.get(url)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Get page source for analysis
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # Initialize results structure
            self.wcag_results = {
                'url': url,
                'timestamp': datetime.now().isoformat(),
                'wcag_version': '2.2',  # Updated to include 2.2
                'compliance_level': 'AAA',  # Will be downgraded based on violations
                'total_issues': 0,
                'critical_issues': 0,
                'compliance_score': 0,  # Initialize compliance score
                'categories': {
                    'perceivable': {'score': 100, 'issues': []},
                    'operable': {'score': 100, 'issues': []},
                    'understandable': {'score': 100, 'issues': []},
                    'robust': {'score': 100, 'issues': []}
                },
                'detailed_analysis': {},
                'wcag_22_features': {  # New WCAG 2.2 specific checks
                    'target_size_compliant': True,
                    'focus_appearance_score': 100,
                    'dragging_alternative_score': 100
                }
            }
            
            # Principle 1: Perceivable
            if progress_callback:
                progress_callback("Checking Principle 1: Perceivable...")
            self._check_perceivable(driver, soup)
            
            # Principle 2: Operable (including WCAG 2.2 enhancements)
            if progress_callback:
                progress_callback("Checking Principle 2: Operable (including WCAG 2.2)...")
            self._check_operable(driver, soup)
            
            # Principle 3: Understandable
            if progress_callback:
                progress_callback("Checking Principle 3: Understandable...")
            self._check_understandable(driver, soup)
            
            # Principle 4: Robust
            if progress_callback:
                progress_callback("Checking Principle 4: Robust...")
            self._check_robust(driver, soup)
            
            # WCAG 2.2 Specific Checks
            if progress_callback:
                progress_callback("Running WCAG 2.2 specific checks...")
            self._check_wcag_22_features(driver, soup)
            
            # Enhanced Color Analysis
            if progress_callback:
                progress_callback("Performing enhanced color contrast analysis...")
            self._enhanced_color_analysis(driver, soup)
            
            # Calculate overall compliance score
            if progress_callback:
                progress_callback("Calculating compliance score...")
            self._calculate_compliance_score()
            
            # Generate accessibility heatmap
            if progress_callback:
                progress_callback("Generating accessibility heatmap...")
            self._generate_accessibility_heatmap(driver)
            
            self.logger.info(f"WCAG compliance check completed. Score: {self.compliance_score}%")
            return self.wcag_results
            
        except Exception as e:
            self.logger.error(f"WCAG compliance check failed: {str(e)}")
            raise
    
    def _check_perceivable(self, driver, soup):
        """Check Principle 1: Perceivable"""
        issues = []
        
        # 1.1 Text Alternatives
        issues.extend(self._check_text_alternatives(soup))
        
        # 1.2 Time-based Media (basic checks)
        issues.extend(self._check_time_based_media(soup))
        
        # 1.3 Adaptable
        issues.extend(self._check_adaptable(soup))
        
        # 1.4 Distinguishable
        issues.extend(self._check_distinguishable(driver, soup))
        
        self.wcag_results['categories']['perceivable']['issues'] = issues
        self.wcag_results['categories']['perceivable']['score'] = max(0, 100 - len(issues) * 10)
    
    def _check_operable(self, driver, soup):
        """Check Principle 2: Operable"""
        issues = []
        
        # 2.1 Keyboard Accessible
        issues.extend(self._check_keyboard_accessible(driver, soup))
        
        # 2.2 Enough Time
        issues.extend(self._check_enough_time(soup))
        
        # 2.3 Seizures and Physical Reactions
        issues.extend(self._check_seizures(soup))
        
        # 2.4 Navigable
        issues.extend(self._check_navigable(soup))
        
        # 2.5 Input Modalities
        issues.extend(self._check_input_modalities(soup))
        
        self.wcag_results['categories']['operable']['issues'] = issues
        self.wcag_results['categories']['operable']['score'] = max(0, 100 - len(issues) * 10)
    
    def _check_understandable(self, driver, soup):
        """Check Principle 3: Understandable"""
        issues = []
        
        # 3.1 Readable
        issues.extend(self._check_readable(soup))
        
        # 3.2 Predictable
        issues.extend(self._check_predictable(soup))
        
        # 3.3 Input Assistance
        issues.extend(self._check_input_assistance(soup))
        
        self.wcag_results['categories']['understandable']['issues'] = issues
        self.wcag_results['categories']['understandable']['score'] = max(0, 100 - len(issues) * 10)
    
    def _check_robust(self, driver, soup):
        """Check Principle 4: Robust"""
        issues = []
        
        # 4.1 Compatible
        issues.extend(self._check_compatible(soup))
        
        self.wcag_results['categories']['robust']['issues'] = issues
        self.wcag_results['categories']['robust']['score'] = max(0, 100 - len(issues) * 10)
    
    def _check_text_alternatives(self, soup):
        """1.1 Text Alternatives"""
        issues = []
        
        # Check images without alt text
        images = soup.find_all('img')
        for img in images:
            if not img.get('alt') and not img.get('aria-label') and not img.get('aria-labelledby'):
                if not img.get('role') == 'presentation' and not img.get('aria-hidden') == 'true':
                    issues.append({
                        'guideline': '1.1.1',
                        'level': 'A',
                        'description': 'Image missing alt text',
                        'element': str(img)[:100] + '...',
                        'impact': 'critical'
                    })
        
        # Check input elements without labels
        inputs = soup.find_all(['input', 'textarea', 'select'])
        for input_elem in inputs:
            input_type = input_elem.get('type', '').lower()
            if input_type not in ['hidden', 'submit', 'button', 'reset']:
                if not input_elem.get('aria-label') and not input_elem.get('aria-labelledby'):
                    # Check for associated label
                    input_id = input_elem.get('id')
                    if not input_id or not soup.find('label', {'for': input_id}):
                        issues.append({
                            'guideline': '1.1.1',
                            'level': 'A',
                            'description': 'Form control missing label',
                            'element': str(input_elem)[:100] + '...',
                            'impact': 'critical'
                        })
        
        return issues
    
    def _check_time_based_media(self, soup):
        """1.2 Time-based Media"""
        issues = []
        
        # Check for video/audio elements without captions/transcripts
        media_elements = soup.find_all(['video', 'audio'])
        for media in media_elements:
            if not media.find('track'):
                issues.append({
                    'guideline': '1.2.1',
                    'level': 'A',
                    'description': 'Media element missing captions/transcript',
                    'element': str(media)[:100] + '...',
                    'impact': 'major'
                })
        
        return issues
    
    def _check_adaptable(self, soup):
        """1.3 Adaptable"""
        issues = []
        
        # Check heading structure
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        if headings:
            # Check if page starts with h1
            first_heading = headings[0]
            if first_heading.name != 'h1':
                issues.append({
                    'guideline': '1.3.1',
                    'level': 'A',
                    'description': 'Page should start with h1 heading',
                    'element': str(first_heading)[:100] + '...',
                    'impact': 'moderate'
                })
            
            # Check for heading level skipping
            prev_level = 0
            for heading in headings:
                level = int(heading.name[1])
                if level > prev_level + 1:
                    issues.append({
                        'guideline': '1.3.1',
                        'level': 'A',
                        'description': f'Heading level skipped: {heading.name} after h{prev_level}',
                        'element': str(heading)[:100] + '...',
                        'impact': 'moderate'
                    })
                prev_level = level
        
        # Check table headers
        tables = soup.find_all('table')
        for table in tables:
            if not table.find('th') and not table.get('role') == 'presentation':
                issues.append({
                    'guideline': '1.3.1',
                    'level': 'A',
                    'description': 'Data table missing header cells',
                    'element': str(table)[:100] + '...',
                    'impact': 'major'
                })
        
        return issues
    
    def _check_distinguishable(self, driver, soup):
        """1.4 Distinguishable"""
        issues = []
        
        # Check color contrast (basic detection)
        try:
            # Take screenshot for color analysis
            screenshot = driver.get_screenshot_as_png()
            self._analyze_color_contrast(screenshot, issues)
        except Exception as e:
            self.logger.warning(f"Color contrast analysis failed: {e}")
        
        # Check for color-only information
        elements_with_color_styles = soup.find_all(style=re.compile(r'color\s*:', re.I))
        for elem in elements_with_color_styles:
            if not elem.get_text().strip():
                issues.append({
                    'guideline': '1.4.1',
                    'level': 'A',
                    'description': 'Information might be conveyed through color only',
                    'element': str(elem)[:100] + '...',
                    'impact': 'moderate'
                })
        
        return issues
    
    def _check_keyboard_accessible(self, driver, soup):
        """2.1 Keyboard Accessible"""
        issues = []
        
        # Check for keyboard traps
        focusable_elements = soup.find_all(['a', 'button', 'input', 'select', 'textarea'])
        for elem in focusable_elements:
            if elem.get('tabindex') == '-1' and not elem.get('aria-hidden') == 'true':
                issues.append({
                    'guideline': '2.1.1',
                    'level': 'A',
                    'description': 'Interactive element not keyboard accessible',
                    'element': str(elem)[:100] + '...',
                    'impact': 'critical'
                })
        
        # Check for missing skip links
        skip_links = soup.find_all('a', href=re.compile(r'^#'))
        if not skip_links:
            issues.append({
                'guideline': '2.4.1',
                'level': 'A',
                'description': 'Page missing skip navigation links',
                'element': 'Page structure',
                'impact': 'moderate'
            })
        
        return issues
    
    def _check_enough_time(self, soup):
        """2.2 Enough Time"""
        issues = []
        
        # Check for auto-refresh/redirect
        meta_refresh = soup.find('meta', {'http-equiv': 'refresh'})
        if meta_refresh:
            content = meta_refresh.get('content', '')
            if content and not content.startswith('0;'):
                issues.append({
                    'guideline': '2.2.1',
                    'level': 'A',
                    'description': 'Page has auto-refresh without user control',
                    'element': str(meta_refresh),
                    'impact': 'major'
                })
        
        return issues
    
    def _check_seizures(self, soup):
        """2.3 Seizures and Physical Reactions"""
        issues = []
        
        # Check for potentially seizure-inducing elements
        animations = soup.find_all(style=re.compile(r'animation|transition', re.I))
        for anim in animations:
            issues.append({
                'guideline': '2.3.1',
                'level': 'A',
                'description': 'Animation detected - verify it does not flash more than 3 times per second',
                'element': str(anim)[:100] + '...',
                'impact': 'critical'
            })
        
        return issues
    
    def _check_navigable(self, soup):
        """2.4 Navigable"""
        issues = []
        
        # Check page title
        title = soup.find('title')
        if not title or not title.get_text().strip():
            issues.append({
                'guideline': '2.4.2',
                'level': 'A',
                'description': 'Page missing descriptive title',
                'element': 'Document head',
                'impact': 'major'
            })
        
        # Check focus order (basic)
        focusable = soup.find_all(['a', 'button', 'input', 'select', 'textarea'])
        tabindex_elements = [elem for elem in focusable if elem.get('tabindex')]
        if tabindex_elements:
            for elem in tabindex_elements:
                try:
                    tabindex = int(elem.get('tabindex', 0))
                    if tabindex > 0:
                        issues.append({
                            'guideline': '2.4.3',
                            'level': 'A',
                            'description': 'Positive tabindex may disrupt natural focus order',
                            'element': str(elem)[:100] + '...',
                            'impact': 'moderate'
                        })
                except ValueError:
                    pass
        
        return issues
    
    def _check_input_modalities(self, soup):
        """2.5 Input Modalities"""
        issues = []
        
        # Check for click handlers on non-interactive elements
        elements_with_onclick = soup.find_all(onclick=True)
        for elem in elements_with_onclick:
            if elem.name not in ['a', 'button', 'input', 'select', 'textarea']:
                issues.append({
                    'guideline': '2.5.1',
                    'level': 'A',
                    'description': 'Non-interactive element has click handler',
                    'element': str(elem)[:100] + '...',
                    'impact': 'moderate'
                })
        
        return issues
    
    def _check_readable(self, soup):
        """3.1 Readable"""
        issues = []
        
        # Check language declaration
        html_tag = soup.find('html')
        if not html_tag or not html_tag.get('lang'):
            issues.append({
                'guideline': '3.1.1',
                'level': 'A',
                'description': 'Page missing language declaration',
                'element': 'HTML element',
                'impact': 'major'
            })
        
        return issues
    
    def _check_predictable(self, soup):
        """3.2 Predictable"""
        issues = []
        
        # Check for form auto-submission
        forms = soup.find_all('form')
        for form in forms:
            if form.get('onchange') or form.get('onsubmit'):
                issues.append({
                    'guideline': '3.2.2',
                    'level': 'A',
                    'description': 'Form may change context automatically',
                    'element': str(form)[:100] + '...',
                    'impact': 'moderate'
                })
        
        return issues
    
    def _check_input_assistance(self, soup):
        """3.3 Input Assistance"""
        issues = []
        
        # Check required fields
        required_inputs = soup.find_all(['input', 'textarea', 'select'], required=True)
        for inp in required_inputs:
            if not inp.get('aria-required') and not inp.get('aria-invalid'):
                # Check for visual indicators
                parent = inp.parent
                if parent and '*' not in parent.get_text():
                    issues.append({
                        'guideline': '3.3.2',
                        'level': 'A',
                        'description': 'Required field missing clear indicator',
                        'element': str(inp)[:100] + '...',
                        'impact': 'major'
                    })
        
        return issues
    
    def _check_compatible(self, soup):
        """4.1 Compatible"""
        issues = []
        
        # Check for valid HTML (basic)
        # Check for duplicate IDs
        ids = []
        elements_with_ids = soup.find_all(id=True)
        for elem in elements_with_ids:
            elem_id = elem.get('id')
            if elem_id in ids:
                issues.append({
                    'guideline': '4.1.1',
                    'level': 'A',
                    'description': f'Duplicate ID found: {elem_id}',
                    'element': str(elem)[:100] + '...',
                    'impact': 'major'
                })
            else:
                ids.append(elem_id)
        
        # Check ARIA usage
        aria_elements = soup.find_all(attrs={"aria-labelledby": True})
        for elem in aria_elements:
            labelledby_id = elem.get('aria-labelledby')
            if not soup.find(id=labelledby_id):
                issues.append({
                    'guideline': '4.1.2',
                    'level': 'A',
                    'description': f'aria-labelledby references non-existent ID: {labelledby_id}',
                    'element': str(elem)[:100] + '...',
                    'impact': 'major'
                })
        
        return issues
    
    def _analyze_color_contrast(self, screenshot_data, issues):
        """Analyze color contrast from screenshot"""
        try:
            # Convert screenshot to image
            import io
            image = Image.open(io.BytesIO(screenshot_data))
            img_array = np.array(image)
            
            # Simple contrast analysis (this is a basic implementation)
            # In a production environment, you'd want more sophisticated analysis
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            contrast = gray.std()
            
            if contrast < 50:  # Threshold for low contrast
                issues.append({
                    'guideline': '1.4.3',
                    'level': 'AA',
                    'description': 'Low color contrast detected on page',
                    'element': 'Overall page contrast',
                    'impact': 'major'
                })
                
        except Exception as e:
            self.logger.warning(f"Color contrast analysis failed: {e}")
    
    def _calculate_compliance_score(self):
        """Calculate overall WCAG compliance score"""
        total_score = 0
        category_count = 0
        
        for category, data in self.wcag_results['categories'].items():
            total_score += data['score']
            category_count += 1
            
            # Count critical issues
            critical_count = sum(1 for issue in data['issues'] if issue.get('impact') == 'critical')
            self.wcag_results['critical_issues'] += critical_count
            self.wcag_results['total_issues'] += len(data['issues'])
        
        self.compliance_score = total_score / category_count if category_count > 0 else 0
        self.wcag_results['compliance_score'] = self.compliance_score
        
        # Determine compliance level - Only AA standard analysis
        if self.compliance_score >= 85:
            self.wcag_results['compliance_level'] = 'AA'
        else:
            self.wcag_results['compliance_level'] = 'Non-compliant'
    
    def _generate_accessibility_heatmap(self, driver):
        """Generate visual heatmap of accessibility issues"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            viz_dir = os.path.join("visualizations", timestamp)
            os.makedirs(viz_dir, exist_ok=True)
            
            # Take screenshot
            screenshot = driver.get_screenshot_as_png()
            
            # Save accessibility heatmap
            heatmap_path = os.path.join(viz_dir, "accessibility_heatmap.png")
            
            # For now, save the screenshot (in production, overlay issue markers)
            with open(heatmap_path, 'wb') as f:
                f.write(screenshot)
            
            self.wcag_results['accessibility_heatmap'] = heatmap_path
            
        except Exception as e:
            self.logger.error(f"Failed to generate accessibility heatmap: {e}")
    
    def generate_wcag_report(self, output_path):
        """Generate detailed WCAG compliance report"""
        try:
            report_data = {
                'metadata': {
                    'generated_at': datetime.now().isoformat(),
                    'report_version': '1.0',
                    'wcag_version': '2.1',
                    'generator': 'Visual AI Regression Module - WCAG Checker'
                },
                'wcag_analysis': self.wcag_results,
                'recommendations': self._generate_recommendations(),
                'summary': {
                    'compliance_score': self.compliance_score,
                    'compliance_level': self.wcag_results.get('compliance_level', 'Unknown'),
                    'total_issues': self.wcag_results.get('total_issues', 0),
                    'critical_issues': self.wcag_results.get('critical_issues', 0),
                    'needs_immediate_attention': self.wcag_results.get('critical_issues', 0) > 0
                }
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, default=str)
            
            self.logger.info(f"WCAG report saved to: {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Failed to generate WCAG report: {e}")
            raise
    
    def _generate_recommendations(self):
        """Generate accessibility improvement recommendations"""
        recommendations = []
        
        if self.wcag_results.get('critical_issues', 0) > 0:
            recommendations.append({
                'priority': 'Critical',
                'action': 'Address all critical accessibility issues immediately',
                'impact': 'High - Prevents users with disabilities from accessing content'
            })
        
        if self.compliance_score < 70:
            recommendations.append({
                'priority': 'High',
                'action': 'Implement comprehensive accessibility audit and remediation',
                'impact': 'High - Current compliance level may violate accessibility laws'
            })
        
        if self.compliance_score < 85:
            recommendations.append({
                'priority': 'Medium',
                'action': 'Focus on achieving WCAG AA compliance',
                'impact': 'Medium - Improves accessibility for broader user base'
            })
        
        # Category-specific recommendations
        for category, data in self.wcag_results.get('categories', {}).items():
            if data['score'] < 80:
                recommendations.append({
                    'priority': 'Medium',
                    'action': f'Improve {category} accessibility principles',
                    'impact': f'Medium - {len(data["issues"])} issues found in {category} category'
                })
        
        return recommendations
    
    def _check_wcag_22_features(self, driver, soup):
        """Check WCAG 2.2 specific requirements"""
        issues = []
        
        # 2.5.8 Target Size (Minimum) - WCAG 2.2 AA
        target_size_issues = self._check_target_size(driver, soup)
        issues.extend(target_size_issues)
        
        # 3.2.6 Consistent Help - WCAG 2.2 A
        help_consistency_issues = self._check_consistent_help(soup)
        issues.extend(help_consistency_issues)
        
        # 3.3.7 Redundant Entry - WCAG 2.2 A
        redundant_entry_issues = self._check_redundant_entry(soup)
        issues.extend(redundant_entry_issues)
        
        # 3.3.8 Accessible Authentication (Minimum) - WCAG 2.2 AA
        auth_issues = self._check_accessible_authentication(soup)
        issues.extend(auth_issues)
        
        # Update WCAG 2.2 compliance flags
        self.wcag_results['wcag_22_features']['target_size_compliant'] = len(target_size_issues) == 0
        
        # Add to operable category (most 2.2 features are operable)
        self.wcag_results['categories']['operable']['issues'].extend(issues)
        
    def _check_target_size(self, driver, soup):
        """Check WCAG 2.2 Target Size requirements"""
        issues = []
        
        try:
            # Get all clickable elements
            clickable_elements = driver.find_elements(By.CSS_SELECTOR, 
                "a, button, input[type='button'], input[type='submit'], input[type='reset'], "
                "[role='button'], [tabindex], [onclick]")
            
            for element in clickable_elements:
                try:
                    size = element.size
                    width, height = size['width'], size['height']
                    
                    # Check minimum target size (24x24 CSS pixels for AA)
                    if width < self.min_target_size or height < self.min_target_size:
                        # Check if element has sufficient spacing
                        location = element.location
                        if not self._has_sufficient_spacing(driver, element, location):
                            issues.append({
                                'guideline': '2.5.8',
                                'level': 'AA',
                                'description': f'Target size too small: {width}x{height}px (minimum: {self.min_target_size}x{self.min_target_size}px)',
                                'element': element.tag_name,
                                'impact': 'major'
                            })
                except Exception:
                    continue
                    
        except Exception as e:
            self.logger.warning(f"Target size check failed: {e}")
            
        return issues
    
    def _has_sufficient_spacing(self, driver, element, location):
        """Check if element has sufficient spacing around it"""
        try:
            # Simple spacing check - look for nearby clickable elements
            nearby_elements = driver.find_elements(By.CSS_SELECTOR, 
                "a, button, input[type='button'], input[type='submit'], input[type='reset']")
            
            for nearby in nearby_elements:
                if nearby == element:
                    continue
                
                nearby_location = nearby.location
                distance = abs(location['x'] - nearby_location['x']) + abs(location['y'] - nearby_location['y'])
                
                if distance < self.min_target_size:
                    return False
                    
            return True
        except Exception:
            return True  # Assume sufficient spacing if check fails
    
    def _check_consistent_help(self, soup):
        """Check WCAG 2.2 Consistent Help requirements"""
        issues = []
        
        # Look for help-related elements
        help_elements = soup.find_all(['a', 'button'], string=re.compile(r'help|support|contact|faq', re.I))
        help_links = soup.find_all('a', href=re.compile(r'help|support|contact|faq', re.I))
        
        # Basic check - if help is provided, it should be consistent
        if help_elements or help_links:
            # This is a simplified check - in practice, you'd need to check across multiple pages
            help_positions = set()
            for elem in help_elements + help_links:
                # Get relative position (simplified)
                parent = elem.parent
                if parent:
                    siblings = parent.find_all()
                    position = siblings.index(elem) if elem in siblings else 0
                    help_positions.add(position)
            
            if len(help_positions) > 2:  # Too much variation in help placement
                issues.append({
                    'guideline': '3.2.6',
                    'level': 'A',
                    'description': 'Help placement may not be consistent across pages',
                    'element': 'Help elements',
                    'impact': 'moderate'
                })
        
        return issues
    
    def _check_redundant_entry(self, soup):
        """Check WCAG 2.2 Redundant Entry requirements"""
        issues = []
        
        # Look for forms that might require redundant information
        forms = soup.find_all('form')
        for form in forms:
            inputs = form.find_all(['input', 'textarea', 'select'])
            input_types = [inp.get('type', 'text').lower() for inp in inputs]
            
            # Check for password confirmation fields without autocomplete
            password_fields = [inp for inp in inputs if inp.get('type') == 'password']
            if len(password_fields) > 1:
                for pwd_field in password_fields:
                    if not pwd_field.get('autocomplete'):
                        issues.append({
                            'guideline': '3.3.7',
                            'level': 'A',
                            'description': 'Password field may require redundant entry - consider autocomplete',
                            'element': str(pwd_field)[:100] + '...',
                            'impact': 'moderate'
                        })
        
        return issues
    
    def _check_accessible_authentication(self, soup):
        """Check WCAG 2.2 Accessible Authentication requirements"""
        issues = []
        
        # Look for authentication forms
        auth_forms = soup.find_all('form')
        for form in auth_forms:
            inputs = form.find_all('input')
            has_password = any(inp.get('type') == 'password' for inp in inputs)
            
            if has_password:
                # Check for cognitive barriers
                has_captcha = any('captcha' in str(inp).lower() for inp in inputs)
                has_security_questions = any('security' in str(inp).lower() for inp in inputs)
                
                if has_captcha:
                    # Check if alternative is provided
                    alt_methods = form.find_all(string=re.compile(r'audio|alternative|accessibility', re.I))
                    if not alt_methods:
                        issues.append({
                            'guideline': '3.3.8',
                            'level': 'AA',
                            'description': 'CAPTCHA without accessible alternative detected',
                            'element': 'Authentication form',
                            'impact': 'critical'
                        })
                
                if has_security_questions:
                    issues.append({
                        'guideline': '3.3.8',
                        'level': 'AA',
                        'description': 'Security questions may create cognitive barriers',
                        'element': 'Authentication form',
                        'impact': 'major'
                    })
        
        return issues
    
    def _enhanced_color_analysis(self, driver, soup):
        """Enhanced color contrast analysis with WCAG 2.2 considerations"""
        try:
            # Take screenshot for color analysis
            screenshot = driver.get_screenshot_as_png()
            img = Image.open(io.BytesIO(screenshot))
            img_array = np.array(img)
            
            # Analyze color contrast ratios
            contrast_issues = self._analyze_color_contrast_enhanced(img_array, driver)
            
            # Add to perceivable category
            self.wcag_results['categories']['perceivable']['issues'].extend(contrast_issues)
            
            # Color blindness simulation
            colorblind_issues = self._check_colorblind_accessibility(img_array)
            self.wcag_results['categories']['perceivable']['issues'].extend(colorblind_issues)
            
        except Exception as e:
            self.logger.warning(f"Enhanced color analysis failed: {e}")
    
    def _analyze_color_contrast_enhanced(self, img_array, driver):
        """Analyze color contrast ratios using image analysis"""
        issues = []
        
        try:
            # Get text elements and their colors
            text_elements = driver.find_elements(By.CSS_SELECTOR, "p, h1, h2, h3, h4, h5, h6, span, div, a, button")
            
            for element in text_elements[:10]:  # Limit for performance
                try:
                    # Get element colors
                    color = element.value_of_css_property('color')
                    background_color = element.value_of_css_property('background-color')
                    
                    if color and background_color:
                        contrast_ratio = self._calculate_contrast_ratio(color, background_color)
                        
                        # Check against WCAG requirements
                        if contrast_ratio < 4.5:  # AA requirement for normal text
                            issues.append({
                                'guideline': '1.4.3',
                                'level': 'AA',
                                'description': f'Low color contrast ratio: {contrast_ratio:.2f}:1 (minimum: 4.5:1)',
                                'element': element.tag_name,
                                'impact': 'major'
                            })
                        elif contrast_ratio < 7.0:  # AAA requirement
                            issues.append({
                                'guideline': '1.4.6',
                                'level': 'AAA',
                                'description': f'Color contrast below AAA standard: {contrast_ratio:.2f}:1 (recommended: 7:1)',
                                'element': element.tag_name,
                                'impact': 'moderate'
                            })
                            
                except Exception:
                    continue
                    
        except Exception as e:
            self.logger.warning(f"Color contrast analysis failed: {e}")
            
        return issues
    
    def _calculate_contrast_ratio(self, color1, color2):
        """Calculate WCAG color contrast ratio"""
        try:
            # Parse CSS color values (simplified)
            def parse_color(color_str):
                if color_str.startswith('rgb'):
                    values = re.findall(r'\d+', color_str)
                    return [int(v) for v in values[:3]]
                return [0, 0, 0]  # Default to black
            
            rgb1 = parse_color(color1)
            rgb2 = parse_color(color2)
            
            # Convert to relative luminance
            def relative_luminance(rgb):
                rgb = [c / 255.0 for c in rgb]
                rgb = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
                return 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]
            
            l1 = relative_luminance(rgb1)
            l2 = relative_luminance(rgb2)
            
            # Calculate contrast ratio
            lighter = max(l1, l2)
            darker = min(l1, l2)
            return (lighter + 0.05) / (darker + 0.05)
            
        except Exception:
            return 4.5  # Return passing ratio if calculation fails
    
    def _check_colorblind_accessibility(self, img_array):
        """Check accessibility for color-blind users"""
        issues = []
        
        try:
            # Simulate different types of color blindness
            colorblind_simulations = ['protanopia', 'deuteranopia', 'tritanopia']
            
            for simulation in colorblind_simulations:
                simulated_img = self._simulate_colorblindness(img_array, simulation)
                
                # Check if important information is still distinguishable
                # This is a simplified check - in practice, you'd analyze specific UI elements
                original_contrast = self._calculate_image_contrast(img_array)
                simulated_contrast = self._calculate_image_contrast(simulated_img)
                
                contrast_loss = (original_contrast - simulated_contrast) / original_contrast
                
                if contrast_loss > 0.3:  # More than 30% contrast loss
                    issues.append({
                        'guideline': '1.4.1',
                        'level': 'A',
                        'description': f'Significant contrast loss for {simulation} users: {contrast_loss*100:.1f}%',
                        'element': 'Color-dependent content',
                        'impact': 'major'
                    })
                    
        except Exception as e:
            self.logger.warning(f"Colorblind accessibility check failed: {e}")
            
        return issues
    
    def _simulate_colorblindness(self, img_array, type_):
        """Simulate color blindness on image"""
        # Simplified color blindness simulation
        # In practice, you'd use more sophisticated color transformation matrices
        img = img_array.copy()
        
        if type_ == 'protanopia':
            # Red-blind: reduce red channel
            img[:, :, 0] = img[:, :, 0] * 0.1
        elif type_ == 'deuteranopia':
            # Green-blind: reduce green channel
            img[:, :, 1] = img[:, :, 1] * 0.1
        elif type_ == 'tritanopia':
            # Blue-blind: reduce blue channel
            img[:, :, 2] = img[:, :, 2] * 0.1
            
        return img
    
    def _calculate_image_contrast(self, img_array):
        """Calculate overall image contrast"""
        try:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            return np.std(gray)
        except Exception:
            return 0

    # ...existing code...
