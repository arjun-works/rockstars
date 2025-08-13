import streamlit as st
import os
import uuid
from visual_ai_regression import VisualAIRegression
from werkzeug.utils import secure_filename
from datetime import datetime
import base64
import zipfile
from io import BytesIO

# Streamlit Cloud only allows writing to /tmp or ./
UPLOAD_FOLDER = 'uploads'
RESULTS_FOLDER = 'results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

st.set_page_config(page_title="Visual AI Regression", layout="wide")
st.title("Visual AI Regression Testing (Streamlit)")
st.markdown("Upload a baseline and current image to compare. Configure analysis options and view/download results.")

# --- File Upload ---
col1, col2 = st.columns(2)
with col1:
    baseline_file = st.file_uploader("Baseline Image", type=["png", "jpg", "jpeg", "gif", "bmp"], key="baseline")
with col2:
    current_file = st.file_uploader("Current Image", type=["png", "jpg", "jpeg", "gif", "bmp"], key="current")

# --- Analysis Options ---
st.sidebar.header("Analysis Settings")
sensitivity = st.sidebar.slider("Sensitivity", 0.1, 1.0, 0.8, 0.05)
analysis_type = st.sidebar.selectbox("Analysis Type", ["comprehensive", "quick", "detailed"])
detect_layout_shifts = st.sidebar.checkbox("Detect Layout Shifts", value=True)
detect_color_changes = st.sidebar.checkbox("Detect Color Changes", value=True)
detect_text_changes = st.sidebar.checkbox("Detect Text Changes", value=True)

if baseline_file and current_file:
    # Save uploaded files
    session_id = str(uuid.uuid4())
    session_dir = os.path.join(UPLOAD_FOLDER, session_id)
    os.makedirs(session_dir, exist_ok=True)
    baseline_path = os.path.join(session_dir, 'baseline_' + secure_filename(baseline_file.name))
    current_path = os.path.join(session_dir, 'current_' + secure_filename(current_file.name))
    with open(baseline_path, 'wb') as f:
        f.write(baseline_file.read())
    with open(current_path, 'wb') as f:
        f.write(current_file.read())

    st.success("Files uploaded successfully!")
    st.image([baseline_path, current_path], caption=["Baseline", "Current"], width=300)

    if st.button("Start Analysis"):
        with st.spinner("Running visual regression analysis..."):
            config = {
                'baseline_image': baseline_path,
                'current_image': current_path,
                'sensitivity': sensitivity,
                'analysis_type': analysis_type,
                'detect_layout_shifts': detect_layout_shifts,
                'detect_color_changes': detect_color_changes,
                'detect_text_changes': detect_text_changes,
                'generate_report': True,
                'output_dir': os.path.join(RESULTS_FOLDER, session_id)
            }
            os.makedirs(config['output_dir'], exist_ok=True)
            regression_module = VisualAIRegression()
            try:
                results = regression_module.run_image_analysis(config)
                st.success("Analysis completed!")
                # Show metrics
                st.subheader("Results")
                st.write(f"**Similarity Score:** {results.get('similarity_score', 0)*100:.1f}%")
                st.write(f"**Differences Found:** {results.get('differences_count', 0)}")
                st.write(f"**Analysis Time:** {results.get('analysis_duration', 0):.2f} seconds")
                # Show difference image
                if results.get('difference_image_path') and os.path.exists(results['difference_image_path']):
                    st.image(results['difference_image_path'], caption="Difference Visualization", use_column_width=True)
                # Download report as zip
                report_dir = config['output_dir']
                memory_file = BytesIO()
                with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
                    for root, dirs, files in os.walk(report_dir):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arc_path = os.path.relpath(file_path, report_dir)
                            zf.write(file_path, arc_path)
                memory_file.seek(0)
                st.download_button(
                    label="Download Full Report (ZIP)",
                    data=memory_file,
                    file_name=f"visual_regression_results_{session_id}.zip",
                    mime="application/zip"
                )
            except Exception as e:
                st.error(f"Analysis failed: {e}")
else:
    st.info("Please upload both baseline and current images to begin.")
