import os
import sys
from server import Server
from utils import *

def main():
    if len(sys.argv) != 6 or sys.argv[1] != 'server' or sys.argv[2] != '-t' or sys.argv[4] != '-i':
        print("Usage: ./main.py server -t <topology-file-name> -i <routing-update-interval>")
        sys.exit(1)

    try:
        path_to_file = os.path.join(os.path.dirname(__file__), "topology", sys.argv[3])
        servers, neighbors = parse_topology_file(path_to_file)
        update_interval = int(sys.argv[5])

        print(servers)
        print(neighbors)

        print(servers[1])

        # MY_ID = 1
        # MY_IP = '127.0.0.1'
        # MY_PORT = 5000
        # UPDATE_INTERVAL = 30  # seconds
        # NEIGHBORS = {
        #     2: ('127.0.0.1', 5001),
        #     3: ('127.0.0.1', 5002)
        # }

        # server = Server(MY_ID, MY_IP, MY_PORT, UPDATE_INTERVAL, NEIGHBORS)
        # server.run()
    except:
        print(f"Invalid command line argument.")

if __name__ == "__main__":
    main()