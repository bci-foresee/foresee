/**
 *  Menu for selecting and dragging nodes onto the canvas.
 */

import { Info } from "lucide-react";
import { useState } from "react";

const MODULES = {
  Processing: [
    {
      id: "fft",
      label: "FFT",
      name: "Fast Fourier Transform",
      inputs: 1,
      outputs: 1,
      icon: "FFT",
      nodeType: "module",
      properties: {
        "Clock Frequency": { value: 0, unit: "Hz" },
        "Number of Samples": { value: 0, unit: "count" },
        "Sampling Frequency": { value: 0, unit: "Hz" },
        "Berger Bands": { value: "", unit: "Hz" },
        "Enable RTL Simulation": { value: true, type: "boolean" },
      },
    },
    {
      id: "bbf",
      label: "BBF",
      name: "Butterworth Bandpass Filter",
      inputs: 1,
      outputs: 1,
      icon: "BBF",
      nodeType: "module",
      properties: {
        "Sampling Frequency": { type: "number", unit: "Hz" },
        "Berger Bands": {
          type: "text",
          unit: "Hz",
          value: "",
        },
        "Clock Frequency": { value: 0, unit: "MHz" },
        "Enable RTL Simulation": { value: true, type: "boolean" },
      },
    },
    {
      id: "pwxc",
      label: "PWXC",
      name: "Pairwise Cross-Correlation",
      inputs: 1,
      outputs: 1,
      icon: "PWXC",
      nodeType: "module",
      properties: {
        "Number of Channels": { value: 0, unit: "count" },
        "Clock Frequency": { value: 0, unit: "Hz" },
        "Enable RTL Simulation": { value: true, type: "boolean" },
      },
    },
    {
      id: "svm",
      label: "SVM",
      name: "Support Vector Machine",
      inputs: 1,
      outputs: 1,
      icon: "SVM",
      nodeType: "module",
      properties: {
        Weights: { value: "", type: "text" },
        "Clock Frequency": { value: 0, unit: "Hz" },
        "Enable RTL Simulation": { value: true, type: "boolean" },
      },
    },
    {
      id: "thr",
      label: "THR",
      name: "Threshold Detection",
      inputs: "multiple",
      outputs: 1,
      icon: "THR",
      nodeType: "module",
      properties: {
        "Lower Bound": { value: 0, type: "integer" },
        "Upper Bound": { value: 0, type: "integer" },
        "Clock Frequency": { value: 0, unit: "Hz" },
        "Enable RTL Simulation": { value: true, type: "boolean" },
      },
    },
    {
      id: "avg",
      label: "AVG",
      name: "Signal Average",
      inputs: 1,
      outputs: 1,
      icon: "AVG",
      nodeType: "module",
      properties: {
        "Number of Channels": { value: 0, unit: "count" },
        "Clock Frequency": { value: 0, unit: "Hz" },
        "Enable RTL Simulation": { value: true, type: "boolean" },
      },
    },
    {
      id: "tkeo",
      label: "TKEO",
      name: "Teager-Kaiser Energy Operator",
      inputs: 1,
      outputs: 1,
      icon: "TKEO",
      nodeType: "module",
      properties: {
        "Number of Channels": { value: 0, unit: "count" },
        "Clock Frequency": { value: 0, unit: "Hz" },
        "Enable RTL Simulation": { value: true, type: "boolean" },
      },
    },
  ],
  Inputs: [
    {
      id: "custom",
      label: "Input",
      name: "Custom Signal",
      inputs: 0,
      outputs: 1,
      icon: "Input",
      nodeType: "input",
      properties: {
        Frequencies: {
          value: "",
          type: "text",
          regex: /^(\d+(\.\d+)?)(,\s*\d+(\.\d+)?)*$/,
          errorMessage: "Must be comma-separated numbers (e.g., 1, 2, 3)",
        },
        Amplitudes: {
          value: "",
          type: "text",
          regex: /^(\d+(\.\d+)?)(,\s*\d+(\.\d+)?)*$/,
          errorMessage: "Must be comma-separated numbers (e.g., 1, 2, 3)",
        },
        "Sampling Frequency": {
          value: 0,
          unit: "Hz",
          type: "number",
          min: 0,
          max: 1000,
          errorMessage: "Must be between 0 and 1000 Hz",
        },
        "Number of Channels": {
          value: 0,
          unit: "count",
          type: "integer",
          min: 0,
          max: 256,
          errorMessage: "Must be a whole number between 0 and 256",
        },
        "Number of Samples": {
          value: 0,
          unit: "count",
          type: "integer",
          min: 0,
          max: 1000000,
          errorMessage: "Must be a whole number between 0 and 1,000,000",
        },
      },
    },
    {
      id: "eeg_dataset",
      label: "iEEG Dataset",
      name: "iEEG Dataset",
      inputs: 0,
      outputs: 1,
      icon: "Input",
      nodeType: "input",
      properties: {
        "Dataset Path": {
          value: "",
          type: "text",
        },
        "Info File Path": {
          value: "",
          type: "text",
        },
        "Window Duration": {
          value: 4.0,
          type: "number",
          unit: "s",
          min: 0.1,
          max: 60.0,
        },
        "Window Offset": {
          value: 2.0,
          type: "number",
          unit: "s",
          min: 0.0,
          max: 30.0,
        },
      },
    },
  ],
  Storage: [
    {
      id: "sst",
      label: "Storage",
      name: "Spin-Transfer Torque",
      inputs: 0,
      outputs: 1,
      icon: "storage",
      nodeType: "storage",
      properties: {
        "Storage Type": {
          type: "dropdown",
          allowedValues: [
            "Spin-Transfer Torque",
            "Phase-Change Memory",
            "Ferroelectric Field-Effect Transistor",
            "Resistive Random Access Memory",
          ],
        },
      },
    },
    {
      id: "pcm",
      label: "Storage",
      name: "Phase-Change Memory",
      inputs: 0,
      outputs: 1,
      icon: "storage",
      nodeType: "storage",
      properties: {
        "Storage Type": {
          type: "dropdown",
          allowedValues: [
            "Spin-Transfer Torque",
            "Phase-Change Memory",
            "Ferroelectric Field-Effect Transistor",
            "Resistive Random Access Memory",
          ],
        },
      },
    },
    {
      id: "fefet",
      label: "Storage",
      name: "Ferroelectric Field-Effect Transistor",
      inputs: 0,
      outputs: 1,
      icon: "storage",
      nodeType: "storage",
      properties: {
        "Storage Type": {
          type: "dropdown",
          allowedValues: [
            "Spin-Transfer Torque",
            "Phase-Change Memory",
            "Ferroelectric Field-Effect Transistor",
            "Resistive Random Access Memory",
          ],
        },
      },
    },
    {
      id: "rram",
      label: "Storage",
      name: "Resistive Random Access Memory",
      inputs: 0,
      outputs: 1,
      icon: "storage",
      nodeType: "storage",
      properties: {
        "Storage Type": {
          type: "dropdown",
          allowedValues: [
            "Spin-Transfer Torque",
            "Phase-Change Memory",
            "Ferroelectric Field-Effect Transistor",
            "Resistive Random Access Memory",
          ],
        },
      },
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
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
