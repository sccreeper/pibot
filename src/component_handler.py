from util import read_file
import json
import importlib

class components:
    def __init__(self):
        self.built_component_types = []
        self.components = {}
        self.component_names = []

        cpnt_manifest = json.loads(read_file("components/component_manifests.json"))
        cpnt_config = json.loads(read_file("component_config.json"))

        #Load 'built' components
        for cpnt in cpnt_manifest:

            self.built_component_types.append(cpnt_manifest[cpnt]['type_name'])

        #Load the components from the component config
        for cpnt in cpnt_config:
            if cpnt["type"] in self.built_component_types:
                #do wierd import crap

                module_name = "components." + cpnt_manifest[cpnt["type"]]["file_name"].split(".")[0]

                cpnt_module = importlib.import_module(module_name)
                cpnt_class = getattr(cpnt_module, cpnt_manifest[cpnt["type"]]["class_name"])

                self.components[cpnt["name"]] = cpnt_class(cpnt["data"])
                self.component_names.append(cpnt["name"])

            else:
                raise ComponentNotFound('{} is not a component!'.format(cpnt["type"]))

class ComponentNotFound(Exception):
    pass
