/**
 * Custom hook for handling dynamic updates and interactions with the graph.
 *
 * This hook provides functions for modifying nodes and edges,
 * including click events, connecting nodes, deleting elements, and handling drag-and-drop.
 */
import { useCallback, useEffect, useState } from "react";
import { addEdge } from "reactflow";
import { getNodeStyle, getEdgeStyle } from "./styles";

export function useGraphEvents(
  setNodes,
  setEdges,
  nodes,
  edges,
  pipelineId,
  pipelineName,
  pipelineDescription,
  router,
  reactFlowInstance
) {
  const [selectedNodeId, setSelectedNodeId] = useState(null);
  const [selectedEdgeId, setSelectedEdgeId] = useState(null);

  const onNodeClick = useCallback(
    (event, node) => {
      // ✅ Prevent collapsing when clicking inside an input field
      const tag = event.target.tagName.toLowerCase();
      if (tag === "input" || tag === "textarea" || tag === "select") {
        event.stopPropagation(); // ✅ Stop event from reaching the node
        return;
      }

      setNodes((nds) =>
        nds.map((n) =>
          n.id === node.id
            ? { ...n, data: { ...n.data, expanded: !n.data.expanded } }
            : n
        )
      );

      setSelectedNodeId(node.id);
      setSelectedEdgeId(null);
    },
    [setNodes]
  );

  const onEdgeClick = useCallback((event, edge) => {
    setSelectedEdgeId(edge.id);
    setSelectedNodeId(null);
  }, []);

  /**
   * Deletes selected nodes or edges when the Delete/Backspace key is pressed.
   * Prevents deletion if an input field is focused.
   */
  const onDeleteKey = useCallback(
    (event) => {
      // ✅ Prevent node deletion if the user is typing in an input or textarea
      if (
        document.activeElement.tagName === "INPUT" ||
        document.activeElement.tagName === "TEXTAREA"
      ) {
        return;
      }

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

  const onConnect = useCallback(
    (params) => {
      setEdges((eds) =>
        addEdge(
          {
            ...params,
            animated: true, // ✅ Ensure animation
            style: getEdgeStyle(params, false), // ✅ Apply dynamic styling
            markerEnd: { type: "arrowclosed" },
          },
          eds
        )
      );
    },
    [setEdges]
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
        id: `${Date.now()}`, // Unique ID
        type: module.type,
        position: reactFlowInstance.project({
          x: event.clientX,
          y: event.clientY,
        }),
        data: {
          label: module.label,
          name: module.name,
          properties: module.properties || {}, // ✅ Ensure properties are included
          expanded: false,
        },
        style: getNodeStyle(module, false),
        sourcePosition: "right",
        targetPosition: "left",
      };

      setNodes((nds) => [...nds, newNode]);
    },
    [reactFlowInstance, setNodes]
  );

  const saveData = () => {
    const graphData = {
      nodes: nodes.map((node) => ({
        id: node.id,
        label: node.data.label,
        name: node.data.name,
        type: node.type,
        x: node.position.x,
        y: node.position.y,
        properties: node.data.properties || {}, // ✅ Ensure properties are saved
      })),
      edges: edges.map((edge) => ({
        source: edge.source,
        target: edge.target,
      })),
    };

    const savePromise = pipelineId
      ? window.electronAPI.editPipeline(
          pipelineId,
          pipelineName,
          pipelineDescription,
          graphData
        )
      : window.electronAPI.savePipeline(
          pipelineName,
          pipelineDescription,
          graphData
        );

    savePromise
      .then(() => {
        router.push(`/`); // Ensure redirect after saving
      })
      .catch((error) => {
        console.error("❌ Failed to save pipeline:", error);
      });
  };

  const updateNodeProperty = useCallback(
    (nodeId, propertyKey, newValue) => {
      setNodes((nds) =>
        nds.map((node) =>
          node.id === nodeId
            ? {
                ...node,
                data: {
                  ...node.data,
                  properties: {
                    ...node.data.properties,
                    [propertyKey]: {
                      ...node.data.properties[propertyKey],
                      value: newValue,
                    },
                  },
                },
              }
            : node
        )
      );
    },
    [setNodes]
  );

  return {
    selectedNodeId,
    selectedEdgeId,
    onNodeClick,
    onEdgeClick,
    onConnect,
    onDragOver,
    onDrop,
    saveData,
    updateNodeProperty,
  };
}
