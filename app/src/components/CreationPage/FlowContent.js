/**
 * FlowContent component that manages drag-and-drop functionality for nodes.
 * Ensures new nodes are positioned correctly on the canvas.
 */

"use client";
import React, { useEffect, useCallback } from "react";
import { useReactFlow } from "reactflow";

export default function FlowContent({ setNodes, reactFlowInstance }) {
  const { fitView } = useReactFlow();

  /**
   * Handles drag-over event to allow dropping nodes onto the canvas.
   */

  const onDragOver = useCallback((event) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = "move";
  }, []);

  /**
   * Handles the drop event, parsing the dropped module and adding it to the canvas.
   */

  const onDrop = useCallback(
    (event) => {
      event.preventDefault();

      if (!reactFlowInstance) {
        console.error("❌ ReactFlow instance is not ready");
        return;
      }

      const data = event.dataTransfer.getData("module");
      if (!data) {
        console.warn("⚠ No module data received.");
        return;
      }

      try {
        const moduleData = JSON.parse(data);
        const { top, left } = event.target.getBoundingClientRect();
        const position = reactFlowInstance.project({
          x: event.clientX - left,
          y: event.clientY - top,
        });

        const newNode = {
          id: `${Date.now()}`,
          ...moduleData,
          position,
          data: {
            label: moduleData.label || moduleData.name,
            name: moduleData.name,
            nodeType: moduleData.nodeType,
            properties: moduleData.properties || {},
          },
          style: getNodeStyle(moduleData, false),
          sourcePosition: "right",
          targetPosition: "left",
        };

        setNodes((nds) => [...nds, newNode]);
      } catch (error) {
        console.error("❌ Failed to parse module data:", error);
      }
    },
    [reactFlowInstance, setNodes]
  );

  useEffect(() => {
    if (reactFlowInstance) {
      fitView();
    }
  }, [fitView, reactFlowInstance]);

  return (
    <div
      style={{ width: "100%", height: "100%" }}
      onDrop={onDrop}
      onDragOver={onDragOver}
    />
  );
}
