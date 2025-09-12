document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('pathlossForm');
  const resultsContainer = document.getElementById('results-container');
  const errorContainer = document.getElementById('error-container');
  const submitButton = form.querySelector('.cta-button');
  const btnText = submitButton.querySelector('.btn-text');
  const btnLoader = submitButton.querySelector('.btn-loader');
  const modelSelect = document.getElementById('model');
  const modelCards = document.querySelectorAll('.model-card');

  // Add click handlers to model cards
  modelCards.forEach(card => {
    card.addEventListener('click', () => {
      const model = card.dataset.model;
      modelSelect.value = model;
      
      // Update visual state
      modelCards.forEach(c => c.classList.remove('selected'));
      card.classList.add('selected');
      
      // Add visual feedback
      card.style.transform = 'scale(0.98)';
      setTimeout(() => {
        card.style.transform = '';
      }, 150);
    });
  });

  // Update model card selection when dropdown changes
  modelSelect.addEventListener('change', () => {
    modelCards.forEach(card => {
      card.classList.remove('selected');
      if (card.dataset.model === modelSelect.value) {
        card.classList.add('selected');
      }
    });
  });

  form.addEventListener('submit', async (e) => {
      e.preventDefault();

      resultsContainer.style.display = 'none';
      errorContainer.style.display = 'none';

      btnText.textContent = 'Calculating...';
      btnLoader.style.display = 'inline-block';
      submitButton.disabled = true;

      try {
          const formData = new FormData(form);
          const response = await fetch('/predict', {
              method: 'POST',
              body: new URLSearchParams(formData)
          });

          const data = await response.json();

          if (data.error) {
              showError(data.error);
          } else {
              displayResults(data);
          }
      } catch (error) {
          showError('An unexpected error occurred. Please try again.');
      } finally {
          btnText.textContent = 'Calculate Pathloss';
          btnLoader.style.display = 'none';
          submitButton.disabled = false;
      }
  });

  function displayResults(data) {
      document.getElementById('pathlossValue').textContent = data.pathloss.toFixed(2);
      document.getElementById('fsplValue').textContent = data.fspl.toFixed(2) + ' dB';
      document.getElementById('additionalLossValue').textContent = data.additional_loss.toFixed(2) + ' dB';
      document.getElementById('usedModel').textContent = data.model;
      document.getElementById('usedEnvironment').textContent = data.parameters.environment;
      document.getElementById('usedFrequency').textContent = data.parameters.frequency;
      document.getElementById('usedDistance').textContent = data.parameters.distance;
      document.getElementById('usedTxHeight').textContent = data.parameters.tx_height;
      document.getElementById('usedRxHeight').textContent = data.parameters.rx_height;

      resultsContainer.style.display = 'block';
      resultsContainer.scrollIntoView({ behavior: 'smooth' });
  }

  function showError(message) {
      errorContainer.textContent = message;
      errorContainer.style.display = 'block';
      errorContainer.scrollIntoView({ behavior: 'smooth' });
  }
});