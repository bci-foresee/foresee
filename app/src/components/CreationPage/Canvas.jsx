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

export default function Canvas({ graphData, pipelineId }) {
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

  const [nodes, setNodes, onNodesChange] = useNodesState(
    parsedData.nodes.map((node) => {
      return {
        id: node.id.toString(),
        data: { label: node.label },
        position: { x: node.x, y: node.y },
        style: {
          border: "2px solid red",
          padding: 10,
          borderRadius: 10,
          backgroundColor: "white",
        },
        sourcePosition: "right",
        targetPosition: "left",
      };
    })
  );

  const [edges, setEdges, onEdgesChange] = useEdgesState(
    parsedData.edges.map((edge) => ({
      id: `${edge.source}-${edge.target}`,
      source: edge.source.toString(),
      target: edge.target.toString(),
      animated: true,
      style: { stroke: "red", strokeWidth: 2 },
    }))
  );

  const [selectedNodeId, setSelectedNodeId] = useState(null);
  const [selectedEdgeId, setSelectedEdgeId] = useState(null);
  const [reactFlowInstance, setReactFlowInstance] = useState(null);

  // Handle node selection
  const onNodeClick = (event, node) => {
    setSelectedNodeId(node.id);
    setSelectedEdgeId(null); // Deselect edge if node is selected
  };

  // Handle edge selection
  const onEdgeClick = (event, edge) => {
    setSelectedEdgeId(edge.id);
    setSelectedNodeId(null); // Deselect node if edge is selected
  };

  // Handle deletion of selected node or edge
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

  // Allow dynamic node connections
  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge(params, eds)),
    []
  );

  // Allow dropping new nodes into the canvas
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
      console.log("Dropped module:", module);

      const position = reactFlowInstance.project({
        x: event.clientX - reactFlowBounds.left,
        y: event.clientY - reactFlowBounds.top,
      });

      console.log("New node position:", position);

      const newNode = {
        id: `${Date.now()}`, // Unique ID
        position,
        data: { label: module.name },
        style: {
          border: "2px solid red",
          padding: 10,
          borderRadius: 10,
          backgroundColor: "white",
        },
        sourcePosition: "right",
        targetPosition: "left",
      };

      setNodes((nds) => [...nds, newNode]);
    },
    [reactFlowInstance, setNodes]
  );

  const savePipeline = () => {
    if (!pipelineId) {
      console.error("Pipeline ID is missing.");
      return;
    }

    const graphData = {
      nodes: nodes.map((node) => ({
        id: node.id,
        label: node.data.label,
        x: node.position.x,
        y: node.position.y,
      })),
      edges: edges.map((edge) => ({
        source: edge.source,
        target: edge.target,
      })),
    };

    window.electronAPI
      .editPipeline(pipelineId, graphData)
      .then(() => console.log("Pipeline saved successfully!"))
      .catch((error) => console.error("Failed to save pipeline:", error));
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
            style: {
              ...node.style,
              border:
                selectedNodeId === node.id ? "3px solid blue" : "2px solid red",
              backgroundColor:
                selectedNodeId === node.id ? "lightblue" : "white",
            },
          }))}
          edges={edges.map((edge) => ({
            ...edge,
            animated: true,
            style: {
              stroke: selectedEdgeId === edge.id ? "blue" : "red",
              strokeWidth: selectedEdgeId === edge.id ? 3 : 2,
            },
          }))}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onNodeClick={onNodeClick}
          onEdgeClick={onEdgeClick}
          onConnect={onConnect}
          fitView
          onInit={(instance) => {
            console.log("ReactFlow instance initialized:", instance);
            setReactFlowInstance(instance);
          }}
        >
          <Controls />
          <Background />
        </ReactFlow>
      </ReactFlowProvider>
      <button
        className="absolute bottom-4 right-4 px-4 py-2 bg-red-500 text-white rounded hover:bg-red-700"
        onClick={savePipeline}
      >
        Save Pipeline
      </button>
    </div>
  );
}
