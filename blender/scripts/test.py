import bpy
import os
import sys

path = os.path.join(os.path.dirname(bpy.data.filepath), "./scripts")
sys.path.append(path)

from clean_scene import clean_scene
import elementti2

import importlib

importlib.reload(elementti2)

from ontelolaatta import ontelolaatta

clean_scene()

ontelolaatta()

bpy.context.view_layer.objects.selected = []

wall1 = ["t6", "x12", "t6", "x12", "x12", "m12", "m12"]

x = 0
for type in wall1:
    obj, width = elementti2.elementti(type1=type)
    bpy.context.view_layer.objects.active = obj
    obj.location = (x, 0, 0)
    x = x + width
