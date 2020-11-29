# - Converts UI JSON into HTML
# - Hardcoded unfortunately

import json
from util import read_file

def gen_ui(json_path):
    ui_dict = json.loads(read_file(json_path))
    ui_string = ""


    for element in ui_dict:
        if element["type"] == "button":
            ui_string += "\n"
            ui_string += "<button onClick=\"postRequest('/command', 'command={}')\">{}</button>".format(element["data"]["command"], element["data"]["text"])

    return ui_string
