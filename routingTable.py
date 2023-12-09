class RoutingTable:
    def __init__(self):
        self.table = {}  # Format: {destination: (next_hop, cost)}
        self.id = 99999  # default garbage value

    def update_route(self, destination, next_hop, cost):
        self.table[destination] = (next_hop, cost)

    def remove_route(self, destination):
        if destination in self.table:
            del self.table[destination]

    def get_next_hop(self, destination):
        return self.table.get(destination, (None, float('inf')))[0]

    def update_from_neighbor(self, neighbor_id, neighbor_table):
        updated = False
        for destination, (next_hop, cost) in neighbor_table.items():
            if destination != self.own_id and (destination not in self.table or cost + 1 < self.table[destination][1]):
                self.table[destination] = (neighbor_id, cost + 1)
                updated = True
        return updated

    def __str__(self):
        return "\n".join([f"Destination: {dest}, Next Hop: {nh}, Cost: {cost}" for dest, (nh, cost) in self.table.items()])

# Example usage
# routing_table = RoutingTable()
# routing_table.update_route(destination="ClientB", next_hop="ClientA", cost=1)
# print(routing_table)