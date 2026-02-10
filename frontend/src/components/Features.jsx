function Features({ features }) {
  // If backend sends nothing or Amazon blocks features
  if (!features || !Array.isArray(features) || features.length === 0) {
    return (
      <div className="card">
        <h3>📋 Product Description</h3>
        <p style={{ color: "#64748b", lineHeight: "1.6" }}>
          Product description is currently unavailable.
          <br />
          Amazon sometimes limits content on first request.
          <br />
          <b>Try again after a few seconds.</b>
        </p>
      </div>
    );
  }

  // Remove duplicates & "Not found"
  const cleanFeatures = [...new Set(features)].filter(
    (f) => f && f !== "Not found"
  );

  return (
    <div className="card">
      <h3>📋 Product Description</h3>

      <ul className="features">
        {cleanFeatures.map((feature, index) => (
          <li key={index}>{feature}</li>
        ))}
      </ul>
    </div>
  );
}

export default Features;
