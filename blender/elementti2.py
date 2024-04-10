import bpy
import re

def elementti(type1):

    r = re.compile("([a-zA-Z]+)([0-9]+)")
    m = r.match(type1)

    type = m.group(1)
    w  = m.group(2)
    width = int(w)/10 

    depth = 0.2
    height = 2.7

    node_x_step = 200

    def window_nodes(node_group, y=-300, window_type='top' ):
        window_width = width - 0.2

        small_height = 0.3
        normal_height = 1.2

        top_position = 0.8
        normal_position = 0.2
        bottom_position = -0.6

        window_height = normal_height if window_type == 'middle' else small_height
        window_position = top_position if window_type == 'top' else bottom_position if window_type == 'bottom' else normal_position

        window_hole = node_group.nodes.new(type="GeometryNodeMeshCube")
        window_hole.location.y = y
        window_hole.location.x = -node_x_step  
        window_hole.inputs["Size"].default_value = (window_width, depth, window_height)

        window_hole_translate = node_group.nodes.new(type="GeometryNodeTransform")
        window_hole_translate.location.y = y
        window_hole_translate.inputs['Translation'].default_value = (0, 0, window_position)

        node_group.links.new(window_hole.outputs["Mesh"], window_hole_translate.inputs["Geometry"])

        return window_hole_translate


    mesh = bpy.data.meshes.new(name="Mesh")
    obj = bpy.data.objects.new(name="Elementti", object_data=mesh)
    bpy.context.collection.objects.link(obj)
    
    obj.select_set(True)
    
    node_tree = obj.modifiers.new(name="Hello", type="NODES")    
    node_tree.node_group = bpy.data.node_groups.new("Elementti", 'GeometryNodeTree')

    node_group = node_tree.node_group
    node_group.interface.new_socket(name="Geometry",in_out ="OUTPUT", socket_type="NodeSocketGeometry")    
      
    body = node_group.nodes.new(type="GeometryNodeMeshCube")
    body.inputs["Size"].default_value = (width, depth, height)

    window_cutter = node_group.nodes.new(type="GeometryNodeMeshBoolean")
    window_cutter.location.x = node_x_step    

    if (type == 'b' or type == 'bm'):
        window_bottom = window_nodes(node_group, window_type='bottom')
        node_group.links.new(window_bottom.outputs["Geometry"], window_cutter.inputs["Mesh 2"])

    if (type == 'm' or type == 'bm'):
        window_top = window_nodes(node_group, -600, window_type='middle')
        node_group.links.new(window_top.outputs["Geometry"], window_cutter.inputs["Mesh 2"])

    if (type == 't'):
        window_top = window_nodes(node_group, -900, window_type='top')
        node_group.links.new(window_top.outputs["Geometry"], window_cutter.inputs["Mesh 2"])


    node_group.links.new(body.outputs["Mesh"], window_cutter.inputs["Mesh 1"])

    originTransform = node_group.nodes.new(type="GeometryNodeTransform")
    originTransform.inputs['Translation'].default_value = (width/2, depth/2, height/2)
    originTransform.location.x = 2 * node_x_step
    node_group.links.new(window_cutter.outputs["Mesh"], originTransform.inputs["Geometry"])

    out_node = node_group.nodes.new(type="NodeGroupOutput")
    out_node.location.x = 3 * node_x_step
    node_group.links.new(originTransform.outputs["Geometry"], out_node.inputs["Geometry"])
    
    
    
    return obj, width