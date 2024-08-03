import bpy
import os
import yaml
import math


def cube(width, depth, height):
    vertices = [
        (0, 0, 0),             # 0
        (0, 0, height),        # 1
        (0, depth, 0),         # 2
        (0, depth, height),    # 3
        (width, 0, 0),         # 4
        (width, 0, height),    # 5
        (width, depth, 0),     # 6
        (width, depth, height)  # 7
    ]

    faces = [
        (0, 1, 3, 2),  # left
        (0, 1, 5, 4),  # front
        (4, 5, 7, 6),  # right
        (2, 3, 7, 6),  # back
        (0, 2, 6, 4),  # bottom
        (1, 3, 7, 5),  # top
    ]

    mesh = bpy.data.meshes.new(name="Cube")
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    cube = bpy.data.objects.new("Cube", mesh)
    return cube


def flatten(nested_list):
    flat_list = []
    for item in nested_list:
        if isinstance(item, list):
            flat_list.extend(flatten(item))
        else:
            flat_list.append(item)
    return flat_list


def get_value(var):
    if isinstance(var, list):
        return sum(flatten(var))
    elif isinstance(var, dict):
        if var["fn"] == "sum":
            return sum(flatten(var["args"]))
        if var["fn"] == "neg_sum":
            return -sum(flatten(var["args"]))
    else:
        return var


def door_01(name):
    obj = cube(
        width=.9,
        depth=.05,
        height=2
    )
    obj.name = name
    return obj


def group(name):
    obj = bpy.data.objects.new("empty", None)
    obj.name = name
    return obj


def interior_wall(length, name='wall', thickness=0.1, height=2.5, angle=0, holes=[]):
    obj = cube(width=get_value(length), depth=thickness, height=height)
    obj.name = name

    for hole_dimensions in holes:
        hole = cube(
            width=hole_dimensions['width'],
            depth=3*thickness,
            height=hole_dimensions['height']
        )

        x_loc = get_value(hole_dimensions.get('x', 0))

        hole.location = (x_loc, -thickness, -0.1)
        hole.parent = obj
        hole.hide_viewport = True
        boolean_modifier = obj.modifiers.new(name="boolean", type="BOOLEAN")
        boolean_modifier.object = hole
        boolean_modifier.operation = "DIFFERENCE"
        boolean_modifier.solver = "FAST"

    obj.rotation_euler = (0, 0, angle/180 * math.pi)
    return obj


def component_assembly(components, parent=None):
    for component in components:
        args = {k: v for k, v in component.items() if k !=
                "type" and k != "components" and k != 'location'}

        component_type = component['type'] if 'type' in component else 'group'

        fn = globals()[component_type]
        obj = fn(**args)

        if (parent):
            obj.parent = parent

        scene = bpy.context.scene
        scene.collection.objects.link(obj)

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
