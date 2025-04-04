/**
 * Styling functions for nodes and edges in React Flow.
 */

export const getNodeStyle = (node, isSelected) => {
  const baseStyle = {
    padding: "5px 10px",
    width: "fit-content",
    maxWidth: "250px",
    minWidth: "30px",
    textAlign: "center",
    whiteSpace: "normal",
    wordBreak: "break-word",
    backgroundColor: "white",
    fontSize: "12px",
  };

  const nodeType = node.data?.nodeType ?? "default";

  const typeStyles = {
    input: { border: "2px solid gray", borderRadius: 10 },
    module: { border: "2px solid red", borderRadius: 10 },
    storage: { border: "2px solid #999", borderRadius: 4 },
    default: { border: "2px solid black", borderRadius: 4 },
  };

  const selectedStyle = isSelected
    ? {
        border: "3px solid blue",
        backgroundColor: "#B3D7FF",
      }
    : {};

  return {
    ...baseStyle,
    ...(typeStyles[nodeType] || typeStyles.default),
    ...selectedStyle,
  };
};

export const getEdgeStyle = (edge, isSelected) => ({
  stroke: isSelected ? "blue" : "orange",
  strokeWidth: isSelected ? 3 : 2,
  markerEnd: "url(#arrow)",
  animated: true,
});
