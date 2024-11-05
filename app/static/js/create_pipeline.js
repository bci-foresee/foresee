const container = document.getElementById("pipeline-creator");
const width = container.clientWidth;
const height = container.clientHeight;

var nodes = [];
var nodeElements;
var edges = [];
var edgeElements;
var simulation;
var currentSvg;

var sourceNodeSelected = false;
var selectedSourceNode;

var pes;
fetch('/pe.json')
    .then(response => response.json())
    .then(data => {
        pes = data;
    })
    .catch(error => {
        console.error('Error fetching JSON:', error);
    });

initializePipelineCreator(width, height);

currentSvg.on("dblclick", (event) => {
    var clickedNode = d3.select(event.target).datum();
    if (clickedNode) {
        sourceNodeSelected = true;
        selectedSourceNode = clickedNode;
        console.log("Source node selected:", clickedNode.id);
    } else {
        sourceNodeSelected = false;
        selectedSourceNode = null;
    }
});

currentSvg.on("click", (event) => {
    if (sourceNodeSelected) {
        const clickedNode = d3.select(event.target).datum();
        if (clickedNode) {
            const newEdge = {
                source: selectedSourceNode.id,
                target: clickedNode.id
            };
            edges.push(newEdge);

            nodes.forEach(node => {
                if (node.id === clickedNode.id) {
                  node.layer = selectedSourceNode.layer + 1;
                }
            });

            updateVisualization();
            sourceNodeSelected = false;
            selectedSourceNode = null;
            console.log("Edge created:", newEdge);
        } else {
            console.log("Invalid target node selection");
        }
    }
});

// Display menu with available PEs to add when the user right-clicks.
currentSvg.on("contextmenu", (event) => {
    event.preventDefault();
  
    const peMenu = document.createElement("div");
    peMenu.classList.add("context-menu");
    peMenu.style.left = event.clientX + "px";
    peMenu.style.top = event.clientY + "px";

    pes.forEach((pe, index) => {
        const peItem = document.createElement("div");
        peItem.textContent = pe.name;
        peItem.addEventListener("click", () => {
            addNode(peItem.textContent, event);
            peMenu.remove();
        });
        peMenu.appendChild(peItem);
      
        // Add a separator after each item except the last one
        if (index !== pes.length - 1) {
            const separator = document.createElement("hr");
            peMenu.appendChild(separator);
        }
    });
  
    document.body.appendChild(peMenu);
});

const pipelineNameInput = document.getElementById("pipeline-name");

document.getElementById("pipeline-save").addEventListener("click", () => {
  const pipelineName = pipelineNameInput.value;

  if (!pipelineName || pipelineName.trim() === "") {
      alert("Please enter a valid pipeline name.");
      return;
  }

  fetch('/create_pipeline', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({ 
        name: pipelineName,
        nodes: nodes,
        edges: edges
    })
  })
  .then(response => {
      if (response.ok) {
          console.log('Pipeline created successfully');
          location.reload();
      } else {
          console.error('Error creating pipeline:', response.statusText);
      }
  })
  .catch(error => {
      console.error('Error:', error);
  });
});

function initializePipelineCreator(width, height) {
    currentSvg = d3.select("#pipeline-creator")
        .append("svg")
        .attr("width", width)
        .attr("height", height);

    fetch('/create/nodes.json')
        .then(response => response.json())
        .then(data => {
            nodes = data;
            createNodes();
            fetch('/create/edges.json')
                .then(response => response.json())
                .then(data => {
                    edges = data;
                    createEdges();
                    initializeSimulation();
                })
                .catch(error => {
                    console.error('Error fetching JSON:', error);
                });
        })
        .catch(error => {
          console.error('Error fetching JSON:', error);
        });
}

function createNodes() {
    nodeElements = currentSvg.selectAll(".node")
        .data(nodes)
        .enter()
        .append("g")
        .call(d3.drag()
            .on("start", dragStarted)
            .on("drag", dragged)
            .on("end", dragEnded)
        );

    nodeElements.append("circle")
        .attr("r", 10)
        .attr("fill", d => d.color);

    nodeElements.append("text")
        .attr("text-anchor", "middle")
        .attr("dy", "2em")
        .text(d => d.label);
}

function createEdges() {
    edgeElements = currentSvg.selectAll(".link")
        .data(edges)
        .enter()
        .append("line")
        .attr("class", "link")
        .attr("stroke", "black")
        .attr("stroke-width", 2);
}

function filterNodes() {
    const filteredNodes = nodes.filter(node => {
        return edges.some(edge => edge.source === node.id || edge.target === node.id);
    });
    return filteredNodes;
}

function initializeSimulation() {
    // Filter out unconnected edges
    const filteredNodes = filterNodes();

    simulation = d3.forceSimulation(filteredNodes)
        .force("link", d3.forceLink().id(d => d.id).links(edges))
        .force("charge", d3.forceManyBody().strength(-100))
        .force("x", d3.forceX().x(d => d.layer * 150))
        .force("y", d3.forceY(300));

    simulation.on("tick", () => {
        nodeElements
        .attr("transform", d => {
            d.x = d.x;
            d.y = d.y;
            return `translate(${d.x},${d.y})`;
        });

        edgeElements
            .attr("x1", d => d.source.x)
            .attr("y1", d => d.source.y)
            .attr("x2", d => d.target.x)
            .attr("y2", d => d.target.y);
    });
}

function dragStarted(event, d) {
    if (!event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
}
  
function dragged(event, d) {
    d.fx = event.x;
    d.fy = event.y;
}
  
function dragEnded(event, d) {
    if (!event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
  
    // Check if the node is outside the screen
    if (d.x < 0 || d.x > currentSvg.attr("width") || d.y < 0 || d.y > currentSvg.attr("height")) {
        removeNode(d.id);
    }
}

function removeNode(nodeId) {
    nodes = nodes.filter(node => node.id !== nodeId);
    edges = edges.filter(edge => edge.source.id !== nodeId && edge.target.id !== nodeId);
    updateVisualization();
}

function addNode(nodeType, event) {
    const newNode = {
        id: `node_${nodes.length}`,
        label: nodeType, 
        color: "black",
        layer: 1,
        x: Math.max(0, Math.min(width - 50, event.clientX)),
        y: Math.max(0, Math.min(height - 50, event.clientY))
    };
    nodes.push(newNode);
    updateVisualization();
}

function updateVisualization() {
    console.log("Nodes");
    console.log(nodes);
    console.log(JSON.stringify(nodes));
    fetch('/create/update_nodes', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(nodes)
    })
    .then(response => {
        if (response.ok) {
            console.log('Nodes updates successfully');
            
            console.log(edges)

            const edgesData = edges.map(edge => ({
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
                    console.log('Edges updates successfully');
                    location.reload();
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
