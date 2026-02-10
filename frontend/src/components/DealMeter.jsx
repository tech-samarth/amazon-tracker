function DealMeter({ history, currentPrice }) {
  if (!history || !currentPrice) return null;

  const { highest, average } = history;

  // Decide deal type
  let label = "🙂 Good Deal";
  let zone = "yellow";

  if (currentPrice > highest) {
    label = "❌ Overpriced";
    zone = "red";
  } else if (currentPrice < average) {
    label = "🔥 Best Deal";
    zone = "green";
  }

  /*
    Needle angle:
    -90deg (far left)  → worst
     0deg (center)
    +90deg (far right) → best
  */
  let ratio;
  if (currentPrice > highest) {
    ratio = 0;
  } else if (currentPrice < average) {
    ratio = 1;
  } else {
    ratio = 1 - (currentPrice - average) / (highest - average);
  }

  const angle = -90 + ratio * 180;

  return (
    <div className="card">
      <h3>💡 Deal Meter</h3>

      <div className="meter-wrapper">
        <div className="meter-arc red"></div>
        <div className="meter-arc yellow"></div>
        <div className="meter-arc green"></div>

        <div
          className="meter-needle"
          style={{ transform: `rotate(${angle}deg)` }}
        />

        <div className="meter-center"></div>
      </div>

      <div className={`deal-label ${zone}`}>
        {label}
      </div>

      <div className="deal-info">
        <span>Current: ₹{currentPrice}</span>
        <span>Average: ₹{average}</span>
        <span>Highest: ₹{highest}</span>
      </div>
    </div>
  );
}

export default DealMeter;
