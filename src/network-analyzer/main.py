import sys
import p_calc
from io_op import read_json
from network import Network
from os import sep

if len(sys.argv) < 3 or len(sys.argv) > 3:
    print('Parâmetros errados: python main.py file_name load_option')
    exit(1)

file_name = sys.argv[1]
option = sys.argv[2]
n = ''

if int(option) == 0:
    nodes_info, links_info = read_json(str(file_name))
    n = Network(nodes_info=nodes_info, links_info=links_info)

    if (n.save_network(file_name.replace("json", "gt"))):
        print("Rede salva com sucesso!")
    else:
        print("Erro ao salvar a rede!")

else:
    n = Network(file_name=file_name)
    # n = Network(file_name='..' + sep + '..' + sep + 'network-grahps' + sep + file_name)

print("Rede:", file_name.replace(".json", ""))
print("Número de times:", n.g.num_vertices(), "\n")

# print("Times com mais chances de ganhar:")
# print("\n".join(["\t" + n + " - PgR: " + str(v["Page Rank"]) +
#                 ", Prob.: " + str(v["Probabilidade"])
#                  for n, v in p_calc.get_top_rank(n)]))

confrontos = [("Furia", "Virtus.pro"), ("MIBR", "Liquid"), ("Heroic", "mousesports"), ("Complexity", "Cloud9")]
for t1, t2 in confrontos:
    print("\nProbabilidades de vitória em um confronto entre", t1, "e", t2)
    print("\n".join(["\t" + n + ": " + "{:.2f}".format(p) + "%"
                    for n, p in p_calc.get_prob_match(t1, t2, n).items()]))
# n.draw()