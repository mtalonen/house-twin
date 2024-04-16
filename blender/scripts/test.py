import math
import bpy
import os
import sys
import importlib
path = os.path.join(os.path.dirname(bpy.data.filepath), "./scripts")
sys.path.append(path)

from clean_scene import clean_scene
import elementti2
importlib.reload(elementti2)

from ontelolaatta import ontelolaatta

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

wall1, x1 = linear_assembly(
    name="Wall1",
    components=["t6", "x12", "t6", "x12", "x12", "t5", "x12", "m12", "m12", "x12", "m6", "m6", "x12","x2"]
)

wall2, x2 = linear_assembly(
    name="Wall2",
    components=["t6", "x12", "x2"]
)
wall2.location = (x1, thickness, 0)
wall2.rotation_euler = (0, 0, math.pi/2)

wall3, x3 = linear_assembly(
    name="Wall3",
    components=["m12", "x12","x2"]
)
wall3.location = (x1,x2, 0)

wall4, x4 = linear_assembly(
    name="Wall4",
    components=["m12", "t6", "x12", "x12", "x12", "t6", "m12", "x2"]
)
wall4.location = (x1 + x3, thickness + x2, 0)
wall4.rotation_euler = (0, 0, math.pi/2)

wall5, x5 = linear_assembly(
    name="Wall5",
    components=["t12", "x12",  "x12", "x12", "bm12", "x2"]
)
wall5.location = (x1 + x3 - thickness, thickness + x2 + x4, 0)
wall5.rotation_euler = (0, 0, math.pi)

wall6, x6 = linear_assembly(
    name="Wall6",
    components=["bm6", "x12", "x2"]
)
wall6.location = (x1 + x3 - thickness - x5, x2 + x4, 0)
wall6.rotation_euler = (0, 0, -math.pi/2)
