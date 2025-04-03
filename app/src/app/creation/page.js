"use client";

import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import Canvas from "../../components/CreationPage/Canvas";
import Navbar from "../../components/CreationPage/Navbar";

const CreationPage = () => {
  const searchParams = useSearchParams();
  const pipelineId = searchParams.get("id");
  const [pipeline, setPipeline] = useState(null);

  useEffect(() => {
    if (pipelineId) {
      window.electronAPI
        .getPipelineById(pipelineId)
        .then((data) => {
          if (data && data.graph_structure) {
            setPipeline(data);
          } else {
            console.error("Invalid pipeline data:", data);
            setPipeline({ graph_structure: JSON.stringify({ nodes: [], edges: [] }) });
          }
        })
        .catch((err) => {
          console.error("Error fetching pipeline:", err);
          setPipeline({ graph_structure: JSON.stringify({ nodes: [], edges: [] }) });
        });
    } else {
      setPipeline({ name: 'Untitled', graph_structure: JSON.stringify({ nodes: [], edges: [] }) });
    }
  }, [pipelineId]);

  const updatePipelineInfo = (newName, newDescription) => {
    setPipeline((prev) => ({ ...prev, name: newName, description: newDescription }));
  };

  return (
    <div className="flex flex-col h-full w-full bg-gray-100">
      {/* Navbar with Modules Dropdown */}
      <Navbar
        pipelineName={pipeline?.name}
        pipelineDescription={pipeline?.description}
        updatePipelineInfo={updatePipelineInfo}
        pipelineId={pipelineId}
      />

      <div className="flex-grow flex flex-col">
        {pipeline ? (
          <Canvas
            graphData={JSON.parse(pipeline.graph_structure)}
            pipelineId={pipelineId}
            pipelineName={pipeline.name}
            pipelineDescription={pipeline.description}
          />
        ) : (
          <p className="text-lg font-semibold p-6">Loading pipeline...</p>
        )}
      </div>
    </div>
  );
};

export default CreationPage;
