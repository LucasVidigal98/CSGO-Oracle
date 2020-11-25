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
    # n.save_network("Test-Network.gt")
else:
    n = Network(file_name='..' + sep + '..' + sep +
                'network-grahps' + sep + file_name)

print("Times com o maior Page Rank:")
print("\n".join(["\t" + n + ": " + str(pgr)
                 for n, pgr in p_calc.get_top_rank(n, 5)]))
# n.draw()
