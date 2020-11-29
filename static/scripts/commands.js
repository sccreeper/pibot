var command_box = document.getElementById('command');

function submit_command() {
    postRequest('/command', "command=" + command_box.value);
}
