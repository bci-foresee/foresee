// components/AnalysisPage/NavBarAnalysis.jsx
import { useRouter } from "next/navigation";
import Image from "next/image";

export default function NavBarAnalysis({ pipelineName, pipelineData, analysisResults }) {
  const router = useRouter();

  const generateFullReport = () => {
    if (!analysisResults || !pipelineData) {
      alert("No analysis data available to download");
      return;
    }

    // Helper function to get display name
    const getDisplayName = (name) => {
      if (name === "Input PE") return "Input";
      return name;
    };

    // Calculate summary statistics
    const moduleData = Object.entries(analysisResults.output_data)
      .filter(([id, data]) => id !== 'simulation_time' && data && typeof data === 'object' && data.name);

    const totalPower = moduleData.reduce((sum, [id, data]) => sum + (data.power_dict?.["Total Power"] ?? 0), 0);
    const totalLatency = moduleData.reduce((sum, [id, data]) => sum + (data.latency ?? 0), 0);
    const simulationTime = analysisResults.simulation_time || 0;

    // Get accuracy if available
    const accuracy = analysisResults.pipeline_accuracy || analysisResults.accuracy?.accuracy || "N/A";

    // Generate detailed module breakdown
    const moduleBreakdown = moduleData.map(([id, data]) => ({
      name: getDisplayName(data.name),
      totalPower: data.power_dict?.["Total Power"] ?? 0,
      internalPower: data.power_dict?.["Internal Power"] ?? 0,
      switchingPower: data.power_dict?.["Switching Power"] ?? 0,
      leakagePower: data.power_dict?.["Leakage Power"] ?? 0,
      latency: data.latency ?? 0,
    }));

    // Calculate maximum values for chart scaling
    const maxPower = Math.max(...moduleBreakdown.map(m => m.totalPower));
    const maxLatency = Math.max(...moduleBreakdown.map(m => m.latency));

    // Create comprehensive HTML report
    const reportHTML = `
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>${pipelineName} - Analysis Report</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f9fafb;
            }
            .header {
                background: linear-gradient(135deg, #dc2626, #ef4444);
                color: white;
                padding: 2rem;
                border-radius: 10px;
                margin-bottom: 2rem;
                text-align: center;
            }
            .header h1 {
                margin: 0;
                font-size: 2.5rem;
                font-weight: bold;
            }
            .header p {
                margin: 0.5rem 0 0;
                opacity: 0.9;
                font-size: 1.1rem;
            }
            .summary-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 1.5rem;
                margin-bottom: 2rem;
            }
            .summary-card {
                background: white;
                padding: 1.5rem;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                text-align: center;
            }
            .summary-card h3 {
                margin: 0 0 0.5rem;
                color: #6b7280;
                font-size: 0.875rem;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }
            .summary-card .value {
                font-size: 2rem;
                font-weight: bold;
                color: #111827;
            }
            .summary-card .unit {
                font-size: 0.875rem;
                color: #6b7280;
            }
            .section {
                background: white;
                padding: 2rem;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                margin-bottom: 2rem;
            }
            .section h2 {
                margin: 0 0 1.5rem;
                color: #dc2626;
                border-bottom: 2px solid #dc2626;
                padding-bottom: 0.5rem;
            }
            .module-table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 1rem;
            }
            .module-table th,
            .module-table td {
                padding: 1rem;
                text-align: left;
                border-bottom: 1px solid #e5e7eb;
            }
            .module-table th {
                background-color: #f9fafb;
                font-weight: 600;
                color: #374151;
            }
            .module-table tr:hover {
                background-color: #f9fafb;
            }
            .power-breakdown {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 1rem;
                margin-top: 1rem;
            }
            .power-item {
                background: #f3f4f6;
                padding: 1rem;
                border-radius: 6px;
                text-align: center;
            }
            .power-item .label {
                font-size: 0.875rem;
                color: #6b7280;
                margin-bottom: 0.25rem;
            }
            .power-item .value {
                font-size: 1.25rem;
                font-weight: bold;
                color: #111827;
            }
            .metadata {
                background: #f9fafb;
                padding: 1rem;
                border-radius: 6px;
                margin-top: 1rem;
            }
            .metadata h3 {
                margin: 0 0 0.5rem;
                color: #374151;
            }
            .metadata p {
                margin: 0.25rem 0;
                color: #6b7280;
            }
            .accuracy-section {
                background: linear-gradient(135deg, #059669, #10b981);
                color: white;
                padding: 1.5rem;
                border-radius: 8px;
                text-align: center;
                margin-bottom: 1rem;
            }
            .accuracy-value {
                font-size: 3rem;
                font-weight: bold;
                margin: 0.5rem 0;
            }
            @media print {
                body { background-color: white; }
                .header { break-inside: avoid; }
                .section { break-inside: avoid; }
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>${pipelineName}</h1>
            <p>${pipelineData?.description || 'Pipeline Analysis Report'}</p>
            <p>Generated on ${new Date().toLocaleString()}</p>
        </div>

        <div class="summary-grid">
            <div class="summary-card">
                <h3>Total Power Consumption</h3>
                <div class="value">${totalPower.toFixed(2)}</div>
                <div class="unit">mW</div>
            </div>
            <div class="summary-card">
                <h3>Total Latency</h3>
                <div class="value">${totalLatency.toFixed(2)}</div>
                <div class="unit">ns</div>
            </div>
            <div class="summary-card">
                <h3>Simulation Time</h3>
                <div class="value">${simulationTime.toFixed(3)}</div>
                <div class="unit">seconds</div>
            </div>
            <div class="summary-card">
                <h3>Number of Modules</h3>
                <div class="value">${moduleData.length}</div>
                <div class="unit">modules</div>
            </div>
            ${accuracy !== "N/A" ? `
            <div class="summary-card">
                <h3>Pipeline Accuracy</h3>
                <div class="value">${typeof accuracy === 'number' ? (accuracy * 100).toFixed(1) : accuracy}%</div>
                <div class="unit">accuracy</div>
            </div>
            ` : ''}
        </div>

        <div class="section">
            <h2>Module Performance Breakdown</h2>
            <table class="module-table">
                <thead>
                    <tr>
                        <th>Module Name</th>
                        <th>Total Power (mW)</th>
                        <th>Internal Power (mW)</th>
                        <th>Switching Power (mW)</th>
                        <th>Leakage Power (mW)</th>
                        <th>Latency (ns)</th>
                    </tr>
                </thead>
                <tbody>
                    ${moduleBreakdown.map(module => `
                    <tr>
                        <td><strong>${module.name}</strong></td>
                        <td>${module.totalPower.toFixed(3)}</td>
                        <td>${module.internalPower.toFixed(3)}</td>
                        <td>${module.switchingPower.toFixed(3)}</td>
                        <td>${module.leakagePower.toFixed(3)}</td>
                        <td>${module.latency.toFixed(3)}</td>
                    </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>
    </body>
    </html>
    `;

    // Create and download the report
    const blob = new Blob([reportHTML], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `${pipelineName.replace(/[^a-z0-9]/gi, '_')}_Analysis_Report_${new Date().toISOString().split('T')[0]}.html`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  const handleDownload = () => {
    generateFullReport();
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
        <button onClick={handleDownload} className="hover:opacity-80 transition" title="Download Full Report">
          <Image src="/icons/import.png" alt="Download" width={24} height={24} />
        </button>
      </div>
    </div>
  );
}
