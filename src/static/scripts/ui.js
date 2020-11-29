// Get a list of elements
var ui_div_btns = document.getElementById('ui').querySelectorAll("button");

//Add event listeners

//Buttons

for (var i = 0; i < ui_div_btns.length; i++) {

    ui_div_btns[i].addEventListener("click", postRequest('/command', "command=" + ui_div_btns[i].getAttribute("command")) )

}
