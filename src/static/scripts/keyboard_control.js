//Generate UI Keybinds

var uiButtons = document.getElementById('ui').getElementsByTagName('button');
var binds = [];

//Generate list of binds at runtime so don't have to do it each time key is pressed.
for (var i = 0; i < uiButtons.length; i++) {
	var element = uiButtons[i];
	
	if(element.getAttribute('bind') === '') continue;
	else {
		binds.push([element.getAttribute('bind'), element.getAttribute('command')]);
	}
}

console.log(binds)

document.addEventListener('keydown', function(e) { 
	
	for(var i = 0; i < binds.length; i++) {
		if(e.key === binds[i][0]) {
			postRequest('/command', "command=" + binds[i][0]);
		}
	}
});

