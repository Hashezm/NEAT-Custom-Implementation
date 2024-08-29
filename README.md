# NEAT-Custom-Implementation
NeuroEvolution of Augmenting Topologies implementation from scratch using information from K. O Stanley's original research paper (check file stanley.pdf - Copy) as well as his neat-users-page Q&amp;A (https://www.kenstanley.net/neat-users-page). This algorithm dynamically evolves neural networks by adding nodes and connections, optimizing weights, and using speciation to maintain diversity. So far, I have tested my NEAT implementation on the simple XOR problem, and I am continuously working on further applications of this "neat" algorithm!

## Overview

NEAT is an evolutionary algorithm that evolves neural networks. This implementation dynamically evolves the network's structure by adding nodes and connections, optimizing weights, and using speciation to maintain diversity. The algorithm achieves high accuracy and demonstrates the potential of NEAT in evolving complex neural networks.

## Features
- **Dynamic Node and Connection Mutation:**
  - Node Mutation: Randomly adds nodes to the neural network, enabling the evolution of complex structures.
  - Connection Mutation: Adds connections between nodes, allowing the network to form new pathways.
- **Speciation:**
  - Speciation Mechanism: Divides the population into species based on genetic similarity.
  - Compatibility Threshold Adjustment: Adjusts the threshold to maintain a target number of species, ensuring diversity.
- **Fitness Evaluation:**
  - Fitness Function: Customizable fitness evaluation to measure the performance of each genome.
  - Adjusted Fitness: Adjusts fitness values within species to promote diversity.
- **Crossover:**
  - Crossover Function: Combines genomes from different parents to produce offspring, preserving beneficial mutations.
  - New Population Creation: Generates a new population through crossover, ensuring continuity and innovation.
- **Survivors Selection:**
  - Top Survivors Selection: Selects the top-performing genomes in each species to pass on their genes to the next generation.
- **Visualization:**
  - Genome Visualization: Visualizes the structure of the best genome, providing insight into the evolved neural network.
- **Population Generation:**
  - Population Initialization: Initializes the population with specified input, output.
  - Deluxe Initialization: Advanced initialization option for the starting population including initial hidden nodes.
- **Utility Functions:**
  - Filter Disabled Genomes: Removes genomes with all connections disabled to maintain an effective population.
  - Layer Assignment: Assigns layers to nodes for proper neural network topology.
  - Global Innovation Counter: Ensures unique innovation numbers for new mutations, facilitating crossover and speciation.
- **Execution Loop:**
  - Generational Loop: Iterates through generations, applying mutation, crossover, and evaluation to evolve the population.
  - Fitness Tracking: Tracks and prints the maximum fitness in each generation, along with the best genome's fitness.
- **Customizability:**
  - Parameters: Population Size, Number of Generations, Node Mutation Rate, Connection Mutation Rate, Weight Mutation Rate, Weight Mutation Strength, Compatibility Threshold, Compatibility Modifier, Target Species Count, Adjusted Fitness, Survival Threshold, Crossover Rate, Interspecies Mating Rate, Disabled Gene Inheritance, Selection Proportion, Champion Copy Minimum, Global Innovation Counter, Fitness No Improvement Limit.
  - Modular Design: Organized code structure with separate modules for different functionalities, allowing easy customization and extension.

### Results

The NEAT implementation successfully evolves neural networks that solve the XOR problem with extremely high accuracy, MAXIMUM FITNESS = 4. Example outputs (BEST GENOME IS VISUALIZED USING MATPLOTLIB):
**NOTE:** Multiple weights on one connection line is an indication of overlapping connections between neurons.
- ![image](https://github.com/user-attachments/assets/bd4d240c-7583-4abd-8956-e8c02b970dc6) EVOLVED FROM POPULATION OF 2 INPUT NODES, 1 HIDDEN NODE, 1 OUTPUT NODE
- OUTPUT:  3.144372587256935e-08
- EXPECTED:  0
- OUTPUT:  0.9999996014919881
- EXPECTED:  1
- OUTPUT:  0.9999955192058493
- EXPECTED:  1
- OUTPUT:  6.300895687077827e-25
- EXPECTED:  0
- BEST GENOME TEST:  3.9999950892541114
- ![image](https://github.com/user-attachments/assets/27446b07-04a3-4849-9f83-bc81e3fcc50a) EVOLVED FROM POPULATION OF 2 INPUT NODES, 0 HIDDEN NODES, 1 OUTPUT NODE
- OUTPUT:  6.4472244260940115e-06
- EXPECTED:  0
- OUTPUT:  0.9999675106118514
- EXPECTED:  1
- OUTPUT:  0.9982781687590014
- EXPECTED:  1
- OUTPUT:  0.0036374236046334244
- EXPECTED:  0
- BEST GENOME TEST:  3.9946018085417934

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.


