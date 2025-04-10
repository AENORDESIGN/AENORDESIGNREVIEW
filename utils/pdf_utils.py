
from fpdf import FPDF
from datetime import datetime

def generate_pdf(content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in content.split("\n"):
        pdf.cell(200, 10, txt=line, ln=True)
    filename = "/mnt/data/심의분석결과_" + datetime.now().strftime('%Y%m%d_%H%M%S') + ".pdf"
    pdf.output(filename)
    return filename
