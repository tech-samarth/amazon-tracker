import requests, re
from bs4 import BeautifulSoup

AMAZON_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0 Safari/537.36"
    ),
    "Accept-Language": "en-IN,en;q=0.9"
}

BUYHATKE_API = "https://buyhatke.com/api/productData"


def clean(t):
    return re.sub(r"\s+", " ", t).strip() if t else "Not found"


def scrape_amazon(url):
    r = requests.get(url, headers=AMAZON_HEADERS, timeout=15)
    soup = BeautifulSoup(r.text, "lxml")

    data = {}

    # BASIC
    data["name"] = clean(
        soup.select_one("#productTitle").text
        if soup.select_one("#productTitle") else None
    )

    brand = soup.select_one("#bylineInfo")
    data["brand"] = clean(
        brand.text.replace("Visit the", "").replace("Store", "")
        if brand else None
    )

    # PRICE
    whole = soup.select_one("span.a-price-whole")
    frac = soup.select_one("span.a-price-fraction")
    data["price"] = (
        f"₹{clean(whole.text)}.{clean(frac.text)}"
        if whole else "Not found"
    )

    mrp = soup.select_one("span.a-text-price span.a-offscreen")
    data["mrp"] = clean(mrp.text if mrp else None)

    discount = soup.select_one("span.savingsPercentage")
    data["discount"] = clean(discount.text if discount else None)

    # META
    availability = soup.select_one("#availability span")
    data["availability"] = clean(availability.text if availability else None)

    rating = soup.select_one("span.a-icon-alt")
    data["rating"] = clean(rating.text if rating else None)

    reviews = soup.select_one("#acrCustomerReviewText")
    data["reviews"] = clean(reviews.text if reviews else None)

    seller = soup.select_one("#sellerProfileTriggerId")
    data["seller"] = clean(seller.text if seller else None)

    data["fulfilled"] = (
        "Fulfilled by Amazon"
        if soup.select_one("#SSOFpopoverLink")
        else "Unknown"
    )

    delivery = soup.select_one("#mir-layout-DELIVERY_BLOCK span")
    data["delivery"] = clean(delivery.text if delivery else None)

    # ASIN
    asin = soup.find("input", {"id": "ASIN"})
    data["asin"] = asin.get("value") if asin else None

    # DESCRIPTION / FEATURES
    data["features"] = [
        clean(li.text)
        for li in soup.select("#feature-bullets li span")
        if clean(li.text) != "Not found"
    ]

    return data


def buyhatke(asin):
    r = requests.get(
        BUYHATKE_API,
        params={"pos": 63, "pid": asin},
        timeout=15
    ).json()["data"]

    timeline = []

    for k, v in r.items():
        if isinstance(v, (int, float)) and 0 < v < 200000:
            m = re.match(r"(20\d{2})_(\d{1,2})", k)
            if m:
                timeline.append({
                    "date": f"{m.group(1)}-{int(m.group(2)):02d}",
                    "price": v
                })

    return {
        "highest": r.get("maxall"),
        "lowest": r.get("min"),
        "average": round(r.get("yearavg", 0), 2),
        "timeline": sorted(timeline, key=lambda x: x["date"]),
        "images": list(set(r.get("thumbnailImages", [])))
    }
