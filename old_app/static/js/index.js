document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("selectPipeline").addEventListener("change", function() {
        var selectPipelineValue = this.value.toLowerCase().replace(/\s+/g, "_");
        if (selectPipelineValue) {
            document.getElementById("selectPipelineForm").submit();
        }
    });

    populateAvailablePipelines();
});

function populateAvailablePipelines() {
    fetch('/available_pipelines')
        .then(response => response.json())
        .then(pipelines => {
            const pipelineSelect = document.getElementById("selectPipeline");
            
            const emptyOption = document.createElement("option");
            emptyOption.value = "";
            emptyOption.text = "";
            pipelineSelect.appendChild(emptyOption);
            
            pipelines.forEach(pipeline => {
                const option = document.createElement("option");
                // Convert snake_case to Title Case for display
                option.value = pipeline;
                option.text = pipeline.split('_').map(word => 
                    word.charAt(0).toUpperCase() + word.slice(1)
                ).join(' ');
                pipelineSelect.appendChild(option);
            });
        })
        .catch(error => {
            console.error("Error fetching pipelines:", error);
        });
}
