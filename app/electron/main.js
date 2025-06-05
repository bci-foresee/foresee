import { app, BrowserWindow, ipcMain, session } from "electron";
import path from "path";
import { fileURLToPath } from "url";
import { createServer } from "http";
import serveStatic from "serve-static";
import {
  savePipeline,
  getPipelines,
  getPipelineById,
  editPipeline,
  deletePipeline,
  savePipelineOutput,
  getPipelineOutput,
} from "./database.js";
import { spawn } from "child_process";

// __dirname is not available in ES modules; recreate it manually
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

let mainWindow;
let backendProcess;

function startBackend() {
  const pythonExecutable = process.env.PYTHON_PATH || "python"; // Allow override via env
  const backendScript = path.resolve(__dirname, "../../backend/app.py");
  console.log("🚀 Starting backend →", pythonExecutable, backendScript);

  backendProcess = spawn(pythonExecutable, [backendScript]);

  backendProcess.stdout.on("data", (data) => {
    console.log(`[Backend] ${data}`.trim());
  });

  backendProcess.stderr.on("data", (data) => {
    console.error(`[Backend error] ${data}`.trim());
  });

  backendProcess.on("exit", (code, signal) => {
    console.log(`⚠️  Backend exited with code ${code} and signal ${signal}`);
  });
}

function stopBackend() {
  if (backendProcess && !backendProcess.killed) {
    console.log("🛑 Stopping backend...");
    backendProcess.kill();
  }
}

app.whenReady().then(() => {
  startBackend();
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, "preload.cjs"), // Securely expose database functions
      nodeIntegration: false, // Keep Node.js disabled in the renderer for security
      contextIsolation: true, // Required for secure IPC communication
      webSecurity: true,
      allowRunningInsecureContent: false,
    },
  });

  mainWindow.webContents.openDevTools();

  const devServerURL = "http://localhost:3000"; // Dev mode

  const isDev = process.env.NODE_ENV !== "production";

  if (isDev) {
    console.log("Loading dev server →", devServerURL);
    mainWindow.loadURL(devServerURL);
  } else {
    // Start a tiny static file server serving the exported build in ../out
    const staticPath = path.join(__dirname, "../out");
    const serve = serveStatic(staticPath, {
      index: ["index.html"],
    });

    // Create HTTP server on a random free port
    const httpServer = createServer((req, res) => {
      serve(req, res, () => {
        res.statusCode = 404;
        res.end("Not Found");
      });
    });

    httpServer.listen(0, "127.0.0.1", () => {
      const { port } = httpServer.address();
      const prodURL = `http://localhost:${port}`;
      console.log("Static server listening →", prodURL);
      mainWindow.loadURL(prodURL);
    });
  }

  mainWindow.on("closed", () => {
    mainWindow = null;
  });

  // 💾 IPC handlers for SQLite database access
  ipcMain.handle("getPipelines", () => getPipelines());
  ipcMain.handle("savePipeline", (event, name, description, graphData) => {
    console.log("💾 Main: Saving pipeline...");
    console.log("💾 Main: Graph data:", graphData);
    const result = savePipeline(name, description, graphData);
    console.log("💾 Main: Save result:", result);
    return result;
  });
  ipcMain.handle("getPipelineById", async (event, id) => getPipelineById(id));
  ipcMain.handle(
    "editPipeline",
    async (event, id, name, description, graphData) => {
      console.log("💾 Main: Editing pipeline...");
      console.log("💾 Main: Pipeline ID:", id);
      console.log("💾 Main: Graph data:", graphData);
      const result = editPipeline(id, name, description, graphData);
      console.log("💾 Main: Edit result:", result);
      return result;
    }
  );
  ipcMain.handle("deletePipeline", async (event, id) => deletePipeline(id));
  ipcMain.handle("savePipelineOutput", async (event, id, outputObject) => savePipelineOutput(id, outputObject));
  ipcMain.handle("getPipelineOutput", async (event, id) => getPipelineOutput(id));
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});

app.on("will-quit", () => {
  stopBackend();
});
