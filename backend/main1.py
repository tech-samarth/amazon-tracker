from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scraper import scrape_amazon, buyhatke

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/track")
def track(url: str):
    product = scrape_amazon(url)
    history = buyhatke(product["asin"])
    return {
        "product": product,
        "history": history
    }
