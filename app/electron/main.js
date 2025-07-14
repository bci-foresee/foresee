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

  console.log(`🚀 Starting backend with conda environment: ${condaEnvName} (${app.isPackaged ? 'packaged' : 'development'} mode)`);
  console.log(`📁 Backend script: ${backendScript}`);

  // Set working directory to backend directory
  const backendDir = path.dirname(backendScript);
  
  // Create conda activation command for Unix systems (macOS/Linux)
  const isWindows = process.platform === 'win32';
  let command, args;
  
  // Use the same robust conda activation for both development and packaged modes
  if (isWindows) {
    // Windows conda activation
    command = 'cmd';
    args = ['/c', `conda activate ${condaEnvName} && python ${path.basename(backendScript)}`];
  } else {
    // Unix conda activation (macOS/Linux) - same logic for both dev and packaged
    command = 'bash';
    const isPackagedFlag = app.isPackaged ? "true" : "false";
    const resourcesPath = app.isPackaged ? process.resourcesPath : "";
    args = ['-c', `
      source ~/.bash_profile 2>/dev/null || true
      source ~/.bashrc 2>/dev/null || true
      
      # Try multiple conda initialization paths (same as development mode)
      CONDA_INIT_SUCCESS=false
      if [ -f "$HOME/anaconda3/bin/conda" ]; then
        echo "🔧 Found conda at: $HOME/anaconda3/bin/conda"
        eval "$($HOME/anaconda3/bin/conda shell.bash hook)"
        export PATH="$HOME/anaconda3/bin:$PATH"
        CONDA_INIT_SUCCESS=true
      elif [ -f "$HOME/miniconda3/bin/conda" ]; then
        echo "🔧 Found conda at: $HOME/miniconda3/bin/conda"
        eval "$($HOME/miniconda3/bin/conda shell.bash hook)"
        export PATH="$HOME/miniconda3/bin:$PATH"
        CONDA_INIT_SUCCESS=true
      elif [ -f "/opt/anaconda3/bin/conda" ]; then
        echo "🔧 Found conda at: /opt/anaconda3/bin/conda"
        eval "$(/opt/anaconda3/bin/conda shell.bash hook)"
        export PATH="/opt/anaconda3/bin:$PATH"
        CONDA_INIT_SUCCESS=true
      elif [ -f "/opt/miniconda3/bin/conda" ]; then
        echo "🔧 Found conda at: /opt/miniconda3/bin/conda"
        eval "$(/opt/miniconda3/bin/conda shell.bash hook)"
        export PATH="/opt/miniconda3/bin:$PATH"
        CONDA_INIT_SUCCESS=true
      elif command -v conda > /dev/null 2>&1; then
        echo "🔧 Found conda in PATH: $(which conda)"
        eval "$(conda shell.bash hook)"
        CONDA_INIT_SUCCESS=true
      else
        echo "❌ Conda not found - only conda environments are supported"
        echo "Please ensure conda is installed and ${condaEnvName} environment exists"
        exit 1
      fi
      
      if [ "$CONDA_INIT_SUCCESS" = "true" ]; then
        echo "🔄 Activating conda environment: ${condaEnvName}"
        # Ensure conda is properly initialized before activation
        conda info --envs
        if conda activate ${condaEnvName}; then
        echo "🐍 Using Python: $(which python)"
        echo "🔧 Environment check for packaged mode:"
        echo "  PATH: $PATH"
        echo "  CONDA_DEFAULT_ENV: $CONDA_DEFAULT_ENV"
        echo "  CONDA_PREFIX: $CONDA_PREFIX"
        echo "  Python location: $(which python)"
        echo "  iverilog available: $(which iverilog || echo 'NOT FOUND')"
        echo "  vvp available: $(which vvp || echo 'NOT FOUND')"
        echo "  yosys available: $(which yosys || echo 'NOT FOUND')"
        
        # Add packaged iverilog binaries to PATH if in packaged mode
        if [ "${isPackagedFlag}" = "true" ]; then
          echo "📦 Packaged mode detected - adding iverilog binaries to PATH"
          PACKAGED_BIN_PATH="${resourcesPath}/app/bin"
          if [ -d "$PACKAGED_BIN_PATH" ]; then
            export PATH="$PACKAGED_BIN_PATH:$PATH"
            echo "✅ Added $PACKAGED_BIN_PATH to PATH"
            echo "  Updated PATH: $PATH"
            echo "  iverilog available: $(which iverilog || echo 'NOT FOUND')"
            echo "  vvp available: $(which vvp || echo 'NOT FOUND')"
          else
            echo "⚠️  Warning: Could not find packaged binaries at $PACKAGED_BIN_PATH"
          fi
        fi
        
        echo "🚀 Starting Flask server with full conda environment..."
        python ${path.basename(backendScript)}
              else
          echo "❌ Failed to activate conda environment: ${condaEnvName}"
          echo "Only conda environments are supported. Please ensure ${condaEnvName} exists and is properly configured."
          exit 1
        fi
      else
        echo "❌ Conda initialization failed"
        echo "Please ensure conda is properly installed and accessible"
        exit 1
      fi
    `];
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
