import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Info, Edit } from "lucide-react";
import { Menu } from "./Menu";
import { DeleteIcon } from "../Icons/icons";

export default function NavBar({
  pipelineName,
  pipelineDescription,
  updatePipelineInfo,
  pipelineId,
  hasUnsavedChanges,
  isModulesOpen,
  setIsModulesOpen,
}) {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [newName, setNewName] = useState("");
  const [newDescription, setNewDescription] = useState("");
  const router = useRouter();

  // Update state when the modal opens
  const openModal = () => {
    setNewName(pipelineName || "Untitled");
    setNewDescription(pipelineDescription || "");
    setIsModalOpen(true);
  };

  const handleModulesClick = (e) => {
    e.stopPropagation(); // Prevent click from bubbling up to page
    setIsModulesOpen((prev) => !prev);
  };

  const handleSave = () => {
    updatePipelineInfo(
      newName ? newName : "Untitled",
      newDescription ? newDescription : ""
    );
    setIsModalOpen(false);
  };

  const handleDelete = () => {
    if (pipelineId) {
      window.electronAPI
        .deletePipeline(pipelineId)
        .then(() => console.log("Pipeline deleted successfully"))
        .catch((error) => console.error("Failed to delete pipeline:", error));
    }
    router.push(`/`);
  };

  const handleForeseeClick = () => {
    if (hasUnsavedChanges) {
      if (
        !window.confirm(
          "You have unsaved changes. Are you sure you want to leave without saving?"
        )
      ) {
        // If user clicks "Cancel", stay on the page
        return;
      }
    }
    // Only navigate if user has no unsaved changes or clicked "OK" to leave without saving
    router.push(`/`);
  };

  return (
    <div className="flex items-center justify-between px-6 py-3 bg-white shadow-md relative">
      {/* Left Side */}
      <div className="flex items-center gap-4">
        <button
          className="bg-red-100 text-red-600 px-4 py-2 rounded-md font-semibold shadow-sm hover:bg-red-200"
          onClick={handleForeseeClick}
        >
          <em>Foresee</em>
        </button>
        <div className="relative" onClick={(e) => e.stopPropagation()}>
          <button
            className="bg-red-100 text-red-600 px-4 py-2 rounded-md font-semibold shadow-sm hover:bg-red-200 flex items-center"
            onClick={handleModulesClick}
          >
            Modules <span className="ml-1">▼</span>
          </button>
          {isModulesOpen && <Menu />}
        </div>
      </div>

      {/* Center Title - Hidden on Small Screens */}
      <div className="absolute left-1/2 transform -translate-x-1/2 hidden sm:flex items-center gap-2">
        <h1 className="text-xl font-bold">{pipelineName}</h1>
        <button
          onClick={openModal}
          className="text-gray-500 hover:text-gray-800"
        >
          <Edit size={16} />
        </button>
      </div>

      {/* Right Side - Delete Button */}
      <div className="flex items-center gap-4">
        <button
          onClick={handleDelete}
          className="text-red-600 hover:text-red-800 transition flex items-center gap-1"
        >
          <DeleteIcon />
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
                Done
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
