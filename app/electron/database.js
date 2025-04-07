const Database = require("better-sqlite3");
const path = require("path");
const { app } = require("electron");

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

// Create images table
db.prepare(
  `
  CREATE TABLE IF NOT EXISTS pipeline_images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pipeline_id INTEGER NOT NULL,
    metric TEXT NOT NULL,  -- e.g., "latency", "power", "accuracy"
    image_path TEXT NOT NULL,
    FOREIGN KEY (pipeline_id) REFERENCES pipelines(id) ON DELETE CASCADE
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
  const parsedId = parseInt(id, 10);
  return db.prepare("SELECT * FROM pipelines WHERE id = ?").get(parsedId);
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
      name || existingPipeline.name,
      description || existingPipeline.description,
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
  db.prepare("DELETE FROM pipelines WHERE id = ?").run(id);
  console.log(`🗑️ Pipeline with ID ${id} deleted.`);
}

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
          x: 100,
          y: 100,
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
          x: 300,
          y: 100,
          properties: {
            "Clock Frequency": { value: 100, unit: "Hz" },
            "Number of Samples": { value: 10240, unit: "count" },
            "Sampling Frequency": { value: 512, unit: "Hz" },
            "Berger Bands": { value: "0.1-4, 4-8", unit: "Hz" },
            "Enable RTL Simulation": { value: true, type: "boolean" },
            "Enable RTL Power Estimation": { value: true, type: "boolean" },
          },
        },
        {
          id: 3,
          label: "Storage",
          nodeType: "storage",
          x: 900,
          y: 100,
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

module.exports = {
  db,
  savePipeline,
  getPipelines,
  getPipelineById,
  editPipeline,
  deletePipeline,
};
