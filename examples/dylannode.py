#---------LIBRARIES-------------------------------
import os
import sys
import time
import socket
sys.path.insert(0, '..') # Import the files where the modules are located. This takes current directory
#from MyOwnPeer2PeerNode import MyOwnPeer2PeerNode
from p2pnetwork.node import Node
from subprocess import call
# from os import listdir
# from os.path import isfile, join
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
        print("\nEnter your message: ")
        
    def inbound_node_connected(self, node):
        print("inbound_node_connected: " + node.id)
        print("\nEnter your message: ")

    def inbound_node_disconnected(self, node):
        print("inbound_node_disconnected: " + node.id)

    def outbound_node_disconnected(self, node):
        print("outbound_node_disconnected: " + node.id)

    def node_message(self, node, data):
        print("node_message from " + node.id + ": " + str(data))
        print("\nEnter your message: ")
        
    def node_disconnect_with_outbound_node(self, node):
        print("node wants to disconnect with oher outbound node: " + node.id)
        
    def node_request_to_stop(self):
        print("node is requested to stop!")

def no_connected_nodes():
    print("The number of connected nodes is: x")

def send_message():
    count = 0
    while True:
        val = input()
        node_1.send_to_nodes(val + "\nMESSAGE " + str(count) + " FROM IP " + local_ip) #THIS SENDS
        count += 1
        time.sleep(1)
        if val == "exit":
            break


def offload_computation():

    # path = os.getcwd()   # gets current directory
    path = "../scripts"

    files = os.listdir(path)

    for f in files:
        print(type(f))
        print("Running " + f)
        call(["python", "../scripts/" + f])

    print("Computation offloaded")

def menu(node):
    print("************Welcome to X**************")
    #print()

    choice = input("""
                        A: Check number of connected nodes
                        B: Send message
                        C: Offload computation
                        D: Broadcast
                        E: Exit

                        Please enter your choice: """)

    if choice == "A" or choice =="a":
        node.print_connections()
    elif choice == "B" or choice =="b":
        send_message()
    elif choice == "C" or choice =="c":
        offload_computation()
    elif choice=="D" or choice=="d":
        broadcast()
    elif choice=="E" or choice=="e":
        sys.exit
    else:
        print("You must only select a valid option")
        print("Please try again")
        menu(node)                
#==================================================

#---------THIS GETS THE LOCAL IPV4 ADDRESS---------
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
# socket.setblocking(0) # make sure all data is sent

print("This is the LOCAL IP: " + local_ip)
#--------------------------------------------------

#---------THIS CREATES THE NODE--------------------
node_1 = MyOwnPeer2PeerNode(local_ip, 8001)
#--------------------------------------------------

#---------FIND NODES AND THEN CONNECT--------------
# below is a hard coded ip, will add the
# automatic finder here later
node_1.connect_with_node(local_ip, 8003)
# node_1.connect_with_node("192.168.1.55", 8003)
#--------------------------------------------------

node_1.start()

time.sleep(1)

menu(node_1)
'''
while True:
	val = input()
	node_1.send_to_nodes(val + "\nMESSAGE " + str(count) + " FROM IP " + local_ip) #THIS SENDS
	time.sleep(5)
	if val == "exit":
            break
'''
node_1.stop()

print('end test')
