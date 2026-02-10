import axios from "axios";

export const fetchProduct = async (url) => {
  const res = await axios.get("http://localhost:8000/track", {
    params: { url }
  });
  return res.data;
};
