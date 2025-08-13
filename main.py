import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import os
import webbrowser
import shutil
import json
from datetime import datetime
from visual_ai_regression import VisualAIRegression
from PIL import Image, ImageTk
import cv2
import numpy as np

class VisualRegressionGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Visual AI Regression Testing Module")
        
        # Maximize the window with cross-platform support
        try:
            # Windows-specific maximization
            self.root.state('zoomed')
        except tk.TclError:
            try:
                # Unix/Linux maximization
                self.root.attributes('-zoomed', True)
            except tk.TclError:
                # Fallback for other systems - get screen dimensions and maximize manually
                self.root.update_idletasks()
                width = self.root.winfo_screenwidth()
                height = self.root.winfo_screenheight()
                self.root.geometry(f"{width}x{height}+0+0")
        
        # Additional window configuration
        self.root.configure(bg='#f0f0f0')  # Light gray background
        self.root.minsize(1200, 800)  # Set minimum window size
        
        # Initialize the regression module
        self.regression_module = VisualAIRegression()
        self.last_results = None  # Store last analysis results
        
        # Image storage for display
        self.image1_path = None
        self.image2_path = None
        self.diff_image = None
        
        self.setup_ui()
        
    def configure_dark_theme(self):
        """Configure a modern dark theme for the application"""
        style = ttk.Style()
        
        # Configure the style theme
        style.theme_use('clam')  # Use clam as base theme
        
        # Define color palette
        colors = {
            'bg': '#2c3e50',           # Main background (dark blue-gray)
            'fg': '#ecf0f1',           # Main text (light gray)
            'select_bg': '#3498db',    # Selection background (blue)
            'select_fg': '#ffffff',    # Selection text (white)
            'button_bg': '#34495e',    # Button background (lighter gray)
            'button_fg': '#ecf0f1',    # Button text (light gray)
            'entry_bg': '#34495e',     # Entry background
            'entry_fg': '#ecf0f1',     # Entry text
            'frame_bg': '#2c3e50',     # Frame background
            'notebook_bg': '#34495e',  # Notebook tab background
            'active_tab': '#3498db'    # Active tab color
        }
        
        # Configure frame styles
        style.configure('TFrame', background=colors['frame_bg'])
        style.configure('TLabelFrame', background=colors['frame_bg'], foreground=colors['fg'])
        style.configure('TLabelFrame.Label', background=colors['frame_bg'], foreground=colors['fg'])
        
        # Configure button styles
        style.configure('TButton', 
                       background=colors['button_bg'], 
                       foreground=colors['button_fg'],
                       borderwidth=1,
                       focuscolor='none')
        style.map('TButton',
                 background=[('active', colors['select_bg']),
                           ('pressed', colors['select_bg'])])
        
        # Configure entry styles
        style.configure('TEntry',
                       background=colors['entry_bg'],
                       foreground=colors['entry_fg'],
                       borderwidth=1,
                       insertcolor=colors['fg'])
        style.map('TEntry',
                 focuscolor=[('!focus', colors['entry_bg'])])
        
        # Configure label styles
        style.configure('TLabel', background=colors['frame_bg'], foreground=colors['fg'])
        
        # Configure notebook (tab) styles
        style.configure('TNotebook', background=colors['frame_bg'], tabmargins=[2, 5, 2, 0])
        style.configure('TNotebook.Tab', 
                       background=colors['notebook_bg'], 
                       foreground=colors['fg'],
                       padding=[20, 8])
        style.map('TNotebook.Tab',
                 background=[('selected', colors['active_tab']),
                           ('active', colors['select_bg'])],
                 foreground=[('selected', colors['select_fg']),
                           ('active', colors['select_fg'])])
        
        # Configure progressbar
        style.configure('TProgressbar', background=colors['select_bg'])
        
        # Configure checkbutton
        style.configure('TCheckbutton', 
                       background=colors['frame_bg'], 
                       foreground=colors['fg'],
                       focuscolor='none')
        style.map('TCheckbutton',
                 background=[('active', colors['frame_bg'])])

    def setup_ui(self):
        # Main title (compact spacing)
        title_label = tk.Label(
            self.root, 
            text="Visual AI Regression Testing Module", 
            font=("Arial", 16, "bold"),  # Slightly smaller font
            bg='#f0f0f0',  # Original light background
            fg='#2c3e50'   # Dark text for contrast
        )
        title_label.pack(pady=8)  # Reduced from 20 to 8
        
        # Main frame (reduced top padding)
        main_frame = ttk.Frame(self.root)
        main_frame.pack(padx=15, pady=5, fill="both", expand=True)
        
        # URL Input Section (compact)
        url_frame = ttk.LabelFrame(main_frame, text="URL Configuration", padding=10)
        url_frame.pack(fill="x", pady=5)
        
        # URL 1
        ttk.Label(url_frame, text="Reference URL (Original):").grid(row=0, column=0, sticky="w", pady=5)
        self.url1_var = tk.StringVar(value="https://example.com")
        self.url1_entry = ttk.Entry(url_frame, textvariable=self.url1_var, width=60)
        self.url1_entry.grid(row=0, column=1, padx=10, pady=5)
        
        # URL 2
        ttk.Label(url_frame, text="Test URL (New Version):").grid(row=1, column=0, sticky="w", pady=5)
        self.url2_var = tk.StringVar(value="https://example.com")
        self.url2_entry = ttk.Entry(url_frame, textvariable=self.url2_var, width=60)
        self.url2_entry.grid(row=1, column=1, padx=10, pady=5)
        
        # Options Section (ultra-compact)
        options_frame = ttk.LabelFrame(main_frame, text="Analysis Options", padding=5)
        options_frame.pack(fill="x", pady=3)
        
        # Checkboxes for analysis types
        self.layout_shift_var = tk.BooleanVar(value=True)
        self.font_color_var = tk.BooleanVar(value=True)
        self.element_detection_var = tk.BooleanVar(value=True)
        self.ai_analysis_var = tk.BooleanVar(value=True)
        self.wcag_analysis_var = tk.BooleanVar(value=True)  # Add WCAG analysis option
        
        # Create a single row with all checkboxes and controls
        controls_frame = ttk.Frame(options_frame)
        controls_frame.pack(fill="x", pady=5)
        
        # Analysis checkboxes
        ttk.Checkbutton(controls_frame, text="Layout Shifts", variable=self.layout_shift_var).pack(side="left", padx=8)
        ttk.Checkbutton(controls_frame, text="Font/Color", variable=self.font_color_var).pack(side="left", padx=8)
        ttk.Checkbutton(controls_frame, text="Element Detection", variable=self.element_detection_var).pack(side="left", padx=8)
        ttk.Checkbutton(controls_frame, text="AI Analysis", variable=self.ai_analysis_var).pack(side="left", padx=8)
        ttk.Checkbutton(controls_frame, text="WCAG Testing", variable=self.wcag_analysis_var).pack(side="left", padx=8)
        
        # Separator
        ttk.Separator(controls_frame, orient="vertical").pack(side="left", fill="y", padx=10)
        
        # Browser selection
        ttk.Label(controls_frame, text="Browser:").pack(side="left", padx=(10, 5))
        self.browser_var = tk.StringVar(value="chrome")
        browser_combo = ttk.Combobox(controls_frame, textvariable=self.browser_var, values=["chrome", "firefox", "edge"], state="readonly", width=12)
        browser_combo.pack(side="left", padx=5)
        
        # Resolution selection
        ttk.Label(controls_frame, text="Resolution:").pack(side="left", padx=(15, 5))
        self.resolution_var = tk.StringVar(value="1920x1080")
        resolution_combo = ttk.Combobox(controls_frame, textvariable=self.resolution_var, values=["1920x1080", "1366x768", "1440x900", "1280x720"], state="readonly", width=12)
        resolution_combo.pack(side="left", padx=5)
        
        # Progress Section
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding=20)
        progress_frame.pack(fill="x", pady=10)
        
        self.progress_var = tk.StringVar(value="Ready to start analysis...")
        self.progress_label = ttk.Label(progress_frame, textvariable=self.progress_var)
        self.progress_label.pack(anchor="w")
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress_bar.pack(fill="x", pady=5)
        
        # Buttons Section
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=20)
        
        # Start Analysis Button
        self.start_button = ttk.Button(
            button_frame, 
            text="Start Visual Regression Analysis", 
            command=self.start_analysis,
            style="Accent.TButton"
        )
        self.start_button.pack(side="left", padx=5)
        
        # View Reports Button
        self.view_reports_button = ttk.Button(
            button_frame, 
            text="View Generated Reports", 
            command=self.view_reports
        )
        self.view_reports_button.pack(side="left", padx=5)
        
        # Share Report Button
        self.share_button = ttk.Button(
            button_frame, 
            text="📤 Share Report", 
            command=self.share_report
        )
        self.share_button.pack(side="left", padx=5)
        self.share_button.config(state="disabled")  # Initially disabled
        
        # Export Package Button
        self.export_button = ttk.Button(
            button_frame, 
            text="📦 Export Package", 
            command=self.export_package
        )
        self.export_button.pack(side="left", padx=5)
        self.export_button.config(state="disabled")  # Initially disabled
        
        # Browse Screenshots Button
        self.browse_button = ttk.Button(
            button_frame, 
            text="📁 Browse Existing Screenshots", 
            command=self.browse_screenshots
        )
        self.browse_button.pack(side="left", padx=5)
        
        # Clear Button
        self.clear_button = ttk.Button(
            button_frame, 
            text="Clear Results", 
            command=self.clear_results
        )
        self.clear_button.pack(side="left", padx=5)
        
        # Create notebook for tabbed interface (reduced top spacing)
        notebook = ttk.Notebook(main_frame)
        self.notebook = notebook  # Store reference for later use
        notebook.pack(fill="both", expand=True, pady=5)
        
        # Tab 1: Image Comparison
        comparison_frame = ttk.Frame(notebook)
        notebook.add(comparison_frame, text="🖼️ Image Comparison")
        
        self.setup_image_comparison_tab(comparison_frame)
        
        # Tab 2: Analysis Results
        results_frame = ttk.Frame(notebook)
        notebook.add(results_frame, text="📊 Analysis Results")
        
        self.setup_results_tab(results_frame)
        
        # Tab 3: WCAG Compliance
        wcag_frame = ttk.Frame(notebook)
        notebook.add(wcag_frame, text="♿ WCAG Compliance")
        
        self.setup_wcag_tab(wcag_frame)
        
    def setup_image_comparison_tab(self, parent):
        """Setup the image comparison tab"""
        # Main container for images
        # Image container (reduced padding)
        images_container = ttk.Frame(parent)
        images_container.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Top frame for image controls
        controls_frame = ttk.Frame(images_container)
        controls_frame.pack(fill="x", pady=(0, 10))
        
        # View options
        ttk.Label(controls_frame, text="View Mode:").pack(side="left", padx=5)
        self.view_mode_var = tk.StringVar(value="side_by_side")
        view_mode_combo = ttk.Combobox(
            controls_frame, 
            textvariable=self.view_mode_var, 
            values=["side_by_side", "overlay", "difference", "slider"],
            state="readonly",
            width=15
        )
        view_mode_combo.pack(side="left", padx=5)
        view_mode_combo.bind("<<ComboboxSelected>>", self.update_image_view)
        
        # Zoom controls
        ttk.Label(controls_frame, text="Zoom:").pack(side="left", padx=(20, 5))
        self.zoom_var = tk.DoubleVar(value=1.0)
        zoom_scale = ttk.Scale(
            controls_frame, 
            from_=0.1, 
            to=3.0, 
            variable=self.zoom_var,
            orient="horizontal",
            length=200
        )
        zoom_scale.pack(side="left", padx=5)
        zoom_scale.bind("<Motion>", self.update_image_zoom)
        
        self.zoom_label = ttk.Label(controls_frame, text="100%")
        self.zoom_label.pack(side="left", padx=5)
        
        # Reset button
        ttk.Button(controls_frame, text="Reset View", command=self.reset_image_view).pack(side="left", padx=10)
        
        # Images frame
        self.images_frame = ttk.Frame(images_container)
        self.images_frame.pack(fill="both", expand=True)
        
        # Create scrollable canvas for images
        self.canvas = tk.Canvas(self.images_frame, bg="white")  # Original white background
        h_scrollbar = ttk.Scrollbar(self.images_frame, orient="horizontal", command=self.canvas.xview)
        v_scrollbar = ttk.Scrollbar(self.images_frame, orient="vertical", command=self.canvas.yview)
        
        self.canvas.configure(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)
        
        # Pack scrollbars and canvas
        h_scrollbar.pack(side="bottom", fill="x")
        v_scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Create frame inside canvas for image content
        self.canvas_frame = ttk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.canvas_frame, anchor="nw")
        
        # Bind canvas resize
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        self.canvas_frame.bind("<Configure>", self.on_frame_configure)
        
        # Mouse wheel scrolling
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)
        
        # Default message
        self.show_default_message()
        
    def setup_results_tab(self, parent):
        """Setup the analysis results tab"""
        # Results Text with Scrollbar
        text_frame = ttk.Frame(parent)
        text_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.results_text = tk.Text(
            text_frame, 
            wrap="word", 
            height=45,  # Increased from 35 to 45 for more space
            font=("Consolas", 12)
            # Reverted to default light theme colors
        )
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
        self.results_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def setup_wcag_tab(self, parent):
        """Setup the WCAG compliance results tab"""
        # Main container
        main_container = ttk.Frame(parent)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(
            main_container,
            text="♿ WCAG 2.1/2.2 Compliance Analysis",
            font=("Arial", 16, "bold"),
            fg='#2c3e50'
        )
        title_label.pack(pady=(0, 20))
        
        # Compliance scores frame
        scores_frame = ttk.LabelFrame(main_container, text="Compliance Scores", padding=15)
        scores_frame.pack(fill="x", pady=(0, 15))
        
        # Scores header with refresh button
        scores_header = ttk.Frame(scores_frame)
        scores_header.pack(fill="x", pady=(0, 10))
        
        refresh_button = ttk.Button(
            scores_header,
            text="🔄 Refresh WCAG Results",
            command=self.refresh_wcag_display
        )
        refresh_button.pack(side="right")
        
        # Create score display areas
        self.wcag_scores_frame = ttk.Frame(scores_frame)
        self.wcag_scores_frame.pack(fill="x")
        
        # Detailed results frame
        details_frame = ttk.LabelFrame(main_container, text="Detailed WCAG Analysis", padding=15)
        details_frame.pack(fill="both", expand=True)
        
        # WCAG Results Text with Scrollbar
        text_frame = ttk.Frame(details_frame)
        text_frame.pack(fill="both", expand=True)
        
        self.wcag_text = tk.Text(
            text_frame, 
            wrap="word", 
            height=40,  # Increased from 30 to 40 for consistency
            font=("Consolas", 12)
            # Reverted to default light theme colors
        )
        wcag_scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.wcag_text.yview)
        self.wcag_text.configure(yscrollcommand=wcag_scrollbar.set)
        
        self.wcag_text.pack(side="left", fill="both", expand=True)
        wcag_scrollbar.pack(side="right", fill="y")
        
        # Default message
        self.wcag_text.insert(tk.END, "🔍 WCAG Compliance Analysis\n\n")
        self.wcag_text.insert(tk.END, "Run an analysis with WCAG Compliance Testing enabled to see accessibility results here.\n\n")
        self.wcag_text.insert(tk.END, "The analysis will check for:\n")
        self.wcag_text.insert(tk.END, "• Principle 1: Perceivable (Text alternatives, adaptable content, distinguishable)\n")
        self.wcag_text.insert(tk.END, "• Principle 2: Operable (Keyboard accessible, enough time, navigable)\n")
        self.wcag_text.insert(tk.END, "• Principle 3: Understandable (Readable, predictable, input assistance)\n")
        self.wcag_text.insert(tk.END, "• Principle 4: Robust (Compatible with assistive technologies)\n\n")
        self.wcag_text.insert(tk.END, "Compliance levels: A, AA, AAA (AAA being the highest)")
        
        self.wcag_text.config(state="disabled")

    def update_wcag_display(self, wcag_results):
        """Update the WCAG compliance display with analysis results"""
        try:
            print(f"DEBUG: Updating WCAG display with results keys: {list(wcag_results.keys()) if wcag_results else 'None'}")
            
            if not wcag_results:
                print("DEBUG: No WCAG results provided")
                return
            
            # Clear previous scores
            for widget in self.wcag_scores_frame.winfo_children():
                widget.destroy()
            
            # Display scores for both URLs
            if 'url1' in wcag_results and 'url2' in wcag_results:
                print(f"DEBUG: Found URL1 and URL2 in WCAG results")
                print(f"DEBUG: URL1 compliance_score: {wcag_results['url1'].get('compliance_score', 'missing')}")
                print(f"DEBUG: URL2 compliance_score: {wcag_results['url2'].get('compliance_score', 'missing')}")
                
                # URL 1 scores
                url1_frame = ttk.LabelFrame(self.wcag_scores_frame, text="Reference URL (URL1)", padding=10)
                url1_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
                
                self._create_wcag_score_display(url1_frame, wcag_results['url1'])
                
                # URL 2 scores
                url2_frame = ttk.LabelFrame(self.wcag_scores_frame, text="Test URL (URL2)", padding=10)
                url2_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))
                
                self._create_wcag_score_display(url2_frame, wcag_results['url2'])
            else:
                print(f"DEBUG: Missing URL1 or URL2 in WCAG results. Available keys: {list(wcag_results.keys())}")
                
                # Show available data anyway
                for url_key, url_data in wcag_results.items():
                    if isinstance(url_data, dict) and 'compliance_score' in url_data:
                        print(f"DEBUG: Creating frame for {url_key} with score {url_data.get('compliance_score')}")
                        url_frame = ttk.LabelFrame(self.wcag_scores_frame, text=f"{url_key.upper()}", padding=10)
                        url_frame.pack(side="left", fill="both", expand=True, padx=5)
                        self._create_wcag_score_display(url_frame, url_data)
            
            # Update detailed text
            self.wcag_text.config(state="normal")
            self.wcag_text.delete(1.0, tk.END)
            
            # Format detailed results
            self._format_wcag_results(wcag_results)
            
            self.wcag_text.config(state="disabled")
            
            # Force GUI update
            self.wcag_scores_frame.update_idletasks()
            self.wcag_text.update_idletasks();
            
            print(f"DEBUG: WCAG display update completed. Scores frame children: {len(self.wcag_scores_frame.winfo_children())}")
            
        except Exception as e:
            print(f"Error updating WCAG display: {e}")
            import traceback
            traceback.print_exc()
    
    def _create_wcag_score_display(self, parent, wcag_data):
        """Create score display for a single URL"""
        print(f"DEBUG: Creating WCAG score display with data keys: {list(wcag_data.keys()) if wcag_data else 'None'}")
        
        # Check for error condition
        if 'error' in wcag_data:
            error_label = tk.Label(
                parent,
                text=f"Analysis Error: {wcag_data['error'][:50]}...",
                font=("Arial", 10),
                fg='#e74c3c',
                wraplength=200
            )
            error_label.pack(pady=5)
            return
        
        # Overall score
        score = wcag_data.get('compliance_score', 0)
        level = wcag_data.get('compliance_level', 'Unknown')
        
        print(f"DEBUG: Score={score}, Level={level}")
        
        score_label = tk.Label(
            parent,
            text=f"Overall Score: {score:.1f}%",
            font=("Arial", 14, "bold"),
            fg='#2c3e50'
        )
        score_label.pack(pady=5)
        
        level_label = tk.Label(
            parent,
            text=f"Compliance Level: {level}",
            font=("Arial", 12),
            fg='#e74c3c' if level == 'Non-compliant' else '#f39c12' if level == 'A' else '#27ae60'
        )
        level_label.pack(pady=2)
        
        # Issues summary
        total_issues = wcag_data.get('total_issues', 0)
        critical_issues = wcag_data.get('critical_issues', 0)
        
        print(f"DEBUG: Total issues={total_issues}, Critical issues={critical_issues}")
        
        issues_label = tk.Label(
            parent,
            text=f"Issues: {total_issues} total, {critical_issues} critical",
            font=("Arial", 10),
            fg='#7f8c8d'
        )
        issues_label.pack(pady=2)
        
        # Category scores
        categories = wcag_data.get('categories', {})
        print(f"DEBUG: Categories: {list(categories.keys())}")
        
        for category, data in categories.items():
            cat_score = data.get('score', 0)
            cat_issues = len(data.get('issues', []))
            
            cat_frame = ttk.Frame(parent)
            cat_frame.pack(fill="x", pady=2)
            
            cat_label = tk.Label(
                cat_frame,
                text=f"{category.capitalize()}:",
                font=("Arial", 9),
                width=12,
                anchor="w"
            )
            cat_label.pack(side="left")
            
            score_color = '#27ae60' if cat_score >= 90 else '#f39c12' if cat_score >= 70 else '#e74c3c'
            cat_score_label = tk.Label(
                cat_frame,
                text=f"{cat_score:.0f}% ({cat_issues} issues)",
                font=("Arial", 9),
                fg=score_color
            )
            cat_score_label.pack(side="left")
    
    def _format_wcag_results(self, wcag_results):
        """Format WCAG results for detailed display"""
        self.wcag_text.insert(tk.END, "♿ WCAG 2.1 COMPLIANCE ANALYSIS RESULTS\n")
        self.wcag_text.insert(tk.END, "=" * 50 + "\n\n")
        
        # URL 1 Results
        if 'url1' in wcag_results:
            self._format_single_url_wcag(wcag_results['url1'], "Reference URL (URL1)")
        
        # URL 2 Results
        if 'url2' in wcag_results:
            self._format_single_url_wcag(wcag_results['url2'], "Test URL (URL2)")
        
        # Comparison
        if 'comparison' in wcag_results:
            self._format_wcag_comparison(wcag_results['comparison'])
    
    def _format_single_url_wcag(self, wcag_data, url_title):
        """Format WCAG results for a single URL"""
        self.wcag_text.insert(tk.END, f"\n📊 {url_title}\n")
        self.wcag_text.insert(tk.END, "-" * 30 + "\n")
        
        # Overall metrics
        score = wcag_data.get('compliance_score', 0)
        level = wcag_data.get('compliance_level', 'Unknown')
        total_issues = wcag_data.get('total_issues', 0)
        critical_issues = wcag_data.get('critical_issues', 0)
        
        self.wcag_text.insert(tk.END, f"Overall Compliance Score: {score:.1f}%\n")
        self.wcag_text.insert(tk.END, f"Compliance Level: {level}\n")
        self.wcag_text.insert(tk.END, f"Total Issues: {total_issues}\n")
        self.wcag_text.insert(tk.END, f"Critical Issues: {critical_issues}\n\n")
        
        # Category breakdown
        categories = wcag_data.get('categories', {})
        for category, data in categories.items():
            self.wcag_text.insert(tk.END, f"🔍 {category.upper()} PRINCIPLE\n")
            cat_score = data.get('score', 0)
            cat_issues = data.get('issues', [])
            
            self.wcag_text.insert(tk.END, f"Score: {cat_score:.1f}%\n")
            self.wcag_text.insert(tk.END, f"Issues Found: {len(cat_issues)}\n")
            
            if cat_issues:
                self.wcag_text.insert(tk.END, "Key Issues:\n")
                for issue in cat_issues[:3]:  # Show top 3 issues
                    if isinstance(issue, dict):
                        # Issue is a dictionary with detailed info
                        guideline = issue.get('guideline', 'Unknown')
                        description = issue.get('description', 'No description')
                        impact = issue.get('impact', 'unknown')
                        self.wcag_text.insert(tk.END, f"  • {guideline} ({impact}): {description}\n")
                    else:
                        # Issue is a simple string
                        self.wcag_text.insert(tk.END, f"  • {str(issue)}\n")
                
                if len(cat_issues) > 3:
                    self.wcag_text.insert(tk.END, f"  ... and {len(cat_issues) - 3} more issues\n")
            
            self.wcag_text.insert(tk.END, "\n")
    
    def _format_wcag_comparison(self, comparison):
        """Format WCAG comparison results"""
        self.wcag_text.insert(tk.END, "\n🔄 ACCESSIBILITY COMPARISON\n")
        self.wcag_text.insert(tk.END, "-" * 30 + "\n")
        
        score_diff = comparison.get('score_difference', 0)
        assessment = comparison.get('assessment', 'No assessment available')
        
        self.wcag_text.insert(tk.END, f"Overall Assessment: {assessment}\n")
        self.wcag_text.insert(tk.END, f"Score Difference: {score_diff:+.1f}%\n\n")
        
        # Issue comparison
        issue_comp = comparison.get('issue_comparison', {})
        url1_issues = issue_comp.get('url1_issues', 0)
        url2_issues = issue_comp.get('url2_issues', 0)
        issue_diff = issue_comp.get('difference', 0)
        
        self.wcag_text.insert(tk.END, f"Issues Comparison:\n")
        self.wcag_text.insert(tk.END, f"  Reference URL: {url1_issues} issues\n")
        self.wcag_text.insert(tk.END, f"  Test URL: {url2_issues} issues\n")
        self.wcag_text.insert(tk.END, f"  Difference: {issue_diff:+d} issues\n\n")
        
        # Critical issues comparison
        critical_comp = comparison.get('critical_issues_comparison', {})
        url1_critical = critical_comp.get('url1_critical', 0)
        url2_critical = critical_comp.get('url2_critical', 0)
        critical_diff = critical_comp.get('difference', 0)
        
        self.wcag_text.insert(tk.END, f"Critical Issues Comparison:\n")
        self.wcag_text.insert(tk.END, f"  Reference URL: {url1_critical} critical issues\n")
        self.wcag_text.insert(tk.END, f"  Test URL: {url2_critical} critical issues\n")
        self.wcag_text.insert(tk.END, f"  Difference: {critical_diff:+d} critical issues\n")

    def show_default_message(self):
        """Show default message when no images are loaded"""
        # Clear canvas
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
            
        # Show message
        message_frame = ttk.Frame(self.canvas_frame)
        message_frame.pack(fill="both", expand=True, padx=50, pady=50)
        
        ttk.Label(
            message_frame, 
            text="📸 Image Comparison View", 
            font=("Arial", 16, "bold")
        ).pack(pady=20)
        
        ttk.Label(
            message_frame, 
            text="Run an analysis to see screenshot comparisons here.\nImages will be displayed side-by-side with difference highlighting.",
            font=("Arial", 12),
            justify="center"
        ).pack(pady=10)
        
        # Update canvas scroll region
        self.canvas_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
    def on_canvas_configure(self, event):
        """Handle canvas resize"""
        self.canvas.itemconfig(self.canvas_window, width=event.width)
        
    def on_frame_configure(self, event):
        """Handle frame resize"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
    def on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    def update_image_view(self, event=None):
        """Update image view based on selected mode"""
        if hasattr(self, 'image1_path') and self.image1_path and hasattr(self, 'image2_path') and self.image2_path:
            self.display_image_comparison()
            
    def update_image_zoom(self, event=None):
        """Update image zoom"""
        zoom_percent = int(self.zoom_var.get() * 100)
        self.zoom_label.config(text=f"{zoom_percent}%")
        if hasattr(self, 'image1_path') and self.image1_path and hasattr(self, 'image2_path') and self.image2_path:
            self.display_image_comparison()
            
    def reset_image_view(self):
        """Reset image view to defaults"""
        self.zoom_var.set(1.0)
        self.view_mode_var.set("side_by_side")
        self.zoom_label.config(text="100%")
        if hasattr(self, 'image1_path') and self.image1_path and hasattr(self, 'image2_path') and self.image2_path:
            self.display_image_comparison()
        
    def start_analysis(self):
        # Validate URLs
        url1 = self.url1_var.get().strip()
        url2 = self.url2_var.get().strip()
        
        if not url1 or not url2:
            messagebox.showerror("Error", "Please enter both URLs")
            return
            
        if url1 == url2:
            messagebox.showwarning("Warning", "URLs are identical. Results may not be meaningful.")
        
        # Disable start button and start progress
        self.start_button.config(state="disabled")
        self.progress_bar.start()
        self.progress_var.set("Starting analysis...")
        self.results_text.delete(1.0, tk.END)
        
        # Start analysis in a separate thread
        analysis_thread = threading.Thread(target=self.run_analysis)
        analysis_thread.daemon = True
        analysis_thread.start()
        
    def run_analysis(self):
        try:
            # Get configuration
            config = {
                'url1': self.url1_var.get().strip(),
                'url2': self.url2_var.get().strip(),
                'browser': self.browser_var.get(),
                'resolution': self.resolution_var.get(),
                'layout_shift': self.layout_shift_var.get(),
                'font_color': self.font_color_var.get(),
                'element_detection': self.element_detection_var.get(),
                'ai_analysis': self.ai_analysis_var.get(),
                'wcag_analysis': self.wcag_analysis_var.get()  # Include WCAG analysis setting
            }
            
            # Update progress
            self.root.after(0, lambda: self.progress_var.set("Capturing screenshots..."))
            
            # Run the regression analysis
            results = self.regression_module.run_analysis(config, self.update_progress)
            
            # Store results for sharing
            self.last_results = results
            
            # Update UI with results
            self.root.after(0, lambda: self.display_results(results))
            
        except Exception as e:
            error_msg = f"Analysis failed: {str(e)}"
            self.root.after(0, lambda: self.display_error(error_msg))
        finally:
            # Re-enable button and stop progress
            self.root.after(0, self.finish_analysis)
    
    def update_progress(self, message):
        """Callback function to update progress from analysis thread"""
        self.root.after(0, lambda: self.progress_var.set(message))
    
    def display_results(self, results):
        """Display analysis results in the text widget"""
        try:
            print(f"DEBUG: display_results called with results keys: {list(results.keys()) if results else 'None'}")
            
            self.results_text.delete(1.0, tk.END)
            
            # Store results for sharing
            self.last_results = results
            
            # Get the actual analysis configuration to determine what was selected
            analysis_results = results.get('analysis_results', {})
            print(f"DEBUG: analysis_results keys: {list(analysis_results.keys()) if analysis_results else 'None'}")
            
            # Format and display results
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.results_text.insert(tk.END, f"🎉 ANALYSIS COMPLETED SUCCESSFULLY!\n")
            self.results_text.insert(tk.END, "="*50 + "\n\n")
            
            # Display summary - handle both dict and string formats
            summary = results.get('summary', {})
            summary_dict = results.get('summary_dict', {})  # Get structured summary
            
            if summary_dict:
                # Use structured summary for precise values
                self.results_text.insert(tk.END, "📊 COMPREHENSIVE METRICS:\n")
                
                # Core similarity metrics
                ssim_score = summary_dict.get('ssim', summary_dict.get('similarity_score', 0))
                mse = summary_dict.get('mse', 0)
                psnr = summary_dict.get('psnr', 0)
                pixel_diff_pct = summary_dict.get('pixel_difference_percentage', 0)
                
                self.results_text.insert(tk.END, f"  • SSIM (Structural Similarity): {ssim_score:.4f}\n")
                self.results_text.insert(tk.END, f"  • MSE (Mean Squared Error): {mse:.6f}\n")
                self.results_text.insert(tk.END, f"  • PSNR (Peak Signal-to-Noise): {psnr:.2f} dB\n")
                self.results_text.insert(tk.END, f"  • Pixel Differences: {pixel_diff_pct:.2f}%\n")
                
                # Pixel detail metrics
                different_pixels = summary_dict.get('different_pixels', 0)
                total_pixels = summary_dict.get('total_pixels', 0)
                avg_pixel_diff = summary_dict.get('avg_pixel_difference', 0)
                max_pixel_diff = summary_dict.get('max_pixel_difference', 0)
                
                if total_pixels > 0:
                    self.results_text.insert(tk.END, f"  • Changed Pixels: {different_pixels:,} of {total_pixels:,}\n")
                    self.results_text.insert(tk.END, f"  • Average Pixel Change: {avg_pixel_diff:.2f}\n")
                    self.results_text.insert(tk.END, f"  • Maximum Pixel Change: {max_pixel_diff:.2f}\n")
                
                self.results_text.insert(tk.END, "\n📊 ANALYSIS SUMMARY:\n")
                
                # Only show metrics for enabled analysis types
                if self.layout_shift_var.get() and 'layout_differences' in summary_dict:
                    self.results_text.insert(tk.END, f"Layout Differences: {summary_dict.get('layout_differences', 0)}\n")
                
                if self.font_color_var.get() and 'color_differences' in summary_dict:
                    self.results_text.insert(tk.END, f"Color Changes: {summary_dict.get('color_differences', 0)}\n")
                
                if self.element_detection_var.get() and ('missing_elements' in summary_dict or 'new_elements' in summary_dict):
                    missing_count = summary_dict.get('missing_elements', 0)
                    new_count = summary_dict.get('new_elements', 0)
                    self.results_text.insert(tk.END, f"Element Changes: {missing_count + new_count} (Missing: {missing_count}, New: {new_count})\n")
                
                if self.ai_analysis_var.get() and 'ai_anomalies' in summary_dict:
                    self.results_text.insert(tk.END, f"AI Anomalies: {summary_dict.get('ai_anomalies', 0)}\n")
                
                similarity = summary_dict.get('similarity_score', 0)
            elif isinstance(summary, dict):
                self.results_text.insert(tk.END, "📊 SUMMARY:\n")
                self.results_text.insert(tk.END, f"Similarity Score: {summary.get('similarity_score', 0):.1%}\n")
                
                # Only show metrics for enabled analysis types
                if self.layout_shift_var.get() and 'layout_differences' in summary:
                    self.results_text.insert(tk.END, f"Layout Differences: {summary.get('layout_differences', 0)}\n")
                
                if self.font_color_var.get() and 'color_differences' in summary:
                    self.results_text.insert(tk.END, f"Color Changes: {summary.get('color_differences', 0)}\n")
                
                if self.element_detection_var.get():
                    missing_elements = len(analysis_results.get('missing_elements', []))
                    new_elements = len(analysis_results.get('new_elements', []))
                    self.results_text.insert(tk.END, f"Element Changes: {missing_elements + new_elements} (Missing: {missing_elements}, New: {new_elements})\n")
                
                if self.ai_analysis_var.get():
                    ai_analysis = analysis_results.get('ai_analysis', {})
                    # Check if anomaly was detected (boolean) not length of anomalies list
                    ai_anomalies = 1 if ai_analysis.get('anomaly_detected', False) else 0
                    self.results_text.insert(tk.END, f"AI Anomalies: {ai_anomalies}\n")
                
                similarity = summary.get('similarity_score', 0)
            else:
                # Handle case where summary is a string or missing
                self.results_text.insert(tk.END, "📊 SUMMARY:\n")
                if isinstance(summary, str):
                    self.results_text.insert(tk.END, f"Summary: {summary}\n")
                else:
                    self.results_text.insert(tk.END, "Summary data not available\n")
                similarity = analysis_results.get('similarity_score', 0)  # Try to get from analysis results
            
            # Add detailed results for enabled analysis types only
            self.results_text.insert(tk.END, "\n📋 DETAILED RESULTS:\n")
            
            # Layout shifts (only if enabled)
            if self.layout_shift_var.get() and 'layout_shifts' in analysis_results:
                layout_shifts = analysis_results.get('layout_shifts', [])
                self.results_text.insert(tk.END, f"🔄 Layout Shifts: {len(layout_shifts)} detected\n")
                if layout_shifts:
                    for i, shift in enumerate(layout_shifts[:3], 1):  # Show first 3
                        distance = shift.get('distance', 0)
                        shift_x = shift.get('shift_x', 0)
                        shift_y = shift.get('shift_y', 0)
                        self.results_text.insert(tk.END, f"  • Shift {i}: Distance {distance:.1f}px, Movement ({shift_x}, {shift_y})\n")
                    if len(layout_shifts) > 3:
                        self.results_text.insert(tk.END, f"  ... and {len(layout_shifts) - 3} more\n")
            
            # Color differences (only if enabled)
            if self.font_color_var.get() and 'color_differences' in analysis_results:
                color_diffs = analysis_results.get('color_differences', [])
                self.results_text.insert(tk.END, f"🎨 Color Changes: {len(color_diffs)} detected\n")
                if color_diffs:
                    for i, diff in enumerate(color_diffs[:3], 1):  # Show first 3
                        position = diff.get('position', (0, 0, 0, 0))
                        color_distance = diff.get('color_distance', 0)
                        area = diff.get('area', 0)
                        self.results_text.insert(tk.END, f"  • Change {i}: Area {area:.0f}px², Distance {color_distance:.1f} at ({position[0]}, {position[1]})\n")
                    if len(color_diffs) > 3:
                        self.results_text.insert(tk.END, f"  ... and {len(color_diffs) - 3} more\n")
            
            # Element detection (only if enabled)
            if self.element_detection_var.get():
                missing_elements = analysis_results.get('missing_elements', [])
                new_elements = analysis_results.get('new_elements', [])
                overlapping_elements = analysis_results.get('overlapping_elements', [])
                
                if missing_elements or new_elements or overlapping_elements:
                    self.results_text.insert(tk.END, f"🔍 Element Changes:\n")
                    if missing_elements:
                        self.results_text.insert(tk.END, f"  • Missing Elements: {len(missing_elements)}\n")
                    if new_elements:
                        self.results_text.insert(tk.END, f"  • New Elements: {len(new_elements)}\n")
                    if overlapping_elements:
                        self.results_text.insert(tk.END, f"  • Overlapping Elements: {len(overlapping_elements)}\n")
            
            # AI analysis (only if enabled)
            if self.ai_analysis_var.get() and 'ai_analysis' in analysis_results:
                ai_results = analysis_results.get('ai_analysis', {})
                anomaly_detected = ai_results.get('anomaly_detected', False)
                confidence = ai_results.get('confidence', 0)
                feature_distance = ai_results.get('feature_distance', 0)
                
                self.results_text.insert(tk.END, f"🤖 AI Analysis:\n")
                self.results_text.insert(tk.END, f"  • Anomaly Detected: {'Yes' if anomaly_detected else 'No'}\n")
                self.results_text.insert(tk.END, f"  • Feature Distance: {feature_distance:.2f}\n")
                self.results_text.insert(tk.END, f"  • Confidence: {confidence:.1%}\n")
                
                # Show semantic analysis if available
                semantic = ai_results.get('semantic_analysis', {})
                if semantic:
                    layout_changes = semantic.get('layout_changes', 0)
                    content_changes = semantic.get('content_changes', 0)
                    style_changes = semantic.get('style_changes', 0)
                    structural_changes = semantic.get('structural_changes', 0)
                    self.results_text.insert(tk.END, f"  • Semantic Changes: Layout({layout_changes}), Content({content_changes}), Style({style_changes}), Structural({structural_changes})\n")
            
            # Add WCAG summary if available and enabled
            if self.wcag_analysis_var.get():
                wcag_analysis = analysis_results.get('wcag_analysis') or results.get('wcag_analysis')
                if wcag_analysis:
                    print("DEBUG: Found WCAG analysis in results, displaying summary...")
                    self.results_text.insert(tk.END, f"\n♿ ACCESSIBILITY SUMMARY:\n")
                    if 'url1' in wcag_analysis:
                        url1_score = wcag_analysis['url1'].get('compliance_score', 0)
                        url1_level = wcag_analysis['url1'].get('compliance_level', 'Unknown')
                        self.results_text.insert(tk.END, f"Reference URL WCAG Score: {url1_score:.1f}% ({url1_level})\n")
                    
                    if 'url2' in wcag_analysis:
                        url2_score = wcag_analysis['url2'].get('compliance_score', 0)
                        url2_level = wcag_analysis['url2'].get('compliance_level', 'Unknown')
                        self.results_text.insert(tk.END, f"Test URL WCAG Score: {url2_score:.1f}% ({url2_level})\n")
                    
                    if 'comparison' in wcag_analysis:
                        assessment = wcag_analysis['comparison'].get('assessment', 'No comparison available')
                        self.results_text.insert(tk.END, f"Accessibility Assessment: {assessment}\n")
                    
                    # Update WCAG tab
                    print("DEBUG: Calling update_wcag_display...")
                    self.update_wcag_display(wcag_analysis)
                    
                    # Switch to WCAG tab to show results
                    self.root.after(100, lambda: self.notebook.select(2))  # WCAG is tab index 2
                else:
                    print("DEBUG: No WCAG analysis found in results")
            
            self.results_text.insert(tk.END, "\n📁 GENERATED REPORTS:\n")
            reports = results.get('reports', {})
            for report_type, report_path in reports.items():
                if os.path.exists(report_path):
                    self.results_text.insert(tk.END, f"✅ {report_type.upper()}: {os.path.basename(report_path)}\n")
            
            self.results_text.insert(tk.END, "\n🎯 RECOMMENDATION:\n")
            if similarity > 0.95:
                self.results_text.insert(tk.END, "✅ No significant differences detected. Safe to proceed.\n")
            elif similarity > 0.9:
                self.results_text.insert(tk.END, "✅ Minor differences. Review recommended but likely acceptable.\n")
            elif similarity > 0.7:
                self.results_text.insert(tk.END, "⚠️ Moderate differences. Manual review required.\n")
            else:
                self.results_text.insert(tk.END, "❌ Significant differences. Thorough review required.\n")
            
            self.results_text.insert(tk.END, "\n📤 Use the sharing buttons to distribute results!")
            
            self.progress_var.set("Analysis completed! Use sharing options above.")
            
        except Exception as e:
            error_msg = f"Error displaying results: {str(e)}"
            print(f"ERROR in display_results: {error_msg}")
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, f"❌ {error_msg}\n")
            # Still try to update WCAG if available
            try:
                wcag_analysis = results.get('wcag_analysis')
                if wcag_analysis and self.wcag_analysis_var.get():
                    self.update_wcag_display(wcag_analysis)
            except Exception as wcag_e:
                print(f"ERROR updating WCAG display: {wcag_e}")
        
        # Enable sharing buttons
        self.share_button.config(state="normal")
        self.export_button.config(state="normal")
        
        # Auto-open the main HTML report
        html_report = reports.get('html')
        if html_report and os.path.exists(html_report):
            try:
                webbrowser.open(f'file://{os.path.abspath(html_report)}')
            except:
                pass  # Ignore if browser opening fails
    
    def display_error(self, error_msg):
        """Display error message"""
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, f"ERROR: {error_msg}\n")
        self.progress_var.set("Analysis failed!")
        messagebox.showerror("Analysis Error", error_msg)
    
    def finish_analysis(self):
        """Reset UI after analysis completion and enable sharing buttons"""
        self.start_button.config(state="normal")
        self.progress_bar.stop()
        
        # Enable sharing buttons if we have results
        if hasattr(self, 'last_results') and self.last_results:
            self.share_button.config(state="normal")
            self.export_button.config(state="normal")
    
    def view_reports(self):
        """Open the reports directory"""
        reports_dir = os.path.join(os.getcwd(), "reports")
        if os.path.exists(reports_dir):
            os.startfile(reports_dir)
        else:
            messagebox.showinfo("No Reports", "No reports have been generated yet.")
    
    def clear_results(self):
        """Clear the results text area"""
        self.results_text.delete(1.0, tk.END)
        self.progress_var.set("Ready to start analysis...")
        
        # Disable sharing buttons when clearing results
        self.share_button.config(state="disabled")
        self.export_button.config(state="disabled")
        self.last_results = None

    def share_report(self):
        """Open sharing options dialog"""
        if not hasattr(self, 'last_results') or not self.last_results:
            messagebox.showwarning("No Results", "Please run an analysis first!")
            return
        
        # Debug info
        reports = self.last_results.get('reports', {})
        print(f"Debug: Available reports: {list(reports.keys())}")
        print(f"Debug: Reports exist check: {[(k, os.path.exists(v) if v else False) for k, v in reports.items()]}")
        
        share_window = tk.Toplevel(self.root)
        share_window.title("📤 Share Report")
        share_window.geometry("500x500")
        share_window.configure(bg='#f0f0f0')  # Original light background
        
        # Center the window
        share_window.transient(self.root)
        share_window.grab_set()
        
        # Main frame
        main_frame = ttk.Frame(share_window)
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="📤 Share Your Visual Regression Report", 
            font=("Arial", 14, "bold"),
            bg='#f0f0f0'  # Original light background
        )
        title_label.pack(pady=(0, 20))
        
        # Show available reports
        info_frame = ttk.LabelFrame(main_frame, text="📋 Available Reports", padding=10)
        info_frame.pack(fill="x", pady=10)
        
        available_reports = [(k, v) for k, v in reports.items() if os.path.exists(v)]
        if available_reports:
            for report_type, report_path in available_reports:
                size = os.path.getsize(report_path) / 1024  # KB
                ttk.Label(
                    info_frame, 
                    text=f"✅ {report_type.upper()}: {os.path.basename(report_path)} ({size:.1f} KB)"
                ).pack(anchor="w", pady=2)
        else:
            ttk.Label(info_frame, text="⚠️ No report files found").pack(anchor="w")
        
        # Quick share section
        quick_frame = ttk.LabelFrame(main_frame, text="🚀 Quick Share", padding=15)
        quick_frame.pack(fill="x", pady=10)
        
        ttk.Button(
            quick_frame, 
            text="🌐 Open in Browser", 
            command=self.open_report_browser,
            width=25
        ).pack(pady=5)
        
        ttk.Button(
            quick_frame, 
            text="📧 Share via Email", 
            command=self.share_via_email,
            width=25
        ).pack(pady=5)
        
        ttk.Button(
            quick_frame, 
            text="🔗 Copy Report Link", 
            command=self.copy_report_link,
            width=25
        ).pack(pady=5)
        
        # File sharing section
        file_frame = ttk.LabelFrame(main_frame, text="📁 File Sharing", padding=15)
        file_frame.pack(fill="x", pady=10)
        
        ttk.Button(
            file_frame, 
            text="📦 Save Complete Package", 
            command=self.save_package,
            width=25
        ).pack(pady=5)
        
        ttk.Button(
            file_frame, 
            text="📄 Save PDF Report", 
            command=self.save_pdf,
            width=25
        ).pack(pady=5)
        
        ttk.Button(
            file_frame, 
            text="🖼️ Save Visual Comparison", 
            command=self.save_visual,
            width=25
        ).pack(pady=5)
        
        # Advanced options
        advanced_frame = ttk.LabelFrame(main_frame, text="⚙️ Advanced", padding=15)
        advanced_frame.pack(fill="x", pady=10)
        
        ttk.Button(
            advanced_frame, 
            text="📊 View JSON Data", 
            command=self.view_json_data,
            width=25
        ).pack(pady=5)
        
        ttk.Button(
            advanced_frame, 
            text="📁 Open Reports Folder", 
            command=lambda: os.startfile("reports") if os.path.exists("reports") else messagebox.showinfo("Info", "Reports folder not found"),
            width=25
        ).pack(pady=5)
        
        # Close button
        ttk.Button(
            main_frame, 
            text="Close", 
            command=share_window.destroy
        ).pack(pady=20)

    def export_package(self):
        """Export complete package for sharing"""
        if not self.last_results:
            messagebox.showwarning("No Results", "Please run an analysis first!")
            return
        
        try:
            reports = self.last_results.get('reports', {})
            
            if not reports:
                messagebox.showerror("Error", "No reports found to export!")
                return
            
            # Check if package already exists
            package_path = reports.get('package')
            
            if not package_path or not os.path.exists(package_path):
                # Create package on demand if it doesn't exist
                messagebox.showinfo("Creating Package", "Creating export package, please wait...")
                
                try:
                    # Import needed modules
                    import zipfile
                    from datetime import datetime
                    
                    # Create a new package
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    package_name = f"visual_regression_package_{timestamp}.zip"
                    package_path = os.path.join("reports", package_name)
                    
                    # Create ZIP package manually
                    with zipfile.ZipFile(package_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                        # Add all available reports
                        files_added = 0
                        for report_type, report_file_path in reports.items():
                            if report_type != 'package' and os.path.exists(report_file_path):
                                zipf.write(report_file_path, os.path.basename(report_file_path))
                                files_added += 1
                        
                        # Add screenshots if available
                        screenshots = self.last_results.get('screenshots', {})
                        for shot_type, shot_path in screenshots.items():
                            if os.path.exists(shot_path):
                                zipf.write(shot_path, f"screenshot_{shot_type}{os.path.splitext(shot_path)[1]}")
                                files_added += 1
                        
                        # Add a README
                        readme_content = self._create_package_readme()
                        zipf.writestr("README.txt", readme_content)
                        files_added += 1
                    
                    if files_added == 0:
                        messagebox.showerror("Error", "No files available to package!")
                        return
                        
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to create package: {str(e)}")
                    return
            
            # Ask user where to save
            save_path = filedialog.asksaveasfilename(
                title="Save Visual Regression Package",
                defaultextension=".zip",
                filetypes=[("ZIP files", "*.zip"), ("All files", "*.*")],
                initialname=f"visual_regression_package_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
            )
            
            if save_path:
                # Copy the package to the chosen location
                shutil.copy2(package_path, save_path)
                
                # Get file size for user info
                file_size = os.path.getsize(save_path)
                file_size_mb = file_size / (1024 * 1024)
                
                messagebox.showinfo(
                    "Export Successful", 
                    f"Package exported successfully!\n\n"
                    f"📁 Location: {save_path}\n"
                    f"📊 Size: {file_size_mb:.1f} MB\n\n"
                    f"This ZIP file contains:\n"
                    f"• All generated reports\n"
                    f"• Original screenshots\n"
                    f"• Analysis data\n"
                    f"• README file\n\n"
                    f"You can now share this file via email, cloud storage, or any file sharing method."
                )
                
                # Ask if user wants to open the folder
                if messagebox.askyesno("Open Folder", "Would you like to open the folder containing the exported package?"):
                    try:
                        folder_path = os.path.dirname(save_path)
                        os.startfile(folder_path)
                    except Exception as e:
                        messagebox.showwarning("Warning", f"Could not open folder: {str(e)}")
                    
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export package: {str(e)}\n\nPlease check that:\n• Analysis has completed\n• Reports folder exists\n• You have write permissions")

    def open_report_browser(self):
        """Open the main HTML report in browser"""
        try:
            if not self.last_results:
                messagebox.showwarning("No Results", "Please run an analysis first!")
                return
                
            reports = self.last_results.get('reports', {})
            
            # Try HTML report first
            html_path = reports.get('html')
            if html_path and os.path.exists(html_path):
                webbrowser.open(f'file://{os.path.abspath(html_path)}')
                messagebox.showinfo("Success", "HTML report opened in your default browser!")
                return
                
            # Try summary report
            summary_path = reports.get('summary')
            if summary_path and os.path.exists(summary_path):
                webbrowser.open(f'file://{os.path.abspath(summary_path)}')
                messagebox.showinfo("Success", "Summary report opened in your default browser!")
                return
                
            # If no HTML reports, open the reports folder
            reports_dir = "reports"
            if os.path.exists(reports_dir):
                os.startfile(reports_dir)
                messagebox.showinfo("Reports Folder", "No HTML reports found. Reports folder opened instead.")
            else:
                messagebox.showerror("Error", "No reports or reports folder found!")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open report: {str(e)}")

    def share_via_email(self):
        """Prepare email with report"""
        try:
            if not self.last_results:
                messagebox.showwarning("No Results", "Please run an analysis first!")
                return
                
            reports = self.last_results.get('reports', {})
            summary = self.last_results.get('summary', {})
            summary_dict = self.last_results.get('summary_dict', {})  # Get structured summary
            
            # Check if we have any reports
            if not reports:
                messagebox.showerror("Error", "No reports found to share!")
                return
            
            subject = "Visual Regression Analysis Report"
            
            # Create a detailed summary for the email - use structured data if available
            if summary_dict:
                similarity_score = summary_dict.get('similarity_score', 0)
                layout_diffs = summary_dict.get('layout_differences', 0)
                color_diffs = summary_dict.get('color_differences', 0)
            else:
                similarity_score = summary.get('similarity_score', 0)
                layout_diffs = summary.get('layout_differences', 0)
                color_diffs = summary.get('color_differences', 0)
            
            body = f"""Hi,

I'm sharing the results of a visual regression analysis that was just completed.

ANALYSIS SUMMARY:
- Overall Similarity: {similarity_score:.1%}
- Layout Differences: {layout_diffs}
- Color Changes: {color_diffs}
- Status: {'PASSED' if similarity_score > 0.9 else 'WARNING' if similarity_score > 0.7 else 'FAILED'}

AVAILABLE REPORTS:
"""
            
            # Add available reports to email body
            for report_type, report_path in reports.items():
                if os.path.exists(report_path):
                    body += f"- {report_type.upper()}: {os.path.basename(report_path)}\n"
            
            body += f"""
RECOMMENDATION:
{self._get_recommendation(similarity_score)}

The complete analysis package is available in the reports folder.
Please find the reports at: {os.path.abspath('reports')}

Best regards,
Visual AI Regression Module"""
            
            # Create mailto link with proper encoding
            import urllib.parse
            subject_encoded = urllib.parse.quote(subject)
            body_encoded = urllib.parse.quote(body)
            
            mailto_link = f"mailto:?subject={subject_encoded}&body={body_encoded}"
            
            # Try to open email client
            try:
                webbrowser.open(mailto_link)
                messagebox.showinfo(
                    "Email Prepared", 
                    f"Your default email client has been opened with the report summary.\n\n"
                    f"Available reports:\n" + 
                    "\n".join([f"- {k}: {os.path.basename(v)}" for k, v in reports.items() if os.path.exists(v)]) +
                    f"\n\nReports location: {os.path.abspath('reports')}\n\n"
                    "Please attach the report files manually if needed."
                )
            except Exception as e:
                # Fallback: copy email content to clipboard
                email_content = f"Subject: {subject}\n\n{body}"
                self.root.clipboard_clear()
                self.root.clipboard_append(email_content)
                messagebox.showinfo(
                    "Email Content Copied", 
                    "Unable to open email client. Email content has been copied to clipboard.\n"
                    "You can paste this into your email application."
                )
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to prepare email: {str(e)}")

    def copy_report_link(self):
        """Copy report file path to clipboard"""
        try:
            if not self.last_results:
                messagebox.showwarning("No Results", "Please run an analysis first!")
                return
                
            reports = self.last_results.get('reports', {})
            
            # Try to find the best report to share
            html_path = reports.get('html')
            if html_path and os.path.exists(html_path):
                full_path = os.path.abspath(html_path)
                file_url = f"file:///{full_path.replace(os.sep, '/')}"
                
                self.root.clipboard_clear()
                self.root.clipboard_append(file_url)
                
                messagebox.showinfo(
                    "Link Copied", 
                    f"Report link copied to clipboard!\n\n"
                    f"Local file URL: {file_url}\n\n"
                    f"You can paste this link to share with others on the same network,\n"
                    f"or use the Export Package option for remote sharing."
                )
            else:
                # Try other report types
                available_reports = [k for k, v in reports.items() if os.path.exists(v)]
                if available_reports:
                    first_report = reports[available_reports[0]]
                    full_path = os.path.abspath(first_report)
                    self.root.clipboard_clear()
                    self.root.clipboard_append(full_path)
                    
                    messagebox.showinfo(
                        "Path Copied", 
                        f"Report path copied to clipboard!\n\n"
                        f"File: {os.path.basename(first_report)}\n"
                        f"Path: {full_path}\n\n"
                        f"Available reports: {', '.join(available_reports)}"
                    )
                else:
                    messagebox.showerror("Error", "No report files found!")
                    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy link: {str(e)}")

    def save_package(self):
        """Same as export_package for consistency"""
        self.export_package()

    def save_pdf(self):
        """Save PDF report to chosen location"""
        try:
            reports = self.last_results.get('reports', {})
            pdf_path = reports.get('pdf')
            
            if not pdf_path or not os.path.exists(pdf_path):
                messagebox.showerror("Error", "PDF report not found!")
                return
            
            save_path = filedialog.asksaveasfilename(
                title="Save PDF Report",
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
                initialname=f"visual_regression_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            )
            
            if save_path:
                shutil.copy2(pdf_path, save_path)
                messagebox.showinfo("Success", f"PDF report saved to: {save_path}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save PDF: {str(e)}")

    def save_visual(self):
        """Save visual comparison image"""
        try:
            reports = self.last_results.get('reports', {})
            visual_path = reports.get('visual')
            
            if not visual_path or not os.path.exists(visual_path):
                messagebox.showerror("Error", "Visual comparison not found!")
                return
            
            save_path = filedialog.asksaveasfilename(
                title="Save Visual Comparison",
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                initialname=f"visual_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            )
            
            if save_path:
                shutil.copy2(visual_path, save_path)
                messagebox.showinfo("Success", f"Visual comparison saved to: {save_path}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save visual comparison: {str(e)}")

    def view_json_data(self):
        """View JSON analysis data"""
        try:
            reports = self.last_results.get('reports', {})
            json_path = reports.get('json')
            
            if json_path and os.path.exists(json_path):
                os.startfile(json_path)
                messagebox.showinfo("Success", "JSON data file opened!")
            else:
                messagebox.showerror("Error", "JSON data not found!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open JSON data: {str(e)}")

    def _get_recommendation(self, similarity_score):
        """Get recommendation based on similarity score"""
        if similarity_score > 0.95:
            return "✅ No significant visual differences detected. Safe to proceed with deployment."
        elif similarity_score > 0.9:
            return "✅ Minor differences detected. Review recommended but changes are likely acceptable."
        elif similarity_score > 0.7:
            return "⚠️ Moderate differences detected. Manual review required before proceeding."
        else:
            return "❌ Significant differences detected. Thorough review and testing required before deployment."

    def _create_package_readme(self):
        """Create README content for the export package"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        summary = self.last_results.get('summary', {})
        summary_dict = self.last_results.get('summary_dict', {})  # Get structured summary
        
        # Use structured data if available
        if summary_dict:
            similarity_score = summary_dict.get('similarity_score', 0)
            layout_diffs = summary_dict.get('layout_differences', 0)
            color_diffs = summary_dict.get('color_differences', 0)
            ai_anomalies = summary_dict.get('ai_anomalies', 0)
        else:
            similarity_score = summary.get('similarity_score', 0)
            layout_diffs = summary.get('layout_differences', 0)
            color_diffs = summary.get('color_differences', 0)
            ai_anomalies = len(self.last_results.get('ai_analysis', {}).get('anomalies', []))
        
        return f"""Visual Regression Analysis Package
=====================================

Generated: {timestamp}
Tool: Visual AI Regression Module v1.0

ANALYSIS SUMMARY:
- Overall Similarity: {similarity_score:.1%}
- Layout Differences: {layout_diffs}
- Color Changes: {color_diffs}
- AI Anomalies: {ai_anomalies}

FILES INCLUDED:
- HTML Report: Interactive web-based report
- PDF Report: Printable summary report  
- JSON Data: Raw analysis data for integration
- Visual Comparisons: Annotated difference images
- Screenshots: Original captured images
- README.txt: This file

HOW TO VIEW:
1. Open the HTML file in any web browser for interactive viewing
2. Use the PDF for printing or offline viewing
3. Screenshots show the original captured images
4. JSON file contains detailed analysis data

SHARING:
This package contains all necessary files for sharing analysis results.
You can send this entire ZIP file via email, upload to cloud storage,
or share through any file transfer method.

STATUS: {self._get_recommendation(similarity_score)}

Generated by Visual AI Regression Module
"""

    def display_image_comparison(self):
        """Display image comparison based on current view mode"""
        if not (hasattr(self, 'image1_path') and self.image1_path and 
                hasattr(self, 'image2_path') and self.image2_path):
            self.show_default_message()
            return
            
        # Clear current display
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
            
        try:
            # Load images
            image1 = Image.open(self.image1_path)
            image2 = Image.open(self.image2_path)
            
            # Get current view mode
            view_mode = self.view_mode_var.get()
            zoom = self.zoom_var.get()
            
            if view_mode == "side_by_side":
                self._display_side_by_side(image1, image2, zoom)
            elif view_mode == "overlay":
                self._display_overlay(image1, image2, zoom)
            elif view_mode == "difference":
                self._display_difference(image1, image2, zoom)
            elif view_mode == "slider":
                self._display_slider(image1, image2, zoom)
                
        except Exception as e:
            # Show error message
            error_frame = ttk.Frame(self.canvas_frame)
            error_frame.pack(fill="both", expand=True, padx=50, pady=50)
            
            ttk.Label(
                error_frame, 
                text="❌ Error Loading Images", 
                font=("Arial", 16, "bold")
            ).pack(pady=20)
            
            ttk.Label(
                error_frame, 
                text=f"Failed to load images: {str(e)}",
                font=("Arial", 12),
                justify="center"
            ).pack(pady=10)
        
        # Update canvas scroll region
        self.canvas_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def _display_side_by_side(self, image1, image2, zoom):
        """Display images side by side"""
        # Create main container
        container = ttk.Frame(self.canvas_frame)
        container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create frames for each image
        left_frame = ttk.LabelFrame(container, text="URL 1 Screenshot", padding=10)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        right_frame = ttk.LabelFrame(container, text="URL 2 Screenshot", padding=10)
        right_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        # Resize images for display
        max_display_size = (600, 800)  # Max size for each image
        display_size = (
            int(max_display_size[0] * zoom),
            int(max_display_size[1] * zoom)
        )
        
        # Resize images maintaining aspect ratio
        img1_resized = self._resize_image_for_display(image1, display_size)
        img2_resized = self._resize_image_for_display(image2, display_size)
        
        # Convert to PhotoImage
        photo1 = ImageTk.PhotoImage(img1_resized)
        photo2 = ImageTk.PhotoImage(img2_resized)
        
        # Create labels to display images
        label1 = tk.Label(left_frame, image=photo1)
        label1.image = photo1  # Keep a reference
        label1.pack()
        
        label2 = tk.Label(right_frame, image=photo2)
        label2.image = photo2  # Keep a reference
        label2.pack()
    
    def _display_overlay(self, image1, image2, zoom):
        """Display images as overlay with transparency"""
        # Create container
        container = ttk.LabelFrame(self.canvas_frame, text="Overlay Comparison", padding=10)
        container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Resize images to match
        max_display_size = (800, 1000)
        display_size = (
            int(max_display_size[0] * zoom),
            int(max_display_size[1] * zoom)
        )
        
        img1_resized = self._resize_image_for_display(image1, display_size)
        img2_resized = self._resize_image_for_display(image2, display_size)
        
        # Make sure both images are the same size
        final_size = (
            min(img1_resized.size[0], img2_resized.size[0]),
            min(img1_resized.size[1], img2_resized.size[1])
        )
        
        img1_resized = img1_resized.resize(final_size, Image.Resampling.LANCZOS)
        img2_resized = img2_resized.resize(final_size, Image.Resampling.LANCZOS)
        
        # Create overlay
        overlay = Image.blend(img1_resized.convert('RGBA'), img2_resized.convert('RGBA'), 0.5)
        
        # Convert to PhotoImage
        photo = ImageTk.PhotoImage(overlay)
        
        # Display
        label = tk.Label(container, image=photo)
        label.image = photo  # Keep a reference
        label.pack()
    
    def _display_difference(self, image1, image2, zoom):
        """Display difference highlighting"""
        # Create container
        container = ttk.LabelFrame(self.canvas_frame, text="Difference Analysis", padding=10)
        container.pack(fill="both", expand=True, padx=10, pady=10)
        
        try:
            # Resize images
            max_display_size = (800, 1000)
            display_size = (
                int(max_display_size[0] * zoom),
                int(max_display_size[1] * zoom)
            )
            
            img1_resized = self._resize_image_for_display(image1, display_size)
            img2_resized = self._resize_image_for_display(image2, display_size)
            
            # Make sure both images are the same size
            final_size = (
                min(img1_resized.size[0], img2_resized.size[0]),
                min(img1_resized.size[1], img2_resized.size[1])
            )
            
            img1_resized = img1_resized.resize(final_size, Image.Resampling.LANCZOS)
            img2_resized = img2_resized.resize(final_size, Image.Resampling.LANCZOS)
            
            # Convert to numpy arrays
            arr1 = np.array(img1_resized)
            arr2 = np.array(img2_resized)
            
            # Calculate difference
            diff = cv2.absdiff(arr1, arr2)
            
            # Enhance differences
            gray_diff = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
            _, thresh = cv2.threshold(gray_diff, 30, 255, cv2.THRESH_BINARY)
            
            # Create highlighted difference image
            highlighted = arr2.copy()
            highlighted[thresh > 0] = [255, 0, 0]  # Highlight differences in red
            
            # Convert back to PIL Image
            diff_image = Image.fromarray(highlighted)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(diff_image)
            
            # Display
            label = tk.Label(container, image=photo)
            label.image = photo  # Keep a reference
            label.pack()
            
        except Exception as e:
            # Fallback to simple overlay
            ttk.Label(container, text=f"Difference view unavailable: {str(e)}").pack()
            self._display_overlay(image1, image2, zoom)
    
    def _display_slider(self, image1, image2, zoom):
        """Display images with interactive slider"""
        # Create container
        container = ttk.LabelFrame(self.canvas_frame, text="Slider Comparison", padding=10)
        container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # For now, show side by side with a note about slider
        ttk.Label(
            container, 
            text="🎚️ Slider view - Use the controls above to switch between images",
            font=("Arial", 12)
        ).pack(pady=10)
        
        # Show side by side for now
        self._display_side_by_side(image1, image2, zoom)
    
    def _resize_image_for_display(self, image, max_size):
        """Resize image for display while maintaining aspect ratio"""
        original_size = image.size
        ratio = min(max_size[0] / original_size[0], max_size[1] / original_size[1])
        
        if ratio < 1:
            new_size = (int(original_size[0] * ratio), int(original_size[1] * ratio))
            return image.resize(new_size, Image.Resampling.LANCZOS)
        else:
            return image

    def browse_screenshots(self):
        """Browse and load existing screenshots for comparison"""
        from tkinter import filedialog
        
        # Ask user to select two image files
        screenshot1 = filedialog.askopenfilename(
            title="Select Reference Screenshot",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif"), ("All files", "*.*")]
        )
        
        if not screenshot1:
            return
            
        screenshot2 = filedialog.askopenfilename(
            title="Select Test Screenshot",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif"), ("All files", "*.*")]
        )
        
        if not screenshot2:
            return
        
        # Set the image paths
        self.image1_path = screenshot1
        self.image2_path = screenshot2
        
        # Update the image comparison display
        self.display_image_comparison()
        
        # Update progress
        self.progress_var.set(f"Loaded screenshots: {os.path.basename(screenshot1)} vs {os.path.basename(screenshot2)}")
        
        # Show success message
        messagebox.showinfo(
            "Screenshots Loaded", 
            f"Successfully loaded:\n• Reference: {os.path.basename(screenshot1)}\n• Test: {os.path.basename(screenshot2)}\n\nSwitch to the Image Comparison tab to view them."
        )

    def save_current_view(self):
        """Save the current image comparison view to a file"""
        try:
            if not (hasattr(self, 'image1_path') and self.image1_path and 
                    hasattr(self, 'image2_path') and self.image2_path):
                messagebox.showwarning("No Images", "No images are currently loaded for comparison!")
                return
            
            # Ask user where to save
            from tkinter import filedialog
            save_path = filedialog.asksaveasfilename(
                title="Save Current Image View",
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")],
                initialname=f"image_comparison_view_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            )
            
            if not save_path:
                return
            
            # Get current view settings
            view_mode = self.view_mode_var.get()
            zoom = self.zoom_var.get()
            
            # Load images
            image1 = Image.open(self.image1_path)
            image2 = Image.open(self.image2_path)
            
            # Create the comparison image based on current view mode
            if view_mode == "side_by_side":
                # Resize images for side-by-side comparison
                max_display_size = (600, 800)
                display_size = (
                    int(max_display_size[0] * zoom),
                    int(max_display_size[1] * zoom)
                )
                
                img1_resized = self._resize_image_for_display(image1, display_size)
                img2_resized = self._resize_image_for_display(image2, display_size)
                
                # Create side-by-side image
                total_width = img1_resized.width + img2_resized.width + 10  # 10px gap
                max_height = max(img1_resized.height, img2_resized.height)
                
                combined_image = Image.new('RGB', (total_width, max_height), 'white')
                combined_image.paste(img1_resized, (0, 0))
                combined_image.paste(img2_resized, (img1_resized.width + 10, 0))
                
                # Save the combined image
                combined_image.save(save_path)
                
            elif view_mode == "overlay":
                # Create overlay image
                max_display_size = (800, 1000)
                display_size = (
                    int(max_display_size[0] * zoom),
                    int(max_display_size[1] * zoom)
                )
                
                img1_resized = self._resize_image_for_display(image1, display_size)
                img2_resized = self._resize_image_for_display(image2, display_size)
                
                # Make sure both images are the same size
                final_size = (
                    min(img1_resized.size[0], img2_resized.size[0]),
                    min(img1_resized.size[1], img2_resized.size[1])
                )
                
                img1_resized = img1_resized.resize(final_size, Image.Resampling.LANCZOS)
                img2_resized = img2_resized.resize(final_size, Image.Resampling.LANCZOS)
                
                # Create overlay with 50% transparency
                overlay = Image.blend(img1_resized.convert('RGBA'), img2_resized.convert('RGBA'), 0.5)
                overlay.save(save_path)
                
            elif view_mode == "difference":
                # Create difference highlighting image
                max_display_size = (800, 1000)
                display_size = (
                    int(max_display_size[0] * zoom),
                    int(max_display_size[1] * zoom)
                )
                
                img1_resized = self._resize_image_for_display(image1, display_size)
                img2_resized = self._resize_image_for_display(image2, display_size)
                
                # Make sure both images are the same size
                final_size = (
                    min(img1_resized.size[0], img2_resized.size[0]),
                    min(img1_resized.size[1], img2_resized.size[1])
                )
                
                img1_resized = img1_resized.resize(final_size, Image.Resampling.LANCZOS)
                img2_resized = img2_resized.resize(final_size, Image.Resampling.LANCZOS)
                
                # Convert to numpy arrays and calculate difference
                arr1 = np.array(img1_resized)
                arr2 = np.array(img2_resized)
                
                # Calculate difference
                diff = cv2.absdiff(arr1, arr2)
                
                # Enhance differences
                gray_diff = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
                _, thresh = cv2.threshold(gray_diff, 30, 255, cv2.THRESH_BINARY)
                
                # Create highlighted difference image
                highlighted = arr2.copy()
                highlighted[thresh > 0] = [255, 0, 0]  # Highlight differences in red
                
                # Convert back to PIL Image and save
                diff_image = Image.fromarray(highlighted)
                diff_image.save(save_path)
                
            else:  # slider or default
                # For slider mode, save side-by-side as default
                max_display_size = (600, 800)
                display_size = (
                    int(max_display_size[0] * zoom),
                    int(max_display_size[1] * zoom)
                )
                
                img1_resized = self._resize_image_for_display(image1, display_size)
                img2_resized = self._resize_image_for_display(image2, display_size)
                
                # Create side-by-side image
                total_width = img1_resized.width + img2_resized.width + 10
                max_height = max(img1_resized.height, img2_resized.height)
                
                combined_image = Image.new('RGB', (total_width, max_height), 'white')
                combined_image.paste(img1_resized, (0, 0))
                combined_image.paste(img2_resized, (img1_resized.width + 10, 0))
                
                combined_image.save(save_path)
            
            # Show success message
            file_size = os.path.getsize(save_path)
            file_size_mb = file_size / (1024 * 1024)
            
            messagebox.showinfo(
                "View Saved Successfully", 
                f"Current image comparison view saved successfully!\n\n"
                f"📁 File: {os.path.basename(save_path)}\n"
                f"📏 Size: {file_size_mb:.2f} MB\n"
                f"🎨 View Mode: {view_mode.replace('_', ' ').title()}\n"
                f"🔍 Zoom: {int(zoom * 100)}%\n\n"
                f"Location: {save_path}"
            )
            
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save current view: {str(e)}")

    def refresh_wcag_display(self):
        """Refresh WCAG display from the last analysis results"""
        print("DEBUG: Refresh WCAG display called")
        
        # Show immediate feedback to user
        self.wcag_text.config(state="normal")
        self.wcag_text.delete(1.0, tk.END)
        self.wcag_text.insert(tk.END, "🔄 Refreshing WCAG results...\n")
        self.wcag_text.config(state="disabled")
        self.wcag_text.update_idletasks()
        
        # Clear previous scores display
        for widget in self.wcag_scores_frame.winfo_children():
            widget.destroy()
        self.wcag_scores_frame.update_idletasks()
        
        if hasattr(self, 'last_results') and self.last_results:
            wcag_analysis = self.last_results.get('wcag_analysis')
            if wcag_analysis:
                print("DEBUG: Refreshing WCAG display from last results...")
                self.update_wcag_display(wcag_analysis)
                
                # Show success message
                self.wcag_text.config(state="normal")
                current_content = self.wcag_text.get(1.0, tk.END)
                if "🔄 Refreshing WCAG results..." in current_content:
                    # Remove loading message and show timestamp
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    self.wcag_text.delete(1.0, "2.0")
                    self.wcag_text.insert(1.0, f"✅ WCAG results refreshed at {timestamp}\n\n")
                self.wcag_text.config(state="disabled")
                return
            else:
                print("DEBUG: No WCAG analysis found in last results, trying to load from latest report...")
        else:
            print("DEBUG: No last results available, trying to load from latest report...")
        
        # Try to load from the latest report file
        try:
            import glob
            reports = glob.glob('reports/visual_regression_report_*.json')
            if reports:
                latest_report = max(reports, key=os.path.getmtime)
                print(f"DEBUG: Loading WCAG data from {os.path.basename(latest_report)}")
                
                with open(latest_report, 'r') as f:
                    report_data = json.load(f)
                
                # Extract WCAG data
                wcag_data = report_data.get('analysis_results', {}).get('wcag_analysis', {})
                
                if wcag_data:
                    print("DEBUG: Found WCAG data in report file, updating display...")
                    self.update_wcag_display(wcag_data)
                    
                    # Show success message with file info
                    self.wcag_text.config(state="normal")
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    file_date = os.path.basename(latest_report).split('_')[3:6]
                    file_time = f"{file_date[2][:2]}:{file_date[2][2:4]}:{file_date[2][4:6]}" if len(file_date) > 2 else "unknown"
                    current_content = self.wcag_text.get(1.0, tk.END)
                    if "🔄 Refreshing WCAG results..." in current_content:
                        self.wcag_text.delete(1.0, "2.0")
                        self.wcag_text.insert(1.0, f"✅ WCAG results loaded from report (analysis time: {file_time}) - refreshed at {timestamp}\n\n")
                    self.wcag_text.config(state="disabled")
                    return
                else:
                    print("DEBUG: No WCAG data found in report file")
            else:
                print("DEBUG: No report files found")
        except Exception as e:
            print(f"DEBUG: Error loading from report file: {e}")
        
        # Clear the display and show helpful message
        for widget in self.wcag_scores_frame.winfo_children():
            widget.destroy()
        self.wcag_scores_frame.update_idletasks()
        
        self.wcag_text.config(state="normal")
        self.wcag_text.delete(1.0, tk.END)
        self.wcag_text.insert(tk.END, "❌ No WCAG analysis data available to refresh.\n\n")
        self.wcag_text.insert(tk.END, "💡 To see WCAG compliance results:\n")
        self.wcag_text.insert(tk.END, "1. Ensure 'WCAG Testing' checkbox is checked ✓\n")
        self.wcag_text.insert(tk.END, "2. Enter valid URLs for analysis 🌐\n")
        self.wcag_text.insert(tk.END, "3. Run a new analysis ▶️\n")
        self.wcag_text.insert(tk.END, "4. Wait for analysis to complete ⏳\n")
        self.wcag_text.insert(tk.END, "5. Results will appear automatically ✨\n\n")
        self.wcag_text.insert(tk.END, f"🕒 Refresh attempted at: {datetime.now().strftime('%H:%M:%S')}\n")
        self.wcag_text.config(state="disabled")

if __name__ == "__main__":
    # Create the main window
    root = tk.Tk()
    
    # Set window icon if available
    try:
        root.iconbitmap(default='icon.ico')
    except:
        pass  # Icon file not found, continue without it
    
    # Ensure the window appears on top initially
    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(root.attributes, '-topmost', False)
    
    # Create and run the application
    app = VisualRegressionGUI(root)
    
    # Center the window on screen after maximizing (in case maximization fails)
    root.update_idletasks()
    
    print("🚀 Visual AI Regression Testing Module started in maximized mode!")
    print("📱 GUI is ready for visual regression testing and WCAG compliance analysis.")
    
    # Start the GUI event loop
    root.mainloop()
