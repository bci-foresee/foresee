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
    console.log("🟡 Dragging over ReactFlow.");
  }, []);

  /**
   * Handles the drop event, parsing the dropped module and adding it to the canvas.
   */

  const onDrop = useCallback(
    (event) => {
      event.preventDefault();
      console.log("🟢 Drop event detected");

      if (!reactFlowInstance) {
        console.error("❌ ReactFlow instance is not ready");
        return;
      }

      const data = event.dataTransfer.getData("module");
      if (!data) {
        console.warn("⚠ No module data received.");
        return;
      }

      console.log("📩 Received data:", data);

      let module;
      try {
        module = JSON.parse(data);
      } catch (error) {
        console.error("❌ Failed to parse module data:", error);
        return;
      }

      console.log("📌 Parsed module:", module);
    },
    [reactFlowInstance]
  );

  useEffect(() => {
    if (reactFlowInstance) {
      console.log("✅ ReactFlow instance ready");
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
