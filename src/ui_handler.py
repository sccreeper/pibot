# - Converts UI JSON into HTML
# - Hardcoded unfortunately

import json
from util import read_file
#So text in button and other elements can be HTML safe
from html import escape

def gen_ui(json_path):
    ui_dict = json.loads(read_file(json_path))
    ui_string = ""


    for element in ui_dict:
        if element["type"] == "button":
            if element["data"]["bind"] == None:
                ui_string += "\n"
                ui_string += "<button id=\"{}\" bind=\"\" onClick=\"postRequest('/command', 'command=' + this.getAttribute(\"command\"))\" command=\"{}\">{}</button>".format(element["id"], element["data"]["command"], escape(element["data"]["text"]))
            else:
                ui_string += "\n"
                ui_string += "<button id=\"{}\" bind=\"{}\" onClick=\"postRequest('/command', 'command=+ this.getAttribute(\"command\"))\" command=\"{}\">{}</button>".format(element["id"], element["data"]["bind"],element["data"]["command"], escape(element["data"]["text"]))
        elif element["type"] == "html":
            ui_string += "\n"
            ui_string += element["data"]["html"]
        elif element["type"] == "slider":
            ui_string += "\n"
            ui_string += "<input id=\"{}\" type=\"range\" min=\"{}\" max=\"{}\" onMouseUp=\"execute_command('{}')\"/>".format(element["id"], element["data"]["min"], element["data"]["max"], element["data"]["command"])

    return ui_string
