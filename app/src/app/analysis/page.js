"use client";

import { useSearchParams } from "next/navigation";
import { useEffect, useState, Suspense } from "react";
import Canvas from "../../components/CreationPage/Canvas";
import NavBarAnalysis from "../../components/AnalysisPage/NavBarAnalysis";
import {
  BarChart,
  Bar,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";

// Real analysis results will be fetched from the Python backend (Flask)
// running in Electron. We therefore remove the dummy imports above.

// No global dummy metrics – metrics are computed dynamically once the
// backend responds with real results.

function AnalysisContent() {
  const searchParams = useSearchParams();
  const pipelineId = searchParams.get("id");
  const [pipeline, setPipeline] = useState(null);
  const [activeTab, setActiveTab] = useState("Summary");
  const [analysisResults, setAnalysisResults] = useState(null);
  const [comparisonResults, setComparisonResults] = useState(null);
  const [comparisonPipeline, setComparisonPipeline] = useState(null);
  const [availablePipelines, setAvailablePipelines] = useState([]);

  // Load pipeline(s) metadata from SQLite and get stored output data
  useEffect(() => {
    if (!pipelineId) return;

    // Fetch selected pipeline metadata and its stored output
    window.electronAPI.getPipelineById(pipelineId).then(async (data) => {
      setPipeline(data);

      // Get stored output data from database instead of running backend
      const outputData = await window.electronAPI.getPipelineOutput(pipelineId);
      if (outputData) {
        setAnalysisResults(outputData);
        console.log("✅ Loaded pipeline output from database:", outputData);
      } else {
        console.log("⚠️ No stored output data found for pipeline:", pipelineId);
      }
    });

    // Get all pipelines for comparison list
    window.electronAPI.getPipelines().then((pipelines) => {
      setAvailablePipelines(pipelines);
      if (pipelines.length > 0) {
        // default: first pipeline not equal to current maybe
        const defaultComparison = pipelines.find((p) => p.id !== parseInt(pipelineId));
        if (defaultComparison) setComparisonPipeline(defaultComparison);
      }
    });
  }, [pipelineId]);

  // When comparisonPipeline changes, fetch its stored results
  useEffect(() => {
    if (!comparisonPipeline) return;

    // Get stored output data for comparison pipeline
    window.electronAPI.getPipelineOutput(comparisonPipeline.id).then((outputData) => {
      if (outputData) {
        setComparisonResults(outputData);
        console.log("✅ Loaded comparison pipeline output from database:", outputData);
      } else {
        console.log("⚠️ No stored output data found for comparison pipeline:", comparisonPipeline.id);
      }
    });
  }, [comparisonPipeline]);

  // Helper function to transform module names for display
  const getDisplayName = (name) => {
    if (name === "Input PE") return "Input";
    return name;
  };

  // If backend has responded, transform results into chart-friendly arrays
  const powerData = analysisResults
    ? Object.entries(analysisResults.output_data)
        .filter(([id, data]) => id !== 'simulation_time' && data && typeof data === 'object' && data.name)
        .map(([id, data]) => ({
          name: getDisplayName(data.name),
          "Total Power": data.power_dict?.["Total Power"] ?? 0,
          "Internal Power": data.power_dict?.["Internal Power"] ?? 0,
          "Switching Power": data.power_dict?.["Switching Power"] ?? 0,
          "Leakage Power": data.power_dict?.["Leakage Power"] ?? 0,
        }))
    : [];

  const latencyData = analysisResults
    ? Object.entries(analysisResults.output_data)
        .filter(([id, data]) => id !== 'simulation_time' && data && typeof data === 'object' && data.name)
        .map(([id, data]) => ({
          name: getDisplayName(data.name),
          latency: data.latency ?? 0,
        }))
    : [];

  // Compute overall metrics for current and comparison pipelines
  const totalPowerCurrent = analysisResults
    ? Object.entries(analysisResults.output_data)
        .filter(([id, data]) => id !== 'simulation_time' && data && typeof data === 'object')
        .reduce((sum, [id, data]) => sum + (data.power_dict?.["Total Power"] ?? 0), 0)
    : 0;

  const totalLatencyCurrent = analysisResults
    ? Object.entries(analysisResults.output_data)
        .filter(([id, data]) => id !== 'simulation_time' && data && typeof data === 'object')
        .reduce((sum, [id, data]) => sum + (data.latency ?? 0), 0)
    : 0;

  const totalPowerComparison = comparisonResults
    ? Object.entries(comparisonResults.output_data)
        .filter(([id, data]) => id !== 'simulation_time' && data && typeof data === 'object')
        .reduce((sum, [id, data]) => sum + (data.power_dict?.["Total Power"] ?? 0), 0)
    : 0;

  const totalLatencyComparison = comparisonResults
    ? Object.entries(comparisonResults.output_data)
        .filter(([id, data]) => id !== 'simulation_time' && data && typeof data === 'object')
        .reduce((sum, [id, data]) => sum + (data.latency ?? 0), 0)
    : 0;

  // Metrics to display in the summary cards
  const pipelineMetrics = {
    Power: analysisResults ? `${totalPowerCurrent.toFixed(6)} mW` : "--",
    Latency: analysisResults ? `${totalLatencyCurrent.toFixed(2)} ns` : "--",
    Accuracy: analysisResults && analysisResults.accuracy
      ? `${(analysisResults.accuracy.accuracy * 100).toFixed(2)} %`
      : "-- %",
    "Simulation Time": analysisResults && analysisResults.simulation_time 
      ? `${analysisResults.simulation_time.toFixed(3)} s` 
      : "-- s",
  };

  // Data for comparison charts (current vs selected comparison pipeline)
  const comparisonData = {
    power: [
      {
        name: pipeline?.name || "Current Pipeline",
        "Total Power": parseFloat(totalPowerCurrent.toFixed(6)),
      },
      {
        name: comparisonPipeline?.name || "Comparison Pipeline",
        "Total Power": parseFloat(totalPowerComparison.toFixed(6)),
      },
    ],
    latency: [
      {
        name: pipeline?.name || "Current Pipeline",
        "Total Latency": parseFloat(totalLatencyCurrent.toFixed(2)),
      },
      {
        name: comparisonPipeline?.name || "Comparison Pipeline",
        "Total Latency": parseFloat(totalLatencyComparison.toFixed(2)),
      },
    ],
    accuracy: [
      {
        name: pipeline?.name || "Current Pipeline",
        Accuracy: analysisResults && analysisResults.accuracy
          ? (analysisResults.accuracy.accuracy * 100)
          : 0,
      },
      {
        name: comparisonPipeline?.name || "Comparison Pipeline",
        Accuracy: comparisonResults && comparisonResults.accuracy
          ? (comparisonResults.accuracy.accuracy * 100)
          : 0,
      },
    ],
  };

  const tabs = ["Summary", "Comparison"];

  const handleComparisonChange = (e) => {
    const selectedPipeline = availablePipelines.find(
      (p) => p.id === parseInt(e.target.value)
    );
    setComparisonPipeline(selectedPipeline);
  };

  return (
    <div className="flex flex-col h-full w-full bg-gray-50">
      <NavBarAnalysis pipelineName={pipeline?.name} />
      <div className="flex-grow flex flex-col px-6">
        {/* Canvas */}
        <div className="h-[25vh] border border-gray-200 rounded-lg overflow-hidden my-4 shadow-sm bg-white flex items-center justify-center">
          {pipeline ? (
            <Canvas
              graphData={JSON.parse(pipeline.graph_structure)}
              pipelineId={pipelineId}
              pipelineName={pipeline.name}
              pipelineDescription={pipeline.description}
              readOnly={true}
              autoFit={true}
              fitView={true}
              fitViewOptions={{ 
                padding: 0.2,
                includeHiddenNodes: true,
              }}
              style={{ width: '100%', height: '100%' }}
            />
          ) : (
            <p className="p-4">Loading pipeline...</p>
          )}
        </div>

        {/* Metric Cards */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          {Object.entries(pipelineMetrics).map(([key, val]) => (
            <div key={key} className="bg-white rounded-lg shadow p-4 text-center">
              <p className="text-sm text-gray-500 uppercase tracking-wider">
                {key}
              </p>
              <p className="text-lg font-bold text-gray-900">{val}</p>
            </div>
          ))}
        </div>

        {/* Performance Breakdown */}
        <div className="bg-white rounded-lg shadow p-6 mb-12">
          {/* Tabs */}
          <div className="flex space-x-4 border-b mb-6">
            {tabs.map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`pb-2 text-sm font-semibold ${
                  activeTab === tab
                    ? "border-b-2 border-red-500 text-red-600"
                    : "text-gray-500 hover:text-gray-700"
                }`}
              >
                {tab}
              </button>
            ))}
          </div>

          {/* Tab Content */}
          <div className="grid grid-cols-1 gap-6">
            {activeTab === "Summary" && (
              <div className="grid grid-cols-2 gap-6">
                <ChartCard title="Power by Module (mW)">
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={powerData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="name" />
                      <YAxis />
                      <Tooltip />
                      <Legend />
                      <Bar dataKey="Internal Power" stackId="power" fill="#82ca9d" />
                      <Bar dataKey="Switching Power" stackId="power" fill="#ffc658" />
                      <Bar dataKey="Leakage Power" stackId="power" fill="#ff8042" />
                    </BarChart>
                  </ResponsiveContainer>
                </ChartCard>
                <ChartCard title="Latency by Module (ns)">
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={latencyData}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="name" />
                      <YAxis />
                      <Tooltip />
                      <Legend />
                      <Bar dataKey="latency" fill="#8884d8" />
                    </BarChart>
                  </ResponsiveContainer>
                </ChartCard>
              </div>
            )}

            {activeTab === "Comparison" && (
              <>
                {/* Pipeline Selection */}
                <div className="mb-6">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Compare with:
                  </label>
                  <select
                    className="block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-red-500 focus:border-red-500"
                    value={comparisonPipeline?.id}
                    onChange={handleComparisonChange}
                  >
                    {availablePipelines.map((p) => (
                      <option key={p.id} value={p.id}>
                        {p.name}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Comparison Charts */}
                <div className="grid grid-cols-3 gap-4">
                  <ChartCard title="Total Power (mW)">
                    <div className="w-full">
                      <ResponsiveContainer width="100%" height={250}>
                        <BarChart data={comparisonData.power}>
                          <CartesianGrid strokeDasharray="3 3" />
                          <XAxis dataKey="name" />
                          <YAxis />
                          <Tooltip />
                          <Legend />
                          <Bar dataKey="Total Power" fill="#8884d8" />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </ChartCard>

                  <ChartCard title="Total Latency (ns)">
                    <div className="w-full">
                      <ResponsiveContainer width="100%" height={250}>
                        <BarChart data={comparisonData.latency}>
                          <CartesianGrid strokeDasharray="3 3" />
                          <XAxis dataKey="name" />
                          <YAxis />
                          <Tooltip />
                          <Legend />
                          <Bar dataKey="Total Latency" fill="#82ca9d" />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </ChartCard>

                  <ChartCard title="Prediction Accuracy (%)">
                    <div className="w-full">
                      <ResponsiveContainer width="100%" height={250}>
                        <BarChart data={comparisonData.accuracy}>
                          <CartesianGrid strokeDasharray="3 3" />
                          <XAxis dataKey="name" />
                          <YAxis domain={[0, 100]} />
                          <Tooltip />
                          <Legend />
                          <Bar dataKey="Accuracy" fill="#ffc658" />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </ChartCard>
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

// 📦 Reusable chart wrapper
function ChartCard({ title, children }) {
  return (
    <div className="bg-gray-50 p-4 rounded-lg shadow-inner">
      <h3 className="font-semibold text-gray-700 mb-2">{title}</h3>
      {children}
    </div>
  );
}

// Exported page component – wraps main content in a Suspense fallback like other pages
const AnalysisPage = () => {
  return (
    <Suspense fallback={<div className="p-6">Loading...</div>}>
      <AnalysisContent />
    </Suspense>
  );
};

export default AnalysisPage;
