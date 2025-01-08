import time
from rest_server import RestServer
from status import Status
from config import Config

if __name__ == '__main__':
    config = Config()
    status = Status()
    server = RestServer(config['ip'], config['server_port'], status, config)
    server.start()

    print('Server started')
    while True:
        time.sleep(1)
        with status.lock:
            status.timer.left += 1