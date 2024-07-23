global_innovation_counter = 0  # Global counter shared by all instances
global_connection_map = {}
def get_next_innovation_number(in_node, out_node):
    global global_innovation_counter
    global global_connection_map

    key = (in_node, out_node)

    if key not in global_connection_map:
        global_connection_map[key] = global_innovation_counter
        global_innovation_counter += 1

    return global_connection_map.get(key)