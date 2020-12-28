function timeStampConverter(unixTimeStamp) {
    let dateTime = new Date(unixTimeStamp * 1000)
    weekDay = ['Mon', 'Sun', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']

    return {
        'weekday': weekDay[dateTime.getDay()],
        'day': dateTime.getDate(),
        'month': month[dateTime.getMonth()],
        'hour': dateTime.getHours(),
        'minute': dateTime.getMinutes(),
        'year': dateTime.getFullYear()
    }
}

function oneDayAgoData(rates) {
    let timeLabels = []
    let values = []

    for (let i = 0; i < rates.length; i++){
        let dateTime = timeStampConverter(rates[i][0])
        let hour = dateTime['hour']
        let minute = "0" + dateTime['minute']

        let formattedDateTime = hour + ":" + minute.substr(-2)

        timeLabels.push(formattedDateTime)
        values.push(rates[i][3])
    }

    return {
        'time': timeLabels,
        'values': values
    }
}

function fiveDaysAgoData(rates) {
    let timeLabels = []
    let values = []

    for (let i = 0; i < rates.length; i++){
        let dateTime = timeStampConverter(rates[i][0])
        let weekDay = dateTime['weekday']
        let day = dateTime['day']
        let month = dateTime['month']
        let hour = dateTime['hour']
        let minute = '0' + dateTime['minute']

        let formattedDateTime = `${weekDay}, ${day} ${month} ${hour}:${minute.substr(-2)}`

        timeLabels.push(formattedDateTime)
        values.push(rates[i][3])
    }

    return {
        'time': timeLabels,
        'values': values
    }
}

function oneMonthAgoData(rates) {
    let timeLabels = []
    let values = []

    for (let i = 0; i < rates.length; i++){
        let dateTime = timeStampConverter(rates[i][0])
        let weekDay = dateTime['weekday']
        let day = dateTime['day']
        let month = dateTime['month']

        let formattedDateTime = `${weekDay}, ${day} ${month}`

        timeLabels.push(formattedDateTime)
        values.push(rates[i][3])
    }

    return {
        'time': timeLabels,
        'values': values
    }
}

function oneYearAgoData(rates) {
    let timeLabels = []
    let values = []

    for (let i = 0; i < rates.length; i++){
        let dateTime = timeStampConverter(rates[i][0])
        let day = dateTime['day']
        let month = dateTime['month']
        let year = dateTime['year']

        let formattedDateTime = `${day} ${month} ${year}`

        timeLabels.push(formattedDateTime)
        values.push(rates[i][3])
    }

    return {
        'time': timeLabels,
        'values': values
    }
}

function fiveYearsAgoData(rates) {
    let timeLabels = []
    let values = []

    for (let i = 0; i < rates.length; i++){
        let dateTime = timeStampConverter(rates[i][0])
        let day = dateTime['day']
        let month = dateTime['month']
        let year = dateTime['year']

        let formattedDateTime = `${day} ${month} ${year}`

        timeLabels.push(formattedDateTime)
        values.push(rates[i][3])
    }

    return {
        'time': timeLabels,
        'values': values
    }
}

function max(rates) {
    let timeLabels = []
    let values = []

    for (let i = 0; i < rates.length; i++){
        let dateTime = timeStampConverter(rates[i][0])
        let day = dateTime['day']
        let month = dateTime['month']
        let year = dateTime['year']

        let formattedDateTime = `${day} ${month} ${year}`

        timeLabels.push(formattedDateTime)
        values.push(rates[i][3])
    }

    return {
        'time': timeLabels,
        'values': values
    }
}

function changeChart(data) {
    document.getElementById('chart').remove()
    
    document.getElementById('canvas-container').innerHTML = '<canvas id="chart"></canvas>'

    let btcChart = document.getElementById('chart').getContext('2d')
    
    let createChart = new Chart(btcChart, {
        type: 'line',
        data: {
            labels: data['time'],
            datasets: [{
                label: '$',
                data: data['values'],
                backgroundColor: 'rgba(247, 147, 26, 0.3)',
                borderColor: 'rgb(247, 147, 26)',
                borderWidth: 1.5,
                lineTension: 0,
                pointRadius: 0,
                pointHitRadius: 10
            }]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,
            title: {
                display: false,
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
                    display: true,
                    ticks: {
                        display: false
                    },
                    gridLines: {
                        display: false
                    }
                }],
                yAxes: [{
                    display: true,
                    ticks: {
                        maxTicksLimit: 3.1
                    }
                }]
            },

            tooltips: {
                mode: 'index',
                intersect: false,
                displayColors: false,
                yPadding: 10,
                xPadding: 10,
                position: 'nearest',
                carretSize: 10,
                backgroundColor: 'rgba(48, 48, 48, 0.8)',
                bodyFontSize: 15,
                bodyFontColor: '#ffffff',
                titleColor: '#ffffff'
            }
        }
    })
}