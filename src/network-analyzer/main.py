import sys
from io_op import read_json
from network import Network

file_name = sys.argv[1]
nodes_info, links_info = read_json(str(file_name))
n = Network(nodes_info, links_info)
#n = Network(file_name="Test-Network.gt")
#n.draw()
#n.save_network("Test-Network.gt")
