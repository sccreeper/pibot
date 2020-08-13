//Init
window.setInterval(updateDebugValues, 1000);

//Chart init
var ctx = document.getElementById('debug.chart.clock').getContext('2d');
var chart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'line',

    // The data for our dataset
    data: {
        labels: [],
        datasets: [{
            label: 'CPU Clock',
            backgroundColor: 'rgba(255, 99, 132, 0.5)',
            borderColor: 'rgb(255, 99, 132)',
            borderWidth: 1,
            data: []
        }]
    },

    // Configuration options go here
    options: {
      scales: {
      yAxes: [{
          gridLines: {
              zeroLineColor: '#ffffff'
          },
          ticks: {
            fontColor: '#ffffff'
          },
          scaleLabel: {
            display: true,
            labelString: 'Clockspeed (MHz)',
            fontColor: '#ffffff'
          }
      }],
      xAxes: [{
          gridLines: {
              zeroLineColor: '#ffffff'
          },
          ticks: {
            fontColor: '#ffffff'
          },
          scaleLabel: {
            display: true,
            labelString: 'Time',
            fontColor: '#ffffff'
          }
      }]
    },
    legend: {
      labels : {
      fontColor: '#ffffff'
    }
    }
  }
});

chart.canvas.parentNode.style.height = '256px';
chart.canvas.parentNode.style.width = '512px';

var ctx1 = document.getElementById('debug.chart.temp').getContext('2d');
var chartTemp = new Chart(ctx1, {
    // The type of chart we want to create
    type: 'line',

    // The data for our dataset
    data: {
        labels: [],
        datasets: [{
            label: 'SOC Temp',
            backgroundColor: 'rgba(30, 93, 175, 0.5)',
            borderColor: 'rgb(30, 93, 175)',
            borderWidth: 1,
            data: []
        }]
    },

    // Configuration options go here
    options: {
      scales: {
      yAxes: [{
          gridLines: {
              zeroLineColor: '#ffffff'
          },
          ticks: {
            fontColor: '#ffffff'
          },
          scaleLabel: {
            display: true,
            labelString: 'Temperature (°C)',
            fontColor: '#ffffff'
          }
      }],
      xAxes: [{
          gridLines: {
              zeroLineColor: '#ffffff'
          },
          ticks: {
            fontColor: '#ffffff'
          },
          scaleLabel: {
            display: true,
            labelString: 'Time',
            fontColor: '#ffffff'
          }
      }]
    },
    legend: {
      labels : {
      fontColor: '#ffffff'
    }
    }
  }
});

chartTemp.canvas.parentNode.style.height = '256px';
chartTemp.canvas.parentNode.style.width = '512px';

function updateDebugValues() {
    console.log("lol")
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        var debugData = JSON.parse(this.responseText);

        document.getElementById('debug.clock.cpu').innerHTML = "<strong>CPU Clock:</strong> " + debugData.clock.cpu + "MHz";
        document.getElementById('debug.clock.gpu').innerHTML = "<strong>GPU Clock (h264):</strong> " + debugData.clock.gpu + "MHz";
        document.getElementById('debug.temp.soc').innerHTML = "<strong>SOC Temp:</strong> " + debugData.temp.soc;
        document.getElementById('debug.ip.host').innerHTML = "<strong>Host IP:</strong> " + debugData.ip.host;
        document.getElementById('debug.ip.client').innerHTML = "<strong>Client IP:</strong> " + debugData.ip.client;
        document.getElementById('debug.upsince').innerHTML = "<strong>Up since:</strong> " + debugData.upsince;
        document.getElementById('debug.log.log').innerHTML = debugData.log.log;
        document.getElementById('debug.log.size.lines').innerHTML = "<strong>Log file size (lines):</strong> " + debugData.log.size.lines;
        document.getElementById('debug.log.size.kb').innerHTML = "<strong>Log file size:</strong> " + debugData.log.size.kb + "kb";

        addData(chart, debugData.timestamp, debugData.chart.clock.cpu);
        addData(chartTemp, debugData.timestamp, debugData.chart.temp.soc);

      }
    };
    xhttp.open("GET", "/debug", true);
    xhttp.send();

}

//Chart functions
function addData(chart1, label, data) {
    chart1.data.labels.push(label);
    chart1.data.datasets.forEach((dataset) => {
        dataset.data.push(data);
    });
    chart1.update();
}
