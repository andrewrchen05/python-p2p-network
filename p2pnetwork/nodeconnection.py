import socket
import sys
import time
import threading
import random
import hashlib
import json
from io import IOBase

class NodeConnection(threading.Thread):
    """The class NodeConnection is used by the class Node and represent the TCP/IP socket connection with another node. 
       Both inbound (nodes that connect with the server) and outbound (nodes that are connected to) are represented by
       this class. The class contains the client socket and hold the id information of the connecting node. Communication
       is done by this class. When a connecting node sends a message, the message is relayed to the main node (that created
       this NodeConnection in the first place).
       
       Instantiates a new NodeConnection. Do not forget to start the thread. All TCP/IP communication is handled by this 
       connection.
        main_node: The Node class that received a connection.
        sock: The socket that is assiociated with the client connection.
        id: The id of the connected node (at the other side of the TCP/IP connection).
        host: The host/ip of the main node.
        port: The port of the server of the main node."""

    def __init__(self, main_node, sock, id, host, port):
        """Instantiates a new NodeConnection. Do not forget to start the thread. All TCP/IP communication is handled by this connection.
            main_node: The Node class that received a connection.
            sock: The socket that is assiociated with the client connection.
            id: The id of the connected node (at the other side of the TCP/IP connection).
            host: The host/ip of the main node.
            port: The port of the server of the main node."""

        super(NodeConnection, self).__init__()

        self.host = host
        self.port = port
        self.main_node = main_node
        self.sock = sock
        self.terminate_flag = threading.Event()

        # The id of the connected node
        self.id = id

        # End of transmission character for the network streaming messages.
        self.EOT_CHAR = 0x04.to_bytes(1, 'big')

        # Datastore to store additional information concerning the node.
        self.info = {}

        self.main_node.debug_print("NodeConnection.send: Started with client (" + self.id + ") '" + self.host + ":" + str(self.port) + "'")

    def send(self, data, encoding_type='utf-8'):
        """Send the data to the connected node. The data can be pure text (str), dict object (send as json) and bytes object.
           When sending bytes object, it will be using standard socket communication. A end of transmission character 0x04 
           utf-8/ascii will be used to decode the packets ate the other node."""
        # self.sock.setblocking(0)
        if isinstance(data, IOBase):
            print("THIS IS A FILE")
        elif isinstance(data, str):
            self.sock.sendall( data.encode(encoding_type) + self.EOT_CHAR )
            while True:
                data = conn.recv(1024) #expiremental
                if not data:            #expirimental
                    break               #expirimental
            #print("THIS IS A STRING")
        elif isinstance(data, dict):
            try:
                json_data = json.dumps(data)
                json_data = json_data.encode(encoding_type) + self.EOT_CHAR
                self.sock.sendall(json_data)

            except TypeError as type_error:
                self.main_node.debug_print('This dict is invalid')
                self.main_node.debug_print(type_error)

            except Exception as e:
                print('Unexpected Error in send message')
                print(e)
           # print("THIS IS A DICT")
#===========================================================================================
        elif isinstance(data, bytes): #we need to insert the packaging send file here
            #bin_data = data + self.EOT_CHAR
            #self.sock.sendall(bin_data)
            print("FROM ISINSTANCE:" + data)         
            """ Sending the filename to the server. """
            #weenie = str(self.main_node.decode(data))
            #print(weenie)
            #print("THIS IS A BYTES")
#===========================================================================================
        else:
            self.main_node.debug_print('datatype used is not valid plese use str, dict (will be send as json) or bytes')
    # This method should be implemented by yourself! We do not know when the message is
    # correct.
    # def check_message(self, data):
    #         return True

    # Stop the node client. Please make sure you join the thread.
    def stop(self):
        """Terminates the connection and the thread is stopped."""
        self.terminate_flag.set()

    def parse_packet(self, packet):
        """Parse the packet and determines wheter it has been send in str, json or byte format. It returns
           the according data."""
        try:
            packet_decoded = packet.decode('utf-8')

            try:
                return json.loads(packet_decoded)

            except json.decoder.JSONDecodeError:
                return packet_decoded

        except UnicodeDecodeError:
            return packet

    # Required to implement the Thread. This is the main loop of the node client.
    def run(self):
        """The main loop of the thread to handle the connection with the node. Within the
           main loop the thread waits to receive data from the node. If data is received 
           the method node_message will be invoked of the main node to be processed."""
        self.sock.settimeout(10.0)          
        buffer = b'' # Hold the stream that comes in!
        FORMAT = "utf-8"
        SIZE = 1024

        while not self.terminate_flag.is_set():
            #self.main_node.delete_closed_connections() #I added this so no errors for abrutply connected node
            chunk = b''
            #print("A")
            try:
                #print("REEECEIVE")
                chunk = self.sock.recv(4096)
                
            except socket.timeout:
                self.main_node.debug_print("NodeConnection: timeout")

            except Exception as e:
                self.terminate_flag.set()
                self.main_node.debug_print('Unexpected error')
                self.main_node.debug_print(e)

            # BUG: possible buffer overflow when no EOT_CHAR is found => Fix by max buffer count or so?
            if chunk != b'':
                #print("C")
                buffer += chunk
                eot_pos = buffer.find(self.EOT_CHAR)

                while eot_pos > 0:
                    #print("D")
                    packet = buffer[:eot_pos]
                    buffer = buffer[eot_pos + 1:]

                    self.main_node.message_count_recv += 1
                    self.main_node.node_message( self, self.parse_packet(packet) )
                    #print(packet)
                    #self.main_node.node_message( self, self.parse_packet(packet) )
                    #print("E")
                    eot_pos = buffer.find(self.EOT_CHAR)
                    time.sleep(0.01)
            #else: #RIGHT HERE WE NEED TO 
                #print("FOUND BYTESTRING")
                #data = self.recv(SIZE).decode(FORMAT)
                #packet = buffer[:eot_pos]
                #packet_decoded = packet.decode('utf-8')
                #text_file = open("JOB.py", "w")
                #n = text_file.write(packet_decoded)
                #output = str(sp.getoutput('python JOB.py'))
                #print ("RUN PYTHON AND ANSWER IS " + output)
                #self.send_to_node(node, output)
                #text_file.close()
                #time.sleep(0.01)
            #time.sleep(5)
        # IDEA: Invoke (event) a method in main_node so the user is able to send a bye message to the node before it is closed?
            time.sleep(0.01)
        self.sock.settimeout(None)
        self.sock.close()
        self.main_node.debug_print("NodeConnection: Stopped")
        #print("G")

    def set_info(self, key, value):
        self.info[key] = value

    def get_info(self, key):
        return self.info[key]

    def __str__(self):
        return 'NodeConnection: {}:{} <-> {}:{} ({})'.format(self.main_node.host, self.main_node.port, self.host, self.port, self.id)

    def __repr__(self):
        return '<NodeConnection: Node {}:{} <-> Connection {}:{}>'.format(self.main_node.host, self.main_node.port, self.host, self.port)
