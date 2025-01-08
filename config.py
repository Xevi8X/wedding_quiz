class Config:
    def __init__(self):
        self.config = {
            'server_ip': '',
            'server_port': 1234,
            'root_html': 'assets/index.html'
        }

    def __getitem__(self, key):
        return self.config[key]