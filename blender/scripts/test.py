import interior_wall_assembly
import wall_element_assembly
from clean_scene import clean_scene
import bpy
import os
import sys
import importlib

path = os.path.join(os.path.dirname(bpy.data.filepath), "./scripts")
sys.path.append(path)


importlib.reload(wall_element_assembly)

importlib.reload(interior_wall_assembly)


clean_scene()
wall_element_assembly.wall_element_assembly()
interior_wall_assembly.interior_wall_assembly(
    'scripts/interior_wall.assembly.yaml')
