import { useState } from "react";
import { useRouter } from "next/navigation";

const MODULES = [
  {
    id: "fft",
    name: "Fast Fourier Transform",
    inputs: 1,
    outputs: 1,
    icon: "FFT",
  },
  {
    id: "bpf",
    name: "Butterworth Bandpass Filter",
    inputs: 1,
    outputs: 1,
    icon: "BPF",
  },
  {
    id: "pcc",
    name: "Pairwise Cross-Correlation",
    inputs: 1,
    outputs: 1,
    icon: "PWXC",
  },
  {
    id: "svm",
    name: "Support Vector Machine",
    inputs: "multiple",
    outputs: 1,
    icon: "SVM",
  },
  {
    id: "thr",
    name: "Threshold Detection",
    inputs: "multiple",
    outputs: 1,
    icon: "THR",
  },
];

const handleDragStart = (e, module) => {
  console.log("Dragging module:", module);
  e.dataTransfer.setData("module", JSON.stringify(module));
};

export default function Navbar({ onDragStart }) {
  const [isModulesOpen, setIsModulesOpen] = useState(false);
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
            <div className="absolute left-0 top-full mt-2 w-72 bg-white shadow-lg border rounded-lg p-4 z-50">
              <h3 className="text-red-600 font-bold text-center">Modules</h3>
              <p className="text-xs text-gray-600 text-center mb-2">
                Drag-and-drop elements into the canvas.
              </p>
              <ul>
                {MODULES.map((module) => (
                  <li
                    key={module.id}
                    draggable
                    onDragStart={(e) => handleDragStart(e, module)}
                    className="p-2 border-b cursor-pointer flex items-center hover:bg-gray-100"
                  >
                    <span className="border border-red-500 text-red-500 px-2 py-1 rounded-md mr-2">
                      {module.icon}
                    </span>
                    <div>
                      <p className="font-bold">{module.name}</p>
                      <p className="text-xs text-gray-600">
                        {module.inputs} inputs / {module.outputs} output
                      </p>
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
