import { app, BrowserWindow, ipcMain, session } from "electron";
import path from "path";
import { fileURLToPath } from "url";
import { createServer } from "http";
import serveStatic from "serve-static";
import fs from "fs";
import {
  savePipeline,
  getPipelines,
  getPipelineById,
  editPipeline,
  deletePipeline,
  savePipelineOutput,
  getPipelineOutput,
  getPipelineOutputs,
} from "./database.js";
import { spawn } from "child_process";

// __dirname is not available in ES modules; recreate it manually
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

let mainWindow;
let backendProcess;

// Unified development detection
function isDevelopment() {
  return !app.isPackaged && process.env.NODE_ENV !== "production";
}

function startBackend() {
  // Only start backend in development mode
  const isDev = isDevelopment();
  
  console.log("🔍 Environment check:", {
    NODE_ENV: process.env.NODE_ENV,
    isPackaged: app.isPackaged,
    isDev: isDev
  });
  
  if (!isDev) {
    console.log("🚀 Backend disabled in packaged/production mode");
    return;
  }

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
  } else {
    console.log("🛑 Backend not running, nothing to stop");
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

  // Only open dev tools in development
  if (isDevelopment()) {
    mainWindow.webContents.openDevTools();
  }

  const devServerURL = "http://localhost:3000"; // Dev mode

  if (isDevelopment()) {
    console.log("🔧 Development mode: Loading dev server →", devServerURL);
    mainWindow.loadURL(devServerURL);
  } else {
    console.log("📦 Production mode: Setting up static file server");
    
    // In packaged mode, find the static files
    const possiblePaths = [
      path.join(__dirname, "../out"),                    // Conveyor: app/out
      path.join(process.resourcesPath, "app", "out"),    // Alternative packaged path
      path.join(__dirname, "../../out"),                 // Development fallback
    ];
    
    let staticPath = null;
    console.log("🔍 __dirname:", __dirname);
    console.log("🔍 process.resourcesPath:", process.resourcesPath);
    
    for (const testPath of possiblePaths) {
      console.log("🔍 Testing path:", testPath);
      if (fs.existsSync(testPath)) {
        const indexExists = fs.existsSync(path.join(testPath, "index.html"));
        console.log(`✅ Path exists: ${testPath}, index.html exists: ${indexExists}`);
        if (indexExists) {
          staticPath = testPath;
          break;
        }
      } else {
        console.log(`❌ Path does not exist: ${testPath}`);
      }
    }
    
    if (!staticPath) {
      console.error("❌ Could not find static files in any expected location!");
      const errorHtml = `
        <html>
          <body>
            <h1>Error: Could not find static files</h1>
            <p>Searched paths:</p>
            <ul>
              ${possiblePaths.map(p => `<li>${p}</li>`).join('')}
            </ul>
            <p>__dirname: ${__dirname}</p>
            <p>process.resourcesPath: ${process.resourcesPath}</p>
          </body>
        </html>
      `;
      mainWindow.loadURL(`data:text/html,${encodeURIComponent(errorHtml)}`);
      return;
    }
    
    console.log("✅ Using static path:", staticPath);
    const files = fs.readdirSync(staticPath);
    console.log("📁 Files in static path:", files.slice(0, 10)); // Show first 10 files
    
    const serve = serveStatic(staticPath, {
      index: ["index.html"],
      fallthrough: false,
    });

    // Create HTTP server on a random free port
    const httpServer = createServer((req, res) => {
      console.log("🌐 Request:", req.url);
      serve(req, res, (err) => {
        if (err) {
          console.log("❌ Static serve error for:", req.url, err.message);
          res.statusCode = 404;
          res.end("Not Found");
        }
      });
    });

    httpServer.listen(0, "127.0.0.1", () => {
      const { port } = httpServer.address();
      const prodURL = `http://localhost:${port}`;
      console.log("🚀 Static server listening →", prodURL);
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
  ipcMain.handle("getPipelineOutputs", async () => getPipelineOutputs());
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});

app.on("will-quit", () => {
  stopBackend();
});
