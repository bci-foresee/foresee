/**
 * Canvas component for rendering the interactive graph using React Flow.
 * Handles node and edge rendering, drag-and-drop, and event listeners.
 */

"use client";
import React, { useMemo, useState, useEffect } from "react";
import ReactFlow, {
  Background,
  Controls,
  ReactFlowProvider,
  addEdge,
} from "reactflow";
import "reactflow/dist/style.css";
import { useRouter } from "next/navigation";
import { useGraphState } from "./useGraphState";
import { useGraphEvents } from "./useGraphEvents";
import { getNodeStyle, getEdgeStyle } from "./styles";
import { ExpandedNode } from "./ExpandedNode"; // ✅ Import the new component
import FlowContent from "./FlowContent"; // ✅ Import FlowContent

export default function Canvas({
  graphData,
  pipelineId,
  pipelineName,
  pipelineDescription,
  readOnly = false, // ← default false
}) {

  if (!graphData) return <p>Loading...</p>;

  let parsedData;
  try {
    parsedData =
      typeof graphData === "string" ? JSON.parse(graphData) : graphData;
  } catch (error) {
    console.error("Invalid graph data format:", error);
    return <p>Error loading graph.</p>;
  }

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
    updateNodeProperty,
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

  const renderedNodes = useMemo(() => {
    if (!nodes || nodes.length === 0) return [];
    return nodes.map((node) => ({
      ...node,
      style: getNodeStyle(node, node.id === selectedNodeId),
      data: {
        ...node.data,
        label: node.data.expanded ? (
          <ExpandedNode
            node={node}
            updateNodeProperty={updateNodeProperty}
          /> // ✅ Use the new component
        ) : (
          node.data.label
        ),
      },
    }));
  }, [nodes, selectedNodeId]);

  const renderedEdges = useMemo(() => {
    if (!edges || edges.length === 0) return [];
    return edges.map((edge) => ({
      ...edge,
      style: getEdgeStyle(edge, edge.id === selectedEdgeId),
    }));
  }, [edges, selectedEdgeId]);

  return (
    <>
      <div
        className="w-full h-full bg-gray-100"
        style={{ height: "100vh" }}
        onDrop={(event) => {
          onDrop(event);
        }}
        onDragOver={(event) => {
          event.preventDefault();
          onDragOver(event);
        }}
      >
        <ReactFlowProvider>
        <ReactFlow
          nodes={renderedNodes.map((n) => ({
            ...n,
            draggable: !readOnly,
          }))}
          edges={renderedEdges}
          onNodesChange={!readOnly ? onNodesChange : undefined}
          onEdgesChange={!readOnly ? onEdgesChange : undefined}
          onNodeClick={!readOnly ? onNodeClick : undefined}
          onEdgeClick={!readOnly ? onEdgeClick : undefined}
          onConnect={!readOnly ? onConnect : undefined}
          fitView
          style={{ width: "100%", height: "100%", zIndex: 1 }}
          onInit={(instance) => setReactFlowInstance(instance)}
        >
            <FlowContent
              setNodes={setNodes}
              reactFlowInstance={reactFlowInstance}
            />

            <Controls />
            <Background />
          </ReactFlow>
        </ReactFlowProvider>
      </div>
      {!readOnly && (
        <button
          className="absolute bottom-4 right-4 px-4 py-2 bg-red-500 text-white rounded hover:bg-red-700"
          onClick={saveData}
        >
          Save Pipeline
        </button>
      )}
    </>
  );
}
