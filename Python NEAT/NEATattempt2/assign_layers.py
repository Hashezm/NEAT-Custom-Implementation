def assign_layers(genome):
    # Initialize the layers for all nodes
    for node in genome.nodes:
        node.layer = -1  # Set initial layer to -1 (undefined)

    # Set input nodes to layer 0
    input_nodes = [node for node in genome.nodes if node.node_type == 'input']
    for node in input_nodes:
        node.layer = 0  # Input nodes are at layer 0

    # Use a queue to assign layers to all other nodes
    queue = input_nodes[:]  # Start with input nodes in the queue
    while queue:
        current_node = queue.pop(0)  # Get the next node from the queue
        current_layer = current_node.layer  # Get the current node's layer

        # Process all outgoing connections of the current node
        for connection in genome.connections:
            if connection.enabled and connection.in_node == current_node.node_id:
                # Find the node that is the output of this connection
                out_node = next(n for n in genome.nodes if n.node_id == connection.out_node)

                # If the output node's layer is not correctly set, update it
                if out_node.layer <= current_layer:
                    out_node.layer = current_layer + 1  # Set layer to one more than current node's layer
                    queue.append(out_node)  # Add the output node to the queue for further processing

# def assign_layers(genome):
#     # Initialize the layers for all nodes
#     for node in genome.nodes:
#         node.layer = -1  # Set initial layer to -1 (undefined)
#
#     # Set input nodes to layer 0
#     input_nodes = [node for node in genome.nodes if node.node_type == 'input']
#     for node in input_nodes:
#         node.layer = 0  # Input nodes are at layer 0
#
#     # Use a queue to assign layers to all other nodes
#     queue = input_nodes[:]  # Start with input nodes in the queue
#     visited = set()  # Keep track of visited nodes to prevent infinite loops
#
#     while queue:
#         current_node = queue.pop(0)  # Get the next node from the queue
#         current_layer = current_node.layer  # Get the current node's layer
#
#         # Process all outgoing connections of the current node
#         for connection in genome.connections:
#             if connection.enabled and connection.in_node == current_node.node_id:
#                 # Find the node that is the output of this connection
#                 out_node = next(n for n in genome.nodes if n.node_id == connection.out_node)
#
#                 # If the output node's layer is not correctly set, update it
#                 if out_node.layer <= current_layer:
#                     out_node.layer = current_layer + 1  # Set layer to one more than current node's layer
#                     if out_node.node_id not in visited:
#                         queue.append(out_node)  # Add the output node to the queue for further processing
#                         visited.add(out_node.node_id)  # Mark the node as visited
