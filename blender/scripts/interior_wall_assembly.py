import bpy
import os
import yaml
import math

import component_lib
from utils import get_value


def component_assembly(components, parent=None):
    for component in components:
        args = {k: v for k, v in component.items() if k !=
                "type" and k != "components" and k != 'location' and k != 'rotation'}

        component_type = component['type'] if 'type' in component else 'group'

        fn = getattr(component_lib, component_type)
        obj = fn(**args)

        if (parent):
            obj.parent = parent

        scene = bpy.context.scene
        scene.collection.objects.link(obj)

        if ('rotation' in component):
            obj.rotation_euler = (0, 0, get_value(
                component['rotation'].get('angle', 0))/180 * math.pi)

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
