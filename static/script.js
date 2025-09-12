document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("pathlossForm")
  const resultsSection = document.getElementById("results")
  const errorDiv = document.getElementById("error")
  const predictBtn = form.querySelector(".predict-btn")
  const btnText = predictBtn.querySelector(".btn-text")
  const btnLoading = predictBtn.querySelector(".btn-loading")

  form.addEventListener("submit", async (e) => {
    e.preventDefault()

    // Clear previous results and errors
    hideResults()
    hideError()

    // Show loading state
    showLoading()

    try {
      const formData = new FormData(form)

      const response = await fetch("/predict", {
        method: "POST",
        body: formData,
      })

      const data = await response.json()

      if (data.error) {
        showError(data.error)
      } else {
        showResults(data)
      }
    } catch (error) {
      console.error("Error:", error)
      showError("Network error. Please check your connection and try again.")
    } finally {
      hideLoading()
    }
  })

  function showLoading() {
    predictBtn.disabled = true
    btnText.style.display = "none"
    btnLoading.style.display = "inline-block"
  }

  function hideLoading() {
    predictBtn.disabled = false
    btnText.style.display = "inline-block"
    btnLoading.style.display = "none"
  }

  function showResults(data) {
    document.getElementById("pathlossValue").textContent = data.pathloss
    document.getElementById("usedModel").textContent = data.model
    document.getElementById("usedEnvironment").textContent = data.parameters.environment

    const parametersList = document.getElementById("parametersList")
    parametersList.innerHTML = `
            <li><strong>Frequency:</strong> ${data.parameters.frequency} MHz</li>
            <li><strong>Distance:</strong> ${data.parameters.distance} km</li>
            <li><strong>TX Height:</strong> ${data.parameters.tx_height} m</li>
            <li><strong>RX Height:</strong> ${data.parameters.rx_height} m</li>
        `

    resultsSection.style.display = "block"
    resultsSection.scrollIntoView({ behavior: "smooth" })
  }

  function showError(message) {
    errorDiv.textContent = message
    errorDiv.style.display = "block"
    errorDiv.scrollIntoView({ behavior: "smooth" })
  }

  function hideResults() {
    resultsSection.style.display = "none"
  }

  function hideError() {
    errorDiv.style.display = "none"
  }

  // Input validation
  const numericInputs = form.querySelectorAll('input[type="number"]')
  numericInputs.forEach((input) => {
    input.addEventListener("input", function () {
      if (this.value < 0) {
        this.value = ""
      }
    })
  })

  // Add tooltips for model selection
  const modelSelect = document.getElementById("model")
  modelSelect.addEventListener("change", function () {
    const selectedOption = this.options[this.selectedIndex]
    if (selectedOption.value) {
      let tooltip = ""
      switch (selectedOption.value) {
        case "ECC-33":
          tooltip = "Best for cellular networks, frequency range 30 MHz - 3 GHz"
          break
        case "SUI":
          tooltip = "Optimized for wireless communications, frequency range 1.9 - 11 GHz"
          break
        case "Okumura-Hata":
          tooltip = "Most widely used, frequency range 150 MHz - 1.5 GHz (extended up to 2 GHz)"
          break
      }
      selectedOption.title = tooltip
    }
  })
})
