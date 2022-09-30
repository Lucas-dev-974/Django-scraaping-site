async function getGraphData(url=null, method='POST', params=null, csrfToken=false){
    const data = new FormData()

    if(params != null){
        try{
            paramsToJson = JSON.stringify(params)
            console.log(paramsToJson)

            Object.entries(params).forEach(param => {
                data.append(param[0], param[1])
            });

        }catch(error){
            console.log(error);
            alert('Désoler une erreur est survenue veuillez recharger la page !')
        }
    }   

    if(csrfToken) data.append('csrfmiddlewaretoken', csrfToken)

    const request = await window.fetch(url, {
        method: method ?? method,
        body: data,
    })

    const JsonResponse = await request.json()
    return JsonResponse
}

document.addEventListener('DOMContentLoaded', async () => {
    const response = await getGraphData('http://127.0.0.1:8000/private/graph/api', method='POST', params={
        'year': '2022',
        'page': '0'
    }, '{{ csrf_token }}')
    
    console.log(response);
    const myChart = new Chart(document.getElementById('myChart'),config);
})

const data = {
  labels: labels,
  datasets: [
    {
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
    }
  ]
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

