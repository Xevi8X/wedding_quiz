import time
from rest_server import RestServer
from status.status import Status, Page
from status.leaderboard import Place
from config import Config

if __name__ == '__main__':
    config = Config()
    status = Status()
    server = RestServer(config['server_ip'], config['server_port'], status, config)
    server.start()

    print('Server started')
    while True:
        time.sleep(1)
        