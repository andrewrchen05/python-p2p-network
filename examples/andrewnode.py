#---------LIBRARIES-------------------------------
import sys
import time
import socket
sys.path.insert(0, '..') # Import the files where the modules are located. This takes current directory
#from MyOwnPeer2PeerNode import MyOwnPeer2PeerNode
from p2pnetwork.node import Node
#--------------------------------------------------

#========NODE CLASS================================
class MyOwnPeer2PeerNode (Node):
    # Python class constructor
    def __init__(self, host, port):
        super(MyOwnPeer2PeerNode, self).__init__(host, port, None)
        print("Node IP4: " + host + " started on PORT: " + str(port))
# all the methods below are called when things happen in the network.
# implement your network node behavior to create the required functionality.
    def outbound_node_connected(self, node):
        print("outbound_node_connected: " + node.id)
        
    def inbound_node_connected(self, node):
        print("inbound_node_connected: " + node.id)

    def inbound_node_disconnected(self, node):
        print("inbound_node_disconnected: " + node.id)

    def outbound_node_disconnected(self, node):
        print("outbound_node_disconnected: " + node.id)

    def node_message(self, node, data):
        print("node_message from " + node.id + ": " + str(data))
        
    def node_disconnect_with_outbound_node(self, node):
        print("node wants to disconnect with oher outbound node: " + node.id)
        
    def node_request_to_stop(self):
        print("node is requested to stop!")
#==================================================

#---------THIS GETS THE LOCAL IPV4 ADDRESS---------
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
print("This is the LOCAL IP: " + local_ip)
#--------------------------------------------------

#---------THIS CREATES THE NODE--------------------
node_1 = MyOwnPeer2PeerNode(local_ip, 8003)
#--------------------------------------------------

#---------FIND NODES AND THEN CONNECT--------------
# below is a hard coded ip, will add the
# automatic finder here later
# node_1.connect_with_node(local_ip, 8001)
#--------------------------------------------------
time.sleep(1)

node_1.start()

# time.sleep(1)

# node_1.send_to_nodes("MESSAGE FROM IP " + local_ip + ": SEND NUDES") #THIS SENDS

# time.sleep(1)

time.sleep(5000)

node_1.stop()

print('end test')
