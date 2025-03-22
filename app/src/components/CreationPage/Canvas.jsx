"use client";
import React, { useMemo, useState, useEffect } from "react";
import ReactFlow, {
  Background,
  Controls,
  ReactFlowProvider,
  useReactFlow,
  addEdge,
} from "reactflow";
import "reactflow/dist/style.css";
import { useRouter } from "next/navigation";
import { useGraphState } from "./useGraphState";
import { useGraphEvents } from "./useGraphEvents";
import { getNodeStyle, getEdgeStyle } from "./styles";

export default function Canvas({
  graphData,
  pipelineId,
  pipelineName,
  pipelineDescription,
}) {
  if (!graphData) return <p>Loading...</p>;
  console.log(graphData, "QQ");

  let parsedData;
  try {
    parsedData =
      typeof graphData === "string" ? JSON.parse(graphData) : graphData;
  } catch (error) {
    console.error("Invalid graph data format:", error);
    return <p>Error loading graph.</p>;
  }

  console.log(parsedData, "QQQ");

  const router = useRouter();
  const [reactFlowInstance, setReactFlowInstance] = useState(null);
  const { nodes, setNodes, onNodesChange, edges, setEdges, onEdgesChange } =
    useGraphState(parsedData);

  const {
    selectedNodeId,
    selectedEdgeId,
    onNodeClick,
    onEdgeClick,
    onConnect,
    onDragOver,
    onDrop,
    saveData,
  } = useGraphEvents(
    setNodes,
    setEdges,
    nodes,
    edges,
    pipelineId,
    pipelineName,
    pipelineDescription,
    router,
    reactFlowInstance
  );

  console.log(nodes);

  // ✅ Ensure nodes have styles and labels correctly set up
  const renderedNodes = useMemo(() => {
    if (!nodes || nodes.length === 0) return [];

    return nodes.map((node) => {
      const { expanded, label, properties } = node.data || {};

      return {
        ...node,
        style: getNodeStyle(node, node.id === selectedNodeId),
        data: {
          ...node.data,
          label: (
            <div>
              <strong>{label || "Unnamed Node"}</strong>
              {expanded && properties && Object.keys(properties).length > 0 && (
                <div className="mt-2 text-xs text-gray-700 bg-white p-2 border rounded shadow">
                  {Object.entries(properties).map(([key, prop]) => (
                    <p key={key}>
                      <strong>{key}:</strong> {prop?.value} {prop?.unit}
                    </p>
                  ))}
                </div>
              )}
            </div>
          ),
        },
      };
    });
  }, [nodes, selectedNodeId]);

  console.log(
    "🔍 Rendered Nodes:",
    nodes.map((node) => node.data)
  );

  const renderedEdges = useMemo(() => {
    if (!edges || edges.length === 0) return [];
    return edges.map((edge) => ({
      ...edge,
      style: getEdgeStyle(edge, edge.id === selectedEdgeId),
    }));
  }, [edges, selectedEdgeId]);

  return (
    <>
      <div className="w-full h-full bg-gray-100" style={{ height: "100vh" }}>
        <ReactFlowProvider>
          <ReactFlow
            nodes={renderedNodes}
            edges={renderedEdges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onNodeClick={onNodeClick} // ✅ Fixes node click issue
            onEdgeClick={onEdgeClick} // ✅ Fixes edge click issue
            onConnect={(params) => setEdges((eds) => addEdge(params, eds))}
            fitView
            style={{ width: "100%", height: "100%", zIndex: 1 }}
            onInit={(instance) => {
              setReactFlowInstance(instance);
              console.log("✅ ReactFlow instance initialized:", instance);
            }}
          >
            <FlowContent
              reactFlowInstance={reactFlowInstance}
              setNodes={setNodes}
              setEdges={setEdges}
              router={router}
              pipelineId={pipelineId}
              pipelineName={pipelineName}
              pipelineDescription={pipelineDescription}
            />
            <Controls />
            <Background />
          </ReactFlow>
        </ReactFlowProvider>
      </div>
      <button
        className="absolute bottom-4 right-4 px-4 py-2 bg-red-500 text-white rounded hover:bg-red-700"
        onClick={saveData}
      >
        Save Pipeline
      </button>
    </>
  );
}

// ✅ Fixes FlowContent Blocking Clicks
function FlowContent({
  reactFlowInstance,
  setNodes,
  setEdges,
  router,
  pipelineId,
  pipelineName,
  pipelineDescription,
}) {
  const { fitView } = useReactFlow();

  const { onDrop, onDragOver } = useGraphEvents(
    setNodes,
    setEdges,
    reactFlowInstance,
    pipelineId,
    pipelineName,
    pipelineDescription,
    router
  );

  useEffect(() => {
    if (reactFlowInstance) {
      console.log("🔄 Running fitView()");
      fitView();
    }
  }, [fitView, reactFlowInstance]);

  return null; // ✅ No extra div blocking clicks
}
