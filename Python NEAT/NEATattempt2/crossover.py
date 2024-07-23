from speciate import allowed_offspring
from genome2 import Genome
import random
from connectionGene import ConnectionGene


def create_new_population_through_crossover(species):
    new_population = []
    total_species_count = len(species)
    allowed_offspring_list = allowed_offspring(species)
    for i in range(len(species)):
        total_fitness_for_s = 0
        for member in species[i]:
            total_fitness_for_s += member.fitness
        for j in range(allowed_offspring_list[i]):
            #calculate total fitness
            parent1 = select_parent(species[i], total_fitness_for_s)
            parent2 = select_parent(species[i], total_fitness_for_s)

            child = crossover(parent1, parent2)
            new_population.append(child)

    return new_population


def select_parent(species_population, total_fitness):
    selection_prob = [genome.fitness / total_fitness for genome in species_population]
    # print("SELECTION PROBABILITIES: ", selection_prob)
    # print("RANDOM CHOICES: ", random.choices(species_population, weights=selection_prob, k=1)[0])
    return random.choices(species_population, weights=selection_prob, k=1)[0]


def crossover(parent1, parent2):
    if parent1.fitness < parent2.fitness:
        parent1, parent2 = parent2, parent1
    # print("BREEDING TWO NODES WITH THESE COUNTS: ", len(parent2.nodes), "AND: ", len(parent1.nodes))
    child = Genome()
    added_nodes = {}

    # inherit matching genes
    for gene1 in parent1.connections:
        match = False
        for gene2 in parent2.connections:
            if gene1.innovation_number == gene2.innovation_number:
                match = True
                if random.random() < 0.5:
                    chosen_gene = gene1
                else:
                    chosen_gene = gene2
                break
        if match:
            # print("HOORAY!")
            in_node_id = chosen_gene.in_node
            out_node_id = chosen_gene.out_node
            if in_node_id not in added_nodes:
                in_node = next(node for node in parent1.nodes + parent2.nodes if node.node_id == in_node_id)
                child.add_node(in_node)
                added_nodes[in_node_id] = in_node
            if out_node_id not in added_nodes:
                out_node = next(node for node in parent1.nodes + parent2.nodes if node.node_id == out_node_id)
                child.add_node(out_node)
                added_nodes[out_node_id] = out_node
            if random.random() < 0.5:
                child.add_connection(ConnectionGene(in_node_id, out_node_id, chosen_gene.weight, chosen_gene.enabled, chosen_gene.innovation_number))
            else:
                child.add_connection(ConnectionGene(in_node_id, out_node_id, chosen_gene.weight, True, chosen_gene.innovation_number))
        # Inherit excess and disjoint genes from the more fit parent
        for gene in parent1.connections:
            if not any(gene.innovation_number == g.innovation_number for g in parent2.connections):
                in_node_id = gene.in_node
                out_node_id = gene.out_node
                if in_node_id not in added_nodes:
                    in_node = next(node for node in parent1.nodes if node.node_id == in_node_id)
                    child.add_node(in_node)
                    added_nodes[in_node_id] = in_node
                if out_node_id not in added_nodes:
                    out_node = next(node for node in parent1.nodes if node.node_id == out_node_id)
                    child.add_node(out_node)
                    added_nodes[out_node_id] = out_node
                child.add_connection(
                    ConnectionGene(in_node_id, out_node_id, gene.weight, gene.enabled, gene.innovation_number))

    return child
