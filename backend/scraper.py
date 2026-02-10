import requests
import re
import time
from bs4 import BeautifulSoup

# ---------------- HEADERS ----------------
AMAZON_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0 Safari/537.36"
    ),
    "Accept-Language": "en-IN,en;q=0.9",
}

BUYHATKE_API = "https://buyhatke.com/api/productData"


# ---------------- HELPERS ----------------
def clean(text):
    if not text:
        return "Not found"
    return re.sub(r"\s+", " ", text).strip()


def blocked(html):
    h = html.lower()
    return "captcha" in h or "robot check" in h or "enter the characters" in h


# ---------------- AMAZON SCRAPER (WITH RETRY) ----------------
def scrape_amazon(url, retries=1):
    try:
        r = requests.get(url, headers=AMAZON_HEADERS, timeout=15)
    except Exception:
        return scrape_amazon(url, retries - 1) if retries > 0 else {}

    if r.status_code != 200 or blocked(r.text):
        if retries > 0:
            time.sleep(2)
            return scrape_amazon(url, retries - 1)
        return {}

    soup = BeautifulSoup(r.text, "lxml")
    data = {}

    # ---------- BASIC ----------
    title = soup.select_one("#productTitle")
    data["name"] = clean(title.text if title else None)

    brand = soup.select_one("#bylineInfo")
    data["brand"] = clean(
        brand.text.replace("Visit the", "").replace("Store", "")
        if brand else None
    )

    # ---------- PRICE ----------
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

    # ---------- META ----------
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

    # ---------- ASIN ----------
    asin = soup.find("input", {"id": "ASIN"})
    data["asin"] = asin.get("value") if asin else None

    # ---------- DESCRIPTION ----------
    features = []
    for li in soup.select("#feature-bullets li span"):
        txt = clean(li.text)
        if txt != "Not found":
            features.append(txt)

    data["features"] = list(dict.fromkeys(features))  # remove duplicates

    # ---------- RETRY CONDITIONS ----------
    critical_missing = (
        data["name"] == "Not found"
        or data["price"] == "Not found"
        or not data["features"]
    )

    if critical_missing and retries > 0:
        time.sleep(2)  # human-like delay
        return scrape_amazon(url, retries - 1)

    return data


# ---------------- BUYHATKE PRICE DATA ----------------
def fetch_buyhatke_data(asin):
    if not asin:
        return {}

    r = requests.get(
        BUYHATKE_API,
        params={"pos": 63, "pid": asin},
        timeout=15
    )

    raw = r.json().get("data", {})

    timeline = []

    for key, price in raw.items():
        if not isinstance(price, (int, float)):
            continue
        if price <= 0 or price > 200000:
            continue

        m = re.match(r"(20\d{2})_(\d{1,2})", key)
        if m:
            timeline.append({
                "date": f"{m.group(1)}-{int(m.group(2)):02d}",
                "price": price
            })

    return {
        "highest": raw.get("maxall"),
        "lowest": raw.get("min"),
        "average": round(raw.get("yearavg", 0), 2),
        "timeline": sorted(timeline, key=lambda x: x["date"]),
        "images": list(set(raw.get("thumbnailImages", [])))
    }
