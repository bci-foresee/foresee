"use client";

import { useEffect, useState, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import Canvas from "../../components/CreationPage/Canvas";
import NavBar from "../../components/CreationPage/NavBar";

function CreationContent() {
  const searchParams = useSearchParams();
  const pipelineId = searchParams.get("id");
  const [pipeline, setPipeline] = useState(null);
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false);
  const [nodes, setNodes] = useState([]);
  const [edges, setEdges] = useState([]);
  const [isModulesOpen, setIsModulesOpen] = useState(false);

  useEffect(() => {
    if (pipelineId) {
      window.electronAPI
        .getPipelineById(pipelineId)
        .then((data) => {
          if (data && data.graph_structure) {
            const parsedGraph = JSON.parse(data.graph_structure);
            setPipeline(data);
            setNodes(parsedGraph.nodes);
            setEdges(parsedGraph.edges);
          } else {
            console.error("Invalid pipeline data:", data);
            setPipeline({
              graph_structure: JSON.stringify({ nodes: [], edges: [] }),
            });
          }
        })
        .catch((err) => {
          console.error("Error fetching pipeline:", err);
          setPipeline({
            graph_structure: JSON.stringify({ nodes: [], edges: [] }),
          });
        });
    } else {
      setPipeline({
        name: "Untitled",
        graph_structure: JSON.stringify({ nodes: [], edges: [] }),
      });
    }
  }, [pipelineId]);

  const updatePipelineInfo = (newName, newDescription) => {
    setPipeline((prev) => ({
      ...prev,
      name: newName,
      description: newDescription,
    }));
  };

  return (
    <div className="flex flex-col h-full w-full bg-gray-100" onClick={() => setIsModulesOpen(false)}>
      {/* NavBar with Modules Dropdown */}
      <NavBar
        pipelineName={pipeline?.name}
        pipelineDescription={pipeline?.description}
        updatePipelineInfo={updatePipelineInfo}
        pipelineId={pipelineId}
        hasUnsavedChanges={hasUnsavedChanges}
        isModulesOpen={isModulesOpen}
        setIsModulesOpen={setIsModulesOpen}
      />

      <div className="flex-grow flex flex-col">
        {pipeline ? (
          <Canvas
            graphData={JSON.parse(pipeline.graph_structure)}
            pipelineId={pipelineId}
            pipelineName={pipeline.name}
            pipelineDescription={pipeline.description}
            setHasUnsavedChanges={setHasUnsavedChanges}
            setNodes={setNodes}
            setEdges={setEdges}
          />
        ) : (
          <p className="text-lg font-semibold p-6">Loading pipeline...</p>
        )}
      </div>
    </div>
  );
}

const CreationPage = () => {
  return (
    <Suspense fallback={<div className="p-6">Loading...</div>}>
      <CreationContent />
    </Suspense>
  );
};

export default CreationPage;
