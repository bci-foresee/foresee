const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("electronAPI", {
  getPipelines: () => ipcRenderer.invoke("getPipelines"),
  savePipeline: (name, description, graphData) => ipcRenderer.invoke("savePipeline", name, description, graphData),
  getPipelineById: (id) => ipcRenderer.invoke("getPipelineById", id),
  editPipeline: (id, name, description, graphData) => ipcRenderer.invoke("editPipeline", id, name, description, graphData),
});

