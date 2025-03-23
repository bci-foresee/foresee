// app/analysis/page.js
"use client";

import { useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import Canvas from "../../components/CreationPage/Canvas";
import NavbarAnalysis from "../../components/AnalysisPage/NavbarAnalysis";

const hardcodedMetrics = {
  runtime: "60.08s",
  coldStartDuration: "0.50s",
  coldStartPercent: "100.00%",
  errorPercent: "0.00%",
  cost: "0.10 cents",
};

export default function AnalysisPage() {
  const searchParams = useSearchParams();
  const pipelineId = searchParams.get("id");
  const [pipeline, setPipeline] = useState(null);

  useEffect(() => {
    if (pipelineId) {
      window.electronAPI.getPipelineById(pipelineId).then((data) => {
        setPipeline(data);
      });
    }
  }, [pipelineId]);

  return (
    <div className="flex flex-col h-full w-full bg-gray-50">
      <NavbarAnalysis pipelineName={pipeline?.name} />
      <div className="flex-grow flex flex-col px-6">
        {/* Canvas (read-only) */}
        <div className="h-[400px] border rounded-lg overflow-hidden my-4 shadow-md bg-white">
          {pipeline ? (
            <Canvas
              graphData={JSON.parse(pipeline.graph_structure)}
              pipelineId={pipelineId}
              pipelineName={pipeline.name}
              pipelineDescription={pipeline.description}
              readOnly={true} // we'll add this to the Canvas component next
            />
          ) : (
            <p className="p-4">Loading pipeline...</p>
          )}
        </div>

        {/* Metrics Overview */}
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-8">
          {Object.entries(hardcodedMetrics).map(([key, val]) => (
            <div key={key} className="bg-white rounded-lg shadow p-4 text-center">
              <p className="text-sm text-gray-500 uppercase tracking-wider">{key.replace(/([A-Z])/g, ' $1')}</p>
              <p className="text-lg font-bold text-gray-900">{val}</p>
            </div>
          ))}
        </div>

        {/* Placeholder: Future Chart Section */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Performance Breakdown</h2>
          <p className="text-gray-500">Charts and logs will appear here.</p>
        </div>
      </div>
    </div>
  );
}
