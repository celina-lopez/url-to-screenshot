import os
import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import mistune
from dotenv import load_dotenv
from services import screenshot

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("img/favicon.ico")
async def favicon(): return FileResponse('./static/favicon.ico')

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def index(request: Request):
  return templates.TemplateResponse("home/index.html", {
        "request": request,
    })

@app.get('/api/{url}')
async def api(url):
    report = await screenshot.get_image_async(url)

    return report


if __name__ == "__main__":
    load_dotenv()
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', "8000")))
