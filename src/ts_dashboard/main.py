from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .crud import get_price_points  # function returning list of dicts

app = FastAPI()

# mount static files (Plotly.js)
app.mount("/static", StaticFiles(directory="src/ts_dashboard/static"), name="static")
templates = Jinja2Templates(directory="src/ts_dashboard/templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/btc")
async def api_btc():
    # returns [{"date": "2025-06-21", "price": 30875.12}, ...]
    data = get_price_points()
    return JSONResponse(data)
