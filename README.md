

# 🛒 Amazon Price Tracker

A modern **full-stack web app** that tracks Amazon product prices, shows historical trends, and visually tells you whether a product is a **Best Deal, Good Deal, or Overpriced**.

Built with **FastAPI (Python)** + **React**.

---

## ✨Features

* 📦 Product details (price, MRP, discount, seller, delivery, reviews)
* 📈 Interactive price history graph
* 🎯 Needle-style deal meter (red → yellow → green)
* ⭐ Visual star ratings
* 🧾 Product description / features
* 🔁 Auto-retry when Amazon returns partial data
* 🎨 Clean landing page + dashboard UI

---

## 🧱 Tech Stack

* **Backend:** Python, FastAPI, BeautifulSoup
* **Frontend:** React, Recharts, CSS

---

## 🚀 Run Locally

### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

Backend → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Frontend

```bash
cd frontend
npm install
npm start
```

Frontend → [http://localhost:3000](http://localhost:3000)

---

## 🧠 Deal Logic

* ❌ Overpriced → price > highest
* 🔥 Best Deal → price < average
* 🙂 Good Deal → between average & highest

---

## ⚠️ Note

Amazon pages are dynamic. The app retries automatically and handles missing data gracefully.

---

## ⭐ Use Cases

* Price tracking
* Deal evaluation
* Full-stack learning project
* Hackathons / portfolio

---

**Built with ❤️ by Samarth**
