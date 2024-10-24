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

// Function to dynamically populate pipeline options from the CSV
function populatePipelineOptionsFromCSV(csvFilePath) {
    fetch(csvFilePath)
        .then(response => response.text())
        .then(text => {
            const lines = text.split('\n');
            const pipelineSelect = document.getElementById("pipeline");
  
            lines.forEach(line => {
                const pipeline = line.trim();
                if (pipeline !== '') {
                    const option = document.createElement("option");
                    option.value = pipeline;
                    option.text = pipeline;
                    pipelineSelect.appendChild(option);
                }
            });
        })
        .catch(error => {
            console.error("Error fetching CSV file:", error);
        });
  }
