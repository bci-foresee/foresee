import Database from "better-sqlite3";
import path from "path";
import { app } from "electron";
import { fileURLToPath } from "url";

// __dirname recreation for ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const dbPath = path.join(app.getPath("userData"), "pipelines.sqlite");
const db = new Database(dbPath);

console.log("📂 Database file path:", dbPath);

// Enable foreign key support
db.prepare("PRAGMA foreign_keys = ON;").run();

// Create pipelines table
db.prepare(
  `
  CREATE TABLE IF NOT EXISTS pipelines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    graph_structure TEXT,  -- Can be NULL
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  )
`
).run();

// Create pipeline output table
db.prepare(
  `
  CREATE TABLE IF NOT EXISTS pipeline_output (
    id INTEGER PRIMARY KEY,
    output TEXT,  -- JSON string of output object
    FOREIGN KEY (id) REFERENCES pipelines(id) ON DELETE CASCADE
  )
`
).run();

// Function to insert a pipeline (modified to match schema)
function savePipeline(name, description = null, graphData = null) {
  console.log("💾 Database: Saving pipeline...");
  console.log("💾 Database: Name:", name);
  console.log("💾 Database: Description:", description);
  console.log("💾 Database: Graph data:", graphData);

  try {
    const stmt = db.prepare(
      "INSERT INTO pipelines (name, description, graph_structure) VALUES (?, ?, ?)"
    );
    const result = stmt.run(
      name,
      description,
      graphData ? JSON.stringify(graphData) : null
    );
    console.log("💾 Database: Save result:", result);
    return result;
  } catch (error) {
    console.error("💾 Database: Error saving pipeline:", error);
    throw error;
  }
}

// Function to retrieve pipelines
function getPipelines() {
  return db
    .prepare("SELECT * FROM pipelines")
    .all()
    .map((pipeline) => ({
      ...pipeline,
      graph_structure: pipeline.graph_structure
        ? JSON.parse(pipeline.graph_structure)
        : null,
    }));
}

function getPipelineById(id) {
  console.log("💾 Database: Getting pipeline by ID:", id);
  const pipeline = db.prepare("SELECT * FROM pipelines WHERE id = ?").get(id);
  console.log("💾 Database: Found pipeline:", pipeline);
  if (pipeline && pipeline.graph_structure) {
    try {
      const parsedGraph = JSON.parse(pipeline.graph_structure);
      console.log("💾 Database: Parsed graph structure:", parsedGraph);
    } catch (e) {
      console.error("💾 Database: Error parsing graph structure:", e);
    }
  }
  return pipeline;
}

// Function to edit an existing pipeline by ID
function editPipeline(id, name = null, description = null, graphData = null) {
  console.log("💾 Database: Editing pipeline...");
  console.log("💾 Database: ID:", id);
  console.log("💾 Database: Name:", name);
  console.log("💾 Database: Description:", description);
  console.log("💾 Database: Graph data:", graphData);

  const existingPipeline = db
    .prepare("SELECT id FROM pipelines WHERE id = ?")
    .get(id);

  if (!existingPipeline) {
    console.error("❌ Database: Pipeline not found:", id);
    throw new Error("Pipeline not found");
  }

  try {
    const stmt = db.prepare(
      "UPDATE pipelines SET name = ?, description = ?, graph_structure = ? WHERE id = ?"
    );
    const result = stmt.run(
      name,
      description,
      graphData ? JSON.stringify(graphData) : null,
      id
    );
    console.log("💾 Database: Edit result:", result);
    return result;
  } catch (error) {
    console.error("💾 Database: Error editing pipeline:", error);
    throw error;
  }
}

// Function to delete a pipeline by ID
function deletePipeline(id) {
  console.log("💾 Database: Deleting pipeline:", id);
  try {
    const result = db.prepare("DELETE FROM pipelines WHERE id = ?").run(id);
    console.log("💾 Database: Delete result:", result);
    return result;
  } catch (error) {
    console.error("💾 Database: Error deleting pipeline:", error);
    throw error;
  }
}

// Function to save pipeline output
function savePipelineOutput(id, outputObject) {
  console.log("💾 Database: Saving pipeline output...");
  console.log("💾 Database: Pipeline ID:", id);
  console.log("💾 Database: Output object:", outputObject);

  try {
    const stmt = db.prepare(
      "INSERT OR REPLACE INTO pipeline_output (id, output) VALUES (?, ?)"
    );
    const result = stmt.run(
      id,
      outputObject ? JSON.stringify(outputObject) : null
    );
    console.log("💾 Database: Save output result:", result);
    return result;
  } catch (error) {
    console.error("💾 Database: Error saving pipeline output:", error);
    throw error;
  }
}

// Function to get pipeline output by ID
function getPipelineOutput(id) {
  console.log("💾 Database: Getting pipeline output for ID:", id);
  try {
    const output = db.prepare("SELECT * FROM pipeline_output WHERE id = ?").get(id);
    if (output && output.output) {
      const parsedOutput = JSON.parse(output.output);
      console.log("💾 Database: Found pipeline output:", parsedOutput);
      return parsedOutput;
    }
    console.log("💾 Database: No output found for pipeline ID:", id);
    return null;
  } catch (error) {
    console.error("💾 Database: Error getting pipeline output:", error);
    throw error;
  }
}

// Function to get all pipeline outputs
function getPipelineOutputs() {
  console.log("💾 Database: Getting all pipeline outputs...");
  try {
    const outputs = db.prepare("SELECT id as pipeline_id, output FROM pipeline_output").all();
    console.log("💾 Database: Found pipeline outputs:", outputs.length);
    return outputs.map(row => ({
      pipeline_id: row.pipeline_id,
      output: row.output ? JSON.parse(row.output) : null
    }));
  } catch (error) {
    console.error("💾 Database: Error getting all pipeline outputs:", error);
    throw error;
  }
}

// Default pipeline
const pipelines = [
  {
    name: "Epileptic Seizure Prediction",
    description: "Predict epileptic seizures from EEG.",
    graph_structure: JSON.stringify({
      nodes: [
        {
          id: 1,
          label: "Input", // ✅ Abbreviation
          name: "Custom Signal", // ✅ Full Name
          nodeType: "input",
          position: { x: 100, y: 100 },
          properties: {
            Frequencies: { value: "10, 20, 40", type: "text" },
            Amplitudes: { value: "20, 15, 10", type: "text" },
            "Sampling Frequency": { value: 400, unit: "Hz" },
            "Number of Channels": { value: 16, unit: "count" },
            "Number of Samples": { value: 10240, unit: "count" },
          },
        },
        {
          id: 2,
          label: "FFT", // ✅ Abbreviation
          name: "Fast Fourier Transform", // ✅ Full Name
          nodeType: "module",
          position: { x: 300, y: 100 },
          properties: {
            "Clock Frequency": { value: 100, unit: "Hz" },
            "Number of Samples": { value: 10240, unit: "count" },
            "Sampling Frequency": { value: 400, unit: "Hz" },
            "Berger Bands": {
              value: [
                [0.1, 4],
                [4, 8],
                [8, 12],
                [12, 30],
                [30, 80],
                [80, 180],
              ],
              unit: "Hz",
            },
            "Enable RTL Simulation": { value: true, unit: "boolean" },
            "Enable RTL Power Estimation": { value: true, unit: "boolean" },
          },
        },
        {
          id: 3,
          label: "Storage",
          nodeType: "storage",
          position: { x: 900, y: 100 },
          properties: {
            "Storage Type": { value: "Spin-Transfer Torque" },
          },
        },
      ],
      edges: [
        { source: 1, target: 2 },
        { source: 2, target: 3 },
      ],
    }),
  },
];

// Insert pipelines if they don't exist
pipelines.forEach((pipeline) => {
  const exists = db
    .prepare("SELECT COUNT(*) AS count FROM pipelines WHERE name = ?")
    .get(pipeline.name);
  if (exists.count === 0) {
    savePipeline(pipeline.name, pipeline.description, pipeline.graph_structure);
  }
});

pipelines.forEach((pipeline) => {
  const exists = db
    .prepare("SELECT COUNT(*) AS count FROM pipelines WHERE name = ?")
    .get(pipeline.name);
  if (exists.count === 0) {
    db.prepare(
      `
      INSERT INTO pipelines (name, description, graph_structure)
      VALUES (?, ?, ?)
    `
    ).run(pipeline.name, pipeline.description, pipeline.graph_structure);
  }
});

pipelines.forEach((pipeline) => {
  const exists = db
    .prepare("SELECT COUNT(*) AS count FROM pipelines WHERE name = ?")
    .get(pipeline.name);
  if (exists.count === 0) {
    savePipeline(pipeline.name, pipeline.description, pipeline.graph_structure);
  }
});

console.log("✅ Pipelines table initialized with three entries.");

export {
  db,
  savePipeline,
  getPipelines,
  getPipelineById,
  editPipeline,
  deletePipeline,
  savePipelineOutput,
  getPipelineOutput,
  getPipelineOutputs,
};
