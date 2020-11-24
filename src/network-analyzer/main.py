import sys
import p_calc
from io_op import read_json
from network import Network

#file_name = sys.argv[1]
#nodes_info, links_info = read_json(str(file_name))
#n = Network(nodes_info, links_info)
n = Network(file_name="Test-Network.gt")
print("Times com o maior Page Rank:")
print("\n".join(["\t" + n + ": " + str(pgr) for n, pgr in p_calc.get_top_rank(n, 5)]))
#n.draw()
#n.save_network("Test-Network.gt")
