import { useState } from "react";
import { useRouter } from "next/navigation";
import { Info } from "lucide-react";

const MODULES = {
  Processing: [
    { id: "fft", name: "Fast Fourier Transform", inputs: 1, outputs: 1, icon: "FFT" },
    { id: "bpf", name: "Butterworth Bandpass Filter", inputs: 1, outputs: 1, icon: "BBF" },
    { id: "pcc", name: "Pairwise Cross-Correlation", inputs: 1, outputs: 1, icon: "PWXC" },
    { id: "svm", name: "Support Vector Machine", inputs: "multiple", outputs: 1, icon: "SVM" },
    { id: "thr", name: "Threshold Detection", inputs: "multiple", outputs: 1, icon: "THR" },
    { id: "avg", name: "Signal Average", inputs: "multiple", outputs: 1, icon: "AVG" },
    { id: "tkeo", name: "Teager-Kaiser Energy Operator", inputs: "single", outputs: 1, icon: "TKEO" },
  ],
  Inputs: [
    { id: "custom", name: "Custom Signal", inputs: 0, outputs: 1, icon: "Input" },
    { id: "dataset", name: "Dataset 1", inputs: 0, outputs: 1, icon: "Input" },
  ],
  Storage: [
    { id: "sst", name: "Spin-Transfer Torque", inputs: 0, outputs: 1, icon: "storage" },
    { id: "pcm", name: "Phase-Change Memory", inputs: 0, outputs: 1, icon: "storage" },
    { id: "fefet", name: "Ferroelectric Field-Effect Transistor", inputs: 0, outputs: 1, icon: "storage" },
    { id: "rram", name: "Resistive Random Access Memory", inputs: 0, outputs: 1, icon: "storage" },
  ],
};

const handleDragStart = (e, module) => {
  e.dataTransfer.setData("module", JSON.stringify(module));
};

export default function Navbar({ onDragStart }) {
  const [isModulesOpen, setIsModulesOpen] = useState(false);
  const [activeTab, setActiveTab] = useState("Processing");
  const router = useRouter();

  return (
    <div className="flex items-center justify-between px-6 py-3 bg-white shadow-md relative">
      {/* Left Side */}
      <div className="flex items-center gap-4">
        <button
          className="bg-red-100 text-red-600 px-4 py-2 rounded-md font-semibold shadow-sm hover:bg-red-200"
          onClick={() => router.push(`/`)}
        >
          <em>Foresee</em>
        </button>
        <div className="relative">
          <button
            className="bg-red-100 text-red-600 px-4 py-2 rounded-md font-semibold shadow-sm hover:bg-red-200 flex items-center"
            onClick={() => setIsModulesOpen((prev) => !prev)}
          >
            Modules <span className="ml-1">▼</span>
          </button>
          {isModulesOpen && (
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
                      <p className="text-xs text-gray-600">{module.inputs} inputs / {module.outputs} output</p>
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>

      {/* Center Title - Hidden on Small Screens */}
      <div className="absolute left-1/2 transform -translate-x-1/2 hidden sm:block">
        <h1 className="text-xl font-bold">Seizure Detection 1</h1>
      </div>
    </div>
  );
}
