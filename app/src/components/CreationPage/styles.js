/**
 * Styling functions for nodes and edges in React Flow.
 */

export const getNodeStyle = (node, isSelected) => {
  const isExpanded = node.data?.expanded ?? false;

  const baseStyle = {
    transition: "0.2s ease-in-out",
    padding: isExpanded ? "10px 15px" : "5px 10px",
    width: isExpanded ? "auto" : "fit-content",
    maxWidth: isExpanded ? "300px" : "250px",
    minWidth: "30px",
    textAlign: "center",
    whiteSpace: "normal",
    wordBreak: "break-word",
    backgroundColor: isExpanded ? "#FFF8DC" : "white",
  };

  const typeStyles = {
    input: { border: "2px solid gray", borderRadius: 10 },
    module: { border: "2px solid red", borderRadius: 10 },
    storage: { border: "2px solid gray" },
    default: { border: "2px solid red" },
  };

  return {
    ...baseStyle,
    ...(typeStyles[node.type] || typeStyles.default),
    ...(isSelected && {
      border: "3px solid blue",
      backgroundColor: "#B3D7FF",
    }),
  };
};

export function getExpandedNodeContent(label, properties) {
  return (
    <div>
      <strong>{label || "Unnamed Node"}</strong>
      {properties && Object.keys(properties).length > 0 && (
        <div className="mt-2 text-xs text-gray-700 bg-white p-2 border rounded shadow">
          {Object.entries(properties).map(([key, prop]) => (
            <p key={key}>
              <strong>{key}:</strong> {prop?.value} {prop?.unit}
            </p>
          ))}
        </div>
      )}
    </div>
  );
}

export const getEdgeStyle = (edge, isSelected) => ({
  stroke: isSelected ? "blue" : "orange",
  strokeWidth: isSelected ? 3 : 2,
  markerEnd: "url(#arrow)",
  transition: "0.2s ease-in-out",
  animated: true,
});
