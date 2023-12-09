import os
import sys

from server import *
from utils import *

def main():
    if len(sys.argv) != 6 or sys.argv[1] != 'server' or sys.argv[2] != '-t' or sys.argv[4] != '-i':
        print("Usage: ./main.py server -t <topology-file-name> -i <routing-update-interval>")
        sys.exit(1)

    try:
        path_to_file = os.path.join(os.path.dirname(__file__), "topology", sys.argv[3])
        servers, neighbors = parse_topology_file(path_to_file)

        MY_ID = int(sys.argv[3][0])
        # print(f"ID: {MY_ID}")
        MY_IP = servers[int(sys.argv[3][0])]['ip']
        # print(f"IP: {MY_IP}")
        MY_PORT = servers[int(sys.argv[3][0])]['port']
        # print(f"PORT: {MY_PORT}")
        UPDATE_INTERVAL = int(sys.argv[5])
        # print(f"UPDATE INTERVAL: {UPDATE_INTERVAL}")
        NEIGHBORS = {}
        for (src_id, dest_id), cost in neighbors.items():
            if src_id == MY_ID:
                neighbor_id = dest_id
            elif dest_id == MY_ID:
                neighbor_id = src_id
            else:
                continue
            if neighbor_id in servers:
                NEIGHBORS[neighbor_id] = (servers[neighbor_id]['ip'], servers[neighbor_id]['port'], cost)
        # print(f"NEIGHBORS: {NEIGHBORS}")

        server = Server(MY_ID, MY_IP, MY_PORT, UPDATE_INTERVAL, NEIGHBORS)
        server.run()
        
    except:
        print(f"Invalid command line argument.")

if __name__ == "__main__":
    main()