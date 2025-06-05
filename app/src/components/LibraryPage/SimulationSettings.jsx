"use client";
import React, { useState } from "react";
import { SettingsIcon } from "../Icons/icons";

export default function SimulationSettings({ selectedPipelineId }) {
  const [selectedOptions, setSelectedOptions] = useState({
    mainAccuracy: true,
    hardwareAccuracy: true,
    latency: true,
    power: true,
  });
  const [runs, setRuns] = useState(1);
  const [progress, setProgress] = useState(100);

  const toggleOption = (option) => {
    setSelectedOptions((prev) => ({
      ...prev,
      [option]: !prev[option],
    }));
  };

  const toggleHardwareAnalysis = () => {
    const currentState = Object.values({
      hardwareAccuracy: selectedOptions.hardwareAccuracy,
      latency: selectedOptions.latency,
      power: selectedOptions.power,
    }).some((value) => value);
    setSelectedOptions((prev) => ({
      ...prev,
      hardwareAccuracy: !currentState,
      latency: !currentState,
      power: !currentState,
    }));
  };

  const isHardwareAnalysisEnabled = () => {
    return (
      selectedOptions.hardwareAccuracy ||
      selectedOptions.latency ||
      selectedOptions.power
    );
  };

  const handleAnalyze = async () => {
    if (!selectedPipelineId) {
      console.log("No pipeline selected");
      return;
    }

    try {
      const pipeline = await window.electronAPI.getPipelineById(
        selectedPipelineId
      );
      if (!pipeline) {
        console.warn("Pipeline not found.");
        return;
      }

      const graphData =
        typeof pipeline.graph_structure === "string"
          ? JSON.parse(pipeline.graph_structure)
          : pipeline.graph_structure;

      const parsedGraphData =
        typeof graphData === "string" ? JSON.parse(graphData) : graphData;

      // Validate the pipeline structure
      if (!parsedGraphData.nodes || !parsedGraphData.edges) {
        console.error("Invalid pipeline structure: missing nodes or edges");
        return;
      }

      // Ensure each node has the required fields
      for (const node of parsedGraphData.nodes) {
        if (!node.id || !node.nodeType) {
          console.error("Invalid node structure: missing id or nodeType", node);
          return;
        }
      }

      // Ensure each edge has the required fields
      for (const edge of parsedGraphData.edges) {
        if (!edge.source || !edge.target) {
          console.error(
            "Invalid edge structure: missing source or target",
            edge
          );
          return;
        }
      }

      // console.log("📦 Sending to backend:", parsedGraphData);
      const response = await fetch("http://localhost:5001/run-pipeline", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        mode: "cors",
        credentials: "same-origin",
        body: JSON.stringify(parsedGraphData),
      });

      const result = await response.json();
      console.log("🧠 Flask pipeline result:", result);

      // Save the output data to the pipeline_output table
      if (result.output_data) {
        await window.electronAPI.savePipelineOutput(selectedPipelineId, result.output_data);
        console.log("✅ Pipeline output saved to database");
      }

      
    } catch (error) {
      console.error("❌ Error analyzing pipeline:", error);
    }
  };

  return (
    <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-300 flex flex-col flex-grow">
      {/* Header */}
      <div className="flex items-center mb-4">
        <div className="bg-orange-100 p-2 rounded-full">
          <SettingsIcon className="text-orange-500" />
        </div>
        <h2 className="text-lg font-semibold ml-3">Analysis Settings</h2>
      </div>

      {/* Options */}
      <div className="flex flex-col space-y-6">
        {/* Main Accuracy */}
        <div className="flex items-center justify-between w-full bg-gray-50 p-3 rounded-lg border border-gray-200">
          <div
            className="flex-1 px-3 py-1 mr-4 text-left border border-gray-300 rounded-md shadow-sm bg-white text-sm font-medium cursor-pointer hover:bg-gray-50 transition-colors"
            onClick={() => toggleOption("mainAccuracy")}
          >
            Accuracy
          </div>
          <div className="w-12 flex justify-center">
            <input
              type="checkbox"
              checked={selectedOptions.mainAccuracy}
              onChange={() => toggleOption("mainAccuracy")}
              className="h-5 w-5 border-gray-400 rounded-md focus:ring-0 checked:bg-red-600 checked:border-red-600 accent-red-500"
            />
          </div>
        </div>

        {/* Hardware Analysis Parent */}
        <div className="flex items-center justify-between w-full bg-gray-50 p-3 rounded-lg border border-gray-200">
          <div
            className="flex-1 px-3 py-1 mr-4 text-left border border-gray-300 rounded-md shadow-sm bg-white text-sm font-medium cursor-pointer hover:bg-gray-50 transition-colors"
            onClick={toggleHardwareAnalysis}
          >
            Hardware Analysis
          </div>
          <div className="w-12 flex justify-center">
            <input
              type="checkbox"
              checked={isHardwareAnalysisEnabled()}
              onChange={toggleHardwareAnalysis}
              className="h-5 w-5 border-gray-400 rounded-md focus:ring-0 checked:bg-red-600 checked:border-red-600 accent-red-500"
            />
          </div>
        </div>

        {/* Nested Hardware Options */}
        <div className="ml-6 flex flex-col space-y-3 border-l-2 border-gray-200 pl-6">
          {[
            { label: "Accuracy", key: "hardwareAccuracy" },
            { label: "Latency", key: "latency" },
            { label: "Power", key: "power" },
          ].map(({ label, key }) => (
            <div key={key} className="flex items-center justify-between w-full">
              <div
                className="flex-1 px-3 py-1 mr-4 text-left border border-gray-300 rounded-md shadow-sm bg-white text-sm font-medium cursor-pointer hover:bg-gray-50 transition-colors"
                onClick={() => toggleOption(key)}
              >
                {label}
              </div>
              <div className="w-18 flex justify-center">
                <input
                  type="checkbox"
                  checked={selectedOptions[key]}
                  onChange={() => toggleOption(key)}
                  className="h-5 w-5 border-gray-400 rounded-md focus:ring-0 checked:bg-red-600 checked:border-red-600 accent-red-500"
                />
              </div>
            </div>
          ))}
        </div>

        {/* Runs Input */}
        <div className="flex items-center justify-between w-full bg-gray-50 p-3 rounded-lg border border-gray-200">
          <div className="flex-1 px-3 py-1 mr-4 text-left border border-gray-300 rounded-md shadow-sm bg-white text-sm font-medium">
            Runs
          </div>
          <div className="w-12 flex justify-center">
            <input
              type="number"
              value={runs}
              onChange={(e) => setRuns(parseInt(e.target.value, 10))}
              className="h-8 w-12 text-center border border-gray-300 rounded-md p-1 text-sm focus:ring-1 focus:ring-red-500 focus:border-red-500"
            />
          </div>
        </div>
      </div>

      {/* Analyze */}
      <div className="mt-auto pt-6">
        <button
          onClick={handleAnalyze}
          className="w-full bg-red-600 text-white py-3 rounded-md shadow-md font-semibold hover:bg-red-700 transition-colors"
        >
          Analyze
        </button>
        <div className="flex items-center mt-3 space-x-2">
          <div className="bg-red-600 h-2 w-full rounded-full"></div>
          <span className="text-sm font-medium">{progress}%</span>
        </div>
      </div>
    </div>
  );
}
