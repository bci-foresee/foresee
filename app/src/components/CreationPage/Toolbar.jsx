export function Toolbar({ className }) {
  return (
    <div
      className={`flex justify-between items-center p-2 bg-white shadow-md border-b ${className}`}
    >
      <div className="flex gap-2">
        <button className="px-3 py-1 bg-gray-300 rounded hover:bg-gray-400">
          Zoom In
        </button>
        <button className="px-3 py-1 bg-gray-300 rounded hover:bg-gray-400">
          Zoom Out
        </button>
      </div>
    </div>
  );
}
