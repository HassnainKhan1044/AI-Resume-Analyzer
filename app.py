import os

from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pdf_reader import extract_text
from ai import analyze_resume

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )


@app.post("/upload")
async def upload_resume(
    request: Request,
    file: UploadFile = File(...),
    job_description: str = Form("")
):

    os.makedirs("uploads", exist_ok=True)

    file_path = os.path.join("uploads", file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    resume_text = extract_text(file_path)

    analysis = analyze_resume(
        resume_text,
        job_description
    )

    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "request": request,
            "analysis": analysis
        }
    )