import json
from threading import RLock

from status_members import Questions, Answers, Tables, Timer


class Status:
    def __init__(self):
        self.lock = RLock()
        self.version = 1
        self.questions = Questions()
        self.answers = Answers()
        self.tables = Tables()
        self.timer = Timer()

    def as_json(self):
        with self.lock:
            data = {
                'version': self.version,
                'question': self.questions.__json__(),
                'answers': self.answers.__json__(),
                'tables': self.tables.__json__(),
                'timer': self.timer.__json__()
            }
            return json.dumps(data)
