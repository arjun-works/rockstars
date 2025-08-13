#!/usr/bin/env python3
"""
Generate comprehensive PDF documentation for Visual AI Regression Testing Module
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import os

def create_documentation_pdf():
    """Create comprehensive PDF documentation"""
    
    # Create PDF document with better margins
    filename = f"Visual_AI_Regression_Module_Documentation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4, 
                          topMargin=0.5*inch, bottomMargin=0.5*inch,
                          leftMargin=0.75*inch, rightMargin=0.75*inch)
    
    # Get styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        textColor=colors.HexColor('#2c3e50'),
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=20,
        spaceBefore=30,
        textColor=colors.HexColor('#34495e'),
        fontName='Helvetica-Bold'
    )
    
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=15,
        spaceBefore=20,
        textColor=colors.HexColor('#2980b9'),
        fontName='Helvetica-Bold'
    )
    
    heading3_style = ParagraphStyle(
        'CustomHeading3',
        parent=styles['Heading3'],
        fontSize=12,
        spaceAfter=10,
        spaceBefore=15,
        textColor=colors.HexColor('#27ae60'),
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=12,
        alignment=TA_JUSTIFY,
        fontName='Helvetica'
    )
    
    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontSize=9,
        spaceAfter=10,
        fontName='Courier',
        backColor=colors.HexColor('#f8f9fa'),
        borderColor=colors.HexColor('#dee2e6'),
        borderWidth=1,
        borderPadding=8
    )
    
    # Helper function for wrapping text in table cells
    def wrap_text(text, style=None):
        """Wrap text in Paragraph for proper table cell formatting"""
        if style is None:
            style = ParagraphStyle(
                'CellText',
                parent=styles['Normal'],
                fontSize=9,
                leading=11,
                fontName='Helvetica'
            )
        return Paragraph(str(text), style)
    
    # Table cell style for wrapped text
    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontSize=9,
        leading=11,
        fontName='Helvetica',
        spaceAfter=4
    )
    
    # Story (content list)
    story = []
    
    # Title Page
    story.append(Paragraph("Visual AI Regression Testing Module", title_style))
    story.append(Spacer(1, 30))
    story.append(Paragraph("Complete Architecture & Documentation", styles['Heading2']))
    story.append(Spacer(1, 50))
    
    # Version info
    version_data = [
        ['Version:', '6.0.0 - Enhanced v6.0 Edition (August 2025)'],
        ['Generated:', datetime.now().strftime('%B %d, %Y at %I:%M %p')],
        ['Python Version:', '3.13.2'],
        ['Latest Update:', 'Configuration Settings + Duration Fix + Image Click Modal'],
        ['Platform:', 'Windows'],
        ['Author:', 'Visual AI Regression Team']
    ]
    
    version_table = Table(version_data, colWidths=[2*inch, 4*inch])
    version_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(version_table)
    story.append(PageBreak())
    
    # Table of Contents
    story.append(Paragraph("Table of Contents", heading1_style))
    
    toc_data = [
        ['1. Project Overview', '3'],
        ['1.1 Latest Updates & Enhancements', '4'],
        ['2. Architecture Overview', '5'],
        ['3. Core Application Files', '6'],
        ['4. Launcher Scripts', '13'],
        ['5. Generated Content Structure', '15'],
        ['6. Configuration Files', '17'],
        ['7. Testing Framework', '19'],
        ['8. Application Workflow', '21'],
        ['9. GUI Architecture', '23'],
        ['10. Technical Specifications', '25'],
        ['11. WCAG Compliance Testing', '27'],
        ['11.1 WCAG Standards Support', '27'],
        ['11.2 WCAG Testing Categories', '28'],
        ['11.3 Advanced Accessibility Features', '28'],
        ['11.4 WCAG Integration & Usage', '29'],
        ['12. Conclusion', '30']
    ]
    
    toc_table = Table(toc_data, colWidths=[5*inch, 1*inch])
    toc_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
    ]))
    story.append(toc_table)
    story.append(PageBreak())
    
    # 1. Project Overview
    story.append(Paragraph("1. Project Overview", heading1_style))
    
    story.append(Paragraph("Purpose", heading2_style))
    story.append(Paragraph(
        "The Visual AI Regression Testing Module is a comprehensive Python application designed for automated visual comparison "
        "of web pages. It combines computer vision techniques, machine learning algorithms, and professional reporting "
        "capabilities to detect and analyze visual differences between web page versions.",
        body_style
    ))
    
    story.append(Paragraph("Key Features", heading2_style))
    features_data = [
        [wrap_text('Feature'), wrap_text('Description')],
        [wrap_text('🖼️ Image Click Modal'), wrap_text('Full-screen image viewing with dark overlay, ESC key support, and smooth animations')],
        [wrap_text('⚙️ Configuration Settings'), wrap_text('Comprehensive analysis parameter display in HTML reports with technical details')],
        [wrap_text('⏱️ Duration Tracking'), wrap_text('Real-time analysis duration calculation and performance monitoring')],
        [wrap_text('📷 Screenshot Management'), wrap_text('Enhanced screenshot loading with auto-copy functionality for reliable display')],
        [wrap_text('🎯 Tabbed HTML Reports'), wrap_text('Professional tabbed interface with enhanced navigation and organization')],
        [wrap_text('Multi-Browser Support'), wrap_text('Chrome, Firefox, Edge with automated WebDriver management')],
        [wrap_text('Computer Vision Analysis'), wrap_text('OpenCV and scikit-image based visual comparison with SSIM, MSE, PSNR')],
        [wrap_text('AI-Powered Detection'), wrap_text('Machine learning algorithms for anomaly detection and layout analysis')],
        [wrap_text('WCAG 2.1/2.2 Compliance'), wrap_text('Comprehensive accessibility testing with latest standards')],
        [wrap_text('Enhanced Color Analysis'), wrap_text('Real-time contrast validation with color blindness simulation')],
        [wrap_text('Target Size Validation'), wrap_text('WCAG 2.2 minimum 24×24 pixel interactive element checking')],
        [wrap_text('Accessible Authentication'), wrap_text('CAPTCHA alternatives and cognitive barrier assessment')],
        [wrap_text('Interactive GUI'), wrap_text('Tkinter-based interface with dedicated WCAG compliance tab')],
        [wrap_text('Multiple Report Formats'), wrap_text('HTML, PDF, JSON, and visual comparison with accessibility data')],
        [wrap_text('Professional Scoring'), wrap_text('0-100% compliance scoring with detailed issue prioritization')],
        [wrap_text('Legal Compliance Support'), wrap_text('ADA, Section 508, EN 301 549, AODA compliance validation')],
        [wrap_text('🌐 Environment Information'), wrap_text('Platform, Python version, and system details in reports')],
        [wrap_text('📊 Metrics Documentation'), wrap_text('Detailed algorithm descriptions and technical explanations')],
        [wrap_text('🚀 Enhanced Launcher'), wrap_text('Advanced launcher v6.0 with feature verification and testing guides')]
    ]
    
    features_table = Table(features_data, colWidths=[2.2*inch, 4.3*inch])
    features_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(features_table)
    
    # Latest Updates Section
    story.append(Paragraph("Latest Updates & Enhancements (v6.0 - August 2025)", heading2_style))
    story.append(Paragraph(
        "Version 6.0 introduces major enhancements including configuration settings, duration tracking, image click modals, and enhanced user experience:",
        body_style
    ))
    
    updates_data = [
        [wrap_text('Update Category'), wrap_text('Enhancement'), wrap_text('Impact')],
        [wrap_text('Configuration Settings'), wrap_text('New ⚙️ Configuration tab in HTML reports with detailed analysis parameters'), wrap_text('Complete transparency in analysis settings')],
        [wrap_text('Duration Tracking'), wrap_text('Fixed Analysis Duration calculation - no more N/A values'), wrap_text('Real performance monitoring and timing insights')],
        [wrap_text('Image Click Modal'), wrap_text('🖼️ Full-screen image viewing with dark overlay and ESC key support'), wrap_text('Professional image viewing experience')],
        [wrap_text('Screenshot Loading'), wrap_text('📷 Fixed screenshot loading in HTML reports with auto-copy functionality'), wrap_text('Reliable screenshot display and access')],
        [wrap_text('Enhanced HTML Reports'), wrap_text('🎯 Tabbed interface with professional styling and smooth animations'), wrap_text('Improved navigation and user experience')],
        [wrap_text('Technical Settings Display'), wrap_text('🛠️ Browser, viewport, timing, and algorithm information in reports'), wrap_text('Complete technical documentation')],
        [wrap_text('Environment Information'), wrap_text('🌐 Platform, Python version, and execution environment details'), wrap_text('Full system transparency')],
        [wrap_text('Metrics Documentation'), wrap_text('📊 Detailed descriptions of SSIM, MSE, PSNR, and AI algorithms'), wrap_text('Educational and professional reporting')],
        [wrap_text('Enhanced Launcher'), wrap_text('🚀 Updated launch_gui.bat v6.0 with feature verification and testing guides'), wrap_text('Better user onboarding and diagnostics')],
        [wrap_text('WCAG 2.2 Compliance'), wrap_text('Complete WCAG 2.2 standard implementation with enhanced accessibility testing'), wrap_text('Industry-leading accessibility validation')],
        [wrap_text('Professional UI/UX'), wrap_text('✨ Modern interface design with responsive elements and visual feedback'), wrap_text('Enhanced user satisfaction and efficiency')]
    ]
    
    updates_table = Table(updates_data, colWidths=[1.6*inch, 2.5*inch, 1.8*inch])
    updates_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#d5f4e6')),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(updates_table)
    
    # V6.0 Detailed Features Section
    story.append(Paragraph("Version 6.0 Feature Highlights", heading2_style))
    story.append(Paragraph(
        "The following sections detail the major enhancements introduced in version 6.0:",
        body_style
    ))
    
    # Configuration Settings Feature
    story.append(Paragraph("🔧 Configuration Settings Tab", heading3_style))
    story.append(Paragraph(
        "HTML reports now include a comprehensive Configuration Settings tab that displays all analysis parameters, "
        "technical settings, metrics descriptions, and environment information. This provides complete transparency "
        "in how the analysis was performed and enables better reproducibility and debugging.",
        body_style
    ))
    
    # Duration Tracking Feature
    story.append(Paragraph("⏱️ Analysis Duration Tracking", heading3_style))
    story.append(Paragraph(
        "Fixed the 'Analysis Duration: N/A' issue by implementing real-time timing calculation. The system now "
        "accurately tracks and displays analysis duration in seconds, providing valuable performance insights "
        "and helping users monitor analysis efficiency.",
        body_style
    ))
    
    # Image Click Modal Feature
    story.append(Paragraph("🖼️ Image Click Full-Screen Modal", heading3_style))
    story.append(Paragraph(
        "Enhanced HTML reports with clickable images that open in professional full-screen modals. Features include "
        "dark overlay background, close button, ESC key support, click-outside-to-close functionality, and smooth "
        "animations for a professional user experience.",
        body_style
    ))
    
    # Screenshot Loading Enhancement
    story.append(Paragraph("📷 Enhanced Screenshot Loading", heading3_style))
    story.append(Paragraph(
        "Resolved screenshot loading issues in HTML reports by implementing automatic screenshot copying to the "
        "reports directory and ensuring proper file path resolution. Original screenshots now display reliably "
        "in all report formats.",
        body_style
    ))
    
    # HTML Report Enhancements
    story.append(Paragraph("🎯 Professional HTML Report Interface", heading3_style))
    story.append(Paragraph(
        "Redesigned HTML reports with tabbed navigation interface, enhanced visual styling, professional color schemes, "
        "detailed image descriptions, and responsive design elements for improved user experience and better information organization.",
        body_style
    ))
    
    story.append(PageBreak())
    
    # 2. Architecture Overview
    story.append(Paragraph("2. Architecture Overview", heading1_style))
    
    story.append(Paragraph("System Architecture", heading2_style))
    story.append(Paragraph(
        "The application follows a modular architecture with clear separation of concerns. The system is built using "
        "the Model-View-Controller (MVC) pattern with additional layers for data processing and report generation.",
        body_style
    ))
    
    story.append(Paragraph("Project Structure", heading2_style))
    story.append(Paragraph(
        "TestProject/<br/>"
        "├── 🎯 Core Application Files<br/>"
        "├── 🚀 Launcher Scripts<br/>"
        "├── 📊 Generated Content<br/>"
        "├── ⚙️ Configuration Files<br/>"
        "├── 🧪 Testing Scripts<br/>"
        "└── 📁 Supporting Directories",
        code_style
    ))
    
    story.append(Paragraph("Component Interaction", heading2_style))
    component_data = [
        ['Component', 'Primary Function', 'Dependencies'],
        ['main.py', 'GUI Frontend & User Interface', 'tkinter, PIL, threading'],
        ['visual_ai_regression.py', 'Core Analysis Orchestrator', 'All analysis modules'],
        ['screenshot_capture.py', 'Web Page Screenshot Capture', 'selenium, webdriver-manager'],
        ['image_comparison.py', 'Computer Vision Analysis', 'opencv-python, scikit-image'],
        ['ai_detector.py', 'Machine Learning Analysis', 'scikit-learn, numpy'],
        ['report_generator.py', 'Multi-format Report Generation', 'reportlab, matplotlib']
    ]
    
    component_table = Table(component_data, colWidths=[2*inch, 2.5*inch, 2*inch])
    component_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(component_table)
    story.append(PageBreak())
    
    # 3. Core Application Files
    story.append(Paragraph("3. Core Application Files", heading1_style))
    
    # main.py
    story.append(Paragraph("3.1 main.py - GUI Frontend (1,192 lines)", heading2_style))
    story.append(Paragraph(
        "The main application file containing the Tkinter-based graphical user interface. This is the primary entry "
        "point for user interaction and coordinates all user-facing functionality.",
        body_style
    ))
    
    story.append(Paragraph("Key Components:", heading3_style))
    story.append(Paragraph(
        "• VisualRegressionGUI class - Main application window<br/>"
        "• Tabbed interface with Image Comparison and Analysis Results<br/>"
        "• URL input and configuration panels<br/>"
        "• Progress tracking and status updates<br/>"
        "• Image display with zoom and pan controls<br/>"
        "• Report sharing and export functionality<br/>"
        "• Screenshot browsing capabilities",
        body_style
    ))
    
    # visual_ai_regression.py
    story.append(Paragraph("3.2 visual_ai_regression.py - Core Engine (394 lines)", heading2_style))
    story.append(Paragraph(
        "The central orchestrator that manages the entire analysis workflow. It coordinates between different "
        "analysis modules and handles the complete pipeline from configuration to report generation.",
        body_style
    ))
    
    story.append(Paragraph("Analysis Pipeline:", heading3_style))
    story.append(Paragraph(
        "1. Configuration Validation → URL and parameter verification<br/>"
        "2. Browser Setup → WebDriver initialization and configuration<br/>"
        "3. Screenshot Capture → Full-page image capture with metadata<br/>"
        "4. Image Processing → Loading, resizing, and preprocessing<br/>"
        "5. Multi-Analysis → Parallel execution of all analysis types<br/>"
        "6. Report Generation → Creation of multiple report formats<br/>"
        "7. Resource Cleanup → Browser closure and memory management",
        body_style
    ))
    
    # screenshot_capture.py
    story.append(Paragraph("3.3 screenshot_capture.py - Web Capture Module", heading2_style))
    story.append(Paragraph(
        "Selenium-based module for automated web page screenshot capture. Supports multiple browsers and "
        "provides comprehensive page information extraction.",
        body_style
    ))
    
    story.append(Paragraph("Capabilities:", heading3_style))
    capabilities_data = [
        ['Browser Support', 'Chrome, Firefox, Edge with automatic WebDriver management'],
        ['Screenshot Types', 'Full-page, viewport-specific, element-specific capture'],
        ['Resolution Control', '1920x1080, 1366x768, 1440x900, 1280x720, custom'],
        ['Metadata Collection', 'Page title, URL, dimensions, load time, DOM structure'],
        ['Error Handling', 'Network timeouts, page load failures, element detection'],
        ['Performance', 'Headless operation, optimized rendering, parallel execution']
    ]
    
    capabilities_table = Table(capabilities_data, colWidths=[1.8*inch, 4.5*inch])
    capabilities_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
    ]))
    story.append(capabilities_table)
    
    # image_comparison.py
    story.append(Paragraph("3.4 image_comparison.py - Computer Vision Engine (392 lines)", heading2_style))
    story.append(Paragraph(
        "Advanced computer vision module using OpenCV and scikit-image for comprehensive visual analysis. "
        "Implements multiple algorithms for different types of visual comparison.",
        body_style
    ))
    
    story.append(Paragraph("Analysis Methods:", heading3_style))
    analysis_data = [
        ['SSIM (Structural Similarity)', 'Perceptual similarity measurement (0.0 to 1.0 scale)'],
        ['Layout Shift Detection', 'Pixel-level movement analysis with vector calculation'],
        ['Color Difference Analysis', 'HSV color space comparison with threshold detection'],
        ['Element Detection', 'Contour-based identification of missing/new elements'],
        ['Overlap Detection', 'Spatial relationship analysis for overlapping content'],
        ['Heatmap Generation', 'Visual difference intensity mapping'],
        ['Annotation Creation', 'Automated markup of detected differences']
    ]
    
    analysis_table = Table(analysis_data, colWidths=[2.2*inch, 4.3*inch])
    analysis_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#9b59b6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lavender),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(analysis_table)
    story.append(PageBreak())
    
    # ai_detector.py
    story.append(Paragraph("3.5 ai_detector.py - AI-Powered Analysis", heading2_style))
    story.append(Paragraph(
        "Machine learning module implementing advanced anomaly detection and pattern recognition. "
        "Uses scikit-learn algorithms for intelligent visual analysis.",
        body_style
    ))
    
    story.append(Paragraph("ML Techniques:", heading3_style))
    ml_data = [
        ['Local Binary Patterns (LBP)', 'Texture analysis for surface pattern detection'],
        ['Histogram of Gradients (HOG)', 'Shape and edge detection algorithms'],
        ['Color Histograms', 'Statistical color distribution analysis'],
        ['Isolation Forest', 'Unsupervised anomaly detection algorithm'],
        ['One-Class SVM', 'Support vector machine for outlier detection'],
        ['Feature Clustering', 'K-means clustering for pattern grouping'],
        ['Confidence Scoring', 'Statistical confidence measurement (0-100%)']
    ]
    
    ml_table = Table(ml_data, colWidths=[2.2*inch, 4.3*inch])
    ml_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e67e22')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (0, 1), (-1, -1), colors.bisque),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(ml_table)
    
    # report_generator.py
    story.append(Paragraph("3.6 report_generator.py - Multi-Format Reporting (1,198 lines)", heading2_style))
    story.append(Paragraph(
        "Comprehensive reporting module that generates professional reports in multiple formats. "
        "Includes advanced sharing capabilities and interactive features.",
        body_style
    ))
    
    story.append(Paragraph("Report Formats:", heading3_style))
    report_data = [
        ['Interactive HTML', 'JavaScript-enabled reports with sharing buttons and responsive design'],
        ['Professional PDF', 'ReportLab-generated documents with embedded images and charts'],
        ['Machine-readable JSON', 'Structured data format for API integration and automation'],
        ['Visual Comparisons', 'Side-by-side, overlay, and difference visualization images'],
        ['Complete ZIP Package', 'Bundled reports with all assets for easy distribution'],
        ['Summary Reports', 'Condensed executive summary with key findings'],
        ['Email Integration', 'SMTP-based automatic report distribution']
    ]
    
    report_table = Table(report_data, colWidths=[1.8*inch, 4.5*inch])
    report_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1abc9c')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightcyan),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(report_table)
    story.append(PageBreak())
    
    # 4. Launcher Scripts
    story.append(Paragraph("4. Launcher Scripts", heading1_style))
    
    story.append(Paragraph(
        "Multiple launcher scripts provide flexible ways to start the application with different configurations "
        "and execution modes. These scripts handle environment setup, dependency verification, and error handling.",
        body_style
    ))
    
    story.append(Paragraph("4.1 Batch Files (.bat)", heading2_style))
    batch_data = [
        ['Script Name', 'Purpose', 'Features'],
        ['launch_gui.bat', 'Standard GUI launcher', 'Console output, error display, pause on completion'],
        ['launch_debug.bat', 'Debug mode launcher', 'Dependency check, detailed output, error tracking'],
        ['launch_silent_venv.bat', 'Silent background launch', 'No console window, virtual environment'],
        ['launch_with_check.bat', 'Launch with verification', 'Pre-flight checks, dependency validation'],
        ['test_gui.bat', 'GUI functionality test', 'Simple interface test, quick verification']
    ]
    
    batch_table = Table(batch_data, colWidths=[2*inch, 2.5*inch, 2*inch])
    batch_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightsteelblue),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(batch_table)
    
    story.append(Paragraph("4.2 PowerShell Scripts (.ps1)", heading2_style))
    story.append(Paragraph(
        "• run_visual_regression.ps1 - Main PowerShell launcher with enhanced Windows integration<br/>"
        "• launch_silent_venv.ps1 - Silent PowerShell launch using virtual environment<br/>"
        "• create_shortcut.ps1 - Desktop shortcut creator with custom icon",
        body_style
    ))
    
    story.append(Paragraph("4.3 VBScript Files (.vbs)", heading2_style))
    story.append(Paragraph(
        "• launch_invisible_venv.vbs - Completely hidden application launch<br/>"
        "• launch_invisible.vbs - Silent VBScript launcher without console window",
        body_style
    ))
    story.append(PageBreak())
    
    # 5. Generated Content Structure
    story.append(Paragraph("5. Generated Content Structure", heading1_style))
    
    story.append(Paragraph("5.1 Reports Directory", heading2_style))
    story.append(Paragraph(
        "All generated reports are stored in timestamped files within the reports/ directory. "
        "Each analysis session creates a complete set of reports with consistent naming.",
        body_style
    ))
    
    story.append(Paragraph("File Naming Convention:", heading3_style))
    story.append(Paragraph(
        "visual_regression_report_YYYYMMDD_HHMMSS.{extension}<br/><br/>"
        "Where:<br/>"
        "• YYYY = Year (2025)<br/>"
        "• MM = Month (01-12)<br/>"
        "• DD = Day (01-31)<br/>"
        "• HH = Hour (00-23)<br/>"
        "• MM = Minute (00-59)<br/>"
        "• SS = Second (00-59)",
        code_style
    ))
    
    story.append(Paragraph("5.2 Report Types Generated", heading2_style))
    report_types_data = [
        ['File Extension', 'Content Type', 'Description'],
        ['.html', 'Interactive Web Report', 'JavaScript-enabled with sharing buttons'],
        ['.pdf', 'Professional Document', 'Printable report with embedded images'],
        ['.json', 'Structured Data', 'Machine-readable analysis results'],
        ['_visual_comparison.png', 'Visual Analysis', '4-panel comparison with annotations'],
        ['_side_by_side.png', 'Screenshot Comparison', 'Original images displayed side-by-side'],
        ['_difference_heatmap.png', 'Difference Map', 'Color-coded difference intensity'],
        ['_complete_package.zip', 'Full Package', 'All reports and assets bundled'],
        ['_summary.html', 'Executive Summary', 'Condensed key findings report']
    ]
    
    report_types_table = Table(report_types_data, colWidths=[2*inch, 2*inch, 2.5*inch])
    report_types_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(report_types_table)
    
    story.append(Paragraph("5.3 Screenshots Directory", heading2_style))
    story.append(Paragraph(
        "Original screenshots are stored in timestamped subdirectories within screenshots/. "
        "Each analysis session creates a new directory containing:",
        body_style
    ))
    
    story.append(Paragraph(
        "• url1_screenshot.png - Reference image capture<br/>"
        "• url2_screenshot.png - Test image capture<br/>"
        "• page_info.json - Metadata including page titles, dimensions, load times",
        body_style
    ))
    
    story.append(Paragraph("5.4 Visualizations Directory", heading2_style))
    story.append(Paragraph(
        "Advanced analysis visualizations including difference heatmaps, annotated comparisons, "
        "layout shift visualizations, and color analysis maps.",
        body_style
    ))
    story.append(PageBreak())
    
    # 6. Configuration Files
    story.append(Paragraph("6. Configuration Files", heading1_style))
    
    story.append(Paragraph("6.1 requirements.txt - Python Dependencies", heading2_style))
    requirements_data = [
        ['Package', 'Version', 'Purpose'],
        ['selenium', '>=4.15.0', 'Web browser automation and screenshot capture'],
        ['opencv-python', '>=4.8.0', 'Computer vision and image processing'],
        ['Pillow', '>=10.0.0', 'Image manipulation and format conversion'],
        ['numpy', '>=1.24.0', 'Numerical computing and array operations'],
        ['scikit-image', '>=0.21.0', 'Advanced image analysis algorithms'],
        ['scikit-learn', '>=1.3.0', 'Machine learning and anomaly detection'],
        ['webdriver-manager', '>=4.0.0', 'Automatic browser driver management'],
        ['matplotlib', '>=3.7.0', 'Plotting and data visualization'],
        ['reportlab', '>=4.0.0', 'PDF generation and document creation'],
        ['requests', '>=2.31.0', 'HTTP requests and web communication'],
        ['beautifulsoup4', '>=4.12.0', 'HTML parsing and web scraping']
    ]
    
    req_table = Table(requirements_data, colWidths=[1.8*inch, 1.2*inch, 3.2*inch])
    req_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('BACKGROUND', (0, 1), (-1, -1), colors.mistyrose),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(req_table)
    
    story.append(Paragraph("6.2 Virtual Environment (venv/)", heading2_style))
    story.append(Paragraph(
        "The virtual environment isolates the application dependencies and ensures consistent execution "
        "across different systems. Key components include:",
        body_style
    ))
    
    venv_data = [
        ['Directory/File', 'Purpose'],
        ['Scripts/python.exe', 'Python 3.13.2 interpreter'],
        ['Scripts/pip.exe', 'Package manager for dependency installation'],
        ['Scripts/activate.bat', 'Environment activation script'],
        ['Lib/', 'Installed Python packages and dependencies'],
        ['pyvenv.cfg', 'Virtual environment configuration'],
        ['Include/', 'Header files for C extensions'],
        ['share/', 'Shared data and documentation']
    ]
    
    venv_table = Table(venv_data, colWidths=[2.2*inch, 4.3*inch])
    venv_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
    ]))
    story.append(venv_table)
    story.append(PageBreak())
    
    # 7. Testing Framework
    story.append(Paragraph("7. Testing Framework", heading1_style))
    
    story.append(Paragraph("7.1 Automated Testing Scripts", heading2_style))
    testing_data = [
        ['Script', 'Purpose', 'Coverage'],
        ['test_dependencies.py', 'Dependency Verification', 'All required packages and import capabilities'],
        ['test_gui.py', 'Basic GUI Testing', 'Window creation and Tkinter functionality'],
        ['test_gui_detailed.py', 'Advanced GUI Testing', 'User interaction and component testing'],
        ['test_application.py', 'Full Application Testing', 'End-to-end workflow and error handling']
    ]
    
    testing_table = Table(testing_data, colWidths=[2*inch, 2.5*inch, 2*inch])
    testing_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(testing_table)
    
    story.append(Paragraph("7.2 Testing Methodology", heading2_style))
    story.append(Paragraph(
        "The testing framework employs multiple validation levels:",
        body_style
    ))
    
    story.append(Paragraph(
        "• Unit Testing - Individual component functionality<br/>"
        "• Integration Testing - Module interaction verification<br/>"
        "• GUI Testing - User interface component validation<br/>"
        "• End-to-End Testing - Complete workflow verification<br/>"
        "• Performance Testing - Resource usage and timing analysis<br/>"
        "• Error Handling - Exception management and recovery",
        body_style
    ))
    
    story.append(Paragraph("7.3 Continuous Validation", heading2_style))
    story.append(Paragraph(
        "Pre-flight checks are integrated into the launcher scripts to ensure environment readiness "
        "before application startup. This includes dependency verification, path validation, and "
        "system compatibility checks.",
        body_style
    ))
    story.append(PageBreak())
    
    # 8. Application Workflow
    story.append(Paragraph("8. Application Workflow", heading1_style))
    
    story.append(Paragraph("8.1 Complete Analysis Pipeline", heading2_style))
    workflow_data = [
        ['Phase', 'Process', 'Components Involved', 'Output'],
        ['Initialization', 'User Input & Validation', 'main.py, visual_ai_regression.py', 'Validated configuration'],
        ['Setup', 'Browser & Environment Setup', 'screenshot_capture.py, webdriver-manager', 'Ready browser instance'],
        ['Capture', 'Screenshot Acquisition', 'selenium, screenshot_capture.py', 'Image files + metadata'],
        ['Processing', 'Image Preprocessing', 'image_comparison.py, PIL, OpenCV', 'Normalized images'],
        ['Analysis', 'Multi-Algorithm Analysis', 'All analysis modules', 'Analysis results'],
        ['Visualization', 'Difference Visualization', 'matplotlib, image_comparison.py', 'Visual comparisons'],
        ['Reporting', 'Multi-Format Reports', 'report_generator.py, reportlab', 'Complete report set'],
        ['Cleanup', 'Resource Management', 'visual_ai_regression.py', 'Clean environment']
    ]
    
    workflow_table = Table(workflow_data, colWidths=[1.2*inch, 1.5*inch, 2*inch, 1.8*inch])
    workflow_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#9b59b6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lavender),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(workflow_table)
    
    story.append(Paragraph("8.2 Parallel Processing", heading2_style))
    story.append(Paragraph(
        "The application utilizes threading for performance optimization:",
        body_style
    ))
    
    story.append(Paragraph(
        "• Background Analysis - Main analysis runs in separate thread<br/>"
        "• Progress Updates - Real-time status communication via callbacks<br/>"
        "• GUI Responsiveness - Interface remains interactive during processing<br/>"
        "• Resource Management - Efficient memory and CPU utilization",
        body_style
    ))
    
    story.append(Paragraph("8.3 Error Handling Strategy", heading2_style))
    error_data = [
        ['Error Type', 'Handling Strategy', 'Recovery Method'],
        ['Network Errors', 'Retry mechanism with exponential backoff', 'Alternative URL or manual retry'],
        ['Browser Failures', 'Multiple WebDriver fallback options', 'Switch to alternative browser'],
        ['Image Processing', 'Graceful degradation of analysis features', 'Skip failed analysis, continue with others'],
        ['Memory Issues', 'Image downscaling and chunked processing', 'Reduce resolution, process in segments'],
        ['File System Errors', 'Alternative path resolution', 'Temporary directory usage'],
        ['GUI Exceptions', 'Error dialogs with detailed information', 'Application state preservation']
    ]
    
    error_table = Table(error_data, colWidths=[1.5*inch, 2.5*inch, 2.5*inch])
    error_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e67e22')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('BACKGROUND', (0, 1), (-1, -1), colors.bisque),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(error_table)
    story.append(PageBreak())
    
    # Continue with more sections...
    # For brevity, I'll add a few more key sections
    
    # 9. GUI Architecture
    story.append(Paragraph("9. GUI Architecture", heading1_style))
    
    story.append(Paragraph("9.1 Main Window Layout", heading2_style))
    story.append(Paragraph(
        "The main application window uses a hierarchical layout with logical grouping of controls:",
        body_style
    ))
    
    gui_layout = """
┌─ Visual AI Regression Testing Module (1400x900)
├─ Title Section
│  └─ Application title and branding
├─ URL Configuration Panel
│  ├─ Reference URL input field
│  └─ Test URL input field
├─ Analysis Options Panel
│  ├─ Layout Shift Detection ☑
│  ├─ Font/Color Analysis ☑
│  ├─ Element Detection ☑
│  └─ AI-Powered Analysis ☑
├─ Browser & Settings Panel
│  ├─ Browser selection (Chrome/Firefox/Edge)
│  └─ Resolution dropdown (1920x1080, etc.)
├─ Progress Section
│  ├─ Status text display
│  └─ Progress bar indicator
├─ Control Buttons Row
│  ├─ Start Analysis
│  ├─ Browse Screenshots
│  ├─ View Reports
│  ├─ Share Report
│  ├─ Export Package
│  └─ Clear Results
└─ Tabbed Interface (Notebook)
   ├─ 🖼️ Image Comparison Tab
   │  ├─ View Mode Controls
   │  ├─ Zoom Controls (10%-300%)
   │  └─ Scrollable Image Canvas
   └─ 📊 Analysis Results Tab
      └─ Scrollable Text Results
"""
    
    story.append(Paragraph(gui_layout, code_style))
    
    story.append(Paragraph("9.2 Image Comparison Features", heading2_style))
    image_features_data = [
        ['Feature', 'Description', 'User Interaction'],
        ['Side-by-Side View', 'Original screenshots displayed horizontally', 'Default view with labels'],
        ['Overlay View', 'Blended transparency comparison', 'Toggle transparency level'],
        ['Difference View', 'Highlighted pixel differences in red', 'Adjustable sensitivity'],
        ['Zoom Controls', '10% to 300% scaling with smooth transitions', 'Slider + percentage display'],
        ['Pan Navigation', 'Mouse-driven canvas movement', 'Click and drag scrolling'],
        ['Auto-fit', 'Automatic sizing to fit window', 'Smart scaling algorithm'],
        ['Reset View', 'Return to default display settings', 'One-click reset button']
    ]
    
    image_features_table = Table(image_features_data, colWidths=[1.5*inch, 2.5*inch, 2.5*inch])
    image_features_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(image_features_table)
    story.append(PageBreak())
    
    # 10. Technical Specifications
    story.append(Paragraph("10. Technical Specifications", heading1_style))
    
    story.append(Paragraph("10.1 System Requirements", heading2_style))
    system_req_data = [
        ['Component', 'Minimum', 'Recommended'],
        ['Operating System', 'Windows 10', 'Windows 11'],
        ['Python Version', '3.8+', '3.13.2'],
        ['RAM', '4 GB', '8 GB or more'],
        ['Storage', '2 GB free space', '5 GB free space'],
        ['Display', '1024x768', '1920x1080 or higher'],
        ['Network', 'Internet connection', 'Broadband connection'],
        ['Browser', 'Chrome/Firefox/Edge', 'Latest versions']
    ]
    
    sys_req_table = Table(system_req_data, colWidths=[2*inch, 2.5*inch, 2*inch])
    sys_req_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(sys_req_table)
    
    story.append(Paragraph("10.2 Performance Characteristics", heading2_style))
    performance_data = [
        ['Metric', 'Typical Value', 'Notes'],
        ['Startup Time', '3-5 seconds', 'Including GUI initialization'],
        ['Screenshot Capture', '5-15 seconds per URL', 'Depends on page complexity'],
        ['Image Analysis', '10-30 seconds', 'Varies with image size and analysis depth'],
        ['Report Generation', '5-10 seconds', 'All formats including PDF'],
        ['Memory Usage', '200-500 MB', 'Scales with image resolution'],
        ['CPU Usage', '50-80% during analysis', 'Multi-threaded processing'],
        ['Network Bandwidth', '10-50 MB per analysis', 'Depends on page content']
    ]
    
    perf_table = Table(performance_data, colWidths=[2*inch, 2*inch, 2.5*inch])
    perf_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(perf_table)
    
    story.append(Paragraph("10.3 Design Patterns", heading2_style))
    story.append(Paragraph(
        "The application implements several software design patterns for maintainability and extensibility:",
        body_style
    ))
    
    patterns_data = [
        ['Pattern', 'Implementation', 'Benefits'],
        ['Model-View-Controller', 'Separation of data, UI, and logic', 'Maintainable, testable code'],
        ['Observer Pattern', 'Progress callbacks and status updates', 'Loose coupling, real-time feedback'],
        ['Factory Pattern', 'Browser driver instantiation', 'Flexible browser support'],
        ['Strategy Pattern', 'Multiple analysis algorithms', 'Pluggable analysis methods'],
        ['Template Method', 'Report generation workflow', 'Consistent report structure'],
        ['Singleton Pattern', 'Configuration management', 'Global state consistency']
    ]
    
    patterns_table = Table(patterns_data, colWidths=[1.8*inch, 2.2*inch, 2.5*inch])
    patterns_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8e44ad')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lavender),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(patterns_table)
    story.append(PageBreak())
    
    # 11. WCAG Compliance Testing
    story.append(Paragraph("11. WCAG Compliance Testing", heading1_style))
    story.append(Paragraph(
        "The Visual AI Regression Testing Module includes comprehensive Web Content Accessibility Guidelines "
        "(WCAG) 2.1 and 2.2 compliance testing capabilities, making it a complete solution for both visual "
        "regression and accessibility validation.",
        body_style
    ))
    
    story.append(Paragraph("11.1 WCAG Standards Support", heading2_style))
    wcag_standards_data = [
        ['WCAG Version', 'Compliance Levels', 'Key Features'],
        ['WCAG 2.1 AA/AAA', 'Complete implementation', 'Text alternatives, color contrast, keyboard navigation'],
        ['WCAG 2.2 AA/AAA', 'Latest 2023 standards', 'Target size, consistent help, accessible authentication'],
        ['Legal Compliance', 'ADA, Section 508, EN 301 549', 'Ready for regulatory requirements'],
        ['Scoring System', '0-100% with detailed breakdown', 'Professional compliance metrics']
    ]
    
    wcag_standards_table = Table(wcag_standards_data, colWidths=[1.8*inch, 2.2*inch, 2.5*inch])
    wcag_standards_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#9b59b6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f4ecf7')),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(wcag_standards_table)
    
    story.append(Paragraph("11.2 WCAG Testing Categories", heading2_style))
    wcag_categories_data = [
        ['Principle', 'WCAG 2.1 Checks', 'WCAG 2.2 Enhancements'],
        ['Perceivable', 'Alt text, color contrast, adaptable content', 'Enhanced color analysis, graphics contrast'],
        ['Operable', 'Keyboard access, navigation, timing', 'Target size validation, focus appearance'],
        ['Understandable', 'Readable text, predictable UI, input help', 'Consistent help, accessible authentication'],
        ['Robust', 'Valid markup, assistive technology support', 'Future compatibility validation']
    ]
    
    wcag_categories_table = Table(wcag_categories_data, colWidths=[1.5*inch, 2.5*inch, 2.5*inch])
    wcag_categories_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#16a085')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#d1f2eb')),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(wcag_categories_table)
    
    story.append(Paragraph("11.3 Advanced Accessibility Features", heading2_style))
    accessibility_features_data = [
        ['Feature', 'Description', 'Business Impact'],
        ['Color Blindness Simulation', 'Protanopia, deuteranopia, tritanopia testing', 'Inclusive design validation'],
        ['Real-time Contrast Analysis', 'Precise WCAG AA/AAA ratio calculation', 'Visual accessibility compliance'],
        ['Target Size Validation', '24×24 pixel minimum for interactive elements', 'Mobile and motor accessibility'],
        ['Cognitive Barrier Assessment', 'CAPTCHA alternatives, security question analysis', 'Universal access validation'],
        ['Accessibility Heatmaps', 'Visual overlay of accessibility issues', 'Design team collaboration'],
        ['Professional Reporting', 'Executive summaries, remediation guides', 'Stakeholder communication']
    ]
    
    accessibility_features_table = Table(accessibility_features_data, colWidths=[1.7*inch, 2.5*inch, 2.3*inch])
    accessibility_features_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e67e22')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#fdeaa7')),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(accessibility_features_table)
    
    story.append(Paragraph("11.4 WCAG Integration & Usage", heading2_style))
    story.append(Paragraph(
        "WCAG testing is seamlessly integrated into the main analysis workflow. Users can enable accessibility "
        "testing through the GUI checkbox, and results are displayed in a dedicated WCAG Compliance tab with "
        "visual scoring indicators and detailed issue breakdowns. The system provides comparative analysis "
        "between two URLs, showing accessibility improvements or regressions.",
        body_style
    ))
    
    story.append(Paragraph(
        "Key integration points include: GUI checkbox activation, dedicated results tab with visual scoring, "
        "HTML/PDF report integration, JSON data export for CI/CD systems, and comprehensive test coverage "
        "with error resolution capabilities.",
        body_style
    ))
    story.append(PageBreak())
    
    # 12. Conclusion
    story.append(Paragraph("12. Conclusion", heading1_style))
    story.append(Paragraph(
        "The Visual AI Regression Testing Module represents a comprehensive solution for automated visual "
        "comparison and accessibility validation of web applications. Through its modular architecture, "
        "advanced analysis capabilities including WCAG 2.1/2.2 compliance testing, and professional reporting "
        "features, it provides organizations with enterprise-grade tools for maintaining visual quality, "
        "detecting regressions, and ensuring accessibility compliance.",
        body_style
    ))
    
    story.append(Paragraph(
        "The combination of computer vision techniques, machine learning algorithms, comprehensive accessibility "
        "testing, and intuitive user interface design makes this tool accessible to both technical and "
        "non-technical users while providing the depth and accuracy required for professional quality "
        "assurance and accessibility compliance workflows. With the latest WCAG 2.2 support and enhanced "
        "error handling, the module is production-ready for enterprise deployment.",
        body_style
    ))
    
    # Build PDF
    doc.build(story)
    return filename

if __name__ == "__main__":
    try:
        print("🔧 Generating comprehensive PDF documentation...")
        pdf_filename = create_documentation_pdf()
        print(f"✅ PDF documentation generated successfully: {pdf_filename}")
        print(f"📄 File size: {os.path.getsize(pdf_filename) / 1024 / 1024:.2f} MB")
        print(f"📁 Location: {os.path.abspath(pdf_filename)}")
    except Exception as e:
        print(f"❌ Error generating PDF: {e}")
        import traceback
        traceback.print_exc()
