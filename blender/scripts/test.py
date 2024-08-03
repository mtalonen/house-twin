
import component_lib
import wall_element_assembly
import interior_wall_assembly
from clean_scene import clean_scene
import bpy
import os
import sys
import importlib

path = os.path.join(os.path.dirname(bpy.data.filepath), "./scripts")
sys.path.append(path)

importlib.reload(wall_element_assembly)
importlib.reload(interior_wall_assembly)
importlib.reload(component_lib)


clean_scene()
wall_element_assembly.wall_element_assembly()
interior_wall_assembly.interior_wall_assembly(
    'scripts/interior_wall.assembly.yaml')
