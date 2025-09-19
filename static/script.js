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

      btnText.textContent = 'Running Simulation...';
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
          btnText.textContent = 'Run Simulation';
          btnLoader.style.display = 'none';
          submitButton.disabled = false;
      }
  });

  function displayResults(data) {
      // Update summary information
      document.getElementById('usedModel').textContent = data.model;
      document.getElementById('usedEnvironment').textContent = data.environment;
      document.getElementById('totalCalculations').textContent = data.summary.total_calculations;
      
      // Update summary statistics
      document.getElementById('minPathloss').textContent = data.summary.min_pathloss + ' dB';
      document.getElementById('maxPathloss').textContent = data.summary.max_pathloss + ' dB';
      document.getElementById('avgPathloss').textContent = data.summary.avg_pathloss + ' dB';
      document.getElementById('pathlossRange').textContent = data.summary.pathloss_range + ' dB';
      
      // Populate results table
      const tableBody = document.getElementById('resultsTableBody');
      tableBody.innerHTML = '';
      
      data.results.forEach(result => {
          const row = document.createElement('tr');
          row.innerHTML = `
              <td>${result.frequency}</td>
              <td>${result.distance}</td>
              <td>${result.tx_height}</td>
              <td>${result.rx_height}</td>
              <td class="pathloss-cell">${result.pathloss}</td>
              <td>${result.fspl}</td>
              <td>${result.additional_loss}</td>
          `;
          tableBody.appendChild(row);
      });

      resultsContainer.style.display = 'block';
      resultsContainer.scrollIntoView({ behavior: 'smooth' });
  }

  function showError(message) {
      errorContainer.textContent = message;
      errorContainer.style.display = 'block';
      errorContainer.scrollIntoView({ behavior: 'smooth' });
  }
});