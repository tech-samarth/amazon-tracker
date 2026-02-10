function Stars({ rating }) {
  if (!rating) return null;

  const value = parseFloat(rating);
  const full = Math.floor(value);

  return (
    <div className="stars">
      {[1,2,3,4,5].map(i => (
        <span key={i} className={i <= full ? "star filled" : "star"}>
          ★
        </span>
      ))}
      <span className="rating-text">{rating}</span>
    </div>
  );
}

function ProductHeader({ product }) {
  if (!product) return null;

  return (
    <div className="card">
      <h2 className="product-title">{product.name}</h2>

      {product.brand && product.brand !== "Not found" && (
        <p className="brand">Brand: <strong>{product.brand}</strong></p>
      )}

      <div className="price-row">
        <span className="price">{product.price}</span>

        {product.mrp !== "Not found" && (
          <span className="mrp">{product.mrp}</span>
        )}

        {product.discount && product.discount !== "Not found" && (
          <span className="discount">{product.discount}</span>
        )}
      </div>

      <Stars rating={product.rating} />

      <div className="meta">
        {product.availability !== "Not found" && (
          <span className="badge green">{product.availability}</span>
        )}

        {product.delivery !== "Not found" && (
          <span className="badge">{product.delivery}</span>
        )}
      </div>

      <div className="details-grid">
        {product.seller !== "Not found" && (
          <div><b>Seller</b><span>{product.seller}</span></div>
        )}
        {product.fulfilled !== "Not found" && (
          <div><b>Fulfilled</b><span>{product.fulfilled}</span></div>
        )}
        {product.reviews !== "Not found" && (
          <div><b>Reviews</b><span>{product.reviews}</span></div>
        )}
        {product.asin && (
          <div><b>ASIN</b><span>{product.asin}</span></div>
        )}
      </div>
    </div>
  );
}

export default ProductHeader;
