import { useMemo } from "react";
import { useNodesState, useEdgesState } from "reactflow";
import { getNodeStyle, getEdgeStyle } from "./styles";

export function useGraphState(parsedData) {
  const initialNodes = useMemo(() => {
    if (!parsedData || !parsedData.nodes) return [];
    return parsedData.nodes.map((node) => ({
      id: node.id.toString(),
      data: {
        label: node.label,
        expanded: false,
        properties: node.properties || {},
      },
      type: node.type || "default", // Ensure type is always set
      position: { x: node.x || 0, y: node.y || 0 },
      style: getNodeStyle(node, false),
      sourcePosition: "right",
      targetPosition: "left",
    }));
  }, [parsedData]);

  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);

  const initialEdges = useMemo(() => {
    if (!parsedData || !parsedData.edges) return [];
    return parsedData.edges.map((edge) => ({
      id: `${edge.source}-${edge.target}`,
      source: edge.source.toString(),
      target: edge.target.toString(),
      animated: true,
      style: getEdgeStyle(edge, false),
    }));
  }, [parsedData]);

  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  return { nodes, setNodes, onNodesChange, edges, setEdges, onEdgesChange };
}
