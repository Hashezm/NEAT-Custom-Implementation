class ConnectionGene:
    def __init__(self, in_node, out_node, weight, enabled, innovation_number):
        self.in_node = in_node
        self.out_node = out_node
        self.weight = weight
        self.enabled = enabled
        self.innovation_number = innovation_number

    def __repr__(self):
        return (
            f"ConnectionGene(in={self.in_node}, out={self.out_node}, " f"weight={self.weight}, enabled={self.enabled}, innovation={self.innovation_number})")
