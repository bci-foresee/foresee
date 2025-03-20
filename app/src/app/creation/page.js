"use client";

import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import Canvas from "../../components/CreationPage/Canvas";
import Navbar from "../../components/CreationPage/Navbar";
import { Button } from "../../components/CreationPage/Button";

const CreationPage = () => {
  const searchParams = useSearchParams();
  const pipelineId = searchParams.get("id");
  const [pipeline, setPipeline] = useState(null);
  const [draggedModule, setDraggedModule] = useState(null);

  useEffect(() => {
    if (pipelineId) {
      window.electronAPI
        .getPipelineById(pipelineId)
        .then(
          (data) => (console.log("Fetched Pipeline:", data), setPipeline(data))
        )
        .catch((err) => console.error("Error fetching pipeline:", err));
    }
  }, [pipelineId]);

  const handleDragStart = (e, module) => {
    e.dataTransfer.setData("module", JSON.stringify(module));
    setDraggedModule(module);
  };

  return (
    <div className="flex flex-col h-full w-full bg-gray-100">
      {/* Navbar with Modules Dropdown */}
      <Navbar onDragStart={handleDragStart} />

      <div className="flex-grow flex flex-col">
        {pipeline ? (
          <Canvas
            graphData={JSON.parse(pipeline.graph_structure)}
            pipelineId={pipelineId}
          />
        ) : (
          <p className="text-lg font-semibold p-6">Create new pipeline.</p>
        )}
      </div>
    </div>
  );
};

export default CreationPage;
