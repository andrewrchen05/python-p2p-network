#---------LIBRARIES-------------------------------
import sys
import time
import socket
import tqdm
import os
import subprocess as sp
from re import search
import itertools

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
        #elif stringer.find("192.168.1.") != -1:
         #   self.connect_with_node(stringer, 8005)
        else:
            print("RECEIVED COMPUTATION")
            print(stringer)
            
    def node_disconnect_with_outbound_node(self, node):
        print("node wants to disconnect with oher outbound node: " + node.id)
        
    def node_request_to_stop(self):
        print("node is requested to stop!")

#==================================================
#==================================================
def send_message():
    count = 0
    while True:
        val = input()
        node_1.send_to_nodes(val + "\nMESSAGE " + str(count) + " FROM IP " + local_ip) #THIS SENDS
        count += 1
        time.sleep(1)
        if val == "exit":
            break       
#==================================================
#==================================================
def offload_computation(node):

    # path = os.getcwd() # gets current directory
    # ANDREW: MAKE A TRY STATEMENT HERE
    # IF IT DOESNT EXIST, MAKE IT MAKE A DIRECTORY
    # AND THE PROCEED WITH THE COMPUTATION
    cwd = os.getcwd()
    path = str(cwd) + "\scripts"
    dirListing = os.listdir(path)
    print("DIRECTORY IS FOUND AT " + path)
    jobFiles = []
    myJobs = []
    #node.
    numJobs = 0
    
    if os.path.isdir(path):
        print("Found calculation jobs folder.")
        for item in dirListing:
            if ".py" in item:
                jobFiles.append(item)
                print("LIST OF COMPUTATION TASKS: " + str(item))
        numJobs = len(jobFiles)
        print("There are " + str(numJobs) + " to be completed.")
        start_time = time.time() #START TIME
        for(nod, jobe) in itertools.zip_longest(node.nodes_inbound, jobFiles, fillvalue=-1):
            if(nod == -1):
                #print(nod)
                #print(jobe)
                myJobs.append(item)
                print("MY ITEMS TO CALCULATE: " + str(jobe))
            else:
                print("OFFLOAD ITEMS TO CALCULATE: " + str(jobe))
                file = open(jobe, "r")
                data = str(file.read())
                node.send_to_node(nod, data)
        for meme in myJobs:
            output = sp.getoutput("python " + str(meme))
            print(output)
    else:
        print("No jobs folder found")
    print("--- %s seconds ---" % (time.time() - start_time)) #END TIME
    
#    for f in files:
#        print(type(f))
#        print("Running " + f)
#        call(["python", "../scripts/" + f])

    print("Computation offloaded complete.")
#==================================================
#==================================================
#def discover_peers(node):
#    hostname = socket.gethostname()
#    local_ip = socket.gethostbyname(hostname)
#    for ping in range(1,200):
#        try
#==================================================
#==================================================
def menu(node):
    print("************Welcome to X**************")
    #print()
    while True:
        choice = input("""
                        A: Check number of connected nodes
                        B: Send message
                        C: Offload computation
                        D: Discover Peers
                        E: Exit
                        Please enter your choice: """)

        if choice == "A" or choice =="a":
            node.delete_closed_connections()
            node.print_connections()
        elif choice == "B" or choice =="b":
            send_message()
        elif choice == "C" or choice =="c":
            offload_computation(node)
        #elif choice=="D" or choice=="d":
         #   discover_peers(node)
        elif choice=="E" or choice=="e":
            break
        else:
            print("You must only select a valid option")
            print("Please try again")
            menu(node)                
#==================================================
#==================================================

#---------THIS GETS THE LOCAL IPV4 ADDRESS---------
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
print("This is the LOCAL IP: " + local_ip)
#--------------------------------------------------

#---------THIS CREATES THE NODE--------------------
node_1 = MyOwnPeer2PeerNode(local_ip, 8006)
#--------------------------------------------------

#---------FIND NODES AND THEN CONNECT--------------
# below is a hard coded ip, will add the
# automatic finder here later
#node_1.connect_with_node(local_ip, 8005)
node_1.start()
time.sleep(1)
#node_1.connect_with_node(local_ip, 8005)

#--------------------------------------------------

#---------------STARTS THE MENU--------------------

menu(node_1)
#--------------------------------------------------

node_1.stop()

print('end test')
