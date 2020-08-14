//Init
var gpioNamesLeft = ['1', '3', '5', '7', '9', '11', '13', '15', '17', '19', '21', '23', '25', '27', '29', '31', '33', '35', '37', '39']
var gpioNamesRight = ['2', '4', '6', '8', '10', '12', '14', '16', '18', '20', '22', '24', '26', '28', '30', '32', '34', '36', '38', '40']
var configGpioIndex = [1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15, 16, 17, 18, 23, 24, 25, 27, 28, 30, 31, 32, 33, 35, 37, 38]
var allGPIO = [false, true, true, true, false, true, true, true, false, true, true, true, false, true, true, true, true, true, true, false, false, false, false, true, true, true, false, true, true, false, true, true, true, true, false, true, false, true, true, true]
//               1      3    5     7      9      11   13    15    17     19   21      23    25    27    29     31    33   35    37    39    2       4       6       8   10  12      14      16    18    20     22   24     26   28     30   32    34      36     38   40
window.setInterval(updateDebugValues, 1000);
var c = document.getElementById("debug.gpio").getContext('2d');

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
            labels: {
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
            labels: {
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
            drawPinouts(debugData.pinouts)
            console.log(debugData.pinouts.left)
            console.log(debugData.pinouts.right)

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

function removeData(chart) {
    chart.data.labels.pop();
    chart.data.datasets.forEach((dataset) => {
        dataset.data.pop();
    });
    chart.update();
}

function drawPinouts(data) {
    var x = 0;
    var y = 0;


    var i = 0;
    var j = 0;

    //This is bad code and i know
    for (var i = 0; i < 20; i++) {
        if (allGPIO[i]) {
            if (data.left[i+1]) {
                c.beginPath();
                c.rect(x, y, x + 24, y + 24);
                c.fillStyle = "darkgreen";
                c.fill();
                j += 1;
            } else {
                c.beginPath();
                c.rect(x, y, x + 24, y + 24);
                c.fillStyle = "crimson";
                c.fill();
            }

            c.beginPath();
            c.lineWidth = "3";
            c.strokeStyle = "black";
            c.rect(x, y, x + 24, y + 24);
            c.stroke();

            c.font = "12px Arial";
            c.fillStyle = "white";
            c.fillText(gpioNamesLeft[i], x + 6, y + 15);

            y += 24;
        } else if (!allGPIO[i]) {
            c.beginPath();
            c.rect(x, y, x + 24, y + 24);
            c.fillStyle = "black";
            c.fill();

            c.beginPath();
            c.lineWidth = "3";
            c.strokeStyle = "black";
            c.rect(x, y, x + 24, y + 24);
            c.stroke();

            c.font = "12px Arial";
            c.fillStyle = "white";
            c.fillText(gpioNamesLeft[i], x + 6, y + 15);

            y += 24;
        }
    }

    x = 24;
    y = 0;
    j = 0;

    for (var i = 20; i < 40; i++) {
        if (allGPIO[i]) {
            //If the pin is outputting
            if (data.right[i-19]) {
                c.beginPath();
                c.rect(x, y, x + 24, y + 24);
                c.fillStyle = "darkgreen";
                c.fill();
                j+=1;
            } else {
                c.beginPath();
                c.rect(x, y, x + 24, y + 24);
                c.fillStyle = "crimson";
                c.fill();
            }

            c.beginPath();
            c.lineWidth = "3";
            c.strokeStyle = "black";
            c.rect(x, y, x + 24, y + 24);
            c.stroke();

            c.font = "12px Arial";
            c.fillStyle = "white";
            c.fillText(gpioNamesRight[i-20], x + 6, y + 15);

            y += 24;
        } else if (!allGPIO[i]) {
            c.beginPath();
            c.rect(x, y, x + 24, y + 24);
            c.fillStyle = "black";
            c.fill();

            c.beginPath();
            c.lineWidth = "3";
            c.strokeStyle = "black";
            c.rect(x, y, x + 24, y + 24);
            c.stroke();

            c.font = "12px Arial";
            c.fillStyle = "white";
            c.fillText(gpioNamesRight[i-20], x + 6, y + 15);

            y += 24;
        }
    }
}

function isLeft(bool, index) {
    if (bool) {
        return index;
    } else {
        return index + 24;
    }
}
