let pipelineVisualization;
let pes;
let sourceNodeSelected = false;
let selectedSourceNode;
let configPanel;
let selectedNode;

// Base nodes and edges for the pipeline, if backend fails to load
const baseNodes = [
    {
        "color": "red",
        "id": "loader",
        "label": "Loader",
        "layer": 1,
        "x": 50,
        "y": 200,
        "fx": null,
        "fy": null
    },
    {
        "color": "black",
        "id": "node_1",
        "label": "BBF",
        "layer": 2,
        "x": 244,
        "y": 350,
        "fx": null,
        "fy": null
    }
];

const baseEdges = [
    {
        "source": "loader",
        "target": "node_1"
    }
];

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById("pipeline-creator");
    const width = container.clientWidth;
    const height = container.clientHeight;

    pipelineVisualization = new PipelineVisualization("pipeline-creator", width, height, true);
    
    // Load PEs data
    fetch('/pe.json')
        .then(response => response.json())
        .then(data => {
            pes = data;
        })
        .catch(error => {
            console.error('Error fetching JSON:', error);
        });

    // Load initial pipeline data
    fetch('/create/nodes.json')
        .then(response => response.json())
        .then(nodes => {
            fetch('/create/edges.json')
                .then(response => response.json())
                .then(edges => {
                    pipelineVisualization.setData(nodes, edges);
                    setupEventHandlers();
                })
                .catch(error => {
                    console.error('Error fetching edges:', error);
                    pipelineVisualization.setData(baseNodes, baseEdges);
                    setupEventHandlers();
                });
        })
        .catch(error => {
            console.error('Error fetching nodes:', error);
            pipelineVisualization.setData(baseNodes, baseEdges);
            setupEventHandlers();
        });
});

function setupEventHandlers() {
    const svg = pipelineVisualization.svg;

    pipelineVisualization.setNodeDoubleClickHandler((event, clickedNode) => {
        if (sourceNodeSelected) {
            sourceNodeSelected = false;
            selectedSourceNode = null;
            svg.selectAll("circle").classed("selected-source", false);
            closeConfigPanel();
        } else {
            sourceNodeSelected = true;
            selectedSourceNode = clickedNode;
            svg.selectAll("circle").classed("selected-source", false);
            d3.select(event.target).classed("selected-source", true);
            showConfigPanel(clickedNode);
        }
    });

    pipelineVisualization.setNodeClickHandler((event, clickedNode) => {
        if (sourceNodeSelected && clickedNode !== selectedSourceNode) {
            const newEdge = {
                source: selectedSourceNode.id,
                target: clickedNode.id
            };

            pipelineVisualization.nodes.forEach(node => {
                if (node.id === clickedNode.id) {
                    node.layer = selectedSourceNode.layer + 1;
                }
            });

            pipelineVisualization.edges.push(newEdge);
            
            svg.selectAll("circle").classed("selected-source", false);
            closeConfigPanel();
            
            updateVisualization();
            sourceNodeSelected = false;
            selectedSourceNode = null;
            console.log("Edge created:", newEdge);
        }
    });

    // Context menu for adding nodes
    var activeContextMenu = null;

    svg.on("contextmenu", (event) => {
        event.preventDefault();
        
        if (activeContextMenu) {
            activeContextMenu.remove();
        }
    
        const peMenu = document.createElement("div");
        peMenu.classList.add("context-menu");
        peMenu.style.left = event.clientX + "px";
        peMenu.style.top = event.clientY + "px";

        activeContextMenu = peMenu;

        const closeMenu = (e) => {
            if (!peMenu.contains(e.target)) {
                peMenu.remove();
                document.removeEventListener('click', closeMenu);
                activeContextMenu = null;
            }
        };
        document.addEventListener('click', closeMenu);

        pes.forEach((pe, index) => {
            const peItem = document.createElement("div");
            peItem.textContent = pe.acronym;
            peItem.addEventListener("click", () => {
                addNode(peItem.textContent, event);
                peMenu.remove();
                activeContextMenu = null;
            });
            peMenu.appendChild(peItem);
        
            if (index !== pes.length - 1) {
                const separator = document.createElement("hr");
                peMenu.appendChild(separator);
            }
        });
    
        document.body.appendChild(peMenu);
    });

    // Save pipeline
    document.getElementById("pipeline-save").addEventListener("click", () => {
        const pipelineName = document.getElementById("pipeline-name").value;

        if (!pipelineName || pipelineName.trim() === "") {
            alert("Please enter a valid pipeline name.");
            return;
        }

        fetch('/save_new_pipeline', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                name: pipelineName,
                nodes: pipelineVisualization.nodes,
                edges: pipelineVisualization.edges
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Pipeline created successfully');
            alert('Pipeline saved successfully!');
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to save pipeline. Please try again.');
        });
    });

    // Reset pipeline
    document.getElementById("pipeline-reset").addEventListener("click", () => {
        fetch('/create_default/nodes.json')
            .then(response => response.json())
            .then(nodes => {
                fetch('/create_default/edges.json')
                    .then(response => response.json())
                    .then(edges => {
                        pipelineVisualization.setData(nodes, edges);
                        document.getElementById("pipeline-name").value = "";
                        sourceNodeSelected = false;
                        selectedSourceNode = null;
                        svg.selectAll("circle").classed("selected-source", false);
                        // Update the working state files after reset
                        updateVisualization();
                    })
                    .catch(error => {
                        console.error('Error fetching edges:', error);
                    });
            })
            .catch(error => {
                console.error('Error fetching nodes:', error);
            });
    });

    // Handle window resize
    window.addEventListener('resize', () => {
        const width = window.innerWidth;
        const height = window.innerHeight;
        pipelineVisualization.resize(width, height);
    });
}

function addNode(nodeType, event) {
    const [sx, sy] = d3.pointer(event, pipelineVisualization.svg.node());
    const x = Math.max(0, Math.min(pipelineVisualization.width - 50, sx));
    const y = Math.max(0, Math.min(pipelineVisualization.height - 50, sy));
    
    const peConfig = pes.find(pe => pe.acronym === nodeType);
    const defaultConfig = {};
    
    if (peConfig) {
        peConfig.configOptions.forEach(option => {
            defaultConfig[option.acronym] = option.default;
        });
    }

    const newNode = {
        id: `node_${pipelineVisualization.nodes.length}`,
        label: nodeType,
        color: "black",
        layer: 1,
        x: x,
        y: y,
        config: defaultConfig
    };
    
    pipelineVisualization.nodes.push(newNode);
    updateVisualization();
}

function updateVisualization() {
    fetch('/create/update_nodes', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(pipelineVisualization.nodes)
    })
    .then(response => {
        if (response.ok) {
            console.log('Nodes updated successfully');
            
            const edgesData = pipelineVisualization.edges.map(edge => ({
                source: edge.source.id ? edge.source.id : edge.source,
                target: edge.target.id ? edge.target.id : edge.target
            }));
            
            fetch('/create/update_edges', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(edgesData)
            })
            .then(response => {
                if (response.ok) {
                    console.log('Edges updated successfully');
                    pipelineVisualization.createVisualization();
                } else {
                    console.error('Error updating edges');
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        } else {
            console.error('Error updating nodes');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function initializeConfigPanel() {
    const panel = document.createElement('div');
    panel.className = 'pe-config-panel';
    document.body.appendChild(panel);
    return panel;
}

function showConfigPanel(node) {
    const panel = document.querySelector('.pe-config-panel');
    const peConfig = pes.find(pe => pe.acronym === node.label);
    
    if (!peConfig) return;
    
    selectedNode = node;
    
    panel.querySelector('.config-title').textContent = `${node.label} Configuration`;
    
    const formContent = panel.querySelector('.form-content');
    formContent.innerHTML = peConfig.configOptions
        .map(option => `
            <div class="form-group">
                <label for="config-${option.name}">${option.label}:</label>
                <input type="${option.type}" 
                       id="config-${option.name}" 
                       value="${node.config?.[option.name] ?? option.default}">
            </div>
        `).join('');
    
    panel.querySelector('.save-btn').onclick = saveConfig;
    panel.querySelector('.close-btn').onclick = closeConfigPanel;
    
    panel.classList.add('active');
}

function saveConfig() {
    if (!selectedNode) return;
    
    const peConfig = pes.find(pe => pe.acronym === selectedNode.label);
    if (!peConfig) return;
    
    const config = {};
    
    peConfig.configOptions.forEach(option => {
        const input = document.getElementById(`config-${option.acronym}`);
        if (option.type === 'number') {
            config[option.acronym] = parseInt(input.value);
        } else {
            config[option.acronym] = input.value;
        }
    });
    
    selectedNode.config = config;
    closeConfigPanel();
}

function closeConfigPanel() {
    document.querySelector('.pe-config-panel').classList.remove('active');
    pipelineVisualization.svg.selectAll("circle").classed("selected-source", false);
    sourceNodeSelected = false;
    selectedSourceNode = null;
    selectedNode = null;
}