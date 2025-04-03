import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { ImplementedPipelinesIcon, EditIcon, ChartIcon, DeleteIcon } from "../Icons/icons";

export default function ImplementedPipelines() {
  const [pipelines, setPipelines] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [filteredPipelines, setFilteredPipelines] = useState([]);

  // Fetch pipelines from SQLite via Electron's IPC
  useEffect(() => {
    window.electronAPI.getPipelines().then((data) => {
      const formattedPipelines = data.map((pipeline) => ({
        id: pipeline.id,
        title: pipeline.name,
        description: pipeline.description,
        icon: "/icons/pipeline.png",
        selected: false,
      }));
      setPipelines(formattedPipelines);
      setFilteredPipelines(formattedPipelines);
    });
  }, []);

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
    console.log(id);
    const updatedPipelines = pipelines.map((pipeline) =>
      pipeline.id === id
        ? { ...pipeline, selected: !pipeline.selected }
        : pipeline
    );

    setPipelines(updatedPipelines);

    // Ensure filteredPipelines is updated as well
    setFilteredPipelines(
      updatedPipelines.filter((pipeline) =>
        pipeline.title.toLowerCase().includes(searchQuery)
      )
    );
  };

  const router = useRouter();

  const handleEditClick = (pipelineId) => {
    router.push(`/creation?id=${pipelineId}`);
  };

  const handleChartClick = (pipelineId) => {
    router.push(`/analysis?id=${pipelineId}`);
  }

  return (
    <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-300 flex flex-col flex-grow min-h-0 overflow-hidden col-span-2">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center">
          <ImplementedPipelinesIcon />
          <h2 className="text-lg font-semibold ml-3">Implemented Pipelines</h2>
        </div>
        <input
          type="text"
          placeholder="Search pipelines..."
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
                checked={pipeline.selected}
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
                  <div className="mr-4" onClick={() => handleChartClick(pipeline.id)}>
                    <ChartIcon />
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
