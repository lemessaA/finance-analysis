import requests
import json
import time
from reportlab.pdfgen import canvas
import sys

def create_pdf(filename, text_lines):
    c = canvas.Canvas(filename)
    text = c.beginText(50, 800)
    text.textLines(text_lines)
    c.drawText(text)
    c.save()

# 1. Create PDFs
r1_text = """Apple Inc. 2024 Annual Report
Revenue: $394.3 billion
Revenue Growth: 8% 
Gross Margin: 43.3%
EBITDA: 130 billion
EBITDA Margin: 33%
Net Profit: $99.8 billion
Net Margin: 25.3%
Operating Income: 119.4 billion
Total Assets: 352.8 billion
Total Liabilities: 302.1 billion
Cash Flow: $122.2 billion
EPS: $6.15
Current Ratio: 0.88
Debt to Equity: 1.9

Highlights:
- Record services revenue
- Strong iPhone sales
- Decreased operating expenses
- Increased dividend

Risks:
- Supply chain constraints
- Regulatory scrutiny
"""

r2_text = """Microsoft 2024 Annual Report
Revenue: $211.9 billion
Revenue Growth YoY: 11%
Gross Margin: 68.9%
EBITDA: $102 billion
EBITDA margin: 48%
Net Profit: $72.4B
Net Margin: 34%
Operating Income: 89 billion
Total Assets: 412 billion
Total Liabilities: 205 billion
Cash flow: $87.6B
EPS: $9.68
Current Ratio: 1.77
Debt to Equity: 0.58

Highlights:
- Azure growth accelerated
- AI integrations drove sales
- Record gaming revenue

Risks:
- Macroeconomic slowdown
- Competition in AI
"""

try:
    create_pdf("/tmp/r1.pdf", r1_text)
    create_pdf("/tmp/r2.pdf", r2_text)
except Exception as e:
    print(f"Error creating PDFs: {e}")
    sys.exit(1)

# 2. Analyze PDF 1
url = "http://localhost:8000/analyze"
try:
    print("Analyzing Apple PDF...")
    with open("/tmp/r1.pdf", "rb") as f:
        res1 = requests.post(url, files={"file": ("r1.pdf", f, "application/pdf")})
    res1.raise_for_status()
    r1_data = res1.json()
    id1 = r1_data.get("filename") # Used as ID
    print(f"Apple analysis success: ID {id1}")
except Exception as e:
    print(f"Failed to analyze Apple PDF: {e}")
    if 'res1' in locals():
        print(res1.text)
    sys.exit(1)

# 3. Analyze PDF 2
try:
    print("Analyzing Microsoft PDF...")
    with open("/tmp/r2.pdf", "rb") as f:
        res2 = requests.post(url, files={"file": ("r2.pdf", f, "application/pdf")})
    res2.raise_for_status()
    r2_data = res2.json()
    id2 = r2_data.get("filename")
    print(f"Microsoft analysis success: ID {id2}")
except Exception as e:
    print(f"Failed to analyze Microsoft PDF: {e}")
    if 'res2' in locals():
        print(res2.text)
    sys.exit(1)

# 4. Compare
compare_url = "http://localhost:8000/compare"
try:
    print(f"Comparing {id1} to {id2}...")
    payload = {"baseline_report_id": id1, "current_report_id": id2}
    compare_res = requests.post(compare_url, json=payload)
    compare_res.raise_for_status()
    print("Comparison Result:")
    print(json.dumps(compare_res.json(), indent=2))
except Exception as e:
    print(f"Failed to compare reports: {e}")
    if 'compare_res' in locals():
         print(compare_res.text)
    sys.exit(1)
print("SUCCESS!")
