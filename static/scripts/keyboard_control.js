document.addEventListener('keydown', function(event) {
	if (document.getElementById('keyboard_enable').checked == true) {
		switch(event.keyCode) {
			case 32:
				//Space key
				postRequest("/control/motor/", "DIRECTION=stop");
				break;
			case 68:
				//d
				postRequest("/control/motor/", "DIRECTION=right")
				break;
			case 65:
				//a
				postRequest("/control/motor/", "DIRECTION=left");
				break;
			case 87:
				//w
				postRequest("/control/motor/", "DIRECTION=forward");
				break;
			case 83:
				//s
				postRequest("/control/motor/", "DIRECTION=backward");
				break;
			default:
				break;	
				
		}
	}else {
		//Debug menu
		if(event.keyCode === 72) {
			document.getElementById("debug").style.display = "block";
		}
	}
});

document.addEventListener('keyup', function(event) {

	//Debug menu
	if(event.keyCode == 72) {
		document.getElementById("debug").style.display = "none";
	} else if(event.keyCode === 68 || event.keyCode === 65 || event.keyCode === 87 || event.keyCode === 83) {
		postRequest("/control/motor/", "DIRECTION=stop");
	}
});

//lol

