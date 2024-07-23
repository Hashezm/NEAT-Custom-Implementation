from assign_layers import assign_layers
import matplotlib.pyplot as plt
import networkx as nx


def visualize_genome(genome):
    assign_layers(genome)

    # Create a directed graph
    G = nx.DiGraph()

    # Add nodes with positions based on layers and node IDs
    pos = {}
    layer_nodes = {}
    for node in genome.nodes:
        if node.layer not in layer_nodes:
            layer_nodes[node.layer] = []
        layer_nodes[node.layer].append(node)

    for layer, nodes in layer_nodes.items():
        for i, node in enumerate(nodes):
            pos[node.node_id] = (layer, -i)

    # Add edges with weights as labels
    edge_colors = []
    edge_labels = {}
    for connection in genome.connections:
        if connection.enabled:
            G.add_edge(connection.in_node, connection.out_node)
            edge_colors.append('green')
            edge_labels[(connection.in_node, connection.out_node)] = f"{connection.weight:.2f}"
        # else:
        #     G.add_edge(connection.in_node, connection.out_node)
        #     edge_colors.append('red')

        # Position the weight label closer to the target node


    # Draw the nodes
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightblue')

    # Draw the edges with colors based on whether they are enabled
    nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=20, edge_color=edge_colors)

    # Draw node labels
    nx.draw_networkx_labels(G, pos, font_size=12, font_color='black')

    # Draw edge labels (weights)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=0.7, font_size=10)

    # Display the plot
    plt.title('Genome Visualization')
    plt.show()
