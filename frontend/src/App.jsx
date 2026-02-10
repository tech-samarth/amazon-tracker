import { useState } from "react";
import { fetchProduct } from "./api";

import ProductHeader from "./components/ProductHeader";
import ImageGallery from "./components/ImageGallery";
import DealMeter from "./components/DealMeter";
import PriceChart from "./components/PriceChart";
import Features from "./components/Features";

function App() {
  const [url, setUrl] = useState("");
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const submit = async () => {
    if (!url) return;
    setLoading(true);
    setError("");
    try {
      const d = await fetchProduct(url);
      setData(d);
    } catch (e) {
      setError("Failed to fetch product. Try again.");
    }
    setLoading(false);
  };

  return (
    <>
      {/* LANDING PAGE */}
      {!data && (
        <div className="landing">
          <div className="hero">
            <h1>Amazon Price Tracker</h1>
            <p>
              Track price history, detect good deals, and decide the best time to
              buy using real data.
            </p>

            <div className="search-box">
              <input
                placeholder="Paste Amazon product URL here"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
              />
              <button onClick={submit}>
                {loading ? "Fetching..." : "Track Price"}
              </button>
            </div>

            {error && <p className="error">{error}</p>}
          </div>
        </div>
      )}

      {/* DASHBOARD */}
      {data && (
        <div className="container">
          <ProductHeader product={data.product} />

          <ImageGallery images={data.history.images} />

          <DealMeter
            history={data.history}
            currentPrice={Number(
              data.product.price?.replace(/[₹,]/g, "")
            )}
          />

          <PriceChart
            timeline={data.history.timeline}
            highest={data.history.highest}
            lowest={data.history.lowest}
            average={data.history.average}
          />

          <Features features={data.product.features} />
        </div>
      )}
    </>
  );
}

export default App;
