def get_top_rank(network, n_positions=None):
	dic_pagerank = {}	
	
	if not n_positions:
		n_positions = network.g.num_vertices()

	sum_pgr = 0
	for v in network.g.vertices():
		dic_pagerank[network.vp_name()[v]] = {"Page Rank": 0, "Probabilidade": 0}
		dic_pagerank[network.vp_name()[v]]["Page Rank"] = network.vp_pagerank()[v]
		sum_pgr += network.vp_pagerank()[v]

	sum_prob = 0
	for v in network.g.vertices():
		dic_pagerank[network.vp_name()[v]]["Probabilidade"] = (network.vp_pagerank()[v] / sum_pgr) * 100
		sum_prob += dic_pagerank[network.vp_name()[v]]["Probabilidade"]

	rank = sorted(dic_pagerank.items(), key=lambda kv:(kv[1]["Page Rank"], kv[0]), reverse=True)
	return rank[:n_positions]

def get_prob_match(team1_name, team2_name, network):
	prob1 = None
	prob2 = None
	
	for v in network.g.vertices():
		if network.g.vp.name[v] == team1_name:
			prob1 = network.g.vp.pagerank[v]
		elif network.g.vp.name[v] == team2_name:
			prob2 = network.g.vp.pagerank[v]
		
		if prob1 and prob2:
			break

	if prob1 == None:
		print("Time não encontrado: \"" + team1_name + "\"")
		return None
	elif prob2 == None:
		print("Time não encontrado: \"" + team2_name + "\"")
		return None

	sum_prob = prob1 + prob2 
	prob1 = prob1 / sum_prob * 100
	prob2 = prob2 / sum_prob * 100

	return {team1_name: prob1, team2_name: prob2}