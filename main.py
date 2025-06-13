from fastapi import FastAPI
from fastapi.responses import FileResponse
from langgraph_app.graph import run_langgraph
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = FastAPI()

def save_report_as_pdf(text: str, file_path: str = "report.pdf"):
    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter
    margin = 40
    y = height - margin
    lines = text.split('\n')

    for line in lines:
        if y < margin:
            c.showPage()
            y = height - margin
        c.drawString(margin, y, line.strip())
        y -= 15  # Line spacing

    c.save()

@app.get("/generate-report")
def generate():
    result = run_langgraph()
    return {"report": result["report"]}

@app.get("/download-report")
def download_report():
    result = run_langgraph()
    save_report_as_pdf(result["report"])
    return FileResponse("report.pdf", media_type="application/pdf", filename="cross_sell_report.pdf")
