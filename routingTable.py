class RoutingTable:
    def __init__(self):
        self.table = {}  # Format: {destination: (next_hop, cost)}
        self.own_id = 99999  # default garbage value

    def update_route(self, destination, next_hop, cost):
        self.table[destination] = (next_hop, cost)

    def remove_route(self, destination):
        if destination in self.table:
            del self.table[destination]

    def get_next_hop(self, destination):
        return self.table.get(destination, (None, float('inf')))[0]

    def update_from_neighbor(self, sender_id, neighbor_routing_table):
        updated = False
        if sender_id not in self.table:
            return False  # Sender not in routing table, so no update is possible
        cost_to_sender = self.table[sender_id][1]
        for destination, (next_hop, cost) in neighbor_routing_table.items():
            destination = int(destination)
            if destination == self.own_id:
                continue  # Skip self
            total_cost = cost + cost_to_sender
            # Check if this route should be updated
            if destination in self.table:
                current_route = self.table[destination]
                current_cost = current_route[1]
                if total_cost < current_cost:
                    self.table[destination] = (sender_id, total_cost)
                    updated = True
                # Handle the case where the neighbor's route to the destination is now unreachable
                elif current_route[0] == sender_id and cost == float('inf'):
                    self.table[destination] = (None, float('inf'))
                    updated = True
            # If the destination is not in the table, add it
            else:
                self.table[destination] = (sender_id, total_cost)
                updated = True
        return updated  

    def print_table(self):
        print("Routing Table:")
        print("Destination ID | Next Hop ID | Cost")
        print("-----------------------------------")
        for destination, (next_hop, cost) in self.table.items():
            next_hop_str = str(next_hop) if next_hop is not None else 'None'
            cost_str = str(cost) if cost != float('inf') else 'inf'
            print(f"{destination:<14} | {next_hop_str:<11} | {cost_str}")

    def __str__(self):
        return "\n".join([f"Destination: {dest}, Next Hop: {nh}, Cost: {cost}" for dest, (nh, cost) in self.table.items()])

# Example usage
# routing_table = RoutingTable()
# routing_table.update_route(destination="ClientB", next_hop="ClientA", cost=1)
# print(routing_table)