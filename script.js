const barColors = ["#b91d47", "#00aba9", "#2b5797", "#e8c3b9", "#1e7145", "#737CA1", "#f8f8ff"];
let dataSets = {};

fetch('/get-data')
  .then(response => response.json())
  .then(data => {
    dataSets = data;

    // Populate the select options for both dropdowns
    const selectElement1 = document.getElementById('select-choice1');
    const selectElement2 = document.getElementById('select-choice2');
    Object.keys(dataSets).forEach(choice => {
      const option1 = document.createElement('option');
      option1.value = choice;
      option1.textContent = choice;
      selectElement1.appendChild(option1);

      const option2 = document.createElement('option');
      option2.value = choice;
      option2.textContent = choice;
      selectElement2.appendChild(option2);
    });

    // Initialize both charts with the first choice
    const initialChoice = Object.keys(dataSets)[0];
    updateChart('myChart1', initialChoice);
    updateChart('myChart2', initialChoice);
  });

let charts = {};

function updateChart(chartId, choice) {
  const newData = dataSets[choice];
  if (charts[chartId]) {
    charts[chartId].data.labels = newData.xValues;
    charts[chartId].data.datasets[0].data = newData.yValues;
    charts[chartId].update();
  } else {
    charts[chartId] = new Chart(chartId, {
      type: 'pie',
      data: {
        labels: newData.xValues,
        datasets: [{
          backgroundColor: barColors,
          data: newData.yValues
        }]
      },
      options: {
        title: {
          display: true,
          text: 'Analysis'
        }
      }
    });
  }
}

document.getElementById('select-choice1').addEventListener('change', function() {
  const selectedValue = this.value;
  updateChart('myChart1', selectedValue);
});

document.getElementById('select-choice2').addEventListener('change', function() {
  const selectedValue = this.value;
  updateChart('myChart2', selectedValue);
});
