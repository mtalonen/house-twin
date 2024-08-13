import bpy
import bmesh
import math
import mathutils

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


def pipe(length, diameter):
    mesh = bpy.data.meshes.new(name="CylinderMesh")
    obj = bpy.data.objects.new(name="Pipe", object_data=mesh)

    bm = bmesh.new()
    bmesh.ops.create_circle(
        bm,
        cap_ends=False,
        radius=diameter/2,
        segments=16
    )

    rotation_matrix = mathutils.Matrix.Rotation(math.radians(90), 4, 'Y')

    for vert in bm.verts:
        vert.co = rotation_matrix @ vert.co

    extrude_result = bmesh.ops.extrude_edge_only(bm, edges=bm.edges)

    bmesh.ops.translate(
        bm,
        vec=(length, 0, 0),
        verts=[v for v in extrude_result['geom']
               if isinstance(v, bmesh.types.BMVert)]
    )

    bm.to_mesh(mesh)
    bm.free()
    return obj


def hvac_duct(length, diameter):
    obj = pipe(length, diameter=diameter)
    return obj


def hvac_duct_90(diameter):

    length = 0.3
    radius = diameter/2

    obj1 = pipe(length + radius, diameter=diameter)
    obj2 = pipe(length + radius, diameter=diameter)

    mesh1 = obj1.data
    mesh2 = obj2.data

    bm1 = bmesh.new()
    bm1.from_mesh(mesh1)

    bmesh.ops.rotate(bm1, verts=bm1.verts, cent=(0, 0, 0),
                     matrix=mathutils.Matrix.Rotation(math.radians(90), 4, 'Z'))
    bmesh.ops.translate(bm1, verts=bm1.verts, vec=(length, -radius, 0))

    bm1.from_mesh(mesh2)
    bm1.to_mesh(mesh1)
    mesh1.update()
    bm1.free()

    return obj1


def hvac_duct_45(diameter):
    length = 0.3
    radius = diameter/2

    obj1 = pipe(length + 0 * radius, diameter=diameter)
    obj2 = pipe(length + 0 * radius, diameter=diameter)

    mesh1 = obj1.data
    mesh2 = obj2.data

    bm1 = bmesh.new()
    bm1.from_mesh(mesh1)

    bmesh.ops.rotate(bm1, verts=bm1.verts, cent=(0, 0, 0),
                     matrix=mathutils.Matrix.Rotation(math.radians(45), 4, 'Z'))
    bmesh.ops.translate(bm1, verts=bm1.verts, vec=(length, 0, 0))

    bm1.from_mesh(mesh2)
    bm1.to_mesh(mesh1)
    mesh1.update()
    bm1.free()

    return obj1


def hvac_duct_t(diameter):
    length = 0.3
    radius = diameter/2

    obj1 = pipe(2 * length, diameter=diameter)
    obj2 = pipe(length, diameter=diameter)

    mesh1 = obj1.data
    mesh2 = obj2.data

    bm1 = bmesh.new()
    bm1.from_mesh(mesh1)

    bmesh.ops.rotate(bm1, verts=bm1.verts, cent=(0, 0, 0),
                     matrix=mathutils.Matrix.Rotation(math.radians(90), 4, 'Z'))
    bmesh.ops.translate(bm1, verts=bm1.verts, vec=(length, -length, 0))

    bm1.from_mesh(mesh2)
    bm1.to_mesh(mesh1)
    mesh1.update()
    bm1.free()

    return obj1


def hvac_duct_t2(diameter):
    length = 0.3
    radius = diameter/2

    obj1 = pipe(1 * length, diameter=diameter)
    obj2 = pipe(2 * length, diameter=diameter)

    mesh1 = obj1.data
    mesh2 = obj2.data

    bm1 = bmesh.new()
    bm1.from_mesh(mesh1)

    bmesh.ops.rotate(bm1, verts=bm1.verts, cent=(0, 0, 0),
                     matrix=mathutils.Matrix.Rotation(math.radians(90), 4, 'Z'))
    bmesh.ops.translate(bm1, verts=bm1.verts, vec=(length, 0, 0))

    bm1.from_mesh(mesh2)
    bm1.to_mesh(mesh1)
    mesh1.update()
    bm1.free()

    return obj1


def interior_wall(length, name='wall', thickness=0.1, height=2.5, holes=[]):
    obj = cuboid_with_holes(length, name, thickness, height, holes)
    return obj
