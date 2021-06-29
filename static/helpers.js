async function printChart(key, value) {
  let times = await value.map(time => time[0])
  let prices = await value.map(price => price[1])

  let chart = document.getElementById(key).getContext('2d')

  let gradient = chart.createLinearGradient(0, 0, 0, 400)

  let alpha_color = "#00C0FF" + "80"

  gradient.addColorStop(0, alpha_color)
  gradient.addColorStop(.425, 'rgba(255,193,119,0)')

  Chart.defaults.global.defaultFontFamily = 'Red Hat Text'
  Chart.defaults.global.defaultFontSize = 12

  createChart = new Chart(chart, {
    type: 'line',
    data: {
      labels: times,
      datasets: [{
        label: '$',
        data: prices,
        backgroundColor: gradient,
        borderColor: '#00C0FF',
        borderJoinStyle: 'round',
        borderCapStyle: 'round',
        borderWidth: 1,
        pointRadius: 0,
        pointHitRadius: 10,
        lineTension: .2,
      }]
    },

    options: {
      title: {
        display: false,
        text: 'Heckin Chart!',
        fontSize: 35
      },

      legend: {
        display: false
      },

      layout: {
        padding: {
          left: 0,
          right: 0,
          top: 0,
          bottom: 0
        }
      },

      scales: {
        xAxes: [{
          display: false,
          gridLines: {}
        }],
        yAxes: [{
          display: false,
          gridLines: {}
        }]
      },

      tooltips: {
        callbacks: {
          //This removes the tooltip title
          title: function() {}
       },
        //this removes legend color
        displayColors: false,
        yPadding: 10,
        xPadding: 10,
        position: 'nearest',
        caretSize: 10,
        backgroundColor: 'rgba(255,255,255,.9)',
        bodyFontSize: 15,
        bodyFontColor: '#303030' 
      }
    }
  })
}