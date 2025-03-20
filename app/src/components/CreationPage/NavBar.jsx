import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Info, Edit } from "lucide-react";
import { Menu } from "./Menu";

export default function Navbar({ pipelineName, pipelineDescription, updatePipelineInfo }) {
  const [isModulesOpen, setIsModulesOpen] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [newName, setNewName] = useState("");
  const [newDescription, setNewDescription] = useState("");
  const router = useRouter();

  // **Update state when the modal opens**
  const openModal = () => {
    setNewName(pipelineName || "Untitled"); // Ensure there's always a default name
    setNewDescription(pipelineDescription || ""); // Default to empty if no description
    setIsModalOpen(true);
  };

  // **Handle Save**
  const handleSave = () => {
    updatePipelineInfo(newName ? newName : "Untitled", newDescription ? newDescription : "");
    setIsModalOpen(false);
  };

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
          {isModulesOpen && <Menu />}
        </div>
      </div>

      {/* Center Title - Hidden on Small Screens */}
      <div className="absolute left-1/2 transform -translate-x-1/2 hidden sm:flex items-center gap-2">
        <h1 className="text-xl font-bold">{pipelineName}</h1>
        <button onClick={openModal} className="text-gray-600 hover:text-gray-800">
          <Edit size={18} />
        </button>
      </div>

      {/* Edit Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-opacity-30 backdrop-blur-md flex justify-center items-center z-50">
          <div className="bg-white p-6 rounded-lg shadow-lg w-96 relative">
            <h2 className="text-lg font-bold mb-4">Edit Pipeline Info</h2>

            {/* Name Input */}
            <label className="block mb-2">
              <span className="text-gray-700">Name</span>
              <input
                type="text"
                className="w-full border p-2 rounded mt-1"
                value={newName}
                onChange={(e) => setNewName(e.target.value)}
              />
            </label>

            {/* Description Input */}
            <label className="block mb-4">
              <span className="text-gray-700">Description</span>
              <textarea
                className="w-full border p-2 rounded mt-1"
                value={newDescription}
                onChange={(e) => setNewDescription(e.target.value)}
              />
            </label>

            {/* Buttons */}
            <div className="flex justify-end gap-2">
              <button
                className="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400"
                onClick={() => setIsModalOpen(false)}
              >
                Cancel
              </button>
              <button
                className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 transition"
                onClick={handleSave}
              >
                Save
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
