import { PROPERTY_VALIDATIONS, validateProperty } from "./validation";

/**
 * Renders the expanded node content, including editable properties.
 *
 * @param {Object} node - The node object containing label and properties.
 * @param {Function} updateNodeProperty - Function to update property values.
 * @returns {JSX.Element} - The expanded node UI.
 */
export function ExpandedNode({ node, updateNodeProperty }) {
  const { label, name, properties } = node.data;

  return (
    <div className="rounded-2xl border bg-white p-4 min-w-[280px]">
      {/* Node Title */}
      <div className="font-semibold text-lg text-gray-800 text-center pb-2 border-b border-gray-300">
        {label === "Storage" ? "Storage" : name || "Unnamed Node"}
      </div>

      {/* Properties */}
      {properties && Object.keys(properties).length > 0 && (
        <div className="mt-2 space-y-3">
          {Object.entries(properties).map(([key, prop]) => {
            const validationRule = PROPERTY_VALIDATIONS[key];
            const isBoolean = validationRule?.type === "boolean";

            /** ✅ Special Handling for Storage Type Toggle **/
            if (key === "Storage Type") {
              return (
                <div key={key} className="flex flex-col gap-2">
                  <label className="font-semibold text-xs text-gray-700">
                    {key}:
                  </label>
                  <select
                    value={prop.value}
                    onChange={(e) =>
                      updateNodeProperty(node.id, key, e.target.value)
                    }
                    className="border rounded-lg px-3 py-2 text-xs bg-white focus:outline-none focus:ring-2 focus:ring-blue-300"
                  >
                    {validationRule.allowedValues.map((option) => (
                      <option key={option} value={option}>
                        {option}
                      </option>
                    ))}
                  </select>
                </div>
              );
            }

            /** ✅ Special Handling for Berger Bands **/
            if (key === "Berger Bands") {
              const bands = prop.value || [];

              return (
                <div key={key} className="flex flex-col gap-2">
                  <label className="font-semibold text-xs text-gray-700">
                    {key} (Hz):
                  </label>

                  {/* Render Each Range as Separate Inputs */}
                  {bands.map((range, index) => (
                    <div key={index} className="flex items-center gap-2">
                      <div className="relative w-24">
                        <input
                          type="number"
                          value={range.min}
                          min={validationRule.minValue}
                          max={validationRule.maxValue}
                          onChange={(e) => {
                            const newBands = [...bands];
                            newBands[index] = {
                              ...newBands[index],
                              min: e.target.value,
                            };
                            updateNodeProperty(node.id, key, newBands);
                          }}
                          className="border rounded-lg px-3 py-2 text-xs w-full pr-8"
                          placeholder="Min"
                        />
                        <span className="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-500 text-xs">
                          Hz
                        </span>
                      </div>
                      <span className="text-gray-700">-</span>
                      <div className="relative w-24">
                        <input
                          type="number"
                          value={range.max}
                          min={validationRule.minValue}
                          max={validationRule.maxValue}
                          onChange={(e) => {
                            const newBands = [...bands];
                            newBands[index] = {
                              ...newBands[index],
                              max: e.target.value,
                            };
                            updateNodeProperty(node.id, key, newBands);
                          }}
                          className="border rounded-lg px-3 py-2 text-xs w-full pr-8"
                          placeholder="Max"
                        />
                        <span className="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-500 text-xs">
                          Hz
                        </span>
                      </div>
                      {/* Remove Button */}
                      <button
                        onClick={(e) => {
                          e.stopPropagation(); // ✅ Prevents collapse
                          const newBands = bands.filter((_, i) => i !== index);
                          updateNodeProperty(node.id, key, newBands);
                        }}
                        className="text-red-500 text-xs font-bold hover:text-red-700"
                      >
                        ✕
                      </button>
                    </div>
                  ))}

                  <button
                    onClick={(e) => {
                      e.stopPropagation(); // ✅ Prevents collapse
                      updateNodeProperty(node.id, key, [
                        ...bands,
                        { min: "", max: "" },
                      ]);
                    }}
                    className="text-blue-500 text-xs font-semibold hover:text-blue-700"
                  >
                    + Add Range
                  </button>
                </div>
              );
            }

            /** ✅ Default Handling for Other Properties **/
            const newValue = isBoolean
              ? prop.value
              : validationRule?.type === "number" ||
                validationRule?.type === "integer"
              ? Number(prop.value) || 0
              : prop.value;

            const isInvalid =
              validationRule &&
              !validateProperty(key, newValue) &&
              newValue !== "";
            return (
              <div key={key} className="flex flex-col gap-1">
                {/* Label */}
                <label className="font-semibold text-xs text-gray-700">
                  {key}:
                </label>

                {/* Input Field with Unit Inside */}
                <div className="relative">
                  <input
                    type={isBoolean ? "checkbox" : "text"}
                    value={isBoolean ? undefined : newValue}
                    checked={isBoolean ? prop.value : undefined}
                    onChange={(e) => {
                      const newValue = isBoolean
                        ? e.target.checked
                        : validationRule?.type === "number" ||
                          validationRule?.type === "integer"
                        ? Number(e.target.value) || 0
                        : e.target.value;

                      if (validateProperty(key, newValue) || newValue === "") {
                        updateNodeProperty(node.id, key, newValue);
                      }
                    }}
                    onClick={(e) => e.stopPropagation()} // Prevents node collapse
                    className={`border rounded-lg px-3 py-2 text-xs w-full pr-8 focus:outline-none focus:ring-2 ${
                      isInvalid
                        ? "border-red-500 focus:ring-red-300"
                        : "border-gray-300 focus:ring-blue-300"
                    }`}
                  />
                  {/* Unit Display Inside Input */}
                  {validationRule?.unit && (
                    <span className="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-500 text-xs">
                      {validationRule.unit}
                    </span>
                  )}
                </div>

                {/* Error Message */}
                {isInvalid && (
                  <span className="text-red-500 text-xs">
                    {validationRule.errorMessage}
                  </span>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
