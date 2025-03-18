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
function editPipeline(id, graphData = null) {
  const existingPipeline = db
    .prepare("SELECT id FROM pipelines WHERE id = ?")
    .get(id);

  if (!existingPipeline) {
    return;
  }

  db.prepare(
    `
      UPDATE pipelines
      SET graph_structure = ?
      WHERE id = ?
    `
  ).run(graphData ? JSON.stringify(graphData) : null, id);
}

// 🔹 Insert Three Initial Pipelines (Avoid Duplicates)
const pipelines = [
  {
    name: "Epileptic Seizure Prediction",
    description: "Predict epileptic seizures from EEG.",
    graph_structure: JSON.stringify({
      nodes: [
        { id: 1, label: "Input", type: "input", x: 100, y: 100 },
        { id: 2, label: "BBF", type: "module", x: 300, y: 100 },
        { id: 3, label: "PWXC", type: "module", x: 300, y: 200 },
        { id: 4, label: "FFT", type: "module", x: 300, y: 300 },
        { id: 5, label: "SVM", type: "module", x: 500, y: 100 },
        { id: 6, label: "THR", type: "module", x: 700, y: 100 },
        { id: 7, label: "Storage", type: "storage", x: 900, y: 100 },
      ],
      edges: [
        { source: 1, target: 2 },
        { source: 1, target: 3 },
        { source: 1, target: 4 },
        { source: 2, target: 5 },
        { source: 3, target: 5 },
        { source: 4, target: 5 },
        { source: 5, target: 6 },
        { source: 6, target: 7 },
      ],
    }),
  },
  {
    name: "Movement Intent",
    description: "Decode movement intent from EEG.",
    graph_structure: JSON.stringify({
      nodes: [
        { id: 1, label: "Input", type: "input", x: 100, y: 200 },
        { id: 2, label: "Feature Extraction", type: "module", x: 300, y: 200 },
        { id: 3, label: "Classifier", type: "module", x: 500, y: 200 },
        { id: 4, label: "Decision", type: "module", x: 700, y: 200 },
      ],
      edges: [
        { source: 1, target: 2 },
        { source: 2, target: 3 },
        { source: 3, target: 4 },
      ],
    }),
  },
  {
    name: "Speech Decoding",
    description: "Translate EEG signals into speech.",
    graph_structure: JSON.stringify({
      nodes: [
        { id: 1, label: "Input", type: "input", x: 100, y: 200 },
        { id: 2, label: "Signal Processing", type: "module", x: 300, y: 200 },
        { id: 3, label: "Phoneme Extraction", type: "module", x: 500, y: 200 },
        { id: 4, label: "Text Output", type: "module", x: 700, y: 200 },
      ],
      edges: [
        { source: 1, target: 2 },
        { source: 2, target: 3 },
        { source: 3, target: 4 },
      ],
    }),
  },
  {
    name: "Test Pipeline 1",
    description: "A test pipeline with sample modules.",
    graph_structure: JSON.stringify({
      nodes: [
        { id: 1, label: "Input", type: "input", x: 100, y: 200 },
        { id: 2, label: "Processing", type: "module", x: 300, y: 200 },
        { id: 3, label: "Output", type: "module", x: 500, y: 200 },
      ],
      edges: [
        { source: 1, target: 2 },
        { source: 2, target: 3 },
      ],
    }),
  },
  {
    name: "Test Pipeline 2",
    description: "Another test pipeline with different structure.",
    graph_structure: JSON.stringify({
      nodes: [
        { id: 1, label: "Start", type: "input", x: 100, y: 200 },
        { id: 2, label: "Intermediate", type: "module", x: 300, y: 200 },
        { id: 3, label: "End", type: "module", x: 500, y: 200 },
      ],
      edges: [
        { source: 1, target: 2 },
        { source: 2, target: 3 },
      ],
    }),
  },
];

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
};
