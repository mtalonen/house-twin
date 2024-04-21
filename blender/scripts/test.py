import math
import bpy
import os
import sys
import importlib
import yaml

path = os.path.join(os.path.dirname(bpy.data.filepath), "./scripts")
sys.path.append(path)

from clean_scene import clean_scene
import elementti2
importlib.reload(elementti2)

from ontelolaatta import ontelolaatta


wall_config_file = os.path.join(os.path.dirname(os.path.dirname(__file__)),  'scripts/walls.yaml')

with open(wall_config_file, 'r') as file:
    wall_config = yaml.safe_load(file)


clean_scene()
#ontelolaatta()

thickness = 0.2

def linear_assembly(components, name):
    wall_collection = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(wall_collection)
    parent_obj = bpy.data.objects.new("empty", None)
    parent_obj.name = name + "_parent"
    wall_collection.objects.link(parent_obj)

    x = 0
    for type in components:
        obj, width = elementti2.elementti(type1=type)
        obj.parent = parent_obj
        wall_collection.objects.link(obj)

        bpy.context.view_layer.objects.active = obj
        obj.location = (x, 0, 0)
        x = x + width

    return parent_obj, x


bpy.context.view_layer.objects.selected = []

x = 0
y = 0
angle = 0

for key in wall_config:
    if wall_config[key][0] == 'UKT':
        width = .2
        x = x + width * math.cos(angle)
        y = y + width * math.sin(angle)
        angle = angle + math.pi/2
        x = x + width * math.cos(angle)
        y = y + width * math.sin(angle)

    elif wall_config[key][0] == 'SK':
        width = .1
        x = x + width * math.cos(angle)
        y = y + width * math.sin(angle)
        angle = angle - math.pi/2
        x = x + width * math.cos(angle)
        y = y + width * math.sin(angle)

    elif wall_config[key][0] == 'DET_A2_2303':
        width = .134
        x = x + width * math.cos(angle)
        y = y + width * math.sin(angle)
        angle = angle - math.pi/4
        x = x + width * math.cos(angle)
        y = y + width * math.sin(angle)

    else:
        obj, width = linear_assembly(
            name=key,
            components=wall_config[key]
        )
        obj.location = (x, y, 0)
        obj.rotation_euler = (0, 0, angle)
        x = x + width * math.cos(angle)
        y = y + width * math.sin(angle)
