import math
import random
from globalinnovationcounter import get_next_innovation_number
from connectionGene import ConnectionGene
from node import Node
from assign_layers import assign_layers


class Genome:

    def __init__(self, fitness=0):  ### lets initialize the genome with empty lists for nodes and connections ###
        self.nodes = []
        self.connections = []
        self.fitness = fitness  # initialize fitness of model to 0
        self.adjusted_fitness = 0.0
        self.connectionMap = {}
        self.species = -1
        self.probOfParent = 0

    def add_node(self, node):
        self.nodes.append(node)

    def add_connection(self, connection):
        key = (connection.in_node, connection.out_node)
        if key in self.connectionMap:
            # print(f"Connection from {connection.in_node} to {connection.out_node} already exists for genome {self}. Skipping.")
            return
        else:
        # Skip adding if connection already exists
            self.connections.append(connection)
            self.connectionMap[key] = connection

    def set_species(self, species_num):
        self.species = species_num

    def load_inputs(self, inputs):
        # Get input nodes
        input_nodes = [node for node in self.nodes if node.node_type == 'input']

        # Ensure the number of inputs matches the number of input nodes
        if len(inputs) != len(input_nodes):
            raise ValueError("Number of inputs does not match number of input nodes")

        # Load inputs into the input nodes
        for node, input_value in zip(input_nodes, inputs):
            node.sum_input = input_value
            node.sum_output = input_value

    def activate(self, value):
        # Clamp the value to a reasonable range to prevent overflow
        value = max(min(value, 500), -500)
        return 1 / (1 + math.exp(-value))
        # RELU
        # return max(0, value)

    def __repr__(self):  # Provide a detailed string representation of the genome
        return f"Genome(nodes={self.nodes}, connections={self.connections}, fitness={self.fitness}, adjusted_fitness={self.adjusted_fitness}, species={self.species})"

    def forward(self, inputs):
        # Load inputs into input nodes
        self.load_inputs(inputs)

        # Process nodes layer by layer
        for layer in sorted(set(node.layer for node in self.nodes)):
            if layer == 0:  # Skip input layer as they are already loaded
                continue
            for node in self.nodes:
                if node.layer == layer:
                    # Reset input sum for the current node
                    node.sum_input = 0

                    # Scan through connections to find those terminating at this node
                    for connection in self.connections:
                        if connection.enabled and connection.out_node == node.node_id:
                            in_node = next(n for n in self.nodes if n.node_id == connection.in_node)
                            node.sum_input += in_node.sum_output * connection.weight

                    # Apply activation function and set output value for the node
                    node.sum_output = self.activate(node.sum_input)

        # Collect output values
        output_nodes = [node for node in self.nodes if node.node_type == 'output']
        outputs = [node.sum_output for node in output_nodes]

        return outputs

    def mutation(self):
        ## weight mutation
        self.mutate_weight()

        if random.random() < 0.01:  # 5% chance for connection mutation
            self.add_connection_mutation()
        #
        if random.random() < 0.006:  # 3% chance for node mutation
            self.add_node_mutation()

    def mutate_weight(self):
        for connection in self.connections:
            if random.random() < 0.8:  # 80% chance of connection weight being mutated
                if random.random() < 0.9:  # 90% chance of + or - 20% change
                    mutation_coefficient = random.uniform(-0.2, 0.2)
                    if mutation_coefficient * connection.weight > 2.5:  #control the amount it can go up or down
                        change = 2.5
                        connection.weight += change
                    elif mutation_coefficient * connection.weight < -2.5:
                        change = -2.5
                        connection.weight += change
                    else:
                        connection.weight += mutation_coefficient * connection.weight
                else:  # 10 % chance of weight becoming competely new
                    connection.weight = random.uniform(-10.0, 10.0)

    def add_node_mutation(self):

        enabled_connections = [c for c in self.connections if c.enabled]
        if not enabled_connections:
            print(self)
            return  # Exit the function if no enabled connections
        connection = random.choice(enabled_connections)
        connection.enabled = False
        # print("DISABLED CONNECTION:    ", connection)
        new_node_id = len(self.nodes)
        new_node = Node(new_node_id, 'hidden')
        self.add_node(new_node)

        new_connection1 = ConnectionGene(connection.in_node, new_node_id, connection.weight, True,
                                         get_next_innovation_number(connection.in_node, new_node_id))
        new_connection2 = ConnectionGene(new_node_id, connection.out_node, random.uniform(-10.0, 10.0), True,
                                         get_next_innovation_number(new_node_id, connection.out_node))

        self.add_connection(new_connection1)
        self.add_connection(new_connection2)

        # print("new node: ", new_node_id)

        assign_layers(self)

    def add_connection_mutation(self, max_attempts=20):
        for _ in range(max_attempts):
            node1 = random.choice(self.nodes)
            node2 = random.choice(self.nodes)

            # Ensure node1 and node2 are not the same, not on the same layer, and node1 is not later than node2
            if self.is_valid_connection(node1, node2):
                # Attempt to add the connection
                weight = random.uniform(-10.0, 10.0)
                new_connection = ConnectionGene(node1.node_id, node2.node_id, weight, True, get_next_innovation_number(node1.node_id, node2.node_id))

                self.add_connection(new_connection)

                # print("New connection added:", new_connection)
                assign_layers(self)
                print("DUHSADHAUSHDOASHDOA")
                break  # Exit if a valid connection is added
        return

    #
    def is_valid_connection(self, in_node, out_node):
        # Prevent self-connections
        if (in_node.node_id, out_node.node_id) in self.connectionMap.keys():
            return False
        if in_node.node_id == out_node.node_id:
            return False
        # Ensure feedforward connections based on node types and IDs
        if in_node.node_type == 'input' and out_node.node_type == 'input':
            return False  # Input nodes should not connect to other input nodes
        if in_node.node_type == 'output':
            return False  # Output nodes should not be the source of connections
        if in_node.node_type == 'hidden' and out_node.node_type == 'input':
            return False  # Hidden nodes should not connect to input nodes
        if in_node.node_type == 'hidden' and out_node.node_type == 'hidden' and in_node.layer >= out_node.layer:
            return False  # Hidden nodes should connect to later hidden nodes (by ID)
        if in_node.layer >= out_node.layer:
            return False
        return True

