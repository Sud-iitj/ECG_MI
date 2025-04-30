
import streamlit as st
import tempfile
from ecg_utils import process_ecg_image, generate_pdf_report
import cv2
from PIL import Image

st.set_page_config(page_title="ECG MI Detector", layout="centered")

st.title("📈 ECG Myocardial Infarction Detection")
st.write("Upload an ECG graph image to detect if it shows signs of Myocardial Infarction.")

uploaded_file = st.file_uploader("Upload ECG Image (PNG/JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_file_path = tmp_file.name

    st.image(uploaded_file, caption="Uploaded ECG Image", use_column_width=True)

    report, processed_img = process_ecg_image(tmp_file_path)

    st.subheader("🩺 Diagnosis")
    st.markdown(f"**Result:** {report['Diagnosis']}")
    st.markdown("### 📄 Detailed Report")
    st.json(report)

    if st.button("Generate PDF Report"):
        generate_pdf_report(report)
        with open("ECG_Report.pdf", "rb") as f:
            st.download_button("📥 Download Report", f, file_name="ECG_Report.pdf")
