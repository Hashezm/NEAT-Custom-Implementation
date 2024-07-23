from globalinnovationcounter import get_next_innovation_number
from genome2 import Genome
from node import Node
import random
from connectionGene import ConnectionGene



# def evaluate_fitness(genome):
#     # Define XOR problem input-output pairs
#     xor_inputs = [
#         ([0, 0], [0]),
#         ([0, 1], [1]),
#         ([1, 0], [1]),
#         ([1, 1], [0])
#     ]
#
#     total_error = 0.0
#
#     for inputs, expected_output in xor_inputs:
#         # Get the network's output
#         output = genome.forward(inputs)
#
#         # Calculate the squared error for this input-output pair
#         error = (output[0] - expected_output[0]) ** 2
#         total_error += error
#
#         # print("OUTPUT: ", output[0])
#         # print("EXPECTED: ", expected_output[0])
#         # print("ERROR: ", error)
#
#     # The fitness is the inverse of the total error (lower error means higher fitness)
#     fitness = 1 / (total_error + 1e-6)  # Add a small value to avoid division by zero
#     # fitness = math.log(fitness + 1)
#     genome.fitness = fitness
#
#     return fitness

def evaluate_fitness(genome):
    xor_inputs_outputs = [
        ([0, 0], [0]),
        ([0, 1], [1]),
        ([1, 0], [1]),
        ([1, 1], [0]),
    ]

    # print("EVALUATING FITNESS OF ", genome)

    total_fitness = 0.0
    for inputs, expected_output in xor_inputs_outputs:
        output = genome.forward(inputs)
        # Assuming output is a single value
        error = abs(output[0] - expected_output[0])
        total_fitness += 1 - error  # This assumes the output is between 0 and 1

        # print("OUTPUT: ", output[0])
        # print("EXPECTED: ", expected_output[0])
        # print("ERROR: ", error)


    genome.fitness = total_fitness
    return total_fitness

def evaluate_fitness_PRINT(genome):
    xor_inputs_outputs = [
        ([0, 0], [0]),
        ([0, 1], [1]),
        ([1, 0], [1]),
        ([1, 1], [0]),
    ]

    print("EVALUATING FITNESS OF ", genome)

    total_fitness = 0.0
    for inputs, expected_output in xor_inputs_outputs:
        output = genome.forward(inputs)
        # Assuming output is a single value
        error = abs(output[0] - expected_output[0])
        total_fitness += 1 - error  # This assumes the output is between 0 and 1

        print("OUTPUT: ", output[0])
        print("EXPECTED: ", expected_output[0])
        # print("ERROR: ", error)


    genome.fitness = total_fitness
    return total_fitness

def initialize_population(input_size, output_size, population_size):
    population = []  # Create an empty list to store the population
    maxInnovationNumber = 0
    for _ in range(population_size):  # Loop to create each genome
        genome = Genome()  # Create a new Genome instance
        # Create and add input nodes
        input_nodes = [Node(i, 'input') for i in range(input_size)]
        for node in input_nodes:
            genome.add_node(node)

        # Create and add output nodes
        output_nodes = [Node(input_size + i, 'output') for i in range(output_size)]
        for node in output_nodes:
            genome.add_node(node)

        # Create initial connections between input and output nodes
        for input_node in input_nodes:
            for output_node in output_nodes:
                weight = random.uniform(-10.0, 10.0)  # Generate a random weight for the connection
                # Add the connection gene to the genome
                connection = ConnectionGene(input_node.node_id, output_node.node_id, weight, True, get_next_innovation_number(input_node.node_id,output_node.node_id))
                genome.add_connection(connection)

        # Add the genome to the population
        population.append(genome)

    return population  # Return the initialized population


def initialize_populationDELUXE(input_size, output_size, hidden_size, population_size):
    population = []  # Create an empty list to store the population
    maxInnovationNumber = 0

    for _ in range(population_size):  # Loop to create each genome
        genome = Genome()  # Create a new Genome instance

        # Create and add input nodes
        input_nodes = [Node(i, 'input') for i in range(input_size)]
        for node in input_nodes:
            genome.add_node(node)

        # Create and add hidden nodes
        hidden_nodes = [Node(input_size + i, 'hidden') for i in range(hidden_size)]
        for node in hidden_nodes:
            genome.add_node(node)

        # Create and add output nodes
        output_nodes = [Node(input_size + hidden_size + i, 'output') for i in range(output_size)]
        for node in output_nodes:
            genome.add_node(node)

        # Create initial connections between input and hidden nodes
        for input_node in input_nodes:
            for hidden_node in hidden_nodes:
                weight = random.uniform(-10.0, 10.0)  # Generate a random weight for the connection
                # Add the connection gene to the genome
                connection = ConnectionGene(input_node.node_id, hidden_node.node_id, weight, True, get_next_innovation_number(input_node.node_id, hidden_node.node_id))
                genome.add_connection(connection)

        # Create initial connections between hidden nodes and output nodes
        for hidden_node in hidden_nodes:
            for output_node in output_nodes:
                weight = random.uniform(-10.0, 10.0)  # Generate a random weight for the connection
                # Add the connection gene to the genome
                connection = ConnectionGene(hidden_node.node_id, output_node.node_id, weight, True, get_next_innovation_number(hidden_node.node_id, output_node.node_id))
                genome.add_connection(connection)

        # Optionally create initial connections between input and output nodes
        for input_node in input_nodes:
            for output_node in output_nodes:
                weight = random.uniform(-10.0, 10.0)  # Generate a random weight for the connection
                # Add the connection gene to the genome
                connection = ConnectionGene(input_node.node_id, output_node.node_id, weight, True, get_next_innovation_number(input_node.node_id, output_node.node_id))
                genome.add_connection(connection)

        # Add the genome to the population
        population.append(genome)

    return population  # Return the initialized population


def select_top_survivors(species, survival_threshold=0.3):
    top_survivors = []
    for s in species:
        s.sort(key=lambda genome: genome.fitness, reverse=True)  # Sort genomes by fitness in descending order
        num_survivors = max(1, int(len(s) * survival_threshold))  # Ensure at least one survivor per species
        top_survivors.append(s[:num_survivors])  # Add the top genomes to the list of survivors
    return top_survivors




