document.addEventListener('keydown', function(event) {
	if (document.getElementById('keyboard_enable').checked == true) {
		if(event.keyCode == 32) {
			//Space key
			post_request("/control/motor/", "DIRECTION=stop")
		}
		else if(event.keyCode == 68) {
			//d
			post_request("/control/motor/", "DIRECTION=right")
		}
		else if (event.keyCode == 65) {
			//a
			post_request("/control/motor/", "DIRECTION=left")
		}
		else if (event.keyCode == 87) {
			//w
			post_request("/control/motor/", "DIRECTION=forward")
		}
		else if (event.keyCode == 83) {
			//s
			post_request("/control/motor/", "DIRECTION=backward")
		}
	}else {
		return ''
	}
});

