import os
import time
from datetime import datetime
import logging
from screenshot_capture import ScreenshotCapture
from image_comparison import ImageComparison
from ai_detector import AIDetector
from report_generator import ReportGenerator
from wcag_checker import WCAGCompliantChecker

class VisualAIRegression:
    def __init__(self):
        self.setup_logging()
        self.screenshot_capturer = None
        self.image_comparator = ImageComparison()
        self.ai_detector = AIDetector()
        self.report_generator = ReportGenerator()
        self.wcag_checker = WCAGCompliantChecker()  # Add WCAG checker
        
    def setup_logging(self):
        """Setup logging for the main regression class"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def run_analysis(self, config, progress_callback=None):
        """Run complete visual regression analysis"""
        start_time = time.time()  # Start timing
        try:
            self.logger.info("Starting visual regression analysis...")
            
            # Initialize progress callback
            if progress_callback is None:
                progress_callback = lambda msg: self.logger.info(msg)
            
            # Step 1: Setup and validation
            progress_callback("Validating configuration...")
            self._validate_config(config)
            
            # Step 2: Initialize screenshot capturer
            progress_callback("Initializing browser...")
            self.screenshot_capturer = ScreenshotCapture(
                browser=config.get('browser', 'chrome'),
                headless=True
            )
            self.screenshot_capturer.initialize_driver(config.get('resolution', '1920x1080'))
            
            # Step 3: Capture screenshots
            progress_callback("Capturing screenshots...")
            screenshot_paths = self._capture_screenshots(config, progress_callback)
            
            # Step 4: Load and preprocess images
            progress_callback("Loading and preprocessing images...")
            img1, img2 = self.image_comparator.load_images(
                screenshot_paths['url1'], 
                screenshot_paths['url2']
            )
            img1, img2 = self.image_comparator.resize_images_to_match(img1, img2)
            
            # Step 5: Run comparisons
            progress_callback("Running image analysis...")
            analysis_results = self._run_comparisons(img1, img2, config, progress_callback)
            
            # Step 5.5: Add screenshot paths to analysis results for report generation
            analysis_results['screenshots'] = {
                'url1': screenshot_paths['url1'],
                'url2': screenshot_paths['url2']
            }
            
            # Step 6: Generate summary and details before reports
            progress_callback("Processing analysis results...")
            summary_dict = self._generate_summary_dict(analysis_results, config)
            summary = self._generate_summary(analysis_results, config)
            details = self._generate_details(analysis_results)
            
            # Add summary_dict to analysis_results so reports can access it
            analysis_results['summary_dict'] = summary_dict
            
            # Add timing information
            end_time_for_analysis = time.time()
            analysis_duration = end_time_for_analysis - start_time
            analysis_results['duration'] = f"{analysis_duration:.1f} seconds"
            analysis_results['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Step 7: Generate reports (now with summary_dict included)
            progress_callback("Generating reports...")
            reports = self.report_generator.generate_comprehensive_report(
                analysis_results, config
            )
            
            # Step 8: Cleanup
            progress_callback("Cleaning up resources...")
            self._cleanup()
            
            # Calculate analysis duration
            end_time = time.time()
            duration_seconds = end_time - start_time
            duration_formatted = f"{duration_seconds:.1f} seconds"
            
            # Prepare final results
            final_results = {
                'analysis_results': analysis_results,
                'reports': reports,
                'screenshot_paths': screenshot_paths,
                'summary': summary,
                'summary_dict': summary_dict,
                'details': details,
                'duration': duration_formatted,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            progress_callback("Analysis completed successfully!")
            self.logger.info("Visual regression analysis completed successfully")
            
            return final_results
            
        except Exception as e:
            self.logger.error(f"Analysis failed: {str(e)}")
            self._cleanup()
            raise
    
    def _validate_config(self, config):
        """Validate configuration parameters"""
        required_fields = ['url1', 'url2']
        for field in required_fields:
            if not config.get(field):
                raise ValueError(f"Missing required configuration: {field}")
        
        # Validate URLs
        for url_key in ['url1', 'url2']:
            url = config[url_key]
            if not (url.startswith('http://') or url.startswith('https://')):
                raise ValueError(f"Invalid URL format: {url}")
        
        self.logger.info("Configuration validated successfully")
    
    def _capture_screenshots(self, config, progress_callback):
        """Capture screenshots of both URLs"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshots_dir = os.path.join("screenshots", timestamp)
            os.makedirs(screenshots_dir, exist_ok=True)
            
            screenshot_paths = {}
            
            # Capture first URL
            progress_callback(f"Capturing screenshot of URL 1: {config['url1']}")
            path1 = os.path.join(screenshots_dir, "url1_screenshot.png")
            self.screenshot_capturer.capture_screenshot(
                config['url1'], 
                path1, 
                wait_time=3, 
                full_page=True
            )
            screenshot_paths['url1'] = path1
            
            # Small delay between captures
            time.sleep(2)
            
            # Capture second URL
            progress_callback(f"Capturing screenshot of URL 2: {config['url2']}")
            path2 = os.path.join(screenshots_dir, "url2_screenshot.png")
            self.screenshot_capturer.capture_screenshot(
                config['url2'], 
                path2, 
                wait_time=3, 
                full_page=True
            )
            screenshot_paths['url2'] = path2
            
            # Get page information
            progress_callback("Gathering page information...")
            page_info1 = self.screenshot_capturer.get_page_info(config['url1'])
            page_info2 = self.screenshot_capturer.get_page_info(config['url2'])
            
            screenshot_paths['page_info'] = {
                'url1': page_info1,
                'url2': page_info2
            }
            
            self.logger.info(f"Screenshots captured successfully: {screenshot_paths}")
            return screenshot_paths
            
        except Exception as e:
            self.logger.error(f"Failed to capture screenshots: {str(e)}")
            raise
    
    def _run_comparisons(self, img1, img2, config, progress_callback):
        """Run all enabled comparison analyses"""
        results = {}
        
        try:
            # Comprehensive metrics analysis
            progress_callback("Calculating comprehensive similarity metrics...")
            metrics = self.image_comparator.calculate_comprehensive_metrics(img1, img2)
            results['similarity_score'] = metrics['ssim']
            results['ssim'] = metrics['ssim']
            results['mse'] = metrics['mse']
            results['psnr'] = metrics['psnr']
            results['pixel_metrics'] = metrics['pixel_metrics']
            results['overall_similarity_percentage'] = metrics['overall_similarity_percentage']
            results['diff_image'] = metrics['ssim_diff_image']
            
            # Layout shift detection
            if config.get('layout_shift', True):
                progress_callback("Detecting layout shifts...")
                layout_shifts = self.image_comparator.detect_layout_shifts(img1, img2)
                results['layout_shifts'] = layout_shifts
            
            # Color and font analysis
            if config.get('font_color', True):
                progress_callback("Analyzing color differences...")
                color_differences, color_diff_img = self.image_comparator.detect_color_differences(img1, img2)
                results['color_differences'] = color_differences
                results['color_diff_image'] = color_diff_img
            
            # Missing/overlapping elements detection
            if config.get('element_detection', True):
                progress_callback("Detecting missing and new elements...")
                missing_elements, new_elements, elements_diff = self.image_comparator.detect_missing_elements(img1, img2)
                results['missing_elements'] = missing_elements
                results['new_elements'] = new_elements
                results['elements_diff_image'] = elements_diff
                
                progress_callback("Detecting overlapping elements...")
                overlapping_elements = self.image_comparator.detect_overlapping_elements(img1, img2)
                results['overlapping_elements'] = overlapping_elements
            
            # AI-powered analysis
            if config.get('ai_analysis', True):
                progress_callback("Running AI-powered analysis...")
                ai_results = self._run_ai_analysis(img1, img2, progress_callback)
                results['ai_analysis'] = ai_results
            
            # WCAG Compliance Analysis
            if config.get('wcag_analysis', True):
                try:
                    progress_callback("Running WCAG compliance analysis...")
                    wcag_results_url1 = self._run_wcag_analysis(config['url1'], progress_callback)
                    wcag_results_url2 = self._run_wcag_analysis(config['url2'], progress_callback)
                    
                    # Always include WCAG analysis even if there are errors
                    results['wcag_analysis'] = {
                        'url1': wcag_results_url1,
                        'url2': wcag_results_url2,
                        'comparison': self._compare_wcag_results(wcag_results_url1, wcag_results_url2)
                    }
                    print(f"DEBUG: WCAG analysis completed. URL1 score: {wcag_results_url1.get('compliance_score', 'error')}, URL2 score: {wcag_results_url2.get('compliance_score', 'error')}")
                except Exception as e:
                    self.logger.error(f"WCAG compliance analysis failed: {str(e)}")
                    # Still include a basic WCAG structure
                    results['wcag_analysis'] = {
                        'url1': {'error': str(e), 'compliance_score': 0, 'compliance_level': 'Error'},
                        'url2': {'error': str(e), 'compliance_score': 0, 'compliance_level': 'Error'},
                        'comparison': {'assessment': 'Analysis failed', 'error': str(e)}
                    }

            # Generate difference visualizations
            progress_callback("Creating difference visualizations...")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            viz_dir = os.path.join("visualizations", timestamp)
            os.makedirs(viz_dir, exist_ok=True)
            
            # Heatmap
            heatmap_path = os.path.join(viz_dir, "difference_heatmap.png")
            self.image_comparator.create_difference_heatmap(img1, img2, heatmap_path)
            results['heatmap_path'] = heatmap_path
            
            # Annotated comparison
            all_differences = []
            if 'layout_shifts' in results:
                all_differences.extend(results['layout_shifts'])
            if 'color_differences' in results:
                all_differences.extend(results['color_differences'])
            
            if all_differences:
                annotated_path = os.path.join(viz_dir, "annotated_comparison.png")
                self.image_comparator.create_annotated_comparison(
                    img1, img2, all_differences, annotated_path
                )
                results['annotated_comparison_path'] = annotated_path
            
            self.logger.info("All comparisons completed successfully")
            return results
            
        except Exception as e:
            self.logger.error(f"Failed to run comparisons: {str(e)}")
            raise
    
    def _run_ai_analysis(self, img1, img2, progress_callback):
        """Run AI-powered analysis"""
        try:
            ai_results = {}
            
            # Extract features
            progress_callback("Extracting image features...")
            features1 = self.ai_detector.extract_features(img1)
            features2 = self.ai_detector.extract_features(img2)
            
            if len(features1) > 0 and len(features2) > 0:
                # Anomaly detection
                progress_callback("Running anomaly detection...")
                anomaly_results = self.ai_detector.detect_anomalies_clustering(features1, features2)
                ai_results.update(anomaly_results)
                
                # Semantic analysis
                progress_callback("Performing semantic analysis...")
                semantic_results = self.ai_detector.analyze_semantic_differences(img1, img2)
                ai_results['semantic_analysis'] = semantic_results
            else:
                self.logger.warning("Could not extract features for AI analysis")
                ai_results = {
                    'anomaly_detected': False,
                    'feature_distance': 0,
                    'confidence': 0,
                    'error': 'Feature extraction failed'
                }
            
            return ai_results
            
        except Exception as e:
            self.logger.error(f"AI analysis failed: {str(e)}")
            return {
                'anomaly_detected': False,
                'feature_distance': 0,
                'confidence': 0,
                'error': str(e)
            }
    
    def _run_wcag_analysis(self, url, progress_callback):
        """Run WCAG compliance analysis for a single URL"""
        try:
            print(f"DEBUG: Starting WCAG analysis for URL: {url}")
            
            if not self.screenshot_capturer or not self.screenshot_capturer.driver:
                raise ValueError("WebDriver not initialized")
            
            # Run WCAG compliance check
            wcag_results = self.wcag_checker.check_wcag_compliance(
                self.screenshot_capturer.driver, 
                url, 
                progress_callback
            )
            
            print(f"DEBUG: WCAG analysis completed for {url}. Score: {wcag_results.get('compliance_score', 'missing')}")
            
            # Generate WCAG report
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            wcag_report_path = os.path.join("reports", f"wcag_report_{timestamp}_{url.replace('://', '_').replace('/', '_')}.json")
            os.makedirs("reports", exist_ok=True)
            self.wcag_checker.generate_wcag_report(wcag_report_path)
            wcag_results['report_path'] = wcag_report_path
            
            return wcag_results
            
        except Exception as e:
            self.logger.error(f"WCAG analysis failed for {url}: {str(e)}")
            print(f"DEBUG: WCAG analysis failed for {url}: {str(e)}")
            return {
                'error': str(e),
                'url': url,
                'compliance_score': 0,
                'compliance_level': 'Error',
                'total_issues': 0,
                'critical_issues': 0,
                'categories': {
                    'perceivable': {'score': 0, 'issues': []},
                    'operable': {'score': 0, 'issues': []},
                    'understandable': {'score': 0, 'issues': []},
                    'robust': {'score': 0, 'issues': []}
                }
            }
    
    def _compare_wcag_results(self, wcag1, wcag2):
        """Compare WCAG results between two URLs"""
        try:
            comparison = {
                'score_difference': wcag2.get('compliance_score', 0) - wcag1.get('compliance_score', 0),
                'level_comparison': {
                    'url1': wcag1.get('compliance_level', 'Unknown'),
                    'url2': wcag2.get('compliance_level', 'Unknown')
                },
                'issue_comparison': {
                    'url1_issues': wcag1.get('total_issues', 0),
                    'url2_issues': wcag2.get('total_issues', 0),
                    'difference': wcag2.get('total_issues', 0) - wcag1.get('total_issues', 0)
                },
                'critical_issues_comparison': {
                    'url1_critical': wcag1.get('critical_issues', 0),
                    'url2_critical': wcag2.get('critical_issues', 0),
                    'difference': wcag2.get('critical_issues', 0) - wcag1.get('critical_issues', 0)
                },
                'category_comparison': {}
            }
            
            # Compare categories
            for category in ['perceivable', 'operable', 'understandable', 'robust']:
                url1_score = wcag1.get('categories', {}).get(category, {}).get('score', 0)
                url2_score = wcag2.get('categories', {}).get(category, {}).get('score', 0)
                comparison['category_comparison'][category] = {
                    'url1_score': url1_score,
                    'url2_score': url2_score,
                    'difference': url2_score - url1_score
                }
            
            # Overall assessment
            if comparison['score_difference'] > 5:
                comparison['assessment'] = 'URL2 has significantly better accessibility'
            elif comparison['score_difference'] < -5:
                comparison['assessment'] = 'URL1 has significantly better accessibility'
            else:
                comparison['assessment'] = 'URLs have similar accessibility levels'
            
            return comparison
            
        except Exception as e:
            self.logger.error(f"WCAG comparison failed: {str(e)}")
            return {'error': str(e)}

    def _generate_summary(self, results, config):
        """Generate a text summary of results based on enabled analysis types"""
        summary_lines = []
        
        # Overall similarity (always included)
        similarity = results.get('similarity_score', 0)
        mse = results.get('mse', 0)
        psnr = results.get('psnr', 0)
        pixel_metrics = results.get('pixel_metrics', {})
        pixel_diff_percentage = pixel_metrics.get('pixel_difference_percentage', 0)
        
        summary_lines.append(f"📊 Comprehensive Metrics:")
        summary_lines.append(f"  • SSIM (Structural Similarity): {similarity:.4f}")
        summary_lines.append(f"  • MSE (Mean Squared Error): {mse:.6f}")
        summary_lines.append(f"  • PSNR (Peak Signal-to-Noise Ratio): {psnr:.2f} dB")
        summary_lines.append(f"  • Pixel Differences: {pixel_diff_percentage:.2f}%")
        
        if similarity > 0.95:
            summary_lines.append("✓ Images are very similar")
        elif similarity > 0.85:
            summary_lines.append("⚠ Images have moderate differences")
        else:
            summary_lines.append("✗ Images have significant differences")
        
        # Layout shifts (only if enabled)
        if config.get('layout_shift', True) and 'layout_shifts' in results:
            layout_shifts = len(results.get('layout_shifts', []))
            if layout_shifts > 0:
                summary_lines.append(f"⚠ {layout_shifts} layout shifts detected")
            else:
                summary_lines.append("✓ No layout shifts detected")
        
        # Color differences (only if enabled)
        if config.get('font_color', True) and 'color_differences' in results:
            color_diffs = len(results.get('color_differences', []))
            if color_diffs > 0:
                summary_lines.append(f"⚠ {color_diffs} color differences detected")
            else:
                summary_lines.append("✓ No significant color differences")
        
        # Missing/new elements (only if enabled)
        if config.get('element_detection', True) and ('missing_elements' in results or 'new_elements' in results):
            missing = len(results.get('missing_elements', []))
            new = len(results.get('new_elements', []))
            if missing > 0 or new > 0:
                summary_lines.append(f"⚠ {missing} missing, {new} new elements detected")
            else:
                summary_lines.append("✓ No missing or new elements detected")
        
        # AI analysis (only if enabled)
        if config.get('ai_analysis', True) and 'ai_analysis' in results:
            ai = results['ai_analysis']
            if ai.get('anomaly_detected', False):
                summary_lines.append(f"🤖 AI detected anomaly (confidence: {ai.get('confidence', 0):.1%})")
            else:
                summary_lines.append("🤖 AI analysis: No anomalies detected")
        
        # WCAG analysis (only if enabled)
        if config.get('wcag_analysis', True) and 'wcag_analysis' in results:
            wcag = results['wcag_analysis']
            url1_level = wcag.get('url1', {}).get('compliance_level', 'Unknown')
            url2_level = wcag.get('url2', {}).get('compliance_level', 'Unknown')
            url1_score = wcag.get('url1', {}).get('compliance_score', 0)
            url2_score = wcag.get('url2', {}).get('compliance_score', 0)
            summary_lines.append(f"♿ WCAG Compliance: URL 1 - {url1_level} ({url1_score:.1f}%), URL 2 - {url2_level} ({url2_score:.1f}%)")
        
        return "\\n".join(summary_lines)
    
    def _generate_summary_dict(self, results, config):
        """Generate a structured dictionary summary of results for GUI display based on enabled analysis types"""
        summary_dict = {}
        
        # Overall similarity and metrics (always included)
        similarity = results.get('similarity_score', 0)
        summary_dict['similarity_score'] = similarity
        summary_dict['ssim'] = results.get('ssim', similarity)
        summary_dict['mse'] = results.get('mse', 0)
        summary_dict['psnr'] = results.get('psnr', 0)
        
        # Pixel difference metrics
        pixel_metrics = results.get('pixel_metrics', {})
        summary_dict['pixel_difference_percentage'] = pixel_metrics.get('pixel_difference_percentage', 0)
        summary_dict['different_pixels'] = pixel_metrics.get('different_pixels', 0)
        summary_dict['total_pixels'] = pixel_metrics.get('total_pixels', 0)
        summary_dict['avg_pixel_difference'] = pixel_metrics.get('avg_pixel_difference', 0)
        summary_dict['max_pixel_difference'] = pixel_metrics.get('max_pixel_difference', 0)
        
        # Layout shifts (only if enabled)
        if config.get('layout_shift', True) and 'layout_shifts' in results:
            layout_shifts = len(results.get('layout_shifts', []))
            summary_dict['layout_differences'] = layout_shifts
        
        # Color differences (only if enabled)
        if config.get('font_color', True) and 'color_differences' in results:
            color_diffs = len(results.get('color_differences', []))
            summary_dict['color_differences'] = color_diffs
        
        # Missing/new elements (only if enabled)
        if config.get('element_detection', True):
            missing = len(results.get('missing_elements', []))
            new = len(results.get('new_elements', []))
            summary_dict['missing_elements'] = missing
            summary_dict['new_elements'] = new
            summary_dict['element_changes'] = missing + new
        
        # AI analysis (only if enabled)
        if config.get('ai_analysis', True) and 'ai_analysis' in results:
            ai_anomalies = 0
            ai = results['ai_analysis']
            if ai.get('anomaly_detected', False):
                ai_anomalies = 1
            # Count semantic changes
            if 'semantic_analysis' in ai:
                semantic = ai['semantic_analysis']
                layout_changes = len(semantic.get('layout_changes', []))
                content_changes = len(semantic.get('content_changes', []))
                style_changes = len(semantic.get('style_changes', []))
                structural_changes = len(semantic.get('structural_changes', []))
                ai_anomalies += layout_changes + content_changes + style_changes + structural_changes
            
            summary_dict['ai_anomalies'] = ai_anomalies
        
        # WCAG analysis (only if enabled)
        if config.get('wcag_analysis', True) and 'wcag_analysis' in results:
            wcag = results['wcag_analysis']
            summary_dict['wcag_url1_score'] = wcag.get('url1', {}).get('compliance_score', 0)
            summary_dict['wcag_url2_score'] = wcag.get('url2', {}).get('compliance_score', 0)
            summary_dict['wcag_url1_level'] = wcag.get('url1', {}).get('compliance_level', 'Unknown')
            summary_dict['wcag_url2_level'] = wcag.get('url2', {}).get('compliance_level', 'Unknown')
            summary_dict['wcag_url1_issues'] = wcag.get('url1', {}).get('total_issues', 0)
            summary_dict['wcag_url2_issues'] = wcag.get('url2', {}).get('total_issues', 0)        
        return summary_dict

    def _generate_details(self, results):
        """Generate detailed breakdown of results"""
        details = {}
        
        # Similarity details
        details['Structural Similarity (SSIM)'] = f"Score: {results.get('similarity_score', 0):.4f}"
        
        # Layout shifts details
        if 'layout_shifts' in results and results['layout_shifts']:
            shift_details = []
            for i, shift in enumerate(results['layout_shifts'][:5]):  # Top 5
                shift_details.append(f"Shift {i+1}: {shift.get('distance', 0):.1f}px movement")
            details['Layout Shifts'] = "\\n".join(shift_details)
        
        # Color differences details
        if 'color_differences' in results and results['color_differences']:
            color_details = []
            for i, diff in enumerate(results['color_differences'][:5]):  # Top 5
                color_details.append(f"Difference {i+1}: Distance {diff.get('color_distance', 0):.1f}, Area {diff.get('area', 0):.0f}px²")
            details['Color Differences'] = "\\n".join(color_details)
        
        # AI analysis details
        if 'ai_analysis' in results:
            ai = results['ai_analysis']
            ai_details = [
                f"Feature Distance: {ai.get('feature_distance', 0):.4f}",
                f"Confidence: {ai.get('confidence', 0):.1%}"
            ]
            if 'semantic_analysis' in ai:
                semantic = ai['semantic_analysis']
                ai_details.extend([
                    f"Layout Changes: {len(semantic.get('layout_changes', []))}",
                    f"Content Changes: {len(semantic.get('content_changes', []))}",
                    f"Style Changes: {len(semantic.get('style_changes', []))}",
                    f"Structural Changes: {len(semantic.get('structural_changes', []))}"
                ])
            details['AI Analysis'] = "\\n".join(ai_details)
        
        # WCAG analysis details
        if 'wcag_analysis' in results:
            wcag = results['wcag_analysis']
            url1_info = wcag.get('url1', {})
            url2_info = wcag.get('url2', {})
            url1_level = url1_info.get('compliance_level', 'Unknown')
            url2_level = url2_info.get('compliance_level', 'Unknown')
            url1_issues = url1_info.get('total_issues', 0)
            url2_issues = url2_info.get('total_issues', 0)
            details['WCAG Compliance'] = f"URL 1: {url1_level} - {url1_issues} issues, URL 2: {url2_level} - {url2_issues} issues"
        
        return details
    
    def run_image_analysis(self, config, progress_callback=None):
        """Run analysis on pre-existing image files"""
        start_time = time.time()
        try:
            self.logger.info("Starting image analysis...")
            
            # Initialize progress callback
            if progress_callback is None:
                progress_callback = lambda msg: self.logger.info(msg)
            
            # Step 1: Validate image paths
            progress_callback("Validating image files...")
            if 'baseline_image' not in config or 'current_image' not in config:
                raise ValueError("Both baseline_image and current_image paths are required")
            
            if not os.path.exists(config['baseline_image']):
                raise FileNotFoundError(f"Baseline image not found: {config['baseline_image']}")
            
            if not os.path.exists(config['current_image']):
                raise FileNotFoundError(f"Current image not found: {config['current_image']}")
            
            # Step 2: Load and preprocess images
            progress_callback("Loading and preprocessing images...")
            img1, img2 = self.image_comparator.load_images(
                config['baseline_image'], 
                config['current_image']
            )
            img1, img2 = self.image_comparator.resize_images_to_match(img1, img2)
            
            # Step 3: Run comparisons
            progress_callback("Running image analysis...")
            analysis_results = self._run_comparisons(img1, img2, config, progress_callback)
            
            # Step 4: Add image paths to analysis results
            analysis_results['screenshots'] = {
                'url1': config['baseline_image'],
                'url2': config['current_image']
            }
            
            # Step 5: Generate summary and details
            progress_callback("Processing analysis results...")
            summary_dict = self._generate_summary_dict(analysis_results, config)
            summary = self._generate_summary(analysis_results, config)
            details = self._generate_details(analysis_results)
            
            # Add summary_dict to analysis_results
            analysis_results['summary_dict'] = summary_dict
            
            # Add timing information
            end_time = time.time()
            analysis_duration = end_time - start_time
            analysis_results['duration'] = f"{analysis_duration:.1f} seconds"
            analysis_results['analysis_duration'] = analysis_duration
            analysis_results['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Step 6: Generate reports if requested
            if config.get('generate_report', False):
                progress_callback("Generating reports...")
                output_dir = config.get('output_dir', 'results')
                os.makedirs(output_dir, exist_ok=True)
                
                reports = self.report_generator.generate_comprehensive_report(
                    analysis_results, config
                )
                analysis_results['reports'] = reports
            
            # Step 7: Prepare final results
            final_results = {
                'similarity_score': analysis_results.get('structural_similarity', {}).get('ssim_score', 0),
                'differences_count': len(analysis_results.get('ai_analysis', {}).get('differences', [])),
                'analysis_duration': analysis_duration,
                'difference_image_path': analysis_results.get('difference_image_path'),
                'summary': summary,
                'details': details,
                'reports': analysis_results.get('reports', {}),
                'timestamp': analysis_results['timestamp']
            }
            
            self.logger.info("Image analysis completed successfully!")
            return final_results
            
        except Exception as e:
            self.logger.error(f"Image analysis failed: {str(e)}")
            raise
    
    def _cleanup(self):
        """Cleanup resources"""
        try:
            if self.screenshot_capturer:
                self.screenshot_capturer.close()
                self.screenshot_capturer = None
            self.logger.info("Cleanup completed")
        except Exception as e:
            self.logger.error(f"Cleanup failed: {str(e)}")

# Example usage
# Example usage (commented out to prevent auto-execution when imported)
# if __name__ == "__main__":
#     # Example configuration
#     config = {
#         'url1': 'https://example.com',
#         'url2': 'https://httpbin.org/html',
#         'browser': 'chrome',
#         'resolution': '1920x1080',
#         'layout_shift': True,
#         'font_color': True,
#         'element_detection': True,
#         'ai_analysis': True,
#         'wcag_analysis': True
#     }
#     
#     # Run analysis
#     regression = VisualAIRegression()
#     
#     try:
#         results = regression.run_analysis(config)
#         print("Analysis completed successfully!")
#         print(f"Summary: {results['summary']}")
#         print(f"Reports generated: {list(results['reports'].keys())}")
#     except Exception as e:
#         print(f"Analysis failed: {e}")
