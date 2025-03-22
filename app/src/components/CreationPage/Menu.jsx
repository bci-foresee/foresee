import { Info } from "lucide-react";
import { useState } from "react";

const MODULES = {
  Processing: [
    {
      id: "fft",
      name: "Fast Fourier Transform",
      inputs: 1,
      outputs: 1,
      icon: "FFT",
      type: "module",
      properties: [
        { label: "Clock Frequency", type: "number", unit: "MHz" },
        { label: "Number of Samples", type: "number", unit: "count" },
        { label: "Sampling Frequency", type: "number", unit: "Hz" },
        {
          label: "Berger Bands",
          type: "range",
          unit: "Hz",
          example: ["(0.1-4)", "(4-8)"],
        },
        { label: "Enable RTL Simulation", type: "boolean" },
      ],
    },
    {
      id: "bpf",
      name: "Butterworth Bandpass Filter",
      inputs: 1,
      outputs: 1,
      icon: "BBF",
      type: "module",
      properties: [
        { label: "Sampling Frequency", type: "number", unit: "Hz" },
        {
          label: "Berger Bands",
          type: "range",
          unit: "Hz",
          example: ["(0.1-4)", "(4-8)"],
        },
        { label: "Clock Frequency", type: "number", unit: "MHz" },
        { label: "Enable RTL Simulation", type: "boolean" },
      ],
    },
    {
      id: "pcc",
      name: "Pairwise Cross-Correlation",
      inputs: 1,
      outputs: 1,
      icon: "PWXC",
      type: "module",
      properties: [
        { label: "Number of Channels", type: "number", unit: "count" },
        { label: "Clock Frequency", type: "number", unit: "MHz" },
        { label: "Enable RTL Simulation", type: "boolean" },
      ],
    },
    {
      id: "svm",
      name: "Support Vector Machine",
      inputs: "multiple",
      outputs: 1,
      icon: "SVM",
      type: "module",
      properties: [
        { label: "Model Weights", type: "file" },
        { label: "Clock Frequency", type: "number", unit: "MHz" },
        { label: "Enable RTL Simulation", type: "boolean" },
      ],
    },
    {
      id: "thr",
      name: "Threshold Detection",
      inputs: "multiple",
      outputs: 1,
      icon: "THR",
      type: "module",
      properties: [
        { label: "Lower Bound", type: "number" },
        { label: "Upper Bound", type: "number" },
        { label: "Clock Frequency", type: "number", unit: "MHz" },
        { label: "Enable RTL Simulation", type: "boolean" },
      ],
    },
    {
      id: "avg",
      name: "Signal Average",
      inputs: "multiple",
      outputs: 1,
      icon: "AVG",
      type: "module",
      properties: [
        { label: "Number of Channels", type: "number", unit: "count" },
        { label: "Clock Frequency", type: "number", unit: "MHz" },
        { label: "Enable RTL Simulation", type: "boolean" },
      ],
    },
    {
      id: "tkeo",
      name: "Teager-Kaiser Energy Operator",
      inputs: "single",
      outputs: 1,
      icon: "TKEO",
      type: "module",
      properties: [
        { label: "Number of Channels", type: "number", unit: "count" },
        { label: "Clock Frequency", type: "number", unit: "MHz" },
        { label: "Enable RTL Simulation", type: "boolean" },
      ],
    },
  ],
  Inputs: [
    {
      id: "custom",
      name: "Custom Signal",
      inputs: 0,
      outputs: 1,
      icon: "Input",
      type: "input",
      properties: [
        { label: "Frequency", type: "number", unit: "Hz" },
        { label: "Number of Channels", type: "number", unit: "count" },
        { label: "Number of Samples", type: "number", unit: "count" },
      ],
    },
    {
      id: "dataset",
      name: "Dataset",
      inputs: 0,
      outputs: 1,
      icon: "Input",
      type: "input",
      properties: [{ label: "File Path", type: "text" }],
    },
  ],
  Storage: [
    {
      id: "sst",
      name: "Spin-Transfer Torque",
      inputs: 0,
      outputs: 1,
      icon: "storage",
      type: "storage",
      properties: [{ label: "Type", type: "string" }],
    },
    {
      id: "pcm",
      name: "Phase-Change Memory",
      inputs: 0,
      outputs: 1,
      icon: "storage",
      type: "storage",
      properties: [{ label: "Type", type: "string" }],
    },
    {
      id: "fefet",
      name: "Ferroelectric Field-Effect Transistor",
      inputs: 0,
      outputs: 1,
      icon: "storage",
      type: "storage",
      properties: [{ label: "Type", type: "string" }],
    },
    {
      id: "rram",
      name: "Resistive Random Access Memory",
      inputs: 0,
      outputs: 1,
      icon: "storage",
      type: "storage",
      properties: [{ label: "Type", type: "string" }],
    },
  ],
};

const handleDragStart = (e, module) => {
  e.dataTransfer.setData("module", JSON.stringify(module));
  e.dataTransfer.effectAllowed = "move";
};

export function Menu({ label, className, onClick }) {
  const [activeTab, setActiveTab] = useState("Processing");

  return (
    <div className="absolute left-0 top-full mt-2 w-80 bg-white shadow-xl border rounded-lg z-50">
      {/* Header */}
      <div className="bg-red-600 text-white text-center font-bold py-2 rounded-t-lg">
        Modules
      </div>

      {/* Instructions */}
      <div className="px-4 py-2 text-gray-700 text-sm flex gap-2 items-center border-b">
        <Info size={16} className="text-gray-500" />
        <span>Drag-and-drop elements into the canvas.</span>
      </div>

      {/* Tabs */}
      <div className="flex border-b">
        {["Inputs", "Processing", "Storage"].map((tab) => (
          <button
            key={tab}
            className={`flex-1 py-2 text-sm font-semibold text-gray-500 ${
              activeTab === tab ? "border-b-2 border-black text-black" : ""
            }`}
            onClick={() => setActiveTab(tab)}
          >
            {tab}
          </button>
        ))}
      </div>

      {/* Scrollable Module List */}
      <ul className="py-2 px-4 max-h-64 overflow-y-auto">
        {MODULES[activeTab].map((module) => (
          <li
            key={module.id}
            draggable
            onDragStart={(e) => handleDragStart(e, module)}
            className="flex items-center p-3 border rounded-lg mb-2 shadow-sm hover:bg-gray-100 cursor-pointer w-full h-[70px] gap-3"
          >
            {/* Icon */}
            <span className="border border-red-500 text-red-500 px-3 py-1 rounded-lg font-semibold w-14 text-center text-sm flex items-center justify-center">
              {module.icon}
            </span>
            {/* Module Details */}
            <div className="flex flex-col flex-1">
              <p className="font-semibold text-sm">{module.name}</p>
              <p className="text-xs text-gray-600">
                {module.inputs} inputs / {module.outputs} output
              </p>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
