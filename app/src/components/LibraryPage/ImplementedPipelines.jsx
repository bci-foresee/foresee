'use client';
import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import {
  ImplementedPipelinesIcon,
  EditIcon,
  ChartIcon,
  DeleteIcon,
} from "../Icons/icons";

export default function ImplementedPipelines({ selectedPipelineId, setSelectPipelineId, refreshTrigger }) {
  const [pipelines, setPipelines] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [filteredPipelines, setFilteredPipelines] = useState([]);
  const [pipelinesWithData, setPipelinesWithData] = useState(new Set());

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

  const router = useRouter();

  const handleEditClick = (pipelineId) => {
    router.push(`/creation?id=${pipelineId}`);
  };

  const handleChartClick = (pipelineId) => {
    router.push(`/analysis?id=${pipelineId}`);
  };

  return (
    <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-300 flex flex-col flex-grow min-h-0 overflow-hidden col-span-2">
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
      <div className="flex-grow overflow-auto min-h-0">
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
                    onClick={() => {
                      if (pipelinesWithData.has(pipeline.id)) {
                        handleChartClick(pipeline.id);
                      }
                    }}
                  >
                    <ChartIcon disabled={!pipelinesWithData.has(pipeline.id)} />
                  </div>
                  <button onClick={() => handleEditClick(pipeline.id)}>
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
    </div>
  );
}
