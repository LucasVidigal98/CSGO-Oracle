def get_top_rank(network, n_positions=None):
	dic_pagerank = {}	
	
	if not n_positions:
		n_positions = network.g.num_vertices()

	for v in network.g.vertices():
		dic_pagerank[network.vp_name()[v]] = network.vp_pagerank()[v]

	rank = sorted(dic_pagerank.items(), key=lambda kv:(kv[1], kv[0]), reverse=True)
	return rank[:n_positions]