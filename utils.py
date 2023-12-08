from server import *

def parse_topology_file(file_name):
    configurations = []
    with open(file_name, 'r') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.strip().split()
            print(parts)
            if len(parts) == 3:
                id, ip, port = int(parts[0]), parts[1], int(parts[2])
                configurations.append((id, ip, port))
    return configurations