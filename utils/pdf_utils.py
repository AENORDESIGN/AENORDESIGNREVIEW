
from fpdf import FPDF
from datetime import datetime

def generate_pdf(content):
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('ArialUnicode', '', '/usr/share/fonts/truetype/nanum/NanumGothic.ttf', uni=True)
    pdf.set_font("ArialUnicode", size=12)
    for line in content.split("\n"):
        pdf.cell(200, 10, txt=line, ln=True)
    filename = f"/mnt/data/심의분석결과_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(filename)
    return filename
