from network import Network
from p_calc import get_prob_match_pgr, get_prob_match_degree

n = Network(file_name="IEM-BEIJING-HAIDIAN-2020-31.gt")

confrontos = [("FaZe", "G2"), ("Astralis", "Natus Vincere"), ("Complexity", "BIG"), ("Heroic", "Vitality"),
				("G2", "Natus Vincere"), ("Complexity", "Vitality"), ("Natus Vincere", "Vitality")
			]

print("Page Rank:")
for t1, t2 in confrontos:
    print("\nProbabilidades de vitória em um confronto entre", t1, "e", t2)
    print("\n".join(["\t" + n + ": " + "{:.2f}".format(p) + "%"
                    for n, p in get_prob_match_pgr(t1, t2, n).items()]))

print("\nCentralidade por Grau:")
for t1, t2 in confrontos:
    print("\nProbabilidades de vitória em um confronto entre", t1, "e", t2)
    print("\n".join(["\t" + n + ": " + "{:.2f}".format(p) + "%"
                    for n, p in get_prob_match_degree(t1, t2, n).items()]))