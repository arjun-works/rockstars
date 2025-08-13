import os
import json
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import numpy as np
import cv2
import logging
import zipfile
import shutil
import webbrowser
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

class ReportGenerator:
    def __init__(self, output_dir="reports"):
        self.output_dir = output_dir
        self.setup_logging()
        self.create_output_directory()
        
    def setup_logging(self):
        """Setup logging for report generator"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def create_output_directory(self):
        """Create output directory if it doesn't exist"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            self.logger.info(f"Created output directory: {self.output_dir}")
    
    def generate_comprehensive_report(self, analysis_results, config):
        """Generate a comprehensive visual regression report with sharing capabilities"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_name = f"visual_regression_report_{timestamp}"
            
            # Generate different report formats
            reports = {}
            
            # 1. PDF Report (generate first)
            pdf_path = os.path.join(self.output_dir, f"{report_name}.pdf")
            self.generate_pdf_report(analysis_results, config, pdf_path)
            reports['pdf'] = pdf_path
            
            # 2. JSON Report (generate second)
            json_path = os.path.join(self.output_dir, f"{report_name}.json")
            self.generate_json_report(analysis_results, config, json_path)
            reports['json'] = json_path
            
            # 3. Enhanced Visual Comparison Images
            visual_path = os.path.join(self.output_dir, f"{report_name}_visual_comparison.png")
            self.generate_enhanced_visual_comparison(analysis_results, visual_path)
            reports['visual'] = visual_path
            
            # 4. Side-by-side comparison
            sidebyside_path = os.path.join(self.output_dir, f"{report_name}_side_by_side.png")
            self.generate_side_by_side_comparison(analysis_results, sidebyside_path)
            reports['sidebyside'] = sidebyside_path
            
            # 5. Difference heatmap
            heatmap_path = os.path.join(self.output_dir, f"{report_name}_difference_heatmap.png")
            self.generate_difference_heatmap(analysis_results, heatmap_path)
            reports['heatmap'] = heatmap_path
            
            # 6. Shareable ZIP package
            zip_path = os.path.join(self.output_dir, f"{report_name}_complete_package.zip")
            self.create_shareable_package(reports, analysis_results, config, zip_path)
            reports['package'] = zip_path
            
            # 7. Summary report for quick sharing
            summary_path = os.path.join(self.output_dir, f"{report_name}_summary.html")
            self.generate_summary_report(analysis_results, config, summary_path)
            reports['summary'] = summary_path
            
            # 8. Enhanced HTML Report with sharing buttons (generate last with all file references)
            html_path = os.path.join(self.output_dir, f"{report_name}.html")
            # Add reports to analysis_results so HTML can reference them
            analysis_results_with_reports = {**analysis_results, 'reports': reports}
            self.generate_enhanced_html_report(analysis_results_with_reports, config, html_path)
            reports['html'] = html_path
            reports['summary'] = summary_path
            
            self.logger.info(f"Comprehensive report generated: {reports}")
            return reports
            
        except Exception as e:
            self.logger.error(f"Failed to generate comprehensive report: {str(e)}")
            raise

    def generate_enhanced_html_report(self, analysis_results, config, output_path):
        """Generate enhanced HTML report with sharing capabilities"""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Extract data from analysis results
            screenshots = analysis_results.get('screenshots', {})
            comparisons = analysis_results.get('comparisons', {})
            ai_analysis = analysis_results.get('ai_analysis', {})
            summary = analysis_results.get('summary_dict', {})  # Fixed: Use summary_dict instead of summary
            
            # Get the base name for the report files
            base_name = os.path.splitext(os.path.basename(output_path))[0]
            
            # Copy screenshot files to reports directory for HTML access
            self._copy_screenshots_to_reports(analysis_results, base_name)
            
            # Pre-generate image HTML content to avoid f-string conflicts
            url1_screenshot_html = self._generate_image_html(analysis_results, 'url1_screenshot', 'Original screenshot')
            url2_screenshot_html = self._generate_image_html(analysis_results, 'url2_screenshot', 'Comparison screenshot')
            sidebyside_html = self._generate_image_html(analysis_results, 'sidebyside', 'Side-by-side comparison')
            heatmap_html = self._generate_image_html(analysis_results, 'heatmap', 'Difference heatmap')
            visual_html = self._generate_image_html(analysis_results, 'visual', 'Visual comparison')
            
            # Pre-generate section HTML content
            analysis_sections_html = self._generate_analysis_sections_html(analysis_results, ai_analysis, config)
            wcag_section_html = self._generate_wcag_section_html(analysis_results, config)
            detailed_findings_html = self._generate_findings_html(analysis_results, ai_analysis, config)
            configuration_settings_html = self._generate_configuration_settings_html(analysis_results, config)
            
            # Generate export links
            export_pdf_link = self._generate_export_link(base_name + '.pdf', '📄 PDF Report', 'PDF version of this analysis report')
            export_json_link = self._generate_export_link(base_name + '.json', '📊 JSON Data', 'Raw analysis data in JSON format')
            export_package_link = self._generate_export_link(base_name + '_complete_package.zip', '📦 Complete Package', 'ZIP file with all reports and images')
            
            html_content = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Visual Regression Analysis Report</title>
                <style>
                    body {{
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        margin: 0;
                        padding: 20px;
                        background-color: #f5f5f5;
                        color: #333;
                        line-height: 1.6;
                    }}
                    .header {{
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        padding: 30px;
                        border-radius: 10px;
                        margin-bottom: 30px;
                        text-align: center;
                    }}
                    .sharing-buttons {{
                        text-align: center;
                        margin: 20px 0;
                        padding: 20px;
                        background: white;
                        border-radius: 10px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    }}
                    .share-btn {{
                        display: inline-block;
                        padding: 12px 24px;
                        margin: 0 10px;
                        background: #667eea;
                        color: white;
                        text-decoration: none;
                        border-radius: 5px;
                        border: none;
                        cursor: pointer;
                        font-size: 14px;
                        transition: background 0.3s;
                    }}
                    .share-btn:hover {{
                        background: #5a6fd8;
                    }}
                    .container {{
                        max-width: 1400px;
                        margin: 0 auto;
                        background: white;
                        padding: 30px;
                        border-radius: 10px;
                        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                    }}
                    .section {{
                        margin-bottom: 30px;
                        padding: 20px;
                        border-left: 4px solid #667eea;
                        background-color: #f9f9f9;
                        border-radius: 5px;
                    }}
                    .section h2 {{
                        color: #667eea;
                        margin-top: 0;
                        border-bottom: 2px solid #667eea;
                        padding-bottom: 10px;
                    }}
                    .config-table {{
                        width: 100%;
                        border-collapse: collapse;
                        margin-bottom: 20px;
                    }}
                    .config-table th, .config-table td {{
                        padding: 12px;
                        text-align: left;
                        border-bottom: 1px solid #ddd;
                    }}
                    .config-table th {{
                        background-color: #667eea;
                        color: white;
                    }}
                    .config-table tr:nth-child(even) {{
                        background-color: #f2f2f2;
                    }}
                    .summary-cards {{
                        display: grid;
                        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                        gap: 20px;
                        margin-bottom: 30px;
                    }}
                    .card {{
                        background: white;
                        padding: 25px;
                        border-radius: 8px;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                        text-align: center;
                        border-top: 4px solid #667eea;
                    }}
                    .card h3 {{
                        margin-top: 0;
                        color: #667eea;
                        font-size: 1.2em;
                    }}
                    .card .number {{
                        font-size: 2.5em;
                        font-weight: bold;
                        color: #764ba2;
                        margin: 10px 0;
                    }}
                    .image-gallery {{
                        display: grid;
                        grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
                        gap: 20px;
                        margin: 20px 0;
                    }}
                    .image-container {{
                        text-align: center;
                        background: white;
                        padding: 15px;
                        border-radius: 8px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    }}
                    .image-container img {{
                        max-width: 100%;
                        height: auto;
                        border-radius: 5px;
                        cursor: pointer;
                        transition: transform 0.3s;
                    }}
                    .image-container img:hover {{
                        transform: scale(1.05);
                    }}
                    .image-container h4 {{
                        margin: 15px 0 5px 0;
                        color: #667eea;
                    }}
                    .difference-highlight {{
                        background-color: #fff3cd;
                        border: 1px solid #ffeaa7;
                        border-radius: 5px;
                        padding: 15px;
                        margin: 10px 0;
                    }}
                    .difference-highlight h4 {{
                        color: #856404;
                        margin-top: 0;
                    }}
                    .status-badge {{
                        display: inline-block;
                        padding: 4px 12px;
                        border-radius: 20px;
                        font-size: 0.9em;
                        font-weight: bold;
                    }}
                    .status-pass {{
                        background-color: #d4edda;
                        color: #155724;
                    }}
                    .status-fail {{
                        background-color: #f8d7da;
                        color: #721c24;
                    }}
                    .status-warning {{
                        background-color: #fff3cd;
                        color: #856404;
                    }}
                    .copy-button {{
                        background: #28a745;
                        color: white;
                        border: none;
                        padding: 8px 16px;
                        border-radius: 4px;
                        cursor: pointer;
                        font-size: 12px;
                        margin-left: 10px;
                    }}
                    .copy-button:hover {{
                        background: #218838;
                    }}
                    .analysis-details {{
                        background: #f8f9fa;
                        border-radius: 8px;
                        padding: 20px;
                        margin: 15px 0;
                    }}
                    .metric-value {{
                        font-weight: bold;
                        color: #495057;
                    }}
                    
                    /* Tab Navigation Styles */
                    .tab-navigation {{
                        display: flex;
                        background: white;
                        border-radius: 10px 10px 0 0;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        overflow-x: auto;
                        margin-bottom: 0;
                    }}
                    .tab-button {{
                        background: none;
                        border: none;
                        padding: 15px 25px;
                        cursor: pointer;
                        font-size: 14px;
                        font-weight: 500;
                        color: #666;
                        transition: all 0.3s ease;
                        white-space: nowrap;
                        border-bottom: 3px solid transparent;
                    }}
                    .tab-button:hover {{
                        background: #f8f9fa;
                        color: #333;
                    }}
                    .tab-button.active {{
                        color: #667eea;
                        border-bottom-color: #667eea;
                        background: #f8f9fa;
                    }}
                    .tab-content {{
                        background: white;
                        border-radius: 0 0 10px 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                        min-height: 400px;
                    }}
                    .tab-panel {{
                        display: none;
                        padding: 30px;
                        animation: fadeIn 0.3s ease-in-out;
                    }}
                    .tab-panel.active {{
                        display: block;
                    }}
                    @keyframes fadeIn {{
                        from {{ opacity: 0; transform: translateY(10px); }}
                        to {{ opacity: 1; transform: translateY(0); }}
                    }}
                    
                    @media (max-width: 768px) {{
                        .summary-cards {{
                            grid-template-columns: 1fr;
                        }}
                        .image-gallery {{
                            grid-template-columns: 1fr;
                        }}
                        .container {{
                            padding: 15px;
                        }}
                        .tab-button {{
                            padding: 12px 15px;
                            font-size: 12px;
                        }}
                        .tab-panel {{
                            padding: 20px;
                        }}
                    }}
                </style>
                <script>
                    function copyToClipboard(text) {{
                        navigator.clipboard.writeText(text).then(() => {{
                            alert('Link copied to clipboard!');
                        }});
                    }}
                    
                    function shareReport() {{
                        const url = window.location.href;
                        if (navigator.share) {{
                            navigator.share({{
                                title: 'Visual Regression Analysis Report',
                                text: 'Check out this visual regression analysis report',
                                url: url
                            }});
                        }} else {{
                            copyToClipboard(url);
                        }}
                    }}
                    
                    function downloadReport() {{
                        const link = document.createElement('a');
                        link.href = window.location.href.replace('.html', '_complete_package.zip');
                        link.download = 'visual_regression_report.zip';
                        link.click();
                    }}
                    
                    function emailReport() {{
                        const subject = encodeURIComponent('Visual Regression Analysis Report');
                        const body = encodeURIComponent('Please find the visual regression analysis report at: ' + window.location.href);
                        window.open('mailto:?subject=' + subject + '&body=' + body);
                    }}
                    
                    // Tab functionality
                    function showTab(tabId) {{
                        // Hide all tab panels
                        const panels = document.querySelectorAll('.tab-panel');
                        panels.forEach(panel => {{
                            panel.classList.remove('active');
                        }});
                        
                        // Remove active class from all tab buttons
                        const buttons = document.querySelectorAll('.tab-button');
                        buttons.forEach(button => {{
                            button.classList.remove('active');
                        }});
                        
                        // Show selected tab panel
                        const selectedPanel = document.getElementById(tabId);
                        if (selectedPanel) {{
                            selectedPanel.classList.add('active');
                        }}
                        
                        // Add active class to clicked button
                        const selectedButton = document.querySelector(`[onclick="showTab('${{tabId}}')"]`);
                        if (selectedButton) {{
                            selectedButton.classList.add('active');
                        }}
                    }}
                    
                    // Initialize first tab as active when page loads
                    document.addEventListener('DOMContentLoaded', function() {{
                        showTab('executive-summary');
                    }});
                    
                    // Image viewing functionality
                    function openImage(src) {{
                        // Create modal overlay
                        const modal = document.createElement('div');
                        modal.style.cssText = `
                            position: fixed;
                            top: 0;
                            left: 0;
                            width: 100%;
                            height: 100%;
                            background: rgba(0, 0, 0, 0.9);
                            z-index: 10000;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            cursor: pointer;
                        `;
                        
                        // Create image element
                        const img = document.createElement('img');
                        img.src = src;
                        img.style.cssText = `
                            max-width: 95%;
                            max-height: 95%;
                            object-fit: contain;
                            border-radius: 8px;
                            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
                        `;
                        
                        // Create close button
                        const closeBtn = document.createElement('button');
                        closeBtn.innerHTML = '✕';
                        closeBtn.style.cssText = `
                            position: absolute;
                            top: 20px;
                            right: 20px;
                            background: rgba(255, 255, 255, 0.9);
                            border: none;
                            border-radius: 50%;
                            width: 40px;
                            height: 40px;
                            font-size: 20px;
                            cursor: pointer;
                            z-index: 10001;
                        `;
                        
                        // Add elements to modal
                        modal.appendChild(img);
                        modal.appendChild(closeBtn);
                        
                        // Add event listeners
                        modal.addEventListener('click', function(e) {{
                            if (e.target === modal || e.target === closeBtn) {{
                                document.body.removeChild(modal);
                            }}
                        }});
                        
                        // Add to page
                        document.body.appendChild(modal);
                        
                        // Prevent body scroll
                        document.body.style.overflow = 'hidden';
                        
                        // Restore body scroll when modal is closed
                        modal.addEventListener('click', function() {{
                            document.body.style.overflow = 'auto';
                        }});
                    }}
                    
                    // Alternative simple function for opening in new tab
                    function openImageNewTab(src) {{
                        window.open(src, '_blank');
                    }}
                </script>
            </head>
            <body>
                <div class="header">
                    <h1>🔍 Visual Regression Analysis Report</h1>
                    <p>Generated on: {timestamp}</p>
                    <p>Comprehensive comparison between two web pages</p>
                </div>
                
                <div class="sharing-buttons">
                    <h3>📤 Share This Report</h3>
                    <button class="share-btn" onclick="shareReport()">📱 Share</button>
                    <button class="share-btn" onclick="emailReport()">📧 Email</button>
                    <button class="share-btn" onclick="downloadReport()">📦 Download Package</button>
                    <button class="share-btn" onclick="copyToClipboard(window.location.href)">🔗 Copy Link</button>
                </div>

                <div class="container">
                    <!-- Tab Navigation -->
                    <div class="tab-navigation">
                        <button class="tab-button active" onclick="showTab('executive-summary')">📊 Executive Summary</button>
                        <button class="tab-button" onclick="showTab('visual-comparison')">🖼️ Visual Comparison</button>
                        <button class="tab-button" onclick="showTab('detailed-analysis')">📈 Detailed Analysis</button>
                        <button class="tab-button" onclick="showTab('wcag-compliance')">♿ WCAG Compliance</button>
                        <button class="tab-button" onclick="showTab('detailed-findings')">📋 Detailed Findings</button>
                        <button class="tab-button" onclick="showTab('configuration-settings')">⚙️ Configuration</button>
                        <button class="tab-button" onclick="showTab('export-options')">💾 Export Options</button>
                        <button class="tab-button" onclick="showTab('report-info')">ℹ️ Report Info</button>
                    </div>

                    <!-- Tab Content -->
                    <div class="tab-content">
                        <!-- Executive Summary Tab -->
                        <div id="executive-summary" class="tab-panel active">
                            <h2>📊 Executive Summary</h2>
                            <div class="summary-cards">
                                <div class="card">
                                    <h3>Overall Similarity</h3>
                                    <div class="number">{summary.get('similarity_score', 0):.1%}</div>
                                    <span class="status-badge {'status-pass' if summary.get('similarity_score', 0) > 0.9 else 'status-warning' if summary.get('similarity_score', 0) > 0.7 else 'status-fail'}">
                                        {'PASS' if summary.get('similarity_score', 0) > 0.9 else 'WARNING' if summary.get('similarity_score', 0) > 0.7 else 'FAIL'}
                                    </span>
                                </div>
                                <div class="card">
                                    <h3>Layout Differences</h3>
                                    <div class="number">{summary.get('layout_differences', 0)}</div>
                                    <span class="status-badge {'status-pass' if summary.get('layout_differences', 0) == 0 else 'status-warning' if summary.get('layout_differences', 0) < 5 else 'status-fail'}">
                                        {'PASS' if summary.get('layout_differences', 0) == 0 else 'WARNING' if summary.get('layout_differences', 0) < 5 else 'FAIL'}
                                    </span>
                                </div>
                                <div class="card">
                                    <h3>Color Changes</h3>
                                    <div class="number">{summary.get('color_differences', 0)}</div>
                                    <span class="status-badge {'status-pass' if summary.get('color_differences', 0) == 0 else 'status-warning' if summary.get('color_differences', 0) < 3 else 'status-fail'}">
                                        {'PASS' if summary.get('color_differences', 0) == 0 else 'WARNING' if summary.get('color_differences', 0) < 3 else 'FAIL'}
                                    </span>
                                </div>
                                <div class="card">
                                    <h3>Element Changes</h3>
                                    <div class="number">{summary.get('element_changes', 0)}</div>
                                    <span class="status-badge {'status-pass' if summary.get('element_changes', 0) == 0 else 'status-warning' if summary.get('element_changes', 0) < 3 else 'status-fail'}">
                                        {'PASS' if summary.get('element_changes', 0) == 0 else 'WARNING' if summary.get('element_changes', 0) < 3 else 'FAIL'}
                                    </span>
                                </div>
                                <div class="card">
                                    <h3>AI Anomalies</h3>
                                    <div class="number">{summary.get('ai_anomalies', 0)}</div>
                                    <span class="status-badge {'status-pass' if summary.get('ai_anomalies', 0) == 0 else 'status-warning' if summary.get('ai_anomalies', 0) < 3 else 'status-fail'}">
                                        {'PASS' if summary.get('ai_anomalies', 0) == 0 else 'WARNING' if summary.get('ai_anomalies', 0) < 3 else 'FAIL'}
                                    </span>
                                </div>
                            </div>
                        </div>

                        <!-- Visual Comparison Tab -->
                        <div id="visual-comparison" class="tab-panel">
                            <h2>🖼️ Visual Comparison</h2>
                            <div class="image-gallery">
                                <div class="image-container">
                                    <h4>📱 Original (URL 1)</h4>
                                    {url1_screenshot_html}
                                    <p style="font-size: 12px; color: #666; margin-top: 10px; padding: 8px; background: #f8f9fa; border-radius: 4px;">
                                        <strong>📋 Description:</strong> Full-page screenshot of the original URL captured using headless Chrome browser. 
                                        This serves as the baseline for comparison analysis.
                                    </p>
                                </div>
                                <div class="image-container">
                                    <h4>📱 Comparison (URL 2)</h4>
                                    {url2_screenshot_html}
                                    <p style="font-size: 12px; color: #666; margin-top: 10px; padding: 8px; background: #f8f9fa; border-radius: 4px;">
                                        <strong>📋 Description:</strong> Full-page screenshot of the comparison URL captured under identical conditions. 
                                        This is compared against the original to detect visual differences.
                                    </p>
                                </div>
                                <div class="image-container">
                                    <h4>🔍 Side-by-side Comparison</h4>
                                    {sidebyside_html}
                                    <p style="font-size: 12px; color: #666; margin-top: 10px; padding: 8px; background: #e3f2fd; border-radius: 4px;">
                                        <strong>📋 Description:</strong> Direct side-by-side view of both screenshots for easy manual comparison. 
                                        The original URL is displayed on the left, and the comparison URL on the right. 
                                        This view helps quickly identify visual layout differences, content changes, and styling variations.
                                    </p>
                                </div>
                                <div class="image-container">
                                    <h4>🌡️ Difference Heatmap</h4>
                                    {heatmap_html}
                                    <p style="font-size: 12px; color: #666; margin-top: 10px; padding: 8px; background: #fff3e0; border-radius: 4px;">
                                        <strong>📋 Description:</strong> Color-coded heatmap showing pixel-level differences between the two images. 
                                        <span style="color: #d32f2f;">Red areas</span> indicate significant differences, 
                                        <span style="color: #f57c00;">orange/yellow areas</span> show moderate changes, and 
                                        <span style="color: #1976d2;">blue areas</span> represent minor variations. 
                                        Identical regions remain unchanged. This visualization helps quantify the extent and location of visual changes.
                                    </p>
                                </div>
                                <div class="image-container">
                                    <h4>🎯 AI-Enhanced Comparison</h4>
                                    {visual_html}
                                    <p style="font-size: 12px; color: #666; margin-top: 10px; padding: 8px; background: #e8f5e8; border-radius: 4px;">
                                        <strong>📋 Description:</strong> AI-powered analysis with automated difference detection and bounding boxes. 
                                        <span style="color: #2e7d32;">Green rectangles</span> highlight areas where the AI detected significant changes including 
                                        layout shifts, color differences, missing elements, and new content. Each bounding box represents a region 
                                        that requires attention during regression testing. The AI considers both visual similarity and semantic content changes.
                                    </p>
                                </div>
                            </div>
                        </div>

                        <!-- Detailed Analysis Tab -->
                        <div id="detailed-analysis" class="tab-panel">
                            <h2>📈 Detailed Analysis</h2>
                            {analysis_sections_html}
                        </div>

                        <!-- WCAG Compliance Tab -->
                        <div id="wcag-compliance" class="tab-panel">
                            {wcag_section_html}
                        </div>

                        <!-- Detailed Findings Tab -->
                        <div id="detailed-findings" class="tab-panel">
                            <h2>📋 Detailed Findings</h2>
                            {detailed_findings_html}
                        </div>

                        <!-- Configuration Settings Tab -->
                        <div id="configuration-settings" class="tab-panel">
                            <h2>⚙️ Configuration Settings</h2>
                            {configuration_settings_html}
                        </div>

                        <!-- Export Options Tab -->
                        <div id="export-options" class="tab-panel">
                            <h2>💾 Export Options</h2>
                            <p>Download different formats of this report:</p>
                            <div style="margin: 15px 0;">
                                {export_pdf_link}
                                {export_json_link}
                                {export_package_link}
                            </div>
                            <p style="font-size: 0.9em; color: #6c757d; margin-top: 10px;">
                                <em>💡 Note: Files are generated alongside this HTML report. Download links will work when accessing from the same location.</em>
                            </p>
                        </div>

                        <!-- Report Information Tab -->
                        <div id="report-info" class="tab-panel">
                            <h2>ℹ️ Report Information</h2>
                            <p><strong>Generated:</strong> {timestamp}</p>
                            <p><strong>Tool:</strong> Visual AI Regression Module v1.0</p>
                            <p><strong>Analysis Duration:</strong> {analysis_results.get('duration', 'N/A')}</p>
                        </div>
                    </div>
                </div>
            </body>
            </html>
            """
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            self.logger.info(f"Enhanced HTML report generated: {output_path}")
            
        except Exception as e:
            self.logger.error(f"Failed to generate enhanced HTML report: {str(e)}")
            raise

    def _generate_findings_html(self, analysis_results, ai_analysis, config=None):
        """Generate HTML for detailed findings based on enabled analysis types"""
        html = ""
        
        # Layout findings (only if enabled)
        if config is None or config.get('layout_shift', True):
            layout_shifts = analysis_results.get('layout_shifts', [])
            if layout_shifts:
                html += '<div class="difference-highlight">'
                html += '<h4>🏗️ Layout Shifts Detected</h4>'
                for i, shift in enumerate(layout_shifts[:5]):  # Show first 5
                    html += f'<p><strong>Shift {i+1}:</strong> {shift}</p>'
                if len(layout_shifts) > 5:
                    html += f'<p><em>... and {len(layout_shifts) - 5} more</em></p>'
                html += '</div>'
        
        # Color findings (only if enabled)
        if config is None or config.get('font_color', True):
            color_diffs = analysis_results.get('color_differences', [])
            if color_diffs:
                html += '<div class="difference-highlight">'
                html += '<h4>🎨 Color Differences</h4>'
                for i, diff in enumerate(color_diffs[:5]):
                    html += f'<p><strong>Change {i+1}:</strong> {diff}</p>'
                if len(color_diffs) > 5:
                    html += f'<p><em>... and {len(color_diffs) - 5} more</em></p>'
                html += '</div>'
        
        # Element detection findings (only if enabled)
        if config is None or config.get('element_detection', True):
            missing_elements = analysis_results.get('missing_elements', [])
            new_elements = analysis_results.get('new_elements', [])
            overlapping_elements = analysis_results.get('overlapping_elements', [])
            
            if missing_elements or new_elements or overlapping_elements:
                html += '<div class="difference-highlight">'
                html += '<h4>🔍 Element Changes</h4>'
                if missing_elements:
                    html += f'<p><strong>Missing Elements:</strong> {len(missing_elements)}</p>'
                if new_elements:
                    html += f'<p><strong>New Elements:</strong> {len(new_elements)}</p>'
                if overlapping_elements:
                    html += f'<p><strong>Overlapping Elements:</strong> {len(overlapping_elements)}</p>'
                html += '</div>'
        
        # AI findings (only if enabled)
        if config is None or config.get('ai_analysis', True):
            anomalies = ai_analysis.get('anomalies', [])
            if anomalies:
                html += '<div class="difference-highlight">'
                html += '<h4>🤖 AI-Detected Anomalies</h4>'
                for i, anomaly in enumerate(anomalies[:5]):
                    html += f'<p><strong>Anomaly {i+1}:</strong> {anomaly}</p>'
                if len(anomalies) > 5:
                    html += f'<p><em>... and {len(anomalies) - 5} more</em></p>'
                html += '</div>'
        
        if not html:
            html = '<p>✅ No significant differences detected!</p>'
        
        return html
    
    def _generate_configuration_settings_html(self, analysis_results, config):
        """Generate configuration settings section HTML"""
        html = '<div class="configuration-section">'
        
        # Analysis Configuration
        html += '''
            <div class="config-category">
                <h3>🔧 Analysis Configuration</h3>
                <div class="config-grid">
        '''
        
        # Analysis type and basic settings
        analysis_type = config.get('analysis_type', 'Standard Visual Regression')
        urls = config.get('urls', {})
        url1 = urls.get('url1', 'N/A') if isinstance(urls, dict) else 'N/A'
        url2 = urls.get('url2', 'N/A') if isinstance(urls, dict) else 'N/A'
        
        html += f'''
                    <div class="config-item">
                        <span class="config-label">Analysis Type:</span>
                        <span class="config-value">{analysis_type}</span>
                    </div>
                    <div class="config-item">
                        <span class="config-label">Original URL:</span>
                        <span class="config-value">{url1}</span>
                    </div>
                    <div class="config-item">
                        <span class="config-label">Comparison URL:</span>
                        <span class="config-value">{url2}</span>
                    </div>
        '''
        
        # Analysis Options
        html += '''
                </div>
            </div>
            <div class="config-category">
                <h3>⚙️ Analysis Options</h3>
                <div class="config-grid">
        '''
        
        # Feature toggles
        features = {
            'Visual Comparison': config.get('visual_comparison', True),
            'AI Analysis': config.get('ai_analysis', True),
            'WCAG Compliance': config.get('wcag_analysis', True),
            'Layout Detection': config.get('layout_analysis', True),
            'Color Analysis': config.get('color_analysis', True),
            'Font Analysis': config.get('font_analysis', True),
            'Screenshot Capture': config.get('capture_screenshots', True),
            'Detailed Logging': config.get('detailed_logging', False)
        }
        
        for feature_name, enabled in features.items():
            status = "✅ Enabled" if enabled else "❌ Disabled"
            html += f'''
                    <div class="config-item">
                        <span class="config-label">{feature_name}:</span>
                        <span class="config-value {('enabled' if enabled else 'disabled')}">{status}</span>
                    </div>
            '''
        
        # Technical Settings
        html += '''
                </div>
            </div>
            <div class="config-category">
                <h3>🛠️ Technical Settings</h3>
                <div class="config-grid">
        '''
        
        # Technical parameters
        tech_settings = {
            'Browser': config.get('browser', 'Chrome'),
            'Viewport Width': f"{config.get('viewport_width', 1920)}px",
            'Viewport Height': f"{config.get('viewport_height', 1080)}px",
            'Wait Time': f"{config.get('wait_time', 3)} seconds",
            'Image Format': config.get('image_format', 'PNG'),
            'Similarity Threshold': f"{config.get('similarity_threshold', 0.95)*100:.1f}%",
            'Comparison Method': config.get('comparison_method', 'SSIM + MSE + PSNR'),
            'Report Format': config.get('report_format', 'HTML + PDF + JSON')
        }
        
        for setting_name, value in tech_settings.items():
            html += f'''
                    <div class="config-item">
                        <span class="config-label">{setting_name}:</span>
                        <span class="config-value">{value}</span>
                    </div>
            '''
        
        # Analysis Metrics Used
        html += '''
                </div>
            </div>
            <div class="config-category">
                <h3>📊 Metrics & Algorithms</h3>
                <div class="metrics-info">
        '''
        
        metrics_info = [
            ("SSIM (Structural Similarity Index)", "Measures structural similarity between images (0-1 scale)"),
            ("MSE (Mean Squared Error)", "Calculates pixel-level differences (lower is better)"),
            ("PSNR (Peak Signal-to-Noise Ratio)", "Measures image quality in decibels (higher is better)"),
            ("Pixel Difference Analysis", "Counts exact pixel differences between images"),
            ("AI-Powered Detection", "Machine learning algorithms for anomaly detection"),
            ("WCAG 2.1/2.2 Compliance", "Accessibility guidelines compliance testing")
        ]
        
        for metric_name, description in metrics_info:
            html += f'''
                    <div class="metric-info">
                        <strong>{metric_name}:</strong> {description}
                    </div>
            '''
        
        # Environment Information
        html += '''
                </div>
            </div>
            <div class="config-category">
                <h3>🌐 Environment Information</h3>
                <div class="config-grid">
        '''
        
        import platform
        import sys
        
        env_info = {
            'Platform': platform.system() + " " + platform.release(),
            'Python Version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            'Module Version': "Visual AI Regression v6.0 (August 2025)",
            'Analysis Timestamp': analysis_results.get('timestamp', 'N/A'),
            'Analysis Duration': analysis_results.get('duration', 'N/A'),
            'Total Screenshots': len(analysis_results.get('screenshots', {})),
            'Total Comparisons': len(analysis_results.get('comparisons', {}))
        }
        
        for info_name, value in env_info.items():
            html += f'''
                    <div class="config-item">
                        <span class="config-label">{info_name}:</span>
                        <span class="config-value">{value}</span>
                    </div>
            '''
        
        html += '''
                </div>
            </div>
        </div>
        
        <style>
            .configuration-section {
                max-width: 100%;
                margin: 20px 0;
            }
            .config-category {
                background: #f8f9fa;
                border-left: 4px solid #007bff;
                padding: 20px;
                margin: 20px 0;
                border-radius: 5px;
            }
            .config-category h3 {
                margin: 0 0 15px 0;
                color: #007bff;
                font-size: 1.2em;
            }
            .config-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 10px;
                margin-top: 15px;
            }
            .config-item {
                display: flex;
                justify-content: space-between;
                padding: 8px 12px;
                background: white;
                border-radius: 4px;
                border: 1px solid #e0e0e0;
            }
            .config-label {
                font-weight: bold;
                color: #495057;
                flex: 1;
            }
            .config-value {
                color: #28a745;
                font-family: monospace;
                text-align: right;
                flex: 1;
            }
            .config-value.disabled {
                color: #dc3545;
            }
            .config-value.enabled {
                color: #28a745;
            }
            .metrics-info {
                margin-top: 15px;
            }
            .metric-info {
                padding: 10px;
                background: white;
                border-radius: 4px;
                margin: 8px 0;
                border-left: 3px solid #17a2b8;
            }
            .metric-info strong {
                color: #17a2b8;
            }
        </style>
        '''
        
        return html
    
    def _generate_analysis_sections_html(self, analysis_results, ai_analysis, config):
        """Generate conditional analysis sections based on enabled options"""
        html = ""
        
        # Image similarity metrics (always included)
        html += '''
                        <div class="analysis-details">
                            <h3>🔍 Image Similarity Metrics</h3>
                            <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
                                <p style="margin: 0 0 10px 0; font-weight: bold; color: #495057;">📚 Metric Definitions:</p>
                                <div style="font-size: 14px; color: #6c757d; line-height: 1.6;">
                                    <p style="margin: 5px 0;"><strong>SSIM (Structural Similarity Index):</strong> Measures how similar the structure, luminance, and contrast are between images. Values range from 0 to 1, where 1 means identical images.</p>
                                    <p style="margin: 5px 0;"><strong>MSE (Mean Squared Error):</strong> Calculates the average squared differences between pixel values. Lower values indicate greater similarity, with 0 meaning identical images.</p>
                                    <p style="margin: 5px 0;"><strong>PSNR (Peak Signal-to-Noise Ratio):</strong> Measures signal quality in decibels. Higher values indicate better quality/similarity.</p>
                                    <p style="margin: 5px 0;"><strong>Pixel Difference:</strong> Shows the percentage of pixels that differ between the two images, providing a straightforward measure of visual change.</p>
                                </div>
                            </div>
                            
                            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 15px; margin-bottom: 15px;">
                                <div style="text-align: center; padding: 15px; background-color: #e3f2fd; border-radius: 8px;">
                                    <div style="font-size: 20px; font-weight: bold, color: #1976d2;">{ssim:.4f}</div>
                                    <div style="font-weight: bold; color: #1976d2; margin: 5px 0;">SSIM Score</div>
                                    <div style="font-size: 12px; color: #616161;">
                                        {ssim_interpretation}
                                    </div>
                                </div>
                                <div style="text-align: center; padding: 15px; background-color: #f3e5f5; border-radius: 8px;">
                                    <div style="font-size: 20px; font-weight: bold, color: #7b1fa2;">{mse:.6f}</div>
                                    <div style="font-weight: bold; color: #7b1fa2; margin: 5px 0;">MSE Score</div>
                                    <div style="font-size: 12px; color: #616161;">
                                        {mse_interpretation}
                                    </div>
                                </div>
                                <div style="text-align: center; padding: 15px; background-color: #fff3e0; border-radius: 8px;">
                                    <div style="font-size: 20px; font-weight: bold, color: #f57c00;">{psnr:.2f} dB</div>
                                    <div style="font-weight: bold; color: #f57c00; margin: 5px 0;">PSNR Score</div>
                                    <div style="font-size: 12px; color: #616161;">
                                        {psnr_interpretation}
                                    </div>
                                </div>
                                <div style="text-align: center; padding: 15px; background-color: #e8f5e8; border-radius: 8px;">
                                    <div style="font-size: 20px; font-weight: bold, color: #388e3c;">{pixel_diff:.2f}%</div>
                                    <div style="font-weight: bold; color: #388e3c; margin: 5px 0;">Pixel Difference</div>
                                    <div style="font-size: 12px; color: #616161;">
                                        {pixel_interpretation}
                                    </div>
                                </div>
                            </div>
                            
                            <div style="background-color: #fff3cd; border: 1px solid #ffeaa7; border-radius: 5px; padding: 12px; margin-top: 15px;">
                                <p style="margin: 0; font-size: 14px; color: #856404;">
                                    <strong>💡 Interpretation Guide:</strong> 
                                    <span style="color: #28a745;">●</span> Excellent (SSIM >0.95, MSE <0.01) | 
                                    <span style="color: #ffc107;">●</span> Good (SSIM 0.85-0.95, MSE 0.01-0.1) | 
                                    <span style="color: #dc3545;">●</span> Poor (SSIM <0.85, MSE >0.1)
                                </p>
                            </div>
                        </div>
        '''.format(
            ssim=analysis_results.get('ssim', 0),
            mse=analysis_results.get('mse', 0),
            psnr=analysis_results.get('psnr', 0),
            pixel_diff=analysis_results.get('pixel_metrics', {}).get('pixel_difference_percentage', 0),
            ssim_interpretation=self._get_ssim_interpretation(analysis_results.get('ssim', 0)),
            mse_interpretation=self._get_mse_interpretation(analysis_results.get('mse', 0)),
            psnr_interpretation=self._get_psnr_interpretation(analysis_results.get('psnr', 0)),
            pixel_interpretation=self._get_pixel_interpretation(analysis_results.get('pixel_metrics', {}).get('pixel_difference_percentage', 0))
        )
        
        # Layout analysis (only if enabled)
        if config.get('layout_shift', True) and ('layout_shifts' in analysis_results):
            html += '''
                        <div class="analysis-details">
                            <h3>🏗️ Layout Analysis Results</h3>
                            <p><strong>Layout Shifts Detected:</strong> <span class="metric-value">{layout_shifts}</span></p>
                        </div>
            '''.format(
                layout_shifts=len(analysis_results.get('layout_shifts', []))
            )
        
        # Element detection analysis (only if enabled)
        if config.get('element_detection', True) and ('missing_elements' in analysis_results or 'new_elements' in analysis_results):
            html += '''
                        <div class="analysis-details">
                            <h3>🔍 Element Detection Results</h3>
                            <p><strong>Missing Elements:</strong> <span class="metric-value">{missing_elements}</span></p>
                            <p><strong>New Elements:</strong> <span class="metric-value">{new_elements}</span></p>
                            <p><strong>Overlapping Elements:</strong> <span class="metric-value">{overlapping_elements}</span></p>
                        </div>
            '''.format(
                missing_elements=len(analysis_results.get('missing_elements', [])),
                new_elements=len(analysis_results.get('new_elements', [])),
                overlapping_elements=len(analysis_results.get('overlapping_elements', []))
            )
        
        # Color & font analysis (only if enabled)
        if config.get('font_color', True) and ('color_differences' in analysis_results):
            html += '''
                        <div class="analysis-details">
                            <h3>🎨 Color & Font Analysis</h3>
                            <p><strong>Color Differences:</strong> <span class="metric-value">{color_differences}</span></p>
                        </div>
            '''.format(
                color_differences=len(analysis_results.get('color_differences', []))
            )
        
        # AI analysis (only if enabled)
        if config.get('ai_analysis', True) and ai_analysis:
            html += '''
                        <div class="analysis-details">
                            <h3>🤖 AI Analysis Results</h3>
                            <p><strong>Anomalies Detected:</strong> <span class="metric-value">{anomalies}</span></p>
                            <p><strong>Confidence Score:</strong> <span class="metric-value">{confidence:.2f}</span></p>
                        </div>
            '''.format(
                anomalies=len(ai_analysis.get('anomalies', [])),
                confidence=ai_analysis.get('confidence', 0)
            )
        
        return html

    def generate_pdf_report(self, analysis_results, config, output_path):
        """Generate PDF report"""
        try:
            doc = SimpleDocTemplate(output_path, pagesize=A4)
            styles = getSampleStyleSheet()
            story = []
            
            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                spaceAfter=30,
                textColor=colors.HexColor('#667eea'),
                alignment=1  # Center alignment
            )
            story.append(Paragraph("Visual Regression Analysis Report", title_style))
            story.append(Spacer(1, 20))
            
            # Timestamp
            story.append(Paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", styles['Normal']))
            story.append(Spacer(1, 30))
            
            # Configuration Section
            story.append(Paragraph("Configuration", styles['Heading2']))
            config_data = [
                ['Parameter', 'Value'],
                ['Reference URL', config.get('url1', 'N/A')],
                ['Test URL', config.get('url2', 'N/A')],
                ['Browser', config.get('browser', 'N/A')],
                ['Resolution', config.get('resolution', 'N/A')],
                ['Layout Shift Detection', 'Enabled' if config.get('layout_shift', False) else 'Disabled'],
                ['Font/Color Analysis', 'Enabled' if config.get('font_color', False) else 'Disabled'],
                ['Element Detection', 'Enabled' if config.get('element_detection', False) else 'Disabled'],
                ['AI Analysis', 'Enabled' if config.get('ai_analysis', False) else 'Disabled'],
                ['WCAG Compliance', 'Enabled' if config.get('wcag_analysis', False) else 'Disabled']
            ]
            
            config_table = Table(config_data)
            config_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(config_table)
            story.append(Spacer(1, 30))
            
            # Summary Section
            story.append(Paragraph("Summary", styles['Heading2']))
            summary_data = [
                ['Metric', 'Value'],
                ['Overall Similarity', f"{analysis_results.get('similarity_score', 0):.1%}"],
                ['Layout Shifts', str(len(analysis_results.get('layout_shifts', [])))],
                ['Color Differences', str(len(analysis_results.get('color_differences', [])))],
                ['Missing Elements', str(len(analysis_results.get('missing_elements', [])))],
                ['New Elements', str(len(analysis_results.get('new_elements', [])))]
            ]
            
            summary_table = Table(summary_data)
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(summary_table)
            story.append(Spacer(1, 30))
            
            # Detailed Analysis Sections
            self._add_detailed_analysis_to_pdf(story, analysis_results, styles)
            
            # Visual Comparison Screenshots
            story.append(Paragraph("Visual Comparison Screenshots", styles['Heading2']))
            reports = analysis_results.get('reports', {})
            img_paths = [
                (reports.get('sidebyside'), 'Side-by-Side Comparison'),
                (reports.get('heatmap'), 'Difference Heatmap'),
                (reports.get('visual'), 'Annotated/Overlay Comparison')
            ]
            for img_path, caption in img_paths:
                if img_path and os.path.exists(img_path):
                    story.append(Paragraph(caption, styles['Heading3']))
                    story.append(RLImage(img_path, width=400, height=220))
                    story.append(Spacer(1, 10))
            story.append(Spacer(1, 20))
            
            # Build PDF
            doc.build(story)
            self.logger.info(f"PDF report saved to: {output_path}")
            
        except Exception as e:
            self.logger.error(f"Failed to generate PDF report: {str(e)}")
            raise
    
    def _add_detailed_analysis_to_pdf(self, story, results, styles):
        """Add detailed analysis sections to PDF"""
        # Layout Shifts
        if 'layout_shifts' in results and results['layout_shifts']:
            story.append(Paragraph("Layout Shifts", styles['Heading2']))
            for i, shift in enumerate(results['layout_shifts'][:5]):  # Limit to top 5
                story.append(Paragraph(f"Shift #{i+1}:", styles['Heading3']))
                story.append(Paragraph(f"Movement Distance: {shift.get('distance', 0):.1f} pixels", styles['Normal']))
                story.append(Paragraph(f"Shift: X: {shift.get('shift_x', 0)}px, Y: {shift.get('shift_y', 0)}px", styles['Normal']))
                story.append(Spacer(1, 10))
        
        # Color Differences
        if 'color_differences' in results and results['color_differences']:
            story.append(Paragraph("Color Differences", styles['Heading2']))
            for i, diff in enumerate(results['color_differences'][:5]):  # Limit to top 5
                story.append(Paragraph(f"Difference #{i+1}:", styles['Heading3']))
                story.append(Paragraph(f"Color Distance: {diff.get('color_distance', 0):.1f}", styles['Normal']))
                story.append(Paragraph(f"Area: {diff.get('area', 0):.1f} pixels²", styles['Normal']))
                story.append(Spacer(1, 10))
        
        # AI Analysis
        if 'ai_analysis' in results and results['ai_analysis']:
            story.append(Paragraph("AI Analysis", styles['Heading2']))
            ai = results['ai_analysis']
            story.append(Paragraph(f"Anomaly Detected: {'Yes' if ai.get('anomaly_detected', False) else 'No'}", styles['Normal']))
            story.append(Paragraph(f"Feature Distance: {ai.get('feature_distance', 0):.4f}", styles['Normal']))
            story.append(Paragraph(f"Confidence: {ai.get('confidence', 0):.1%}", styles['Normal']))
    
    def generate_json_report(self, analysis_results, config, output_path):
        """Generate JSON report for programmatic access"""
        try:
            report_data = {
                'metadata': {
                    'generated_at': datetime.now().isoformat(),
                    'report_version': '1.0',
                    'generator': 'Visual AI Regression Module'
                },
                'configuration': config,
                'analysis_results': analysis_results,
                'summary': {
                    'total_differences': (
                        len(analysis_results.get('layout_shifts', [])) +
                        len(analysis_results.get('color_differences', [])) +
                        len(analysis_results.get('missing_elements', [])) +
                        len(analysis_results.get('new_elements', []))
                    ),
                    'similarity_score': analysis_results.get('similarity_score', 0),
                    'has_significant_changes': analysis_results.get('similarity_score', 1) < 0.95
                }
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, default=str)
            
            self.logger.info(f"JSON report saved to: {output_path}")
            
        except Exception as e:
            self.logger.error(f"Failed to generate JSON report: {str(e)}")
            raise
    
    def generate_enhanced_visual_comparison(self, analysis_results, output_path):
        """Generate enhanced visual comparison with annotations"""
        try:
            # First priority: Use annotated comparison if available (this is the enhanced visual comparison)
            if 'annotated_comparison_path' in analysis_results and os.path.exists(analysis_results['annotated_comparison_path']):
                import shutil
                shutil.copy2(analysis_results['annotated_comparison_path'], output_path)
                self.logger.info(f"Enhanced visual comparison (annotated) copied to: {output_path}")
                return output_path
            
            # Fallback: Try to create annotated comparison from available data
            screenshots = analysis_results.get('screenshots', {})
            comparisons = analysis_results.get('comparisons', {})
            
            if screenshots.get('url1') and screenshots.get('url2'):
                self._create_annotated_comparison_from_data(analysis_results, output_path)
                return output_path
            else:
                # Create a placeholder image
                self._create_placeholder_image(output_path, "Enhanced Visual Comparison", 
                                             "Annotated comparison with AI-detected differences and bounding boxes.\nThis image will be available after running a complete visual analysis.")
                return output_path
                
        except Exception as e:
            self.logger.error(f"Failed to generate enhanced visual comparison: {str(e)}")
            self._create_placeholder_image(output_path, "Enhanced Visual Comparison", 
                                         f"Error generating annotated comparison: {str(e)}")
            return output_path

    def generate_side_by_side_comparison(self, analysis_results, output_path):
        """Generate side-by-side comparison image"""
        try:
            # Create side-by-side from screenshots (NOT from annotated comparison)
            screenshots = analysis_results.get('screenshots', {})
            url1_screenshot = screenshots.get('url1')
            url2_screenshot = screenshots.get('url2')
            
            if url1_screenshot and url2_screenshot and os.path.exists(url1_screenshot) and os.path.exists(url2_screenshot):
                self._create_side_by_side_from_screenshots(url1_screenshot, url2_screenshot, output_path)
                self.logger.info(f"Side-by-side comparison created from screenshots: {output_path}")
                return output_path
            else:
                # Create placeholder with specific side-by-side description
                self._create_placeholder_image(output_path, "Side-by-Side Comparison", 
                                             "Reference and test screenshots placed side-by-side for direct comparison.\nThis image will be available after capturing screenshots.")
                return output_path
                
        except Exception as e:
            self.logger.error(f"Failed to generate side-by-side comparison: {str(e)}")
            self._create_placeholder_image(output_path, "Side-by-Side Comparison", 
                                         f"Error generating side-by-side comparison: {str(e)}")
            return output_path

    def generate_difference_heatmap(self, analysis_results, output_path):
        """Generate difference heatmap image"""
        try:
            # First priority: Use existing heatmap from analysis
            if 'heatmap_path' in analysis_results and os.path.exists(analysis_results['heatmap_path']):
                import shutil
                shutil.copy2(analysis_results['heatmap_path'], output_path)
                self.logger.info(f"Difference heatmap copied to: {output_path}")
                return output_path
            
            # Fallback: Try to create heatmap from screenshot data
            screenshots = analysis_results.get('screenshots', {})
            if screenshots.get('url1') and screenshots.get('url2'):
                self._create_heatmap_from_screenshots(analysis_results, output_path)
                return output_path
            else:
                # Create placeholder with specific heatmap description
                self._create_placeholder_image(output_path, "Difference Heatmap", 
                                             "Heat-mapped overlay showing pixel-level differences.\nRed/warm colors indicate differences, cool colors show similarity.\nThis heatmap will be available after running visual comparison analysis.")
                return output_path
                
        except Exception as e:
            self.logger.error(f"Failed to generate difference heatmap: {str(e)}")
            self._create_placeholder_image(output_path, "Difference Heatmap", 
                                         f"Error generating heatmap: {str(e)}")
            return output_path

    def _create_side_by_side_from_screenshots(self, img1_path, img2_path, output_path):
        """Create side-by-side comparison from screenshot paths"""
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # Load images
            img1 = Image.open(img1_path)
            img2 = Image.open(img2_path)
            
            # Resize to same height
            max_height = max(img1.height, img2.height)
            if img1.height != max_height:
                img1 = img1.resize((int(img1.width * max_height / img1.height), max_height), Image.Resampling.LANCZOS)
            if img2.height != max_height:
                img2 = img2.resize((int(img2.width * max_height / img2.height), max_height), Image.Resampling.LANCZOS)
            
            # Create combined image
            gap = 20
            total_width = img1.width + img2.width + gap
            combined = Image.new('RGB', (total_width, max_height), 'white')
            
            # Paste images
            combined.paste(img1, (0, 0))
            combined.paste(img2, (img1.width + gap, 0))
            
            # Add labels
            draw = ImageDraw.Draw(combined)
            try:
                font = ImageFont.truetype("arial.ttf", 20)
            except:
                font = ImageFont.load_default()
            
            # Add "Reference" and "Test" labels
            draw.text((10, 10), "Reference", fill='blue', font=font)
            draw.text((img1.width + gap + 10, 10), "Test", fill='red', font=font)
            
            # Save
            combined.save(output_path, 'PNG', quality=95)
            self.logger.info(f"Side-by-side comparison created: {output_path}")
            
        except Exception as e:
            self.logger.error(f"Failed to create side-by-side from screenshots: {str(e)}")
            self._create_placeholder_image(output_path, "Side-by-Side Comparison", 
                                         f"Error creating comparison: {str(e)}")

    def _create_placeholder_image(self, output_path, title, description):
        """Create a placeholder image when actual comparison is not available"""
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # Create placeholder image
            width, height = 800, 400
            img = Image.new('RGB', (width, height), '#f8f9fa')
            draw = ImageDraw.Draw(img)
            
            # Try to load fonts
            try:
                title_font = ImageFont.truetype("arial.ttf", 24)
                desc_font = ImageFont.truetype("arial.ttf", 16)
            except:
                title_font = ImageFont.load_default()
                desc_font = ImageFont.load_default()
            
            # Draw border
            draw.rectangle([10, 10, width-10, height-10], outline='#dee2e6', width=3)
            
            # Draw icon (camera emoji replacement)
            draw.text((width//2 - 20, height//2 - 80), "📊", font=title_font, anchor="mm")
            
            # Draw title
            title_bbox = draw.textbbox((0, 0), title, font=title_font)
            title_width = title_bbox[2] - title_bbox[0]
            draw.text((width//2 - title_width//2, height//2 - 20), title, fill='#495057', font=title_font)
            
            # Draw description (wrap text if needed)
            words = description.split()
            lines = []
            current_line = []
            max_width = width - 40
            
            for word in words:
                test_line = ' '.join(current_line + [word])
                test_bbox = draw.textbbox((0, 0), test_line, font=desc_font)
                if test_bbox[2] - test_bbox[0] <= max_width:
                    current_line.append(word)
                else:
                    if current_line:
                        lines.append(' '.join(current_line))
                        current_line = [word]
                    else:
                        lines.append(word)
            
            if current_line:
                lines.append(' '.join(current_line))
            
            # Draw description lines
            y_offset = height//2 + 20
            for line in lines:
                line_bbox = draw.textbbox((0, 0), line, font=desc_font)
                line_width = line_bbox[2] - line_bbox[0]
                draw.text((width//2 - line_width//2, y_offset), line, fill='#6c757d', font=desc_font)
                y_offset += 25
            
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Save placeholder
            img.save(output_path, 'PNG')
            self.logger.info(f"Placeholder image created: {output_path}")
            
        except Exception as e:
            self.logger.error(f"Failed to create placeholder image: {str(e)}")

    def _create_annotated_comparison_from_data(self, analysis_results, output_path):
        """Create annotated comparison from analysis data when original is not available"""
        try:
            import cv2
            import numpy as np
            from PIL import Image, ImageDraw, ImageFont
            
            screenshots = analysis_results.get('screenshots', {})
            comparisons = analysis_results.get('comparisons', {})
            
            # Load the screenshots
            url1_path = screenshots.get('url1')
            url2_path = screenshots.get('url2')
            
            if not (url1_path and url2_path and os.path.exists(url1_path) and os.path.exists(url2_path)):
                self._create_placeholder_image(output_path, "Enhanced Visual Comparison", 
                                             "Screenshot data not available for annotated comparison")
                return
            
            # Load images
            img1 = cv2.imread(url1_path)
            img2 = cv2.imread(url2_path)
            
            if img1 is None or img2 is None:
                self._create_placeholder_image(output_path, "Enhanced Visual Comparison", 
                                             "Could not load screenshot images")
                return
            
            # Resize images to match if needed
            if img1.shape != img2.shape:
                h = min(img1.shape[0], img2.shape[0])
                w = min(img1.shape[1], img2.shape[1])
                img1 = cv2.resize(img1, (w, h))
                img2 = cv2.resize(img2, (w, h))
            
            # Create difference mask
            diff = cv2.absdiff(img1, img2)
            gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            
            # Find contours of differences
            _, thresh = cv2.threshold(gray_diff, 30, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Create annotated image (use img2 as base)
            annotated = img2.copy()
            
            # Draw bounding boxes around differences
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 100:  # Filter small noise
                    x, y, w, h = cv2.boundingRect(contour)
                    # Draw green bounding box
                    cv2.rectangle(annotated, (x, y), (x + w, y + h), (0, 255, 0), 3)
                    # Add label
                    cv2.putText(annotated, 'DIFF', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            # Save the annotated image
            cv2.imwrite(output_path, annotated)
            self.logger.info(f"Annotated comparison created from data: {output_path}")
            
        except Exception as e:
            self.logger.error(f"Failed to create annotated comparison from data: {str(e)}")
            self._create_placeholder_image(output_path, "Enhanced Visual Comparison", 
                                         f"Error creating annotated comparison: {str(e)}")

    def _create_heatmap_from_screenshots(self, analysis_results, output_path):
        """Create difference heatmap from screenshots when original is not available"""
        try:
            import cv2
            import numpy as np
            import matplotlib.pyplot as plt
            import matplotlib.colors as mcolors
            
            screenshots = analysis_results.get('screenshots', {})
            
            # Load the screenshots
            url1_path = screenshots.get('url1')
            url2_path = screenshots.get('url2')
            
            if not (url1_path and url2_path and os.path.exists(url1_path) and os.path.exists(url2_path)):
                self._create_placeholder_image(output_path, "Difference Heatmap", 
                                             "Screenshot data not available for heatmap generation")
                return
            
            # Load images
            img1 = cv2.imread(url1_path)
            img2 = cv2.imread(url2_path)
            
            if img1 is None or img2 is None:
                self._create_placeholder_image(output_path, "Difference Heatmap", 
                                             "Could not load screenshot images")
                return
            
            # Resize images to match if needed
            if img1.shape != img2.shape:
                h = min(img1.shape[0], img2.shape[0])
                w = min(img1.shape[1], img2.shape[1])
                img1 = cv2.resize(img1, (w, h))
                img2 = cv2.resize(img2, (w, h))
            
            # Convert to grayscale for difference calculation
            gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
            gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
            
            # Calculate absolute difference
            diff = cv2.absdiff(gray1, gray2)
            
            # Normalize difference values
            diff_normalized = diff.astype(np.float32) / 255.0;
            
            # Create heatmap
            plt.figure(figsize=(12, 8))
            
            # Create custom colormap (blue for no difference, red for high difference)
            colors = ['#000080', '#0000FF', '#00FFFF', '#FFFF00', '#FF8000', '#FF0000']
            n_bins = 256
            cmap = mcolors.LinearSegmentedColormap.from_list('custom_heatmap', colors, N=n_bins)
            
            # Display heatmap
            plt.imshow(diff_normalized, cmap=cmap, interpolation='nearest')
            plt.colorbar(label='Difference Intensity', shrink=0.8)
            plt.title('Pixel Difference Heatmap\n(Blue = Similar, Red = Different)', fontsize=14, fontweight='bold')
            plt.axis('off');
            
            # Save the heatmap
            plt.tight_layout()
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            plt.close()
            
            self.logger.info(f"Difference heatmap created from screenshots: {output_path}")
            
        except Exception as e:
            self.logger.error(f"Failed to create heatmap from screenshots: {str(e)}")
            self._create_placeholder_image(output_path, "Difference Heatmap", 
                                         f"Error creating heatmap: {str(e)}")

    def _copy_screenshots_to_reports(self, analysis_results, base_name):
        """Copy screenshot files to reports directory for HTML access"""
        try:
            screenshots = analysis_results.get('screenshots', {})
            
            for screenshot_type, screenshot_path in screenshots.items():
                if screenshot_path and os.path.exists(screenshot_path):
                    # Create filename for the copied screenshot
                    dest_filename = f"{base_name}_{screenshot_type}_screenshot.png"
                    dest_path = os.path.join(self.output_dir, dest_filename)
                    
                    # Copy the screenshot file
                    shutil.copy2(screenshot_path, dest_path)
                    self.logger.info(f"Copied screenshot {screenshot_type} to reports: {dest_filename}")
                    
                    # Update the reports dict to include the screenshot paths
                    if 'reports' not in analysis_results:
                        analysis_results['reports'] = {}
                    analysis_results['reports'][f'{screenshot_type}_screenshot'] = dest_path
                    
        except Exception as e:
            self.logger.error(f"Failed to copy screenshots to reports directory: {str(e)}")

    def _generate_image_html(self, analysis_results, image_type, alt_text):
        """Generate HTML for image with proper path handling and fallbacks"""
        try:
            # Get the image path from reports
            reports = analysis_results.get('reports', {})
            image_path = reports.get(image_type, '')
            
            # If no image in reports, check analysis_results for alternative paths
            if not image_path:
                # Check for screenshots first
                if image_type == 'url1_screenshot':
                    screenshots = analysis_results.get('screenshots', {})
                    image_path = screenshots.get('url1', '')
                elif image_type == 'url2_screenshot':
                    screenshots = analysis_results.get('screenshots', {})
                    image_path = screenshots.get('url2', '')
                else:
                    # Check other path mappings
                    path_mapping = {
                        'heatmap': 'heatmap_path',
                        'visual': 'annotated_comparison_path',
                        'sidebyside': None  # Side-by-side should only use generated reports, not fallback to annotated
                    }
                    alt_key = path_mapping.get(image_type)
                    if alt_key and alt_key in analysis_results:
                        image_path = analysis_results[alt_key]
            
            if not image_path:
                # No image path provided
                return f"""
                <div style="background: #f8f9fa; padding: 40px; text-align: center; border: 2px dashed #dee2e6; border-radius: 8px;">
                    <p style="color: #6c757d; margin: 0; font-style: italic;">📷 {alt_text} not available</p>
                    <p style="color: #6c757d; margin: 5px 0 0 0; font-size: 0.9em;">Image will be generated during live analysis</p>
                </div>
                """
            
            # For screenshots, check if there's a copy in the reports directory with the proper naming
            image_filename = os.path.basename(image_path)
            
            # Special handling for screenshots - look for the copied version in reports directory
            if image_type in ['url1_screenshot', 'url2_screenshot']:
                # Look for a file in the reports directory that matches the expected pattern
                reports_dir = self.output_dir
                try:
                    for filename in os.listdir(reports_dir):
                        if f'_{image_type}.png' in filename:
                            image_filename = filename
                            image_path = os.path.join(reports_dir, filename)
                            break
                except OSError:
                    pass  # Directory doesn't exist or can't be read
            
            # Check if the image file actually exists
            if os.path.exists(image_path):
                # Image exists - show it normally
                return f"""
                <img src="{image_filename}" 
                     alt="{alt_text}" 
                     onclick="openImage(this.src)"
                     style="max-width: 100%; height: auto; border-radius: 5px; cursor: pointer; transition: transform 0.3s;"
                     onmouseover="this.style.transform='scale(1.02)'"
                     onmouseout="this.style.transform='scale(1)'">
                """
            else:
                # Image doesn't exist - show placeholder with info
                return f"""
                <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 40px; text-align: center; border: 2px dashed #dee2e6; border-radius: 8px;">
                    <div style="font-size: 48px; margin-bottom: 15px;">📊</div>
                    <p style="color: #495057; margin: 0; font-weight: 600;">{alt_text}</p>
                    <p style="color: #6c757d; margin: 5px 0 0 0; font-size: 0.9em;">Expected: {image_filename}</p>
                    <p style="color: #6c757d; margin: 5px 0 0 0; font-size: 0.8em; font-style: italic;">This image will be available after running a complete analysis</p>
                </div>
                """
                
        except Exception as e:
            # Error handling - show error placeholder
            return f"""
            <div style="background: #f8d7da; padding: 30px; text-align: center; border: 2px solid #f5c6cb; border-radius: 8px;">
                <p style="color: #721c24; margin: 0;">⚠️ Error loading {alt_text}</p>
                <p style="color: #721c24; margin: 5px 0 0 0; font-size: 0.9em;">{str(e)}</p>
            </div>
            """

    def create_shareable_package(self, reports, analysis_results, config, zip_path):
        """Create a shareable ZIP package with all reports and images"""
        try:
            import zipfile
            
            # Create ZIP file
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Add all report files
                for report_type, file_path in reports.items():
                    if file_path and os.path.exists(file_path) and report_type != 'package':
                        # Add with just the filename
                        zipf.write(file_path, os.path.basename(file_path))
                        self.logger.info(f"Added {report_type} to package: {os.path.basename(file_path)}")
                
                # Add screenshots if available
                screenshots = analysis_results.get('screenshots', {})
                for screenshot_type, screenshot_path in screenshots.items():
                    if screenshot_path and os.path.exists(screenshot_path):
                        filename = f"original_screenshot_{screenshot_type}.png"
                        zipf.write(screenshot_path, filename)
                        self.logger.info(f"Added screenshot to package: {filename}")
                
                # Add README file explaining the package
                readme_content = self._generate_package_readme(reports, analysis_results, config)
                zipf.writestr("README.txt", readme_content)
                
            self.logger.info(f"Shareable package created: {zip_path}")
            return zip_path
            
        except Exception as e:
            self.logger.error(f"Failed to create shareable package: {str(e)}")
            # Create a simple text file instead
            try:
                with open(zip_path.replace('.zip', '_error.txt'), 'w') as f:
                    f.write(f"Package creation failed: {str(e)}\n")
                    f.write(f"Available reports: {list(reports.keys())}\n")
                return zip_path.replace('.zip', '_error.txt')
            except:
                return None

    def _generate_package_readme(self, reports, analysis_results, config):
        """Generate README content for the shareable package"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        readme = f"""Visual AI Regression Analysis Package
Generated: {timestamp}

CONTENTS:
=========

Reports:
"""
        
        for report_type, file_path in reports.items():
            if file_path and os.path.exists(file_path) and report_type != 'package':
                filename = os.path.basename(file_path)
                readme += f"- {filename} - {report_type.title()} report\n"
        
        readme += f"""
Test Configuration:
==================
- Reference URL: {config.get('url1', 'N/A')}
- Test URL: {config.get('url2', 'N/A')}
- Browser: {config.get('browser', 'chrome')}
- Resolution: {config.get('resolution', '1920x1080')}
- Layout Analysis: {'Enabled' if config.get('layout_shift', True) else 'Disabled'}
- Color Analysis: {'Enabled' if config.get('font_color', True) else 'Disabled'}
- AI Analysis: {'Enabled' if config.get('ai_analysis', True) else 'Disabled'}
- WCAG Analysis: {'Enabled' if config.get('wcag_analysis', True) else 'Disabled'}

Results Summary:
===============
- Overall Similarity: {analysis_results.get('similarity_score', 0):.2%}
- Layout Differences: {len(analysis_results.get('layout_shifts', []))}
- Color Changes: {len(analysis_results.get('color_differences', []))}
- Missing Elements: {len(analysis_results.get('missing_elements', []))}
- New Elements: {len(analysis_results.get('new_elements', []))}

How to Use:
===========
1. Extract all files to a folder
2. Open the HTML report in your web browser
3. View the PDF report for printing/sharing
4. Use the JSON file for data integration
5. Image files show visual comparisons and differences

For detailed analysis, start with the HTML report which includes



interactive features and comprehensive results.
"""
        
        return readme

    def generate_summary_report(self, analysis_results, config, output_path):
        """Generate a quick summary HTML report"""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Calculate quick metrics
            similarity = analysis_results.get('similarity_score', 0)
            layout_changes = len(analysis_results.get('layout_shifts', []))
            color_changes = len(analysis_results.get('color_differences', []))
            missing_elements = len(analysis_results.get('missing_elements', []))
            new_elements = len(analysis_results.get('new_elements', []))
            
            # Determine status
            if similarity > 0.95:
                status = "PASSED"
                status_class = "status-pass"
                recommendation = "No significant differences detected. Safe to proceed."
            elif similarity > 0.85:
                status = "WARNING"
                status_class = "status-warning"
                recommendation = "Minor differences detected. Review recommended."
            else:
                status = "FAILED"
                status_class = "status-fail"
                recommendation = "Significant differences detected. Investigation required."
            
            html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Visual Regression Summary - {timestamp}</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
        .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .header {{ text-align: center; border-bottom: 2px solid #eee; padding-bottom: 20px; margin-bottom: 30px; }}
        .status-badge {{ padding: 8px 16px; border-radius: 20px; font-weight: bold; text-transform: uppercase; }}
        .status-pass {{ background: #d4edda; color: #155724; }}
        .status-warning {{ background: #fff3cd; color: #856404; }}
        .status-fail {{ background: #f8d7da; color: #721c24; }}
        .metric {{ display: inline-block; margin: 10px; padding: 20px; background: #f8f9fa; border-radius: 8px; text-align: center; min-width: 120px; }}
        .metric-value {{ font-size: 2em; font-weight: bold; color: #007bff; }}
        .metric-label {{ color: #666; font-size: 0.9em; }}
        .section {{ margin: 30px 0; }}
        .config-table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        .config-table th, .config-table td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        .config-table th {{ background: #f8f9fa; font-weight: 600; }}
        .recommendation {{ background: #e3f2fd; padding: 20px; border-radius: 8px; border-left: 4px solid #2196f3; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 Visual Regression Analysis Summary</h1>
            <p>Generated: {timestamp}</p>
            <div class="status-badge {status_class}">{status}</div>
        </div>
        
        <div class="section">
            <h2>📊 Key Metrics</h2>
            <div style="text-align: center;">
                <div class="metric">
                    <div class="metric-value">{similarity:.1%}</div>
                    <div class="metric-label">Similarity</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{layout_changes}</div>
                    <div class="metric-label">Layout Changes</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{color_changes}</div>
                    <div class="metric-label">Color Changes</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{missing_elements}</div>
                    <div class="metric-label">Missing Elements</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{new_elements}</div>
                    <div class="metric-label">New Elements</div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>🔧 Test Configuration</h2>
            <table class="config-table">
                <tr><th>Parameter</th><th>Value</th></tr>
                <tr><td>Reference URL</td><td>{config.get('url1', 'N/A')}</td></tr>
                <tr><td>Test URL</td><td>{config.get('url2', 'N/A')}</td></tr>
                <tr><td>Browser</td><td>{config.get('browser', 'N/A')}</td></tr>
                <tr><td>Resolution</td><td>{config.get('resolution', 'N/A')}</td></tr>
            </table>
        </div>
        
        <div class="section">
            <h2>🎯 Recommendation</h2>
            <div class="recommendation">
                <strong>{recommendation}</strong>
            </div>
        </div>
        
        <div class="section" style="text-align: center; border-top: 2px solid #eee; padding-top: 20px;">
            <p><em>For detailed analysis, open the complete HTML report.</em></p>
        </div>
    </div>
</body>
</html>
"""
            
            # Write summary report
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            self.logger.info(f"Summary report generated: {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Failed to generate summary report: {str(e)}")
            raise

    def _get_wcag_summary_score(self, analysis_results):
        """Get summary WCAG compliance score"""
        try:
            wcag_analysis = analysis_results.get('wcag_analysis', {})
            if not wcag_analysis:
                return 0
            
            # Get scores from both URLs
            url1_score = wcag_analysis.get('url1', {}).get('compliance_score', 0)
            url2_score = wcag_analysis.get('url2', {}).get('compliance_score', 0)
            
            # Return average score
            if url1_score > 0 and url2_score > 0:
                return (url1_score + url2_score) / 2
            elif url1_score > 0:
                return url1_score
            elif url2_score > 0:
                return url2_score
            else:
                return 0
                
        except Exception as e:
            self.logger.error(f"Failed to get WCAG summary score: {str(e)}")
            return 0

    def _get_wcag_status_class(self, analysis_results):
        """Get CSS class for WCAG status badge - AA standard only"""
        score = self._get_wcag_summary_score(analysis_results)
        
        if score >= 85:
            return "status-pass"
        elif score >= 70:
            return "status-warning"
        else:
            return "status-fail"

    def _get_wcag_status_text(self, analysis_results):
        """Get text for WCAG status - AA standard only"""
        score = self._get_wcag_summary_score(analysis_results)
        
        if score >= 85:
            return "AA COMPLIANT"
        elif score >= 70:
            return "APPROACHING AA"
        elif score >= 50:
            return "NEEDS IMPROVEMENT"
        else:
            return "NON-COMPLIANT"

    def _get_compliance_badge_class(self, compliance_level):
        """Get CSS class for compliance level badge - AA standard only"""
        level = compliance_level.lower() if compliance_level else ""
        
        if level == "aa":
            return "status-pass"
        else:
            return "status-fail"

    def _generate_export_link(self, filename, display_name, description):
        """Generate export link with file size and availability check"""
        try:
            file_path = os.path.join(self.output_dir, filename)
            
            if os.path.exists(file_path):
                # Get file size
                size_bytes = os.path.getsize(file_path)
                if size_bytes < 1024:
                    size_text = f"{size_bytes} B"
                elif size_bytes < 1024 * 1024:
                    size_text = f"{size_bytes / 1024:.1f} KB"
                else:
                    size_text = f"{size_bytes / (1024 * 1024):.1f} MB"
                
                return f"""
                <div class="export-link available">
                    <a href="{filename}" download="{filename}" class="download-link">
                        <span class="link-icon">📥</span>
                        <span class="link-text">
                            <strong>{display_name}</strong>
                            <small>{description} ({size_text})</small>
                        </span>
                    </a>
                </div>
                """
            else:
                return f"""
                <div class="export-link unavailable">
                    <span class="link-icon">⚠️</span>
                    <span class="link-text">
                        <strong>{display_name}</strong>
                        <small>{description} (Not available)</small>
                    </span>
                </div>
                """
                
        except Exception as e:
            self.logger.error(f"Failed to generate export link for {filename}: {str(e)}")
            return f"""
            <div class="export-link error">
                <span class="link-icon">❌</span>
                <span class="link-text">
                    <strong>{display_name}</strong>
                    <small>Error: {str(e)}</small>
                </span>
            </div>
            """

    def _generate_wcag_html(self, analysis_results):
        """Generate detailed WCAG compliance HTML section"""
        try:
            wcag_analysis = analysis_results.get('wcag_analysis', {})
            
            if not wcag_analysis:
                return """
                <div class="analysis-details">
                    <p>⚠️ WCAG analysis was not performed or no results available.</p>
                    <p>Enable WCAG analysis in settings to see detailed accessibility compliance information.</p>
                </div>
                """
            
            html = ""
            
            # Overall compliance summary
            url1_score = wcag_analysis.get('url1', {}).get('compliance_score', 0)
            url2_score = wcag_analysis.get('url2', {}).get('compliance_score', 0)
            avg_score = (url1_score + url2_score) / 2 if url1_score > 0 and url2_score > 0 else max(url1_score, url2_score)
            
            html += f"""
            <div class="analysis-details">
                <h3>📊 Compliance Overview</h3>
                <div class="wcag-summary">
                    <div class="score-display">
                        <span class="score-number">{avg_score:.1f}%</span>
                        <span class="score-label">Overall Score</span>
                    </div>
                    <p><strong>Compliance Level:</strong> 
                        <span class="status-badge {self._get_wcag_status_class(analysis_results)}">
                            {self._get_wcag_status_text(analysis_results)}
                        </span>
                    </p>
                </div>
            </div>
            """
            
            # Process each URL's WCAG results
            for url_key, url_results in wcag_analysis.items():
                if url_key in ['url1', 'url2']:
                    url_display = "Reference Page" if url_key == 'url1' else "Test Page"
                    
                    html += f"""
                    <div class="analysis-details">
                        <h3>🌐 {url_display} Accessibility Analysis</h3>
                        <p><strong>URL:</strong> {url_results.get('url', 'N/A')}</p>
                        <p><strong>WCAG Version:</strong> {url_results.get('wcag_version', '2.2')}</p>
                        <p><strong>Compliance Level:</strong> 
                            <span class="status-badge {self._get_compliance_badge_class(url_results.get('compliance_level', 'Not Assessed'))}">
                                {url_results.get('compliance_level', 'Not Assessed')}
                            </span>
                        </p>
                        <p><strong>Overall Score:</strong> <span class="metric-value">{url_results.get('compliance_score', 0):.1f}%</span></p>
                        <p><strong>Total Issues:</strong> <span class="metric-value">{url_results.get('total_issues', 0)}</span></p>
                        <p><strong>Critical Issues:</strong> <span class="metric-value">{url_results.get('critical_issues', 0)}</span></p>
                    </div>
                    """
                    
                    # WCAG 2.2 Features Section
                    wcag_22_features = url_results.get('wcag_22_features', {})
                    if wcag_22_features:
                        html += f"""
                        <div class="analysis-details">
                            <h4>🆕 WCAG 2.2 Specific Features</h4>
                            <p><strong>Target Size Compliance:</strong> 
                                <span class="status-badge {'status-pass' if wcag_22_features.get('target_size_compliant', False) else 'status-fail'}">
                                    {'✅ Compliant' if wcag_22_features.get('target_size_compliant', False) else '❌ Non-Compliant'}
                                </span>
                            </p>
                            <p><strong>Focus Appearance Score:</strong> <span class="metric-value">{wcag_22_features.get('focus_appearance_score', 0):.1f}%</span></p>
                            <p><strong>Dragging Alternative Score:</strong> <span class="metric-value">{wcag_22_features.get('dragging_alternative_score', 0):.1f}%</span></p>
                        </div>
                        """
                    
                    # Issues breakdown
                    issues = url_results.get('issues', {})
                    if issues:
                        html += f"""
                        <div class="analysis-details">
                            <h4>🔍 Issues Breakdown</h4>
                            <ul>
                        """
                        for issue_type, issue_list in issues.items():
                            if issue_list:
                                html += f"<li><strong>{issue_type.replace('_', ' ').title()}:</strong> {len(issue_list)} issues</li>"
                        html += "</ul></div>"
            
            # Comparison section
            comparison = wcag_analysis.get('comparison', {})
            if comparison:
                html += f"""
                <div class="analysis-details">
                    <h3>🔍 Accessibility Comparison</h3>
                    <p><strong>Assessment:</strong> {comparison.get('assessment', 'No comparison available')}</p>
                    <p><strong>Score Difference:</strong> {comparison.get('score_difference', 0):.1f} points</p>
                    <p><strong>Recommendation:</strong> {comparison.get('recommendation', 'Continue accessibility improvements')}</p>
                </div>
                """
            
            return html
            
        except Exception as e:
            self.logger.error(f"Failed to generate WCAG HTML: {str(e)}")
            return f"""
            <div class="analysis-details">
                <p>❌ Error generating WCAG compliance details: {str(e)}</p>
            </div>
            """

    def _generate_wcag_section_html(self, analysis_results, config):
        """Generate WCAG section only if enabled"""
        if config.get('wcag_analysis', True) and analysis_results.get('wcag_analysis'):
            return f'''
                    <div class="section">
                        <h2>♿ WCAG Accessibility Compliance Analysis</h2>
                        {self._generate_wcag_html(analysis_results)}
                    </div>
            '''
        return ""

    def _get_ssim_interpretation(self, ssim_value):
        """Get interpretation text for SSIM score"""
        if ssim_value >= 0.95:
            return "Excellent similarity"
        elif ssim_value >= 0.85:
            return "Good similarity"
        elif ssim_value >= 0.70:
            return "Moderate similarity"
        else:
            return "Poor similarity"
    
    def _get_mse_interpretation(self, mse_value):
        """Get interpretation text for MSE score"""
        if mse_value <= 50:
            return "Minimal differences"
        elif mse_value <= 200:
            return "Moderate differences"
        elif mse_value <= 500:
            return "Significant differences"
        else:
            return "Major differences"
    
    def _get_pixel_interpretation(self, pixel_diff):
        """Get interpretation text for pixel difference percentage"""
        if pixel_diff <= 1.0:
            return "Minimal change"
        elif pixel_diff <= 5.0:
            return "Minor change"
        elif pixel_diff <= 15.0:
            return "Moderate change"
        else:
            return "Major change"

    def _get_psnr_interpretation(self, psnr_value):
        """Get interpretation text for PSNR score"""
        if psnr_value >= 30:
            return "Excellent quality"
        elif psnr_value >= 20:
            return "Good quality"
        elif psnr_value >= 10:
            return "Moderate quality"
        else:
            return "Poor quality"

    # Example usage
if __name__ == "__main__":
    # Example usage
    generator = ReportGenerator()
    
    # Mock analysis results
    mock_results = {
        'similarity_score': 0.87,
        'layout_shifts': [
            {'distance': 25.5, 'shift_x': 10, 'shift_y': 15, 'original_position': [100, 200, 50, 30]},
            {'distance': 18.2, 'shift_x': -5, 'shift_y': 8, 'original_position': [300, 400, 80, 40]}
        ],
        'color_differences': [
            {'color_distance': 45.2, 'area': 1250, 'position': [150, 300, 60, 40]},
            {'color_distance': 32.1, 'area': 890, 'position': [400, 500, 70, 50]}
        ],
        'missing_elements': [],
        'new_elements': [],
        'ai_analysis': {
            'anomaly_detected': True,
            'feature_distance': 0.1234,
            'confidence': 0.85
        }
    }
    
    mock_config = {
        'url1': 'https://example.com/original',
        'url2': 'https://example.com/modified',
        'browser': 'chrome',
        'resolution': '1920x1080',
        'layout_shift': True,
        'font_color': True,
        'element_detection': True,
        'ai_analysis': True
    }
    
    try:
        reports = generator.generate_comprehensive_report(mock_results, mock_config)
        print(f"Generated reports: {reports}")
    except Exception as e:
        print(f"Error generating reports: {e}")
