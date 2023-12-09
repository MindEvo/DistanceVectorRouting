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
        for destination, (next_hop, cost) in neighbor_routing_table.items():
            if destination != self.own_id and destination in self.table:
                total_cost = cost + self.table[sender_id][1]  # Add cost to reach the neighbor

                current_route = self.table[destination]
                is_better_route = total_cost < current_route[1]
                is_same_next_hop = current_route[0] == sender_id

                if is_better_route or is_same_next_hop:
                    self.table[destination] = (sender_id, total_cost)
                    updated = True

        return updated

    def print_table(self):
        print("Routing Table:")
        print("Destination ID | Next Hop ID | Cost")
        print("-----------------------------------")
        for destination, (next_hop, cost) in self.table.items():
            print(f"{destination:<14} | {next_hop:<11} | {cost}")

    def __str__(self):
        return "\n".join([f"Destination: {dest}, Next Hop: {nh}, Cost: {cost}" for dest, (nh, cost) in self.table.items()])

# Example usage
# routing_table = RoutingTable()
# routing_table.update_route(destination="ClientB", next_hop="ClientA", cost=1)
# print(routing_table)