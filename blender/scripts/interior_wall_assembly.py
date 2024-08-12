import bpy
import os
import yaml
import math

import component_lib
from utils import get_value
from map_network import map_network

import json


def component_assembly(components, parent=None):
    for component in components:
        component_type = component['type'] if 'type' in component else 'group'

        if component_type == 'hvac':
            a = map_network(component['network'])

            # print(json.dumps(a, indent=2, sort_keys=True))

            node = {
                "name": 'hvac',
                "location": component['location'],
                "components": a
            }

            component_assembly([node])
            continue

        args = {k: v for k, v in component.items() if k !=
                "type" and k != "components" and k != 'location' and k != 'rotation'}

        fn = getattr(component_lib, component_type)
        obj = fn(**args)

        if (parent):
            obj.parent = parent

        scene = bpy.context.scene
        scene.collection.objects.link(obj)

        if ('rotation' in component):
            x = math.radians(get_value(component['rotation'].get('x', 0)))
            y = math.radians(get_value(component['rotation'].get('y', 0)))
            z = math.radians(get_value(component['rotation'].get('angle', 0)))
            obj.rotation_euler = (x, y, z)

        if ('location' in component):
            obj.location = (get_value(component['location'].get(
                'x', 0)), get_value(component['location'].get('y', 0)), get_value(component['location'].get('z', 0)))

        if 'components' in component:
            component_assembly(component['components'], obj)


def interior_wall_assembly(config_path):

    wall_config_file = os.path.join(os.path.dirname(
        os.path.dirname(__file__)),  config_path)

    with open(wall_config_file, 'r') as file:
        wall_config = yaml.safe_load(file)

    walls = wall_config['walls']
    component_assembly(walls)
