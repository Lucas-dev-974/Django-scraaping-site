const labels = [
    'Janvier',
    'Fevrier',
    'Mars',
    'Avril',
    'Mai',
    'Juin',
  ];

const data = {
labels: labels,
datasets: [{
    type: 'bar',
    label: 'Threads Scrapped',
    backgroundColor: 'rgba(99, 198, 255, 0.2)',
    borderColor: 'rgba(99, 190, 255,1)',
    borderWidth: 2,
    hoverBackgroundColor: "rgba(99, 167, 255, 0.4)",
    hoverBorderColor: "rgba(78, 124, 199, 1)",
    data: [1, 10, 5, 2, 20, 15, 25],
},
{
  type: 'line',
  label: 'Threads (moy) Scrapped',
  backgroundColor: 'rgba(55, 146, 66, 1)',
  borderColor: 'rgba(55, 146, 66, 0.7)',
  data: [1, 5, 2, 1, 10, 8, 0],
}]
};

const config = {
data: data,
  options: {
    scales: {
      y: {
        ticks: { color: 'rgba(255, 255, 255,1)', beginAtZero: true },
        grid:{
            drawBorder: false,
            color: 'rgba(255, 255, 255,0.5)'
        }
      },
      x: {
        ticks: { color: 'rgba(255, 255, 255,1)', beginAtZero: true }
      }
    }
  }
};

const myChart = new Chart(document.getElementById('myChart'),config);