function ImageGallery({ images }) {
  if (!images || images.length === 0) return null;

  return (
    <div className="image-grid card">
      {images.map((img, i) => (
        <img key={i} src={img} alt="" />
      ))}
    </div>
  );
}

export default ImageGallery;
