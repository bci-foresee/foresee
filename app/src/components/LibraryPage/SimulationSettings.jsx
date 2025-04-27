'use client'
import React, { useState } from 'react';
import { SettingsIcon } from '../Icons/icons';

export default function SimulationSettings({ selectedPipelineId }) {
  const [selectedOptions, setSelectedOptions] = useState({
    power: true,
    latency: true,
    accuracy: true,
    storage: true,
  });
  const [runs, setRuns] = useState(1);
  const [progress, setProgress] = useState(100);

  const toggleOption = (option) => {
    setSelectedOptions((prev) => ({
      ...prev,
      [option]: !prev[option],
    }));
  };

const handleAnalyze = async () => {
  if (!selectedPipelineId) {
    console.log("No pipeline selected");
    return;
  }

  try {
    const pipeline = await window.electronAPI.getPipelineById(selectedPipelineId);
    if (!pipeline) {
      console.warn("Pipeline not found.");
      return;
    }

    const graphData = typeof pipeline.graph_structure === 'string'
      ? JSON.parse(pipeline.graph_structure)
      : pipeline.graph_structure;
    
    const parsedGraphData = typeof graphData === 'string'
      ? JSON.parse(graphData)
      : graphData;
      
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
          console.error("Invalid edge structure: missing source or target", edge);
          return;
        }
      }
  
      console.log("📦 Sending to backend:", parsedGraphData);
      const response = await fetch('http://localhost:5001/run-pipeline', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        mode: 'cors',
        credentials: 'same-origin',
        body: JSON.stringify(parsedGraphData),
    });
  
    const result = await response.json();
    console.log("🧠 Flask pipeline result:", result);
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
        <h2 className="text-lg font-semibold ml-3">Simulation Settings</h2>
      </div>

      {/* Options */}
      <div className="flex flex-col space-y-5">
        {["Power", "Latency", "Accuracy", "Storage"].map((option) => (
          <div key={option} className="flex items-center justify-between w-full">
            <div
              className="px-3 py-1 w-24 text-center border border-gray-300 rounded-md shadow-sm bg-white text-sm font-medium"
              onClick={() => toggleOption(option.toLowerCase())}
            >
              {option}
            </div>
            <input
              type="checkbox"
              checked={selectedOptions[option.toLowerCase()]}
              onChange={() => toggleOption(option.toLowerCase())}
              className="h-6 w-6 border-gray-400 rounded-md focus:ring-0 checked:bg-red-600 checked:border-red-600 accent-red-500"
            />
          </div>
        ))}

        {/* Runs Input */}
        <div className="flex items-center justify-between w-full">
          <div className="px-3 py-1 w-24 text-center border border-gray-300 rounded-md shadow-sm bg-white text-sm font-medium">
            Runs
          </div>
          <input
            type="number"
            value={runs}
            onChange={(e) => setRuns(parseInt(e.target.value, 10))}
            className="h-6 w-12 text-center border border-gray-300 rounded-md p-1 text-sm"
          />
        </div>
      </div>

      {/* Analyze */}
      <div className="mt-auto pt-4">
        <button
          onClick={handleAnalyze}
          className="w-full bg-red-600 text-white py-2 rounded-md shadow-md font-semibold hover:bg-red-700 transition"
        >
          Analyze
        </button>
        <div className="flex items-center mt-2 space-x-2">
          <div className="bg-red-600 h-2 w-full rounded-full"></div>
          <span className="text-sm font-medium">{progress}%</span>
        </div>
      </div>
    </div>
  );
}
