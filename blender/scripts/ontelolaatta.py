import bpy
import math

def ontelolaatta():

    w_slab = 1.2    
    z_slab = 0.2
    n_holes = 5
    r_hole = 0.075
    d_hole = 0.25

    n_x0 = -100
    n_w = 200


    bpy.ops.mesh.primitive_plane_add()
    bpy.ops.node.new_geometry_nodes_modifier()
    node_tree = bpy.data.node_groups["Geometry Nodes"]
    node_tree.name = "Ontelolaatta"

    out_node = node_tree.nodes["Group Output"]
    out_node.location.x = 600
    
    cube1 = node_tree.nodes.new(type="GeometryNodeMeshCube")
    cube1.location.x = n_x0
    cube1.location.y = 150
    cube1.inputs["Size"].default_value = (w_slab ,1 , z_slab)

    boolean = node_tree.nodes.new(type="GeometryNodeMeshBoolean")
    boolean.location.x = n_x0 + 2.5*n_w

    for i in range(n_holes):
        node_y = -330*i + -100
        
        hole = node_tree.nodes.new(type="GeometryNodeMeshCylinder")
        hole.location.x = n_x0
        hole.location.y = node_y
        hole.inputs["Radius"].default_value = r_hole
                

        transform2 = node_tree.nodes.new(type="GeometryNodeTransform")
        transform2.location.x = n_x0 + n_w
        transform2.location.y = node_y
        transform2.inputs["Rotation"].default_value = (math.pi/2,0,0)
        transform2.inputs["Translation"].default_value = (d_hole*(0.5 + i - n_holes/2),0,0)

        node_tree.links.new(hole.outputs["Mesh"], transform2.inputs["Geometry"])
        node_tree.links.new(boolean.outputs["Mesh"], out_node.inputs["Geometry"])
        node_tree.links.new(transform2.outputs["Geometry"], boolean.inputs["Mesh 2"])


    node_tree.links.new(cube1.outputs["Mesh"], boolean.inputs["Mesh 1"])

