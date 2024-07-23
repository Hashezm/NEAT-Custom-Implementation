class Node:
    def __init__(self, node_id, node_type):
        self.node_id = node_id
        self.node_type = node_type  # 'input', 'hidden', 'output'
        self.layer = 0
        self.sum_input = 0
        self.sum_output = 0

    def __repr__(self):
        return f"Node(id={self.node_id}, type={self.node_type})"