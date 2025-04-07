"use client";

import { useState, useRef, useEffect, useCallback } from "react";
import { PROPERTY_VALIDATIONS, validateProperty } from "./validation";
import { GripVertical } from "lucide-react";

export function RightSidebar({ node, updateNodeProperty, onClose, saveData }) {
  if (!node) return null;

  const [width, setWidth] = useState(384); // 96 * 4 = Tailwind w-96
  const sidebarRef = useRef(null);
  const isResizing = useRef(false);
  const [localProperties, setLocalProperties] = useState({});
  const [isSaving, setIsSaving] = useState(false);
  const [saveError, setSaveError] = useState(null);

  useEffect(() => {
    if (node) {
      // Initialize local properties with the correct structure
      const initialProperties = {};
      Object.entries(node.properties || {}).forEach(([key, value]) => {
        initialProperties[key] = {
          value: value.value,
          type: value.type,
          unit: value.unit,
        };
      });
      setLocalProperties(initialProperties);
    }
  }, [node?.id]); // ✅ only reinitialize when the selected node changes

  const handleSave = async () => {
    if (!node) return;

    try {
      setIsSaving(true);

      // Update ALL properties, not just the first one
      for (const [key, prop] of Object.entries(localProperties)) {
        await updateNodeProperty(node.id, key, prop);
      }

      setIsSaving(false);
      onClose?.();
    } catch (error) {
      console.error("❌ Failed to save properties:", error);
      setSaveError("Failed to save properties");
      setIsSaving(false);
    }
  };

  // Handle RTL simulation/power estimation dependency
  useEffect(() => {
    if (localProperties["Enable RTL Simulation"]?.value === false) {
      setLocalProperties((prev) => ({
        ...prev,
        "Enable RTL Power Estimation": {
          ...prev["Enable RTL Power Estimation"],
          value: false,
        },
      }));
    }
  }, [localProperties["Enable RTL Simulation"]?.value]);

  useEffect(() => {
    const handleMouseMove = (e) => {
      if (isResizing.current) {
        const newWidth = window.innerWidth - e.clientX;
        setWidth(Math.min(Math.max(newWidth, 240), 640));
      }
    };

    const stopResizing = () => {
      isResizing.current = false;
      document.body.style.userSelect = ""; // ✅ re-enable text selection
    };

    window.addEventListener("mousemove", handleMouseMove);
    window.addEventListener("mouseup", stopResizing);

    return () => {
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("mouseup", stopResizing);
    };
  }, []);

  const { label, name } = node;
  const properties = node.properties || {};

  return (
    <>
      <div
        style={{ right: `${width}px` }}
        className="fixed top-0 z-50 h-full w-3 cursor-ew-resize"
        onMouseDown={(e) => {
          e.preventDefault();
          isResizing.current = true;
          document.body.style.userSelect = "none";
        }}
      >
        <div className="h-full flex items-center justify-center border-l border-gray-200 bg-white">
          <GripVertical className="w-4 h-4 text-gray-400" />
        </div>
      </div>
      <div
        ref={sidebarRef}
        style={{ width: `${width}px` }}
        className="fixed top-0 right-0 h-full bg-white border-l border-gray-200 shadow-lg overflow-hidden z-50 flex flex-col"
      >
        {/* Top toolbar row */}
        <div className="sticky top-0 z-10 bg-white flex justify-between items-center p-4 border-b border-gray-200">
          <div className="font-semibold text-lg text-gray-800">
            {label === "Storage" ? "Storage" : name || "Unnamed Node"}
          </div>

          <div className="flex gap-2">
            {saveData && (
              <button
                onClick={handleSave}
                disabled={isSaving}
                className={`px-2 py-1 text-white text-xs rounded transition-colors ${
                  isSaving
                    ? "bg-gray-400 cursor-not-allowed"
                    : "bg-blue-500 hover:bg-blue-600"
                }`}
              >
                {isSaving ? "Saving..." : "Save"}
              </button>
            )}

            <button
              onClick={onClose}
              className="text-gray-500 hover:text-black text-xs"
              title="Close sidebar"
            >
              ✕
            </button>
          </div>
        </div>

        {saveError && (
          <div className="p-2 bg-red-100 text-red-700 text-sm">{saveError}</div>
        )}

        <div className="relative p-4 overflow-y-auto flex-1">
          {/* Properties */}
          {localProperties && Object.keys(localProperties).length > 0 && (
            <div className="mt-4 space-y-4">
              {Object.entries(localProperties).map(([key, prop]) => {
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
                        onChange={(e) => {
                          const newVal = e.target.value;
                          setLocalProperties((prev) => ({
                            ...prev,
                            [key]: {
                              ...prev[key],
                              value: newVal,
                            },
                          }));
                        }}
                        className="border border-gray-300 rounded-lg px-3 py-2 text-xs bg-white focus:outline-none focus:ring-2 focus:ring-blue-300"
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
                  return (
                    <div key={key} className="flex flex-col gap-2">
                      <label className="font-semibold text-xs text-gray-700">
                        {key}:
                      </label>
                      <input
                        type="text"
                        value={prop.value || ""}
                        onChange={(e) => {
                          const newVal = e.target.value;
                          setLocalProperties((prev) => ({
                            ...prev,
                            [key]: {
                              ...prev[key],
                              value: newVal,
                            },
                          }));
                        }}
                        placeholder="e.g., 0.1-4, 4-8, 8-12"
                        className="border border-gray-300 rounded-lg px-3 py-2 text-xs bg-white focus:outline-none focus:ring-2 focus:ring-blue-300"
                      />
                    </div>
                  );
                }

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
                  <div key={key} className="flex items-center gap-2">
                    <label className="w-40 text-xs text-gray-700 font-semibold ">
                      {key}:
                    </label>
                    {isBoolean ? (
                      <input
                        type="checkbox"
                        checked={!!prop.value}
                        onChange={(e) => {
                          const newVal = e.target.checked;
                          setLocalProperties((prev) => ({
                            ...prev,
                            [key]: {
                              ...prev[key],
                              value: newVal,
                            },
                          }));
                        }}
                        onClick={(e) => e.stopPropagation()}
                        className="h-4 w-4"
                      />
                    ) : (
                      <div className="relative">
                        <input
                          type="text"
                          value={newValue ?? ""}
                          onChange={(e) => {
                            const val =
                              validationRule?.type === "number" ||
                              validationRule?.type === "integer"
                                ? Number(e.target.value)
                                : e.target.value;

                            if (validateProperty(key, val) || val === "") {
                              setLocalProperties((prev) => ({
                                ...prev,
                                [key]: {
                                  ...prev[key],
                                  value: val,
                                },
                              }));
                            }
                          }}
                          onClick={(e) => e.stopPropagation()}
                          className={`border rounded-lg px-3 py-2 text-xs w-full pr-8 focus:outline-none focus:ring-2 ${
                            isInvalid
                              ? "border-red-500 focus:ring-red-300"
                              : "border-gray-300 focus:ring-blue-300"
                          }`}
                        />
                        {validationRule?.unit && (
                          <span className="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-500 text-xs">
                            {validationRule.unit}
                          </span>
                        )}
                      </div>
                    )}

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
      </div>
    </>
  );
}
