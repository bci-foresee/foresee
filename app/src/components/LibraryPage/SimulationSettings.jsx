"use client";
import React, { useState, useRef } from "react";
import { SettingsIcon } from "../Icons/icons";

export default function SimulationSettings({ selectedPipelineId, onAnalysisComplete }) {
  const [selectedOptions, setSelectedOptions] = useState({
    accuracy: true,
    hardwareAnalysis: true,
  });
  const [isLoading, setIsLoading] = useState(false);
  const [errorModal, setErrorModal] = useState({ show: false, message: "" });
  const abortControllerRef = useRef(null);

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

    setIsLoading(true);

    // Create new AbortController for this request
    const abortController = new AbortController();
    abortControllerRef.current = abortController;

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

      // Record start time for API response timing
      const startTime = performance.now();

      // Prepare the request payload with analysis settings
      const requestPayload = {
        ...parsedGraphData,
        analysis_settings: {
          run_accuracy: selectedOptions.accuracy,
          run_power_latency: selectedOptions.hardwareAnalysis,
        }
      };

      // console.log("📦 Sending to backend:", requestPayload);
      const response = await fetch("http://localhost:5001/run-pipeline", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        mode: "cors",
        credentials: "same-origin",
        body: JSON.stringify(requestPayload),
        signal: abortController.signal, // Add abort signal to fetch
      });

      const result = await response.json();
      
      // Check if the API returned an error
      if (result.error) {
        setErrorModal({
          show: true,
          message: result.error
        });
        return;
      }
      
      // Record end time and calculate duration
      const endTime = performance.now();
      const simulationTime = (endTime - startTime) / 1000; // Convert to seconds
      
      console.log("🧠 Flask pipeline result:", result);
      console.log(`⏱️ API response time: ${simulationTime.toFixed(3)} seconds`);

      // Save the complete result to the pipeline_output table
      if (result) {
        // Add timing information to the result
        const completeResult = {
          ...result,
          simulation_time: simulationTime
        };
        
        await window.electronAPI.savePipelineOutput(selectedPipelineId, completeResult);
        console.log("✅ Complete pipeline result saved to database");
        
        // Notify parent that analysis completed successfully
        if (onAnalysisComplete) {
          onAnalysisComplete();
        }
      }

      
    } catch (error) {
      if (error.name === 'AbortError') {
        console.log("🛑 Analysis was aborted by user");
      } else {
        console.error("❌ Error analyzing pipeline:", error);
        setErrorModal({
          show: true,
          message: `Network error: ${error.message}`
        });
      }
    } finally {
      setIsLoading(false);
      abortControllerRef.current = null;
    }
  };

  const handleAbort = () => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      console.log("🛑 Aborting analysis...");
    }
  };

  const closeErrorModal = () => {
    setErrorModal({ show: false, message: "" });
  };

  return (
    <>
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
          {/* Accuracy */}
          <div className="flex items-center justify-between w-full bg-gray-50 p-3 rounded-lg border border-gray-200">
            <div
              className="flex-1 px-3 py-1 mr-4 text-left border border-gray-300 rounded-md shadow-sm bg-white text-sm font-medium cursor-pointer hover:bg-gray-50 transition-colors"
              onClick={() => toggleOption("accuracy")}
            >
              Accuracy
            </div>
            <div className="w-12 flex justify-center">
              <input
                type="checkbox"
                checked={selectedOptions.accuracy}
                onChange={() => toggleOption("accuracy")}
                className="h-5 w-5 border-gray-400 rounded-md focus:ring-0 checked:bg-red-600 checked:border-red-600 accent-red-500"
              />
            </div>
          </div>

          {/* Hardware Analysis */}
          <div className="flex items-center justify-between w-full bg-gray-50 p-3 rounded-lg border border-gray-200">
            <div
              className="flex-1 px-3 py-1 mr-4 text-left border border-gray-300 rounded-md shadow-sm bg-white text-sm font-medium cursor-pointer hover:bg-gray-50 transition-colors"
              onClick={() => toggleOption("hardwareAnalysis")}
            >
              Hardware Analysis
            </div>
            <div className="w-12 flex justify-center">
              <input
                type="checkbox"
                checked={selectedOptions.hardwareAnalysis}
                onChange={() => toggleOption("hardwareAnalysis")}
                className="h-5 w-5 border-gray-400 rounded-md focus:ring-0 checked:bg-red-600 checked:border-red-600 accent-red-500"
              />
            </div>
          </div>
        </div>

        {/* Analyze */}
        <div className="mt-auto pt-6">
          <div className="flex gap-2">
            <button
              onClick={handleAnalyze}
              disabled={isLoading}
              className="flex-1 bg-red-600 text-white py-3 rounded-md shadow-md font-semibold hover:bg-red-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
            >
              {isLoading ? (
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              ) : (
                "Analyze"
              )}
            </button>
            
            {isLoading && (
              <button
                onClick={handleAbort}
                className="px-4 py-3 bg-gray-600 text-white rounded-md shadow-md font-semibold hover:bg-gray-700 transition-colors flex items-center justify-center"
                title="Stop analysis"
              >
                ✕
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Error Modal */}
      {errorModal.show && (
        <div className="fixed inset-0 backdrop-blur-sm flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4 shadow-2xl border border-gray-200">
            <div className="flex items-center mb-4">
              <div className="bg-red-100 p-2 rounded-full mr-3">
                <svg className="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold text-gray-900">Analysis Error</h3>
            </div>
            
            <div className="mb-6">
              <p className="text-gray-700 leading-relaxed">
                {errorModal.message}
              </p>
            </div>
            
            <div className="flex justify-end">
              <button
                onClick={closeErrorModal}
                className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors font-medium"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
