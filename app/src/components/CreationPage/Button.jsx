export function Button({ label, className, onClick }) {
  return (
    <button
      className={`px-4 py-2 text-white font-semibold rounded-md shadow-md bg-red-500 hover:bg-red-600 ${className}`}
      onClick={onClick}
    >
      {label}
    </button>
  );
}
