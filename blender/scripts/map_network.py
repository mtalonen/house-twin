def map_network(node):
    out = {}
    if 'type' in node:
        out['type'] = node['type']
        out["diameter"] = node["diameter"]

        if node['type'] == 'hvac_duct_t2':
            child1 = {
                "name": "out1",
                "location": {
                    "x": 0.3,
                    "y": 0.3
                },
                "rotation": {
                    "angle": 90
                }
            }
            if "out1" in node:
                nodeOut1 = node["out1"]
                if 'rotation' in nodeOut1:
                    child1["rotation"]['x'] = nodeOut1["rotation"]
                child1['components'] = map_network(nodeOut1)

            child2 = {
                "name": "out2",
                "location": {
                    "x": 0.6,
                },
            }
            if "out2" in node:
                nodeOut2 = node["out2"]
                if 'rotation' in nodeOut2:
                    child2["rotation"] = {'x': nodeOut2["rotation"]}
                child2['components'] = map_network(nodeOut2)

            out["components"] = [child1, child2]

        if node['type'] == 'hvac_duct_t':
            child1 = {
                "name": "out1",
                "location": {
                    "x": 0.3,
                    "y": 0.3
                },
                "rotation": {
                    "angle": 90
                }
            }
            if "out1" in node:
                nodeOut1 = node["out1"]
                if 'rotation' in nodeOut1:
                    child1["rotation"]['x'] = nodeOut1["rotation"]
                child1['components'] = map_network(nodeOut1)

            child2 = {
                "name": "out2",
                "location": {
                    "x": 0.3,
                    "y": -0.3
                },
                "rotation": {
                    "angle": -90
                }
            }
            if "out2" in node:
                nodeOut2 = node["out2"]
                if 'rotation' in nodeOut2:
                    child2["rotation"]['x'] = nodeOut2["rotation"]
                child2['components'] = map_network(nodeOut2)

            out["components"] = [child1, child2]

        if node['type'] == 'hvac_duct_90':
            if "out" in node:
                child = {
                    "name": "out",
                    "location": {
                        "x": 0.3,
                        "y": 0.3
                    },
                    "rotation": {
                        "angle": 90
                    }
                }
                if 'rotation' in node['out']:
                    child["rotation"]['x'] = node['out']["rotation"]

                child['components'] = map_network(node["out"])
                out["components"] = [child]

        if node['type'] == 'hvac_duct':
            out['length'] = node['length']

            child = {
                "name": "out",
                "location": {
                    "x": node["length"]
                },

            }
            if "out" in node:
                child['components'] = map_network(node["out"])
                if 'rotation' in node["out"]:
                    child["rotation"] = {
                        "x": node["out"]["rotation"]
                    }

            out["components"] = [child]

    return [out]
