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
        self.neighbors = neighbors  # Format: {neighbor_id: (ip, port)}
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
        # Process incoming message (either a routing update or a user message)
        pass

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
        # Update the link cost in the routing table
        pass

    def display_packets(self):
        # Display the number of received routing packets
        pass

    def display_routing_table(self):
        print(self.routing_table)

    def disable_link(self, server_id):
        # Disable the link to the given server
        pass

    def crash(self):
        # Simulate a server crash
        self.running = False
        self.socket.close()

# Example of creating a server instance
if __name__ == "__main__":
    MY_ID = 1
    MY_IP = '127.0.0.1'
    MY_PORT = 5000
    UPDATE_INTERVAL = 30  # seconds
    NEIGHBORS = {
        2: ('127.0.0.1', 5001),
        3: ('127.0.0.1', 5002)
    }

    server = Server(MY_ID, MY_IP, MY_PORT, UPDATE_INTERVAL, NEIGHBORS)
    server.run()