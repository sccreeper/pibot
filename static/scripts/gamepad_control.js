var gamepads = {};

function gamepadHandler(event, connecting) {
  var gamepad = event.gamepad;
  // Note:
  // gamepad === navigator.getGamepads()[gamepad.index]

  if (connecting) {
    gamepads[gamepad.index] = gamepad;
    window.setInterval(function(){
		gamepadState(gamepad.index)
	}, 100);
  } else {
    delete gamepads[gamepad.index];
    window.clearInterval(); 
  }
}

window.addEventListener("gamepadconnected", function(e) { gamepadHandler(e, true); }, false);
window.addEventListener("gamepaddisconnected", function(e) { gamepadHandler(e, false); }, false);

function gamepadState(gamepadIndex) {
	console.log(gamepadIndex)
	
	var gp = window.navigator.getGamepads()[gamepadIndex]
	
	if (gp.axes[0] < -0.5) {
		post_request('/control/motor/', 'DIRECTION=left');
	} else if (gp.axes[0] > 0.5) {
		post_request('/control/motor/', 'DIRECTION=right');
	} else if (gp.buttons[7].pressed) {
		console.log(gp.buttons[7].value * 100)
		
		document.getElementById('motorSpeed').value = Math.round(gp.buttons[7].value * 100);
		post_request('/control/motor/', 'DIRECTION=forward')
		post_request('/control/motor/', 'SPEED=' + Math.round(gp.buttons[7].value * 100));
	} else if(gp.buttons[6].pressed) {
		post_request('/control/motor/', 'DIRECTION=stop');
		document.getElementById('motorSpeed').value = 1;
	} else if((gp.axes[0] < 0.5) && (gp.axes[0] > -0.5))	{
		post_request('/control/motor/', 'DIRECTION=stop');
	}
}
