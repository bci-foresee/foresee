'use client';
import React, { useState, useEffect, useRef } from "react";
import { useRouter } from "next/navigation";
import {
  ImplementedPipelinesIcon,
  EditIcon,
  ChartIcon,
  DeleteIcon,
} from "../Icons/icons";

export default function ImplementedPipelines({ selectedPipelineId, setSelectPipelineId, refreshTrigger, onAnalysisComplete }) {
  const [pipelines, setPipelines] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [filteredPipelines, setFilteredPipelines] = useState([]);
  const [pipelinesWithData, setPipelinesWithData] = useState(new Set());
  
  // Analysis settings state (moved from SimulationSettings)
  const [selectedOptions, setSelectedOptions] = useState({
    accuracy: true,
    hardwareAnalysis: true,
  });
  const [isLoading, setIsLoading] = useState(false);
  const [errorModal, setErrorModal] = useState({ show: false, message: "" });
  const abortControllerRef = useRef(null);

  // Function to fetch pipeline outputs and update pipelinesWithData
  const refreshPipelineData = async () => {
    if (typeof window !== 'undefined' && window?.electronAPI?.getPipelineOutputs) {
      try {
        const outputs = await window.electronAPI.getPipelineOutputs();
        const pipelineIdsWithData = new Set(outputs.map(output => output.pipeline_id));
        setPipelinesWithData(pipelineIdsWithData);
      } catch (err) {
        console.error("Failed to load pipeline outputs:", err);
        setPipelinesWithData(new Set());
      }
    } else {
      console.warn("getPipelineOutputs API unavailable");
      setPipelinesWithData(new Set());
    }
  };

  // Fetch pipelines from SQLite via Electron's IPC – guard for non-Electron environments
  useEffect(() => {
    const fetchPipelines = async () => {
      if (typeof window !== 'undefined' && window?.electronAPI?.getPipelines) {
        try {
          const data = await window.electronAPI.getPipelines();
          const formattedPipelines = data.map((pipeline) => ({
            id: pipeline.id,
            title: pipeline.name,
            description: pipeline.description,
            icon: "/icons/pipeline.png",
          }));
          setPipelines(formattedPipelines);
          setFilteredPipelines(formattedPipelines);

          // Initial load of pipeline outputs
          await refreshPipelineData();
        } catch (err) {
          console.error("Failed to load pipelines via Electron IPC:", err);
        }
      } else {
        // Running outside of Electron (e.g. Next.js dev in browser). Avoid hard-crash by using empty list.
        console.warn("Electron API unavailable – skipping pipeline fetch.");
        setPipelines([]);
        setFilteredPipelines([]);
        setPipelinesWithData(new Set());
      }
    };

    fetchPipelines();
  }, []);

  // Refresh pipeline data when refreshTrigger changes
  useEffect(() => {
    if (refreshTrigger > 0) {
      refreshPipelineData();
    }
  }, [refreshTrigger]);

  // Search function
  const handleSearchChange = (event) => {
    const query = event.target.value.toLowerCase();
    setSearchQuery(query);

    const filtered = pipelines.filter((pipeline) =>
      pipeline.title.toLowerCase().includes(query)
    );
    setFilteredPipelines(filtered);
  };

  // Function to toggle selection state
  const handleCheckboxChange = (id) => {
    if (selectedPipelineId === id) {
      setSelectPipelineId(null);
    } else {
      setSelectPipelineId(id);
    }
  };

  // Analysis settings functions (moved from SimulationSettings)
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

  const router = useRouter();

  const handleEditClick = (pipelineId) => {
    router.push(`/creation?id=${pipelineId}`);
  };

  const handleChartClick = (pipelineId) => {
    router.push(`/analysis?id=${pipelineId}`);
  };

  return (
    <>
      <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-300 flex flex-col flex-grow min-h-0 overflow-hidden">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center">
            <ImplementedPipelinesIcon />
            <h2 className="text-lg font-semibold ml-3">Implemented Pipelines</h2>
          </div>
          <input
            type="text"
            placeholder="Search..."
            value={searchQuery}
            onChange={handleSearchChange}
            className="border border-gray-300 p-1 text-sm rounded-md w-48 pl-2"
          />
        </div>

        {/* List of Pipelines - Prevents overflow */}
        <div className="flex-grow overflow-auto min-h-0 mb-4">
          {filteredPipelines.length > 0 ? (
            filteredPipelines.map((pipeline) => (
              <div key={pipeline.id} className="flex items-center mb-4">
                {" "}
                {/* Added mb-4 for spacing */}
                <input
                  type="checkbox"
                  checked={pipeline.id === selectedPipelineId}
                  onChange={() => handleCheckboxChange(pipeline.id)}
                  className="mr-3 accent-red-500 h-6 w-6 cursor-pointer"
                />
                <div
                  className="flex-1 p-4 border border-gray-300 rounded-lg shadow-sm transition hover:border-red-500"
                  onClick={() => handleCheckboxChange(pipeline.id)}
                >
                  <div className="flex items-start">
                    <img
                      src={pipeline.icon}
                      alt={pipeline.title}
                      className="h-7 w-7 mr-5 mt-1"
                    />
                    <div>
                      <div className="font-semibold text-base">
                        {pipeline.title}
                      </div>
                      <p className="text-sm text-gray-600 mt-1">
                        {pipeline.description}
                      </p>
                    </div>
                  </div>
                  <div className="flex justify-end text-xs text-gray-500 mt-2">
                    <div
                      className="mr-4"
                      title="Results"
                      onClick={() => {
                        if (pipelinesWithData.has(pipeline.id)) {
                          handleChartClick(pipeline.id);
                        }
                      }}
                    >
                      <ChartIcon disabled={!pipelinesWithData.has(pipeline.id)} />
                    </div>
                    <button title="Edit" onClick={() => handleEditClick(pipeline.id)}>
                      <EditIcon />
                    </button>
                  </div>
                </div>
              </div>
            ))
          ) : (
            <div className="flex items-center justify-center h-full text-gray-500 text-sm">
              <p className="text-gray-500 text-lg text-center mb-15">
                No pipelines found.
              </p>
            </div>
          )}
        </div>

        {/* Analysis Settings - Right-aligned at bottom */}
        <div className="border-t border-gray-200 pt-4 mt-auto">
          <div className="flex justify-end">
            <div className="flex items-center space-x-6">
              {/* Accuracy Checkbox */}
              <div className="flex items-center space-x-2">
                <label className="text-sm font-medium text-gray-700 cursor-pointer" onClick={() => toggleOption("accuracy")}>
                  Accuracy
                </label>
                <input
                  type="checkbox"
                  checked={selectedOptions.accuracy}
                  onChange={() => toggleOption("accuracy")}
                  className="h-4 w-4 border-gray-400 rounded focus:ring-0 checked:bg-red-600 checked:border-red-600 accent-red-500"
                />
              </div>

              {/* Hardware Analysis Checkbox */}
              <div className="flex items-center space-x-2">
                <label className="text-sm font-medium text-gray-700 cursor-pointer" onClick={() => toggleOption("hardwareAnalysis")}>
                  Hardware Analysis
                </label>
                <input
                  type="checkbox"
                  checked={selectedOptions.hardwareAnalysis}
                  onChange={() => toggleOption("hardwareAnalysis")}
                  className="h-4 w-4 border-gray-400 rounded focus:ring-0 checked:bg-red-600 checked:border-red-600 accent-red-500"
                />
              </div>

              {/* Analyze Button */}
              <div className="flex gap-2">
                <button
                  onClick={handleAnalyze}
                  disabled={isLoading || !selectedPipelineId}
                  className="bg-red-600 text-white px-6 py-2 rounded-md shadow-md font-semibold hover:bg-red-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
                >
                  {isLoading ? (
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  ) : (
                    "Analyze"
                  )}
                </button>
                
                {isLoading && (
                  <button
                    onClick={handleAbort}
                    className="px-3 py-2 bg-gray-600 text-white rounded-md shadow-md font-semibold hover:bg-gray-700 transition-colors flex items-center justify-center"
                    title="Stop analysis"
                  >
                    ✕
                  </button>
                )}
              </div>
            </div>
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
