#---------LIBRARIES-------------------------------
import sys
import time
import socket
import tqdm
import os
import subprocess as sp
from re import search

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
#==================================================================================================================
    def send_file_to_nodes(self, data, exclude=[]):
        """ Send a message to all the nodes that are connected with this node. data is a python variable which is
            converted to JSON that is send over to the other node. exclude list gives all the nodes to which this
            data should not be sent."""
        self.message_count_send = self.message_count_send + 1
        for n in self.nodes_inbound:
            if n in exclude:
                self.debug_print("Node send_to_nodes: Excluding node in sending the message")
            else:
                self.send_file_node(n, data)

        for n in self.nodes_outbound:
            if n in exclude:
                self.debug_print("Node send_to_nodes: Excluding node in sending the message")
            else:
                self.send_file_node(n, data)

    def send_file_node(self, n, data):
        """ Send the file to the node n if it exists."""
        self.delete_closed_connections()
        if n in self.nodes_inbound or n in self.nodes_outbound:
            try:
                n.send(f"{filename}{SEPARATOR}{filesize}".encode())

            except Exception as e:
                self.debug_print("Node send_to_node: Error while sending file to the node (" + str(e) + ")")
        else:
            self.debug_print("Node send_to_node: Could not send the file, node is not found!")
#==================================================================================================================
    def outbound_node_connected(self, node):
        print("outbound_node_connected: " + node.id)
        
    def inbound_node_connected(self, node):
        print("inbound_node_connected: " + node.id)
        #sendamessage here if they can connect 

    def inbound_node_disconnected(self, node):
        print("inbound_node_disconnected: " + node.id)

    def outbound_node_disconnected(self, node):
        print("outbound_node_disconnected: " + node.id)

    def node_message(self, node, data): #THIS IS THE SHT FUNCTION THAT GETS THE MSG
        #print("node_message from " + node.id + ": " + (data))
        #print("you got mail" + data)
        #fullstring = "StackAbuse"
        substring = "print"
        stringer = str(data)
        if  stringer.find(substring) != -1:
            print("RECEIVED JOB. CALCULATING AND SENDING BACK RESULT")
            text_file = open("JOB.py", "w")
            n = text_file.write(data)
            text_file.close()        
            output = sp.getoutput('python JOB.py')
            print (output)
            self.send_to_nodes(str(output))
        else:
            print("RECEIVED CHAT. I HAVE FRIENDS?")
            print(stringer)
            
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
node_1 = MyOwnPeer2PeerNode(local_ip, 8005)
#--------------------------------------------------

#---------FIND NODES AND THEN CONNECT--------------
# below is a hard coded ip, will add the
# automatic finder here later
#node_1.connect_with_node("192.168.1.66", 8001)
#--------------------------------------------------

node_1.start()

#try:
#    node_1.connect_with_node("192.168.1.51", 8003)
#except: 
#    print("NOT A NODE")
node_1.connect_with_node(local_ip, 8006)
#node_1.connect_with_node("192.168.1.51", 8003)
#node_1.connect_with_node("192.168.1.66", 8003)
#for ping in range(1,69):
#    address = "192.168.1." + str(ping)
#    print("testing " + address)
#    try:
#        #tn = telnetlib.Telnet(address,PORT,.1)
#        #print("adding " + address + "\n")
##        #LEET.append(Switch(address,"root","","0","0"))
 #       node_1.connect_with_node(address, 8003)
 #   except:
#        print(address + " not found or not a node")
print("Printing Connections" + "\n")
node_1.print_connections();
FORMAT = "utf-8"
SIZE = 1024
#print("Sending bola to node 21" + "\n")
#node_1.send_to_node(node_1.nodes_outbound[0],"bola")
#time.sleep(1)
#count = 1
#node_1.send_file_to_nodes("yoo.txt");
while True:
    val = input("Enter your message: ")
    #node_1.send_to_nodes("\nMESSAGE " + " FROM IP " + local_ip + ": " + val) #THIS SENDS
    file = open(val, "r")
    data = str(file.read())
    #print("THIS IS FILE" + file)
    #print("THIS IS DATA" + data)

    node_1.send_to_nodes(data)
    #node_1.send_to_nodes("REGULAR")
    
    #node_1.send_to_nodes(bytes(data,'utf-8'))
    #try:
    #node_1.send_to_nodes(f'yoo.txt'.encode()) #THIS SENDS
    #print("Printing Connections" + "\n")
    #node_1.print_connections();
    time.sleep(2)
    #count += 1
    #except:
    #print("error, this node no longer exists")

#print("DYLAN SENDING JOBS TO EVERYONE" + "\n")
#for n in node_1.nodes_outbound:
#    node_1.send_to_node(n, f"ariga.py".encode())



node_1.stop()

print('end test')
