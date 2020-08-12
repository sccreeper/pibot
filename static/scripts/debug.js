// document.onkeydown = function (e) {
//     e = e || window.event;
    
//     if(e.keyCode === 72) {
//         document.getElementById("debug").style.display = "block";
//     }
// };
window.setInterval(updateDebugValues, 1000);

function updateDebugValues() {
    console.log("lol")
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        var debugData = JSON.parse(this.responseText);

        document.getElementById('debug.clock.cpu').innerHTML = "<strong>CPU Clock:</strong> " + debugData.clock.cpu + "MHz";
        document.getElementById('debug.clock.gpu').innerHTML = "<strong>CPU Clock (h264):</strong> " + debugData.clock.gpu + "MHz";
        document.getElementById('debug.temp.soc').innerHTML = "<strong>SOC Temp:</strong> " + debugData.temp.soc;
        document.getElementById('debug.ip.host').innerHTML = "<strong>Host IP:</strong> " + debugData.ip.host;
        document.getElementById('debug.ip.client').innerHTML = "<strong>Client IP:</strong> " + debugData.ip.client;
        document.getElementById('debug.upsince').innerHTML = "<strong>Up since:</strong> " + debugData.upsince;
        document.getElementById('debug.log').innerHTML = debugData.log;

      }
    };
    xhttp.open("GET", "/debug", true);
    xhttp.send();

    

    
}
