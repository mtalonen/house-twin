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
        (width, depth, height) # 7
    ]

    faces = [
        (0, 1, 3, 2), # left
        (0, 1, 5, 4), # front
        (4, 5, 7, 6), # right
        (2, 3, 7, 6), # back
        (0, 2, 6, 4), # bottom
        (1, 3, 7, 5), # top
    ]

    mesh = bpy.data.meshes.new(name="Cube")
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    
    cube = bpy.data.objects.new("Cube", mesh)
    scene = bpy.context.scene
    scene.collection.objects.link(cube)

    return cube


def get_value(var):
    return sum(var) if isinstance(var, list) else var
    

def interior_wall(length, name='wall', thickness=0.1, height=2.5, x=0, y=0, angle=0, holes=[]):
    obj = cube(width=length, depth=thickness, height=height)
    obj.name = name

    for hole_dimensions in holes:
        hole = cube(
            width=hole_dimensions['width'],
            depth=3*thickness, 
            height=hole_dimensions['height']
        )
        
        x_loc = get_value(hole_dimensions.get('x', 0))

        hole.location = (x_loc, -thickness ,-0.1)
        hole.parent = obj
        hole.hide_viewport = True
        boolean_modifier = obj.modifiers.new(name="boolean", type="BOOLEAN")
        boolean_modifier.object = hole
        boolean_modifier.operation = "DIFFERENCE"
        boolean_modifier.solver = "FAST"

    obj.rotation_euler = (0, 0, angle/180 * math.pi)
    x_loc = get_value(x)
    y_loc = get_value(y)
    obj.location = (x_loc, y_loc, 0)

wall_config_file = os.path.join(os.path.dirname(os.path.dirname(__file__)),  'scripts/interior_wall_config.yaml')

with open(wall_config_file, 'r') as file:
    wall_config = yaml.safe_load(file)

def interior_wall_assembly():
    
    walls = wall_config['walls']
    
    for wall_name in walls:
        wall = walls[wall_name]
        interior_wall(
            name=wall_name,
            length=wall['length'],
            height=wall.get('height', 2.5),
            x=wall.get('x', 0),
            y=wall.get('y', 0),
            angle=wall.get('angle', 0),
            holes=wall.get('holes', [])
        )


