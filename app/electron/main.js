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
  console.log("🔍 Environment check:", {
    NODE_ENV: process.env.NODE_ENV,
    isPackaged: app.isPackaged,
    isDev: isDevelopment()
  });
  
  // Check for conda environment activation
  const condaEnvName = "foresee_alejo";
  console.log(`🐍 Target conda environment: ${condaEnvName}`);
  
  // Determine backend script path based on packaging
  let backendScript;
  if (app.isPackaged) {
    // In packaged app, backend should be in Resources
    const possibleBackendPaths = [
      path.join(process.resourcesPath, "backend", "app.py"),
      path.join(__dirname, "../../backend/app.py"),  // Relative from electron dir
      path.join(__dirname, "../backend/app.py"),     // Alternative path
    ];
    
    for (const testPath of possibleBackendPaths) {
      console.log("🔍 Testing backend path:", testPath);
      if (fs.existsSync(testPath)) {
        backendScript = testPath;
        console.log("✅ Found backend script:", backendScript);
        break;
      } else {
        console.log("❌ Backend script not found:", testPath);
      }
    }
    
    if (!backendScript) {
      console.error("❌ Could not find backend script in packaged app!");
      // Create error notification for user
      if (mainWindow) {
        mainWindow.webContents.executeJavaScript(`
          console.error("Backend unavailable: Python backend script not found in packaged app");
          alert("Backend services are currently unavailable. Pipeline analysis will not work.");
        `);
      }
      return;
    }
  } else {
    // Development mode
    backendScript = path.resolve(__dirname, "../../backend/app.py");
  }

  console.log("🚀 Starting backend with conda environment:", condaEnvName, backendScript);

  // Set working directory to backend directory
  const backendDir = path.dirname(backendScript);
  
  // Create conda activation command for Unix systems (macOS/Linux)
  const isWindows = process.platform === 'win32';
  let command, args;
  
  if (app.isPackaged) {
    // In packaged mode, try to find system Python with fallback
    console.log("📦 Packaged mode: Trying to find suitable Python installation");
    
    const possiblePythonPaths = [
      "python3",                      // Standard Python 3
      "python",                       // Generic Python
      "/usr/bin/python3",            // System Python 3
      "/usr/local/bin/python3",      // Homebrew Python 3
      "/opt/homebrew/bin/python3",   // Apple Silicon Homebrew
    ];

    let pythonExecutable = "python3"; // Default fallback
    for (const pythonPath of possiblePythonPaths) {
      try {
        // Synchronous check using spawnSync
        const { execSync } = require('child_process');
        execSync(`${pythonPath} --version`, { stdio: 'pipe' });
        pythonExecutable = pythonPath;
        console.log(`✅ Found Python: ${pythonPath}`);
        break;
      } catch (e) {
        console.log(`❌ Python not found: ${pythonPath}`);
      }
    }
    
    console.log(`🐍 Using Python executable for packaged app: ${pythonExecutable}`);
    
    if (isWindows) {
      command = 'cmd';
      args = ['/c', `${pythonExecutable} ${path.basename(backendScript)}`];
    } else {
      command = pythonExecutable;
      args = [path.basename(backendScript)];
    }
  } else {
    // Development mode: Use conda environment
    if (isWindows) {
      // Windows conda activation
      command = 'cmd';
      args = ['/c', `conda activate ${condaEnvName} && python ${path.basename(backendScript)}`];
    } else {
      // Unix conda activation (macOS/Linux)
      // Use bash to source conda and activate environment
      command = 'bash';
      args = ['-c', `
        source ~/.bash_profile 2>/dev/null || true
        source ~/.bashrc 2>/dev/null || true
        
        # Try multiple conda initialization paths
        if [ -f "$HOME/anaconda3/bin/conda" ]; then
          eval "$($HOME/anaconda3/bin/conda shell.bash hook)"
        elif [ -f "$HOME/miniconda3/bin/conda" ]; then
          eval "$($HOME/miniconda3/bin/conda shell.bash hook)"
        elif [ -f "/opt/anaconda3/bin/conda" ]; then
          eval "$(/opt/anaconda3/bin/conda shell.bash hook)"
        elif [ -f "/opt/miniconda3/bin/conda" ]; then
          eval "$(/opt/miniconda3/bin/conda shell.bash hook)"
        elif command -v conda > /dev/null 2>&1; then
          eval "$(conda shell.bash hook)"
        else
          echo "❌ Conda not found, falling back to system Python"
          python3 ${path.basename(backendScript)}
          exit $?
        fi
        
        echo "🔄 Activating conda environment: ${condaEnvName}"
        if conda activate ${condaEnvName}; then
          echo "🐍 Using Python: $(which python)"
          echo "🚀 Starting Flask server..."
          python ${path.basename(backendScript)}
        else
          echo "❌ Failed to activate conda environment, falling back to system Python"
          python3 ${path.basename(backendScript)}
        fi
      `];
    }
  }
  
  backendProcess = spawn(command, args, {
    cwd: backendDir,
    stdio: ['pipe', 'pipe', 'pipe'],
    shell: false  // We're handling the shell ourselves
  });

  backendProcess.stdout.on("data", (data) => {
    console.log(`[Backend] ${data}`.trim());
  });

  backendProcess.stderr.on("data", (data) => {
    console.error(`[Backend error] ${data}`.trim());
  });

  backendProcess.on("exit", (code, signal) => {
    console.log(`⚠️  Backend exited with code ${code} and signal ${signal}`);
    if (code !== 0 && mainWindow) {
      mainWindow.webContents.executeJavaScript(`
        console.warn("Backend process exited unexpectedly. Pipeline analysis may not work.");
      `);
    }
  });

  backendProcess.on("error", (error) => {
    console.error("❌ Failed to start backend:", error);
    if (mainWindow) {
      mainWindow.webContents.executeJavaScript(`
        console.error("Failed to start backend: ${error.message}");
        alert("Backend services failed to start. Please check that Python is installed.");
      `);
    }
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
