document.addEventListener("DOMContentLoaded", function() {
    const textElement = document.getElementById("selectedPipeline");
    const textContent = textElement.textContent.replace(/_/g, " ");
    textElement.textContent = textContent;
});

// Makes the customPath option visible if selected.
document.addEventListener("DOMContentLoaded", function() {
    const customElement = document.getElementById("custom");

    if (customElement) {
        customElement.addEventListener("change", function() {
            var customPathDiv = document.getElementById("customPath");
            if (this.checked) {
                customPathDiv.style.display = "block";
            } else {
                customPathDiv.style.display = "none";
            }
        });
    } else {
        console.error("Element with ID 'custom' not found.");
    }
});

fetch('/dummy_data')
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            console.error("Error from Flask:", data.error);
            return;
        }
        data.forEach(d => {
            d.Accuracy = +d.Accuracy;
            d.Latency = +d.Latency;
            d.Power = +d.Power;
            });
        createVisualizations(data);
    })
    .catch(error => console.error('Error fetching data:', error));

function createVisualizations(data){
    createAccuracyVisualization(data);
    createLatencyVisualization(data);
    createPowerVisualization(data);
}

function createAccuracyVisualization(data) {
    const tooltip = d3.select(".tooltip");
    const accuracyMargin = {top: 20, right: 30, bottom: 30, left: 40},
        accuracyWidth = 400 - accuracyMargin.left - accuracyMargin.right,
        accuracyHeight = 300 - accuracyMargin.top - accuracyMargin.bottom;

    d3.select(`#latestAccuracyVis svg`).remove();

    const accuracySvg = d3.select("#latestAccuracyVis").append("svg")
        .attr("width", accuracyWidth + accuracyMargin.left + accuracyMargin.right)
        .attr("height", accuracyHeight + accuracyMargin.top + accuracyMargin.bottom)
    .append("g")
        .attr("transform", "translate(" + accuracyMargin.left + "," + accuracyMargin.top + ")");

    const xAccuracy = d3.scaleBand()
        .rangeRound([0, accuracyWidth])
        .padding(0.1)
        .domain(data.map(d => d.PE));

    const yAccuracy = d3.scaleLinear()
        .rangeRound([accuracyHeight, 0])
        .domain([0, 100]);

    const accuracyExtent = d3.extent(data, d => d.Accuracy);
    const accuracyColorScale = d3.scaleLinear()
        .domain(accuracyExtent)
        .range(["lightblue", "darkblue"]);

    accuracySvg.selectAll(".bar")
    .data(data)
    .enter().append("rect")
        .attr("class", "bar")
        .attr("x", d => xAccuracy(d.PE))
        .attr("y", d => yAccuracy(d.Accuracy))
        .attr("height", d => accuracyHeight - yAccuracy(d.Accuracy))
        .attr("width", xAccuracy.bandwidth())
        .attr("fill", d => accuracyColorScale(d.Accuracy));

    accuracySvg.append("g")
        .attr("transform", "translate(0," + accuracyHeight + ")")
        .call(d3.axisBottom(xAccuracy));

    accuracySvg.append("g")
        .call(d3.axisLeft(yAccuracy));

    accuracySvg.selectAll(".bar")
    .on("mouseover", function(event, d) {
        tooltip.transition()
            .duration(200)
            .style("opacity", .9);
        tooltip.html("PE: " + d.PE + "<br>Accuracy: " + d.Accuracy)
            .style("left", (event.pageX) + "px")
            .style("top", (event.pageY - 28) + "px");
    })
    .on("mouseout", function(event, d) {
        tooltip.transition()
            .duration(500)
            .style("opacity", 0);
    });
}

function createLatencyVisualization(data) {
    const tooltip = d3.select(".tooltip");
    const latencyMargin = {top: 20, right: 30, bottom: 30, left: 40},
        latencyWidth = 400 - latencyMargin.left - latencyMargin.right,
        latencyHeight = 300 - latencyMargin.top - latencyMargin.bottom;
    
    d3.select(`#latestLatencyVis svg`).remove();

    const latencySvg = d3.select("#latestLatencyVis").append("svg")
        .attr("width", latencyWidth + latencyMargin.left + latencyMargin.right)
        .attr("height", latencyHeight + latencyMargin.top + latencyMargin.bottom)
    .append("g")
        .attr("transform", "translate(" + latencyMargin.left + "," + latencyMargin.top + ")");

    const xLatency = d3.scaleBand()
        .rangeRound([0, latencyWidth])
        .padding(0.1)
        .domain(data.map(d => d.PE));

    const yLatency = d3.scaleLinear()
        .rangeRound([latencyHeight, 0])
        .domain([0, d3.max(data, d => d.Latency)]);

    const latencyExtent = d3.extent(data, d => d.Latency);
    const latencyColorScale = d3.scaleLinear()
        .domain(latencyExtent.reverse())
        .range(["lightblue", "darkblue"]);

    latencySvg.selectAll(".bar")
    .data(data)
    .enter().append("rect")
        .attr("class", "bar")
        .attr("x", d => xLatency(d.PE))
        .attr("y", d => yLatency(d.Latency))
        .attr("height", d => latencyHeight - yLatency(d.Latency))
        .attr("width", xLatency.bandwidth())
        .attr("fill", d => latencyColorScale(d.Latency));

    latencySvg.append("g")
        .attr("transform", "translate(0," + latencyHeight + ")")
        .call(d3.axisBottom(xLatency));

    latencySvg.append("g")
        .call(d3.axisLeft(yLatency));

    latencySvg.selectAll(".bar")
    .on("mouseover", function(event, d) {
        tooltip.transition()
            .duration(200)
            .style("opacity", .9);
        tooltip.html("PE: " + d.PE + "<br>Latency: " + d.Latency)
            .style("left", (event.pageX) + "px")
            .style("top", (event.pageY - 28) + "px");
    })
    .on("mouseout", function(event, d) {
        tooltip.transition()
            .duration(500)
            .style("opacity", 0);
    });
}

function createPowerVisualization(data) {
    const tooltip = d3.select(".tooltip");
    const powerMargin = {top: 20, right: 20, bottom: 20, left: 20},
        powerWidth = 300 - powerMargin.left - powerMargin.right,
        powerHeight = 300 - powerMargin.top - powerMargin.bottom,
        radius = Math.min(powerWidth, powerHeight) / 2;
    
    d3.select(`#latestPowerVis svg`).remove();

    const powerSvg = d3.select("#latestPowerVis").append("svg")
        .attr("width", powerWidth + powerMargin.left + powerMargin.right)
        .attr("height", powerHeight + powerMargin.top + powerMargin.bottom)
    .append("g")
        .attr("transform", "translate(" + (powerWidth / 2 + powerMargin.left) + "," + (powerHeight / 2 + powerMargin.top) + ")");

    const powerExtent = d3.extent(data, d => d.Power);
    const powerColorScale = d3.scaleLinear()
        .domain(powerExtent)
        .range(["lightblue", "darkblue"]);

    const pie = d3.pie()
        .value(d => d.Power);

    const arc = d3.arc()
        .outerRadius(radius - 10)
        .innerRadius(0);

    const arcs = powerSvg.selectAll(".arc")
    .data(pie(data))
    .enter().append("g")
        .attr("class", "arc");

    arcs.append("path")
        .attr("d", arc)
        .attr("fill", d => powerColorScale(d.data.Power));

    arcs.append("text")
        .attr("transform", d => "translate(" + arc.centroid(d) + ")")
        .attr("dy", ".35em")
        .text(d => d.data.PE);

    arcs.on("mouseover", function(event, d) {
        tooltip.transition()
            .duration(200)
            .style("opacity", .9);
        tooltip.html("PE: " + d.data.PE + "<br>Power: " + d.data.Power)
            .style("left", (event.pageX) + "px")
            .style("top", (event.pageY - 28) + "px");
    })
    .on("mouseout", function(event, d) {
        tooltip.transition()
            .duration(500)
            .style("opacity", 0);
    });
}
