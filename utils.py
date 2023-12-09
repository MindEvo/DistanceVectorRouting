from server import *

def parse_topology_file(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()

    total_servers = int(lines[0].strip())
    total_neighbors = int(lines[1].strip())

    servers = {}
    neighbors = {}

    # Read server details
    for i in range(2, 2 + total_servers):
        parts = lines[i].split()
        server_id, ip, port = int(parts[0]), parts[1], int(parts[2])
        servers[server_id] = {'ip': ip, 'port': port}

    # Read neighbor links and costs
    for i in range(2 + total_servers, 2 + total_servers + total_neighbors):
        parts = lines[i].split()
        src_id, dest_id = int(parts[0]), int(parts[1])
        cost = parts[2]
        if cost.lower() == 'inf':
            cost = float('inf')
        else:
            cost = int(cost)

        neighbors[(src_id, dest_id)] = cost

    return servers, neighbors
