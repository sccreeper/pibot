var command_box = document.getElementById('command');

function submit_command() {
    postRequest('/command', "command=" + command_box.value);
}

//Function to do some of the parsing before the command is passed to the server.
//Passes in values of elements like sliders.
function execute_command(cmd) {
    var parsing_id = false;
    var current_id = "";
    

    for (var i = 0; i < cmd.length; i++) {
        var element = cmd[i];
        console.log(parsing_id)
        console.log(current_id)

        if(element === "]") {
            parsing_id = false;
            //Replace string in command with current value
            cmd = cmd.replace("[" + current_id + "]", document.getElementById(current_id).value);
            current_id = "";
        }
        
        if(parsing_id) {
            current_id += element;
        }

        if (element === "[") {
            parsing_id = true;
        }
        
    }

    postRequest('/command', "command=" + cmd);

    
}