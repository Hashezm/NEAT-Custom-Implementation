import random


def speciate(population, compatibility_threshold, compatibility_modifier, target_species_count):
    species = []
    speciesIds = []
    unassigned = population[:]
    count = 0
    while unassigned:  # Select a random genome as a new species representative
        new_species_rep = random.choice(unassigned)
        new_species = [new_species_rep]
        unassigned.remove(new_species_rep)

        for genome in unassigned[:]:
            if calculate_distance(new_species_rep, genome) < compatibility_threshold:
                new_species.append(genome)
                # print("DISTANCE: ", calculate_distance(new_species_rep, genome), "ASSIGNED SPECIES: ", count)
                unassigned.remove(genome)

        species.append(new_species)
        for s in new_species:
            s.species = count
        speciesIds.append(count)
        count += 1

    return species
    # return speciesIds


def adjust_compatibility_threshold(species, compatibility_threshold, compatibility_modifier, target_species_count):
    if len(species) < target_species_count:
        # print("OLD COMPATIBITLIY THRESHOLD = ", compatibility_threshold)
        compatibility_threshold -= compatibility_modifier
        print("NEW COMPATIBITLIY THRESHOLD = ", compatibility_threshold)
    elif len(species) > target_species_count:
        # print("OLD COMPATIBITLIY THRESHOLD = ", compatibility_threshold)
        compatibility_threshold += compatibility_modifier
        print("NEW COMPATIBITLIY THRESHOLD = ", compatibility_threshold)
    return compatibility_threshold


def calculate_distance(genome1, genome2, c1=2.0, c2=2.0, c3=1.0):
    excess_genes = count_excess_genes(genome1, genome2)
    disjoint_genes = count_disjoint_genes(genome1, genome2)
    avg_weight_diff = average_weight_difference(genome1, genome2)
    N = max(len(genome1.connections), len(genome2.connections))

    distance = ((c1 * excess_genes) / N) + ((c2 * disjoint_genes) / N) + (c3 * avg_weight_diff)
    return distance


def count_excess_genes(genome1, genome2):
    # Get the innovation numbers of the connections in both genomes
    innovation_numbers1 = [conn.innovation_number for conn in genome1.connections]
    innovation_numbers2 = [conn.innovation_number for conn in genome2.connections]

    # Find the maximum innovation numbers in both genomes
    max_innovation1 = max(innovation_numbers1)
    max_innovation2 = max(innovation_numbers2)

    # Count the excess genes
    excess_genes = 0

    if max_innovation1 > max_innovation2:
        for innovation_number in innovation_numbers1:
            if innovation_number > max_innovation2:
                excess_genes += 1
    else:
        for innovation_number in innovation_numbers2:
            if innovation_number > max_innovation1:
                excess_genes += 1

    return excess_genes


def count_disjoint_genes(genome1, genome2):
    innovation_numbers1 = {conn.innovation_number for conn in genome1.connections}
    innovation_numbers2 = {conn.innovation_number for conn in genome2.connections}

    max_innovation1 = max(innovation_numbers1, default=-1)
    max_innovation2 = max(innovation_numbers2, default=-1)

    lesser_max_innovation = min(max_innovation1, max_innovation2)

    disjoint_genes = 0

    for innovation_number in innovation_numbers1:
        if innovation_number not in innovation_numbers2 and innovation_number <= lesser_max_innovation:
            disjoint_genes += 1

    for innovation_number in innovation_numbers2:
        if innovation_number not in innovation_numbers1 and innovation_number <= lesser_max_innovation:
            disjoint_genes += 1

    return disjoint_genes


def average_weight_difference(genome1, genome2):
    # Create dictionaries to map innovation numbers to connection genes for quick lookup
    connections1 = {conn.innovation_number: conn for conn in genome1.connections}
    connections2 = {conn.innovation_number: conn for conn in genome2.connections}

    # Find matching genes and calculate the weight differences
    matching_genes = 0
    total_weight_difference = 0.0

    for innovation_number in connections1.keys():
        if innovation_number in connections2:
            weight1 = connections1[innovation_number].weight
            weight2 = connections2[innovation_number].weight
            total_weight_difference += abs(weight1 - weight2)
            matching_genes += 1

    # Calculate the average weight difference
    if matching_genes == 0:
        return 0.0
    else:
        return total_weight_difference / matching_genes


def adjust_fitness(species):
    for s in species:
        species_size = len(s)
        for genome in s:
            genome.adjusted_fitness = genome.fitness / species_size


def allowed_offspring(species):
    total_avg_fitness = 0
    members = 0
    for s in species:
        for member in s:
            total_avg_fitness += member.adjusted_fitness
            # print(member.adjusted_fitness)
            members += 1

    global_avg_adjusted_fitness = total_avg_fitness / members
    # print(global_avg_adjusted_fitness)
    avg_adjusted_fitness = []
    for s in species:
        no_of_members = 0
        total_adj_fitness = 0
        for member in s:
            no_of_members += 1
            total_adj_fitness += member.adjusted_fitness
        avg_adjusted_fitness.append(total_adj_fitness / no_of_members)
    # print("AVERAGE ADJUSTED FITNESS: ", avg_adjusted_fitness)

    allowed_offspring_list = []
    count = 0

    for s in species:
        allowed_offspring_list.append(round((avg_adjusted_fitness[count] / global_avg_adjusted_fitness) * len(s)))
        # print("avg_adjusted_fitness[count]: ",avg_adjusted_fitness[count], "  LENGTH OF SPECIES:", len(s))
        count += 1

    # print("ALLOWED OFFSPRING: ", allowed_offspring_list)
    return allowed_offspring_list
