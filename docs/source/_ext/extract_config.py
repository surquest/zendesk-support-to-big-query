from docutils import nodes
from docutils.parsers.rst import directives, roles
from docutils.parsers.rst.directives.tables import Table
from docutils.parsers.rst import Directive
import yaml
import json
import os
import re

def config_item():

    def load_json(path):

        with open(path) as file:

            out = json.load(file)

        return out

    def is_list_of(obj, subject):

        return bool(obj) and all(isinstance(elem, subject) for elem in obj)

    def role(name, rawtext, text, lineno, inliner, options={}, content=[]):

        options = dict()
        options["glue"] = "-"
        options["sufix"] = ""
        options["prefix"] = ""
        app = inliner.document.settings.env.app

        if "[" in text:

            params = re.search('\[(.*)\]', text).group(1)

            for param in params.split(","):
                key = param.split(":")[0]
                value = param.split(":")[1].strip("'")
                options[key] = value

            items = re.search('(.*)\[', text).group(1).split("+")

        else:

            items = text.split("+")

        config = load_json(app.config.config_file)

        config_values = list()

        for item in items:

            keys = item.split(">")

            for idx, val in enumerate(keys):

                if idx == 0:

                    config_value = config

                if isinstance(config_value, dict):

                    config_value = config_value.get(val)

                elif isinstance(config_value, list):

                    config_value = config_value[int(val)]

                if idx+1 == len(keys):

                    config_values.append(str(config_value))


        if is_list_of(config_values, str):

            out = options["prefix"]+options["glue"].join(config_values)+options["sufix"]
            node = nodes.literal(out, out)

        elif is_list_of(config_values, (int, float)):

            out = options["prefix"]+options["glue"].join(config_values)+options["sufix"]
            node = nodes.literal(out, out)

        elif isinstance(config_values, (int, float)):

            out = options["prefix"] + str(config_values) + options["sufix"]
            node = nodes.literal(out, out)

        else:

            listnode = nodes.bullet_list()

            for el in config_values[0]:

                listnode += nodes.list_item('', nodes.literal(
                            json.dumps(el),
                            json.dumps(el)
                        ))

            node = listnode

        return [node], []

    return role

def setup(app):

    app.add_config_value('config_file', '', 'html')
    app.add_role('config_item', config_item())

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
        }
