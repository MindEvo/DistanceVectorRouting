import socket
import threading
import json
import time
from routingTable import RoutingTable

class Server:
    def __init__(self, my_id, my_ip, my_port, update_interval, neighbors):
        self.id = my_id
        self.ip = my_ip
        self.port = my_port
        self.update_interval = update_interval
        self.routing_table = RoutingTable()
        self.routing_table.id = my_id
        self.neighbors = neighbors
        self.disabled_links = set()
        self.packet_count = 0
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.ip, self.port))
        self.running = True

    def run(self):
        # Start a thread for listening to incoming messages
        threading.Thread(target=self.listen_for_messages, daemon=True).start()

        # Start a thread for periodic routing updates
        threading.Thread(target=self.send_periodic_updates, daemon=True).start()

        # Main thread for handling user commands
        while self.running:
            command = input("> ")
            self.handle_command(command)

    def listen_for_messages(self):
        while self.running:
            try:
                message, addr = self.socket.recvfrom(1024)
                self.process_message(message, addr)
            except socket.error:
                break

    def send_periodic_updates(self):
        while self.running:
            self.send_update_to_neighbors()
            time.sleep(self.update_interval)

    def send_update_to_neighbors(self):
        update_message = json.dumps(self.routing_table.table).encode()
        for neighbor_id, (ip, port) in self.neighbors.items():  
            self.socket.sendto(update_message, (ip, port))

    def process_message(self, message, addr):
        try:
            # Decode the message from JSON
            update = json.loads(message.decode())

            # Extract sender ID and their routing table from the message
            sender_id = update['sender_id']
            neighbor_routing_table = update['routing_table']

            # Update this server's routing table with the received information
            if self.routing_table.update_from_neighbor(sender_id, neighbor_routing_table):
                print(f"Routing table updated from neighbor: {sender_id}")
                # Optionally, further actions such as propagating updates can be added here
            self.packet_count += 1

        except json.JSONDecodeError:
            print("Invalid message format received.")

    def handle_command(self, command):
        parts = command.split()
        if parts[0] == 'update' and len(parts) == 4:
            self.update_link_cost(int(parts[1]), int(parts[2]), parts[3])
        elif parts[0] == 'step':
            self.send_update_to_neighbors()
        elif parts[0] == 'packets':
            self.display_packets()
        elif parts[0] == 'display':
            self.display_routing_table()
        elif parts[0] == 'disable' and len(parts) == 2:
            self.disable_link(int(parts[1]))
        elif parts[0] == 'crash':
            self.crash()
        else:
            print("Unknown command")

    def update_link_cost(self, server_id1, server_id2, new_cost):
        # Check if this server is involved in the update
        if self.id not in [server_id1, server_id2]:
            return

        # Convert new_cost to an appropriate format (integer or infinity)
        if new_cost.lower() == 'inf':
            new_cost = float('inf')
        else:
            try:
                new_cost = int(new_cost)
            except ValueError:
                print("Error: Invalid cost value.")
                return

        # Identify the neighbor's ID and update the cost in the neighbors dictionary
        neighbor_id = server_id2 if self.id == server_id1 else server_id1
        if neighbor_id in self.neighbors:
            self.neighbors[neighbor_id] = new_cost
            print(f"Link cost updated: Server {self.id} to Server {neighbor_id} is now {new_cost}")

        # Update the routing table accordingly
        self.routing_table.update_route(neighbor_id, neighbor_id, new_cost)

        # Optionally, trigger an immediate routing update to neighbors
        self.send_update_to_neighbors()

    def display_packets(self):
        # Display the number of received routing packets
        print(f"Number of routing packets received: {self.packet_count}")


    def display_routing_table(self):
        print(self.routing_table)

    def disable_link(self, server_id):
        # Disable the link to the given server
        if server_id in self.neighbors and server_id not in self.disabled_links:
            # Set the link cost to infinity in the routing table
            self.routing_table.update_route(server_id, None, float('inf'))
            self.disabled_links.add(server_id)
            print(f"Link to server {server_id} has been disabled.")
        else:
            print(f"Error: No direct link to server {server_id} or it's already disabled.")

    def crash(self):
        # Simulate a server crash
        self.running = False
        self.socket.close()