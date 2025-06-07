'use client'
import React, { useState, useEffect } from 'react';
import ImplementedPipelines from "../components/LibraryPage/ImplementedPipelines"
import SimulationSettings from "../components/LibraryPage/SimulationSettings"
import PipelineCreator from '../components/LibraryPage/PipelineCreator';
import Modules from '../components/LibraryPage/Modules';

export default function Home() {
  const [selectedPipelineId, setSelectedPipelineId] = useState(null);
  const [pipelineDataRefresh, setPipelineDataRefresh] = useState(0);

  const handleAnalysisComplete = () => {
    // Trigger refresh of pipeline data in ImplementedPipelines
    setPipelineDataRefresh(prev => prev + 1);
  };

  return (
    <div className="h-screen w-full overflow-hidden p-4 bg-gray-50 font-sans text-sm flex flex-col">
      <header className="flex justify-between items-start mb-4">
        <div>
          <h1 className="text-2xl font-bold italic mb-1">Foresee</h1>
          <p className="text-sm text-gray-600">
            Create, analyze, and visualize pipelines for novel BCIs with on-device processing.
          </p>
        </div>
      </header>

      {/* Main container that holds all sections */}
      <div className="flex flex-col flex-grow min-h-0">
        {/* Top Section: 5/8 height */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 h-5/8 min-h-0">
          <ImplementedPipelines 
            setSelectPipelineId={setSelectedPipelineId} 
            selectedPipelineId={selectedPipelineId}
            refreshTrigger={pipelineDataRefresh}
          />
          <SimulationSettings 
            selectedPipelineId={selectedPipelineId}
            onAnalysisComplete={handleAnalysisComplete}
          />
        </div>

        {/* Bottom Section: 3/8 height */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 h-3/8 min-h-0 mt-4">
          <PipelineCreator />
          <Modules />
        </div>
      </div>
    </div>
  );
}