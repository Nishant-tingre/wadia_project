document.addEventListener("DOMContentLoaded", () => {
    // DOM Elements Selection
    const symptomsInput = document.getElementById("symptoms-input");
    const analyzeBtn = document.getElementById("analyze-btn");
    const btnText = document.getElementById("btn-text");
    const btnSpinner = document.getElementById("btn-spinner");
    
    const welcomeState = document.getElementById("welcome-state");
    const resultsState = document.getElementById("results-state");
    
    const nlpCleaned = document.getElementById("nlp-cleaned");
    const nlpPrediction = document.getElementById("nlp-prediction");
    const nlpConfidenceLbl = document.getElementById("nlp-confidence-lbl");
    const nlpConfidenceBar = document.getElementById("nlp-confidence-bar");
    
    const mlMappedSymptoms = document.getElementById("ml-mapped-symptoms");
    const mlPrediction = document.getElementById("ml-prediction");
    const mlConfidenceLbl = document.getElementById("ml-confidence-lbl");
    const mlConfidenceBar = document.getElementById("ml-confidence-bar");
    
    const tipTags = document.querySelectorAll(".tip-tag");

    // Add suggested keywords to textarea when clicked
    tipTags.forEach(tag => {
        tag.addEventListener("click", () => {
            const currentVal = symptomsInput.value.strip ? symptomsInput.value.strip() : symptomsInput.value.trim();
            const tagText = tag.textContent;
            
            if (currentVal === "") {
                symptomsInput.value = tagText;
            } else {
                // If it ends with a comma, space, or letter
                if (currentVal.endsWith(",") || currentVal.endsWith(".") || currentVal.endsWith(" ")) {
                    symptomsInput.value = currentVal + (currentVal.endsWith(" ") ? "" : " ") + tagText;
                } else {
                    symptomsInput.value = currentVal + ", " + tagText;
                }
            }
            symptomsInput.focus();
        });
    });

    // Handle symptom analysis
    analyzeBtn.addEventListener("click", async () => {
        const symptomsText = symptomsInput.value.trim();
        
        if (!symptomsText) {
            alert("Please enter a description of your symptoms first.");
            symptomsInput.focus();
            return;
        }

        // Set Loading State
        analyzeBtn.disabled = true;
        btnText.classList.add("hidden");
        btnSpinner.classList.remove("hidden");

        try {
            // Call Flask backend prediction API
            const response = await fetch("/api/predict", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ symptoms: symptomsText })
            });

            if (!response.ok) {
                throw new Error("Prediction API request failed.");
            }

            const data = await response.json();
            displayResults(data);

        } catch (error) {
            console.error("Error analyzing symptoms:", error);
            alert("An error occurred while analyzing symptoms. Please ensure both models are trained by running `python src/train_all.py` first.");
        } finally {
            // Reset Button State
            analyzeBtn.disabled = false;
            btnText.classList.remove("hidden");
            btnSpinner.classList.add("hidden");
        }
    });

    // Render results on screen
    function displayResults(data) {
        // Toggle Panels
        welcomeState.classList.add("hidden");
        resultsState.classList.remove("hidden");

        // 1. Populate NLP Model Results
        if (data.nlp && data.nlp.success) {
            nlpCleaned.textContent = data.nlp.cleaned_text || "none";
            nlpPrediction.textContent = data.nlp.predicted_disease;
            
            // Animate confidence meter
            const confidencePercent = data.nlp.confidence * 100;
            animateMeter(nlpConfidenceBar, nlpConfidenceLbl, confidencePercent);
        } else {
            nlpCleaned.textContent = "N/A";
            nlpPrediction.textContent = "Model Not Trained";
            animateMeter(nlpConfidenceBar, nlpConfidenceLbl, 0);
        }

        // 2. Populate ML Model Results
        if (data.ml && data.ml.success) {
            mlMappedSymptoms.innerHTML = ""; // Clear old tags
            
            const mapped = data.ml.mapped_symptoms || [];
            if (mapped.length > 0) {
                mapped.forEach(symptom => {
                    const pill = document.createElement("span");
                    pill.className = "mapped-pill";
                    pill.textContent = symptom;
                    mlMappedSymptoms.appendChild(pill);
                });
            } else {
                const noSymptomMsg = document.createElement("span");
                noSymptomMsg.className = "no-mapped-pill";
                noSymptomMsg.textContent = "No symptom keywords matched.";
                mlMappedSymptoms.appendChild(noSymptomMsg);
            }

            if (data.ml.predicted_disease) {
                mlPrediction.textContent = data.ml.predicted_disease;
                const confidencePercent = data.ml.confidence * 100;
                animateMeter(mlConfidenceBar, mlConfidenceLbl, confidencePercent);
            } else {
                mlPrediction.textContent = "No Match";
                animateMeter(mlConfidenceBar, mlConfidenceLbl, 0);
            }
        } else {
            mlMappedSymptoms.innerHTML = `<span class="no-mapped-pill">Model Not Trained</span>`;
            mlPrediction.textContent = "Model Not Trained";
            animateMeter(mlConfidenceBar, mlConfidenceLbl, 0);
        }
    }

    // Function to animate meter width and count up label text
    function animateMeter(barElement, labelElement, targetValue) {
        // Set bar width
        barElement.style.width = `${targetValue}%`;
        
        // Counter animation for label
        let currentValue = 0;
        const duration = 1000; // 1 second animation duration
        const stepTime = 15; // update every 15ms
        const increment = targetValue / (duration / stepTime);
        
        const counterInterval = setInterval(() => {
            currentValue += increment;
            if (currentValue >= targetValue) {
                currentValue = targetValue;
                clearInterval(counterInterval);
            }
            labelElement.textContent = `${currentValue.toFixed(1)}%`;
        }, stepTime);
    }
});
