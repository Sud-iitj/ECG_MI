
import cv2
import numpy as np
from fpdf import FPDF

def process_ecg_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 180, 255, cv2.THRESH_BINARY_INV)

    # Simulate extracting Lead II (middle section)
    h, w = thresh.shape
    lead_ii = thresh[h//3:2*h//3, :]

    vertical_sum = np.sum(lead_ii, axis=0)
    threshold = np.max(vertical_sum) * 0.6
    qrs_locs = np.where(vertical_sum > threshold)[0]
    num_qrs = len(qrs_locs)
    heart_rate = int((num_qrs / 10) * 60)  # assuming 10s

    # Simulated features (replace with true values if you implement peak detection)
    st_segment_status = "Depression"  # simulate MI
    diagnosis = "Myocardial Infarction" if "depression" in st_segment_status.lower() else "Normal"

    report = {
        "Heart Rate": f"{heart_rate} BPM",
        "RR Interval": "0.78 sec",
        "Heart Rhythm": "Regular",
        "Cardiac Axis": "Normal Axis",
        "ST Segment": st_segment_status,
        "Diagnosis": diagnosis
    }

    return report, img

def generate_pdf_report(report_dict, output_path="ECG_Report.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="ECG Analysis Report", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", size=10)
    for key, value in report_dict.items():
        pdf.cell(80, 10, txt=f"{key}", border=1)
        pdf.cell(100, 10, txt=f"{value}", border=1)
        pdf.ln()

    pdf.output(output_path)
