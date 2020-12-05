from graph_tool.all import Graph, graph_draw
from graph_tool.centrality import pagerank
from os import sep

class Network:

    def __init__(self, nodes_info=None, links_info=None, file_name=None):
        self.g = Graph()

        if nodes_info and links_info:
            self.nodes_info = nodes_info
            self.links_info = links_info
            self.g.vertex_properties["name"] = self.g.new_vertex_property('string')
            self.g.vertex_properties["id"] = self.g.new_vertex_property('int32_t')
            self.g.edge_properties["weight"] = self.g.new_edge_property('int32_t')

            self.create_network()
            self.g.vertex_properties["pagerank"] = pagerank(self.g)
            #self.normalize_pagerank()

        elif file_name:
            self.load_network(file_name)

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

            for team_id in self.g.vertex_properties.id:
                if loser == team_id:
                    break
                n_loser += 1

            for team_id in self.g.vertex_properties.id:
                if winner == team_id:
                    break
                n_winner += 1

            self.add_l(n_loser, n_winner, weight)

    def load_network(self, file_name):
        new_file_name = '..' + sep + '..' + sep + 'network-graphs' + sep + file_name
        self.g.load(new_file_name, fmt="gt")

    def get_normalized_pagerank(self):
        max_pgr = 0
        for pgr in self.g.vertex_properties.pagerank:
            if pgr > max_pgr:
                max_pgr = pgr

        return [self.g.vertex_properties.pagerank[v] / max_pgr for v in self.g.vertices()]

    def add_n(self, node_info):
        n = self.g.add_vertex()
        self.g.vertex_properties.id[n] = node_info['id']
        self.g.vertex_properties.name[n] = node_info['Team_Name']

    def add_l(self, loser, winner, weight):
        n1 = self.g.vertex(loser)
        n2 = self.g.vertex(winner)
        l = self.g.add_edge(n1, n2)
        self.g.edge_properties.weight[l] = 16 / weight

    def draw(self):
        graph_draw(self.g, vertex_text=self.g.vertex_index, output="network.pdf")

    def save_network(self, file_name):
        new_file_name = '..' + sep + '..' + sep + 'network-graphs' + sep + file_name
        self.g.save(new_file_name, fmt="gt")

    def vp_pagerank(self):
        return self.g.vertex_properties.pagerank

    def vp_name(self):
        return self.g.vertex_properties.name

    def vp_id(self):
        return self.g.vertex_properties.id

    def ep_weight(self):
        return self.g.edge_properties.weight