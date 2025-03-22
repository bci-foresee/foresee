import { useCallback, useEffect, useState } from "react";
import { addEdge } from "reactflow";

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

  const onNodeClick = useCallback((event, node) => {
    setNodes((nds) =>
      nds.map((n) =>
        n.id === node.id
          ? { ...n, data: { ...n.data, expanded: !n.data.expanded } }
          : n
      )
    );

    setSelectedNodeId(node.id);
    setSelectedEdgeId(null);
  }, []);

  const onEdgeClick = useCallback((event, edge) => {
    setSelectedEdgeId(edge.id);
    setSelectedNodeId(null);
  }, []);

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

  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge(params, eds)),
    []
  );

  /** 🔹 Drag & Drop Handling */
  const onDragOver = (event) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = "move";
    console.log("🟢 Dragging over canvas");
  };

  const onDrop = useCallback(
    (event) => {
      event.preventDefault();
      console.log("🟢 Drop event detected");

      if (!reactFlowInstance) {
        console.error("❌ ReactFlow instance not initialized");
        return;
      }

      const reactFlowBounds = event.target.getBoundingClientRect();
      const data = event.dataTransfer.getData("module");

      if (!data) {
        console.warn("⚠ No module data received.");
        return;
      }

      const module = JSON.parse(data);
      const position = reactFlowInstance.project({
        x: event.clientX - reactFlowBounds.left,
        y: event.clientY - reactFlowBounds.top,
      });

      console.log("📌 New node position:", position);

      const newNode = {
        id: `${Date.now()}`,
        type: module.type,
        position,
        data: { label: module.icon },
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

    console.log("🔍 Saving Data:", graphData); // Debugging log

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
        console.log("✅ Pipeline saved successfully!");
        router.push(`/`); // Ensure redirect after saving
      })
      .catch((error) => {
        console.error("❌ Failed to save pipeline:", error);
      });
  };

  return {
    selectedNodeId,
    selectedEdgeId,
    onNodeClick,
    onEdgeClick,
    onConnect,
    onDragOver,
    onDrop,
    saveData,
  };
}
