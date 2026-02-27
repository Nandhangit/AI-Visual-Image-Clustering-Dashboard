import { useState } from "react";
import UploadSection from "./components/UploadSection";
import ResultsSection from "./components/ResultsSection";
import "./App.css";

function App() {
  const [clusters, setClusters] = useState({});
  const [loading, setLoading] = useState(false);

  return (
    <div className="app">
      <div className="container">
        <h1 className="title">Smart Semantic Image Grouping</h1>

        <UploadSection
          setClusters={setClusters}
          setLoading={setLoading}
        />

        <ResultsSection
          clusters={clusters}
          loading={loading}
        />
      </div>
    </div>
  );
}

export default App;