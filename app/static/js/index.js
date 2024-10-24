document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("selectPipeline").addEventListener("change", function() {
        var selectPipelineValue = this.value.toLowerCase().replace(/\s+/g, "_");
        if (selectPipelineValue) {
            document.getElementById("selectPipelineForm").submit();
        }
    })
});

// Function to dynamically populate pipeline options from the CSV
function populatePipelineOptionsFromCSV(csvFilePath) {
    fetch(csvFilePath)
        .then(response => response.text())
        .then(text => {
            const lines = text.split('\n');
            const pipelineSelect = document.getElementById("selectPipeline");
            const option = document.createElement("option");
            option.value = "";
            option.text = "";
            pipelineSelect.appendChild(option);
  
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
