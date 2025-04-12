/**
 * Custom hook for initializing and managing the state of nodes and edges in React Flow.
 *
 * This hook sets up the initial graph state based on provided data.
 * It does not handle updates—state changes should be managed using `useGraphEvents.js`.
 */

import { useMemo, useCallback } from "react";
import {
  useNodesState,
  useEdgesState,
  applyNodeChanges,
  applyEdgeChanges,
} from "reactflow";
import { getNodeStyle, getEdgeStyle } from "./styles";

export function useGraphState(parsedData) {
  const initialNodes = useMemo(() => {
    if (!parsedData || !parsedData.nodes) return [];
    return parsedData.nodes.map((node) => ({
      ...node,
      id: node.id.toString(),
      position: node.position || { x: 0, y: 0 },
      style: getNodeStyle(node, false),
      sourcePosition: "right",
      targetPosition: "left",
    }));
  }, [parsedData]);

  const [nodes, setNodes] = useNodesState(initialNodes);

  const initialEdges = useMemo(() => {
    if (!parsedData || !parsedData.edges) return [];
    return parsedData.edges.map((edge) => ({
      ...edge,
      id: `${edge.source}-${edge.target}`,
      source: edge.source.toString(),
      target: edge.target.toString(),
      animated: true,
      style: getEdgeStyle(edge, false),
    }));
  }, [parsedData]);

  const [edges, setEdges] = useEdgesState(initialEdges);

  const onNodesChange = useCallback(
    (changes) => {
      setNodes((nds) => applyNodeChanges(changes, nds));
    },
    [setNodes]
  );

  const onEdgesChange = useCallback(
    (changes) => {
      setEdges((eds) => applyEdgeChanges(changes, eds));
    },
    [setEdges]
  );

  return {
    nodes,
    setNodes,
    onNodesChange,
    edges,
    setEdges,
    onEdgesChange,
  };
}
