from graph_tool.all import Graph, graph_draw
from graph_tool.centrality import pagerank
from graph_tool.clustering import global_clustering, local_clustering
from os import sep
from math import fsum

class Network:

    def __init__(self, nodes_info=None, links_info=None, file_name=None):
        self.g = Graph()

        if nodes_info and links_info:
            self.nodes_info = nodes_info
            self.links_info = links_info
            self.g.vertex_properties["name"] = self.g.new_vertex_property(
                'string')
            self.g.vertex_properties["id"] = self.g.new_vertex_property(
                'int32_t')
            self.g.edge_properties["weight"] = self.g.new_edge_property(
                'int32_t')

            self.create_network()
            self.g.vertex_properties["pagerank"] = pagerank(self.g, weight=self.g.edge_properties["weight"])
            self.g.vertex_properties["degree_centrality"] = self.degree_centrality()

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

            self.add_l(n_loser, n_winner, 16 / weight * 100)

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
        self.g.edge_properties.weight[l] = weight

    def draw(self, output_file, fmt):
        graph_draw(self.g, vertex_text=self.g.vertex_index,
                   output=output_file, fmt=fmt)

    def save_network(self, file_name):
        try:
            new_file_name = '..' + sep + '..' + sep + 'network-graphs' + sep + file_name
            self.g.save(new_file_name, fmt="gt")
        except:
            return False
        return True

    def vp_pagerank(self):
        return self.g.vertex_properties.pagerank

    def vp_degree_cent(self):
        return self.g.vertex_properties.degree_centrality

    def vp_name(self):
        return self.g.vertex_properties.name

    def vp_id(self):
        return self.g.vertex_properties.id

    def ep_weight(self):
        return self.g.edge_properties.weight

    # Calcula as características básicas da rede
    def get_basic_info(self):
        info = {}

        try:
            n_vertices = self.g.num_vertices()
            n_edges = self.g.num_edges()
            density = n_edges / ((n_vertices * (n_vertices - 1)) / 2)
            mean_degree = (2 * n_edges) / n_vertices

            # Cálculo do coeficiente de clusterização "na mão", usando a média dos
            # coeficientes locais calculados pela Graph Tools
            local_cc = local_clustering(self.g)
            clustering_coef = fsum([local_cc[x] for x in self.g.vertices() if local_cc[x] != 0.0])
            clustering_coef /= n_vertices
            
            info["Número de times"] = n_vertices
            info["Número de confrontos"] = n_edges
            info["Densidade"] = density
            info["Grau médio"] = mean_degree
            info["Coeficiente de Clusterização"] = clustering_coef
        except:
            info.clear()

        return info

    def degree_centrality(self):
        degree_centrality = self.g.new_vertex_property('float')

        for v in self.g.vertices():
            degree_centrality[v] = v.in_degree() / (self.g.num_vertices() - 1)
	
        return degree_centrality

    # Calcula a distribuição de graus da rede
    def degree_distribution(self):
        degree_dist = {}

        try:
            for v in self.g.vertices():
                if v.in_degree() not in degree_dist.keys():
                    degree_dist[v.in_degree()] = 1
                else:
                    degree_dist[v.in_degree()] += 1

            for k in degree_dist.keys():
                degree_dist[k] /= self.g.num_vertices()
        except:
            degree_dist.clear()
            
        return degree_dist