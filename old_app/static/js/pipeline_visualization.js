class PipelineVisualization {
    constructor(containerId, width, height, isEditable = false) {
        this.container = document.getElementById(containerId);
        this.width = width || this.container.clientWidth;
        this.height = height || this.container.clientHeight;
        this.isEditable = isEditable;
        
        this.nodes = [];
        this.edges = [];
        this.simulation = null;
        this.svg = null;
        this.nodeElements = null;
        this.edgeElements = null;
        
        // Event handlers
        this.onNodeClick = null;
        this.onNodeDoubleClick = null;
        
        this.initializeVisualization();
    }
    
    initializeVisualization() {
        this.svg = d3.select(`#${this.container.id}`)
            .append("svg")
            .attr("width", this.width)
            .attr("height", this.height);

        // Grid pattern
        this.createGrid(this.width, this.height, 50);

        this.svg.append("g").attr("class", "edges-container");
        this.svg.append("g").attr("class", "nodes-container");
    }

    createGrid(width, height, gridSize) {
        const numHorizontalLines = Math.ceil(height / gridSize);
        const numVerticalLines = Math.ceil(width / gridSize);

        this.svg.select(".grid").remove();

        const grid = this.svg.insert("g", ":first-child")
            .attr("class", "grid");
        
        for (let i = 0; i <= numVerticalLines; i++) {
            grid.append("line")
                .attr("x1", i * gridSize)
                .attr("y1", 0)
                .attr("x2", i * gridSize)
                .attr("y2", height);
        }

        for (let i = 0; i <= numHorizontalLines; i++) {
            grid.append("line")
                .attr("x1", 0)
                .attr("y1", i * gridSize)
                .attr("x2", width)
                .attr("y2", i * gridSize);
        }
    }

    setData(nodes, edges) {
        this.nodes = nodes;
        this.edges = edges;
        this.createVisualization();
    }

    createVisualization() {
        if (this.simulation) {
            this.simulation.stop();
        }

        // Update nodes
        this.nodeElements = this.svg.select(".nodes-container")
            .selectAll(".node")
            .data(this.nodes, d => d.id);

        // Remove old nodes
        this.nodeElements.exit().remove();

        // Create new nodes
        const nodeEnter = this.nodeElements.enter()
            .append("g")
            .attr("class", "node");

        if (this.isEditable) {
            nodeEnter.call(d3.drag()
                .on("start", (event, d) => this.dragStarted(event, d))
                .on("drag", (event, d) => this.dragged(event, d))
                .on("end", (event, d) => this.dragEnded(event, d))
            );
        }

        // Add circle and bind events to it
        const circles = nodeEnter.append("circle")
            .attr("r", 15)
            .attr("fill", d => d.color);

        if (this.onNodeClick) {
            circles.on("click", (event, d) => {
                event.stopPropagation();
                this.onNodeClick(event, d);
            });
        }

        if (this.onNodeDoubleClick) {
            circles.on("dblclick", (event, d) => {
                event.stopPropagation();
                this.onNodeDoubleClick(event, d);
            });
        }

        nodeEnter.append("text")
            .attr("text-anchor", "middle")
            .attr("dy", "2em")
            .text(d => d.label);

        // Merge enter + update selections
        this.nodeElements = nodeEnter.merge(this.nodeElements);

        // Update existing nodes' event handlers
        if (this.onNodeClick) {
            this.nodeElements.select("circle")
                .on("click", (event, d) => {
                    event.stopPropagation();
                    this.onNodeClick(event, d);
                });
        }

        if (this.onNodeDoubleClick) {
            this.nodeElements.select("circle")
                .on("dblclick", (event, d) => {
                    event.stopPropagation();
                    this.onNodeDoubleClick(event, d);
                });
        }

        // Update edges with proper id handling
        this.edgeElements = this.svg.select(".edges-container")
            .selectAll(".link")
            .data(this.edges, d => {
                const sourceId = d.source.id ? d.source.id : d.source;
                const targetId = d.target.id ? d.target.id : d.target;
                return `${sourceId}-${targetId}`;
            });

        this.edgeElements.exit().remove();

        const edgeEnter = this.edgeElements.enter()
            .append("line")
            .attr("class", "link")
            .attr("stroke", "black")
            .attr("stroke-width", 2);

        this.edgeElements = edgeEnter.merge(this.edgeElements);

        // Initialize or restart simulation with proper link initialization
        if (this.simulation) {
            this.simulation.nodes(this.nodes);
            this.simulation.force("link").links(this.edges);
            this.simulation.alpha(1).restart();
        } else {
            this.initializeSimulation();
        }
    }

    initializeSimulation() {
        if (this.simulation) {
            this.simulation.stop();
        }

        this.simulation = d3.forceSimulation(this.nodes)
            .force("link", d3.forceLink(this.edges).id(d => d.id))
            .force("charge", d3.forceManyBody().strength(-100))
            .force("x", d3.forceX().x(d => {
                const centerX = this.width / 2;
                const maxLayer = Math.max(...this.nodes.map(n => n.layer));
                const offset = (maxLayer - 1) * 75;
                return centerX - offset + (d.layer - 1) * 150;
            }).strength(0.5))
            .force("y", d3.forceY(this.height / 2).strength(0.3));

        this.simulation.on("tick", () => {
            this.nodeElements
                .attr("transform", d => `translate(${d.x},${d.y})`);

            this.edgeElements
                .attr("x1", d => d.source.x)
                .attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x)
                .attr("y2", d => d.target.y);
        });
    }

    dragStarted(event, d) {
        if (!event.active) this.simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    }
    
    dragged(event, d) {
        d.fx = event.x;
        d.fy = event.y;
    }
    
    dragEnded(event, d) {
        if (!event.active) this.simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;

        // Remove node if outside the screen
        if (this.isEditable) {
            if (d.x < 0 || d.x > this.width || d.y < 0 || d.y > this.height) {
                this.nodes = this.nodes.filter(node => node.id !== d.id);
                this.edges = this.edges.filter(edge => 
                    (edge.source.id || edge.source) !== d.id && 
                    (edge.target.id || edge.target) !== d.id
                );
                this.createVisualization();
            }
        }
    }

    resize(width, height) {
        this.width = width;
        this.height = height;
        
        this.svg
            .attr("width", width)
            .attr("height", height);
        
        this.createGrid(width, height, 50);
            
        this.simulation.force("x", d3.forceX().x(d => {
            const centerX = width / 2;
            const maxLayer = Math.max(...this.nodes.map(n => n.layer));
            const offset = (maxLayer - 1) * 75;
            return centerX - offset + (d.layer - 1) * 150;
        }).strength(0.5))
        .force("y", d3.forceY(height / 2).strength(0.3));
        
        this.simulation.alpha(1).restart();
    }

    setNodeClickHandler(handler) {
        this.onNodeClick = handler;
        if (this.nodeElements) {
            this.nodeElements.select("circle")
                .on("click", (event, d) => {
                    event.stopPropagation();
                    handler(event, d);
                });
        }
    }

    setNodeDoubleClickHandler(handler) {
        this.onNodeDoubleClick = handler;
        if (this.nodeElements) {
            this.nodeElements.select("circle")
                .on("dblclick", (event, d) => {
                    event.stopPropagation();
                    handler(event, d);
                });
        }
    }
} 