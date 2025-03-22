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
  db.prepare(
    `
    INSERT INTO pipelines (name, description, graph_structure)
    VALUES (?, ?, ?)
  `
  ).run(name, description, graphData ? JSON.stringify(graphData) : null);
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
  const existingPipeline = db
    .prepare("SELECT id FROM pipelines WHERE id = ?")
    .get(id);

  if (!existingPipeline) {
    return;
  }

  db.prepare(
    `
      UPDATE pipelines
      SET graph_structure = ?, name = ?, description = ?
      WHERE id = ?
    `
  ).run(graphData ? JSON.stringify(graphData) : null, name, description, id);
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
          label: "Custom Signal",
          type: "input",
          x: 100,
          y: 100,
          properties: {
            Frequency: { value: 100, unit: "Hz" },
            "Number of Channels": { value: 16, unit: "int" },
            "Number of Samples": { value: 10240, unit: "int" },
          },
          expanded: false,
        },
        {
          id: 2,
          label: "FFT",
          type: "module",
          x: 300,
          y: 100,
          properties: {
            "Clock Frequency": { value: 100, unit: "MHz" },
            "Number of Samples": { value: 10240, unit: "int" },
            "Sampling Frequency": { value: 512, unit: "Hz" },
            "Berger Bands": { value: "(0.1-4), (4-8)", unit: "Hz" },
            "Enable RTL Simulation": { value: true, unit: "boolean" },
          },
          expanded: false,
        },
        {
          id: 3,
          label: "Storage",
          type: "storage",
          x: 900,
          y: 100,
          properties: {
            Type: { value: "Spin-Transfer Torque", unit: "string" },
          },
          expanded: false,
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
