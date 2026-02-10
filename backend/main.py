from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from scraper import scrape_amazon, fetch_buyhatke_data

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/track")
def track(url: str = Query(..., description="Amazon product URL")):
    product = scrape_amazon(url)

    history = {}
    if product.get("asin"):
        history = fetch_buyhatke_data(product["asin"])

    return {
        "product": product,
        "history": history
    }
