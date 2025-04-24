"use client";

import { useSearchParams } from "next/navigation";
import { useEffect, useState, Suspense } from "react";
import Canvas from "../../components/CreationPage/Canvas";
import NavbarAnalysis from "../../components/AnalysisPage/NavbarAnalysis";
import {
  LineChart,
  Line,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

// 🔢 Hardcoded metrics
const hardcodedMetrics = {
  runtime: "60.08s",
  coldStartDuration: "0.50s",
  coldStartPercent: "100.00%",
  errorPercent: "0.00%",
  cost: "0.10 cents",
};

function AnalysisContent() {
  const searchParams = useSearchParams();
  const pipelineId = searchParams.get("id");
  const [pipeline, setPipeline] = useState(null);
  const [activeTab, setActiveTab] = useState("All");

  useEffect(() => {
    if (pipelineId) {
      window.electronAPI.getPipelineById(pipelineId).then((data) => {
        setPipeline(data);
      });
    }
  }, [pipelineId]);

  // 🔹 Sample data for charts
  const timeSeries = [
    { time: "21:55", value: 0 },
    { time: "22:00", value: 1 },
    { time: "22:05", value: 0 },
  ];

  const moduleData = [
    { name: "FFT", latency: 120 },
    { name: "BBF", latency: 160 },
    { name: "SVM", latency: 240 },
  ];

  const storageData = [
    { name: "Storage", throughput: 80 },
  ];

  const tabs = ["All", "Pipeline", "Modules", "Storage"];

  return (
    <div className="flex flex-col h-full w-full bg-gray-50">
      <NavbarAnalysis pipelineName={pipeline?.name} />
      <div className="flex-grow flex flex-col px-6">
        {/* Canvas */}
        <div className="h-[25vh] border rounded-lg overflow-hidden my-4 shadow-md bg-white">
          {pipeline ? (
            <Canvas
              graphData={JSON.parse(pipeline.graph_structure)}
              pipelineId={pipelineId}
              pipelineName={pipeline.name}
              pipelineDescription={pipeline.description}
              readOnly={true}
              autoFit={true}
            />
          ) : (
            <p className="p-4">Loading pipeline...</p>
          )}
        </div>

        {/* Metric Cards */}
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-8">
          {Object.entries(hardcodedMetrics).map(([key, val]) => (
            <div key={key} className="bg-white rounded-lg shadow p-4 text-center">
              <p className="text-sm text-gray-500 uppercase tracking-wider">
                {key.replace(/([A-Z])/g, " $1")}
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
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {(activeTab === "All" || activeTab === "Pipeline") && (
              <>
                <ChartCard title="Cold Starts">
                  <SimpleLineChart data={timeSeries} color="#EF4444" />
                </ChartCard>
                <ChartCard title="Init Duration (ms)">
                  <SimpleLineChart data={[{ time: "22:00", value: 600 }]} color="#3B82F6" />
                </ChartCard>
                <ChartCard title="Timeouts">
                  <SimpleLineChart data={[{ time: "21:57", value: 1 }]} color="#6366F1" />
                </ChartCard>
                <ChartCard title="Out of Memory Errors">
                  <SimpleLineChart data={[{ time: "22:00", value: 0 }]} color="#F59E0B" />
                </ChartCard>
              </>
            )}

            {activeTab === "Modules" && (
              <ChartCard title="Module Latency (ms)">
                <ResponsiveContainer width="100%" height={200}>
                  <LineChart data={moduleData}>
                    <Line type="monotone" dataKey="latency" stroke="#10B981" />
                    <CartesianGrid stroke="#ccc" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                  </LineChart>
                </ResponsiveContainer>
              </ChartCard>
            )}

            {activeTab === "Storage" && (
              <ChartCard title="Storage Throughput">
                <ResponsiveContainer width="100%" height={200}>
                  <LineChart data={storageData}>
                    <Line type="monotone" dataKey="throughput" stroke="#8B5CF6" />
                    <CartesianGrid stroke="#ccc" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                  </LineChart>
                </ResponsiveContainer>
              </ChartCard>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default function AnalysisPage() {
  return (
    <Suspense fallback={<div className="p-6">Loading...</div>}>
      <AnalysisContent />
    </Suspense>
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

// 📈 Generic line chart
function SimpleLineChart({ data, color }) {
  return (
    <ResponsiveContainer width="100%" height={200}>
      <LineChart data={data}>
        <Line type="monotone" dataKey="value" stroke={color} />
        <CartesianGrid stroke="#eee" strokeDasharray="5 5" />
        <XAxis dataKey="time" />
        <YAxis allowDecimals={false} />
        <Tooltip />
      </LineChart>
    </ResponsiveContainer>
  );
}
