import React from "react";

function ResultsSection({ clusters }) {
  return (
    <div id="results" className="results-section">
      <h2>Cluster Results</h2>

      {Object.keys(clusters).map((group) => (
        <div key={group} className="cluster-card">
          <h3>Group {group}</h3>
          <div className="image-grid">
            {clusters[group].map((img, index) => (
              <img
                key={index}
                src={`http://127.0.0.1:8000/images/${img}`}
                alt=""
              />
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}

export default ResultsSection;