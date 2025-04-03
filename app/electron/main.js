const { app, BrowserWindow, ipcMain } = require("electron");
const path = require("path");
const {
  savePipeline,
  getPipelines,
  getPipelineById,
  editPipeline,
  deletePipeline,
} = require("./database"); // ✅ Import database functions

let mainWindow;

app.whenReady().then(() => {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      preload: path.join(__dirname, "preload.js"), // Securely expose database functions
      nodeIntegration: false, // Keep Node.js disabled in the renderer for security
      contextIsolation: true, // Required for secure IPC communication
    },
  });

  const devServerURL = "http://localhost:3000"; // Dev mode
  const prodServerURL = `file://${path.join(__dirname, "../out/index.html")}`; // Production

  mainWindow.loadURL(app.isPackaged ? prodServerURL : devServerURL);

  mainWindow.on("closed", () => {
    mainWindow = null;
  });

  // 💾 IPC handlers for SQLite database access
  ipcMain.handle("getPipelines", () => getPipelines());
  ipcMain.handle("savePipeline", (event, name, description, graphData) => {
    savePipeline(name, description, graphData);
    return "Pipeline saved!";
  });
  ipcMain.handle("getPipelineById", async (event, id) => getPipelineById(id));
  ipcMain.handle("editPipeline", async (event, id, name, description, graphData) =>
    editPipeline(id, name, description, graphData)
  );
  ipcMain.handle("deletePipeline", async (event, id) => deletePipeline(id));
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});
