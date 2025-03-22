"use client";
import React, { useState, useEffect, useCallback } from "react";
import ReactFlow, {
  Background,
  Controls,
  addEdge,
  useNodesState,
  useEdgesState,
  ReactFlowProvider,
} from "reactflow";
import "reactflow/dist/style.css";
import { useRouter } from "next/navigation";


export default function Canvas({ graphData, pipelineId, pipelineName, pipelineDescription }) {
  if (!graphData) return <p>Loading...</p>;

  let parsedData;
  try {
    parsedData =
      typeof graphData === "string" ? JSON.parse(graphData) : graphData;
  } catch (error) {
    console.error("Invalid graph data format:", error);
    return <p>Error loading graph.</p>;
  }

  if (!parsedData.nodes || !parsedData.edges)
    return <p>No graph data found.</p>;

  const router = useRouter();

  /** 🔹 Returns styles based on node type */
  const getNodeStyle = (node, isSelected) => {
    const baseStyle = {
      transition: "0.2s ease-in-out",
      padding: "5px 10px", // Balanced padding
      display: "inline-block", // Prevents it from stretching
      width: "fit-content", // Only expands based on content
      maxWidth: "250px", // Prevents excessive width
      minWidth: "30px", // Ensures it's not too small
      textAlign: "center",
      whiteSpace: "normal", // Allows text wrapping
      wordBreak: "break-word", // Ensures long words break properly
    };

    const typeStyles = {
      input: { border: "2px solid gray", borderRadius: 10 },
      module: { border: "2px solid red", borderRadius: 10 },
      storage: { border: "2px solid gray" },
      default: { border: "2px solid red" },
    };

    return {
      ...baseStyle,
      ...(typeStyles[node.type] || typeStyles.default),
      ...(isSelected && {
        border: "3px solid blue",
        backgroundColor: "#B3D7FF",
      }),
    };
  };

  /** 🔹 Returns styles for edges */
  const getEdgeStyle = (edge, isSelected) => ({
    stroke: isSelected ? "blue" : "orange",
    strokeWidth: isSelected ? 3 : 2,
    markerEnd: "url(#arrow)", // Add arrow marker
    transition: "0.2s ease-in-out",
  });

  /** 🔹 Nodes & Edges State */
  const [nodes, setNodes, onNodesChange] = useNodesState(
    parsedData.nodes.map((node) => ({
      id: node.id.toString(),
      data: { label: node.label },
      type: node.type,
      position: { x: node.x, y: node.y },
      style: getNodeStyle(node, false), // Apply default style
      sourcePosition: "right",
      targetPosition: "left",
    }))
  );

  const [edges, setEdges, onEdgesChange] = useEdgesState(
    (parsedData.edges || []).map((edge) => ({
      id: `${edge.source}-${edge.target}`,
      source: edge.source.toString(),
      target: edge.target.toString(),
      animated: true,
      style: getEdgeStyle(edge, false),
    }))
  );

  /** 🔹 Selection State */
  const [selectedNodeId, setSelectedNodeId] = useState(null);
  const [selectedEdgeId, setSelectedEdgeId] = useState(null);
  const [reactFlowInstance, setReactFlowInstance] = useState(null);

  /** 🔹 Handle Node Click */
  const onNodeClick = (event, node) => {
    setSelectedNodeId(node.id);
    setSelectedEdgeId(null);
  };

  /** 🔹 Handle Edge Click */
  const onEdgeClick = (event, edge) => {
    setSelectedEdgeId(edge.id);
    setSelectedNodeId(null);
  };

  /** 🔹 Handle Delete Key */
  const onDeleteKey = useCallback(
    (event) => {
      if (event.key === "Delete" || event.key === "Backspace") {
        if (selectedNodeId) {
          setNodes((nds) => nds.filter((n) => n.id !== selectedNodeId));
          setEdges((eds) =>
            eds.filter(
              (edge) =>
                edge.source !== selectedNodeId && edge.target !== selectedNodeId
            )
          );
          setSelectedNodeId(null);
        } else if (selectedEdgeId) {
          setEdges((eds) => eds.filter((edge) => edge.id !== selectedEdgeId));
          setSelectedEdgeId(null);
        }
      }
    },
    [selectedNodeId, selectedEdgeId, setNodes, setEdges]
  );

  useEffect(() => {
    window.addEventListener("keydown", onDeleteKey);
    return () => window.removeEventListener("keydown", onDeleteKey);
  }, [onDeleteKey]);

  /** 🔹 Enable Connections */
  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge(params, eds)),
    []
  );

  /** 🔹 Drag & Drop Handling */
  const onDragOver = (event) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = "move";
  };

  const onDrop = useCallback(
    (event) => {
      event.preventDefault();
      const reactFlowBounds = event.target.getBoundingClientRect();
      const data = event.dataTransfer.getData("module");

      if (!reactFlowInstance) {
        console.error("ReactFlow instance is not ready yet.");
        return;
      }

      if (!data) {
        console.log("No module data received.");
        return;
      }

      const module = JSON.parse(data);
      const position = reactFlowInstance.project({
        x: event.clientX - reactFlowBounds.left,
        y: event.clientY - reactFlowBounds.top,
      });

      const newNode = {
        id: `${Date.now()}`,
        type: module.type,
        position,
        data: { label: module.icon },
        style: getNodeStyle(module, false),
        sourcePosition: "right",
        targetPosition: "left",
      };

      setNodes((nds) => [...nds, newNode]);
    },
    [reactFlowInstance, setNodes]
  );

  /** 🔹 Save Pipeline */
  const saveData = () => {
    const graphData = {
      nodes: nodes.map((node) => ({
        id: node.id,
        label: node.data.label,
        type: node.type,
        x: node.position.x,
        y: node.position.y,
      })),
      edges: edges.map((edge) => ({
        source: edge.source,
        target: edge.target,
      })),
    };

    if (pipelineId) {
      window.electronAPI
      .editPipeline(pipelineId, pipelineName, pipelineDescription, graphData)
      .then(() => console.log("Pipeline saved successfully!"))
      .catch((error) => console.error("Failed to edit pipeline:", error));
    } else {
      window.electronAPI
      .savePipeline(pipelineName, pipelineDescription, graphData)
      .then(() => console.log("Pipeline saved successfully!"))
      .catch((error) => console.error("Failed to save pipeline:", error));
    }
  };

  return (
    <div
      className="w-full h-full bg-gray-100"
      style={{ height: "100vh" }}
      onDrop={onDrop}
      onDragOver={onDragOver}
    >
      <ReactFlowProvider>
        <ReactFlow
          nodes={nodes.map((node) => ({
            ...node,
            style: getNodeStyle(node, node.id === selectedNodeId),
          }))}
          edges={edges.map((edge) => ({
            ...edge,
            animated: true,
            style: getEdgeStyle(edge, edge.id === selectedEdgeId),
          }))}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onNodeClick={onNodeClick}
          onEdgeClick={onEdgeClick}
          onConnect={onConnect}
          fitView
          onInit={(instance) => setReactFlowInstance(instance)}
        >
          <Controls />
          <Background />
          <svg>
            <defs>
              <marker
                id="arrow"
                viewBox="0 0 10 10"
                refX="8"
                refY="5"
                markerWidth="6"
                markerHeight="6"
                orient="auto-start-reverse"
              >
                <path
                  d="M 0 2 L 8 5 L 0 8"
                  fill="none"
                  stroke="orange"
                  strokeWidth="2"
                />
              </marker>
            </defs>
          </svg>
        </ReactFlow>
      </ReactFlowProvider>

      <button
        className="absolute bottom-4 right-4 px-4 py-2 bg-red-500 text-white rounded hover:bg-red-700"
        onClick={() => {
          saveData();
          router.push(`/`);
        }}
      >
        Save Pipeline
      </button>
    </div>
  );
}
