from network import Network
from p_calc import get_prob_match_pgr, get_prob_match_degree
import pprint

n = Network(file_name="IEM-BEIJING-HAIDIAN-2020-31.gt")

playofs = {
			"Quarter Finals": [("FaZe", "G2"), ("Astralis", "Natus Vincere"),
							("Complexity", "BIG"), ("Heroic", "Vitality")],
			"Semi Finals": [],
			"Grand Final": [],
			"Winner": ""
		}

match = []
for t1, t2 in playofs["Quarter Finals"]:
	prob = get_prob_match_pgr(t1, t2, n)
	
	if prob[t1] > prob[t2]:
		match.append(t1)
	else:
		match.append(t2)

	if len(match) == 2:
		playofs["Semi Finals"].append((match[0], match[1]))
		match.clear()

match.clear()
for t1, t2 in playofs["Semi Finals"]:
	prob = get_prob_match_pgr(t1, t2, n)
	
	if prob[t1] > prob[t2]:
		match.append(t1)
	else:
		match.append(t2)

	if len(match) == 2:
		playofs["Grand Final"].append((match[0], match[1]))
		match.clear()

t1 = playofs["Grand Final"][0][0]
t2 = playofs["Grand Final"][0][1]

prob = get_prob_match_pgr(t1, t2, n)
	
if prob[t1] > prob[t2]:
	playofs["Winner"] = t1
else:
	playofs["Winner"] = t2

pprint.pprint(playofs)