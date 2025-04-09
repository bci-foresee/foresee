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
  reactFlowInstance,
  setHasUnsavedChanges
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
      setHasUnsavedChanges(true);
    },
    [setEdges, setHasUnsavedChanges]
  );

  /** 🔹 Drag & Drop Handling */
  const onDragOver = (event) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = "move";
  };

  const onDrop = useCallback(
    (event) => {
      event.preventDefault();

      const reactFlowBounds = event.currentTarget.getBoundingClientRect();

      if (!reactFlowInstance) {
        console.error("❌ ReactFlow instance is not ready yet.");
        return;
      }

      const data = event.dataTransfer.getData("module");

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
        ...module,
        position,
        data: {
          label: module.label || module.name,
          name: module.name,
          nodeType: module.nodeType,
          properties: module.properties || {},
        },
        style: getNodeStyle(module, false),
        sourcePosition: "right",
        targetPosition: "left",
      };

      setNodes((nds) => [...nds, newNode]);
      setHasUnsavedChanges(true);
    },
    [reactFlowInstance, setNodes, setHasUnsavedChanges]
  );

  const updateNodeProperty = useCallback(
    async (nodeId, propertyName, value) => {
      try {
        // First, update the node in state and get the updated nodes
        let updatedNodes;
        setNodes((currentNodes) => {
          updatedNodes = currentNodes.map((node) => {
            if (node.id === nodeId) {
              return {
                ...node,
                properties: {
                  ...(node.properties || {}),
                  [propertyName]: value,
                },
              };
            }
            return node;
          });
          return updatedNodes;
        });

        // Wait for state update to complete
        await new Promise((resolve) => setTimeout(resolve, 0));

        // Then save to database with the updated nodes
        const graphData = {
          nodes: updatedNodes, // Use the updatedNodes we created
          edges,
        };

        if (pipelineId) {
          await window.electronAPI.editPipeline(
            pipelineId,
            pipelineName,
            pipelineDescription,
            JSON.stringify(graphData)
          );
        } else {
          await window.electronAPI.savePipeline(
            pipelineName,
            pipelineDescription,
            JSON.stringify(graphData)
          );
        }

        setHasUnsavedChanges(false);
      } catch (error) {
        console.error("❌ Failed to update property:", error);
        throw error;
      }
    },
    [
      setNodes,
      setHasUnsavedChanges,
      edges,
      pipelineId,
      pipelineName,
      pipelineDescription,
    ]
  );

  const saveData = async () => {
    if (!nodes || nodes.length === 0) {
      console.error("❌ No nodes to save!");
      return;
    }

    const graphData = {
      nodes: nodes.map((node) => {
        return {
          ...node,
        };
      }),
      edges,
    };

    try {
      let result;
      if (pipelineId) {
        result = await window.electronAPI.editPipeline(
          pipelineId,
          pipelineName,
          pipelineDescription,
          JSON.stringify(graphData)
        );
      } else {
        result = await window.electronAPI.savePipeline(
          pipelineName,
          pipelineDescription,
          JSON.stringify(graphData)
        );
      }

      setHasUnsavedChanges(false);
      return result;
    } catch (error) {
      console.error("❌ Failed to save pipeline:", error);
      throw error;
    }
  };

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
