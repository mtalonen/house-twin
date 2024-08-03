import bpy

from utils import get_value


def cuboid(width, depth, height):
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
    obj = bpy.data.objects.new("Cube", mesh)
    return obj


def group(name):
    obj = bpy.data.objects.new("empty", None)
    obj.name = name
    return obj


def cuboid_with_holes(length, name, thickness, height, holes=[]):
    obj = cuboid(width=get_value(length), depth=thickness, height=height)
    obj.name = name

    for hole_dimensions in holes:
        hole = cuboid(
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

    return obj


def door_01(name):
    obj = cuboid(
        width=.9,
        depth=.05,
        height=2
    )
    obj.name = name
    return obj


def basement_wall(length, name='b_wall', thickness=0.3, height=2.7, holes=[]):
    obj = cuboid_with_holes(length, name, thickness, height, holes)
    return obj


def basement_wall(length, name='b_wall', thickness=0.3, height=2.7, holes=[]):
    obj = cuboid_with_holes(length, name, thickness, height, holes)
    return obj


def floor_casting(length, width, height, name='floor_casting'):
    obj = cuboid_with_holes(length=length, thickness=width,
                            height=height, name=name, holes=[])
    return obj


def hvac_duct(length):
    obj = cuboid(width=length, depth=0.1, height=0.1)
    return obj


def interior_wall(length, name='wall', thickness=0.1, height=2.5, holes=[]):
    obj = cuboid_with_holes(length, name, thickness, height, holes)
    return obj
