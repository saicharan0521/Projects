document
  .getElementById("predictionForm")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    // Show loading state
    const resultDiv = document.getElementById("result");
    const predictionValue = document.getElementById("predictionValue");
    const submitBtn = this.querySelector("button");
    const originalBtnText = submitBtn.textContent;

    submitBtn.textContent = "Predicting...";
    submitBtn.disabled = true;

    // Create FormData object
    const formData = new FormData(this);

    // Handle radio buttons properly
    // Property type
    const typeH = document.querySelector('input[name="type_h"]:checked');
    const typeT = document.querySelector('input[name="type_t"]:checked');
    formData.set("type_h", typeH ? typeH.value : "0");
    formData.set("type_t", typeT ? typeT.value : "0");

    // Method
    const methodPI = document.querySelector('input[name="method_pi"]:checked');
    const methodSP = document.querySelector('input[name="method_sp"]:checked');
    const methodVB = document.querySelector('input[name="method_vb"]:checked');
    formData.set("method_pi", methodPI ? methodPI.value : "0");
    formData.set("method_sp", methodSP ? methodSP.value : "0");
    formData.set("method_vb", methodVB ? methodVB.value : "0");

    // Region selections - get all checked region inputs
    const regionInputs = document.querySelectorAll('input[name^="region_"]');
    regionInputs.forEach((input) => {
      formData.set(input.name, input.checked ? "1" : "0");
    });

    try {
      const response = await fetch("/predict", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (data.success) {
        predictionValue.textContent = data.prediction;
        resultDiv.style.display = "block";

        // Scroll to result
        resultDiv.scrollIntoView({ behavior: "smooth", block: "nearest" });
      } else {
        alert("Error: " + data.error);
      }
    } catch (error) {
      alert("An error occurred. Please try again.");
      console.error("Error:", error);
    } finally {
      submitBtn.textContent = originalBtnText;
      submitBtn.disabled = false;
    }
  });
