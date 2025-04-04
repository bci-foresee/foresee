/**
 * Custom hook for handling dynamic updates and interactions with the graph.
 *
 * This hook provides functions for modifying nodes and edges,
 * including click events, connecting nodes, deleting elements, and handling drag-and-drop.
 */
import { useCallback, useEffect, useState, useMemo } from "react";
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
  const selectedNode = useMemo(
    () => nodes.find((n) => n.id === selectedNodeId),
    [nodes, selectedNodeId]
  );
  const onNodeClick = useCallback(
    (event, node) => {
      const tag = event.target.tagName.toLowerCase();
      if (["input", "textarea", "select", "button"].includes(tag)) {
        event.stopPropagation();
        return;
      }

      const clickedNode = nodes.find((n) => n.id === node.id);
      if (!clickedNode || !reactFlowInstance) return;

      const offsetX = -200;
      const offsetY = 100;

      const targetX = clickedNode.position.x - offsetX;
      const targetY = clickedNode.position.y + offsetY;

      setTimeout(() => {
        reactFlowInstance.setCenter(targetX, targetY, {
          zoom: 1.2,
          duration: 300,
        });
      }, 50);

      setSelectedNodeId(node.id);
      setSelectedEdgeId(null);
    },
    [nodes, reactFlowInstance, setSelectedNodeId, setSelectedEdgeId]
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
          setSelectedNode(null);
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

      const newNode = {
        id: `${Date.now()}`, // Unique ID
        position: reactFlowInstance.project({
          x: event.clientX,
          y: event.clientY,
        }),
        data: {
          label: module.label,
          name: module.name,
          properties: module.properties || {}, // ✅ Ensure properties are included
          nodeType: module.nodeType || "default",
        },
        style: getNodeStyle(module, false),
        sourcePosition: "right",
        targetPosition: "left",
      };

      setNodes((nds) => [...nds, newNode]);
    },
    [reactFlowInstance, setNodes]
  );

  const saveData = (nodeId, updatedProperties) => {
    setNodes((currentNodes) =>
      currentNodes.map((node) =>
        node.id === nodeId
          ? {
              ...node,
              data: {
                ...node.data,
                properties: structuredClone(updatedProperties),
              },
            }
          : node
      )
    );

    // After setNodes resolves, you can also debounce or delay this:
    const graphData = {
      nodes: nodes.map((node) => ({
        id: node.id,
        label: node.data.label,
        name: node.data.name,
        nodeType: node.data.nodeType,
        x: node.position.x,
        y: node.position.y,
        properties:
          node.id === nodeId
            ? structuredClone(updatedProperties)
            : node.data.properties || {},
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

    savePromise.catch((error) => {
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
    selectedNode,
    selectedNodeId,
    selectedEdgeId,
    setSelectedNodeId,
    onNodeClick,
    onEdgeClick,
    onConnect,
    onDragOver,
    onDrop,
    saveData,
    updateNodeProperty,
  };
}
