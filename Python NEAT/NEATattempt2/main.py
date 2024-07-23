import random
from globalinnovationcounter import get_next_innovation_number
from node import Node
from connectionGene import ConnectionGene
from genome2 import Genome
from assign_layers import assign_layers
from functions import evaluate_fitness
from functions import initialize_population
from speciate import count_excess_genes
from speciate import count_disjoint_genes
from speciate import average_weight_difference
from speciate import calculate_distance
from speciate import adjust_fitness
from speciate import speciate
from speciate import allowed_offspring
from speciate import adjust_compatibility_threshold
from globalinnovationcounter import global_connection_map
from crossover import crossover
from crossover import create_new_population_through_crossover
from functions import initialize_populationDELUXE
from functions import evaluate_fitness_PRINT
from functions import select_top_survivors
import copy

from visualize_genome import visualize_genome

import copy


def filter_disabled_genomes(population):
    return [genome for genome in population if any(connection.enabled for connection in genome.connections)]


population = initialize_population(2, 1, 100)
# population = initialize_populationDELUXE(2, 1, 10, 500)

compatibility_threshold = 6
compatibility_modifier = 0.3
target_species_count = 5
maxFitness = 0
bestgenome = None
#
# for i in range(20000):
#     population[0].mutation()
#
# for node in population[0].nodes:
#     print(node.node_id, ":", node.layer)
# visualize_genome(population[0])
#


for generation in range(2000):
    print("GENERATION: ", generation)

    species = speciate(population, compatibility_threshold, compatibility_modifier, target_species_count)
    compatibility_threshold = adjust_compatibility_threshold(species, compatibility_threshold, compatibility_modifier,
                                                             target_species_count)

    for s in species:
        for member in s:
            assign_layers(member)
            evaluate_fitness(member)

    adjust_fitness(species)


    print("NUMBER OF SPECIES: ", len(species))
    print("ALLOWED OFFSPRING: ", allowed_offspring(species))
    print("DISTANCE BETWEEN THEM = ", calculate_distance(population[0], population[1]))

    new_population = create_new_population_through_crossover(species)
    species = select_top_survivors(species, 40)

    MAXFITNESSPERGENERATION = 0
    best_genome_of_generation = None  # Track the best genome of the current generation

    for person in new_population:
        person.mutation()
        assign_layers(person)
        evaluate_fitness(person)
        if person.fitness > MAXFITNESSPERGENERATION:
            MAXFITNESSPERGENERATION = person.fitness
            best_genome_of_generation = copy.deepcopy(person)

    population = new_population

    if MAXFITNESSPERGENERATION > maxFitness:
        maxFitness = MAXFITNESSPERGENERATION
        bestgenome = best_genome_of_generation

    print(f"Max Fitness in Generation {generation}: {MAXFITNESSPERGENERATION}")
    print("MAX FITNESS SO FAR: ", maxFitness)
    print("BEST GENOME TEST: ", evaluate_fitness_PRINT(bestgenome))
    # if generation % 100 == 0:
    #     visualize_genome(bestgenome)

print("FINAL MAXFITNESS:", maxFitness)
print("FINAL BEST GENOME FITNESS:", bestgenome.fitness)
print("BEST GENOME TEST: ", evaluate_fitness_PRINT(bestgenome))
print("best genome nodes: ", bestgenome.nodes)
print("best genome connections: ", bestgenome.connections)
visualize_genome(bestgenome)
