import React, { useState } from "react";
import Loader from "./Loader";

function UploadSection({ setClusters }) {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFiles(Array.from(e.target.files));
  };

  const handleUpload = async () => {
    if (!files.length) return alert("Please select images");

    const formData = new FormData();
    files.forEach((file) => formData.append("files", file));

    setLoading(true);

    const res = await fetch("http://127.0.0.1:8000/cluster-images", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    setClusters(data.clusters);
    setLoading(false);

    document.getElementById("results").scrollIntoView({ behavior: "smooth" });
  };

  const clearAll = () => {
    setFiles([]);
    setClusters({});
  };

  return (
    <div className="upload-card">
      <h2>Upload Images</h2>

      <label className="drop-area">
        Drag & Drop Images Here
        <input type="file" multiple onChange={handleChange} hidden />
      </label>

      <p className="file-count">{files.length} files selected</p>

      {loading ? (
        <Loader />
      ) : (
        <div className="button-group">
          <button className="primary-btn" onClick={handleUpload}>
            Upload & Cluster
          </button>
          <button className="danger-btn" onClick={clearAll}>
            Clear All
          </button>
        </div>
      )}
    </div>
  );
}

export default UploadSection;