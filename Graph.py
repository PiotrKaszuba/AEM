from PRIM import PRIM

class Graph:
    def __init__(self, points, distance_matrix):
        self.points = points
        self._recompute = True
        self._MST_length = 0
        self._candidate_nodes_costs = {}
        self._distance_matrix = distance_matrix

    def appendPoint(self, node):
        self.points.append(node)
        self._recompute = True
        self._MST_length = PRIM(self.points, self._distance_matrix, True)

    def compute_nodes_costs(self, nodes):
        if self._recompute:
            self._candidate_nodes_costs.clear()
            self._candidate_nodes_costs = {
                node: PRIM(
                    list(self.points) + [node],
                    self._distance_matrix,
                    True
                ) - self._MST_length
                for node in nodes}
            self._recompute = False

    def get_min_cost_node(self):
        key = min(self._candidate_nodes_costs, key=self._candidate_nodes_costs.get)
        return key

    def pop_from_candidates(self, node):
        self._candidate_nodes_costs.pop(node)



