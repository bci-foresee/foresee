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

  // Load pipeline(s) metadata from SQLite and trigger backend runs
  useEffect(() => {
    if (!pipelineId) return;

    // Fetch selected pipeline metadata
    window.electronAPI.getPipelineById(pipelineId).then((data) => {
      setPipeline(data);

      // Once we have pipeline and its graph structure, request analysis
      if (data?.graph_structure) {
        // Parse text JSON into object before sending to backend
        const graphObj = typeof data.graph_structure === "string" ? JSON.parse(data.graph_structure) : data.graph_structure;
        runBackendPipeline(graphObj).then((res) => {
          setAnalysisResults(res);
        });
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

  // When comparisonPipeline changes, fetch its results
  useEffect(() => {
    if (!comparisonPipeline || !comparisonPipeline.graph_structure) return;

    const compGraph = typeof comparisonPipeline.graph_structure === "string" ? JSON.parse(comparisonPipeline.graph_structure) : comparisonPipeline.graph_structure;

    runBackendPipeline(compGraph).then((res) => {
      setComparisonResults(res);
    });
  }, [comparisonPipeline]);

  // Helper to call Flask backend via fetch
  const runBackendPipeline = async (graphStructure) => {
    try {
      const response = await fetch("http://localhost:5001/run-pipeline", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(graphStructure),
      });
      if (!response.ok) {
        const err = await response.json();
        throw new Error(err?.error || "Backend error");
      }
      const data = await response.json();
      return data;
    } catch (e) {
      console.error("Pipeline run error", e);
      return null;
    }
  };

  // If backend has responded, transform results into chart-friendly arrays
  const powerData = analysisResults
    ? Object.entries(analysisResults.output_data).map(([id, data]) => ({
        name: data.name,
        "Total Power": data.power_dict?.["Total Power"] ?? 0,
        "Internal Power": data.power_dict?.["Internal Power"] ?? 0,
        "Switching Power": data.power_dict?.["Switching Power"] ?? 0,
        "Leakage Power": data.power_dict?.["Leakage Power"] ?? 0,
      }))
    : [];

  const latencyData = analysisResults
    ? Object.entries(analysisResults.output_data).map(([id, data]) => ({
        name: data.name,
        latency: data.latency ?? 0,
      }))
    : [];

  // Compute overall metrics for current and comparison pipelines
  const totalPowerCurrent = analysisResults
    ? Object.values(analysisResults.output_data).reduce(
        (sum, m) => sum + (m.power_dict?.["Total Power"] ?? 0),
        0
      )
    : 0;

  const totalLatencyCurrent = analysisResults
    ? Object.values(analysisResults.output_data).reduce(
        (sum, m) => sum + (m.latency ?? 0),
        0
      )
    : 0;

  const totalPowerComparison = comparisonResults
    ? Object.values(comparisonResults.output_data).reduce(
        (sum, m) => sum + (m.power_dict?.["Total Power"] ?? 0),
        0
      )
    : 0;

  const totalLatencyComparison = comparisonResults
    ? Object.values(comparisonResults.output_data).reduce(
        (sum, m) => sum + (m.latency ?? 0),
        0
      )
    : 0;

  // Metrics to display in the summary cards
  const pipelineMetrics = {
    Power: analysisResults ? `${totalPowerCurrent.toFixed(6)} mW` : "--",
    Latency: analysisResults ? `${totalLatencyCurrent.toFixed(2)} ns` : "--",
    Accuracy: "-- %", // TODO: wire up when available
    "Simulation Time": "-- s", // TODO
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
        Accuracy: 95,
      },
      {
        name: comparisonPipeline?.name || "Comparison Pipeline",
        Accuracy: 92,
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
      <NavbarAnalysis pipelineName={pipeline?.name} />
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
