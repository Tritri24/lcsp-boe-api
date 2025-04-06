from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import requests
from bs4 import BeautifulSoup

app = FastAPI(title="LCSP BOE Article API")

BOE_LCSP_ID = "BOE-A-2017-12902"
BOE_URL = "https://www.boe.es/buscar/act.php"

@app.get("/lcsp/article")
def get_lcsp_article(article: str = Query(..., description="Número del artículo a consultar")):
    params = {
        "id": BOE_LCSP_ID,
        "articulo": article,
        "modo": "consolidado"
    }

    response = requests.get(BOE_URL, params=params)
    if response.status_code != 200:
        return JSONResponse(status_code=500, content={"error": "Error consultando el BOE."})

    soup = BeautifulSoup(response.text, 'html.parser')
    content_div = soup.find("div", {"class": "texto"})
    if not content_div:
        return JSONResponse(status_code=404, content={"error": "Artículo no encontrado o sin contenido visible."})

    paragraphs = content_div.find_all("p")
    article_text = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))

    return {
        "article": article,
        "text": article_text
    }
