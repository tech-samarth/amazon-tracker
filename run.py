import requests
from bs4 import BeautifulSoup
import re
import sys

# ---------------- HEADERS ----------------
AMAZON_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-IN,en;q=0.9"
}

BUYHATKE_HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "*/*"
}

BUYHATKE_API = "https://buyhatke.com/api/productData"

# ---------------- HELPERS ----------------
def clean(text):
    if not text:
        return ""
    return re.sub(r"\s+", " ", text).strip()

def blocked(html):
    return "captcha" in html.lower() or "robot check" in html.lower()

# ---------------- AMAZON SCRAPER ----------------
def scrape_amazon(url):
    r = requests.get(url, headers=AMAZON_HEADERS, timeout=15)

    if r.status_code != 200:
        print("❌ Failed to load Amazon page")
        sys.exit(1)

    if blocked(r.text):
        print("⚠️ Amazon blocked the request (CAPTCHA)")
        sys.exit(1)

    soup = BeautifulSoup(r.text, "lxml")
    data = {}

    data["Product Name"] = clean(
        soup.select_one("#productTitle").text
    ) if soup.select_one("#productTitle") else "Not found"

    brand = soup.select_one("#bylineInfo")
    data["Brand"] = clean(
        brand.text.replace("Visit the", "").replace("Store", "")
    ) if brand else "Not found"

    whole = soup.select_one("span.a-price-whole")
    fraction = soup.select_one("span.a-price-fraction")
    data["Price"] = (
        "₹" + clean(whole.text) + ("." + clean(fraction.text) if fraction else "")
        if whole else "Not found"
    )

    mrp = soup.select_one("span.a-text-price span.a-offscreen")
    data["Mrp"] = clean(mrp.text) if mrp else "Not found"

    discount = soup.select_one("span.savingsPercentage")
    data["Discount"] = clean(discount.text) if discount else "Not found"

    availability = soup.select_one("#availability span")
    data["Availability"] = clean(availability.text) if availability else "Not found"

    rating = soup.select_one("span.a-icon-alt")
    data["Rating"] = clean(rating.text) if rating else "Not found"

    reviews = soup.select_one("#acrCustomerReviewText")
    data["Reviews"] = clean(reviews.text) if reviews else "Not found"

    asin_tag = soup.find("input", {"id": "ASIN"})
    data["Asin"] = asin_tag.get("value") if asin_tag else "Not found"

    categories = [
        clean(c.text)
        for c in soup.select("#wayfinding-breadcrumbs_container span.a-list-item")
        if clean(c.text)
    ]
    data["Category"] = " › ".join(categories) if categories else "Not found"

    seller = soup.select_one("#sellerProfileTriggerId")
    data["Seller"] = clean(seller.text) if seller else "Not found"

    data["Fulfilled"] = (
        "Fulfilled by Amazon" if soup.select_one("#SSOFpopoverLink") else "Unknown"
    )

    delivery = soup.select_one("#mir-layout-DELIVERY_BLOCK span")
    data["Delivery"] = clean(delivery.text) if delivery else "Not found"

    data["Features"] = [
        clean(li.text)
        for li in soup.select("#feature-bullets li span")
        if clean(li.text)
    ]

    return data

# ---------------- BUYHATKE PRICE + IMAGES ----------------
def fetch_buyhatke_data(asin):
    r = requests.get(
        BUYHATKE_API,
        headers=BUYHATKE_HEADERS,
        params={"pos": 63, "pid": asin},
        timeout=15
    )

    raw = r.json()["data"]

    # ---- PRICE TIMELINE ----
    timeline = {}

    for key, price in raw.items():
        if not isinstance(price, (int, float)):
            continue
        if price <= 0 or price > 200000:
            continue

        # YYYY_M (preferred)
        m = re.fullmatch(r"(20\d{2})_(\d{1,2})", key)
        if m:
            y, mo = m.groups()
            timeline[f"{y}-{str(int(mo)).zfill(2)}"] = price
            continue

        # YYYYm_M (fallback)
        m = re.fullmatch(r"(20\d{2})m_(\d{1,2})", key)
        if m:
            y, mo = m.groups()
            date = f"{y}-{str(int(mo)).zfill(2)}"
            if date not in timeline:
                timeline[date] = price

    # ---- BUYHATKE IMAGES ONLY ----
    images = set()

    if isinstance(raw.get("image"), str):
        images.add(raw["image"])

    if isinstance(raw.get("thumbnailImages"), list):
        for img in raw["thumbnailImages"]:
            if isinstance(img, str):
                images.add(img)

    return {
        "highest": raw.get("maxall"),
        "lowest": raw.get("min"),
        "average": round(raw.get("yearavg", 0), 2),
        "timeline": sorted(timeline.items()),
        "images": list(images)
    }

# ---------------- MAIN ----------------
if __name__ == "__main__":
    print("\n🔗 Enter Amazon product URL:")
    url = input(">> ").strip()

    product = scrape_amazon(url)

    print("\n================ AMAZON PRODUCT DATA ================\n")
    for k, v in product.items():
        if isinstance(v, list):
            continue
        print(f"{k:18}: {v}")

    print("\n✨ Key Features:")
    for i, f in enumerate(product["Features"], 1):
        print(f"  {i}. {f}")

    if product["Asin"] != "Not found":
        bh = fetch_buyhatke_data(product["Asin"])

        print("\n📈 PRICE HISTORY (BuyHatke)")
        print("⬆ Highest Price :", bh["highest"])
        print("⬇ Lowest Price  :", bh["lowest"])
        print("📊 Avg (1 Year) :", bh["average"])

        print("\n📉 Price Timeline:")
        for i, (date, price) in enumerate(bh["timeline"], 1):
            print(f"  {i}. {date} : ₹{price}")

        print("\n🖼 BuyHatke Images:")
        for i, img in enumerate(bh["images"], 1):
            print(f"  {i}. {img}")

    print("\n=====================================================\n")
