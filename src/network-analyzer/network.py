from graph_tool.all import *


class Network:

    def __init__(self, nodes_info, links_info):
        self.g = Graph()
        self.nodes_info = nodes_info
        self.links_info = links_info
        self.nprop_name = self.g.new_vertex_property('string')
        self.nprop_id = self.g.new_vertex_property('int32_t')
        self.lprop_weight = self.g.new_edge_property('int32_t')

    def create_network(self):
        # Add Nodes
        for node in self.nodes_info:
            self.add_n(node)

        # Add Links
        for link in self.links_info:
            n_loser = 0
            n_winner = 0
            loser = link['loser']
            winner = link['winner']
            weight = link['rounds']

            for team_id in self.nprop_id:
                if loser == team_id:
                    break
                n_loser += 1

            for team_id in self.nprop_id:
                if winner == team_id:
                    break
                n_winner += 1

            self.add_l(n_loser, n_winner, weight)

    def add_n(self, node_info):
        n = self.g.add_vertex()
        self.nprop_id[n] = node_info['id']
        self.nprop_name[n] = node_info['Team_Name']

    def add_l(self, loser, winner, weight):
        n1 = self.g.vertex(loser)
        n2 = self.g.vertex(winner)
        l = self.g.add_edge(n1, n2)
        self.lprop_weight[l] = weight

    def draw(self):
        graph_draw(
            self.g, vertex_text=self.g.vertex_index, output="network.pdf")
