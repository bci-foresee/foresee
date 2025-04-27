// components/AnalysisPage/NavBarAnalysis.jsx
import { useRouter } from "next/navigation";
import Image from "next/image";

export default function NavBarAnalysis({ pipelineName }) {
  const router = useRouter();

  const handleDownload = () => {
    // You can customize this
    alert("Download triggered (you can wire this to actual export logic)");
  };

  return (
    <div className="flex items-center justify-between px-6 py-3 bg-white shadow-md relative">
      {/* Left Side: App name + Back */}
      <div className="flex items-center gap-4">
        <button
          className="bg-red-100 text-red-600 px-4 py-2 rounded-md font-semibold shadow-sm hover:bg-red-200"
          onClick={() => router.push(`/`)}
        >
          <em>Foresee</em>
        </button>
      </div>

      {/* Center: Pipeline Name */}
      <div className="absolute left-1/2 transform -translate-x-1/2 hidden sm:flex items-center gap-2">
        <h1 className="text-xl font-bold">{pipelineName}</h1>
      </div>

      {/* Right Side: Download button */}
      <div className="flex items-center gap-4">
        <button onClick={handleDownload} className="hover:opacity-80 transition">
          <Image src="/icons/import.png" alt="Download" width={24} height={24} />
        </button>
      </div>
    </div>
  );
}
