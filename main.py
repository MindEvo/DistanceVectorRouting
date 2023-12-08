import sys
from server import Server
from utils import parse_topology_file

def main():
    if len(sys.argv) != 5 or sys.argv[1] != 'server' or sys.argv[2] != '-t' or sys.argv[4] != '-i':
        print("Usage: ./main.py server -t <topology-file-name> -i <routing-update-interval>")
        sys.exit(1)

    topology_file_name = sys.argv[3]
    update_interval = int(sys.argv[5])

    configurations = parse_topology_file(topology_file_name)
    server = Server(configurations, update_interval)
    server.run()

if __name__ == "__main__":
    main()
