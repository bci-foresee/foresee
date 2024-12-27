let pipelineVisualization;

// Base nodes and edges for the pipeline, if backend fails to load
const defaultNodes = [
    {
        "color": "red",
        "id": "loader",
        "label": "Loader",
        "layer": 1,
        "x": 50,
        "y": 200
    },
    {
        "color": "black",
        "id": "node_1",
        "label": "BBF",
        "layer": 2,
        "x": 244,
        "y": 350
    }
];

const defaultEdges = [
    {
        "source": "loader",
        "target": "node_1"
    }
];

document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById("pipeline-viewer");
    const width = container.clientWidth;
    const height = 400; 

    pipelineVisualization = new PipelineVisualization("pipeline-viewer", width, height, false);
    
    const pipelineName = document.getElementById("selectedPipeline").textContent.replace(" Pipeline", "");
    
    Promise.all([
        fetch(`/pipeline/${pipelineName}/d3/nodes`).then(response => response.json()),
        fetch(`/pipeline/${pipelineName}/d3/edges`).then(response => response.json())
    ])
    .then(([nodes, edges]) => {
        pipelineVisualization.setData(
            nodes?.length > 0 ? nodes : defaultNodes,
            edges?.length > 0 ? edges : defaultEdges
        );
    })
    .catch(error => {
        console.error('Error loading pipeline data:', error);
        pipelineVisualization.setData(defaultNodes, defaultEdges);
    });
});

// Handle window resize
window.addEventListener('resize', () => {
    const container = document.getElementById("pipeline-viewer");
    const width = container.clientWidth;
    const height = 400;
    pipelineVisualization.resize(width, height);
}); 