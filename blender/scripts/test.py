import wall_element_assembly
import interior_wall_assembly
import component_lib
import map_network
from clean_scene import clean_scene
import importlib

importlib.reload(component_lib)
importlib.reload(wall_element_assembly)
importlib.reload(interior_wall_assembly)
importlib.reload(map_network)


clean_scene()
wall_element_assembly.wall_element_assembly()
interior_wall_assembly.interior_wall_assembly(
    'scripts/interior_wall.assembly.yaml')
